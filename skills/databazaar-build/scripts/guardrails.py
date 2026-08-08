"""Pre-flight refusal checks for acquire/aggregate/prepare requests.

Returns (allowed: bool, reason: str). The orchestrator exits with
non-zero + writes `reason` to stderr if not allowed.

Philosophy: the skill does not maintain host-level blocklists. The owner
decides which sources are appropriate to acquire from, and that decision is
captured by the opt-in scrape gate (--allow-scrape + --tos-ack), which is
recorded in provenance.json for audit. The only hard refusal is PII
aggregation about private individuals (which is about *what* the dataset
contains, not where it came from).
"""
from __future__ import annotations
import re
from urllib.parse import urlparse

# Personal-data nouns that, in aggregate, are PII.
_PII_NOUNS = [
    "email", "emails", "email address", "email addresses",
    "phone", "phones", "phone number", "phone numbers",
    "home address", "home addresses", "addresses of",
    "ssn", "social security",
    "salary", "salaries of",
    "medical", "diagnoses",
    "credit card", "bank account",
    "dob", "date of birth", "dates of birth",
]

# Group-of-private-individuals patterns ("emails of all dentists in SF").
_GROUP_TARGETING = re.compile(
    r"\b(of|for)\s+(all\s+|every\s+)?[a-z\- ]{3,40}\b",
    re.IGNORECASE,
)


def _mentions_pii(text: str) -> bool:
    t = text.lower()
    return any(noun in t for noun in _PII_NOUNS)


def check_request(request: str, *, allow_scrape: bool = False,
                  tos_ack: str | None = None) -> tuple[bool, str]:
    """Returns (allowed, reason).

    allow_scrape + tos_ack are required to enable arbitrary web acquisition.
    Without them, only databazaar.io + the public-API adapters in
    references/sources.md are used. The owner is responsible for ToS
    compliance on any site the skill is pointed at; that responsibility is
    captured by the tos_ack string and recorded in provenance.json.
    """
    if _mentions_pii(request) and _GROUP_TARGETING.search(request):
        return False, (
            "REFUSED: PII aggregation about private individuals is not "
            "allowed. See references/pii-patterns.md. Public-record facts "
            "about public figures (executives, elected officials) in their "
            "professional capacity may be fine — rephrase if that's the "
            "actual intent."
        )

    # Web acquisition is opt-in. If the request mentions an explicit URL or
    # the words "scrape"/"crawl"/"fetch from", require allow_scrape + tos_ack.
    looks_like_scrape = (
        bool(re.search(r"https?://", request))
        or bool(re.search(r"\b(scrape|crawl|fetch from|extract from)\b",
                          request, re.I))
    )
    if looks_like_scrape and not allow_scrape:
        return False, (
            "REFUSED: web acquisition is opt-in. To allow scraping, pass "
            "--allow-scrape AND --tos-ack \"<one-line acknowledgment that "
            "you have the right to acquire and resell this data>\". "
            "Acknowledgment is recorded in provenance.json."
        )
    if looks_like_scrape and allow_scrape and not (tos_ack and tos_ack.strip()):
        return False, (
            "REFUSED: --allow-scrape requires --tos-ack with a non-empty "
            "acknowledgment string. This is recorded in provenance.json."
        )

    return True, ""
