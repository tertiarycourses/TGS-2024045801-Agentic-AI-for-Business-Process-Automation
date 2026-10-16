#!/usr/bin/env python3
"""Generate the Agentic AI for Business Process Automation (TGS-2024045801) Lesson Plan.

Cover page + Document Version Control Record + auto TOC + Arial 11pt body +
colour-coded 2-day schedule tables (9:30am-6:30pm, 7 training hours/day, 1h
lunch, tea breaks within). Topics/labs come from course_data + the domain data
files, and the SLIDE NUMBERS are computed from the same build order as
build_slides.py, so the LP can never drift from the deck.
"""
import os, sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import course_data as C
from data_domain1 import DOMAIN1
from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3
ACT=DOMAIN1+DOMAIN2+DOMAIN3
import prodoc
from slide_index import SLIDES      # computed slide map, shared with build_slides.py

def _find_repo(start):
    env=os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d=start
    for _ in range(8):
        d=os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(HERE))
REPO=_find_repo(HERE); ASSETS=os.path.join(os.path.dirname(HERE),"assets")

BRAND=RGBColor(0x1F,0x6F,0xEB); DARK=RGBColor(0x11,0x18,0x27); GREY=RGBColor(0x55,0x5B,0x66)
HEADER_FILL="1F6FEB"; TOPIC_FILL="E8F0FE"; BREAK_FILL="FFF4E5"; LUNCH_FILL="FDE9D9"; ASSESS_FILL="E8F7EE"

def S(key):
    """Slide reference string for the schedule, e.g. 'Slides 44–58'."""
    r=SLIDES.get(key)
    if not r: return ""
    a,b=r
    return f"Slides {a}–{b}" if b>a else f"Slide {a}"

def lab(n):
    return next(a for a in ACT if a["num"]==n)

