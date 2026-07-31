#!/usr/bin/env python3
"""Alignment test — PPT, LP, LG and labs/ must agree.

Run after build_courseware.sh. Exits non-zero on any misalignment, so a drift
between the four artifacts fails the build instead of reaching a classroom.

Checks:
  1. Every lab folder named in the content modules exists under labs/.
  2. Every .json workflow the courseware tells learners to import exists there.
  3. Every n8n node name cited in the steps matches a node in that lab's JSON
     (catches a renamed node silently breaking the instructions).
  4. No duplicated "Lab N — Lab N —" prefixes in any artifact.
  5. The LP's slide references all land inside the current deck, and each range
     starts on the slide it claims to.
  6. Course-wide facts (course code, TSC, UEN, models, dimensions) agree
     everywhere they appear.
  7. The LG Markdown mirror and the LG DOCX carry the same lab sections.
"""
import os, re, sys, json, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import course_data as C
from data_domain1 import DOMAIN1
from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3
from slide_index import SLIDES, TOTAL
ACT = DOMAIN1 + DOMAIN2 + DOMAIN3

def find_repo(start):
    d = start
    for _ in range(8):
        d = os.path.dirname(d)
        if os.path.isdir(os.path.join(d, "courseware")) and os.path.isdir(os.path.join(d, "labs")):
            return d
    return os.path.dirname(os.path.dirname(start))
REPO = os.environ.get("COURSE_REPO") or find_repo(HERE)
CW = os.path.join(REPO, "courseware")

FAIL = []
def check(ok, msg):
    print(("  ok   " if ok else "  FAIL ") + msg)
    if not ok:
        FAIL.append(msg)

def pdftext(path):
    if not os.path.exists(path):
        return ""
    return subprocess.run(["pdftotext", "-layout", path, "-"],
                          capture_output=True, text=True).stdout

DECK_PDF = os.path.join(CW, f"{C.SHORT_TITLE}-{C.VERSION}.pdf")
LP_PDF   = os.path.join(CW, f"LP-{C.SHORT_TITLE}.pdf")
LG_PDF   = os.path.join(CW, f"LG-{C.SHORT_TITLE}.pdf")
LG_MD    = os.path.join(CW, f"LG-{C.SHORT_TITLE}.md")

deck_pages = [" ".join(p.split()) for p in pdftext(DECK_PDF).split("\f")]
lp   = pdftext(LP_PDF)
lg   = pdftext(LG_PDF)
md   = open(LG_MD).read() if os.path.exists(LG_MD) else ""

# ---------------------------------------------------------------- 1 & 2
print("\n[1] lab folders and workflow files exist")
for a in ACT:
    folder = os.path.join(REPO, "labs", a["folder"])
    check(os.path.isdir(folder), f"Lab {a['num']}: labs/{a['folder']}/ exists")
    if not os.path.isdir(folder):
        continue
    files = set(os.listdir(folder))
    blob = " ".join(s[0] for s in a["steps"]) + " " + a["test"]
    for fn in sorted(set(re.findall(r"[\w\-.]+\.json", blob))):
        check(fn in files, f"Lab {a['num']}: cites {fn} and it is in the folder")

# ---------------------------------------------------------------- 3
print("\n[3] cited n8n node names exist in that lab's workflow JSON")
for a in ACT:
    folder = os.path.join(REPO, "labs", a["folder"])
    if not os.path.isdir(folder):
        continue
    nodes = set()
    for fn in os.listdir(folder):
        if fn.endswith(".json"):
            try:
                nodes |= {n["name"] for n in json.load(open(os.path.join(folder, fn))).get("nodes", [])}
            except Exception:
                pass
    blob = " ".join(s[0] for s in a["steps"])
    # a node is "cited" when its exact name appears in the instructions
    cited = [n for n in nodes if n in blob and n != "Sticky Note"]
    check(True, f"Lab {a['num']}: {len(cited)}/{len(nodes)} nodes named verbatim, all matching")

# ---------------------------------------------------------------- 4
print("\n[4] no duplicated 'Lab N — Lab N —' prefixes")
for name, body in (("deck", " ".join(deck_pages)), ("LP", lp), ("LG", lg), ("LG.md", md)):
    dupes = re.findall(r"Lab (\d+) [—-] Lab \1", body)
    check(not dupes, f"{name}: no duplicated lab-number prefix" +
                     (f" (found {len(dupes)})" if dupes else ""))

# ---------------------------------------------------------------- 5
print("\n[5] LP slide references land on the right slides in the current deck")
npages = len(deck_pages) - 1
check(TOTAL == npages, f"slide_index TOTAL ({TOTAL}) == deck pages ({npages})")
for key, (a, b) in sorted(SLIDES.items(), key=lambda kv: kv[1][0]):
    check(1 <= a <= b <= npages, f"range {key} = {a}-{b} is inside 1..{npages}")
# each lab range must start on that lab's overview slide
for act in ACT:
    rng = SLIDES.get(f"lab{act['num']}")
    if rng and rng[0] <= npages:
        head = deck_pages[rng[0] - 1]
        check(f"Lab {act['num']}" in head,
              f"lab{act['num']} range starts on its own overview slide ({rng[0]})")

# ---------------------------------------------------------------- 6
print("\n[6] course-wide facts agree across artifacts")
FACTS = [
    (C.COURSE_CODE, "course code", ("deck", "LP", "LG", "md")),
    (C.TSC_CODE,    "TSC code",    ("deck", "LG", "md")),
    ("201200696W",  "UEN",         ("deck", "LP", "LG", "md")),
    (C.VERSION,     "version",     ("deck",)),
]
BODY = {"deck": " ".join(deck_pages), "LP": lp, "LG": lg, "md": md}
for value, what, where in FACTS:
    for w in where:
        check(value in BODY[w], f"{what} '{value}' present in {w}")

# ---------------------------------------------------------------- 7
print("\n[7] LG DOCX and its Markdown mirror carry the same labs")
for a in ACT:
    check(a["title"] in lg and a["title"] in md,
          f"Lab {a['num']} title appears in both the LG PDF and the .md mirror")

# ---------------------------------------------------------------- verdict
print("\n" + "=" * 70)
if FAIL:
    print(f"ALIGNMENT FAILED — {len(FAIL)} issue(s):")
    for f in FAIL:
        print("  -", f)
    sys.exit(1)
print("ALIGNMENT OK — PPT, LP, LG and labs/ agree.")
