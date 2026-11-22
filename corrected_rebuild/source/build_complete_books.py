#!/usr/bin/env python3
"""Rebuild five complete coursebooks from the original PDFs with integrated exercise edits.

The repository has no original publishing source. The original PDF is therefore an explicit
source asset. This script makes reversible page-level edits inside each chapter's existing
mixed-practice sequence; it does not append supplementary pages. Every output keeps the
original page count, chapter sequence, explanations, examples, identity and pagination.
"""
from pathlib import Path
import sys, re, json, shutil
import fitz
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).parent))
from exercise_content import BOOKS
OUT=ROOT/'corrected_rebuild/complete_books'; OUT.mkdir(parents=True,exist_ok=True)
QA=ROOT/'corrected_rebuild/qa'; QA.mkdir(parents=True,exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FONTB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
# Logical chapter starts and first logical page after the final chapter.
SPECS={
1:{'starts':[18,35,53,74,95,114,133,155,174,194],'after':216,'offset':0,'color':'#B85C38'},
2:{'starts':[19,35,50,66,84,102,123,147,167,188,206],'after':222,'offset':0,'color':'#147980'},
3:{'starts':[19,36,53,71,91,111,134,155,181,206],'after':231,'offset':0,'color':'#6657A0'},
4:{'starts':[1,31,57,81,105,127,149,171,193,221,251,281,315],'after':343,'offset':11,'color':'#0D635D'},
5:{'starts':[1,23,43,63,89,109,129,151,173,195,217,233],'after':245,'offset':13,'color':'#0B4D48'},
}

def clean(s):
    table=str.maketrans({'₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5','₆':'6','₇':'7','₈':'8','₉':'9','ₙ':'n','₊':'+','₋':'-','–':'–','—':'—'})
    return s.translate(table)

def find_target_pages(doc,year,ch):
    sp=SPECS[year]; start=sp['starts'][ch-1]+sp['offset']; nextlog=sp['starts'][ch] if ch<len(sp['starts']) else sp['after']; end=nextlog-1+sp['offset']
    hits=[]
    for physical in range(start,end+1):
        text=doc[physical-1].get_text()
        if re.search(r'MIXED\s+PRACTICE|M I X E D\s+P R|Mixed practice',text,re.I): hits.append(physical)
    # Books 1–3 place the substantial mixed-practice pages immediately before the next chapter;
    # the heading sometimes appears at the foot of the preceding summary page, so use the final
    # two pages rather than that heading hit. Books 4–5 have explicit multi-page mixed-practice
    # runs followed by assessment and review pages; edit the first two pages of that run so the
    # assessment and summary remain intact.
    if year<=3:
        candidates=[]
        for physical in range(end,start-1,-1):
            text=doc[physical-1].get_text().strip()
            # Skip part-divider artwork and intentionally sparse transition pages.
            if len(text)>=700:
                candidates.append(physical)
            if len(candidates)==2:
                break
        if len(candidates)==2:
            return sorted(candidates)
        return [end-1,end]
    if len(hits)>=2:return hits[:2]
    if len(hits)==1:
        a=hits[0]
        if a+1<=end:return [a,a+1]
        if a-1>=start:return [a-1,a]
    return [end-1,end]

def rgb(hexv):
    hexv=hexv.lstrip('#');return tuple(int(hexv[i:i+2],16)/255 for i in (0,2,4))

def draw_mini_visual(page,kind,rect,color):
    x0,y0,x1,y1=rect; c=color; sh=page.new_shape()
    # Restrained mathematical cue, only where it supports the task family.
    if kind in ('numberline','bounds'):
        y=(y0+y1)/2; sh.draw_line((x0+4,y),(x1-4,y))
        for i in range(5):
            x=x0+8+i*(x1-x0-16)/4;sh.draw_line((x,y-4),(x,y+4))
    elif kind in ('graph','function','parabola','growth','scatter','sequence','polynomial','region','transform','vectors'):
        ox=x0+12;oy=y1-12;sh.draw_line((ox,y0+6),(ox,oy));sh.draw_line((ox,oy),(x1-5,oy))
        pts=[]
        for i in range(6):
            x=ox+5+i*(x1-ox-14)/5
            yy=oy-7-i*5 if kind!='parabola' else oy-5-(i-2.5)**2*3
            pts.append((x,max(y0+7,yy)))
        for a,b in zip(pts,pts[1:]):sh.draw_line(a,b)
    elif kind in ('tree','factor','network'):
        m=(y0+y1)/2;sh.draw_line((x0+5,m),(x0+32,y0+12));sh.draw_line((x0+5,m),(x0+32,y1-12));sh.draw_line((x0+32,y0+12),(x1-5,y0+7));sh.draw_line((x0+32,y1-12),(x1-5,y1-7))
    elif kind=='venn':
        sh.draw_circle(((x0+x1)/2-10,(y0+y1)/2),15);sh.draw_circle(((x0+x1)/2+10,(y0+y1)/2),15)
    elif kind in ('triangle','scale','angles'):
        sh.draw_line((x0+7,y1-7),(x1-7,y1-7));sh.draw_line((x0+7,y1-7),((x0+x1)/2,y0+7));sh.draw_line(((x0+x1)/2,y0+7),(x1-7,y1-7))
    elif kind in ('circle','spinner'):
        sh.draw_circle(((x0+x1)/2,(y0+y1)/2),min(x1-x0,y1-y0)*.28);sh.draw_line(((x0+x1)/2,(y0+y1)/2),((x0+x1)/2+15,(y0+y1)/2-12))
    elif kind in ('solid','composite'):
        sh.draw_rect(fitz.Rect(x0+8,y0+12,x1-18,y1-8));sh.draw_line((x0+8,y0+12),(x0+18,y0+4));sh.draw_line((x1-18,y0+12),(x1-8,y0+4));sh.draw_line((x0+18,y0+4),(x1-8,y0+4))
    else:
        for i,v in enumerate([.35,.65,.48,.8]):
            xx=x0+7+i*13;sh.draw_rect(fitz.Rect(xx,y1-7-(y1-y0-14)*v,xx+8,y1-7))
    sh.finish(color=c,fill=None,width=.8)
    sh.commit()

def textbox(page,rect,text,font,size,color=(0.1,0.12,0.11),align=0):
    return page.insert_textbox(rect,clean(text),fontname=font,fontsize=size,lineheight=1.25,color=color,align=align,overlay=True)

def patch_page(page,year,ch,title,task_a,task_b,kind,color,page_no):
    W,H=page.rect.width,page.rect.height
    # Preserve the actual original page above the edit and its original running footer.
    top=max(285,H*.355); bottom=H-47
    redact=fitz.Rect(48,top,W-48,bottom)
    page.add_redact_annot(redact,fill=(0.982,0.975,0.95));page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
    page.insert_font(fontname='EDBody',fontfile=FONT);page.insert_font(fontname='EDBold',fontfile=FONTB)
    page.draw_rect(redact,color=None,fill=(0.982,0.975,0.95),overlay=True)
    page.draw_line((48,top+2),(W-48,top+2),color=color,width=1.4,overlay=True)
    textbox(page,fitz.Rect(50,top+10,W-50,top+27),f'UPGRADED MIXED PRACTICE  ·  CHAPTER {ch:02d}  ·  {"BUILD AND APPLY" if page_no==1 else "REASON AND EXTEND"}','EDBold',7,color)
    textbox(page,fitz.Rect(50,top+29,W-50,top+49),'Integrated revision: show a complete method, use precise notation and check the result in context.','EDBody',7.2,(.30,.31,.29))
    ptop=top+60; gap=12; ph=(bottom-ptop-gap)/2
    for idx,(label,q) in enumerate((task_a,task_b)):
        y=ptop+idx*(ph+gap); r=fitz.Rect(50,y,W-50,y+ph)
        page.draw_rect(r,color=(.78,.76,.70),fill=(1,1,1),width=.7,overlay=True)
        page.draw_rect(fitz.Rect(r.x0,r.y0,r.x0+7,r.y1),color=None,fill=color,overlay=True)
        textbox(page,fitz.Rect(r.x0+16,r.y0+12,r.x1-100,r.y0+30),label.upper(),'EDBold',7.4,color)
        status=textbox(page,fitz.Rect(r.x0+16,r.y0+36,r.x1-95,r.y1-28),q,'EDBody',9.0,(.10,.12,.11))
        textbox(page,fitz.Rect(r.x0+16,r.y1-25,r.x1-15,r.y1-9),'Evidence: method · representation · justification · independent check','EDBody',6.6,(.38,.39,.36))
        draw_mini_visual(page,kind,(r.x1-85,r.y0+15,r.x1-16,r.y0+72),color)
        if status<0: raise RuntimeError(f'Text overflow MYP{year} chapter {ch} page {page_no}: {q}')

def build():
    manifest={}; patch_index={}
    for year,b in BOOKS.items():
        src=ROOT/b['file'];doc=fitz.open(src);sp=SPECS[year];color=rgb(sp['color']);records=[]
        for ch,(title,end,kind,tasks,answers) in enumerate(b['chapters'],1):
            targets=find_target_pages(doc,year,ch)
            patch_page(doc[targets[0]-1],year,ch,title,tasks[0],tasks[1],kind,color,1)
            patch_page(doc[targets[1]-1],year,ch,title,tasks[2],tasks[3],kind,color,2)
            records.append({'chapter':ch,'title':title,'physical_pages_modified':targets,'tasks':[x[1] for x in tasks]})
        out=OUT/f'MYP_Mathematics_{year}_Student_Coursebook_Corrected_Complete_2026.pdf'
        meta=doc.metadata;meta.update({'title':f'MYP Mathematics {year} — Complete Corrected Upgraded Edition','author':'Sadikou Moukoddim','subject':'Complete original student coursebook with integrated chapter exercise revisions','keywords':'MYP mathematics complete upgraded edition reasoning modelling'})
        doc.set_metadata(meta);doc.save(out,garbage=4,clean=True,deflate=True,deflate_images=True,deflate_fonts=True,use_objstms=1,compression_effort=100);pages=len(doc);doc.close()
        manifest[year]={'source':b['file'],'output':str(out.relative_to(ROOT)),'pages':pages,'chapters_modified':len(records),'modified_pages':sum((r['physical_pages_modified'] for r in records),[])}
        patch_index[year]=records
    (ROOT/'corrected_rebuild/source/patch_manifest.json').write_text(json.dumps(patch_index,indent=2,ensure_ascii=False),encoding='utf-8')
    (QA/'build_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    return manifest

if __name__=='__main__':print(json.dumps(build(),indent=2))
