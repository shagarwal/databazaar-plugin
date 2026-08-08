"""Eval harness for the databazaar skill.

Each case lives in `evals/cases/*.yaml` and is one of:
  - acquire — feed a request, score the output against expectations
  - aggregate — feed N inputs, score merged result
  - prepare — feed proprietary file, score normalization + datacard
  - refusal — feed a request that should be refused

Run:
    python scripts/eval.py            # run all cases
    python scripts/eval.py --case 01  # run one
    python scripts/eval.py --tag refusal

Every run writes a record to `evals/runs/<ISO>-<git-sha>.json` so iteration
history is auditable. Intermediate artifacts (the actual output files
produced by the skill) live under `evals/runs/<run>/<case>/`.
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys, traceback, hashlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVAL_DIR = ROOT / "evals"
CASES_DIR = EVAL_DIR / "cases"
RUNS_DIR = EVAL_DIR / "runs"


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except Exception:
        return "nogit"


def _load_yaml(path: Path) -> dict:
    """Tiny YAML loader — avoid PyYAML dep for v0. Only supports flat
    key: value + simple lists. For complex cases switch to PyYAML later."""
    try:
        import yaml  # type: ignore
        return yaml.safe_load(path.read_text())
    except ImportError:
        pass
    out, current_list_key = {}, None
    for line in path.read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - "):
            out.setdefault(current_list_key, []).append(line[4:].strip())
        elif ":" in line:
            k, v = line.split(":", 1)
            v = v.strip()
            if v == "":
                current_list_key = k.strip()
                out[current_list_key] = []
            else:
                out[k.strip()] = v.strip('"').strip("'")
                current_list_key = None
    return out


def load_cases(filter_id: str = None, filter_tag: str = None) -> list[dict]:
    cases = []
    for p in sorted(CASES_DIR.glob("*.yaml")):
        c = _load_yaml(p)
        c["_path"] = str(p)
        c["_id"] = p.stem
        if filter_id and filter_id not in p.stem:
            continue
        if filter_tag and filter_tag not in c.get("tags", ""):
            continue
        cases.append(c)
    return cases


# --- scoring ---------------------------------------------------------------

def score_output(case: dict, out_dir: Path) -> dict:
    """Apply per-case checks. Returns {passed: [...], failed: [...], score}."""
    checks = []
    expected = case.get("expects", {})

    # Required output files
    for f in ["data.csv", "schema.json", "datacard.md", "provenance.json",
              "sample.csv", "pii_report.json", "listing_suggestion.json"]:
        checks.append({
            "name": f"output_file:{f}",
            "passed": (out_dir / f).exists(),
        })

    # Min rows
    if "min_rows" in expected:
        try:
            data = (out_dir / "data.csv").read_text().splitlines()
            rows = max(0, len(data) - 1)
            checks.append({
                "name": f"min_rows>={expected['min_rows']}",
                "passed": rows >= int(expected["min_rows"]),
                "actual": rows,
            })
        except FileNotFoundError:
            checks.append({"name": "min_rows", "passed": False, "actual": 0})

    # Datacard rubric — 7 sections
    if (out_dir / "datacard.md").exists():
        dc = (out_dir / "datacard.md").read_text()
        for section in ["Overview", "Schema", "Sources", "Methodology",
                        "Known gaps", "Intended use", "Provenance"]:
            checks.append({
                "name": f"datacard_section:{section}",
                "passed": section in dc,
            })
        checks.append({
            "name": "marketing_footer",
            "passed": "databazaar.io" in dc and "Built with the `databazaar` skill" in dc,
        })

    # Provenance: every row must have source
    if (out_dir / "provenance.json").exists():
        prov = json.loads((out_dir / "provenance.json").read_text())
        rows = prov.get("rows", [])
        all_sourced = all(r.get("source") and r.get("source") != "unknown" for r in rows)
        checks.append({
            "name": "provenance_complete",
            "passed": all_sourced if rows else True,
        })

    # PII gate
    if expected.get("pii_blocked") is not None:
        pii = json.loads((out_dir / "pii_report.json").read_text())
        checks.append({
            "name": "pii_block_correct",
            "passed": pii.get("blocked", False) == expected["pii_blocked"],
        })

    passed = [c for c in checks if c["passed"]]
    failed = [c for c in checks if not c["passed"]]
    return {
        "checks": checks,
        "passed": len(passed),
        "failed": len(failed),
        "score": len(passed) / max(1, len(checks)),
    }


def score_refusal(case: dict, stderr: str, exit_code: int) -> dict:
    expected_in = case.get("expects", {}).get("stderr_contains", "")
    return {
        "checks": [
            {"name": "non_zero_exit", "passed": exit_code != 0},
            {"name": "stderr_match", "passed": expected_in in stderr if expected_in else True},
        ],
        "score": 1.0 if (exit_code != 0 and (not expected_in or expected_in in stderr)) else 0.0,
    }


# --- runner ---------------------------------------------------------------

def run_case(case: dict, run_dir: Path) -> dict:
    case_dir = run_dir / case["_id"]
    case_dir.mkdir(parents=True, exist_ok=True)
    mode = case.get("mode", "acquire")

    cmd = ["python", str(ROOT / "scripts" / "build.py"), mode]
    if mode == "acquire":
        cmd += ["--request", case["request"], "--out", str(case_dir)]
    elif mode == "prepare":
        input_path = case["input"]
        if not os.path.isabs(input_path):
            input_path = str(ROOT / input_path)
        cmd += ["--input", input_path, "--out", str(case_dir)]
    elif mode == "aggregate":
        inputs = case.get("inputs", [])
        inputs = [str(ROOT / i) if not os.path.isabs(i) else i for i in inputs]
        cmd += ["--inputs", *inputs, "--on", case.get("on", "id"), "--out", str(case_dir)]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        stdout, stderr, rc = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired:
        stdout, stderr, rc = "", "TIMEOUT", -1
    except Exception:
        stdout, stderr, rc = "", traceback.format_exc(), -1

    if case.get("kind") == "refusal":
        score = score_refusal(case, stderr, rc)
    else:
        score = score_output(case, case_dir) if rc == 0 else {
            "checks": [{"name": "exit_code", "passed": False, "stderr": stderr[-500:]}],
            "score": 0.0,
        }

    return {
        "case_id": case["_id"],
        "mode": mode,
        "exit_code": rc,
        "stdout_tail": stdout[-1000:],
        "stderr_tail": stderr[-1000:],
        **score,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case")
    ap.add_argument("--tag")
    args = ap.parse_args()

    cases = load_cases(args.case, args.tag)
    if not cases:
        print("No cases matched.", file=sys.stderr)
        sys.exit(1)

    run_id = f"{_ts()}-{_git_sha()}"
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    results = [run_case(c, run_dir) for c in cases]

    # Tally results, segregating "expected_fail" cases
    actual_pass, actual_fail, expected_fail_pass, expected_fail_fail = 0, 0, 0, 0
    for c, r in zip(cases, results):
        passed = r.get("score", 0) >= 0.9
        is_xfail = str(c.get("expected_fail", "")).lower() == "true"
        if is_xfail:
            if passed:
                expected_fail_pass += 1   # surprise — flag for review
            else:
                expected_fail_fail += 1   # known gap, on-track
        else:
            if passed:
                actual_pass += 1
            else:
                actual_fail += 1

    summary = {
        "run_id": run_id,
        "started_at": _ts(),
        "case_count": len(cases),
        "passed_cases": actual_pass + expected_fail_pass,
        "graded": {
            "passed": actual_pass,
            "failed": actual_fail,
            "total": actual_pass + actual_fail,
        },
        "expected_failures": {
            "still_failing_as_expected": expected_fail_fail,
            "now_passing_review_needed": expected_fail_pass,
        },
        "mean_score": sum(r.get("score", 0) for r in results) / len(results),
        "graded_pass_rate": actual_pass / max(1, (actual_pass + actual_fail)),
        "results": results,
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2))

    print(f"\n=== run {run_id} ===")
    for c, r in zip(cases, results):
        is_xfail = str(c.get("expected_fail", "")).lower() == "true"
        passed = r.get("score", 0) >= 0.9
        if is_xfail:
            flag = "XPASS" if passed else "xfail"
        else:
            flag = "PASS " if passed else "FAIL "
        print(f"  [{flag}] {r['case_id']:50s} score={r.get('score',0):.2f}")
    print()
    print(f"  graded:           {actual_pass}/{actual_pass + actual_fail} pass "
          f"({summary['graded_pass_rate']:.1%})")
    print(f"  expected-fail:    {expected_fail_fail} still failing (ok), "
          f"{expected_fail_pass} now passing (review)")
    print(f"  mean score:       {summary['mean_score']:.2f}")
    print(f"  artifacts:        {run_dir}")


if __name__ == "__main__":
    main()
