#!/usr/bin/env python3
"""Build five upgraded student editions plus an educator answer reference.
Requires: reportlab, pypdf, pymupdf, pillow. Run from repository root.
"""
from pathlib import Path
import sys, math, json, re
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).parent))
from content import BOOKS
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, Color, white, black
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import simpleSplit
from pypdf import PdfReader, PdfWriter

OUT=ROOT/'upgraded_editions'; MOD=OUT/'generated_modules'; OUT.mkdir(exist_ok=True); MOD.mkdir(exist_ok=True)
W,H=A4
font_regular='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; font_bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; font_serif='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'; font_serif_b='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
pdfmetrics.registerFont(TTFont('Interish',font_regular));pdfmetrics.registerFont(TTFont('Interish-Bold',font_bold));pdfmetrics.registerFont(TTFont('Serif',font_serif));pdfmetrics.registerFont(TTFont('Serif-Bold',font_serif_b))

def clean(s):
    return s.replace('ₙ','n').replace('₁','1').replace('₂','2').replace('₃','3').replace('₄','4').replace('₅','5').replace('₆','6').replace('₇','7').replace('₈','8').replace('₉','9').replace('₀','0').replace('₊','+').replace('₋','-')

def lines(c,text,font,size,width): return simpleSplit(clean(text),font,size,width)
def draw_wrapped(c,text,x,y,width,font='Serif',size=10,leading=14,color=black,max_lines=20):
    c.setFont(font,size); c.setFillColor(color)
    ls=lines(c,text,font,size,width)[:max_lines]
    for line in ls: c.drawString(x,y,line); y-=leading
    return y

def header(c,year,ch,title,color,page_label):
    c.setFillColor(HexColor('#F8F5EE'));c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(color);c.rect(0,H-92,W,92,fill=1,stroke=0)
    c.setFillColor(white);c.setFont('Interish-Bold',8);c.drawString(42,H-27,f'MYP MATHEMATICS {year}  ·  PREMIUM ENRICHMENT')
    heading=f'{ch:02d}  {title}'
    heading_size=20
    while pdfmetrics.stringWidth(heading,'Serif-Bold',heading_size)>W-84 and heading_size>11:
        heading_size-=0.5
    c.setFont('Serif-Bold',heading_size); c.drawString(42,H-55,heading)
    c.setFont('Interish',7);c.drawRightString(W-42,H-27,page_label)
    c.setFillColor(HexColor('#6A665E'));c.setFont('Interish',7);c.drawString(42,25,'SADIKOU MOUKODDIM  ·  PREMIUM UPGRADED EDITION 2026')
    c.drawRightString(W-42,25,f'ENRICHMENT {year}.{ch}')

def box(c,x,y,w,h,label,text,color):
    c.setFillColor(white);c.setStrokeColor(HexColor('#D8D2C7'));c.roundRect(x,y-h,w,h,8,fill=1,stroke=1)
    c.setFillColor(color);c.roundRect(x+10,y-25,100,18,5,fill=1,stroke=0)
    c.setFillColor(white);c.setFont('Interish-Bold',7);c.drawCentredString(x+60,y-19,label)
    draw_wrapped(c,text,x+14,y-40,w-28,'Serif',10,14,HexColor('#252927'),15)

