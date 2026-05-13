#!/usr/bin/env python3
"""Local retrieval tutor for KAIST Foundations of AI for Business PDFs.

This is not a fine-tuned language model. It is a grounded retrieval layer that
extracts your course PDFs, indexes them, and returns only course-material
evidence for study questions, quiz prep, and cheat-sheet drafting.
"""

from __future__ import annotations

import argparse
import json
import pickle
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from textwrap import fill

from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SOURCE_FILES = [
    "/Users/bangtaeyun/Desktop/coursenotes/2026_Course Notes_Ch. 1 — The General Problem of Intelligence_ Credit Assignment - FAB (1).pdf",
    "/Users/bangtaeyun/Desktop/coursenotes/BTM.40047 - CS 40711_Syllabus_Foundations of AI for Business_English_Spring 2026 (1).pdf",
    "/Users/bangtaeyun/Desktop/coursenotes/Course Notes — Evolutionary Strategies - FAB Spring 2026.pdf",
    "/Users/bangtaeyun/Desktop/coursenotes/Course Notes — Knowledge Representation and Reasoning - FAB Spring 2026.pdf",
    "/Users/bangtaeyun/Desktop/coursenotes/Course Notes — Representation - FAB.pdf",
    "/Users/bangtaeyun/Desktop/coursenotes/Course Notes — Search - FAB - Spring 2026.pdf",
    "/Users/bangtaeyun/Desktop/coursenotes/Course Notes 7 — Interaction - FAB (1).pdf",
    "/Users/bangtaeyun/Desktop/coursenotes/Course Notes 8 — Reasoning about the Physical World - FAB.pdf",
    "/Users/bangtaeyun/Desktop/coursenotes/Course Notes, Session 2 — Information Processing - FAB.pdf",
    "/Users/bangtaeyun/Desktop/Intermediate Feedback_All Groups_Evolutionary Strategies Module_FAB 2026.pdf",
    "/Users/bangtaeyun/Desktop/Classwide List_Concepts, Metadata, Constraints_FAB 2026.pdf",
    "/Users/bangtaeyun/Desktop/weekly module file/Group Project Overview_FAB Spring 2026 (1).pdf",
    "/Users/bangtaeyun/Desktop/weekly module file/Weekly Module 3_Group Project_Representation (1).pdf",
    "/Users/bangtaeyun/Desktop/weekly module file/Weekly Module 4_Group Project_Knowledge Representation and Reasoning (1).pdf",
    "/Users/bangtaeyun/Desktop/weekly module file/Weekly Module_Search_Group Project_FAB Spring 2026 .pdf",
]

DEFAULT_SOURCES_FILE = Path("sources.txt")
INDEX_DIR = Path("fab_tutor_index")
CHUNKS_FILE = INDEX_DIR / "chunks.json"
MODEL_FILE = INDEX_DIR / "tfidf.pkl"

SYSTEM_BOUNDARY = (
    "Use only the retrieved KAIST FAB course passages. If the retrieved passages "
    "do not cover the question, say: This topic is not covered in the current "
    "course materials provided."
)


@dataclass
class Chunk:
    source: str
    page_start: int
    page_end: int
    text: str


def normalize_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_words(text: str, size: int = 220, overlap: int = 45) -> list[str]:
    words = text.split()
    if not words:
        return []
    chunks = []
    step = max(size - overlap, 1)
    for start in range(0, len(words), step):
        segment = words[start : start + size]
        if len(segment) >= 35:
            chunks.append(" ".join(segment))
    return chunks


def extract_chunks(paths: list[str]) -> list[Chunk]:
    chunks: list[Chunk] = []
    missing = []
    for raw_path in paths:
        path = Path(raw_path)
        if not path.exists():
            missing.append(raw_path)
            continue

        reader = PdfReader(str(path))
        for page_number, page in enumerate(reader.pages, start=1):
            text = normalize_text(page.extract_text() or "")
            for piece in chunk_words(text):
                chunks.append(
                    Chunk(
                        source=path.name,
                        page_start=page_number,
                        page_end=page_number,
                        text=piece,
                    )
                )

    if missing:
        print("Missing files:")
        for path in missing:
            print(f"- {path}")
    return chunks


def load_source_paths(sources_file: Path = DEFAULT_SOURCES_FILE) -> list[str]:
    if sources_file.exists():
        paths = []
        for line in sources_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                paths.append(line)
        return paths
    return SOURCE_FILES


