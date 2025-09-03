import re
from typing import List, Set

TOKEN = re.compile(r"\w+", flags=re.UNICODE)
STOP: Set[str] = {
    "a","an","the","and","or","is","are","was","were","be","been","being",
    "to","of","in","on","for","with","as","by","at","from","that","this",
    "it","its","into","about","up","down","over","under"
}

def tokenize(text: str) -> List[str]:
    text = text.lower()
    return [t for t in TOKEN.findall(text) if t not in STOP]

def tokenize_phrase(text: str) -> List[str]:
    return TOKEN.findall(text.lower())
