# Pedagogically Reconstructed Coursebooks

This is the corrected delivery in which examination PDFs are references only.

The build starts from the complete original-derived books, removes all previous examination-facsimile integration by not using those outputs, and generates:

- integrated worked examples for every chapter;
- original progressive practice for every chapter;
- source-informed exercises reconstructed in the coursebook design;
- enriched chapter summaries;
- a separate educator answer reference.

No examination PDF page is imported.

## Rebuild

```bash
python pedagogical_rebuild/source/build_books.py
python pedagogical_rebuild/source/build_answer_reference.py
python pedagogical_rebuild/source/run_qa.py
```

See `FINAL_QA_REPORT.md` and `source/coverage_matrix.json`.
