from typing import List, Sequence, Set
from .types import IndexType
from .tokenize import tokenize_phrase

def positional_merge(a: Sequence[int], b: Sequence[int], gap: int = 1) -> List[int]:
    i, j = 0, 0
    out: List[int] = []
    while i < len(a) and j < len(b):
        diff = b[j] - a[i]
        if diff == gap:
            out.append(b[j]); i += 1; j += 1
        elif diff > gap:
            i += 1
        else:
            j += 1
    return out

def phrase_in_doc(index: IndexType, terms: Sequence[str], doc: str) -> bool:
    for t in terms:
        if doc not in index.get(t, {}):
            return False
    positions = index[terms[0]][doc]
    for t in terms[1:]:
        positions = positional_merge(positions, index[t][doc], gap=1)
        if not positions:
            return False
    return True

def phrase_docs(index: IndexType, phrase: str) -> Set[str]:
    terms = tokenize_phrase(phrase)
    if not terms:
        return set()
    cand = set(index.get(terms[0], {}).keys())
    for t in terms[1:]:
        cand &= set(index.get(t, {}).keys())
        if not cand:
            return set()
    return {doc for doc in cand if phrase_in_doc(index, terms, doc)}
