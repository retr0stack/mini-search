#!/usr/bin/env python3
from __future__ import annotations

import logging
from pathlib import Path
from typing import List
import typer

from .indexing import build_index, save_index, load_index
from .planner import search

app = typer.Typer(help="Mini Search Engine: positional index + phrase search + BM25 ranking")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


@app.command()
def index(
    path: Path = typer.Argument(..., help="Folder with .txt files"),
    out: Path = typer.Option(Path("index.pkl"), "--out", "-o", help="Path to save the index"),
) -> None:
    index_obj, meta = build_index(path)
    save_index(index_obj, meta, out)
    logging.info("Indexed %d files -> %s", len(meta.files), out)


@app.command()
def query(
    q: List[str] = typer.Argument(..., help='Search query (phrases in quotes, e.g., python "machine learning")'),
    idx: Path = typer.Option(Path("index.pkl"), "--index", "-i", help="Path to the saved index"),
    k: int = typer.Option(10, "--top-k", "-k", help="How many results to show"),
) -> None:
    request = " ".join(q)
    index_obj, meta = load_index(idx)
    results = search(index_obj, meta, request, top_k=k)

    if not results:
        typer.echo("No results found.")
        raise typer.Exit()

    typer.secho("Top results:", bold=True)
    for doc, score, snippet in results:
        score_str = "-" if score is None else f"{score:.4f}"
        typer.echo(f"- {doc}\tBM25: {score_str}\n  {snippet}\n")


if __name__ == "__main__":
    app()
