#!/usr/bin/env python3
"""Generate the Agentic AI for Business Process Automation (TGS-2024045801) slide deck.

All-white Tertiary house style. Design helpers are the component set used by the
tertiary-course-slides skill that produced the n8n reference deck (cover, section,
content, two_col, cards3, big_statement, tile_grid, flow_h, trainer_slide,
image_slide, step_slide, test_slide, brk). Content is driven entirely by
course_data.py + data_domainN.py so the deck stays 100% aligned with the LP, LG
and labs.
"""
import os, sys, math
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import course_data as C
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
RED=RGBColor(0xDC,0x26,0x26)

prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
SW,SH=prs.slide_width,prs.slide_height
BLANK=prs.slide_layouts[6]

def slide(): return prs.slides.add_slide(BLANK)
def rect(s,x,y,w,h,color,line=None):
    sp=s.shapes.add_shape(1,x,y,w,h); sp.fill.solid(); sp.fill.fore_color.rgb=color
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb=line; sp.line.width=Pt(1)
    sp.shadow.inherit=False; return sp
def oval(s,x,y,w,h,color):
    sp=s.shapes.add_shape(9,x,y,w,h); sp.fill.solid(); sp.fill.fore_color.rgb=color
    sp.line.fill.background(); sp.shadow.inherit=False; return sp
def txt(s,x,y,w,h,runs,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,space=4):
    tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True; tf.vertical_anchor=anchor
    for i,line in enumerate(runs):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment=align; p.space_after=Pt(space)
        for t,sz,col,bold in line:
            r=p.add_run(); r.text=t; r.font.size=Pt(sz); r.font.bold=bold
            r.font.color.rgb=col; r.font.name="Arial"
    return tb
def bullets(s,x,y,w,h,items,size=18,color=INK,gap=10,mcolor=BLUE):
    tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True
    for i,it in enumerate(items):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.space_after=Pt(gap)
        lvl=it[1] if isinstance(it,tuple) else 0
        text=it[0] if isinstance(it,tuple) else it
        r=p.add_run(); r.text=("•  " if lvl==0 else "–  ")+text
        r.font.size=Pt(size if lvl==0 else size-2); r.font.color.rgb=color if lvl==0 else GREY
        r.font.name="Arial"; r.font.bold=(lvl==0 and isinstance(it,tuple) and len(it)>2 and it[2])
    return tb

PAGE={"n":0}
def footer(s):
    PAGE["n"]+=1
    txt(s,Inches(0.4),Inches(7.05),Inches(7.5),Inches(0.35),
        [[(f"{C.SHORT_TITLE}  ·  {C.COURSE_CODE}",9,GREY,False)]])
    txt(s,Inches(5.0),Inches(7.05),Inches(3.3),Inches(0.35),
        [[("© 2026 Tertiary Infotech Academy Pte Ltd",9,GREY,False)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(12.4),Inches(7.05),Inches(0.6),Inches(0.35),
        [[(str(PAGE["n"]),9,GREY,False)]],align=PP_ALIGN.RIGHT)
def head(s,title,kicker=None,kcolor=BLUE):
    """Slide header. Long titles are auto-shrunk so they never wrap into the rule."""
    rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),Inches(1.55),kcolor)
    if kicker: txt(s,Inches(0.85),Inches(0.5),Inches(11.6),Inches(0.4),[[(kicker,14,kcolor,True)]])
    # ~0.52 * pt = chars that fit across 11.9in at Arial bold; shrink rather than wrap
    size=29
    for lim,sz in ((52,29),(62,25),(74,21),(90,18)):
        if len(title)<=lim: size=sz; break
    else:
        size=16
    txt(s,Inches(0.85),Inches(0.9),Inches(11.9),Inches(0.9),[[(title,size,INK,True)]])
    rect(s,Inches(0.85),Inches(1.7),Inches(11.63),Inches(0.02),LINE)
    return s
def _logo(name):
    p=os.path.join(ASSETS,name)
    return p if os.path.exists(p) else None
def _asset(name):
    p=os.path.join(CWASSETS,name)
    return p if os.path.exists(p) else None

# ---------------- slide templates ----------------
def cover():
    s=slide(); rect(s,0,0,SW,SH,WHITE)
    rect(s,0,0,SW,Inches(0.22),BLUE); rect(s,0,Inches(7.28),SW,Inches(0.22),TEAL)
    org=_logo("tertiary-infotech-logo.png")
    if org: s.shapes.add_picture(org,Inches(0.85),Inches(0.7),height=Inches(1.05))
    n8n=_logo("n8n-logo.png")
    if n8n: s.shapes.add_picture(n8n,Inches(11.3),Inches(0.62),height=Inches(1.2))
    txt(s,Inches(0.9),Inches(2.3),Inches(12),Inches(0.6),[[("COURSE SLIDES  ·  WSQ",16,BLUE,True)]])
    txt(s,Inches(0.9),Inches(2.85),Inches(12.0),Inches(1.9),[[(C.TITLE,40,INK,True)]])
    rect(s,Inches(0.92),Inches(4.75),Inches(2.4),Inches(0.06),TEAL)
    txt(s,Inches(0.9),Inches(5.05),Inches(12),Inches(1.4),
        [[(f"WSQ Course Code: {C.COURSE_CODE}",16,GREY,False)],
         [(f"TSC: {C.TSC_TITLE}  ·  {C.TSC_CODE}",13,GREY,False)],
         [("Conducted by Tertiary Infotech Academy Pte Ltd  ·  UEN 201200696W",14,GREY,False)]],space=6)
    txt(s,Inches(0.9),Inches(6.5),Inches(12),Inches(0.4),[[(f"Version {C.VERSION}  ·  {C.VERSION_DATE}",12,GREY,False)]])
    txt(s,Inches(0.9),Inches(6.85),Inches(12),Inches(0.34),[[("© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved.  ·  www.tertiarycourses.com.sg",10,GREY,False)]])

