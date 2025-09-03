import re
from typing import Set, Tuple

def make_snippet(text: str, terms: Set[str], window: int = 50) -> str:
    if not text:
        return ""
    lower = text.lower()
    hit: Tuple[int, int] | None = None
    for term in sorted(terms, key=len, reverse=True):
        i = lower.find(term.lower())
        if i != -1:
            hit = (i, i + len(term))
            break
    if not hit:
        return (text[:120] + "...") if len(text) > 120 else text
    start = max(0, hit[0] - window)
    end = min(len(text), hit[1] + window)
    snippet = text[start:end]
    for term in sorted(terms, key=len, reverse=True):
        snippet = re.sub(fr"(?i)\b({re.escape(term)})\b", r"[\1]", snippet)
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet = snippet + "..."
    return snippet
