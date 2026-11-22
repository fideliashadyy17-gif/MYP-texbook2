#!/usr/bin/env python3
from pathlib import Path
import fitz,json,re
ROOT=Path(__file__).resolve().parents[2];SRC=ROOT/'final_integrated_editions/source';manifest=json.loads((SRC/'build_manifest.json').read_text());result={'status':'PASS','issues':[],'books':{},'exact_exam_pages':[],'rendered_final_pages':0}
def norm(s):return re.sub(r'\s+',' ',s).strip()
for year,v in manifest.items():
 d=fitz.open(ROOT/v['output']);blank=[];worked=0;summaries=0;alltexts=[]
 for i,p in enumerate(d,1):
  t=p.get_text();alltexts.append(t);pix=p.get_pixmap(matrix=fitz.Matrix(.13,.13),colorspace=fitz.csGRAY,alpha=False);result['rendered_final_pages']+=1
  if sum(x<245 for x in pix.samples)/len(pix.samples)<.001:blank.append(i)
  worked+=('WORKED REASONING' in t);summaries+=('CONCEPT CONNECTIONS' in t)
  if any(label in t for label in ['WORKED REASONING','CONCEPT CONNECTIONS','UPGRADED MIXED PRACTICE']):
   for b in p.get_text('blocks'):
    x0,y0,x1,y1=b[:4]
    if x0<-1 or y0<-1 or x1>p.rect.width+1 or y1>p.rect.height+1:result['issues'].append(f'MYP{year} p{i}: text out of bounds')
 exp=v['source_pages']+v['chapters']+sum(x['pages'] for x in v['exact_exam_facsimiles'])
 if len(d)!=exp:result['issues'].append(f'MYP{year}: pages {len(d)} != {exp}')
 if worked!=v['chapters']:result['issues'].append(f'MYP{year}: worked pages {worked}')
 if summaries!=v['chapters']:result['issues'].append(f'MYP{year}: summary panels {summaries}')
 # Every examination source page must occur exactly and raster-identically in final book.
 for e in v['exact_exam_facsimiles']:
  ed=fitz.open(ROOT/e['file'])
  for epi,ep in enumerate(ed):
   key=norm(ep.get_text());matches=[j for j,t in enumerate(alltexts) if key==norm(t)]
   if len(matches)!=1:result['issues'].append(f"{e['file']} p{epi+1}: occurrence count {len(matches)}");continue
   fp=d[matches[0]];a=ep.get_pixmap(matrix=fitz.Matrix(.28,.28),alpha=False);b=fp.get_pixmap(matrix=fitz.Matrix(.28,.28),alpha=False);same=(a.width,a.height,a.samples)==(b.width,b.height,b.samples)
   if not same:result['issues'].append(f"{e['file']} p{epi+1}: raster differs")
   result['exact_exam_pages'].append({'file':e['file'],'source_page':epi+1,'final_page':matches[0]+1,'text_exact':norm(ep.get_text())==norm(fp.get_text()),'raster_exact':same})
  ed.close()
 result['books'][year]={'pages':len(d),'expected_pages':exp,'worked_example_pages_found':worked,'summary_panels_found':summaries,'integrated_practice_pages':v['chapters']*2,'nearly_blank_pages':blank};d.close()
# Coverage matrix completeness
matrix=json.loads((SRC/'coverage_matrix.json').read_text());
if len(matrix)!=56:result['issues'].append(f'coverage rows {len(matrix)}')
for r in matrix:
 for key in ['original_reviewed','worked_examples_improved','practice_enriched','summary_improved','mathematical_answers_present']:
  if not r[key]:result['issues'].append(f"MYP{r['level']}.{r['chapter']}: {key}")
if result['issues']:result['status']='FAIL'
(ROOT/'final_integrated_editions/qa/full_qa.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'status':result['status'],'issues':len(result['issues']),'rendered_final_pages':result['rendered_final_pages'],'exact_exam_pages_verified':len(result['exact_exam_pages']),'books':result['books']},indent=2))
if result['issues']:print('\n'.join(result['issues']));raise SystemExit(1)
