# FAB AI Tutor Starter

This starter project turns your KAIST FAB PDFs into a local course-grounded tutor index.

It does not fine-tune a model. Instead, it uses retrieval over your exact course files, which is usually the best first version for a private class tutor because it reduces hallucination and can cite the source pages.

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

## Create a Prompt for Another LLM

```bash
python3 fab_ai_tutor.py prompt "Explain reinforcement learning using only Session 1"
```

Copy the output into Gemini, ChatGPT, or another model. It includes the strict knowledge boundary plus retrieved passages from your course files.

## Files Created

- `fab_ai_tutor.py`: local PDF extraction, TF-IDF indexing, search, answer drafting, quiz generation, and prompt generation.
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