def visual(c,kind,x,y,w,h,color):
    c.saveState();c.setStrokeColor(color);c.setFillColor(HexColor('#E9EFEA'));c.setLineWidth(1.3)
    if kind in ('numberline','bounds'):
        c.line(x+20,y+h/2,x+w-20,y+h/2)
        for i in range(9):
            xx=x+25+i*(w-50)/8;c.line(xx,y+h/2-5,xx,y+h/2+5);c.setFont('Interish',6);c.drawCentredString(xx,y+h/2-16,str(i-4))
    elif kind in ('graph','function','parabola','growth','scatter','sequence','polynomial'):
        ox=x+38;oy=y+24;c.line(ox,oy,ox,y+h-12);c.line(ox,oy,x+w-12,oy)
        pts=[]
        for i in range(9):
            xx=ox+i*(w-55)/8
            if kind=='parabola': yy=oy+5+(i-4)**2*2.2
            elif kind=='scatter': yy=oy+15+i*6+((-1)**i)*7
            elif kind in ('growth','sequence'): yy=oy+8+3*(1.32**i)
            else: yy=oy+12+i*6
            pts.append((xx,min(yy,y+h-15)))
        for a,b in zip(pts,pts[1:]):c.line(*a,*b)
        for p in pts:c.circle(*p,2.2,fill=1,stroke=0)
    elif kind in ('tree','factor','network'):
        c.line(x+20,y+h/2,x+w*.42,y+h*.72);c.line(x+20,y+h/2,x+w*.42,y+h*.28)
        c.line(x+w*.42,y+h*.72,x+w*.78,y+h*.82);c.line(x+w*.42,y+h*.72,x+w*.78,y+h*.6)
        c.line(x+w*.42,y+h*.28,x+w*.78,y+h*.4);c.line(x+w*.42,y+h*.28,x+w*.78,y+h*.18)
        for px,py in [(x+20,y+h/2),(x+w*.42,y+h*.72),(x+w*.42,y+h*.28)]:c.circle(px,py,3,fill=1,stroke=0)
    elif kind in ('venn',):
        c.circle(x+w*.43,y+h*.52,h*.27,fill=0);c.circle(x+w*.60,y+h*.52,h*.27,fill=0)
    elif kind in ('circle','angles'):
        cx=x+w*.52;cy=y+h*.5;r=min(w,h)*.28;c.circle(cx,cy,r,fill=0);c.line(cx-r,cy,cx+r*.7,cy+r*.7);c.line(cx,cy,cx+r*.55,cy-r*.83);c.circle(cx,cy,2,fill=1)
    elif kind in ('triangle','scale'):
        c.line(x+30,y+20,x+w-30,y+20);c.line(x+30,y+20,x+w*.65,y+h-15);c.line(x+w*.65,y+h-15,x+w-30,y+20)
        c.setFont('Interish',7);c.drawString(x+25,y+8,'A');c.drawString(x+w-30,y+8,'B');c.drawString(x+w*.65,y+h-10,'C')
    elif kind in ('solid','composite'):
        a=(x+40,y+25);b=(x+w*.62,y+25);d=(x+40,y+h*.62);e=(x+w*.62,y+h*.62);dx=w*.18;dy=h*.18
        for p,q in [(a,b),(a,d),(b,e),(d,e),((a[0]+dx,a[1]+dy),(b[0]+dx,b[1]+dy)),((d[0]+dx,d[1]+dy),(e[0]+dx,e[1]+dy)),(a,(a[0]+dx,a[1]+dy)),(b,(b[0]+dx,b[1]+dy)),(d,(d[0]+dx,d[1]+dy)),(e,(e[0]+dx,e[1]+dy))]:c.line(*p,*q)
    elif kind in ('region','transform','vectors'):
        ox=x+w*.48;oy=y+h*.45;c.line(x+15,oy,x+w-15,oy);c.line(ox,y+12,ox,y+h-10)
        c.setFillColor(HexColor('#D9E9E3'));c.wedge(ox-8,oy-5,x+w-25,y+h-12,0,90,fill=1,stroke=0)
        c.setStrokeColor(color);c.line(x+25,y+20,x+w-30,y+h-15)
    elif kind in ('bar','chart','boxplot','rate','ratio','fraction','spinner','balance','model'):
        for i,v in enumerate([.32,.58,.8,.46,.68]):
            bw=(w-70)/5;xx=x+20+i*(bw+7);c.rect(xx,y+18,bw,(h-35)*v,fill=1,stroke=0)
    else:
        for i in range(5): c.circle(x+35+i*35,y+h/2,8+i*2,fill=0)
    c.restoreState()

def make_module(year,ch,title,tasks,color,kind,path):
    c=Canvas(str(path),pagesize=A4); c.setTitle(f'MYP Mathematics {year} Chapter {ch} Enrichment');c.setAuthor('Sadikou Moukoddim')
    header(c,year,ch,title,color,'STUDIO · 1 OF 2')
    c.setFillColor(HexColor('#343B38'));c.setFont('Serif-Bold',15);c.drawString(42,H-122,'Build fluency, then make the reasoning visible')
    c.setFont('Interish',8);c.setFillColor(HexColor('#6A665E'));c.drawString(42,H-140,'Work without notes first. Show representations, units and checks—not only final answers.')
    box(c,42,H-165,W-84,215,tasks[0][0],tasks[0][1],color)
    box(c,42,H-400,W-84,250,tasks[1][0],tasks[1][1],color)
    c.setFillColor(HexColor('#E8E1D4'));c.roundRect(42,60,W-84,80,8,fill=1,stroke=0)
    c.setFillColor(HexColor('#343B38'));c.setFont('Interish-Bold',8);c.drawString(56,120,'CHECKPOINT')
    draw_wrapped(c,'Estimate before calculating. Annotate each line with the reason for the step. Ask: does the answer fit the context?',56,103,W-112,'Serif',9,13)
    c.showPage()
    header(c,year,ch,title,color,'STUDIO · 2 OF 2')
    c.setFillColor(HexColor('#343B38'));c.setFont('Serif-Bold',15);c.drawString(42,H-122,'Reason, model and extend')
    box(c,42,H-150,W-84,190,tasks[2][0],tasks[2][1],color)
    visual(c,kind,56,H-495,W-112,120,color)
    c.setFillColor(HexColor('#6A665E'));c.setFont('Interish-Bold',7);c.drawString(56,H-510,'VISUAL THINKING SPACE · REDRAW, LABEL OR ADAPT THIS REPRESENTATION')
    box(c,42,H-540,W-84,185,tasks[3][0],tasks[3][1],color)
    c.setFillColor(HexColor('#343B38'));c.setFont('Interish-Bold',8);c.drawString(42,58,'REFLECT')
    draw_wrapped(c,'Which assumption or representation mattered most? Give one independent check of your result.',105,58,W-147,'Serif',8.5,12)
    c.save()