def section(kicker,title,n,sub=""):
    s=slide(); rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),SH,BLUE)
    rect(s,Inches(0.85),Inches(2.5),Inches(0.14),Inches(2.0),TEAL)
    txt(s,Inches(1.25),Inches(2.55),Inches(11),Inches(0.6),[[(kicker,18,BLUE,True)]])
    txt(s,Inches(1.25),Inches(3.0),Inches(11.4),Inches(1.6),[[(title,40,INK,True)]])
    if sub: txt(s,Inches(1.27),Inches(4.55),Inches(11),Inches(0.8),[[(sub,16,GREY,False)]])
    txt(s,Inches(10.0),Inches(0.7),Inches(2.8),Inches(1.6),[[(n,72,RGBColor(0xE2,0xE8,0xF0),True)]],align=PP_ALIGN.RIGHT)
    footer(s)
def content(title,items,kicker=None,size=20):
    s=head(slide(),title,kicker); bullets(s,Inches(0.85),Inches(1.95),Inches(11.6),Inches(4.9),items,size=size); footer(s); return s
def two_col(title,left,right,kicker=None,lhead="",rhead=""):
    s=head(slide(),title,kicker)
    rect(s,Inches(0.85),Inches(1.95),Inches(5.7),Inches(4.7),LIGHT); rect(s,Inches(6.95),Inches(1.95),Inches(5.55),Inches(4.7),LIGHT)
    if lhead: txt(s,Inches(1.1),Inches(2.15),Inches(5.2),Inches(0.4),[[(lhead,16,BLUE,True)]])
    if rhead: txt(s,Inches(7.2),Inches(2.15),Inches(5.0),Inches(0.4),[[(rhead,16,TEAL,True)]])
    bullets(s,Inches(1.1),Inches(2.7),Inches(5.2),Inches(3.8),left,size=16)
    bullets(s,Inches(7.2),Inches(2.7),Inches(5.05),Inches(3.8),right,size=16,mcolor=TEAL); footer(s); return s
def cards3(title,cards,kicker):
    s=head(slide(),title,kicker); xs=[Inches(0.85),Inches(5.0),Inches(9.15)]
    for i,c in enumerate(cards[:3]):
        x=xs[i]; col=c[0]
        rect(s,x,Inches(1.95),Inches(3.65),Inches(4.7),LIGHT); rect(s,x,Inches(1.95),Inches(3.65),Inches(0.12),col)
        txt(s,x+Inches(0.25),Inches(2.2),Inches(3.2),Inches(0.6),[[(c[1],19,col,True)]])
        bullets(s,x+Inches(0.25),Inches(2.95),Inches(3.2),Inches(3.4),c[2],size=14,mcolor=col,gap=9)
    footer(s); return s
def big_statement(line1,line2,kicker,color=BLUE):
    s=slide(); rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),SH,color)
    txt(s,Inches(1.1),Inches(2.2),Inches(11),Inches(0.5),[[(kicker,16,color,True)]])
    txt(s,Inches(1.1),Inches(2.8),Inches(11.3),Inches(2.4),[[(line1,38,INK,True)]])
    if line2: txt(s,Inches(1.12),Inches(4.9),Inches(11),Inches(1.2),[[(line2,20,GREY,False)]])
    footer(s); return s
