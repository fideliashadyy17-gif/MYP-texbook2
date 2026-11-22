#!/usr/bin/env python3
from pathlib import Path
import fitz,json,sys
ROOT=Path(__file__).resolve().parents[2];SRC=ROOT/'pedagogical_rebuild/source';sys.path.insert(0,str(SRC))
from exercise_content import BOOKS
from reference_reconstructions import REFERENCE_PRACTICE
m=json.loads((SRC/'build_manifest.json').read_text());result={'status':'PASS','issues':[],'books':{},'rendered_pages':0}
for year,v in m.items():
 d=fitz.open(ROOT/v['output']);counts={'worked':0,'summary':0,'practice':0,'reference':0};blank=[];forbidden=[]
 for i,p in enumerate(d,1):
  t=p.get_text();pix=p.get_pixmap(matrix=fitz.Matrix(.14,.14),colorspace=fitz.csGRAY,alpha=False);result['rendered_pages']+=1
  if sum(x<245 for x in pix.samples)/len(pix.samples)<.001:blank.append(i)
  counts['worked']+=('WORKED REASONING' in t);counts['summary']+=('CONCEPT CONNECTIONS' in t);counts['practice']+=('UPGRADED MIXED PRACTICE' in t);counts['reference']+=('REFERENCE-RECONSTRUCTED MATHEMATICS' in t)
  if any(x in t.upper() for x in ['OAK INTERNATIONAL SCHOOL, BENIN','DURATION 2 HOURS','END OF FIRST TERM E-ASSESSMENT','SUMMATIVE ASSESSMENT · VERSION']):forbidden.append(i)
  if any(x in t for x in ['WORKED REASONING','CONCEPT CONNECTIONS','UPGRADED MIXED PRACTICE','REFERENCE-RECONSTRUCTED MATHEMATICS']):
   for b in p.get_text('blocks'):
    x0,y0,x1,y1=b[:4]
    if x0<-1 or y0<-1 or x1>p.rect.width+1 or y1>p.rect.height+1:result['issues'].append(f'MYP{year} p{i}: text overflow')
 expected=v['source_pages']+v['chapters']+len(v['reference_reconstruction_pages'])
 if len(d)!=expected:result['issues'].append(f'MYP{year}: page count')
 if counts['worked']!=v['chapters']:result['issues'].append(f'MYP{year}: worked {counts["worked"]}')
 if counts['summary']!=v['chapters']:result['issues'].append(f'MYP{year}: summary {counts["summary"]}')
 if counts['practice']!=v['chapters']*2:result['issues'].append(f'MYP{year}: practice {counts["practice"]}')
 if counts['reference']!=len(v['reference_reconstruction_pages']):result['issues'].append(f'MYP{year}: reference pages {counts["reference"]}')
 if forbidden:result['issues'].append(f'MYP{year}: examination document text on pages {forbidden}')
 result['books'][year]={'pages':len(d),'expected':expected,'worked_examples':counts['worked'],'integrated_practice_pages':counts['practice'],'summary_panels':counts['summary'],'reference_reconstruction_pages':counts['reference'],'forbidden_exam_pages':forbidden,'nearly_blank_pages':blank};d.close()
matrix=json.loads((SRC/'coverage_matrix.json').read_text())
if len(matrix)!=56:result['issues'].append(f'coverage rows {len(matrix)}')
for r in matrix:
 for k in ['existing_material_reviewed','worked_examples_completed','practice_completed','chapter_summary_completed','mathematical_visuals_verified','answers_verified']:
  if not r[k]:result['issues'].append(f'MYP{r["level"]}.{r["chapter"]}: {k}')
if sum(len(x['tasks']) for x in REFERENCE_PRACTICE.values())!=40:result['issues'].append('reference task count')
if any(len(x['tasks'])!=len(x['answers']) for x in REFERENCE_PRACTICE.values()):result['issues'].append('reference answer mismatch')
if result['issues']:result['status']='FAIL'
(ROOT/'pedagogical_rebuild/qa/full_qa.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'status':result['status'],'issues':len(result['issues']),'rendered_pages':result['rendered_pages'],'books':result['books']},indent=2))
if result['issues']:print('\n'.join(result['issues']));raise SystemExit(1)
