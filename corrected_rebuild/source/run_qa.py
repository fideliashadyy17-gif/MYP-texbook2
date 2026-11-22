#!/usr/bin/env python3
"""Full-document rendering and integrity QA for corrected complete editions."""
from pathlib import Path
import json,hashlib,fitz
ROOT=Path(__file__).resolve().parents[2];QA=ROOT/'corrected_rebuild/qa'
manifest=json.loads((QA/'build_manifest.json').read_text())
result={'status':'PASS','books':{},'total_final_pages_rendered':0,'total_original_pages_rendered_for_comparison':0,'issues':[]}
for year,v in manifest.items():
 src=fitz.open(ROOT/v['source']);out=fitz.open(ROOT/v['output']);modified=set(v['modified_pages']);rec={'source_pages':len(src),'output_pages':len(out),'modified_pages':sorted(modified),'unchanged_pages_raster_matched':0,'modified_pages_with_all_labels':0,'blank_output_pages':[],'metadata':out.metadata}
 if len(src)!=len(out):result['issues'].append(f'MYP{year}: page count changed')
 for i,(a,b) in enumerate(zip(src,out),1):
  pa=a.get_pixmap(matrix=fitz.Matrix(.16,.16),colorspace=fitz.csGRAY,alpha=False);pb=b.get_pixmap(matrix=fitz.Matrix(.16,.16),colorspace=fitz.csGRAY,alpha=False)
  result['total_original_pages_rendered_for_comparison']+=1;result['total_final_pages_rendered']+=1
  dark=sum(x<245 for x in pb.samples)/len(pb.samples)
  if dark<.001:rec['blank_output_pages'].append(i)
  if i not in modified:
   if pa.samples==pb.samples:rec['unchanged_pages_raster_matched']+=1
   else:result['issues'].append(f'MYP{year} p{i}: unmodified page differs')
  else:
   text=b.get_text()
   required=['UPGRADED MIXED PRACTICE','Evidence: method','CHAPTER']
   if all(x in text for x in required):rec['modified_pages_with_all_labels']+=1
   else:result['issues'].append(f'MYP{year} p{i}: integrated labels missing')
   for block in b.get_text('blocks'):
    x0,y0,x1,y1=block[:4]
    if x0<-1 or y0<-1 or x1>b.rect.width+1 or y1>b.rect.height+1:result['issues'].append(f'MYP{year} p{i}: text block out of bounds')
 rec['expected_unchanged_pages']=len(out)-len(modified);result['books'][year]=rec
 src.close();out.close()
# Validate editable content coverage.
sys_path=ROOT/'corrected_rebuild/source';import sys;sys.path.insert(0,str(sys_path));from exercise_content import BOOKS
for year,b in BOOKS.items():
 for ch,item in enumerate(b['chapters'],1):
  tasks=item[3];answers=item[4]
  if len(tasks)!=4 or len(answers)!=4 or any(not q[1].strip() for q in tasks) or any(not a.strip() for a in answers):result['issues'].append(f'MYP{year}.{ch}: task/answer structure')
result['chapter_count']=sum(len(b['chapters']) for b in BOOKS.values());result['integrated_new_tasks']=result['chapter_count']*4
if result['issues']:result['status']='FAIL'
(QA/'full_page_qa.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
print(json.dumps({'status':result['status'],'final_pages_rendered':result['total_final_pages_rendered'],'comparison_pages_rendered':result['total_original_pages_rendered_for_comparison'],'issues':len(result['issues']),'books':{k:{'pages':x['output_pages'],'raster_matched_unchanged':x['unchanged_pages_raster_matched'],'expected_unchanged':x['expected_unchanged_pages'],'modified_labels_ok':x['modified_pages_with_all_labels']} for k,x in result['books'].items()}},indent=2))
if result['issues']:raise SystemExit(1)
