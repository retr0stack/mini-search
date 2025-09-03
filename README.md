# Mini Search Engine

Search engine in Python that builds a **positional inverted index** from `.txt` files and supports:

- ✅ **Phrase search** (e.g., `"machine learning"`)
- ✅ **BM25 ranking** for relevance
- ✅ **Snippet generation** with highlighted query terms
- ✅ **Command-line interface (CLI)** powered by **Typer**

---

## 🚀 Features
- **Indexing**: Parse and normalize text, remove stopwords, and build a positional inverted index.
- **Phrase Search**: Supports exact multi-word phrases using a two-pointer merge algorithm.
- **Ranking**: Implements [BM25](https://en.wikipedia.org/wiki/Okapi_BM25) scoring for relevant document ranking.
- **Snippets**: Extracts text fragments around matches and highlights query terms.
- **CLI**: Easy-to-use interface with two commands: `index` and `query`.

---

## 📂 Project Structure
```
Mini Search Engine/
  mini_search/
    __init__.py
    cli.py
    indexing.py
    planner.py
    phrase.py
    ranking.py
    snippets.py
    tokenize.py
    types.py
  documents/         # Example .txt documents
  README.md
```

---

## ⚙️ Installation
Clone the repo and install dependencies:

```bash
pip install typer[all]
```

---

## 📥 Index Documents
Put `.txt` files into the `documents/` folder.  
Then build the index:

```bash
python -m mini_search.cli index documents/ -o index.pkl
```

---

## 🔎 Search
Run a query:

```bash
python -m mini_search.cli query python -i index.pkl
```

Phrase queries are supported:

```bash
python -m mini_search.cli query python "machine learning" -i index.pkl -k 5
```

Example output:

```
Top results:
- doc2.txt   BM25: 5.8421
  ...Machine [learning] is a field of artificial intelligence that uses statistical techniques...

- doc5.txt   BM25: 4.9130
  ...Deep [learning] architectures such as deep neural networks...
```

---

## 🛠 Tech Stack
- **Python 3.10+**
- **Typer** for CLI
- **Dataclasses** and **Type Hints** for clean code
- **Pickle** for index persistence

---