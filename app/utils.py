import re, uuid
PII_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PII_SSN   = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
def redact_pii(s: str) -> str:
    s = PII_EMAIL.sub("[EMAIL]", s)
    s = PII_SSN.sub("[SSN]", s)
    return s
def request_id() -> str:
    return str(uuid.uuid4())
