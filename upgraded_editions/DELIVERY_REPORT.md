# MYP Mathematics 1–5 — Premium Upgrade Delivery Report

**Edition:** 2026 premium upgraded student coursebooks  
**Author preserved:** Sadikou Moukoddim, Head of Mathematics Department, Mathematics Teacher, Category 1  
**Completion boundary:** all 56 chapters across MYP 1–5 received a directly integrated two-page enrichment studio; final PDFs and editable enrichment source were generated and checked.

## Primary deliverables

| Level | Upgraded printable PDF | Chapters upgraded | Final pages |
|---|---|---:|---:|
| MYP 1 | `MYP_Mathematics_1_Student_Coursebook_Upgraded_2026.pdf` | 10/10 | 261 |
| MYP 2 | `MYP_Mathematics_2_Student_Coursebook_Upgraded_2026.pdf` | 11/11 | 283 |
| MYP 3 | `MYP_Mathematics_3_Student_Coursebook_Upgraded_2026.pdf` | 10/10 | 295 |
| MYP 4 | `MYP_Mathematics_4_Student_Coursebook_Upgraded_2026.pdf` | 13/13 | 485 |
| MYP 5 | `MYP_Mathematics_5_Student_Coursebook_Upgraded_2026.pdf` | 12/12 | 365 |

Also delivered:

- `MYP_1-5_Premium_Enrichment_Educator_Answer_Reference.pdf` — concise answer checks for every new task; separate from student books.
- `source/content.py` — editable, structured source for all enrichment questions and answers.
- `source/build.py` — reproducible PDF generation, chapter integration, metadata, bookmarks and structural QA workflow.
- `generated_modules/` — individually editable/rebuildable two-page chapter inserts and upgrade guides.
- `qa_results.json` and `render_qa.json` — machine-readable QA records.
- `qa_contact_MYP1.jpg` through `qa_contact_MYP5.jpg` — rendered visual contact sheets used for layout review.

The original eleven repository PDFs remain unchanged at repository root.

## Chapters upgraded

### MYP 1
Number systems and place value; powers, expanded form and order of operations; factors, multiples and primes; fractions and decimals; percentages and applications; patterns, expressions and equations; lines, angles, triangles and constructions; sets and classification; perimeter, area, surface area and volume; data, tables and graphs.

### MYP 2
Ratios; proportional reasoning; rates; integers; algebraic expressions and equations; numerical patterns; 2D geometry; 3D geometry; transformations; probability and simulation; univariate data.

### MYP 3
Real numbers; powers, roots and scientific notation; functions and algebra; linear relationships; equations, inequalities and systems; transformations and congruence; similarity and trigonometry; solids and measurement; bivariate data; probability, sampling and evidence.

### MYP 4
Exponents, surds and accuracy; factorisation; linear equations and systems; functions and linear models; quadratic equations; quadratic functions; sequences; financial growth; congruence and similarity; Pythagoras and trigonometry; surface area and volume; statistics; combined probability.

### MYP 5
Polynomials and algebraic fractions; functions and inverses; exponential and logarithmic functions; sequences and series; quadratic inequalities and linear programming; circle geometry; sine/cosine rules and 3D trigonometry; vectors and matrices; statistics and regression; conditional probability and counting; modelling capstone; cumulative revision.

## Exercise improvements

- Added **224 original student tasks** across 56 chapter studios.
- Every chapter now has a deliberate progression: **Foundation → Application → Reasoning → Challenge**.
- Added non-routine constraints, proof prompts, error analysis, modelling assumptions, interpretation and independent checks.
- Added contextual work with FCFA, water, transport, energy, school data, construction and finance where mathematically appropriate.
- Included open modelling prompts only where multiple defensible outcomes are pedagogically useful; answer guidance states acceptance conditions.
- Added 56 chapter reflection prompts focused on mathematical communication and self-management.

## Supplied-exercise analysis and integration

The six additional assessment PDFs were extracted and reviewed. Their strongest recurring features were mapped rather than copied randomly:

- **MYP 2 Term 1 assessments (two versions):** criterion-labelled progression, probability simulation, ratio/rate contexts and full-working expectations informed MYP 2 studios.
- **MYP 3 assessment:** unfamiliar multi-step contexts and Criteria A–D communication informed MYP 3 algebra, systems, evidence and probability tasks.
- **MYP 4 assessment:** statistical tables, distribution comparison and applied reasoning informed statistics/probability studios; sequence-style progression was adapted for Chapter 7.
- **MYP 5 sequence assessments (two versions):** explicit/recursive conversion, first/second differences, arithmetic/geometric comparisons, sigma notation and annuity contexts informed the MYP 5 sequences studio and cross-level progression.

No supplied question was pasted wholesale. New values, structures and reasoning demands were written to fit each chapter and year.

## Mathematical visuals

Every enrichment studio includes a professionally styled visual-thinking area. The 56 chapter visuals include number lines, ratio/data bars, function and sequence graphs, parabolas, scatter plots, probability trees, Venn diagrams, coordinate regions, vector/transform grids, triangles, circles, solids and network models. Visuals are vector-drawn by the build source and remain sharp in print.

## QA actually performed

1. Extracted text from all 11 input PDFs and inventoried **1,572 original pages**.
2. Confirmed all five original coursebooks, six supplied assessments, author metadata and course structures.
3. Checked the presence of all expected chapter counts: 10 + 11 + 10 + 13 + 12 = **56**.
4. Wrote concise answer checks for all **224** new tasks and manually reviewed calculations, domains, units and stated assumptions; substantive errors found during review were corrected before the final build.
5. Built all five books and checked exact expected page totals and valid page media boxes (`qa_results.json`: PASS).
6. Rendered every page in the five final PDFs after the final rebuild (**1,689 final pages**) plus all 112 enrichment pages; all files opened and rendered successfully.
7. Scanned every enrichment text block for page-boundary overflow; final result: **0 boundary issues**.
8. Verified that every module contains all four progression labels and exactly two pages; final result: PASS.
9. Visually inspected rendered contact sheets for all 56 studios to check hierarchy, spacing, page balance and diagram presence.
10. Compared nearly blank final pages with the original books. The blank separator pages in MYP 4 and MYP 5 are inherited from, and correspond to, deliberate pages in the original PDFs; no new blank enrichment page was introduced.
11. Verified final metadata: title and author are present in every upgraded PDF, and chapter enrichment bookmarks were added.

## Genuine limitations

- The repository contained PDF coursebooks only—no original HTML/CSS, InDesign, Affinity Publisher, Word or LaTeX source. Therefore, original pages were preserved exactly and the upgrade is integrated as premium two-page studios following each chapter. The **new enrichment content is fully editable** in `source/content.py` and reproducibly typeset by `source/build.py`; inherited original pages are not editable source.
- Original printed page numbers remain unchanged. Enrichment inserts use chapter labels (for example, “Enrichment 3.7”), and PDF bookmarks provide direct navigation.
- QA included full automated rendering and visual review of all newly created pages, but it was not a commercial offset-printer preflight (for example, physical proofing, ink limits or press-specific ICC conversion).