PALETTE=[BLUE,TEAL,VIOLET,AMBER]
def tile_grid(title,items,kicker=None,cols=2,size=15,icons=None,accent=BLUE):
    s=head(slide(),title,kicker,kcolor=accent)
    n=len(items); rows=math.ceil(n/cols)
    X0=Inches(0.85); Y0=Inches(1.95); TOTW=Inches(11.63); AREAH=Inches(4.78)
    gx=Inches(0.3); gy=Inches(0.26)
    cw=int((TOTW-gx*(cols-1))/cols); ch=int((AREAH-gy*(rows-1))/rows)
    # Cap tile height so one- or two-row grids don't stretch into giant empty panels,
    # and centre the block vertically in the content area instead.
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
        txt(s,x+Inches(0.28),int(y+ch/2-bd/2),bd,bd,[[(ic,19,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        tx=x+Inches(1.08); tw=cw-Inches(1.32)
        if isinstance(it,tuple):
            # Shrink a long heading rather than let it wrap and push the body past
            # the tile's bottom border. ~0.085in per char at (size+2)pt Arial bold.
            hsize=size+2
            avail_chars=int(tw/Inches(0.085)/((size+2)/15.0))
            if len(it[0])>avail_chars: hsize=max(size-1, size+2-3)
            txt(s,tx,int(y+Inches(0.14)),tw,int(ch-Inches(0.2)),
                [[(it[0],hsize,INK,True)],[(it[1],size-2,GREY,False)]],anchor=MSO_ANCHOR.MIDDLE,space=3)
        else:
            txt(s,tx,int(y+Inches(0.1)),tw,int(ch-Inches(0.16)),[[(it,size,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s
def flow_h(title,steps,kicker=None,color=BLUE):
    s=head(slide(),title,kicker,kcolor=color)
    n=len(steps); X0=Inches(0.85); TOTW=Inches(11.63); gap=Inches(0.34)
    cw=int((TOTW-gap*(n-1))/n); y=Inches(2.55); ch=Inches(3.15); bd=Inches(0.82)
    for i,st in enumerate(steps):
        x=int(X0+(cw+gap)*i)
        rect(s,x,y,cw,ch,LIGHT); rect(s,x,y,cw,Inches(0.1),color)
        oval(s,int(x+cw/2-bd/2),int(y+Inches(0.42)),bd,bd,color)
        txt(s,int(x+cw/2-bd/2),int(y+Inches(0.42)),bd,bd,[[(str(i+1),30,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        txt(s,x+Inches(0.16),int(y+Inches(1.55)),cw-Inches(0.32),int(ch-Inches(1.7)),[[(st,14,INK,False)]],align=PP_ALIGN.CENTER)
        if i<n-1:
            txt(s,int(x+cw-Inches(0.04)),int(y+ch/2-Inches(0.3)),int(gap+Inches(0.08)),Inches(0.6),
                [[("▶",15,color,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s
def image_slide(title,imgname,caption="",kicker=None,accent=BLUE,cap_size=13):
    """Full-width diagram slide: a reference visual with a one-line caption beneath.
    The image gets the whole content area minus a tight caption band, so a wide
    screenshot fills the slide instead of floating as a thumbnail."""
    s=head(slide(),title,kicker,kcolor=accent)
    p=_asset(imgname)
    AREA_TOP=Inches(1.92); AREA_BOT=Inches(6.9)    # rule → footer
    CAP_H=Inches(0.62) if caption else 0           # tight caption band
    if p:
        from PIL import Image
        iw,ih=Image.open(p).size
        maxw=Inches(12.0); maxh=AREA_BOT-AREA_TOP-CAP_H
        scale=min(maxw/iw, maxh/ih)
        w=int(iw*scale); h=int(ih*scale)
        y=int(AREA_TOP+((AREA_BOT-CAP_H)-AREA_TOP-h)/2)
        s.shapes.add_picture(p,int((SW-w)/2),y,width=w,height=h)
        cy=y+h+Inches(0.12)
    else:
        cy=Inches(2.4)
    if caption:
        txt(s,Inches(0.85),cy,Inches(11.63),CAP_H or Inches(0.9),
            [[(caption,cap_size,GREY,False)]],align=PP_ALIGN.CENTER)
    footer(s); return s
def trainer_slide(kicker,name,role,rows,initials,accent=BLUE):
    s=head(slide(),"About the Trainer",kicker,kcolor=accent)
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
def activity_overview(tag,title,desc,build,services,kicker):
    s=head(slide(),title,kicker,kcolor=TEAL)
    rect(s,Inches(0.85),Inches(1.85),Inches(1.7),Inches(0.5),TEAL)
    txt(s,Inches(0.85),Inches(1.9),Inches(1.7),Inches(0.4),[[(tag,16,WHITE,True)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(0.85),Inches(2.55),Inches(11.7),Inches(1.6),[[(desc,18,INK,False)]])
    rect(s,Inches(0.85),Inches(4.55),Inches(11.7),Inches(1.85),LIGHT)
    txt(s,Inches(1.1),Inches(4.72),Inches(11),Inches(0.4),[[("You'll build",14,BLUE,True)]])
    txt(s,Inches(1.1),Inches(5.1),Inches(11.2),Inches(0.7),[[(build,16,INK,True)]])
    txt(s,Inches(1.1),Inches(5.9),Inches(11.2),Inches(0.5),[[("Tools:  ",13,GREY,True),(services,13,GREY,False)]]); footer(s); return s
def step_slide(kicker,act_title,n,total,text,cmd="",why="",progress=None):
    """One lab step. The lower half carries the command, the 'why' note and a
    progress strip, so the slide is not two-thirds empty."""
    s=head(slide(),act_title,kicker,TEAL)
    oval(s,Inches(0.85),Inches(2.5),Inches(1.4),Inches(1.4),TEAL)
    txt(s,Inches(0.85),Inches(2.74),Inches(1.4),Inches(0.9),[[(str(n),38,WHITE,True)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(0.95),Inches(1.95),Inches(11),Inches(0.4),[[(f"STEP {n} OF {total}",13,GREY,True)]])
    txt(s,Inches(2.55),Inches(2.4),Inches(10.1),Inches(1.5),[[(text,21,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
    y=Inches(4.25)
    if cmd:
        rect(s,Inches(2.55),y,Inches(10.1),Inches(0.9),RGBColor(0x0B,0x12,0x20))
        txt(s,Inches(2.8),y+Inches(0.12),Inches(9.7),Inches(0.66),
            [[("$ "+cmd,13,RGBColor(0x9C,0xDC,0xFE),False)]],anchor=MSO_ANCHOR.MIDDLE)
        y=y+Inches(1.1)
    if why:
        rect(s,Inches(2.55),y,Inches(10.1),Inches(1.05),LIGHT)
        rect(s,Inches(2.55),y,Inches(0.1),Inches(1.05),AMBER)
        txt(s,Inches(2.85),y+Inches(0.1),Inches(9.6),Inches(0.85),
            [[("WHY THIS STEP",10,AMBER,True)],[(why,13,GREY,False)]],anchor=MSO_ANCHOR.MIDDLE,space=2)
    # progress strip along the bottom — one pip per step, current one filled
    if progress:
        pw=Inches(10.1)/total; py=Inches(6.55)
        for i in range(total):
            col=TEAL if i<n else LINE
            rect(s,int(Inches(2.55)+pw*i+Inches(0.02)),py,int(pw-Inches(0.04)),Inches(0.09),col)
    footer(s); return s
def test_slide(act_title,text,kicker):
    s=head(slide(),act_title,kicker,TEAL)
    rect(s,Inches(0.85),Inches(2.3),Inches(11.7),Inches(2.9),RGBColor(0xE8,0xF7,0xEE))
    txt(s,Inches(1.2),Inches(2.6),Inches(11),Inches(0.5),[[("✅  Test it",20,RGBColor(0x12,0x7A,0x3E),True)]])
    txt(s,Inches(1.2),Inches(3.3),Inches(11),Inches(1.7),[[(text,17,INK,False)]]); footer(s); return s
def brk(kind,dur,color=AMBER):
    s=slide(); rect(s,0,0,SW,SH,WHITE)
    rect(s,0,0,SW,Inches(0.22),color); rect(s,0,Inches(7.28),SW,Inches(0.22),color)
    rect(s,Inches(5.4),Inches(2.35),Inches(2.53),Inches(0.1),color)
    txt(s,0,Inches(2.75),SW,Inches(1.2),[[(kind,48,INK,True)]],align=PP_ALIGN.CENTER)
    txt(s,0,Inches(4.05),SW,Inches(0.8),[[(dur,22,color,True)]],align=PP_ALIGN.CENTER); PAGE["n"]+=1

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
content("Let's Know Each Other",[
 "Your name and organisation / role.",
 "Your experience with automation or AI tools (if any).",
 "One business process in your work you would most like to automate.",
 "What you want to be able to build by the end of this course."],kicker="ICE-BREAKER")
tile_grid("Ground Rules",[
 "Set your mobile phone to silent mode.","Participate actively — no question is too small.",
 "Mutual respect: agree to disagree.","One conversation at a time.",
 "Be punctual; return from breaks on time.","75% attendance is required."],
 kicker="HOUSEKEEPING",cols=2,size=15)
image_slide("Download Course Material","lms-portal.png",
 "Log in at lms-tms.tertiaryinfotech.com with your registered email and the OTP sent to your inbox, "
 "then open this course to download the slides and Learner Guide.",
 kicker="COURSE PORTAL")
flow_h("Download Course Material",[
 "Go to lms-tms.tertiaryinfotech.com",
 "Enter your registered email and click Send OTP",
 "Key in the one-time password from your inbox",
 "Open this course and download the slides + Learner Guide",
 "Keep them open — the assessment is open book"],kicker="COURSE PORTAL · STEPS")
content("Get the Course Workflows",[
 "Every lab ships with a ready-made n8n workflow (.json) in the course labs/ folder.",
 "In n8n: Workflows → Add workflow → ⋯ → Import from File → pick the lab .json.",
 "After importing, re-select YOUR OWN credentials on every node that shows a warning.",
 "Imported workflows reference credential names, not secrets — nothing of yours is shared."],kicker="GET THE FLOWS")

# Skills Framework
content("Skills Framework (TSC)",[
 f"TSC Title: {C.TSC_TITLE}",
 f"TSC Code: {C.TSC_CODE}",
 "This WSQ course is mapped to the SkillsFuture Singapore Skills Framework.",
 "The assessment covers every Ability (A) and Knowledge (K) statement listed next."],kicker="WSQ ALIGNMENT")
two_col("TSC Abilities and Knowledge",
 [(f"{c} {t}",1) for c,t in C.TSC_ABILITIES],
 [(f"{c} {t}",1) for c,t in C.TSC_KNOWLEDGE],
 kicker="SKILLS FRAMEWORK",lhead="Abilities (assessed by PP)",rhead="Knowledge (assessed by WA)")

# Lesson plan overview
two_col(f"Lesson Plan — {C.DAYS} Days, {C.HOURS_PER_DAY} hours/day",[
 (f"Day 1 — {C.DAY_THEMES[1]}",0),
 ("Topic 1: Overview of n8n and AI Agents",1),
 ("Lab 1 — n8n trigger and action",1),
 ("Lab 2 — Webhook and AI Agent",1),
 ("Topic 2 begins: Agentic workflows",1),
 ("Lab 3 — Chatbot webhook",1)],
 [(f"Day 2 — {C.DAY_THEMES[2]}",0),
 ("Topic 2: Human in the loop",1),
 ("Lab 4 — Human in the loop",1),
 ("Topic 3: RAG — Lab 5",1),
 ("Final Assessment (WA + PP)",1),
 ("Daily timing",0),
 (f"Day 1: {C.DAY_TIMES[1]}",1),
 (f"Day 2: {C.DAY_TIMES[2]}",1),
 ("1-hour lunch; tea breaks additional",1)],
 kicker="SCHEDULE",lhead="Day 1",rhead="Day 2 & timing")
tile_grid("Learning Outcomes",[
 ("LO1 · n8n and AI agents","Explain what n8n and AI agents are, and build workflows using triggers and actions."),
 ("LO2 · Webhook-triggered agents","Implement AI agent applications triggered by webhooks and integrated with business systems."),
 ("LO3 · Agentic chatbots","Design agentic chatbot workflows that operate within business and regulatory constraints."),
 ("LO4 · Human in the loop","Apply human approval so that sensitive actions are authorised by a named person."),
 ("LO5 · RAG","Deploy Retrieval-Augmented Generation to ground an agent in your organisation's documents.")],
 kicker="WHAT YOU'LL ACHIEVE",cols=1,size=15)
content("Course Outline",[
 ("Topic 1: Overview of n8n and AI Agents",0),
 ("What is n8n · Lab 1: n8n trigger and action · What is an AI Agent · Lab 2: Webhook and AI Agent",1),
 ("Topic 2: Agentic Chatbot and Human in the Loop",0),
 ("What is an agentic workflow · Lab 3: Chatbot webhook · Lab 4: Human in the loop",1),
 ("Topic 3: Retrieval-Augmented Generation (RAG)",0),
 ("What is RAG · Lab 5: RAG customer care chatbot",1)],kicker="WHAT WE'LL COVER",size=18)
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

# ---------------------------------------------------------------- FOUNDATION CONCEPTS
section("FOUNDATION","Why Agentic AI, and Why Now","")
tile_grid("The Evolution of AI",[
 ("Artificial Intelligence · 1950s","Turing's test and symbolic, rule-based systems that encode human expertise by hand."),
 ("Machine Learning · 1990s","Data-driven systems that learn patterns from examples instead of being programmed with rules."),
 ("Deep Learning · 2000s","Neural networks — DNNs and CNNs — trained on large datasets with GPU compute."),
 ("Generative AI · 2020s","The 2017 Transformer and its attention mechanism made models that generate fluent text and images."),
 ("Agentic AI · 2024","LLMs given goals, tools and memory: they plan, act, observe and adapt rather than answering once."),
 ("Physical AI · 2025","Agents that perceive and act in the physical world — robotics and embodied systems.")],
 kicker="FROM RULES TO AGENTS",cols=2,size=14)
big_statement("Agentic AI is AI that does the work, not just describes it.",
 "An agent uses the reasoning power of a large language model to run a complex task by breaking it into "
 "simpler ones — calling tools, checking results and deciding what to do next.","THE CORE IDEA",color=BLUE)
image_slide("How an AI Agent Works","ai-agent-llm-loop.png",
 "The agent loop: given a goal, the LLM observes, chooses an action, acts on the world through a tool, "
 "observes the result, and repeats until the goal is met.",kicker="THE AGENT LOOP")
two_col("Agentic AI vs Generative AI",
 [("Generative AI",0),
  ("Creates content — text, images, code",1),
  ("Responds to a prompt, once",1),
  ("Relies on you for context and goals",1),
  ("Stops when the answer is produced",1),
  ("Example: draft me an email",1)],
 [("Agentic AI",0),
  ("Takes actions towards a goal",1),
  ("Plans, acts, observes, adapts",1),
  ("Uses tools to reach real systems",1),
  ("Continues until the goal is met",1),
  ("Example: read the enquiry, check the CRM, reply and log it",1)],
 kicker="THE DISTINCTION",lhead="Content creation",rhead="Action and autonomy")
image_slide("From RPA to Agentic Process Automation","rpa-to-apa.png",
 "Robotic Process Automation follows a rigid path you construct by hand. Agentic Process Automation lets "
 "an agent orchestrate the workflow, so it handles both rigid and flexible tasks.",kicker="APA")
tile_grid("Business Value of Agentic Automation",[
 ("Free people from repetitive admin","Scheduling, form processing, data entry, report generation and email routing run themselves."),
 ("Shift effort to high-value work","When the admin burden lifts, people spend time on judgement, relationships and strategy."),
 ("Respond in real time","Events — a form, a payment, a customer message — trigger a workflow the moment they happen."),
 ("Work around the clock","An agent answers a 2am enquiry with the same care as a 2pm one, and never forgets to log it."),
 ("Reduce human error","The same rules are applied to every case, and every decision is written to an audit trail."),
 ("Scale without headcount","Handling ten times the volume costs compute, not another ten hires.")],
 kicker="WHY ORGANISATIONS ADOPT IT",cols=2,size=14)
tile_grid("Where Agentic Automation is Used",[
 ("Customer service","Answer enquiries from your own documents, capture leads, and escalate what needs a person."),
 ("Finance & accounting","Invoice processing, bank reconciliation, accounts-payable routing and exception handling."),
 ("Risk & compliance","Screen applications, flag anomalies, and route sensitive cases for human review."),
 ("HR & people ops","Onboarding, leave applications, policy questions and approval chains."),
 ("Sales & marketing","Lead qualification, follow-up sequencing, CRM enrichment and content drafting."),
 ("Operations","Order processing, status notifications, document generation and reporting.")],
 kicker="USE CASES",cols=2,size=14,accent=VIOLET)
cards3("Where AI Agent Platforms Sit",[
 (BLUE,"No-code",["Fully visual builders","Fastest to a working agent","Least control over internals","e.g. AgentX, chatbot builders"]),
 (TEAL,"Low-code  ·  n8n",["Visual canvas plus code nodes","400+ integrations out of the box","Self-host or cloud","This course's platform"]),
 (VIOLET,"Full-code",["SDKs and frameworks","Maximum control and customisation","Requires engineering effort","e.g. LangChain, agent SDKs"])],
 kicker="COMPLEXITY VS CUSTOMISATION")

# ---------------------------------------------------------------- TOPICS + LABS
TOPIC_CONCEPT_IMAGES = {
 3: [("rag-concept.png","How RAG Works",
      "Retrieval finds the documents that resemble the question · Augmentation adds them to the prompt · "
      "Generation produces an answer grounded in what was retrieved."),
     ("text-embedding.png","Tokenization and Text Embedding",
      "Text is split into tokens, then an embedding model turns it into a vector — a list of numbers that "
      "places similar meanings close together."),
     ("vector-database.png","Vector Databases",
      "A vector store holds the embeddings and finds the nearest neighbours to a question, fast.")],
}

TOPIC_ACTS = {t["num"]: [a for a in ACTIVITIES if a["topic"]==t["num"]] for t in C.TOPICS}
CARD_COLORS=[BLUE,TEAL,VIOLET]

# --- extra teaching slides per topic (rich, NotebookLM-style depth) ---
def topic1_extra():
    tile_grid("What is n8n?",[
     ("A workflow automation platform","Connect apps, data and AI on one canvas, with little or no code."),
     ("Visual node editor","Drag nodes onto a canvas and wire them together; each node shows its input and output as JSON."),
     ("400+ integrations","Gmail, Google Sheets, Telegram, Slack, HTTP, databases — plus a generic HTTP node for anything else."),
     ("Fair-code and self-hostable","Run it on n8n Cloud, or host it yourself with Docker or npm and keep full control of your data."),
     ("AI-native","Built-in AI Agent, chat model, memory, vector store and tool nodes for building agents."),
     ("Exportable workflows","Every workflow is a JSON file you can version, share and import.")],
     kicker="THE PLATFORM",cols=2,size=14)
    cards3("Three Ways to Run n8n",[
     (BLUE,"n8n Cloud",["Sign up at n8n.io","Nothing to install","Free trial period","Best for this course"]),
     (TEAL,"Docker / self-host",["docker compose up -d","Runs at localhost:5678","Your data stays with you","Best for production"]),
     (VIOLET,"npm",["npx n8n","Quickest local start","Node.js required","Best for a quick trial"])],
     kicker="SETUP OPTIONS")
    content("Credential Setup",[
     "Add credentials once under Credentials → Add credential; every workflow can then reuse them.",
     "Google (Sheets, Drive, Gmail) uses OAuth2 — you sign in and grant access.",
     "AI models use an API key: Google Gemini or OpenAI.",
     "Imported workflows reference credential NAMES, not secrets — re-select your own after importing.",
     "Never paste an API key into a node field; always store it in a credential."],kicker="ACCOUNTS & KEYS")
    tile_grid("The Building Blocks — n8n Nodes",[
     ("Trigger nodes","Start a workflow: Form, Webhook, Schedule, Chat, Manual, or an app event such as a new email."),
     ("Action nodes","Do something: send Gmail, append a Google Sheets row, call an HTTP API, write to a database."),
     ("Logic nodes","Control the flow: IF and Switch to branch, Merge and Split Out to reshape, Code for custom logic."),
     ("AI nodes","Reason and act: AI Agent, Chat Model, Memory, Embeddings, Vector Store and Tool nodes.")],
     kicker="FOUR KINDS OF NODE",cols=2,size=14)
    two_col("Triggers and Actions",
     [("A trigger decides WHEN",0),
      ("Manual — run on demand while testing",1),
      ("Schedule — run on a timer or cron",1),
      ("Form — a hosted web form",1),
      ("Webhook — an external system calls a URL",1),
      ("Chat — the built-in chat window",1)],
     [("An action decides WHAT",0),
      ("Gmail / Outlook — send an email",1),
      ("Google Sheets — append or update a row",1),
      ("HTTP Request — call any API",1),
      ("Code — run JavaScript or Python",1),
      ("Edit Fields (Set) — reshape the data",1)],
     kicker="CORE CONCEPT",lhead="Triggers",rhead="Actions")
    content("Data, JSON and Expressions",[
     "Data flows between nodes as a list of items, each one a JSON object.",
     "JSON stores key/value pairs, e.g. { \"name\": \"Alice\", \"age\": 30 }.",
     "Read a value from the previous node with an expression: {{ $json.Name }}.",
     "Drag a field from the input panel into any field to map it automatically.",
     "Expressions work anywhere — subject lines, URLs, conditions and message bodies."],kicker="HOW DATA MOVES")
    two_col("Test vs Production Execution",
     [("Test execution",0),
      ("Run manually from the editor",1),
      ("Inspect the data at every node",1),
      ("Test URL listens for ONE request",1),
      ("Use it while you are building",1)],
     [("Production execution",0),
      ("Runs automatically when Active",1),
      ("Production URL accepts unlimited requests",1),
      ("Every run is kept in Execution History",1),
      ("Switch to it the moment others use it",1)],
     kicker="HOW IT RUNS",lhead="While building",rhead="Once live")
    big_statement("An agent is an LLM with a goal, tools and memory.",
     "The model supplies judgement — which tool to call and when. You supply the goal, the guardrails and "
     "the tools it is allowed to use.","WHAT IS AN AI AGENT",color=TEAL)
    tile_grid("The Four Parts of an n8n AI Agent",[
     ("Chat Model","The LLM that reasons and writes the reply — Google Gemini or OpenAI in this course."),
     ("System Instruction","The agent's role, scope, prohibitions and routing rules. Your main control surface."),
     ("Memory","Recalls the conversation, keyed on a session ID so users never see each other's messages."),
     ("Tools","What the agent can actually do — look up a sheet, search a vector store, send an email, call an API.")],
     kicker="MODEL · INSTRUCTION · MEMORY · TOOLS",cols=2,size=14,accent=TEAL)
    content("Writing a Good System Instruction",[
     "State the role plainly: 'You are the onboarding assistant for Marina Trust Bank.'",
     "Give the scope and the limits — what it must answer, and what it must refuse.",
     "Say which tool to use for which kind of question, explicitly.",
     "Ask for a specific output format when something downstream depends on it.",
     "Tell it to say 'I don't know' rather than invent an answer.",
     "Keep it concise, specific and testable — then test it with real questions and refine."],kicker="INSTRUCTION DESIGN")
    tile_grid("Webhooks — the Front Door to Your Agent",[
     ("What it is","A URL that any external system can send data to. It starts your workflow when called."),
     ("The opposite of an API call","With an HTTP Request node YOU call the outside world; with a Webhook the outside world calls YOU."),
     ("Test vs Production URL","The Test URL works for one request while you are listening; the Production URL works whenever the workflow is Active."),
     ("GET vs POST","GET carries data in the URL query string; POST carries it in a JSON body — which is what a website chat widget sends."),
     ("CORS","Set Allowed Origins so a browser page is permitted to read the reply. '*' is fine in class, never in production."),
     ("Authentication","None, Basic Auth, Header Auth or JWT. An open webhook costs you money every time a stranger calls it.")],
     kicker="EXTERNAL TRIGGERS",cols=2,size=14,accent=VIOLET)
    content("Structured Output — Why It Matters",[
     "By default an agent returns a paragraph of prose. Prose cannot be branched on, sorted or coloured.",
     "A Structured Output Parser forces named fields, e.g. decision, reason and riskFlags.",
     "An IF node can then route on decision; a Sheets node can log it; a web page can colour the card.",
     "Enumerate the allowed values (APPROVED / REJECTED / REVIEW / DUPLICATE) so the field is reliable.",
     "This is the single most useful habit when putting an agent inside a business process."],kicker="MAKING AGENTS USABLE")

def topic2_extra():
    big_statement("An agentic workflow is one where the LLM makes the routing decisions.",
     "You still design the process, the guardrails and the tools. What you hand over is the judgement about "
     "which path this particular case should take.","WHAT IS AN AGENTIC WORKFLOW",color=BLUE)
    two_col("Rule-Based Workflow vs Agentic Workflow",
     [("Rule-based (RPA)",0),
      ("You wire every branch by hand",1),
      ("IF / Switch on exact values",1),
      ("Breaks on anything unexpected",1),
      ("Predictable and easy to audit",1),
      ("Best for: fixed, high-volume rules",1)],
     [("Agentic (APA)",0),
      ("The agent chooses the path",1),
      ("Understands free text and intent",1),
      ("Handles cases you did not foresee",1),
      ("Needs guardrails and logging",1),
      ("Best for: varied, language-driven work",1)],
     kicker="TWO WAYS TO AUTOMATE",lhead="Deterministic",rhead="Judgement-based")
    tile_grid("Designing a Safe Agentic Chatbot",[
     ("Define the role narrowly","A chatbot for one job refuses far more reliably than a general assistant."),
     ("Write the prohibitions explicitly","'Never recommend a product, predict a return, or guarantee an outcome' does real compliance work."),
     ("Add a fallback sentence","'When in doubt, say less and offer a consultation' covers the cases you did not anticipate."),
     ("Gate what must be collected","Ask for the contact details before answering, and enforce it in the agent as well as the browser."),
     ("Keep the FAQ in the prompt","A handful of short answers costs nothing to retrieve and can be reviewed by compliance in one sitting."),
     ("Test with adversarial questions","Probe it with the questions you most fear being asked, not the ones you hope for.")],
     kicker="CHATBOT DESIGN",cols=2,size=14,accent=TEAL)
    content("Memory — and When Not to Use It",[
     "A memory node lets a follow-up question be answered in context, without repeating everything.",
     "Memory is keyed on a session ID, so two visitors never see each other's conversation.",
     "Window buffer memory keeps the last N messages; older turns fall out of context.",
     "Some workflows must have NO memory: an application decision should never be influenced by the previous applicant.",
     "Ask, for every agent: should this case know about the last one?"],kicker="CONTEXT ACROSS TURNS")
    big_statement("Some actions are too consequential to automate.",
     "A human-in-the-loop step pauses the workflow until a named person approves or declines. The agent may "
     "do everything except the one thing that matters.","HUMAN IN THE LOOP",color=AMBER)
    flow_h("The Human-in-the-Loop Pattern",[
     "An event arrives — a customer message or an application",
     "The agent classifies, flags and drafts a proposal",
     "The proposal is logged before any human sees it",
     "A named person receives it and clicks Approve or Decline",
     "Only on approval is the action taken and logged"],kicker="THE APPROVAL GATE",color=AMBER)
    tile_grid("When to Put a Human in the Loop",[
     ("Money moves","Payments, refunds, credit decisions and anything with a financial consequence."),
     ("It is a regulated communication","A licensed firm writing to a client about their money, health or legal position."),
     ("The action is irreversible","Sending an email, deleting a record or publishing content cannot be undone."),
     ("A person is vulnerable","Distress, illness, bereavement or savings someone cannot afford to lose."),
     ("The stakes exceed the error rate","The question is never 'is the model good?' but 'what does one bad output cost?'."),
     ("Someone must be accountable","A regulator asks which licensed person is answerable — not what the machine decided.")],
     kicker="THE DECISION CRITERIA",cols=2,size=14,accent=AMBER)
    content("Building the Audit Trail",[
     "Log what the agent PROPOSED separately from what a human AUTHORISED.",
     "Keeping them apart is what lets an auditor ask: did anyone send something a human never saw?",
     "Every approved action carries the name of the person who approved it.",
     "Every declined action is reassigned to a named person — a decline is not a deletion.",
     "No accountability column should ever be empty.",
     "Treat classifications about a person (emotional tone, risk flags) as personal data under the PDPA."],kicker="ACCOUNTABILITY")

def topic3_extra():
    content("Why Not Just Paste Everything Into the Prompt?",[
     "For twenty short documents, pasting them all would actually work.",
     "Add two hundred more and the prompt exceeds the model's context window.",
     "Long prompts also degrade quality — models attend less well to the middle of a very long context.",
     "And you pay for every token, on every single question, whether it was relevant or not.",
     "RAG turns the problem around: retrieve the few documents that resemble the question, and send only those."],kicker="THE DESIGN QUESTION")
    flow_h("The RAG Pipeline",[
     "Collect the source documents",
     "Split them into chunks",
     "Embed each chunk into a vector",
     "Store the vectors in a vector store",
     "Embed the question and retrieve the nearest chunks",
     "The LLM answers from what was retrieved"],kicker="INGESTION THEN RETRIEVAL",color=VIOLET)
    tile_grid("Chunking — the Biggest Lever on RAG Quality",[
     ("The rule","The right chunk is the smallest piece of text that still answers a question on its own."),
     ("Too small","A brochure sliced into thirds separates the course name from its fee — retrieval finds one without the other."),
     ("Too large","Irrelevant text crowds the prompt and dilutes what actually matters."),
     ("Overlap","A small overlap between chunks stops a sentence being cut in half at a boundary."),
     ("In this lab","Chunk size 4000, overlap 0 — one brochure becomes exactly one vector."),
     ("The lesson","Most RAG projects fail quietly at chunking, not at the model.")],
     kicker="WHERE RAG PROJECTS FAIL",cols=2,size=14,accent=VIOLET)
    two_col("Choosing a Vector Store",
     [("Simple Vector Store (built in)",0),
      ("No account, key or index needed",1),
      ("Running RAG in ten minutes",1),
      ("WIPED when n8n restarts",1),
      ("Good for: learning and prototypes",1)],
     [("A real vector database",0),
      ("Pinecone, Supabase (pgvector), Qdrant",1),
      ("Account, index and dimension to set up",1),
      ("Persists and scales; shared across instances",1),
      ("Good for: anything in production",1)],
     kicker="IN-MEMORY VS HOSTED",lhead="Activity 5 uses this",rhead="What production needs")
    content("The Rules That Keep RAG Working",[
     "The ingestion and retrieval embedding models must be IDENTICAL — the numbers mean different things otherwise.",
     "The vector store's dimension must match the embedding model's output (Gemini embedding-001 = 3072).",
     "The memory key or index name must match between ingestion and retrieval.",
     "Turn Clear Store on when re-ingesting, or every document is stored — and retrieved — twice.",
     "topK controls how many chunks are retrieved: too few misses the answer, too many dilutes the prompt."],kicker="THE COMMON FAILURES")
    tile_grid("Grounding an Agent Against Hallucination",[
     ("Always call the tool first","Instruct the agent to search before answering any factual question."),
     ("Answer only from what came back","Every factual claim must trace to a retrieved document."),
     ("Give it permission to fail","'Say I don't have that in our course information' is a better answer than a confident invention."),
     ("Name what it must never invent","A fee, a date, a duration, a course code, an instructor name, a discount."),
     ("Hide the machinery","Never mention the vector store or that it is searching documents — the customer does not care."),
     ("Test the traps","Ask about a course you do not run, a person who does not exist, and a discount never offered.")],
     kicker="THE INSTRUCTIONS THAT MATTER",cols=2,size=14,accent=VIOLET)

TOPIC_EXTRA = {1: topic1_extra, 2: topic2_extra, 3: topic3_extra}

for t in C.TOPICS:
    section(f"TOPIC {t['code']}", t["title"], t["code"], t["subtitle"])
    tile_grid(f"Key Concepts — {t['title']}", t["concepts"],
              kicker=f"LEARNING OUTCOMES {t['weighting']}", cols=2, size=13)
    # concept images for this topic (RAG has several)
    for img,ttl,cap in TOPIC_CONCEPT_IMAGES.get(t["num"],[]):
        image_slide(ttl,img,cap,kicker=f"TOPIC {t['code']} · CONCEPT",accent=VIOLET)
    # rich teaching slides
    TOPIC_EXTRA[t["num"]]()
    acts=TOPIC_ACTS[t["num"]]
    # One tile per lab in this topic — never a fixed 3-up padded with placeholders,
    # and summary lines are whole phrases (never truncated mid-word).
    lab_tiles=[(f"Lab {a['num']} — {a['title'].split('—')[-1].strip()}",
                a["build"]) for a in acts]
    tile_grid(f"Hands-On Labs — {t['title']}", lab_tiles,
              kicker="WHAT YOU'LL DO", cols=1, size=15, accent=TEAL)
    for a in acts:
        short=a.get("short", a["title"])
        activity_overview(f"LAB {a['num']}", a["title"], a["desc"], a["build"], a["services"], kicker=f"TOPIC {t['code']} · HANDS-ON")
        # what the learner will actually see — the lab's website / n8n canvas
        sites=a.get("site",[])
        for img,cap in sites:
            image_slide(short+" — What You'll Build", img, cap,
                        kicker=f"LAB {a['num']} · THE APPLICATION", accent=VIOLET)
        flows=a.get("flows",[])
        for fi,(img,cap) in enumerate(flows):
            suffix=" — Workflow" if len(flows)==1 else (" — Ingestion Workflow" if fi==0 else " — Answering Workflow")
            image_slide(short+suffix, img, cap,
                        kicker=f"LAB {a['num']} · THE WORKFLOW", accent=TEAL)
        steps=a["steps"]; total=len(steps)
        for i,st in enumerate(steps,1):
            instr,cmd = st[0], st[1]
            why = st[2] if len(st)>2 else ""
            step_slide(f"LAB {a['num']} · HANDS-ON", short, i, total, instr, cmd,
                       why=why, progress=True)
        test_slide(short, a["test"], kicker=f"LAB {a['num']} · VERIFY")
        tile_grid(f"What You Learned — Lab {a['num']}", a["learned"],
                  kicker="LAB DEBRIEF", cols=1, size=15, accent=TEAL)  # (label,text) or plain str
    # Topic recap: what you can now do, plus the key takeaways from each lab.
    # A takeaway may be a plain string (rendered as body text with no heading) or a
    # (label, text) pair. Never derive a heading by truncating the body — that
    # produces a clipped duplicate of the sentence beneath it. Headings stay SHORT
    # so they cannot wrap and push the body past the tile border.
    recap=[(a["learned"][0][0] if isinstance(a["learned"][0],tuple) else f"Lab {a['num']}",
            f"Lab {a['num']} — you can now "+a["objective"].split("(")[0].strip()+".")
           for a in acts]
    for a in acts:
        for x in a["learned"][1:3]:
            recap.append(x if isinstance(x,tuple) else x)
    tile_grid(f"Recap — {t['title']}", recap[:6],
              kicker="TOPIC RECAP", cols=1, size=13)

# ---------------------------------------------------------------- CLOSE
section("WRAP-UP","Course Summary & Next Steps","")
tile_grid("What You Achieved",[
 ("LO1 · n8n and AI agents","Built a trigger-and-action workflow and explained how an LLM agent differs from generative AI."),
 ("LO2 · Webhook-triggered agents","Put an AI agent behind a real website, with tools, structured output and an audit log."),
 ("LO3 · Agentic chatbots","Designed a chatbot that collects contact details and refuses to give regulated advice."),
 ("LO4 · Human in the loop","Paused a workflow on an approval gate so no drafted communication was sent unsupervised."),
 ("LO5 · RAG","Ingested 20 documents into a vector store and grounded a chatbot so it stopped inventing answers.")],
 kicker="LEARNING OUTCOMES",cols=1,size=14)
tile_grid("Taking This Back to Work",[
 ("Start with one painful process","Pick something repetitive, high-volume and low-risk. Automate that first."),
 ("Map it before you build it","Draw the trigger, the decisions and the actions on paper. The canvas comes second."),
 ("Decide where the human belongs","Anything irreversible, regulated or expensive keeps an approval gate."),
 ("Ground the agent in your own data","RAG over your policies and documents beats a general model every time."),
 ("Log everything from day one","You will need the audit trail long before you think you will."),
 ("Iterate with real cases","Test with the questions you fear, not the ones you hope for.")],
 kicker="NEXT STEPS",cols=2,size=14)
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
big_statement("Thank You!",
 "Keep your n8n instance running and keep building. The next process you automate is the one you were "
 "dreading this morning.","HAPPY AUTOMATING",color=TEAL)

# ---- verify the LP's slide index agrees with what we actually emitted ----
import slide_index
_actual=len(prs.slides.__iter__.__self__._sldIdLst)
assert slide_index.TOTAL==_actual, (
    f"slide_index.TOTAL={slide_index.TOTAL} but the deck has {_actual} slides. "
    "Update slide_index.py so the Lesson Plan's slide references stay correct.")
for _k,(_a,_b) in slide_index.SLIDES.items():
    assert 1<=_a<=_b<=_actual, f"slide_index range {_k}={_a}-{_b} is outside 1..{_actual}"

OUT=os.path.join(REPO,"courseware",f"{C.SHORT_TITLE}-{C.VERSION}.pptx")
prs.save(OUT)
print(f"Saved {OUT}  ({_actual} slides)")
print(f"slide_index verified: {slide_index.TOTAL} slides, {len(slide_index.SLIDES)} named blocks")
