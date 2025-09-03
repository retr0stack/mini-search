from __future__ import annotations
from pathlib import Path
from typing import Dict, Tuple
import pickle

from .types import IndexMeta, IndexType
from .tokenize import tokenize

def build_index(folder_path: Path) -> Tuple[IndexType, IndexMeta]:
    if not folder_path.is_dir():
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    files = tuple(sorted(f.name for f in folder_path.iterdir() if f.suffix.lower() == ".txt"))
    if not files:
        raise FileNotFoundError(f"No .txt files in folder: {folder_path}")

    index: IndexType = {}
    doc_len: Dict[str, int] = {}
    doc_raw: Dict[str, str] = {}

    for fname in files:
        p = folder_path / fname
        raw = p.read_text(encoding="utf-8", errors="ignore")
        doc_raw[fname] = raw
        toks = tokenize(raw)
        doc_len[fname] = len(toks)
        for i, term in enumerate(toks):
            index.setdefault(term, {}).setdefault(fname, []).append(i)

    meta = IndexMeta(files=files, doc_len=doc_len, doc_raw=doc_raw, folder_path=str(folder_path))
    return index, meta

def save_index(index: IndexType, meta: IndexMeta, out_path: Path) -> None:
    out_path.write_bytes(pickle.dumps({"index": index, "meta": meta}))

def load_index(pkl_path: Path) -> Tuple[IndexType, IndexMeta]:
    if not pkl_path.is_file():
        raise FileNotFoundError(f"Index file not found: {pkl_path}")
    payload = pickle.loads(pkl_path.read_bytes())
    return payload["index"], payload["meta"]