def build_index(sources_file: Path = DEFAULT_SOURCES_FILE) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    source_paths = load_source_paths(sources_file)
    chunks = extract_chunks(source_paths)
    if not chunks:
        raise SystemExit("No text chunks were extracted. Check the PDF paths.")

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=60000)
    matrix = vectorizer.fit_transform([chunk.text for chunk in chunks])

    CHUNKS_FILE.write_text(
        json.dumps([asdict(chunk) for chunk in chunks], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    with MODEL_FILE.open("wb") as f:
        pickle.dump({"vectorizer": vectorizer, "matrix": matrix}, f)

    print(f"Indexed {len(chunks)} chunks from {len(source_paths)} PDFs into {INDEX_DIR}/")


def load_index():
    if not CHUNKS_FILE.exists() or not MODEL_FILE.exists():
        build_index()

    chunks = [Chunk(**item) for item in json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))]
    with MODEL_FILE.open("rb") as f:
        model = pickle.load(f)
    return chunks, model["vectorizer"], model["matrix"]


def search(query: str, top_k: int = 5) -> list[tuple[float, Chunk]]:
    chunks, vectorizer, matrix = load_index()
    query_vector = vectorizer.transform([query])
    scores = cosine_similarity(query_vector, matrix).ravel()
    ranked = scores.argsort()[::-1][:top_k]
    return [(float(scores[i]), chunks[i]) for i in ranked if scores[i] > 0]


def print_sources(results: list[tuple[float, Chunk]], max_chars: int = 650) -> None:
    if not results:
        print("This topic is not covered in the current course materials provided.")
        return

    for rank, (score, chunk) in enumerate(results, start=1):
        print(f"\n[{rank}] {chunk.source}, page {chunk.page_start} | relevance {score:.3f}")
        print(fill(chunk.text[:max_chars], width=96))


def answer(query: str, top_k: int = 5) -> None:
    results = search(query, top_k=top_k)
    if not results or results[0][0] < 0.04:
        print("This topic is not covered in the current course materials provided.")
        return

    print("Grounded answer draft")
    print("---------------------")
    print(SYSTEM_BOUNDARY)
    print("\nUse these retrieved course passages to answer:")
    print_sources(results)


def quiz(topic: str, count: int = 5) -> None:
    results = search(topic, top_k=max(count, 5))
    if not results:
        print("This topic is not covered in the current course materials provided.")
        return

    print(f"Quiz practice topic: {topic}")
    print("Answer from the course materials, then check against the cited passages.\n")
    stems = [
        "Which course concept best explains the situation described in the cited passage?",
        "What problem, limitation, or tension is the passage emphasizing?",
        "How would this idea apply to an organization or business problem?",
        "Which term from the course notes is most central here?",
        "What kind of feedback, constraint, representation, or strategy is being discussed?",
    ]
    for i, (_, chunk) in enumerate(results[:count], start=1):
        print(f"{i}. {stems[(i - 1) % len(stems)]}")
        print(f"   Source: {chunk.source}, page {chunk.page_start}")
        print(f"   Evidence: {fill(chunk.text[:360], width=88)}\n")


def prompt_for_llm(query: str, top_k: int = 6) -> None:
    results = search(query, top_k=top_k)
    if not results:
        print("This topic is not covered in the current course materials provided.")
        return

    print("Paste this into an LLM with your course files uploaded:\n")
    print(SYSTEM_BOUNDARY)
    print(f"\nUser question: {query}\n")
    print("Relevant course passages:")
    for i, (_, chunk) in enumerate(results, start=1):
        print(f"\nPassage {i}: {chunk.source}, page {chunk.page_start}")
        print(chunk.text)


def main() -> None:
    parser = argparse.ArgumentParser(description="KAIST FAB course-grounded AI tutor starter.")
    sub = parser.add_subparsers(dest="command", required=True)

    build_parser = sub.add_parser("build", help="Extract PDF text and build the local search index.")
    build_parser.add_argument("--sources-file", type=Path, default=DEFAULT_SOURCES_FILE)

    search_parser = sub.add_parser("search", help="Retrieve relevant course passages.")
    search_parser.add_argument("query")
    search_parser.add_argument("--top-k", type=int, default=5)

    answer_parser = sub.add_parser("answer", help="Prepare a grounded answer draft.")
    answer_parser.add_argument("query")
    answer_parser.add_argument("--top-k", type=int, default=5)

    quiz_parser = sub.add_parser("quiz", help="Generate practice questions with cited evidence.")
    quiz_parser.add_argument("topic")
    quiz_parser.add_argument("--count", type=int, default=5)

    prompt_parser = sub.add_parser("prompt", help="Create a strict prompt with retrieved evidence.")
    prompt_parser.add_argument("query")
    prompt_parser.add_argument("--top-k", type=int, default=6)

    args = parser.parse_args()
    if args.command == "build":
        build_index(args.sources_file)
    elif args.command == "search":
        print_sources(search(args.query, top_k=args.top_k))
    elif args.command == "answer":
        answer(args.query, top_k=args.top_k)
    elif args.command == "quiz":
        quiz(args.topic, count=args.count)
    elif args.command == "prompt":
        prompt_for_llm(args.query, top_k=args.top_k)


if __name__ == "__main__":
    main()
