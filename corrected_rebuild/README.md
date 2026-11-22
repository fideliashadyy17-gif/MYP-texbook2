# Corrected Complete Rebuild — Production Source

This directory is the corrected delivery. It is separate from `upgraded_editions/`, which is retained only for traceability.

## Production architecture

The repository contains complete PDF originals but no original HTML, CSS, InDesign, Affinity, Word or LaTeX files. The source workflow therefore treats each original PDF as the immutable full-book source asset and applies editable, reversible page-level exercise replacements:

1. `source/exercise_content.py` contains all new exercise and answer text in editable form.
2. `source/patch_manifest.json` maps every replacement to its chapter and physical source pages.
3. `source/build_complete_books.py` starts from each complete original PDF, removes selected weak/repetitive regions inside the existing mixed-practice sequence, and places the upgraded exercises there using the book's established accent colour, margins, header/footer and page size.
4. No enrichment pages are appended. Page counts and original pagination remain unchanged.
5. `source/build_answer_reference.py` regenerates the separate educator reference.
6. `source/run_qa.py` renders and compares every original/final page.

Run from the repository root:

```bash
.venv/bin/python corrected_rebuild/source/build_complete_books.py
.venv/bin/python corrected_rebuild/source/build_answer_reference.py
.venv/bin/python corrected_rebuild/source/run_qa.py
```

The five complete outputs are in `complete_books/`. The original books at repository root are not overwritten.
