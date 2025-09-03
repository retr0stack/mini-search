from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Mapping, Tuple

IndexType = Dict[str, Dict[str, List[int]]]

@dataclass(frozen=True)
class IndexMeta:
    files: Tuple[str, ...]
    doc_len: Mapping[str, int]
    doc_raw: Mapping[str, str]
    folder_path: str
