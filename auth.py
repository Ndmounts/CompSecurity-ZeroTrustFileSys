import json
import fnmatch

with open("policy.json") as f:
    POLICY = json.load(f)

def user_from_cert(peercert) -> str:
    """
    peercert comes from ssl.SSLSocket.getpeercert()
    It's already parsed as a dict.
    We'll grab the commonName (CN) from the subject.
    """
    if not peercert:
        raise ValueError("No client certificate presented")

    subject = peercert.get('subject', ())
    # subject is a tuple of tuples like: ((('commonName', 'nick'),),)
    cn = None
    for tup in subject:
        for key, value in tup:
            if key == 'commonName':
                cn = value
                break
    if not cn:
        raise ValueError("Client cert has no commonName")
    return f"CN={cn}"

def policy_allows(user: str, op: str, path: str) -> bool:
    user_rules = POLICY.get(user)
    if not user_rules:
        return False

    allowed_patterns = user_rules.get(op)
    if not allowed_patterns:
        return False

    # try patterns like "/public/*" or "*"
    for pat in allowed_patterns:
        if pat == "*":
            return True
        if fnmatch.fnmatch(path, pat):
            return True
    return False
