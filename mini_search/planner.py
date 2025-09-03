import re
from typing import List, Set, Tuple
from .types import IndexType, IndexMeta
from .tokenize import tokenize, tokenize_phrase
from .phrase import phrase_docs
from .ranking import bm25_scores
from .snippets import make_snippet

def query_candidates(index: IndexType, meta: IndexMeta, request: str) -> Tuple[Set[str], List[str], List[str]]:
    phrases = re.findall(r'"([^"]+)"', request)
    rest = re.sub(r'"[^"]+"', " ", request)
    terms = tokenize(rest)
    cand: Set[str] = set(meta.files)
    for ph in phrases:
        cand &= phrase_docs(index, ph)
        if not cand:
            return set(), terms, phrases
    for t in terms:
        cand &= set(index.get(t, {}).keys())
        if not cand:
            return set(), terms, phrases
    return cand, terms, phrases

def search(index: IndexType, meta: IndexMeta, request: str, top_k: int = 10):
    cand, terms, phrases = query_candidates(index, meta, request)
    if not terms and cand:
        out = []
        phrase_terms = set(sum((tokenize_phrase(p) for p in phrases), []))
        for doc in sorted(cand):
            out.append((doc, None, make_snippet(meta.doc_raw[doc], phrase_terms)))
        return out
    scores = bm25_scores(index, meta, terms, candidates=cand if cand else None)
    if not scores:
        return []
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    all_query_terms = set(terms) | set(sum((tokenize_phrase(p) for p in phrases), []))
    results = []
    for doc, score in ranked:
        results.append((doc, score, make_snippet(meta.doc_raw[doc], all_query_terms)))
    return results