def make_guide(year,color,path):
    c=Canvas(str(path),pagesize=A4);c.setTitle(f'MYP Mathematics {year} Upgraded Edition Guide');c.setAuthor('Sadikou Moukoddim')
    c.setFillColor(HexColor('#F8F5EE'));c.rect(0,0,W,H,fill=1,stroke=0);c.setFillColor(color);c.rect(0,H-220,W,220,fill=1,stroke=0)
    c.setFillColor(white);c.setFont('Interish-Bold',9);c.drawString(48,H-50,'PREMIUM UPGRADED EDITION · 2026')
    c.setFont('Serif-Bold',35);c.drawString(48,H-105,f'MYP Mathematics {year}')
    c.setFont('Serif',19);c.drawString(48,H-140,'Chapter Enrichment Studios')
    c.setFont('Interish',9);c.drawString(48,H-178,'Original coursebook preserved · targeted reasoning added to every chapter')
    c.setFillColor(HexColor('#2E3532'));c.setFont('Serif-Bold',18);c.drawString(48,H-270,'How the upgrade works')
    paras=[('DIRECTLY INTEGRATED','A two-page studio follows each original chapter. Original printed page numbers remain unchanged; enrichment pages use chapter labels such as Enrichment 3.7.'),('PROGRESSION','Each studio moves from Foundation to Application, Reasoning and Challenge. Tasks require interpretation, justification, modelling or ingenuity rather than repetitive volume.'),('VISUAL MATHEMATICS','Each chapter includes a reusable visual-thinking space: a graph, model, diagram or data display intended to be labelled, corrected or extended.'),('ASSESSMENT AND ATL','Prompts foreground communication, strategic checking, assumptions and reflection, supporting MYP Criteria A–D and thinking/self-management skills.'),('EDITORIAL NOTE','The separately generated educator reference contains concise answer checks. Open modelling tasks admit multiple valid solutions when assumptions are stated and defended.')]
    y=H-310
    for h,p in paras:
        c.setFillColor(color);c.setFont('Interish-Bold',8);c.drawString(48,y,h);y-=20
        y=draw_wrapped(c,p,48,y,W-96,'Serif',10,15,HexColor('#333735'));y-=24
    c.setFillColor(HexColor('#6A665E'));c.setFont('Interish',8);c.drawString(48,45,'Author: Sadikou Moukoddim · Head of Mathematics Department · Mathematics Teacher · Category 1')
    c.save()

def build_books():
    manifest={}
    for year,b in BOOKS.items():
        color=HexColor(b['color']); guide=MOD/f'MYP{year}_guide.pdf';make_guide(year,color,guide)
        modules=[]
        for ch,(title,end,kind,tasks,answers) in enumerate(b['chapters'],1):
            p=MOD/f'MYP{year}_chapter_{ch:02d}.pdf';make_module(year,ch,title,tasks,color,kind,p);modules.append((end,p,title))
        src=ROOT/b['file'];r=PdfReader(str(src));w=PdfWriter();
        # Keep original cover first, then guide, then original remainder; insert modules at verified chapter-end pages.
        w.add_page(r.pages[0]);
        for gp in PdfReader(str(guide)).pages:
            w.add_page(gp)
        insert_map={end + b.get('offset',0): (p,title,ch) for ch,(end,p,title) in enumerate(modules,1)}
        chapter_bookmarks=[]
        out_page=2
        for original_page in range(2,len(r.pages)+1):
            w.add_page(r.pages[original_page-1]);out_page+=1
            if original_page in insert_map:
                p,title,ch=insert_map[original_page]
                modreader=PdfReader(str(p)); first=len(w.pages)
                for mp in modreader.pages:w.add_page(mp)
                chapter_bookmarks.append((f'Enrichment {year}.{ch} · {title}',first))
        w.add_metadata({'/Title':f'MYP Mathematics {year} — Student Coursebook — Premium Upgraded Edition','/Author':'Sadikou Moukoddim','/Subject':'Original coursebook with chapter-by-chapter reasoning enrichment','/Keywords':'MYP mathematics inquiry reasoning challenge modelling'})
        try:
            w.add_outline_item('Premium Upgrade Guide',1)
            parent=w.add_outline_item('Chapter Enrichment Studios',1)
            for title,pno in chapter_bookmarks:w.add_outline_item(title,pno,parent=parent)
        except Exception: pass
        out=OUT/f'MYP_Mathematics_{year}_Student_Coursebook_Upgraded_2026.pdf'
        with open(out,'wb') as f:w.write(f)
        manifest[year]={'source':b['file'],'output':str(out.relative_to(ROOT)),'original_pages':len(r.pages),'new_pages':len(w.pages),'chapters':len(b['chapters'])}
    return manifest

