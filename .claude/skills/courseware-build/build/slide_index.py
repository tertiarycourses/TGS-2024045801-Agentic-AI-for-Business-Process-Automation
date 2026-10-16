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
# after its divider: history of AI, generative vs agentic AI, agentic AI vs AI agents,
# workflow first vs agent first, AI-assisted creation, platform tiers, business value,
# use cases, AI security x2, what is n8n x2, training accounts, sign in, n8n Assistant
# screenshot and the social-campaign demo.
# MUST match topic1_intro() in build_slides.py — the build asserts it.
TOPIC1_INTRO = 16

# Topic 2's Telegram HR chatbot demo (overview, BotFather steps, n8n Assistant prompt, n8n canvas, connect-and-publish steps, live chat).
# MUST match telegram_demo() in build_slides.py — the build asserts it.
TELEGRAM_DEMO_SLIDES = 6

def _concepts(keys, extra_after=()):
    """Slides for a run of concepts: each concept, its screenshot, and any extra slide."""
    for k in keys:
        _adv()
        if k in CONCEPT_IMAGE_KEYS:
            _adv()
        if k in extra_after:
            _adv()

def _lab(a):
    """MUST match lab_block() in build_slides.py."""
    l0 = _n + 1
    if a.get("primer"):
        _adv()                                   # how the building blocks fit
    _adv(max(1, len(a.get("canvas", []))))       # one lab slide per workflow canvas
    if a.get("n8n_shot"):
        _adv()                                   # the real n8n canvas screenshot
    _adv(len(a.get("site", [])))                 # the application screenshot(s)
    _adv(len(a.get("extras", [])))               # step screenshots, how-to strips, gallery
    _adv()                                       # verify + debrief
    _mark(f"lab{a['num']}", l0, _n)

# ---- TOPICS ----
for tp in C.TOPICS:
    tnum = tp["num"]
    labs = [x for x in ACT if x["topic"] == tnum]
    t0 = _n + 1
    _adv()                                       # section divider
    if tnum == 1:
        _adv(TOPIC1_INTRO)
        _mark("topic1_intro", t0, _n)
        c0 = _n + 1; _concepts(CN.TOPIC1_FUNDAMENTALS); _mark("topic1_concepts", c0, _n)
        _lab(labs[0])
        _adv()                                   # lunch break divider
        c0 = _n + 1; _concepts(CN.TOPIC1_AGENT, extra_after=("model_params",))   # + free AI credits
        _mark("topic1_agent", c0, _n)
        c0 = _n + 1; _concepts(CN.TOPIC1_WEBHOOK); _mark("topic1_webhook", c0, _n)
        _lab(labs[1])
    elif tnum == 2:
        # knowledge before the lab: chatbot concepts → Lab 3 → HITL + guardrails → Lab 4
        c0 = _n + 1; _concepts(CN.TOPIC2_CHATBOT)
        _adv(TELEGRAM_DEMO_SLIDES)               # Telegram HR chatbot demo, before Lab 3
        _mark("topic2_chatbot", t0, _n)
        _lab(labs[0])
        c0 = _n + 1; _concepts(CN.TOPIC2_HITL); _mark("topic2_hitl", c0, _n)
        _lab(labs[1])
        _adv()                                   # tea break divider
    else:
        _concepts(CN.TOPIC_CONCEPTS[tnum])
        _mark("topic3_concepts", t0, _n)
        for a in labs:
            _lab(a)
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
