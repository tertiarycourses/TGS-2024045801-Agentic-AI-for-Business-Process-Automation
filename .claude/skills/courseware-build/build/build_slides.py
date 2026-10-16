#!/usr/bin/env python3
"""Generate the Agentic AI for Business Process Automation (TGS-2024045801) deck.

Style follows the reference decks in courseware/reference/ (Business Process
Automation with Power Automate and Copilot Studio Agents, and Agentic AI
Automation with n8n v47): white theme, kicker + bold title, an intro line, then
ONE visual structure per slide — chevron flow strips, outlined concept cards,
comparison panels, or a data table — closed by a takeaway band.

Hard rule carried over from the reference decks: the deck carries the CONCEPTS
and ONE visual slide per lab (chevron flow + real n8n canvas screenshot + LAB
band). The click-by-click steps live in the Learner Guide and never on a slide.

Content is driven entirely by course_data.py, concepts.py and data_domainN.py so
the deck stays 100% aligned with the LP, the LG and the labs.
"""
import os, sys, math
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import course_data as C
import concepts as CN
from data_domain1 import DOMAIN1
from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3
ACTIVITIES = DOMAIN1 + DOMAIN2 + DOMAIN3

def _find_repo(start):
    env = os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env):
        return env
    d = start
    for _ in range(8):
        d = os.path.dirname(d)
        if os.path.isdir(os.path.join(d, "courseware")) and os.path.isdir(os.path.join(d, "labs")):
            return d
    return os.path.dirname(os.path.dirname(HERE))
REPO = _find_repo(HERE)
ASSETS = os.path.join(os.path.dirname(HERE), "assets")      # skill-local brand assets
CWASSETS = os.path.join(REPO, "courseware", "assets")       # course diagram assets

# ---------------- palette ----------------
BLUE=RGBColor(0x1F,0x6F,0xEB); TEAL=RGBColor(0x10,0xB9,0x81); AMBER=RGBColor(0xF5,0x9E,0x0B)
INK=RGBColor(0x16,0x1B,0x26); GREY=RGBColor(0x5B,0x63,0x72); LIGHT=RGBColor(0xF5,0xF8,0xFC)
WHITE=RGBColor(0xFF,0xFF,0xFF); LINE=RGBColor(0xE2,0xE8,0xF0); VIOLET=RGBColor(0x7C,0x3A,0xED)
RED=RGBColor(0xC6,0x2F,0x2F); GREEN=RGBColor(0x12,0x7A,0x3E)
# concepts.py names colours as strings so the content module stays free of pptx imports
COLORS = dict(BLUE=BLUE, TEAL=TEAL, AMBER=AMBER, VIOLET=VIOLET, RED=RED, GREEN=GREEN, GREY=GREY)

prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
SW,SH=prs.slide_width,prs.slide_height
BLANK=prs.slide_layouts[6]
FONT="Arial"

def slide(): return prs.slides.add_slide(BLANK)
def rect(s,x,y,w,h,color,line=None):
    sp=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,x,y,w,h); sp.fill.solid(); sp.fill.fore_color.rgb=color
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb=line; sp.line.width=Pt(1)
    sp.shadow.inherit=False; return sp
def box(s,x,y,w,h,edge,fill=WHITE,lw=1.25,round_=True):
    sp=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if round_ else MSO_SHAPE.RECTANGLE,x,y,w,h)
    try: sp.adjustments[0]=0.055
    except Exception: pass
    sp.fill.solid(); sp.fill.fore_color.rgb=fill
    sp.line.color.rgb=edge; sp.line.width=Pt(lw); sp.shadow.inherit=False; return sp
def oval(s,x,y,w,h,color):
    sp=s.shapes.add_shape(MSO_SHAPE.OVAL,x,y,w,h); sp.fill.solid(); sp.fill.fore_color.rgb=color
    sp.line.fill.background(); sp.shadow.inherit=False; return sp
def txt(s,x,y,w,h,runs,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,space=4):
    tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True; tf.vertical_anchor=anchor
    tf.margin_left=tf.margin_right=Pt(0); tf.margin_top=tf.margin_bottom=Pt(0)
    if runs and not isinstance(runs[0],list): runs=[runs]
    first=True
    for para in runs:
        p=tf.paragraphs[0] if first else tf.add_paragraph(); first=False
        p.alignment=align; p.space_after=Pt(space); p.space_before=Pt(0)
        for (t,sz,col,bold) in para:
            r=p.add_run(); r.text=t; r.font.size=Pt(sz); r.font.bold=bold
            r.font.color.rgb=col; r.font.name=FONT
    return tb
def bullets(s,x,y,w,h,items,size=18,color=INK,gap=10,mcolor=BLUE):
    tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True
    tf.margin_left=tf.margin_right=Pt(0)
    first=True
    for it in items:
        lvl=0; text=it
        if isinstance(it,tuple): text,lvl=it[0],it[1]
        p=tf.paragraphs[0] if first else tf.add_paragraph(); first=False
        p.space_after=Pt(gap); p.space_before=Pt(0)
        rm=p.add_run(); rm.text=("   "*lvl)+("•  " if lvl==0 else "–  ")
        rm.font.size=Pt(size); rm.font.color.rgb=(mcolor if lvl==0 else GREY)
        rm.font.bold=True; rm.font.name=FONT
        r=p.add_run(); r.text=text; r.font.size=Pt(size-lvl); r.font.color.rgb=color; r.font.name=FONT
    return tb