# ------------------------------------------------ schedule (single source of truth for timing)
# (start, end, minutes, kind, activity_text)
#
# WSQ rule: each training day is 9:30am–6:30pm with a 1-hour lunch, giving exactly
# 480 minutes (8 hours) of instructional time. Tea breaks are counted WITHIN the
# instructional total; only lunch is excluded. The self-check below enforces this.
SCHEDULE = {
 1: (C.DAY_THEMES[1], [
    ("9:30","10:00",30,"admin",
     "Welcome, trainer and learner introductions, ground rules, course outline, learning outcomes, "
     "Skills Framework alignment and mandatory digital attendance (AM). "+S("admin")),
    ("10:00","11:00",60,"topic",
     "Topic 1 — Overview of n8n and AI Agents: why agentic AI, and why workflow first — a brief "
     "history of AI 2023–2026, generative AI vs agentic AI, agentic AI vs AI agents, workflow first vs "
     "agent first, AI-assisted workflow creation, platform tiers (no-code, AI-assisted low-code, "
     "AI-generated full-code), business value, use cases, the five principles of AI security, what "
     "n8n is, signing in to n8n, and a demo that builds a social media campaign workflow with n8n "
     "Assistant. "+S("topic1_intro")),
    ("11:00","11:15",15,"break","Tea break"),
    ("11:15","11:45",30,"topic",
     "Topic 1 (continued) — n8n fundamentals: trigger nodes, data-processing nodes, storage and app "
     "actions, JSON and expressions, test vs production executions, and credentials. "+S("topic1_concepts")),
    ("11:45","12:30",45,"lab",
     f"Hands-on {lab(1)['title']}: build the form-to-Gmail workflow, publish it, copy the form's "
     "Production URL and create a QR-code event flyer; present and scan-test the flyers. "+S("lab1")),
    ("12:30","13:30",60,"lunch","Lunch break"),
    ("13:30","15:15",105,"topic",
     "Topic 1 (continued) — The building blocks of an AI agent, before Lab 2: the AI agent and its "
     "loop, the model (popular LLM providers, model parameters and temperature, claiming the free AI "
     "credits), tools and MCP, instructions with worked examples, memory, and structured output. "
     +S("topic1_agent")),
    ("15:15","15:30",15,"break","Tea break"),
    ("15:30","16:15",45,"topic",
     "Topic 1 (continued) — Webhooks: the inbound URL, webhook vs HTTP Request, GET vs POST, Test vs "
     "Production URL and webhook configuration. "+S("topic1_webhook")),
    ("16:15","18:15",120,"lab",
     f"Hands-on {lab(2)['title']}: how the webhook, agent, model, tools, instructions, memory and "
     "structured output fit together, then build and test the onboarding agent. "+S("lab2")),
    ("18:15","18:30",15,"recap","Day 1 recap, Q&A and PM digital attendance"),
 ]),
 2: (C.DAY_THEMES[2], [
    ("9:30","9:45",15,"recap","Day 1 recap and mandatory digital attendance (AM)"),
    ("9:45","10:30",45,"topic",
     "Topic 2 — Agentic Chatbot and Human in the Loop, before Lab 3: rule-based vs agentic "
     "workflows, designing a safe agentic chatbot, and a chatbot demo on Telegram — learners create "
     "a bot with BotFather /newbot, build an HR policy chatbot with n8n Assistant from one prompt, "
     "then connect, publish and chat with it. "
     +S("topic2_chatbot")),
    ("10:30","11:00",30,"lab",
     f"Hands-on {lab(3)['title']}: import the workflow, read the contact gate, the non-advisory rule "
     "and the FAQ, and deploy the chatbot behind the website. "+S("lab3")),
    ("11:00","11:15",15,"break","Tea break"),
    ("11:15","11:45",30,"lab",
     f"Hands-on {lab(3)['short']} (continued): test the contact gate and the four compliance probes, "
     "and debrief."),
    ("11:45","12:30",45,"topic",
     "Topic 2 (continued) — Human in the loop and guardrails, before Lab 4: human in, on and out of "
     "the loop; how an approval suspends a running workflow; when a human belongs in the workflow; "
     "and guardrails. "+S("topic2_hitl")),
    ("12:30","13:30",60,"lunch","Lunch break"),
    ("13:30","15:00",90,"lab",
     f"Hands-on {lab(4)['title']}: the approve and decline paths. "+S("lab4")),
    ("15:00","15:15",15,"break","Tea break"),
    ("15:15","16:30",75,"topic",
     "Topic 3 — Retrieval-Augmented Generation: why retrieval rather than a bigger prompt, the RAG "
     "pipeline, tokenization and embeddings, chunking, vector stores and grounding. "+S("topic3_concepts")),
    ("16:30","18:00",90,"lab",
     f"Hands-on {lab(5)['title']}: ingestion and the grounded chatbot. "+S("lab5")),
    ("18:00","18:30",30,"recap",
     "Course recap, taking it back to work, Q&A. "+S("wrapup")),
    ("18:30","18:45",15,"assess",
     "Briefing for Assessment and Assessment digital attendance"),
    ("18:45","19:45",60,"assess",
     "Written Assessment (WA) — Short-Answer Questions (SAQ), 1 hour, open book"),
    ("19:45","20:45",60,"assess",
     "Practical Performance (PP) — hands-on n8n build tasks, 1 hour, open book. "
     "TRAQOM survey and Assessment digital attendance"),
 ]),
}

# Enforce the WSQ 8-hour rule at build time rather than trusting the table above.
#
# 9:30am-6:30pm is 540 elapsed minutes; removing the 1-hour lunch leaves exactly
# 480. So the tea breaks are necessarily counted WITHIN the instructional time —
# excluding them as well would make the rule arithmetically unsatisfiable.
# Instructional minutes therefore exclude lunch and the assessment block only.
for _d,(_theme,_rows) in SCHEDULE.items():
    _instr=sum(m for _s,_e,m,k,_t in _rows if k not in ("lunch","assess"))
    assert _instr==480, (
        f"Day {_d} has {_instr} instructional minutes; the WSQ rule requires exactly 480 "
        "(8 hours: 9:30am-6:30pm less a 1-hour lunch, tea breaks counted within).")

# ------------------------------------------------ build document
doc=Document()
normal=doc.styles["Normal"]; normal.font.name="Arial"; normal.font.size=Pt(11)
prodoc.style_headings(doc)

prodoc.add_cover_page(doc,"LESSON PLAN",C.TITLE,C.VERSION.lstrip("v"),
                      org_logo=os.path.join(ASSETS,"tertiary-infotech-logo.png"),
                      course_logo=os.path.join(ASSETS,"n8n-logo.png"), course_code=C.COURSE_CODE)
