# Agentic AI for Business Process Automation

**WSQ Course Code:** TGS-2024045801
**TSC:** Artificial Intelligence Application · AER-TEM-3026-1.1
**Duration:** 2 days · 14 instructional hours
**Conducted by:** Tertiary Infotech Academy Pte Ltd (UEN 201200696W)

**Register:** [tertiarycourses.com.sg](https://www.tertiarycourses.com.sg/wsq-agentic-ai-for-business-process-automation.html) ·
[MySkillsFuture course directory](https://www.myskillsfuture.gov.sg/content/portal/en/training-exchange/course-directory/course-detail.html?courseReferenceNumber=TGS-2024045801)

Learners build five working automations in [n8n](https://n8n.io): a form-triggered workflow, a
webhook-triggered AI agent behind a real website, an agentic chatbot bound by compliance rules, a
human-in-the-loop approval chain, and a Retrieval-Augmented Generation chatbot grounded in an
organisation's own documents.

## Learning outcomes

- **LO1** — Explain what n8n and AI agents are, and build automated workflows using triggers and actions.
- **LO2** — Implement AI agent applications that are triggered by webhooks and integrated with business systems.
- **LO3** — Design agentic chatbot workflows that operate safely within business and regulatory constraints.
- **LO4** — Apply human-in-the-loop approval so that sensitive actions are authorised by a person.
- **LO5** — Deploy Retrieval-Augmented Generation (RAG) to ground an agent in an organisation's own documents.

## Course structure

| Topic | Content | Labs |
|---|---|---|
| 1 — Overview of n8n and AI Agents | What n8n is, triggers and actions, what an AI agent is, webhooks | Lab 1, Lab 2 |
| 2 — Agentic Chatbot and Human in the Loop | Agentic workflows, safe chatbot design, approval gates, accountability | Lab 3, Lab 4 |
| 3 — Retrieval-Augmented Generation (RAG) | Tokenization, embeddings, vector stores, chunking, grounding | Lab 5 |

## Labs

| # | Lab | Scenario | Folder |
|---|---|---|---|
| 1 | n8n Trigger and Action | Event flyer with a QR code — Form Trigger → Gmail | [`labs/lab1-trigger-actions/`](labs/lab1-trigger-actions/) |
| 2 | Webhook and AI Agent | Marina Trust Bank onboarding — website → webhook → agent with tools | [`labs/lab2-webhook-agent/`](labs/lab2-webhook-agent/) |
| 3 | Chatbot Webhook | Investment advisor — an agentic chatbot that refuses to give advice | [`labs/lab3-chatbot-webhook/`](labs/lab3-chatbot-webhook/) |
| 4 | Human in the Loop | Meridian Asset Management — the agent drafts, a human approves | [`labs/lab4-human-in-the-loop/`](labs/lab4-human-in-the-loop/) |
| 5 | RAG Customer Care Chatbot | Cook & Bake Academy — 20 brochures in a vector store | [`labs/lab5-rag/`](labs/lab5-rag/) |

## Courseware

Current version **v1.2** — all artifacts live in [`courseware/`](courseware/); superseded versions are
moved to `courseware/archive/`.

| Artifact | File |
|---|---|
| Trainer slide deck | `courseware/Agentic AI for Business Process Automation-v1.2.pptx` (+ `.pdf`) |
| Lesson Plan | `courseware/LP-Agentic AI for Business Process Automation.docx` (+ `.pdf`) |
| Learner Guide | `courseware/LG-Agentic AI for Business Process Automation.docx` (+ `.pdf`) |
| Learner Guide (Markdown mirror) | `courseware/LG-Agentic AI for Business Process Automation.md` |

## Building the courseware

All artifacts are generated from a single source — `course_data.py` plus `data_domain1..3.py` — so the
deck, Lesson Plan and Learner Guide can never drift apart.

```bash
bash .claude/skills/courseware-build/build/build_courseware.sh
```

The build asserts that the Lesson Plan's slide references match the deck it just produced, and that
each day totals the stated instructional hours. It fails loudly if either is untrue.

## Assessment

Written Assessment (SAQ, 1 hour) covering the Knowledge statements, and a Practical Performance
(1 hour) covering the Ability statements. Both are open book.

> Assessment material is confidential. It is distributed via Google Drive only and is **never**
> committed to this repository.

## Repository layout

```
courseware/          the current build — deck, LP, LG (+ PDFs) and the LG Markdown mirror
courseware/assets/   diagrams and screenshots placed on the slides
courseware/archive/  superseded versions (kept locally, not tracked in git)
labs/                the five hands-on labs — workflow JSON, websites and sample data
.claude/skills/      the single-source build pipeline and the WSQ generators
```

Two folders are deliberately **not** in this repository:

- `assessment/` — confidential question papers and answer keys; Google Drive only.
- `reference/` — the source decks this courseware was derived from; third-party material.

---

© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved. · [www.tertiarycourses.com.sg](https://www.tertiarycourses.com.sg)