# The cover is slide 1 but carries no footer, so the counter starts at 1: the
# first numbered slide is 2 and every printed footer then equals the slide's real
# position. Otherwise the Lesson Plan's "Slides 58-61" lands a slide early against
# what the learner reads in the corner of the page.
PAGE={"n":1}
def footer(s):
    PAGE["n"]+=1
    txt(s,Inches(0.55),Inches(7.08),Inches(6.2),Inches(0.3),
        [[(f"{C.SHORT_TITLE}  ·  {C.COURSE_CODE}",8.5,GREY,False)]])
    txt(s,Inches(6.0),Inches(7.08),Inches(6),Inches(0.3),
        [[("© 2026 Tertiary Infotech Academy Pte Ltd",8.5,GREY,False)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(11.9),Inches(7.08),Inches(0.9),Inches(0.3),
        [[(str(PAGE["n"]),9,GREY,True)]],align=PP_ALIGN.RIGHT)
def head(s,title,kicker=None,kcolor=BLUE):
    """Slide header. Returns the y at which body content may safely start.

    A long title is shrunk rather than allowed to wrap — a wrapped second line
    runs straight through the intro line beneath it."""
    rect(s,0,0,SW,SH,WHITE)
    y=Inches(0.55)
    if kicker:
        txt(s,Inches(0.8),Inches(0.5),Inches(11.8),Inches(0.34),[[(kicker,13,kcolor,True)]])
        y=Inches(0.82)
    # ~0.55 * pt gives the characters that fit across 12in of Arial bold
    size=28
    for lim,sz in ((56,28),(66,24),(78,21),(92,18)):
        if len(title)<=lim: size=sz; break
    else:
        size=16
    txt(s,Inches(0.8),y,Inches(12.0),Inches(0.85),[[(title,size,INK,True)]])
    # the accent bar tracks the kicker+title block, so it never stops short
    bar_h=Inches(0.66) if kicker else Inches(0.55)
    rect(s,Inches(0.55),Inches(0.60),Inches(0.14),bar_h,kcolor)
    return s
def _logo(name):
    p=os.path.join(ASSETS,name); return p if os.path.exists(p) else None
def _asset(name):
    p=os.path.join(CWASSETS,name); return p if os.path.exists(p) else None

# ---------------- reference-style building blocks ----------------
def intro_line(s,text,y=Inches(1.58)):
    txt(s,Inches(0.85),y,Inches(11.6),Inches(0.36),[[(text,12.5,GREY,False)]])
def chev_strip(s,items,y=Inches(2.0),h=Inches(1.05),color=BLUE,x0=Inches(0.85),
               tw=Inches(11.63),tsz=12.5,ssz=9):
    """Horizontal flow of outlined boxes joined by ▶ — items: (title, sub)."""
    n=len(items); gap=Inches(0.34)
    cw=int((tw-gap*(n-1))/n)
    for i,(t,sub) in enumerate(items):
        x=int(x0+(cw+gap)*i)
        box(s,x,y,cw,h,color)
        runs=[[(t,tsz,INK,True)]]
        if sub: runs.append([(sub,ssz,GREY,False)])
        txt(s,x+Inches(0.1),y,cw-Inches(0.2),h,runs,align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.MIDDLE,space=2)
        if i<n-1:
            txt(s,int(x+cw-Inches(0.03)),int(y+h/2-Inches(0.18)),int(gap+Inches(0.06)),Inches(0.36),
                [[("▶",12,color,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
def ncards(s,items,y=Inches(3.4),h=Inches(2.6),cols=2,numbered=True,bsz=10.5):
    """Grid of outlined cards — items: (color, title, body)."""
    n=len(items); rows=math.ceil(n/cols)
    X0=Inches(0.85); TOTW=Inches(11.63); gx=Inches(0.32); gy=Inches(0.24)
    cw=int((TOTW-gx*(cols-1))/cols); ch=int((h-gy*(rows-1))/rows)
    for i,(col,t,body) in enumerate(items):
        x=int(X0+(cw+gx)*(i%cols)); yy=int(y+(ch+gy)*(i//cols))
        box(s,x,yy,cw,ch,col)
        tx=x+Inches(0.22)
        if numbered:
            bd=Inches(0.34)
            oval(s,x+Inches(0.2),yy+Inches(0.16),bd,bd,col)
            txt(s,x+Inches(0.2),yy+Inches(0.16),bd,bd,[[(str(i+1),13,WHITE,True)]],
                align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
            txt(s,x+Inches(0.68),yy+Inches(0.17),cw-Inches(0.9),Inches(0.34),[[(t,13,col,True)]])
        else:
            txt(s,tx,yy+Inches(0.16),cw-Inches(0.44),Inches(0.34),[[(t,13,col,True)]])
        txt(s,tx,yy+Inches(0.6),cw-Inches(0.44),ch-Inches(0.76),[[(body,bsz,INK,False)]],space=3)
def takeaway(s,text,y=Inches(6.32),color=INK):
    box(s,Inches(0.85),y,Inches(11.63),Inches(0.46),LINE,fill=LIGHT,lw=1)
    txt(s,Inches(1.1),y,Inches(11.13),Inches(0.46),[[(text,12.5,color,True)]],anchor=MSO_ANCHOR.MIDDLE)
def data_table(s,widths,header,rows,y=Inches(2.0),rh=Inches(0.44),hcolor=BLUE,fsz=10.5):
    X0=Inches(0.85); xs=[X0]
    for w in widths: xs.append(int(xs[-1]+Inches(w)))
    for j,htxt in enumerate(header):
        rect(s,xs[j],y,int(Inches(widths[j])),rh,hcolor)
        txt(s,xs[j]+Inches(0.14),y,int(Inches(widths[j]))-Inches(0.28),rh,
            [[(htxt,11,WHITE,True)]],anchor=MSO_ANCHOR.MIDDLE)
    for i,row in enumerate(rows):
        yy=int(y+rh*(i+1)); fill=LIGHT if i%2 else WHITE
        for j,cell in enumerate(row):
            rect(s,xs[j],yy,int(Inches(widths[j])),rh,fill,line=LINE)
            txt(s,xs[j]+Inches(0.14),yy,int(Inches(widths[j]))-Inches(0.28),rh,
                [[(cell,fsz,INK,j==0)]],anchor=MSO_ANCHOR.MIDDLE)
    return int(y+rh*(len(rows)+1))
def pic_fit(s,img,x,y,maxw,maxh,border=True):
    """Place an image inside the box, scaled to fit and centred.

    The border is drawn around the PICTURE, not around the box — a tall narrow
    graph in a wide panel otherwise gets a frame of mostly empty white."""
    if not img or not os.path.exists(img): return None
    pic=s.shapes.add_picture(img,x,y,width=maxw)
    if pic.height>maxh:
        s.shapes._spTree.remove(pic._element)
        pic=s.shapes.add_picture(img,x,y,height=maxh)
    pic.left=int(x+(maxw-pic.width)/2)
    pic.top=int(y+(maxh-pic.height)/2)
    if border:
        ln=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,pic.left-Pt(1),pic.top-Pt(1),
                              pic.width+Pt(2),pic.height+Pt(2))
        ln.fill.background(); ln.line.color.rgb=LINE; ln.line.width=Pt(1); ln.shadow.inherit=False
    return pic
def concept_slide(kicker,title,intro=None,kcolor=BLUE):
    s=slide(); head(s,title,kicker,kcolor=kcolor)
    if intro: intro_line(s,intro)
    return s
def two_panel(title,ltitle,litems,rtitle,ritems,kicker=None,lcolor=BLUE,rcolor=VIOLET,
              take=None,intro=None):
    s=slide(); head(s,title,kicker,kcolor=lcolor)
    if intro: intro_line(s,intro)
    # Both panels always run to the takeaway band. Sizing them to their bullet
    # count left a visible dead strip whenever the two sides had different
    # lengths, which read as a layout bug rather than as breathing room.
    TOP=Inches(1.95); BOT=Inches(6.15)
    ph=BOT-TOP-Inches(0.5)
    for (x,w,t,items,col) in ((Inches(0.85),Inches(5.68),ltitle,litems,lcolor),
                              (Inches(6.8),Inches(5.68),rtitle,ritems,rcolor)):
        rect(s,x,TOP,w,Inches(0.5),col)
        txt(s,x,TOP,w,Inches(0.5),[[(t,14,WHITE,True)]],
            align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        box(s,x,TOP+Inches(0.5),w,ph,col,lw=1.25,round_=False)
        # indent any line the content module wrote with leading spaces (code samples)
        its=[(it.strip(),1) if it.startswith("   ") else (it,0) for it in items]
        bullets(s,x+Inches(0.3),TOP+Inches(0.72),w-Inches(0.6),ph-Inches(0.4),its,
                size=13,mcolor=col,gap=9)
    if take: takeaway(s,take)
    footer(s); return s

# ---------------- slide templates ----------------
def cover():
    s=slide(); rect(s,0,0,SW,SH,WHITE)
    rect(s,0,0,SW,Inches(0.22),BLUE); rect(s,0,Inches(7.28),SW,Inches(0.22),TEAL)
    org=_logo("tertiary-infotech-logo.png")
    if org: s.shapes.add_picture(org,Inches(0.85),Inches(0.7),height=Inches(1.05))
    n8n=_logo("n8n-logo.png") or _logo("n8n-course-logo.png")
    if n8n: s.shapes.add_picture(n8n,Inches(11.3),Inches(0.72),height=Inches(1.0))
    txt(s,Inches(0.9),Inches(2.3),Inches(12),Inches(0.6),[[("COURSE SLIDES  ·  WSQ",16,BLUE,True)]])
    txt(s,Inches(0.9),Inches(2.85),Inches(12.0),Inches(1.9),[[(C.TITLE,40,INK,True)]])
    rect(s,Inches(0.92),Inches(4.75),Inches(2.4),Inches(0.06),TEAL)
    txt(s,Inches(0.9),Inches(5.05),Inches(12),Inches(1.4),
        [[(f"WSQ Course Code: {C.COURSE_CODE}",16,GREY,False)],
         [(f"TSC: {C.TSC_TITLE}  ·  {C.TSC_CODE}",13,GREY,False)],
         [("Conducted by Tertiary Infotech Academy Pte Ltd  ·  UEN 201200696W",14,GREY,False)]],space=6)
    txt(s,Inches(0.9),Inches(6.5),Inches(12),Inches(0.4),
        [[(f"Version {C.VERSION}  ·  {C.VERSION_DATE}",12,BLUE,True)]])
    txt(s,Inches(0.9),Inches(6.85),Inches(12),Inches(0.34),
        [[("© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved.  ·  www.tertiarycourses.com.sg",10,GREY,False)]])

def section(kicker,title,n,sub="",applied="",color=BLUE):
    s=slide(); rect(s,0,0,SW,SH,WHITE)
    box(s,Inches(1.5),Inches(2.15),Inches(10.3),Inches(3.2),color,lw=1.5)
    rect(s,Inches(1.5),Inches(2.15),Inches(0.22),Inches(3.2),color)
    txt(s,Inches(2.1),Inches(2.5),Inches(9.3),Inches(0.4),[[(kicker,15,color,True)]])
    txt(s,Inches(2.1),Inches(2.95),Inches(9.4),Inches(1.2),[[(title,34,INK,True)]])
    if sub: txt(s,Inches(2.12),Inches(4.15),Inches(9.3),Inches(0.6),[[(sub,14,GREY,False)]])
    if applied: txt(s,Inches(2.12),Inches(4.75),Inches(9.3),Inches(0.4),[[(applied,12,color,True)]])
    txt(s,Inches(10.2),Inches(0.6),Inches(2.5),Inches(1.6),[[(n,72,LINE,True)]],align=PP_ALIGN.RIGHT)
    footer(s)
def content(title,items,kicker=None,size=20):
    s=slide(); head(s,title,kicker)
    bullets(s,Inches(0.85),Inches(1.9),Inches(11.6),Inches(4.9),items,size=size)
    footer(s); return s
def image_slide(title,imgname,caption="",kicker=None,accent=BLUE):
    s=slide(); head(s,title,kicker,kcolor=accent)
    pic_fit(s,_asset(imgname),Inches(1.0),Inches(1.9),Inches(11.3),Inches(4.5))
    if caption:
        txt(s,Inches(0.8),Inches(6.5),Inches(11.7),Inches(0.5),
            [[(caption,11.5,GREY,False)]],align=PP_ALIGN.CENTER)
    footer(s); return s
PALETTE=[BLUE,TEAL,VIOLET,AMBER]
def tile_grid(title,items,kicker=None,cols=2,size=15,icons=None,accent=BLUE):
    s=slide(); head(s,title,kicker,kcolor=accent)
    n=len(items); rows=math.ceil(n/cols)
    X0=Inches(0.85); Y0=Inches(1.95); TOTW=Inches(11.63); AREAH=Inches(4.78)
    gx=Inches(0.3); gy=Inches(0.26)
    cw=int((TOTW-gx*(cols-1))/cols); ch=int((AREAH-gy*(rows-1))/rows)
    MAXH=Inches(1.55)
    if ch>MAXH:
        ch=MAXH
        used=ch*rows+gy*(rows-1)
        Y0=int(Inches(1.95)+(AREAH-used)/2)
    bd=Inches(0.6)
    for i,it in enumerate(items):
        r=i//cols; c=i%cols
        x=int(X0+(cw+gx)*c); y=int(Y0+(ch+gy)*r); col=PALETTE[i%len(PALETTE)]
        rect(s,x,y,cw,ch,LIGHT); rect(s,x,y,Inches(0.1),ch,col)
        oval(s,x+Inches(0.28),int(y+ch/2-bd/2),bd,bd,col)
        ic=icons[i] if icons else str(i+1)
        txt(s,x+Inches(0.28),int(y+ch/2-bd/2),bd,bd,[[(ic,19,WHITE,True)]],
            align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        tx=x+Inches(1.08); tw=cw-Inches(1.32)
        if isinstance(it,tuple):
            hsize=size+2
            avail_chars=int(tw/Inches(0.085)/((size+2)/15.0))
            if len(it[0])>avail_chars: hsize=max(size-1, size+2-3)
            txt(s,tx,int(y+Inches(0.14)),tw,int(ch-Inches(0.2)),
                [[(it[0],hsize,INK,True)],[(it[1],size-2,GREY,False)]],
                anchor=MSO_ANCHOR.MIDDLE,space=3)
        else:
            txt(s,tx,int(y+Inches(0.1)),tw,int(ch-Inches(0.16)),[[(it,size,INK,False)]],
                anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s
def flow_h(title,steps,kicker=None,color=BLUE,size=14):
    s=slide(); head(s,title,kicker,kcolor=color)
    n=len(steps); X0=Inches(0.85); TOTW=Inches(11.63); gap=Inches(0.34)
    cw=int((TOTW-gap*(n-1))/n); y=Inches(2.55); ch=Inches(3.15); bd=Inches(0.82)
    for i,st in enumerate(steps):
        x=int(X0+(cw+gap)*i)
        rect(s,x,y,cw,ch,LIGHT); rect(s,x,y,cw,Inches(0.1),color)
        oval(s,int(x+cw/2-bd/2),int(y+Inches(0.42)),bd,bd,color)
        txt(s,int(x+cw/2-bd/2),int(y+Inches(0.42)),bd,bd,[[(str(i+1),30,WHITE,True)]],
            align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        txt(s,x+Inches(0.16),int(y+Inches(1.55)),cw-Inches(0.32),int(ch-Inches(1.7)),
            [[(st,size,INK,False)]],align=PP_ALIGN.CENTER)
        if i<n-1:
            txt(s,int(x+cw-Inches(0.04)),int(y+ch/2-Inches(0.3)),int(gap+Inches(0.08)),Inches(0.6),
                [[("▶",15,color,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s
def trainer_slide(kicker,name,role,rows,initials,accent=BLUE):
    s=slide(); head(s,"About the Trainer",kicker,kcolor=accent)
    lx=Inches(0.85); lw=Inches(3.65)
    rect(s,lx,Inches(1.95),lw,Inches(4.7),LIGHT); rect(s,lx,Inches(1.95),lw,Inches(0.12),accent)
    bd=Inches(1.7); ax=int(lx+(lw-bd)/2)
    oval(s,ax,Inches(2.5),bd,bd,accent)
    txt(s,ax,Inches(2.5),bd,bd,[[(initials,44,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    txt(s,lx+Inches(0.15),Inches(4.55),lw-Inches(0.3),Inches(0.6),[[(name,21,INK,True)]],align=PP_ALIGN.CENTER)
    txt(s,lx+Inches(0.15),Inches(5.2),lw-Inches(0.3),Inches(1.2),[[(role,13,GREY,False)]],align=PP_ALIGN.CENTER)
    rx=Inches(4.9); rw=Inches(7.6); ry=Inches(1.95); rh=Inches(4.7)
    n=len(rows); gy=Inches(0.2); th=int((rh-gy*(n-1))/n)
    for i,(label,val) in enumerate(rows):
        y=int(ry+(th+gy)*i); col=PALETTE[i%len(PALETTE)]
        rect(s,rx,y,rw,th,LIGHT); rect(s,rx,y,Inches(0.1),th,col)
        vruns=[(val,14,INK,False)] if val else [("____________________________________________",13,LINE,False)]
        txt(s,rx+Inches(0.32),y,rw-Inches(0.6),th,
            [[(label.upper(),11,col,True)],vruns],anchor=MSO_ANCHOR.MIDDLE,space=3)
    footer(s); return s
def brk(kind,dur,color=AMBER):
    s=slide(); rect(s,0,0,SW,SH,WHITE)
    rect(s,0,0,SW,Inches(0.22),color); rect(s,0,Inches(7.28),SW,Inches(0.22),color)
    rect(s,Inches(5.4),Inches(2.35),Inches(2.53),Inches(0.1),color)
    txt(s,0,Inches(2.75),SW,Inches(1.2),[[(kind,48,INK,True)]],align=PP_ALIGN.CENTER)
    txt(s,0,Inches(4.05),SW,Inches(0.8),[[(dur,22,color,True)]],align=PP_ALIGN.CENTER)
    footer(s)

# ---------------- the concept renderer ----------------
def render_concept(c,kicker,accent=BLUE):
    """Render one concepts.py block as a reference-style visual slide.

    Every kind ends with the takeaway band, so a slide is never a bare bullet
    wall — that is the whole point of matching the reference decks."""
    kind=c["kind"]; col=lambda name: COLORS[name]
    if kind=="cards":
        s=concept_slide(kicker,c["title"],c.get("intro"),kcolor=accent)
        cards=[(col(a),b,d) for a,b,d in c["cards"]]
        cols=c.get("cols",2)
        rows=math.ceil(len(cards)/cols)
        h=Inches(4.15) if rows>2 else Inches(3.9)
        ncards(s,cards,y=Inches(1.98),h=h,cols=cols,numbered=c.get("numbered",True),
               bsz=10 if cols>=4 else 10.5)
        takeaway(s,c["takeaway"]); footer(s); return s
    if kind=="cards2":
        s=concept_slide(kicker,c["title"],c.get("intro"),kcolor=accent)
        ncards(s,[(col(a),b,d) for a,b,d in c["cards"]],y=Inches(1.95),h=Inches(2.05),cols=3)
        ncards(s,[(col(a),b,d) for a,b,d in c["cards2"]],y=Inches(4.22),h=Inches(1.95),cols=3)
        takeaway(s,c["takeaway"]); footer(s); return s
    if kind=="chev+cards":
        s=concept_slide(kicker,c["title"],c.get("intro"),kcolor=accent)
        chev_strip(s,c["chevrons"],y=Inches(2.0),h=Inches(1.0),color=accent,
                   tsz=11.5 if len(c["chevrons"])>4 else 12.5,ssz=8.5)
        ncards(s,[(col(a),b,d) for a,b,d in c["cards"]],y=Inches(3.35),h=Inches(2.7),
               cols=c.get("cols",3),numbered=c.get("numbered",True))
        takeaway(s,c["takeaway"]); footer(s); return s
    if kind=="panels":
        lt,lc,li=c["left"]; rt,rc,ri=c["right"]
        return two_panel(c["title"],lt,li,rt,ri,kicker=kicker,lcolor=col(lc),rcolor=col(rc),
                         take=c["takeaway"],intro=c.get("intro"))
    if kind=="table":
        s=concept_slide(kicker,c["title"],c.get("intro"),kcolor=accent)
        data_table(s,c["widths"],c["header"],c["rows"],y=Inches(2.05),rh=Inches(0.5),hcolor=accent)
        takeaway(s,c["takeaway"]); footer(s); return s
    if kind=="json":
        s=concept_slide(kicker,c["title"],c.get("intro"),kcolor=accent)
        bullets(s,Inches(0.85),Inches(2.05),Inches(5.6),Inches(3.6),c["bullets"],size=14,gap=10)
        box(s,Inches(6.8),Inches(2.05),Inches(5.68),Inches(3.4),accent)
        txt(s,Inches(7.1),Inches(2.25),Inches(5.1),Inches(0.3),[[(c["code_title"],11,accent,True)]])
        txt(s,Inches(7.1),Inches(2.65),Inches(5.1),Inches(2.6),
            [[(ln,13,INK,False)] for ln in c["code"]],space=3)
        takeaway(s,c["takeaway"]); footer(s); return s
    if kind=="hub":
        s=concept_slide(kicker,c["title"],c.get("intro"),kcolor=accent)
        box(s,Inches(4.7),Inches(3.35),Inches(3.9),Inches(1.15),VIOLET,lw=2)
        txt(s,Inches(4.7),Inches(3.35),Inches(3.9),Inches(1.15),
            [[(c["hub"][0],15,VIOLET,True)],[(c["hub"][1],10.5,GREY,False)]],
            align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE,space=2)
        spots=[(Inches(0.85),Inches(2.05)),(Inches(8.85),Inches(2.05)),
               (Inches(0.85),Inches(4.55)),(Inches(8.85),Inches(4.55))]
        for (cname,t,body),(x,y) in zip(c["parts"],spots):
            cc=col(cname)
            box(s,x,y,Inches(3.6),Inches(1.6),cc)
            txt(s,x+Inches(0.2),y+Inches(0.14),Inches(3.2),Inches(0.32),[[(t,13,cc,True)]])
            txt(s,x+Inches(0.2),y+Inches(0.5),Inches(3.2),Inches(1.1),[[(body,10.5,INK,False)]],space=3)
        takeaway(s,c["takeaway"]); footer(s); return s
    if kind=="goodbad":
        s=concept_slide(kicker,c["title"],c.get("intro"),kcolor=accent)
        PH=Inches(3.5)
        box(s,Inches(0.85),Inches(2.0),Inches(5.68),PH,RED)
        txt(s,Inches(1.15),Inches(2.2),Inches(5.1),Inches(0.3),[[(c["bad_title"],12.5,RED,True)]])
        txt(s,Inches(1.15),Inches(2.62),Inches(5.1),Inches(1.0),[[(c["bad_quote"],13,INK,False)]])
        txt(s,Inches(1.15),Inches(3.95),Inches(5.1),Inches(1.4),
            [[(n,11,GREY,False)] for n in c["bad_notes"]],space=6)
        box(s,Inches(6.8),Inches(2.0),Inches(5.68),PH,GREEN)
        txt(s,Inches(7.1),Inches(2.2),Inches(5.1),Inches(0.3),[[(c["good_title"],12.5,GREEN,True)]])
        txt(s,Inches(7.1),Inches(2.62),Inches(5.15),Inches(2.7),
            [[(ln,12,INK,False)] for ln in c["good_lines"]],space=5)
        takeaway(s,c["takeaway"]); footer(s); return s
    raise ValueError(f"unknown concept kind: {kind}")

# ---------------- the lab slide (ONE per lab — steps live in the LG) ----------------
def lab_band(s,tag,name,meta,color=TEAL,y=Inches(6.28)):
    box(s,Inches(0.85),y,Inches(11.63),Inches(0.56),color,lw=1.25)
    rect(s,Inches(1.05),int(y+Inches(0.11)),Inches(1.05),Inches(0.34),color)
    txt(s,Inches(1.05),int(y+Inches(0.11)),Inches(1.05),Inches(0.34),
        [[(tag,12,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    txt(s,Inches(2.3),y+Inches(0.05),Inches(10.0),Inches(0.26),[[(name,12,INK,True)]])
    # the meta line is one line only — it is clipped if it wraps, so keep it short
    txt(s,Inches(2.3),y+Inches(0.30),Inches(10.0),Inches(0.24),[[(meta,8.5,GREY,False)]])
def lab_slide(kicker,tag,title,intro,flows,img,meta,cap="",color=TEAL):
    """ONE slide per lab: a short intro line, the workflow chevron strip(s), the
    real n8n canvas screenshot, and a LAB band. Click-by-click steps stay in the
    Learner Guide — that separation is the whole point of this layout."""
    s=slide(); head(s,title,kicker,kcolor=color)
    # The intro must fit ONE line above the chevrons or it runs under them, so the
    # lab data carries a short "desc" for the deck (and "desc_long" for the guide).
    # Fail the build rather than silently truncating: an ellipsis mid-sentence on a
    # slide reads as a defect, and the fix belongs in the source text.
    if intro:
        assert len(intro)<=175, (
            f"Lab intro is {len(intro)} chars and will not fit the slide's one-line intro. "
            f"Shorten 'desc' (keep the long form in 'desc_long'): {intro[:80]}...")
        intro_line(s,intro,y=Inches(1.56))
    y=Inches(2.02)
    for f in flows:
        chev_strip(s,f,y=y,h=Inches(0.8),color=color,tsz=11.0,ssz=8.5)
        y=int(y+Inches(0.94))
    CAP_Y=Inches(6.02)
    top=int(y+Inches(0.1)); maxh=int((CAP_Y if cap else Inches(6.18))-top)
    if img: pic_fit(s,img,Inches(0.85),top,Inches(11.63),maxh)
    if cap:
        assert len(cap)<=175, (
            f"Canvas caption is {len(cap)} chars and will not fit its one-line band. "
            f"Shorten it in the lab's 'canvas' entry: {cap[:80]}...")
        txt(s,Inches(0.85),CAP_Y,Inches(11.63),Inches(0.24),
            [[(cap,9,GREY,False)]],align=PP_ALIGN.CENTER)
    lab_band(s,tag,title.split("—",1)[-1].strip() if "—" in title else title,meta,color=color)
    footer(s); return s
def side_cards(s,items,x,y,w,h,bsz=10):
    """Numbered cards stacked in one column — items: (color, title, body)."""
    n=len(items); gy=Inches(0.16); ch=int((h-gy*(n-1))/n)
    for i,(col,t,body) in enumerate(items):
        yy=int(y+(ch+gy)*i)
        box(s,x,yy,w,ch,col)
        bd=Inches(0.3)
        oval(s,x+Inches(0.18),yy+Inches(0.14),bd,bd,col)
        txt(s,x+Inches(0.18),yy+Inches(0.14),bd,bd,[[(str(i+1),12,WHITE,True)]],
            align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        txt(s,x+Inches(0.6),yy+Inches(0.14),w-Inches(0.78),bd,[[(t,12.5,col,True)]],anchor=MSO_ANCHOR.MIDDLE)
        txt(s,x+Inches(0.2),yy+Inches(0.54),w-Inches(0.4),ch-Inches(0.62),[[(body,bsz,INK,False)]],space=2)
def flow_shot(d,kicker,acc=TEAL):
    """A real n8n canvas screenshot with a title, an intro line, one card per part of the flow and a takeaway.

    layout="side" puts the screenshot on the left at full height with the cards
    stacked beside it — for near-16:10 screenshots that the wide band would shrink."""
    s=concept_slide(kicker,d["title"],d["intro"],kcolor=acc)
    cards=[(COLORS[c],t,b) for c,t,b in d["cards"]]
    if d.get("layout")=="side":
        for _c,t,b in cards:
            assert len(b)<=200, f"Side card '{t}' is {len(b)} chars and will overflow its card: {b[:80]}..."
        pic_fit(s,_asset(d["img"]),Inches(0.85),Inches(1.95),Inches(6.75),Inches(4.2))
        side_cards(s,cards,Inches(7.9),Inches(1.95),Inches(4.58),Inches(4.2))
    else:
        pic_fit(s,_asset(d["img"]),Inches(0.85),Inches(1.95),Inches(11.63),Inches(2.55))
        ncards(s,cards,y=Inches(4.65),h=Inches(1.5),cols=len(cards),numbered=True,bsz=10)
    takeaway(s,d["takeaway"]); footer(s); return s

def chat_shot(d,kicker,acc=TEAL):
    """A portrait app screenshot on the right, explanation bullets on the left, and a takeaway."""
    s=slide(); head(s,d["title"],kicker,kcolor=acc)
    bullets(s,Inches(0.85),Inches(2.0),Inches(6.4),Inches(4.0),d["bullets"],size=14,gap=10,mcolor=acc)
    pic_fit(s,_asset(d["img"]),Inches(7.6),Inches(1.85),Inches(4.88),Inches(4.3))
    takeaway(s,d["takeaway"]); footer(s); return s

def website_lab(kicker,title,img,items,color=BLUE):
    s=slide(); head(s,title,kicker,kcolor=color)
    bullets(s,Inches(0.85),Inches(2.0),Inches(5.4),Inches(4.0),items,size=14,gap=9,mcolor=color)
    pic_fit(s,img,Inches(6.5),Inches(2.0),Inches(6.0),Inches(4.2))
    footer(s); return s

# ============================================================ BUILD
cover()

# ---------------------------------------------------------------- ADMIN
section("COURSE ADMINISTRATION","Welcome & Housekeeping","")
tile_grid("Digital Attendance (Mandatory)",[
 ("AM, PM and Assessment","It is mandatory to take all three digital attendances for WSQ-funded courses."),
 ("The QR code","The trainer or administrator displays the attendance QR code from the SSG portal."),
 ("Scan and submit","Scan it with your mobile phone camera and submit your attendance."),
 ("75% minimum","At least 75% attendance is required to be eligible for assessment and funding.")],
 kicker="TRAQOM · SSG DIGITAL ATTENDANCE",cols=2,size=15)
trainer_slide("YOUR TRAINER · GENERAL","Your Trainer","General Trainer template —\nto be completed by the trainer",
 [("Name",""),("Title / Designation",""),("Qualifications",""),
  ("Areas of expertise",""),("Training & industry experience",""),("Contact","")],
 initials="?",accent=GREY)
trainer_slide("YOUR TRAINER",C.TRAINER,"Principal Trainer\nTertiary Infotech Academy Pte. Ltd.",
 [("Role","Principal Trainer, Tertiary Infotech Academy Pte. Ltd."),
  ("Qualifications","PhD — specialises in AI, automation and software engineering."),
  ("Delivers","WSQ courses on agentic AI, workflow automation (n8n) and app development."),
  ("Founder","Founder and lead instructor at Tertiary Infotech / Tertiary Courses.")],
 initials="AA",accent=BLUE)
tile_grid("Let's Know Each Other",[
 ("Who you are","Your name, your organisation and your role."),
 ("Your starting point","Your experience with automation or AI tools — including none at all."),
 ("Your pain point","One business process in your work you would most like to automate."),
 ("Your goal","What you want to be able to build by the end of this course.")],
 kicker="ICE-BREAKER",cols=2,size=15)
tile_grid("Ground Rules",[
 "Set your mobile phone to silent mode.","Participate actively — no question is too small.",
 "Mutual respect: agree to disagree.","One conversation at a time.",
 "Be punctual; return from breaks on time.","75% attendance is required."],
 kicker="HOUSEKEEPING",cols=2,size=15)
image_slide("Login to LMS and Download Course Material","lms-login.png",
 "Log in at lms-tms.tertiaryinfotech.com with your registered email and the OTP sent to your inbox, "
 "then open this course to download the slides and Learner Guide.",
 kicker="COURSE PORTAL")
flow_h("Download Course Material",[
 "Go to lms-tms.tertiaryinfotech.com",
 "Enter your registered email and click Send OTP",
 "Key in the one-time password from your inbox",
 "Open this course and download the slides + Learner Guide",
 "Keep them open — the assessment is open book"],kicker="COURSE PORTAL · STEPS")
tile_grid("Get the Course Workflows",[
 ("Every lab ships a workflow","A ready-made n8n workflow (.json) sits in each lab's folder under labs/."),
 ("Import it","In n8n: Workflows → Add workflow → the '...' menu → Import from File → pick the lab .json."),
 ("Re-select your credentials","After importing, re-select YOUR OWN credentials on every node showing a warning."),
 ("Nothing of yours is shared","Imported workflows reference credential NAMES, not secrets — no key travels in the file.")],
 kicker="GET THE FLOWS",cols=2,size=14)
tile_grid("Skills Framework (TSC)",[
 ("TSC Title",C.TSC_TITLE),
 ("TSC Code",C.TSC_CODE),
 ("Mapped to the national framework","This WSQ course is mapped to the SkillsFuture Singapore Skills Framework."),
 ("Fully assessed","The assessment covers every Ability (A) and Knowledge (K) statement listed next.")],
 kicker="WSQ ALIGNMENT",cols=2,size=15)
two_panel("TSC Abilities and Knowledge",
 "ABILITIES (assessed by the PP)",[f"{c} {t}" for c,t in C.TSC_ABILITIES],
 "KNOWLEDGE (assessed by the WA)",[f"{c} {t}" for c,t in C.TSC_KNOWLEDGE],
 kicker="SKILLS FRAMEWORK",lcolor=BLUE,rcolor=TEAL)
two_panel(f"Lesson Plan — {C.DAYS} Days, {C.HOURS_PER_DAY} hours/day",
 f"DAY 1 — {C.DAY_THEMES[1]}",
 ["Topic 1: Why agentic AI, and why workflow first",
  "n8n fundamentals → Lab 1 — trigger, action and QR flyer",
  "AI agent building blocks and webhooks",
  "Lab 2 — Webhook and AI Agent",
  f"Timing: {C.DAY_TIMES[1]}"],
 f"DAY 2 — {C.DAY_THEMES[2]}",
 ["Topic 2: Agentic chatbot and human in the loop",
  "Lab 3 — Chatbot webhook",
  "Lab 4 — Human in the loop",
  "Topic 3: RAG",
  "Lab 5 — RAG customer care chatbot",
  "Final Assessment (WA + PP)",
  f"Timing: {C.DAY_TIMES[2]}"],
 kicker="SCHEDULE",lcolor=BLUE,rcolor=TEAL,take=C.TIMING_NOTE)
tile_grid("Learning Outcomes",[
 ("LO1 · n8n and AI agents","Explain what n8n and AI agents are, and build workflows using triggers and actions."),
 ("LO2 · Webhook-triggered agents","Implement AI agent applications triggered by webhooks and integrated with business systems."),
 ("LO3 · Agentic chatbots","Design agentic chatbot workflows that operate within business and regulatory constraints."),
 ("LO4 · Human in the loop","Apply human approval so that sensitive actions are authorised by a named person."),
 ("LO5 · RAG","Deploy Retrieval-Augmented Generation to ground an agent in your organisation's documents.")],
 kicker="WHAT YOU'LL ACHIEVE",cols=1,size=15)
s=concept_slide("COURSE JOURNEY","Five Connected Labs",
 "Each lab keeps the agent and changes one thing — the front door, the tools, the oversight, the knowledge.")
chev_strip(s,[("LAB 1","form → email"),("LAB 2","webhook + agent + tools"),("LAB 3","chatbot + memory"),
              ("LAB 4","human approval gate"),("LAB 5","RAG over documents")],
           y=Inches(2.05),h=Inches(1.05),color=TEAL)
ncards(s,[(BLUE,"The front door changes","Form Trigger in Lab 1 becomes a Webhook in Labs 2–5 — the workflow behind it barely moves."),
 (TEAL,"The agent gains abilities","Lab 2 adds tools, Lab 3 adds memory, Lab 5 adds retrieval over your own documents."),
 (AMBER,"The oversight grows","Lab 4 stops the workflow dead until a licensed person approves what the agent drafted.")],
 y=Inches(3.45),h=Inches(2.6),cols=3)
takeaway(s,"By Lab 5 you have built the whole pattern: a front door, an agent, its tools, its guardrails and its knowledge.")
footer(s)
tile_grid("Criteria for Funding",[
 ("75% attendance","A minimum attendance rate of 75%, based on the SSG Digital Attendance record."),
 ("Assessed Competent","Complete the assessment and be assessed as 'Competent'."),
 ("Both are required","Both criteria must be met for the course fee funding to be granted.")],
 kicker="WSQ FUNDING",cols=1,size=16)
tile_grid("Briefing for Assessment",[
 "Place phones and other materials under the table or on the floor.",
 "No photos or recording of assessment scripts.",
 "No discussion during the assessment.",
 "Use a black or blue pen for hard-copy assessments.",
 "No liquid paper or correction tape.",
 "Scripts are collected when time is up."],
 kicker="ASSESSMENT BRIEFING",cols=2,size=15,accent=AMBER)
tile_grid("Assessment",[
 ("Written Assessment (SAQ)","1 hour. Short-answer questions covering the course knowledge."),
 ("Practical Performance (PP)","1 hour. Hands-on n8n build tasks drawn from the five labs."),
 ("Open book","Slides, Learner Guide and approved materials only."),
 ("75% attendance",C.ASSESSMENT["note"]),
 ("Appeals","An appeal process is available if required.")],
 kicker="FINAL ASSESSMENT",cols=1,size=14)
flow_h("Assessment Flow",[
 "TRAQOM survey — scan the QR code on the LMS",
 "Assessment digital attendance — scan the SSG QR",
 "Sit WA (SAQ) then PP — open book",
 "Submit your answers on the LMS",
 "Sign the Assessment Summary Record"],kicker="ON ASSESSMENT DAY")

# ---------------------------------------------------------------- TOPIC 1 OPENER
# Why agentic AI, and why workflow first. These slides open Topic 1 straight after
# its section divider (there is no separate Foundation section). slide_index.py
# counts them as TOPIC1_INTRO — keep the two in step.
def principle_cols(s,items,y=Inches(2.05),h=Inches(4.0)):
    """Five numbered columns — items: (color, title, kicker, body)."""
    n=len(items); X0=Inches(0.85); TOTW=Inches(11.63); gx=Inches(0.22)
    cw=int((TOTW-gx*(n-1))/n); bd=Inches(0.5)
    for i,(col,t,k,body) in enumerate(items):
        x=int(X0+(cw+gx)*i)
        box(s,x,y,cw,h,col)
        oval(s,int(x+cw/2-bd/2),y+Inches(0.22),bd,bd,col)
        txt(s,int(x+cw/2-bd/2),y+Inches(0.22),bd,bd,[[(str(i+1),16,WHITE,True)]],
            align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        txt(s,x+Inches(0.12),y+Inches(0.85),cw-Inches(0.24),Inches(0.62),[[(t,13.5,col,True)]],
            align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        txt(s,x+Inches(0.12),y+Inches(1.5),cw-Inches(0.24),Inches(0.3),[[(k,9,GREY,True)]],
            align=PP_ALIGN.CENTER)
        txt(s,x+Inches(0.18),y+Inches(1.9),cw-Inches(0.36),h-Inches(2.0),[[(body,11,INK,False)]],
            align=PP_ALIGN.CENTER,space=3)
def source_note(s,text,y=Inches(5.9)):
    txt(s,Inches(0.85),y,Inches(11.63),Inches(0.3),[[(text,9,GREY,False)]],align=PP_ALIGN.RIGHT)

# n8n training accounts for this run (18 Oct class) — replace when the class changes
N8N_ACCOUNTS=[f"n8n18oct{i}@tertiaryinfotech.com" for i in range(1,13)]
# The password is NEVER written in source: the repo is public. It is read from the
# gitignored .env (N8N_PASSWORD=...) for the class deck that goes to Drive/TMS.
# PUBLIC_BUILD=1 (the GitHub copy) forces the placeholder.
def _env(key):
    if os.environ.get(key): return os.environ[key]
    try:
        for ln in open(os.path.join(REPO,".env")):
            if ln.strip().startswith(key+"="): return ln.split("=",1)[1].strip()
    except OSError: pass
    return None
N8N_PASSWORD=None if os.environ.get("PUBLIC_BUILD") else _env("N8N_PASSWORD")
def topic1_intro(acc):
    k=lambda x: f"TOPIC 1 · {x}"
    # 1 — a brief history of AI, 2023–2026
    s=concept_slide(k("A BRIEF HISTORY OF AI"),"A Brief History of AI, 2023–2026",
     "Each year moved the skill that matters — from the words you type to the system you build.",kcolor=acc)
    chev_strip(s,[("Prompt Engineering","2023"),("Context Engineering","2024"),
                  ("Harness Engineering","2025"),("AI Agents","2026")],y=Inches(2.05),h=Inches(1.0),color=acc)
    ncards(s,[(BLUE,"Wording the prompt","ChatGPT goes mainstream. Results depend on how well you word the prompt."),
     (TEAL,"Curating the context","Models call tools and MCP launches. Results depend on the documents, data and tools you supply."),
     (VIOLET,"Building the harness","Claude Code and Codex: systems that plan, act and check their own work in a loop."),
     (AMBER,"Agents at work","Always-on agents work 24/7 — OpenClaw, Hermes Agent and agent teams take on whole jobs.")],
     y=Inches(3.35),h=Inches(2.7),cols=4,numbered=False,bsz=11)
    takeaway(s,"From wording one prompt → curating context → engineering the harness → AI agents that work around the clock.")
    footer(s)
    # generative AI vs agentic AI — straight after the history, before AI agents
    render_concept(CN.BY_KEY["gen_vs_agentic"],k("GENERATIVE VS AGENTIC AI"),accent=acc)
    # 2 — agentic AI vs AI agents
    two_panel("Agentic AI vs AI Agents",
     "Agentic AI — the broad category",[
      "Any AI system that pursues a goal over many steps: plans, acts through tools, checks the result",
      "Usually started by a person or a trigger, and stops when the task is done",
      "Built as a workflow with AI steps, or around an LLM loop",
      "Includes the orchestration, guardrails and human approvals",
      "Examples: a Claude Code or Codex session; an n8n workflow with AI steps"],
     "AI Agents — always-on agentic AI",[
      "A special type of agentic AI system that exists 24/7",
      "Usually installed in the cloud, so it serves all the time — no laptop needs to be open",
      "Waits for events — messages, emails, webhooks, schedules — and acts on them around the clock",
      "Keeps its memory across conversations and days",
      "Examples: OpenClaw, Hermes Agent, an n8n agent on a cloud instance behind a webhook"],
     kicker=k("AGENTIC AI VS AI AGENTS"),lcolor=acc,rcolor=VIOLET,
     intro="AI agents are a special type of agentic AI system — the kind that never switches off.",
     take="Every AI agent is agentic AI, but not every agentic AI is an AI agent — an AI agent is always on, serving 24/7 from the cloud.")
    # 3 — workflow first vs agent first
    s=concept_slide(k("WORKFLOW FIRST VS AGENT FIRST"),"Workflow First vs Agent First",
     "Workflow first evolves rule-based (RPA) automation: the workflow owns the path, and its steps can be AI or AI agents, as in n8n.",
     kcolor=acc)
    data_table(s,[2.5,4.55,4.58],["","Workflow First","Agent First"],[
     ["Who decides the path","The workflow — steps may be AI nodes or AI Agent nodes","The agent decides the steps and tools at run time"],
     ["Behaviour","Deterministic — same input, same path, every time","Probabilistic — the path can change between runs"],
     ["Efficiency","More effort to design every branch up front","Efficient — one instruction replaces many hand-built branches"],
     ["Reliability & testing","Easy to test, debug and certify step by step","Harder to test; edge cases surface in production"],
     ["Cost & speed","An LLM call only where needed — cheap and fast","An LLM call at every step — more tokens, more latency"],
     ["Best for","Repeatable, regulated, high-volume processes","Open-ended tasks with unpredictable inputs"]],
     y=Inches(2.05),rh=Inches(0.5),hcolor=acc)
    source_note(s,"Source: n8n, In The Loop 2026 — opening keynote and product direction (youtube.com/watch?v=KQRe5UurLQ0)")
    takeaway(s,"Workflow first is more deterministic; agent first is more efficient. Companies make as much deterministic as they can.")
    footer(s)
    # 4 — the trend: AI-assisted workflow creation
    s=concept_slide(k("THE MODERN VIEW"),"The Trend: AI-Assisted Workflow Creation",
     "AI-powered coding has flipped the trade-off — the agent's efficiency goes into BUILDING the workflow, not running it.",
     kcolor=acc)
    chev_strip(s,[("Describe","the process in plain English"),("n8n Assistant","or Claude Code / Codex drafts it"),
                  ("You review","test and approve it"),("Workflow runs","deterministic and logged"),
                  ("AI and agent nodes","where judgement is needed")],y=Inches(2.05),h=Inches(1.0),color=acc,
               tsz=11.5,ssz=8.5)
    ncards(s,[(BLUE,"Companies want determinism","Reliability, compliance and audit push businesses to make as much of a process deterministic as possible."),
     (VIOLET,"AI coding made it cheap","n8n Assistant, Claude Code and Codex are AI agents themselves — they make designing, building and changing workflows fast and cheap."),
     (TEAL,"The best of both","An AI agent BUILDS the workflow; a deterministic workflow RUNS the process, with AI and AI Agent nodes where judgement is needed.")],
     y=Inches(3.35),h=Inches(2.7),cols=3)
    takeaway(s,"The trend: AI-assisted workflow creation — the AI builds the workflow, and the workflow runs the business process.")
    footer(s)
    # platform tiers — AI now assists every tier
    s=concept_slide(k("COMPLEXITY VS CUSTOMISATION"),"Where AI Agent Platforms Sit",
     "Three tiers — and AI now helps build at every one of them. This course teaches the middle one.",kcolor=acc)
    TIERS=[(BLUE,"No-code",[("HOW YOU BUILD","Drag and drop in a fully visual builder."),
                            ("CUSTOMISATION","Lowest. Fastest route to a working agent, least control over the internals.")]),
           (TEAL,"Low-code  ·  n8n",[("HOW YOU BUILD","AI-assisted: n8n Assistant, Claude Code or Codex drafts the workflow on a visual canvas."),
                            ("CODE WHEN NEEDED","Add JavaScript or Python in a Code node where a built-in node is not enough."),
                            ("CUSTOMISATION","High. 400+ integrations, self-host or cloud. This course's platform.")]),
           (VIOLET,"Full-code",[("HOW YOU BUILD","AI generates the code — Claude Code or Codex write it, instead of coding manually."),
                            ("CUSTOMISATION","Highest — the most customisable tier. SDKs and frameworks such as LangChain, with real engineering effort to test and run.")])]
    X0=Inches(0.85); gx=Inches(0.32); cw=int((Inches(11.63)-gx*2)/3); y0=Inches(2.05); ch=Inches(3.55)
    for i,(col,t,rows) in enumerate(TIERS):
        x=int(X0+(cw+gx)*i); box(s,x,y0,cw,ch,col)
        bd=Inches(0.34); oval(s,x+Inches(0.2),y0+Inches(0.16),bd,bd,col)
        txt(s,x+Inches(0.2),y0+Inches(0.16),bd,bd,[[(str(i+1),13,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        txt(s,x+Inches(0.68),y0+Inches(0.17),cw-Inches(0.9),Inches(0.34),[[(t,14,col,True)]])
        paras=[]
        for lab_,val in rows: paras+= [[(lab_,9,col,True)],[(val,11,INK,False)]]
        txt(s,x+Inches(0.22),y0+Inches(0.66),cw-Inches(0.44),ch-Inches(0.8),paras,space=4)
    # the axis: customisation (and effort) grows left to right
    ar=s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,X0,Inches(5.72),Inches(11.63),Inches(0.4))
    ar.fill.solid(); ar.fill.fore_color.rgb=LIGHT; ar.line.color.rgb=LINE; ar.shadow.inherit=False
    txt(s,X0+Inches(0.3),Inches(5.72),Inches(10.8),Inches(0.4),
        [[("Less control, less effort   ·   more customisation, more engineering effort  →",10.5,GREY,True)]],
        align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    takeaway(s,"AI drafts the workflow in low-code and writes the code in full-code. n8n: analysts build it, engineers extend it.")
    footer(s)
    # 10 — business value, the modern view
    s=concept_slide(k("WHY ORGANISATIONS ADOPT IT"),"Business Value of Workflow-First Agentic Automation",
     "The modern view: what a business gains when AI builds the workflow and the workflow runs the process.",kcolor=acc)
    ncards(s,[(BLUE,"Reliable and predictable","The same input follows the same path every time, so the process can be tested and trusted like software."),
     (TEAL,"Secure by design","Each step holds only the data and credentials it needs; risky actions wait at an approval gate."),
     (VIOLET,"Auditable end to end","Every run is logged node by node — you can explain, replay and correct any decision."),
     (AMBER,"Lower running cost","Deterministic steps cost nothing in tokens; the LLM is called only where judgement is needed."),
     (GREEN,"Faster to build and change","Claude Code and Codex draft the workflow in minutes; your team reviews, tests and owns it."),
     (RED,"Scale around the clock","Triggers respond in real time, 24/7 — ten times the volume costs compute, not ten more hires.")],
     y=Inches(1.98),h=Inches(4.15),cols=3)
    takeaway(s,"AI where judgement is needed, workflow everywhere else — reliability you can audit, at a cost you can predict.")
    footer(s)
    # 11 — use cases
    s=concept_slide(k("USE CASES"),"Where Agentic Automation Is Used",
     "The same pattern — trigger, agent, tools, oversight — recurs across every function.",kcolor=acc)
    ncards(s,[(BLUE,"Customer service","Answer enquiries from your own documents, capture leads, and escalate what needs a person."),
     (TEAL,"Finance & accounting","Invoice processing, bank reconciliation, accounts-payable routing and exception handling."),
     (VIOLET,"Risk & compliance","Screen applications, flag anomalies, and route sensitive cases for human review."),
     (AMBER,"HR & people ops","Onboarding, leave applications, policy questions and approval chains."),
     (GREEN,"Sales & marketing","Lead qualification, follow-up sequencing, CRM enrichment and content drafting."),
     (RED,"Operations","Order processing, status notifications, document generation and reporting.")],
     y=Inches(1.98),h=Inches(4.15),cols=3)
    takeaway(s,"Every one of these is a front door, an agent, some tools and a decision about where the human belongs.")
    footer(s)
    # 8 — five principles of AI security
    s=concept_slide(k("AI SECURITY"),"5 Principles of AI Security",
     "Agents act on your behalf. These five controls keep what they can see and do safe, reviewable and accountable.",
     kcolor=RED)
    principle_cols(s,[(BLUE,"Data Control","WHAT AI CAN SEE",
       "Classify your data — public, internal, confidential — and decide exactly which data the AI may access."),
     (TEAL,"Permission Control","WHAT AI CAN DO",
       "Grant only the rights needed — read, write, edit, delete. Ask before anything destructive."),
     (VIOLET,"Human in the Loop","WHO APPROVES",
       "A person reviews and approves high-impact actions — payments, deletions, customer emails."),
     (AMBER,"Traceability","WHAT HAPPENED",
       "Log every prompt, tool call and change so actions can be audited, explained and rolled back."),
     (RED,"Right-Sized Models","NOT THE MOST POWERFUL",
       "The smallest model that does the job carries less autonomy and less risk than the most powerful one.")])
    takeaway(s,"In n8n: scoped credentials per node, approval gates (Send and Wait), the Executions log, and a small model per AI step.")
    footer(s)
    # 9 — why workflow first is more secure
    s=concept_slide(k("AI SECURITY"),"Workflow First vs Agent First — AI Security",
     "A fixed path limits the blast radius: a manipulated AI step cannot reach tools that are not wired to it.",
     kcolor=RED)
    data_table(s,[2.5,4.55,4.58],["Principle","Workflow First","Agent First"],[
     ["Data control","Each node sees only the fields wired into it","The agent can reach any data its tools expose"],
     ["Permission control","Each credential is scoped to one node and one action","The agent holds every tool's rights at once"],
     ["Human in the loop","The approval gate sits at a fixed, designed step","Depends on the agent choosing to ask"],
     ["Traceability","Every run is logged node by node in Executions","Reasoning varies run to run and is harder to explain"],
     ["Right-sized models","A small model for each narrow AI step","One capable model with broad autonomy"]],
     y=Inches(2.05),rh=Inches(0.56),hcolor=RED)
    takeaway(s,"The path is fixed, so every control is designed in rather than hoped for — that is why regulated processes stay workflow first.")
    footer(s)
    # 5b — what n8n is: a workflow-first agentic AI platform
    for key in CN.TOPIC1_OPENER_CONCEPTS: render_concept(CN.BY_KEY[key],k("WHAT IS n8n"),accent=acc)
    # 6a — the n8n training accounts
    s=concept_slide(k("TRAINING ACCOUNTS"),"n8n Training Accounts",
     "Each learner signs in to n8n with ONE assigned account. Use only the account your trainer gives you.")
    _h=len(N8N_ACCOUNTS)//2
    data_table(s,[0.8,5.0,0.8,5.03],["#","Account (email)","#","Account (email)"],
     [[str(i+1),N8N_ACCOUNTS[i],str(i+1+_h),N8N_ACCOUNTS[i+_h]] for i in range(_h)],
     y=Inches(2.05),rh=Inches(0.52),hcolor=BLUE,fsz=12)
    takeaway(s,(f"Password for every account:  {N8N_PASSWORD}   ·   Do not change the password or save real credentials in it."
                if N8N_PASSWORD else "Password: provided by your trainer in class   ·   Do not change the password or save real credentials in it."))
    footer(s)
    # 6b — sign in to n8n
    s=flow_h("Sign In to n8n",[
     "Go to app.n8n.cloud/login — or open your own instance URL directly",
     "Enter your assigned account email, e.g. n8n18oct5@tertiaryinfotech.com",
     ("Enter the password: "+N8N_PASSWORD) if N8N_PASSWORD else "Enter the password your trainer gives you",
     "Open your instance from the dashboard — a free 14-day trial, active through the training",
     "You land in n8n — open Assistant or Overview to start building"],
     kicker=k("SIGN IN"),color=acc)
    takeaway(s,"Your account is already set up — the name is your email prefix and onboarding is done. Do not change the password.")
    # 5 — n8n Assistant screenshot
    image_slide("n8n Assistant — Describe It, n8n Builds It","n8n-assistant.png",
     "Open Assistant in the left sidebar and answer \"What do you want to automate?\". It plans, builds and tests a normal n8n "
     "workflow you can inspect, edit and publish. Assistant chats use the plan's monthly Assistant credits.",
     kicker=k("AI-ASSISTED WORKFLOW CREATION"),accent=acc)
    # 7 — demo: AI-assisted workflow creation
    s=concept_slide(k("DEMO"),"Demo: Build a Social Media Campaign Workflow with n8n Assistant",
     "Give n8n Assistant one clear prompt — it plans and builds the workflow below, with a human approval gate.",kcolor=acc)
    chev_strip(s,[("Form Trigger","you enter a topic"),("Research","AI Agent + web search"),
                  ("Draft post","AI writes the copy"),("Human in the loop","email approve / reject"),
                  ("Schedule post","wait, then publish")],y=Inches(2.0),h=Inches(0.95),color=acc,tsz=11.5,ssz=8.5)
    box(s,Inches(0.85),Inches(3.15),Inches(7.2),Inches(2.95),VIOLET)
    txt(s,Inches(1.1),Inches(3.27),Inches(6.8),Inches(0.3),[[("THE PROMPT",11,VIOLET,True)]])
    txt(s,Inches(1.1),Inches(3.6),Inches(6.8),Inches(2.45),[[(ln,10.5,INK,False)] for ln in C.DEMO_PROMPT],space=2)
    box(s,Inches(8.3),Inches(3.15),Inches(4.18),Inches(2.95),TEAL)
    txt(s,Inches(8.55),Inches(3.27),Inches(3.8),Inches(0.3),[[("THEN YOU",11,TEAL,True)]])
    bullets(s,Inches(8.55),Inches(3.62),Inches(3.75),Inches(2.4),[
     "Review the plan before it builds","Connect Gmail and the social account when it asks",
     "Test with a real topic and approve the draft","Publish only when the run looks right"],size=11.5,mcolor=TEAL,gap=6)
    takeaway(s,"The AI built it; the workflow runs it — and nothing is posted until a person approves the draft.")
    footer(s)

def free_ai_credits(acc):
    # claim the free AI credits — taught with the Model, just before Lab 2 needs it
    k=lambda x: f"TOPIC 1 · {x}"
    s=flow_h("Claim Your Free AI Credits",[
     "Sign in to n8n Cloud with your training account — the free trial includes Gateway credits",
     "Open a workflow and add an AI node, e.g. AI Agent → Gemini or OpenAI Chat Model",
     "In the node's Credential field, choose Use Gateway credits — your balance shows beside it",
     "Pick a supported model and run the node — no provider account or API key needed",
     "Track the balance on the node, or in Admin Panel → Gateway credits"],
     kicker=k("FREE AI CREDITS"),color=TEAL)
    takeaway(s,"A red \"Free AI credits — Enable to claim credits\" toast is the legacy OpenAI offer: Gateway instances don't get it. Use Gateway credits.")

def telegram_demo(acc):
    """Chatbot demo before Lab 3 (Lab 3 itself stays the website chatbot): learners create a Telegram
    bot with BotFather, build the HR chatbot with n8n Assistant from one prompt, then connect and chat."""
    D=C.TELEGRAM_DEMO; k=lambda x: f"TOPIC 2 · {x}"
    s=concept_slide(k("DEMO"),"Demo: An HR Policy Chatbot on Telegram",
     "What is a chatbot? An agent behind a chat channel. Build one on Telegram first — then Lab 3 puts one behind a website.",kcolor=acc)
    chev_strip(s,D["flow"],y=Inches(2.0),h=Inches(0.95),color=acc,tsz=12.5,ssz=8.5)
    ncards(s,[(BLUE,"What Ava knows","Sample HR policies written into the system instruction — leave, sick leave, claims, hours, probation."),
              (RED,"Guardrails in the prompt","Answer only from the policies, never invent a number, and refer salary, medical or disciplinary questions to HR."),
              (TEAL,"Same agent, new front door","Telegram Trigger is the front door here. Lab 3 puts the same kind of agent behind a website.")],
           y=Inches(3.3),h=Inches(2.75),cols=3)
    takeaway(s,"You will: create a bot with BotFather  →  build the workflow with n8n Assistant  →  connect, publish and chat.")
    footer(s)
    # step 1 — the bot
    s=flow_h("Demo Step 1: Create a Telegram Bot with BotFather",[x[0] for x in D["botfather"]],
             kicker=k("DEMO · TELEGRAM BOT"),color=acc,size=12)
    takeaway(s,"The token is the bot's password — never share or commit it. If it leaks, send /revoke to BotFather for a new one.")
    # step 2 — n8n Assistant builds the workflow from one prompt
    chat_shot(D["assistant_shot"],k("DEMO · n8n ASSISTANT"),acc=acc)
    s=concept_slide(k("DEMO · n8n ASSISTANT"),"Demo Step 2: Paste the Prompt into n8n Assistant",
     "Create a new workflow, open n8n Assistant and paste this prompt — it plans and builds the chatbot for you.",kcolor=acc)
    box(s,Inches(0.85),Inches(2.0),Inches(7.2),Inches(4.05),VIOLET)
    txt(s,Inches(1.1),Inches(2.12),Inches(6.8),Inches(0.3),[[("THE PROMPT",11,VIOLET,True)]])
    txt(s,Inches(1.1),Inches(2.5),Inches(6.8),Inches(3.45),[[(ln,12,INK,False)] for ln in D["prompt"]],space=4)
    box(s,Inches(8.3),Inches(2.0),Inches(4.18),Inches(4.05),TEAL)
    txt(s,Inches(8.55),Inches(2.12),Inches(3.8),Inches(0.3),[[("THEN YOU",11,TEAL,True)]])
    bullets(s,Inches(8.55),Inches(2.5),Inches(3.75),Inches(3.45),D["review"],size=12.5,mcolor=TEAL,gap=8)
    takeaway(s,f"Reference solution: labs/lab3-chatbot-webhook/{D['file']}")
    footer(s)
    flow_shot(D["flow_shot"],k("DEMO · THE WORKFLOW IN n8n"),acc=acc)
    # step 3 — credentials, publish, chat
    s=flow_h("Demo Step 3: Connect the Bot, Publish and Chat",[x[0] for x in D["connect"]],
             kicker=k("DEMO · TELEGRAM BOT"),color=acc)
    takeaway(s,"A Telegram bot has ONE webhook at a time — testing in the editor swaps in the Test URL, so publish again when you are done.")
    chat_shot(D["chat_shot"],k("DEMO · TELEGRAM BOT"),acc=acc)

# ---------------------------------------------------------------- TOPICS + LABS
KICKERS={1:"TOPIC 1 · n8n AND AI AGENTS",2:"TOPIC 2 · AGENTIC CHATBOT & HITL",3:"TOPIC 3 · RAG"}
ACCENTS={1:BLUE,2:AMBER,3:VIOLET}
# a generic n8n UI screenshot shown right after the concept it illustrates
CONCEPT_IMAGES={
 "trigger_nodes":("n8n-triggers.png","Trigger Nodes on the n8n Canvas",
   "n8n trigger nodes: Manual · Schedule · WhatsApp · Telegram · Gmail · Chat · Form · Webhook"),
 "data_nodes":("n8n-key-nodes.png","Data-Processing Nodes on the Canvas",
   "If · Switch · Filter · Edit Fields · Split Out · Aggregate · Merge · Loop · Date & Time · Wait · Code"),
 "test_vs_prod_exec":("n8n-execution-history.png","Execution History",
   "The Executions tab — every run shows its status, duration, ID and the full data at each node"),
 "what_is_webhook":("n8n-webhook.png","Webhook Nodes in n8n",
   "The Webhook node starts the workflow when it is called; Respond to Webhook returns data to the caller"),
 "webhook_vs_http":("n8n-http-request.png","The HTTP Request Node",
   "The HTTP Request node calls out to any API — the outbound counterpart to an inbound webhook"),
 "rag_pipeline":("rag-concept.png","How RAG Works",
   "Retrieval finds the documents that resemble the question · Augmentation adds them to the prompt · "
   "Generation produces an answer grounded in what was retrieved"),
 "chunking":("text-embedding.png","Tokenization and Text Embedding",
   "Text is split into tokens, then an embedding model turns it into a vector — a list of numbers that "
   "places similar meanings close together"),
 "vector_stores":("vector-database.png","Vector Databases",
   "A vector store holds the embeddings and finds the nearest neighbours to a question, fast"),
}

import slide_index as _si
assert set(CONCEPT_IMAGES)==_si.CONCEPT_IMAGE_KEYS, "slide_index.CONCEPT_IMAGE_KEYS is out of step with CONCEPT_IMAGES"
TOPIC_ACTS={t["num"]:[a for a in ACTIVITIES if a["topic"]==t["num"]] for t in C.TOPICS}

def shots_slide(kicker,title,imgs,caption,color=VIOLET):
    """One or more screenshots side by side at a common height, with a caption.

    Widths follow each image's aspect ratio, so a portrait flyer and a wide
    canvas sit in one row without either being squashed."""
    from PIL import Image
    s=slide(); head(s,title,kicker,kcolor=color)
    paths=[_asset(n) for n in imgs]; paths=[p for p in paths if p]
    ars=[(lambda im:(im.size[0]/im.size[1]))(Image.open(p)) for p in paths]
    gap=Inches(0.3); W=Inches(11.63); top=Inches(1.75); MAXH=Inches(4.45)
    H=min(MAXH,int((W-gap*(len(paths)-1))/sum(ars)))
    ws=[int(H*a) for a in ars]
    x=int(Inches(0.85)+(W-sum(ws)-gap*(len(paths)-1))/2); y=int(top+(MAXH-H)/2)
    for p,w in zip(paths,ws):
        pic_fit(s,p,x,y,w,H); x+=w+gap
    if caption:
        assert len(caption)<=210, f"Screenshot caption too long for its band: {caption[:80]}..."
        txt(s,Inches(0.85),Inches(6.35),Inches(11.63),Inches(0.6),[[(caption,12,GREY,False)]],align=PP_ALIGN.CENTER)
    footer(s); return s

def render_concepts(keys,kicker,acc,after=None):
    """Concept slides, each followed by its n8n screenshot where it has one.
    `after` maps a concept key to an extra slide renderer called right after it."""
    for key in keys:
        render_concept(CN.BY_KEY[key],kicker,accent=acc)
        if key in CONCEPT_IMAGES:
            img,ttl,cap=CONCEPT_IMAGES[key]
            image_slide(ttl,img,cap,kicker=kicker,accent=acc)
        # a real n8n canvas that shows this concept in practice (course_data.CONCEPT_SHOTS)
        if key in C.CONCEPT_SHOTS:
            flow_shot(C.CONCEPT_SHOTS[key],kicker,acc=acc)
        if after and key in after: after[key]()

def lab_block(a,K):
    """Every slide for one lab. The click-by-click steps stay in the Learner Guide."""
    short=a.get("short",a["title"])
    # how the building blocks just taught map onto this lab (Lab 2)
    if a.get("primer"):
        s=concept_slide(f"LAB {a['num']} · PUTTING IT TOGETHER",short+" — How the Building Blocks Fit",
         "Website → Webhook → AI Agent → Respond. Every block you have just learned has one job in this lab.",kcolor=TEAL)
        data_table(s,[2.3,4.9,4.43],["Building block","In this lab","Why it matters"],
                   [list(r) for r in a["primer"]],y=Inches(2.0),rh=Inches(0.5),hcolor=TEAL,fsz=10)
        takeaway(s,"Six building blocks, one workflow: the webhook brings the applicant in, the agent decides, the page shows the result.")
        footer(s)
    canv=a.get("canvas",[])
    chevs=a.get("chev",[[]])
    meta=f"{a['build']}  ·  full click-by-click steps in the Learner Guide"
    # n8n_shot is one dict, or a list with one real screenshot per workflow canvas
    # (Lab 5) — those are interleaved so each sits right after its own workflow.
    shots=a.get("n8n_shot") or []
    shots=shots if isinstance(shots,list) else [shots]
    paired=len(shots)>1 and len(shots)==len(canv)
    for ci,(img,cap) in enumerate(canv or [(None,"")]):
        # A lab with two workflows (Lab 5) gets one slide per workflow. Use the
        # SHORT title for those, because the full title plus a suffix wraps to a
        # second line and runs through the intro line beneath it.
        title=a["title"] if len(canv)<2 else (
            short+" — Ingestion Workflow" if ci==0 else short+" — Answering Workflow")
        flows=[chevs[ci]] if ci<len(chevs) else [chevs[0]]
        lab_slide(f"{K} · LAB WORKFLOW",f"LAB {a['num']}",title,
                  a["desc"] if ci==0 else cap,
                  flows,_asset(img) if img else None,meta,cap=cap if ci==0 else "",
                  color=TEAL)
        if paired:
            flow_shot(shots[ci],f"LAB {a['num']} · THE WORKFLOW IN n8n")
    # the real n8n canvas, as the learner sees it after import
    if not paired:
        for d in shots:
            flow_shot(d,f"LAB {a['num']} · THE WORKFLOW IN n8n")
    # The application the learner actually sees. Each screenshot gets its OWN
    # caption as the body — repeating the lab's takeaways on every one of these
    # slides produced near-identical bullets on consecutive pages.
    for si,(img,cap) in enumerate(a.get("site",[])):
        body=[cap]
        if si==0:
            body += [x[1] for x in a["learned"][:2]]
        website_lab(f"LAB {a['num']} · THE APPLICATION",short+" — What You'll Build",
                    _asset(img),body,color=VIOLET)
    # step screenshots, numbered how-to strips and galleries, in teaching order
    for kind,ttl,payload,note in a.get("extras",[]):
        kick=f"LAB {a['num']} · " + ("STEP BY STEP" if kind!="gallery" else "INSPIRATION")
        if kind=="flow":
            s=flow_h(ttl,payload,kicker=kick,color=TEAL); takeaway(s,note)
        elif kind=="annotated":
            # one screenshot explained by numbered cards (payload is an n8n_shot-style dict)
            flow_shot(dict(payload,title=ttl),f"LAB {a['num']} · THE APPLICATION",acc=VIOLET)
        else:
            shots_slide(kick,ttl,payload,note,color=VIOLET)
    # verify + debrief, as one card slide rather than a wall of prose
    s=concept_slide(f"LAB {a['num']} · VERIFY AND DEBRIEF",short,a["test"])
    ncards(s,[(PALETTE[i%len(PALETTE)],x[0],x[1]) if isinstance(x,tuple) else (BLUE,f"Takeaway {i+1}",x)
              for i,x in enumerate(a["learned"])],
           y=Inches(2.5),h=Inches(3.5),cols=2)
    takeaway(s,f"Lab {a['num']} — you can now "+a["objective"].split("(")[0].strip()+".")
    footer(s)

for t in C.TOPICS:
    tnum=t["num"]; K=KICKERS[tnum]; acc=ACCENTS[tnum]
    labs=TOPIC_ACTS[tnum]
    section(f"TOPIC {t['code']}",t["title"],t["code"],t["subtitle"],
            "Applied in "+", ".join(f"Lab {a['num']}" for a in labs),color=acc)
    if tnum==1:
        _p0=PAGE["n"]; topic1_intro(acc)
        assert PAGE["n"]-_p0==_si.TOPIC1_INTRO, "slide_index.TOPIC1_INTRO is out of step with topic1_intro()"
        # n8n fundamentals → Lab 1 → lunch → agent building blocks + webhooks → Lab 2
        render_concepts(CN.TOPIC1_FUNDAMENTALS,"TOPIC 1 · n8n FUNDAMENTALS",acc)
        lab_block(labs[0],K)
        brk("Lunch Break","1 hour",AMBER)
        render_concepts(CN.TOPIC1_AGENT,"TOPIC 1 · AI AGENT BUILDING BLOCKS",acc,
                        after={"model_params":lambda: free_ai_credits(acc)})
        render_concepts(CN.TOPIC1_WEBHOOK,"TOPIC 1 · WEBHOOKS",acc)
        lab_block(labs[1],K)
        continue
    if tnum==2:
        # knowledge before the lab: chatbot concepts → Lab 3 → HITL + guardrails → Lab 4
        render_concepts(CN.TOPIC2_CHATBOT,"TOPIC 2 · AGENTIC CHATBOT",acc)
        _p0=PAGE["n"]; telegram_demo(acc)
        assert PAGE["n"]-_p0==_si.TELEGRAM_DEMO_SLIDES, "slide_index.TELEGRAM_DEMO_SLIDES is out of step with telegram_demo()"
        lab_block(labs[0],K)
        render_concepts(CN.TOPIC2_HITL,"TOPIC 2 · HUMAN IN THE LOOP & GUARDRAILS",acc)
        lab_block(labs[1],K)
        brk("Tea Break","15 minutes",TEAL)
        continue
    render_concepts(CN.TOPIC_CONCEPTS[tnum],K,acc)
    for a in labs: lab_block(a,K)

# ---------------------------------------------------------------- CLOSE
section("WRAP-UP","Course Summary & Next Steps","")
tile_grid("What You Achieved",[
 ("LO1 · n8n and AI agents","Built a trigger-and-action workflow and explained how an LLM agent differs from generative AI."),
 ("LO2 · Webhook-triggered agents","Put an AI agent behind a real website, with tools, structured output and an audit log."),
 ("LO3 · Agentic chatbots","Designed a chatbot that collects contact details and refuses to give regulated advice."),
 ("LO4 · Human in the loop","Paused a workflow on an approval gate so no drafted communication was sent unsupervised."),
 ("LO5 · RAG","Ingested 20 documents into a vector store and grounded a chatbot so it stopped inventing answers.")],
 kicker="LEARNING OUTCOMES",cols=1,size=14)
s=concept_slide("NEXT STEPS","Taking This Back to Work",
 "Six moves that turn what you built this week into something your organisation actually runs.")
ncards(s,[(BLUE,"Start with one painful process","Pick something repetitive, high-volume and low-risk. Automate that first."),
 (TEAL,"Map it before you build it","Draw the trigger, the decisions and the actions on paper. The canvas comes second."),
 (VIOLET,"Decide where the human belongs","Anything irreversible, regulated or expensive keeps an approval gate."),
 (AMBER,"Ground the agent in your own data","RAG over your policies and documents beats a general model every time."),
 (GREEN,"Log everything from day one","You will need the audit trail long before you think you will."),
 (RED,"Iterate with real cases","Test with the questions you fear, not the ones you hope for.")],
 y=Inches(1.98),h=Inches(4.15),cols=3)
takeaway(s,"The next process you automate is the one you were dreading this morning.")
footer(s)
tile_grid("Support",[
 ("Email","enquiry@tertiaryinfotech.com"),
 ("Telephone","+65 6100 0613"),
 ("Website","www.tertiarycourses.com.sg"),
 ("LMS / TMS portal","lms-tms.tertiaryinfotech.com")],
 kicker="WE'RE HERE TO HELP — DURING AND AFTER THE CLASS",cols=2,size=15)
# --- mandated closing block: Assessment -> Assessment Flow -> Digital Attendance -> Thank You ---
tile_grid("Assessment",[
 ("Written Assessment (SAQ)","1 hour. Short-answer questions covering the course knowledge."),
 ("Practical Performance (PP)","1 hour. Hands-on n8n build tasks drawn from the five labs."),
 ("Open book","Slides, Learner Guide and approved materials only."),
 ("Submit on the LMS","Upload your completed answers at lms-tms.tertiaryinfotech.com."),
 ("Digital attendance","Remember to take the Assessment digital attendance (TRAQOM)."),
 ("Appeals","An appeal process is available if required.")],
 kicker="WRAP-UP · FINAL ASSESSMENT",cols=2,size=14)
flow_h("Assessment Flow",[
 "TRAQOM survey — scan the QR code on the LMS",
 "Assessment digital attendance — scan the SSG QR",
 "Sit WA (SAQ) then PP — open book",
 "Submit your answers on the LMS",
 "Sign the Assessment Summary Record"],kicker="ON ASSESSMENT DAY")
tile_grid("Digital Attendance (Mandatory)",[
 ("AM, PM and Assessment","It is mandatory to take all three digital attendances for WSQ-funded courses."),
 ("The QR code","The trainer or administrator displays the attendance QR code from the SSG portal."),
 ("Scan and submit","Scan it with your mobile phone camera and submit your attendance."),
 ("75% minimum","At least 75% attendance is required to be eligible for assessment and funding.")],
 kicker="TRAQOM · SSG DIGITAL ATTENDANCE",cols=2,size=15)
s=slide(); rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),SH,TEAL)
txt(s,Inches(1.1),Inches(2.2),Inches(11),Inches(0.5),[[("HAPPY AUTOMATING",16,TEAL,True)]])
txt(s,Inches(1.1),Inches(2.8),Inches(11.3),Inches(1.6),[[("Thank You!",44,INK,True)]])
txt(s,Inches(1.12),Inches(4.5),Inches(11),Inches(1.2),
    [[("Keep your n8n instance running and keep building. The next process you automate is the one you "
       "were dreading this morning.",18,GREY,False)]])
footer(s)

# ---- verify the LP's slide index agrees with what we actually emitted ----
import slide_index
_actual=len(prs.slides.__iter__.__self__._sldIdLst)
assert slide_index.TOTAL==_actual, (
    f"slide_index.TOTAL={slide_index.TOTAL} but the deck has {_actual} slides. "
    "Update slide_index.py so the Lesson Plan's slide references stay correct.")
for _k,(_a,_b) in slide_index.SLIDES.items():
    assert 1<=_a<=_b<=_actual, f"slide_index range {_k}={_a}-{_b} is outside 1..{_actual}"

OUT=os.path.join(os.environ.get("DECK_OUT_DIR") or os.path.join(REPO,"courseware"),f"{C.SHORT_TITLE}-{C.VERSION}.pptx")
# Edge-safe PDF: every autoshape carries <p:style><a:effectRef idx="2"> — the theme's drop
# shadow. PowerPoint honours the shape's own empty <a:effectLst/> and draws no shadow, but
# LibreOffice applies the theme shadow anyway and exports each one as a blurred greyscale
# bitmap with a soft mask (~1,300 per deck). Microsoft Edge's PDF engine renders pages full of
# those as BLANK. Point every shape at "no effect" so the PDF matches the deck and opens everywhere.
from pptx.oxml.ns import qn as _qn
for _s in prs.slides:
    for _ref in _s._element.iter(_qn("a:effectRef")):
        _ref.set("idx","0")
prs.save(OUT)
print(f"Saved {OUT}  ({_actual} slides)")
print(f"slide_index verified: {slide_index.TOTAL} slides, {len(slide_index.SLIDES)} named blocks")
