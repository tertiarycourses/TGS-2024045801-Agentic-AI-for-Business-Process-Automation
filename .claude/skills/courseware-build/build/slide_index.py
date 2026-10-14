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
import concepts as CN
from data_domain1 import DOMAIN1
from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3
ACT = DOMAIN1 + DOMAIN2 + DOMAIN3

# concepts that are followed by an illustrating n8n screenshot slide.
# MUST match CONCEPT_IMAGES in build_slides.py.
CONCEPT_IMAGE_KEYS = {
    "trigger_nodes", "data_nodes", "test_vs_prod_exec", "what_is_webhook",
    "webhook_vs_http", "rag_pipeline", "chunking", "vector_stores",
}

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
_adv()      # n8n Training Accounts
_adv()      # Skills Framework (TSC)
_adv()      # TSC Abilities and Knowledge
_adv()      # Lesson Plan overview
_adv()      # Learning Outcomes
_adv()      # Course Journey — Five Connected Labs
_adv()      # Criteria for Funding
_adv()      # Briefing for Assessment
_adv()      # Assessment
_adv()      # Assessment Flow
_mark("admin", a0, _n)

# Topic 1 opens with the "why agentic AI, and why workflow first" slides straight
# after its divider (history of AI, agentic AI vs AI agents, workflow first vs AI
# first, AI-assisted workflow creation + n8n Assistant
# screenshot + free AI credits + social-campaign demo, AI security x2, business value, use cases, platform tiers).
# MUST match topic1_intro() in build_slides.py — the build asserts it.
TOPIC1_INTRO = 12

# ---- TOPICS ----
for tp in C.TOPICS:
    tnum = tp["num"]
    t0 = _n + 1
    _adv()                                       # section divider
    if tnum == 1:
        _adv(TOPIC1_INTRO)                       # the Topic 1 opener
        _mark("topic1_intro", t0, _n)

    keys = CN.TOPIC_CONCEPTS[tnum]
    c0 = _n + 1
    for k in keys:
        _adv()                                   # the concept slide
        if k in CONCEPT_IMAGE_KEYS:
            _adv()                               # its n8n screenshot
    c_end = _n

    # sub-marks the lesson plan refers to
    if tnum == 1:
        # topic 1 concepts run: platform/nodes/data (through "credentials"),
        # then the agent block, then the webhook block
        def _upto(key):
            n = c0
            for k in keys:
                n += 1 + (1 if k in CONCEPT_IMAGE_KEYS else 0)
                if k == key:
                    return n - 1
            return c_end
        _mark("topic1_concepts", c0, _upto("credentials"))
        _mark("topic1_agent", _upto("credentials") + 1, _upto("mcp_in_n8n"))
        _mark("topic1_webhook", _upto("mcp_in_n8n") + 1, c_end)
    elif tnum == 2:
        _mark("topic2_hitl", t0, c_end)
    elif tnum == 3:
        _mark("topic3_concepts", t0, c_end)

    for a in [x for x in ACT if x["topic"] == tnum]:
        l0 = _n + 1
        _adv(max(1, len(a.get("canvas", []))))   # one lab slide per workflow canvas
        _adv(len(a.get("site", [])))             # the application screenshot(s)
        _adv()                                   # verify + debrief
        _mark(f"lab{a['num']}", l0, _n)
    if tnum in (1, 2):
        _adv()                                   # lunch / tea break divider
    _mark(f"topic{tnum}_all", t0, _n)

# ---- CLOSE ----
w0 = _n + 1
_adv()      # section: Wrap-up
_adv()      # What You Achieved
_adv()      # Taking This Back to Work
_mark("wrapup", w0, _n)
_adv()      # Support
_adv()      # Assessment
_adv()      # Assessment Flow
_adv()      # Digital Attendance
_adv()      # Thank You

TOTAL = _n

if __name__ == "__main__":
    for k in sorted(SLIDES, key=lambda x: SLIDES[x][0]):
        print(f"{k:22s} {SLIDES[k][0]:>4}–{SLIDES[k][1]}")
    print("TOTAL", TOTAL)