prodoc.add_version_control(doc,[
 ("1.0","31 July 2026",
  "Initial release — 2-day (14-hour) lesson plan for Agentic AI for Business Process Automation, "
  "aligned to the 5 hands-on labs and TSC "+C.TSC_CODE+".",C.TRAINER),
 ("1.1","1 August 2026",
  "Day 2 rescheduled so the final assessment follows instruction within the training day; daily "
  "timing now driven from a single source shared with the slide deck; assessment time stated "
  "separately from instructional time.","Dr. Alfred Ang"),
 ("1.2","1 August 2026",
  "Added a screenshot of each lab's application — the four lab websites with their chat widgets "
  "open, plus the Lab 1 n8n canvas and sample flyer — to the slide deck and the Learner Guide.",
  C.TRAINER),
 ("2.0","8 August 2026",
  "Slide deck restyled to the house reference format (visual concept cards, chevron flow strips, "
  "comparison panels and takeaway bands). Lab step slides removed from the deck; the click-by-click "
  "steps now live only in the Learner Guide, and each lab carries a rendered screenshot of its own "
  "n8n canvas. Concept coverage expanded: trigger nodes, data-processing nodes, the four components "
  "of an AI agent, instruction design, model parameters, MCP, webhooks (GET/POST, Test vs Production "
  "URL) and human-in-the-loop with guardrails.",C.TRAINER),
 ("2.1","15 October 2026",
  "Topic 1 now opens with the modern view of agentic automation, replacing the separate Foundation section: a brief history of AI 2023–2026 (prompt, context and harness engineering to AI agents), agentic AI vs AI agents, workflow first vs agent first, AI-assisted workflow creation with n8n Assistant (plus claiming the free AI credits and a social media campaign demo), an n8n training-accounts slide, the five principles of AI security and why workflow first is more secure, and the business value of workflow-first agentic automation. Slide references updated to match.",C.TRAINER),
 ("2.2","15 October 2026",
  "Topic 1 re-sequenced so each lab follows the concepts it needs: n8n fundamentals, then Lab 1, then the AI agent building blocks (AI agent, model, tools and MCP, instructions, memory) and webhooks, then Lab 2. Lab 1 now covers publishing the workflow, copying the form’s Production URL and creating a QR-code flyer, with step screenshots and flyers from previous learners. Lab 2 opens with how the building blocks fit together. Platform tiers updated for AI-assisted low-code and AI-generated full-code. New LMS login screenshot; Publish replaces the retired Active toggle. Schedule and slide references updated.",C.TRAINER),
 ("2.3","16 October 2026",
  "Every lab now follows the knowledge it needs. Topic 2 is taught in two blocks: rule-based vs agentic workflows, designing a safe agentic chatbot and a Telegram HR chatbot demo (BotFather /newbot, built with n8n Assistant from one prompt, then a live chat), then Lab 3; then human in, on and out of the loop, how an approval suspends a workflow, when to put a human in the loop and guardrails, then Lab 4. The agent loop is now explained as Context → Plan → Action → Verify and repeat. Lab workflow files and their n8n names are now 'Lab N - <description>', replacing the old LU/Activity names. Real n8n canvas screenshots added for Lab 2, Lab 3 and the Telegram demo, plus a live Telegram chat. Each lab's key concepts in the Learner Guide now sit directly before that lab. Day 2 schedule and slide references updated.",C.TRAINER),
 ("2.4","16 October 2026",
  "Real n8n screenshots added and explained: the Lab 4 approval workflow and the Lab 4 website with its lab configuration panel; n8n's Guardrails node (an input check and an output sanitiser) after the guardrails concept; a GET webhook example that publishes a recipe page, in the webhooks block before Lab 2; and the Build with AI start screen in the Telegram chatbot demo. PDFs made compatible with Microsoft Edge (the theme shadow LibreOffice exported as masked bitmaps is removed). Lab websites now say Published instead of the retired Active toggle.",C.TRAINER),
 (C.VERSION.lstrip("v"),C.VERSION_DATE,
  "Real n8n screenshots added and explained for Lab 5: the ingestion workflow (fetch the brochures, split and embed, insert into the vector store) directly after the ingestion workflow slide, the answering workflow (webhook, agent and model, retrieval tool) directly after the answering workflow slide, and a live Course Assistant conversation showing a misspelt question still retrieving the right brochures, fees quoted from the brochure, and the assistant admitting a gap instead of inventing a fee. Notes that the ingestion and answering workflows must use the same embedding model and memory key whichever provider is used. Slide references updated.",C.TRAINER),
])
prodoc.add_toc(doc)

