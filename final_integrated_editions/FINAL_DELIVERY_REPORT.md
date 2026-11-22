# Final Integrated Editions — MYP Mathematics 1–5

## Delivered books

| Level | Complete integrated PDF | Pages | Chapters processed |
|---|---|---:|---:|
| MYP 1 | `complete_books/MYP_Mathematics_1_Student_Coursebook_Final_Integrated_2026.pdf` | 250 | 10/10 |
| MYP 2 | `complete_books/MYP_Mathematics_2_Student_Coursebook_Final_Integrated_2026.pdf` | 275 | 11/11 |
| MYP 3 | `complete_books/MYP_Mathematics_3_Student_Coursebook_Final_Integrated_2026.pdf` | 286 | 10/10 |
| MYP 4 | `complete_books/MYP_Mathematics_4_Student_Coursebook_Final_Integrated_2026.pdf` | 473 | 13/13 |
| MYP 5 | `complete_books/MYP_Mathematics_5_Student_Coursebook_Final_Integrated_2026.pdf` | 356 | 12/12 |

The original books and both earlier deliveries remain unchanged for traceability.

## Chapter-level integration

All 56 chapters received all three required interventions:

1. **Worked examples:** one new chapter-specific worked-reasoning page integrated inside the concept sequence. Each page models reading conditions, planning, execution and an independent check, using two original chapter tasks.
2. **Practice:** two existing chapter-practice pages contain integrated Foundation, Application, Reasoning and Challenge tasks. Across the series this contributes 224 new original tasks, with an editable answer entry for each.
3. **Chapter summary:** every chapter review contains an integrated Concept Connections / Common Error / Reasoning panel.

The JSON coverage matrix at `source/coverage_matrix.json` has 56 rows and records completion of each component.

## Exact supplied-examination integration

All six supplied examination PDFs are reproduced as **unaltered PDF facsimile pages** inside the complete books. This is the only method that guarantees exact wording, values, question order, subquestions, diagrams, tables, fonts and spatial relationships without pretending the PDF source is editable.

- MYP 2: both two-page Term 1 examinations are placed after Chapter 10 as cumulative first-term practice covering Chapters 1, 2, 3, 8 and 10.
- MYP 3: the complete two-page Grade 8 assessment is placed after Chapter 3, covering the first-term cluster.
- MYP 4: the complete two-page Grade 9 assessment is placed between Chapters 12 and 13 for statistics/probability practice.
- MYP 5: both two-page sequence-and-series assessments are placed immediately after Chapter 4.
- MYP 1: no examination file was supplied; all added material is original.

The exact topic map is in `source/examination_integration_map.json`.

## Design and production

- Inherited pages retain the original covers, author attribution, typography, chapter order, explanations, examples, assessments, headers, footers and graphics.
- New pages use each level’s established accent colour and the original A4 geometry.
- Examination facsimiles are inserted without reflow or recreation.
- Editable sources include all new questions, answers, worked pages, summary panels, page mappings, palettes and build logic.
- The original PDF books are explicit source assets because no native InDesign/HTML/Word source exists in the repository.

## QA performed

`source/run_full_qa.py` returned **PASS with zero issues**:

- 1,640 final pages rendered.
- 56/56 worked-example pages found.
- 56/56 chapter-summary panels found.
- 112 integrated practice pages found.
- 224 new tasks represented in the coverage source.
- 12/12 supplied examination pages verified by exact normalized text and raster equality against their source PDFs.
- Expected and actual page totals matched for all five books.
- No out-of-bounds text was detected in newly produced components.
- Preview sheets for all five levels were rendered and visually inspected for hierarchy, alignment, colour continuity and examination fidelity.

Blank separator pages detected in MYP 4 and MYP 5 are inherited chapter/part transitions from the original books, not newly generated empty enrichment pages.

## Educator reference

`MYP_1-5_Final_Integrated_Educator_Answer_Reference.pdf` supplies concise verified checks for the 224 newly authored integrated tasks. The exact examination facsimiles preserve the source papers’ original marks and criterion structure; the repository did not include official examination mark schemes, so no answer key is falsely attributed to those source assessments.

## Editable/reproducible sources

- `source/exercise_content.py`
- `source/build_integrated_books.py`
- `source/build_answer_reference.py`
- `source/run_full_qa.py`
- `source/build_manifest.json`
- `source/coverage_matrix.json`
- `source/examination_integration_map.json`
