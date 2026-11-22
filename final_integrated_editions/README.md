# Final Integrated MYP Mathematics Editions

This is the current delivery. Earlier folders remain for traceability.

## Rebuild

From repository root, with PyMuPDF, ReportLab, Pillow and pypdf installed:

```bash
python final_integrated_editions/source/build_integrated_books.py
python final_integrated_editions/source/build_answer_reference.py
python final_integrated_editions/source/run_full_qa.py
```

The build uses the complete corrected original-derived PDFs as base assets, integrates new chapter content, and inserts the six supplied examination files as exact PDF facsimiles at their mapped curriculum locations. Originals are never overwritten.

See `FINAL_DELIVERY_REPORT.md` and `source/examination_integration_map.json` for coverage and provenance.
