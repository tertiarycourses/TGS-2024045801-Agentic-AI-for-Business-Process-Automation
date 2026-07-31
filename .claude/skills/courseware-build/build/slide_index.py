"""Compute the deck's slide numbering WITHOUT building the PPTX.

build_slides.py emits slides in a fixed order. This module replays that order and
records the 1-based page number of each named block, so build_lesson_plan.py can
print slide references that always match the current deck. If the deck's build
order changes, change it here too — the self-check at the bottom of
build_slides.py compares the two and fails loudly if they disagree.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import course_data as C
from data_domain1 import DOMAIN1
from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3
ACT = DOMAIN1 + DOMAIN2 + DOMAIN3

_n = 0
def _adv(k=1):
    global _n
    _n += k
    return _n

SLIDES = {}
def _mark(name, start, end):
    SLIDES[name] = (start, end)

# 1 cover
_adv()                                   # 1  cover

# ---- ADMIN ----
a0 = _n + 1
_adv()      # section: Course Administration
_adv()      # Digital Attendance
_adv()      # trainer (general)
_adv()      # trainer (named)
_adv()      # Let's Know Each Other
_adv()      # Ground Rules
_adv()      # Download Course Material (image)
_adv()      # Download Course Material (steps)
_adv()      # Get the Course Workflows
_adv()      # Skills Framework (TSC)
_adv()      # TSC Abilities and Knowledge
_adv()      # Lesson Plan overview
_adv()      # Learning Outcomes
_adv()      # Course Outline
_adv()      # Criteria for Funding
_adv()      # Briefing for Assessment
_adv()      # Assessment
_adv()      # Assessment Flow
_mark("admin", a0, _n)

# ---- FOUNDATION ----
f0 = _n + 1
_adv()      # section: Why Agentic AI
_adv()      # Evolution of AI
_adv()      # big statement: agentic AI does the work
_adv()      # image: agent loop
_adv()      # Agentic vs Generative
_adv()      # image: RPA -> APA
_adv()      # Business value
_adv()      # Use cases
_adv()      # Platform tiers
_mark("foundation", f0, _n)

# ---- TOPICS ----
# per-topic extra teaching slide counts, in build order (must match build_slides.py)
EXTRA_COUNTS = {1: 12, 2: 8, 3: 6}
# concept images per topic
CONCEPT_IMAGES = {3: 3}
# sub-marks inside topic 1 / 2 / 3 used by the lesson plan
for tp in C.TOPICS:
    tnum = tp["num"]
    t0 = _n + 1
    _adv()                                   # section divider
    _adv()                                   # key concepts tile grid
    ci = CONCEPT_IMAGES.get(tnum, 0)
    if ci:
        c0 = _n + 1
        _adv(ci)                             # concept image slides
    extra_start = _n + 1
    _adv(EXTRA_COUNTS[tnum])                 # rich teaching slides
    extra_end = _n

    if tnum == 1:
        # 12 extras: 7 on the platform/nodes/data/execution, then 5 agent-focused
        _mark("topic1_concepts", t0, extra_start + 6)
        _mark("topic1_agent",   extra_start + 7, extra_end)
    elif tnum == 2:
        # 8 extras: 4 on agentic chatbots, then 4 on human-in-the-loop
        _mark("topic2_chatbot", t0, extra_start + 3)
        _mark("topic2_hitl",    extra_start + 4, extra_end)
    elif tnum == 3:
        _mark("topic3_concepts", t0, extra_end)

    _adv()                                   # cards3 "Hands-On Labs"
    for a in [x for x in ACT if x["topic"] == tnum]:
        l0 = _n + 1
        _adv()                               # activity overview
        _adv(len(a.get("flows", [])))        # workflow diagram(s)
        _adv(len(a["steps"]))                # step slides
        _adv()                               # test slide
        _adv()                               # what you learned
        _mark(f"lab{a['num']}", l0, _n)
    _adv()                                   # topic recap
    _mark(f"topic{tnum}_all", t0, _n)

# ---- CLOSE ----
w0 = _n + 1
_adv()      # section: Wrap-up
_adv()      # What You Achieved
_adv()      # Taking This Back to Work
_mark("wrapup", w0, _n)
_adv()      # Assessment
_adv()      # Assessment Flow
_adv()      # Digital Attendance
_adv()      # Support
_adv()      # Thank You

TOTAL = _n

if __name__ == "__main__":
    for k in sorted(SLIDES, key=lambda x: SLIDES[x][0]):
        print(f"{k:22s} {SLIDES[k][0]:>4}–{SLIDES[k][1]}")
    print("TOTAL", TOTAL)