def H(text,level=1):
    return doc.add_heading(text,level=level)

H("Course Information",1)
info=[("Course Title",C.TITLE),("WSQ Course Reference",C.COURSE_CODE),
      ("TSC Title / Code",f"{C.TSC_TITLE}  ·  {C.TSC_CODE}"),
      ("Training Provider",C.ORG+"  ("+C.UEN.replace('UEN: ','UEN ')+")"),
      ("Duration",f"{C.DAYS} days · {C.HOURS_PER_DAY} training hours per day ({C.TRAINING_HOURS} hours)"),
      # TIMING_NOTE is a complete sentence, so it takes no article in front of it.
      ("Daily Timing",f"Day 1: {C.DAY_TIMES[1]}.  Day 2: {C.DAY_TIMES[2]}.  "
                      f"{C.TIMING_NOTE}."),
      ("Mode","Instructor-led, hands-on workflow-automation labs built in n8n"),
      ("Trainer",C.TRAINER)]
t=doc.add_table(rows=0,cols=2); t.style="Table Grid"
for k,v in info:
    c=t.add_row().cells; c[0].text=""; r=c[0].paragraphs[0].add_run(k); r.bold=True; r.font.size=Pt(10)
    prodoc._shade_cell(c[0],TOPIC_FILL)
    c[1].text=""; c[1].paragraphs[0].add_run(v).font.size=Pt(10)

H("Learning Outcomes",1)
doc.add_paragraph("On completion of this course, learners will be able to:")
for lo in C.LEARNING_OUTCOMES:
    p=doc.add_paragraph(style="List Bullet"); p.add_run(lo).font.size=Pt(10.5)

H("Skills Framework Alignment",1)
doc.add_paragraph(f"This course is mapped to the TSC {C.TSC_TITLE} ({C.TSC_CODE}).")
ta=doc.add_table(rows=0,cols=2); ta.style="Table Grid"
hdr=ta.add_row().cells
for i,htext in enumerate(["Code","Ability / Knowledge statement"]):
    cell=hdr[i]; cell.text=""; r=cell.paragraphs[0].add_run(htext); r.bold=True
    r.font.size=Pt(10); r.font.color.rgb=RGBColor(0xFF,0xFF,0xFF); prodoc._shade_cell(cell,HEADER_FILL)
for code,txt_ in C.TSC_ABILITIES+C.TSC_KNOWLEDGE:
    cells=ta.add_row().cells
    cells[0].text=""; r=cells[0].paragraphs[0].add_run(code); r.bold=True; r.font.size=Pt(9.5)
    prodoc._shade_cell(cells[0],TOPIC_FILL)
    cells[1].text=""; cells[1].paragraphs[0].add_run(txt_).font.size=Pt(9.5)
for row in ta.rows:
    row.cells[0].width=Inches(0.8); row.cells[1].width=Inches(5.9)

H("Assessment",1)
for a in [C.ASSESSMENT["written"],C.ASSESSMENT["practical"],
          "Format: Open Book — course slides, Learner Guide and approved materials only.",
          "The Written Assessment covers the Knowledge (K) statements; the Practical Performance covers the Ability (A) statements.",
          "Final assessment is conducted at the end of Day 2.",C.ASSESSMENT["note"]]:
    p=doc.add_paragraph(style="List Bullet"); p.add_run(a).font.size=Pt(10.5)

def set_cell(cell,text,bold=False,size=9.5,color=None,fill=None,align=None):
    cell.text=""; p=cell.paragraphs[0]
    if align: p.alignment=align
    r=p.add_run(text); r.bold=bold; r.font.size=Pt(size); r.font.name="Arial"
    if color: r.font.color.rgb=color
    if fill: prodoc._shade_cell(cell,fill)

KIND_FILL={"topic":TOPIC_FILL,"break":BREAK_FILL,"lunch":LUNCH_FILL,"assess":ASSESS_FILL,
           "admin":"F3F5F8","recap":"F3F5F8","lab":None}

