# FAB AI Tutor Starter

This starter project turns your KAIST FAB PDFs into a local prototype for studying AI ideas under limited processing capacity.

The main course ideas applied are **Search**, **Representation**, **Information Processing**, and **Aggregation**. The system represents course materials as searchable chunks, searches over those chunks with a heuristic, aggregates candidate passages into an evidence board, and constrains study outputs to course-grounded evidence.

It does not fine-tune a model or claim to be a full reasoning engine. Instead, it uses retrieval over your exact course files, which is useful for a private class tutor because it reduces hallucination and can cite the source pages.

Presentation framing:

> This prototype applies multiple course AI ideas to the problem of studying AI ideas: it represents course materials as searchable chunks, searches over them with a heuristic, aggregates candidate passages into an evidence board, and constrains answers to course-grounded knowledge.

## Course AI Ideas Applied

- **Credit Assignment:** decides which passages deserve credit for helping answer a student question.
- **Information Processing:** reduces the burden of reading every page by surfacing a small evidence set.
- **Search:** treats a query as a goal and uses a heuristic to find promising course chunks.
- **Representation:** converts PDFs into structured `source/page/text` chunks plus searchable features.
- **Knowledge Representation and Reasoning:** treats retrieved course passages as a small knowledge base for evidence-based answer scaffolds.
- **Interaction:** supports study through search, answer draft, quiz, and prompt modes.
- **Aggregation:** gathers competing candidate passages from multiple files into one shared evidence board.

## Build the Index

First, create a private local source list:

```bash
cp sources.example.txt sources.txt
```

Then edit `sources.txt` so it contains one local PDF path per line.

```bash
python3 fab_ai_tutor.py build
```

## Ask for Relevant Course Passages

```bash
python3 fab_ai_tutor.py search "credit assignment and intermediate feedback"
```

## Prepare a Grounded Answer Draft

```bash
python3 fab_ai_tutor.py answer "What is the credit assignment problem?"
```

## Generate Quiz Practice

```bash
python3 fab_ai_tutor.py quiz "Weekly Module 4 knowledge representation and reasoning" --count 5
```

## Run the Browser Prototype

Open `fab_ai_tutor_web.html` directly in a browser. No backend server is required.

The web version mirrors the Python pipeline in JavaScript while making the course ideas visible:

```text
PDF upload -> representation as chunks -> heuristic search -> aggregation into evidence board
```

Internally, the heuristic search is implemented with TF-IDF features and cosine similarity. This is an implementation detail, not the main AI idea being claimed.

Because browsers cannot read private local file paths automatically, choose your PDFs from the web UI. You can also save a generated browser index as JSON and load it again later.

## Create a Prompt for Another LLM

```bash
python3 fab_ai_tutor.py prompt "Explain reinforcement learning using only Session 1"
```

Copy the output into Gemini, ChatGPT, or another model. It includes the strict knowledge boundary plus retrieved passages from your course files.

## Files Created

- `fab_ai_tutor.py`: local PDF extraction, TF-IDF indexing, search, answer drafting, quiz generation, and prompt generation.
- `fab_ai_tutor_web.html`: single-file browser prototype with upload, build, search, answer, quiz, and prompt modes.
- `FAB_TUTOR_SYSTEM_PROMPT.md`: strict tutor prompt for any LLM.
- `sources.example.txt`: template for your private PDF path list.
- `fab_tutor_index/`: generated index folder after running `build`.

## GitHub Note

The `.gitignore` excludes PDFs, `sources.txt`, and `fab_tutor_index/` because they may contain private course material or local file paths. Upload the code and prompt files, then rebuild the index locally after cloning.

## Why This Approach

For your goal, retrieval-augmented generation is better than fine-tuning at the start:

- It uses the latest version of your uploaded files immediately.
- It can show source passages and page numbers.
- It avoids teaching the model facts that may change when course notes are updated.
- It works without needing paid training infrastructure.
