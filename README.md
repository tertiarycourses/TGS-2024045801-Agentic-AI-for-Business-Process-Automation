# Agentic AI for Business Process Automation

A 2-day WSQ course in building reliable, workflow-first agentic automation with n8n — from triggers and AI agents to human-in-the-loop approval and RAG.

| Course detail | Information |
|---|---|
| Course code | `TGS-2024045801` |
| Programme | WSQ |
| TSC | Artificial Intelligence Application · AER-TEM-3026-1.1 |
| Duration | 2 days · 16 instructional hours (9:30am–6:30pm, 8 hours/day) |
| Registration | [View course details and register](https://www.tertiarycourses.com.sg/wsq-agentic-ai-for-business-process-automation.html) · [MySkillsFuture course directory](https://www.myskillsfuture.gov.sg/content/portal/en/training-exchange/course-directory/course-detail.html?courseReferenceNumber=TGS-2024045801) |
| Funding | Up to 70% WSQ course fee funding — 50% baseline for Singapore Citizens/PRs aged 21+, up to 70% for Singapore Citizens aged 40+ (MCES) and SME-sponsored employees. Eligibility and terms apply — see the course page. |
| Provider | Tertiary Infotech Academy Pte Ltd (UEN 201200696W) |

## About the course

Learners build five working automations in [n8n](https://n8n.io): a form-triggered workflow, a
webhook-triggered AI agent behind a real website, an agentic chatbot bound by compliance rules, a
human-in-the-loop approval chain, and a Retrieval-Augmented Generation chatbot grounded in an
organisation's own documents. The course takes the modern, workflow-first view: AI coding agents
such as Claude Code and Codex help build the workflow, and a deterministic, auditable workflow runs
the process — with AI only at the steps that need judgement.

## Learning outcomes

- **LO1** — Explain what n8n and AI agents are, and build automated workflows using triggers and actions.
- **LO2** — Implement AI agent applications that are triggered by webhooks and integrated with business systems.
- **LO3** — Design agentic chatbot workflows that operate safely within business and regulatory constraints.
- **LO4** — Apply human-in-the-loop approval so that sensitive actions are authorised by a person.
- **LO5** — Deploy Retrieval-Augmented Generation (RAG) to ground an agent in an organisation's own documents.

## Topics covered

| Topic | Content | Labs |
|---|---|---|
| 1 — Overview of n8n and AI Agents | A brief history of AI 2023–2026, generative vs agentic AI, agentic AI vs AI agents, workflow first vs agent first, AI-assisted workflow creation and platform tiers, business value, the 5 principles of AI security, what n8n is, signing in, an n8n Assistant demo; n8n fundamentals → Lab 1; the AI agent building blocks (AI agent, model, tools and MCP, instructions, memory) and webhooks → Lab 2 | Lab 1, Lab 2 |
| 2 — Agentic Chatbot and Human in the Loop | Agentic workflows, safe chatbot design and a Telegram HR chatbot demo → Lab 3; human in the loop, approval gates and guardrails → Lab 4 | Lab 3, Lab 4 |
| 3 — Retrieval-Augmented Generation (RAG) | Tokenization, embeddings, vector stores, chunking, grounding | Lab 5 |

## Labs

| # | Lab | Scenario | Folder |
|---|---|---|---|
| 1 | n8n Trigger and Action | Event flyer with a QR code — Form Trigger → Gmail | [`labs/lab1-trigger-actions/`](labs/lab1-trigger-actions/) |
| 2 | Webhook and AI Agent | Marina Trust Bank onboarding — website → webhook → agent with tools | [`labs/lab2-webhook-agent/`](labs/lab2-webhook-agent/) |
| 3 | Chatbot Webhook | Investment advisor — an agentic chatbot that refuses to give advice | [`labs/lab3-chatbot-webhook/`](labs/lab3-chatbot-webhook/) |
| 4 | Human in the Loop | Meridian Asset Management — the agent drafts, a human approves | [`labs/lab4-human-in-the-loop/`](labs/lab4-human-in-the-loop/) |
| 5 | RAG Customer Care Chatbot | Cook & Bake Academy — 20 brochures in a vector store | [`labs/lab5-rag/`](labs/lab5-rag/) |

## Courseware (public package)

Current version **v2.3** — all artifacts live in [`courseware/`](courseware/); superseded versions are
moved to `courseware/archive/`.

| Artifact | File |
|---|---|
| Trainer slide deck | `courseware/Agentic AI for Business Process Automation-v2.3.pptx` (+ `.pdf`) |
| Lesson Plan | `courseware/LP-Agentic AI for Business Process Automation.docx` (+ `.pdf`) |
| Learner Guide | `courseware/LG-Agentic AI for Business Process Automation.docx` (+ `.pdf`) |
| Learner Guide (Markdown mirror) | `courseware/LG-Agentic AI for Business Process Automation.md` |

## What goes on a slide, and what goes in the Learner Guide

The deck follows the house reference format: a kicker, a bold title, a one-line intro, then **one**
visual structure — a chevron flow strip, outlined concept cards, a two-panel comparison, or a data
table — closed by a takeaway band.

**The click-by-click lab steps are deliberately not on the slides.** Each lab gets a single visual
slide (workflow chevron + a rendered n8n canvas + a LAB band) — Labs 2 and 3 also get a screenshot of
the real n8n canvas with a card per part of the flow — and the full steps live only in the Learner Guide. Keep it that way when editing — a step-by-step slide belongs in the LG.

The lab canvas screenshots are **rendered from each lab's own workflow JSON** by `render_flows.py`,
so the picture on the slide is the canvas the learner imports and cannot drift out of date:

```bash
python3 .claude/skills/courseware-build/build/render_flows.py   # -> courseware/assets/canvas-lab*.png
```

## Building the courseware

All artifacts are generated from a single source — `course_data.py` (metadata, outcomes, schedule),
`concepts.py` (the teaching concepts, shared by the deck and the LG) and `data_domain1..3.py` (the
labs) — so the deck, Lesson Plan and Learner Guide can never drift apart.

```bash
bash .claude/skills/courseware-build/build/build_courseware.sh
```

The build fails loudly rather than shipping courseware that disagrees with itself. It asserts that:

- the Lesson Plan's slide references match the deck it just produced;
- each training day totals exactly 480 instructional minutes — 9:30am–6:30pm less the 1-hour lunch,
  with the tea breaks counted within, which is the only reading that makes 8 hours arithmetically
  possible on that day;
- no lab intro or canvas caption is too long for its one-line band, so nothing ships truncated
  mid-sentence;
- and — via `check_alignment.py` — that the PPT, LP, LG and `labs/` all agree:
  every cited workflow file and n8n node name exists in the lab's JSON, no lab number is
  duplicated, every LP slide range starts on the slide it claims, and the course code, TSC,
  UEN and version read the same in all four artifacts.

Run the alignment test on its own with:

```bash
python3 .claude/skills/courseware-build/build/check_alignment.py
```

## Assessment

Written Assessment (SAQ, 1 hour) covering the Knowledge statements, and a Practical Performance
(1 hour) covering the Ability statements. Both are open book.

> Assessment material is confidential. It is distributed via Google Drive only and is **never**
> committed to this repository.

## Repository layout

```
courseware/          the current build — deck, LP, LG (+ PDFs) and the LG Markdown mirror
courseware/assets/   slide diagrams, n8n UI screenshots, and the generated canvas-lab*.png
courseware/archive/  superseded versions (kept locally, not tracked in git)
labs/                the five hands-on labs — workflow JSON, websites and sample data
.claude/skills/      the single-source build pipeline and the WSQ generators
```

The build modules under `.claude/skills/courseware-build/build/`:

| File | Role |
|---|---|
| `course_data.py` | Metadata, learning outcomes, topics, daily timing — the single source for all four artifacts |
| `concepts.py` | The teaching concepts, rendered as visual slides AND as Learner Guide sections |
| `data_domain1..3.py` | Per-topic lab content: steps, canvas screenshots, chevron flows, takeaways |
| `build_slides.py` | The deck engine and its visual component library |
| `build_lesson_plan.py` | The Lesson Plan, including the 8-hour-per-day assertion |
| `build_learner_guide.py` | The Learner Guide DOCX + its Markdown mirror |
| `render_flows.py` | Renders each lab's n8n canvas from the lab's own workflow JSON |
| `check_alignment.py` | Cross-artifact alignment test run by the build |

Two folders are deliberately **not** in this repository:

- `assessment/` — confidential question papers and answer keys; Google Drive only.
- `reference/` — the source decks this courseware was derived from; third-party material.

---

© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · [www.tertiarycourses.com.sg](https://www.tertiarycourses.com.sg)