def answer_reference(path):
    c=Canvas(str(path),pagesize=A4);c.setTitle('MYP Mathematics 1–5 Premium Enrichment — Educator Answer Reference');c.setAuthor('Sadikou Moukoddim')
    def newpage(year=None):
        c.setFillColor(HexColor('#F8F5EE'));c.rect(0,0,W,H,fill=1,stroke=0)
        c.setFillColor(HexColor('#1E4C47'));c.rect(0,H-70,W,70,fill=1,stroke=0);c.setFillColor(white);c.setFont('Serif-Bold',18);c.drawString(42,H-43,'Educator Answer Reference' if year is None else f'MYP Mathematics {year} · Answer Checks')
        c.setFillColor(HexColor('#6A665E'));c.setFont('Interish',7);c.drawString(42,25,'CONCISE CHECKING REFERENCE · NOT FOR INSERTION IN STUDENT BOOKS')
    newpage();c.setFillColor(HexColor('#26312E'));c.setFont('Serif-Bold',26);c.drawString(42,H-125,'Premium chapter enrichment')
    draw_wrapped(c,'Concise decisive results for all 56 chapter studios. Teachers should accept equivalent reasoning and defensible modelling assumptions. Open tasks require a method, not only a result.',42,H-160,W-84,'Serif',11,16);c.showPage()
    for year,b in BOOKS.items():
        newpage(year);y=H-100
        for ch,(title,end,kind,tasks,answers) in enumerate(b['chapters'],1):
            needed=42+sum(len(lines(c,a,'Serif',8.2,W-108))*11 for a in answers)
            if y-needed<48:c.showPage();newpage(year);y=H-100
            c.setFillColor(HexColor(b['color']));c.setFont('Interish-Bold',8);c.drawString(42,y,f'{year}.{ch}  {title.upper()}');y-=15
            for i,a in enumerate(answers,1):
                c.setFillColor(HexColor('#303532'));c.setFont('Interish-Bold',7.5);c.drawString(48,y,f'{i}.');
                y=draw_wrapped(c,a,65,y,W-108,'Serif',8.2,11,HexColor('#303532'));y-=3
            y-=10
        c.showPage()
    c.save()

def qa(manifest):
    issues=[]; expected={1:10,2:11,3:10,4:13,5:12}
    for year,b in BOOKS.items():
        if len(b['chapters'])!=expected[year]:issues.append(f'MYP{year}: chapter count')
        ends=[]
        for ch,(title,end,kind,tasks,answers) in enumerate(b['chapters'],1):
            ends.append(end)
            if len(tasks)!=4 or len(answers)!=4:issues.append(f'MYP{year}.{ch}: task/answer count')
            if [x[0] for x in tasks]!=['FOUNDATION','APPLICATION','REASONING','CHALLENGE']:issues.append(f'MYP{year}.{ch}: progression')
            if any(not x[1].strip() for x in tasks) or any(not a.strip() for a in answers):issues.append(f'MYP{year}.{ch}: blank')
        if ends!=sorted(ends):issues.append(f'MYP{year}: chapter ends unordered')
        p=ROOT/manifest[year]['output']; rr=PdfReader(str(p)); exp=manifest[year]['original_pages']+1+2*expected[year]
        if len(rr.pages)!=exp:issues.append(f'MYP{year}: pages {len(rr.pages)} != {exp}')
        # Every page must have a valid media box.
        for i,pg in enumerate(rr.pages):
            if float(pg.mediabox.width)<=0 or float(pg.mediabox.height)<=0:issues.append(f'MYP{year} page {i+1}: bad box')
    result={'status':'PASS' if not issues else 'FAIL','issues':issues,'manifest':manifest,'chapter_total':sum(len(b['chapters']) for b in BOOKS.values()),'new_student_tasks':sum(4*len(b['chapters']) for b in BOOKS.values())}
    (OUT/'qa_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    if issues:raise SystemExit('\n'.join(issues))
    return result

if __name__=='__main__':
    m=build_books();answer_reference(OUT/'MYP_1-5_Premium_Enrichment_Educator_Answer_Reference.pdf');print(json.dumps(qa(m),indent=2))
