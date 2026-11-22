#!/usr/bin/env python3
from pathlib import Path
import sys
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent))
from exercise_content import BOOKS
from reference_reconstructions import REFERENCE_PRACTICE
OUT=ROOT/'pedagogical_rebuild/MYP_1-5_Pedagogically_Integrated_Educator_Answer_Reference.pdf'
W,H=A4
pdfmetrics.registerFont(TTFont('Body','/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'));pdfmetrics.registerFont(TTFont('Bold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
def wrap(c,s,x,y,w,size=8.2,lead=11):
 for line in simpleSplit(s,'Body',size,w):c.drawString(x,y,line);y-=lead
 return y
def head(c,title):
 c.setFillColor(HexColor('#F9F7F1'));c.rect(0,0,W,H,fill=1,stroke=0);c.setFillColor(HexColor('#0B4D48'));c.rect(0,H-72,W,72,fill=1,stroke=0);c.setFillColor(white);c.setFont('Bold',17);c.drawString(40,H-44,title);c.setFillColor(HexColor('#77736B'));c.setFont('Bold',6.8);c.drawString(40,24,'EDUCATOR REFERENCE · INTEGRATED MIXED-PRACTICE REVISIONS · NOT FOR STUDENT INSERTION')
c=Canvas(str(OUT),pagesize=A4);c.setTitle('MYP Mathematics 1–5 Pedagogically Integrated Editions — Educator Answer Reference');c.setAuthor('Sadikou Moukoddim')
head(c,'Pedagogically Integrated Editions · Answer Reference');c.setFillColor(HexColor('#26312E'));c.setFont('Bold',22);c.drawString(40,H-125,'Integrated chapter exercise revisions');c.setFont('Body',11);wrap(c,'Decisive results and checking guidance for the 224 questions integrated into the existing mixed-practice pages of the five complete coursebooks. Accept equivalent valid reasoning and explicitly justified modelling assumptions.',40,H-165,W-80,11,16);c.showPage()
for year,b in BOOKS.items():
 head(c,f'MYP Mathematics {year} · Integrated Answer Checks');y=H-102
 for ch,(title,end,kind,tasks,answers) in enumerate(b['chapters'],1):
  need=38+sum((len(simpleSplit(a,'Body',8.2,W-112))*11+3) for a in answers)
  if y-need<48:c.showPage();head(c,f'MYP Mathematics {year} · Integrated Answer Checks');y=H-102
  c.setFillColor(HexColor(b['color']));c.setFont('Bold',8);c.drawString(40,y,f'{year}.{ch}  {title.upper()}');y-=16
  for i,a in enumerate(answers,1):
   c.setFillColor(HexColor('#303532'));c.setFont('Bold',7.5);c.drawString(48,y,f'{i}.');c.setFont('Body',8.2);y=wrap(c,a,65,y,W-112);y-=3
  y-=9
 c.showPage()
# Source-informed reconstructed practice answers
head(c,'Source-informed reconstructed practice · Answers');y=H-102
for key,data in REFERENCE_PRACTICE.items():
 year=key[0];chapter=int(key[1]);need=34+sum((len(simpleSplit(a,'Body',8.2,W-112))*11+3) for a in data['answers'])
 if y-need<48:c.showPage();head(c,'Source-informed reconstructed practice · Answers');y=H-102
 c.setFillColor(HexColor(BOOKS[year]['color']));c.setFont('Bold',8);c.drawString(40,y,f'MYP {year} · CHAPTER {chapter} · {data["title"].upper()}');y-=16
 for i,a in enumerate(data['answers'],1):
  c.setFillColor(HexColor('#303532'));c.setFont('Bold',7.5);c.drawString(48,y,f'{i}.');c.setFont('Body',8.2);y=wrap(c,a,65,y,W-112);y-=3
 y-=10
c.showPage();c.save();print(OUT)