H("Course Schedule",1)
EXPECT=C.HOURS_PER_DAY*60          # instructional minutes per day (excludes lunch, tea and assessment)
grand_train=0; grand_assess=0
for day,(theme,rows) in SCHEDULE.items():
    H(f"Day {day} — {theme}",2)
    tbl=doc.add_table(rows=0,cols=3); tbl.style="Table Grid"; tbl.alignment=WD_TABLE_ALIGNMENT.CENTER
    hdr=tbl.add_row().cells
    for i,htext in enumerate(["Time","Duration","Topic / Activity (with slide references)"]):
        set_cell(hdr[i],htext,bold=True,size=10,color=RGBColor(0xFF,0xFF,0xFF),fill=HEADER_FILL)
    training=0; assessing=0
    for start,end,mins,kind,text in rows:
        cells=tbl.add_row().cells; fill=KIND_FILL.get(kind)
        set_cell(cells[0],f"{start}–{end}",bold=(kind in ("topic","assess")),size=9.5,fill=fill)
        set_cell(cells[1],f"{mins} min",size=9.5,fill=fill)
        set_cell(cells[2],text,bold=(kind in ("topic","assess")),size=9.5,fill=fill)
        if kind=="assess": assessing+=mins
        # Tea breaks count within the instructional time; only lunch is excluded.
        elif kind!="lunch": training+=mins
    for row in tbl.rows:
        row.cells[0].width=Inches(1.0); row.cells[1].width=Inches(0.8); row.cells[2].width=Inches(4.9)
    p=doc.add_paragraph()
    note=f"Instructional time: {training} minutes ({training//60} hours)."
    if assessing:
        note+=("  Assessment: 2 hours (WA 1 hour + PP 1 hour), plus a 15-minute briefing.")
    note+=("  The day runs 9:30 am - 6:30 pm: the 1-hour lunch is excluded from "
           "instructional time and the tea breaks are counted within it.")
    r=p.add_run(note); r.italic=True; r.font.size=Pt(9.5); r.font.color.rgb=GREY
    grand_train+=training; grand_assess+=assessing
    assert training==EXPECT, f"Day {day} instructional minutes = {training}, expected {EXPECT}"

p=doc.add_paragraph()
r=p.add_run(f"Total instructional time across the course: {grand_train//60} hours "
            f"({C.DAYS} days × {C.HOURS_PER_DAY} hours), plus 2 hours of assessment "
            f"(WA 1 hour + PP 1 hour) and a 15-minute assessment briefing.")
r.bold=True; r.font.size=Pt(10)
assert grand_train==C.TRAINING_HOURS*60, \
    f"Course instructional minutes = {grand_train}, expected {C.TRAINING_HOURS*60}"

H("Lab Reference (aligned to topics and learning outcomes)",1)
tt=doc.add_table(rows=0,cols=4); tt.style="Table Grid"
hdr=tt.add_row().cells
for i,htext in enumerate(["Topic","Outcomes","Labs","Deck slides"]):
    set_cell(hdr[i],htext,bold=True,size=10,color=RGBColor(0xFF,0xFF,0xFF),fill=HEADER_FILL)
for tp in C.TOPICS:
    acts=[a for a in ACT if a["topic"]==tp["num"]]
    cells=tt.add_row().cells
    set_cell(cells[0],f"Topic {tp['code']}: {tp['title']}",bold=True,size=9.5,fill=TOPIC_FILL)
    set_cell(cells[1],tp["weighting"],size=9.5,fill=TOPIC_FILL)
    set_cell(cells[2],", ".join(f"Lab {a['num']}" for a in acts),size=9.5)
    set_cell(cells[3],S(f"topic{tp['num']}_all"),size=9.5)
for row in tt.rows:
    row.cells[0].width=Inches(2.6); row.cells[1].width=Inches(0.9)
    row.cells[2].width=Inches(1.6); row.cells[3].width=Inches(1.4)

prodoc.add_page_numbers(doc)
prodoc.enable_update_fields(doc)
OUT=os.path.join(REPO,"courseware",f"LP-{C.SHORT_TITLE}.docx")
doc.save(OUT)
print("Saved",OUT)
