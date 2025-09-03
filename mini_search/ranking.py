import math
from collections import Counter, defaultdict
from typing import Dict, Iterable, MutableMapping, Set
from .types import IndexType, IndexMeta

def _idf(index: IndexType, N: int, term: str) -> float:
    df = len(index.get(term, {}))
    if df == 0:
        return 0.0
    return math.log(1 + (N - df + 0.5) / (df + 0.5))

def bm25_scores(
    index: IndexType,
    meta: IndexMeta,
    query_terms: Iterable[str],
    candidates: Set[str] | None = None,
    k1: float = 1.5,
    b: float = 0.75,
) -> Dict[str, float]:
    terms = list(query_terms)
    if not terms:
        return {}
    files = meta.files
    doc_len = meta.doc_len
    N = len(files)
    avgdl = (sum(doc_len.values()) / N) if N else 0.0
    q_counts = Counter(terms)
    scores: MutableMapping[str, float] = defaultdict(float)
    if candidates is None:
        cand: Set[str] = set()
        for t in q_counts:
            cand |= set(index.get(t, {}).keys())
        candidates = cand if cand else set(files)
    for term in q_counts:
        postings = index.get(term)
        if not postings:
            continue
        w_idf = _idf(index, N, term)
        for doc in candidates:
            tf = len(postings.get(doc, []))
            if tf == 0:
                continue
            dl = doc_len[doc]
            denom = tf + k1 * (1 - b + b * (dl / (avgdl or 1.0)))
            score = w_idf * (tf * (k1 + 1)) / (denom if denom else 1.0)
            scores[doc] += score
    return dict(scores)
