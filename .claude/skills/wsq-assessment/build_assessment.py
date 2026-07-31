#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the WSQ assessment set for 'Application Integration with Docker and Kubernetes' (TGS-2021010366):
  - Written Assessment (SAQ)  — 5 open-ended KNOWLEDGE questions (K1–K5), aligned to the slides
  - Practical Performance (PP) — 4 PRACTICAL tasks (LO1–LO4), aligned to the in-class activities
Each instrument is produced as a Question Paper and a matching Answer Key (4 DOCX total),
all with the WSQ house cover page (same as the Lesson Plan / Learner Guide). Page 1 is the cover;
page 2 carries Trainee Information + Instructions + Grading; the questions/tasks begin on page 3.
Body: Arial 11.
"""
import os, sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# This script lives in the wsq-assessment skill (.claude/skills/wsq-assessment/) and runs in
# place — it detects the course repo root by walking up to the nearest dir that has a .git
# folder (or both courseware/ and assessment/). Override with env REPO=/path if needed.
def _find_repo():
    env = os.environ.get("REPO")
    if env and os.path.isdir(env):
        return os.path.abspath(env)
    d = os.path.dirname(os.path.abspath(__file__))
    while d != os.path.dirname(d):
        if os.path.isdir(os.path.join(d, ".git")) or \
           (os.path.isdir(os.path.join(d, "courseware")) and os.path.isdir(os.path.join(d, "assessment"))):
            return d
        d = os.path.dirname(d)
    return os.getcwd()

REPO = _find_repo()
# prodoc.py (WSQ cover page + version control + page numbers, same as LP/LG) ships with the
# tertiary-lesson-plan skill. Look for it at the project level first, then the user level.
for _cand in (os.path.join(REPO, ".claude/skills/tertiary-lesson-plan"),
              os.path.expanduser("~/.claude/skills/tertiary-lesson-plan")):
    if os.path.exists(os.path.join(_cand, "prodoc.py")):
        sys.path.insert(0, _cand); break
import prodoc  # cover page + version control + page numbers (same as LP/LG)

# ─── EDIT PER COURSE ────────────────────────────────────────────────────────
TITLE       = "Agentic AI for Business Process Automation"
COURSE_CODE = "TGS-2024045801"
# ────────────────────────────────────────────────────────────────────────────
# The cover page renders prodoc's module-level TGS constant. Override it so the
# assessment cover shows THIS course's ref (works with either prodoc version —
# the older project prodoc has no course_code kwarg).
prodoc.TGS = f"TGS Ref No: {COURSE_CODE}"
OUT   = os.path.join(REPO, "assessment")

# Logos: prefer the course's own courseware/assets, else fall back to the copies bundled
# in this skill (so the assessment builds even outside this project). Replace the course
# logo per course; the Tertiary Infotech logo is the same for every WSQ course.
def _logo(name):
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(REPO, "courseware/assets", name), os.path.join(here, "assets", name)):
        if os.path.exists(p):
            return p
    return None
ORG_LOGO    = _logo("tertiary-infotech-logo.png")
COURSE_LOGO = _logo("n8n-logo.png")   # None if absent → Tertiary-only cover (as LP/LG)

Q_VER, A_VER = "v1", "v1"   # single standardised version across all four files
BRAND = RGBColor(0x1F, 0x6F, 0xEB); DARK = RGBColor(0x11, 0x18, 0x27); GREY = RGBColor(0x55, 0x5B, 0x66)
# Assessments carry the cover page only — no Document Version Control Record.

# ---------------------------------------------------------------- WRITTEN (KNOWLEDGE) — K1..K8
WRITTEN = [
 ("K1",
  "A business team is investigating how agentic AI could be introduced into their workflows to boost "
  "productivity and take over routine tasks. Before choosing a tool they want to be clear about what "
  "\"agentic\" actually adds over the generative AI they already use.",
  "Explain what agentic AI is, and describe how it differs from generative AI. In your answer, refer to how "
  "each one behaves when given a task.",
  ["Generative AI creates content — text, images or code — in response to a prompt. It answers once and then "
   "stops, and it relies on the user to supply the context and the goal.",
   "Agentic AI is given a GOAL rather than a prompt. It uses the reasoning power of a large language model to "
   "break a complex task into simpler ones.",
   "An agent runs a loop: it observes the situation, chooses an action, acts on the world through a TOOL, "
   "observes the result, and repeats until the goal is met.",
   "An agent therefore takes actions and reaches real systems (a spreadsheet, an inbox, an API); a generative "
   "model only produces an answer for a human to act on.",
   "Example contrast: generative AI = \"draft me an email\"; agentic AI = \"read the enquiry, check the CRM, "
   "reply to the customer and log the decision\".",
   "(Slides: The Evolution of AI · Agentic AI is AI that does the work · How an AI Agent Works · "
   "Agentic AI vs Generative AI)"]),

 ("K2",
  "A logistics company wants to automate the handling of delivery-exception emails. Their analyst has been "
  "told that n8n workflows are built from nodes, and that the first node is special.",
  "Describe how an n8n workflow is structured. In your answer explain what a trigger is, what an action is, "
  "and how data passes from one node to the next.",
  ["An n8n workflow is a set of NODES wired together on a visual canvas; data flows along the connections from "
   "one node to the next.",
   "A TRIGGER is the first node and decides WHEN the workflow runs — for example a Form Trigger, a Webhook, a "
   "Schedule, a Chat Trigger or a Manual trigger.",
   "An ACTION decides WHAT the workflow does — send a Gmail message, append a Google Sheets row, call an HTTP "
   "API, or write to a database.",
   "Logic nodes (IF, Switch, Merge, Split Out, Code, Edit Fields) control the flow between them; AI nodes "
   "(AI Agent, Chat Model, Memory, Embeddings, Vector Store, Tools) add reasoning.",
   "Data travels as a list of ITEMS, each a JSON object of key/value pairs. Each node reads the previous "
   "node's output and adds to it.",
   "A later node reads an earlier value with an EXPRESSION, e.g. {{ $json.Name }}. Expressions work in any "
   "field — subject lines, URLs, conditions and message bodies. The field must be in Expression mode, not "
   "Fixed mode, or n8n prints the braces literally.",
   "(Slides: The Building Blocks — n8n Nodes · Triggers and Actions · Data, JSON and Expressions. Lab 1.)"]),

 ("K3",
  "A bank is about to put an AI agent in front of customers. The compliance officer asks to see \"the thing "
  "that controls what it will and will not say\" before approving the launch.",
  "Explain what a system instruction is and why it matters. Provide one example of a system instruction you "
  "would write for a customer-service agent, and state four rules a good system instruction should contain.",
  ["A system instruction defines the agent's ROLE, SCOPE, PROHIBITIONS and ROUTING RULES. It is the main "
   "control surface for the agent's behaviour — in a regulated setting it is a compliance control, not "
   "prompt-engineering polish.",
   "Example: \"You are the customer-service assistant for Marina Trust Bank. Answer only questions about "
   "account opening, branch locations and opening hours. Use the customer_lookup tool for any question about "
   "an existing account. Never give financial or investment advice, and never state a fee that the tool did "
   "not return. If you do not know, say so and offer to connect the customer to a human.\"",
   "Rule 1 — State the role plainly, and narrowly. A chatbot for one job refuses far more reliably than a "
   "general assistant.",
   "Rule 2 — Give the scope and the limits: what it must answer, and what it must refuse.",
   "Rule 3 — Say which tool to use for which kind of question, explicitly.",
   "Rule 4 — Tell it to say \"I don't know\" rather than invent an answer; and ask for a specific output "
   "format when something downstream depends on it.",
   "Then test it with real questions — including the ones you most fear being asked — and refine.",
   "(Slides: The Four Parts of an n8n AI Agent · Writing a Good System Instruction · Designing a Safe Agentic "
   "Chatbot. Labs 2, 3, 4.)"]),

 ("K4",
  "An insurer runs two automations. The first routes claim forms by claim type using fixed rules. The second "
  "reads free-text complaint emails and decides how to handle each one. The team is debating whether both "
  "should be built the same way.",
  "Compare a rule-based (RPA) workflow with an agentic workflow. Explain the strengths and weaknesses of each, "
  "and state which of the two automations above suits which approach, and why.",
  ["A RULE-BASED (RPA) workflow has every branch wired by hand — IF/Switch on exact values. It is predictable, "
   "easy to audit and cheap to run, but it breaks on anything the designer did not foresee.",
   "An AGENTIC workflow is one where the LLM makes the routing decisions. It understands free text and intent "
   "and handles cases nobody anticipated, but it needs guardrails, logging and testing.",
   "In an agentic workflow you still design the process, the guardrails and the tools; what you hand over is "
   "the JUDGEMENT about which path a particular case should take.",
   "Claim forms by claim type → rule-based. The input is structured, the rules are fixed and high-volume, and "
   "determinism is worth more than flexibility.",
   "Free-text complaint emails → agentic. The input is language, the cases vary, and no fixed branch could "
   "cover them.",
   "This is the shift from Robotic Process Automation (RPA), which constructs the workflow manually and only "
   "handles rigid tasks, to Agentic Process Automation (APA), where an agent orchestrates the workflow and "
   "handles rigid and flexible tasks alike.",
   "(Slides: What is an Agentic Workflow · Rule-Based Workflow vs Agentic Workflow · From RPA to Agentic "
   "Process Automation)"]),

 ("K5",
  "A retailer's website needs a chat widget that reaches an AI agent running in n8n. The developer asks how "
  "the browser is supposed to start a workflow that lives on another server.",
  "Explain what a webhook is and how it differs from an HTTP Request node. In your answer describe the "
  "difference between the Test URL and the Production URL, and state two settings you must configure before a "
  "public website can use the webhook.",
  ["A WEBHOOK is a URL that any external system can send data to (usually an HTTP POST). It starts your "
   "workflow when it is called — the website, an app, a payment provider or another workflow.",
   "It is the OPPOSITE direction from an HTTP Request node: with an HTTP Request node YOUR workflow calls the "
   "outside world; with a Webhook the outside world calls YOU.",
   "The TEST URL (/webhook-test/…) works only while you have clicked \"Listen for test event\", and accepts "
   "exactly ONE request. It shows the incoming data live on the canvas while you build.",
   "The PRODUCTION URL (/webhook/…) works only while the workflow is ACTIVE, and accepts unlimited requests. "
   "Switch to it the moment anyone but you needs the page to work. A QR code or website pointing at a Test URL "
   "works exactly once and then returns 404.",
   "Setting 1 — Allowed Origins (CORS). Without it the n8n execution succeeds but the browser refuses to read "
   "the reply (the classic \"Failed to fetch\"). '*' is acceptable in class, never in production.",
   "Setting 2 — Authentication (None / Basic Auth / Header Auth / JWT). An open webhook can be called by "
   "anyone who learns the URL, and every call costs you an LLM invocation.",
   "Also relevant: the HTTP method (GET carries data in the query string; POST carries a JSON body, which is "
   "what a chat widget sends), and the Respond mode, so a \"Respond to Webhook\" node can return the agent's "
   "answer to the caller.",
   "(Slides: Webhooks — the Front Door to Your Agent · Test vs Production Execution. Labs 2, 3, 4, 5.)"]),

 ("K6",
  "A wealth-management firm wants an AI assistant to draft replies to worried clients. Compliance will not "
  "approve an agent that emails clients on its own, but the firm still wants the speed benefit.",
  "Explain what human-in-the-loop means and how it is implemented in an n8n workflow. State four situations in "
  "which you would insist on a human approval step, and explain what the workflow must record so that the "
  "process is auditable.",
  ["HUMAN-IN-THE-LOOP means some actions are too consequential to automate: the workflow PAUSES until a named "
   "person approves or declines. The agent may do everything except the one thing that matters — sending.",
   "In n8n this is the Gmail \"Send and Wait for Response\" node. It emails the approver with Approve and "
   "Decline buttons, and the execution genuinely pauses on the canvas until a button is clicked.",
   "An IF node then routes on the decision: the true branch performs the action; the false branch reassigns "
   "the case instead of discarding it.",
   "Situation 1 — Money moves: payments, refunds, credit decisions.",
   "Situation 2 — It is a regulated communication: a licensed firm writing to a client about their money, "
   "health or legal position.",
   "Situation 3 — The action is irreversible: sending an email, deleting a record, publishing content.",
   "Situation 4 — A person is vulnerable, or the stakes exceed the model's error rate. The question is never "
   "\"is the model good?\" but \"what does one bad output cost?\"",
   "For the audit trail, log what the agent PROPOSED separately from what a human AUTHORISED. Keeping them "
   "apart is what lets an auditor ask whether anyone ever sent something a human never saw.",
   "Every approved action carries the NAME of the approver; every declined one is reassigned to a NAMED "
   "person. No accountability column should ever be empty — a decline is a reassignment, not a deletion.",
   "(Slides: Human in the Loop · The Human-in-the-Loop Pattern · When to Put a Human in the Loop · Building "
   "the Audit Trail. Lab 4.)"]),

 ("K7",
  "A training academy's chatbot keeps quoting course fees that do not exist. The academy has 20 course "
  "brochures that contain every correct answer, and someone suggests simply pasting all of them into the "
  "agent's prompt.",
  "Explain what Retrieval-Augmented Generation (RAG) is and why it is preferable to pasting all the documents "
  "into the prompt. Describe the steps of the RAG pipeline, and explain the role of embeddings and chunking.",
  ["RAG (Retrieval-Augmented Generation) retrieves the few documents that RESEMBLE the question and gives the "
   "model only those, instead of everything. The model reads what matters rather than the whole corpus.",
   "Why not paste everything: for 20 short brochures it would work, but add 200 more and the prompt exceeds "
   "the model's context window; long prompts also degrade quality because models attend less well to the "
   "middle of a long context; and you pay for every token on every question whether it was relevant or not.",
   "Pipeline — INGESTION (run once): collect the source documents → split them into chunks → embed each chunk "
   "into a vector → store the vectors in a vector store.",
   "Pipeline — RETRIEVAL (every question): embed the question with the SAME model → retrieve the nearest "
   "chunks from the store → the LLM answers from what was retrieved.",
   "EMBEDDINGS: text is first split into tokens, then an embedding model turns a chunk into a vector — a list "
   "of numbers positioned so text about similar things lands close together. \"How much is the sourdough "
   "course?\" lands near the sourdough brochure and far from the sushi one, even though they share no words.",
   "CHUNKING is the single biggest lever on RAG quality. The right chunk is the smallest piece of text that "
   "still answers a question on its own. Too small and a brochure is sliced so the course name is separated "
   "from its fee — retrieval finds one without the other. Too large and irrelevant text crowds the prompt.",
   "In the lab, chunk size 4000 with overlap 0 makes one brochure exactly one vector, so the fee is never "
   "separated from the course it belongs to.",
   "A VECTOR STORE holds the embeddings and finds nearest neighbours fast. n8n's Simple Vector Store needs no "
   "setup but is wiped when n8n restarts; production uses Pinecone, Supabase (pgvector) or Qdrant.",
   "(Slides: What is RAG · Why Not Just Paste Everything · The RAG Pipeline · Chunking — the Biggest Lever · "
   "Choosing a Vector Store. Lab 5.)"]),

 ("K8",
  "You are deploying the academy's RAG chatbot. During testing it answers \"I don't have that in our course "
  "information\" to every question, and on another occasion invents an instructor's name. Both must be fixed "
  "before go-live.",
  "Describe the procedure for deploying a RAG application in n8n, and explain how you would diagnose these two "
  "failures. State the instructions you would give the agent to keep its answers grounded.",
  ["Deployment procedure — INGESTION: put the source documents in a Drive folder; import the ingestion "
   "workflow; point it at your folder; set the memory key / index name; configure the splitter (chunk size and "
   "overlap); select the embeddings credential; turn Clear Store ON so re-running replaces rather than "
   "duplicates; then run it once.",
   "Deployment procedure — ANSWERING: import the agent workflow; point the retrieval tool at the SAME memory "
   "key / index; select the SAME embeddings model; write the grounding instructions; set the webhook path and "
   "CORS; activate and copy the Production URL into the website.",
   "Diagnosing \"I don't have that\" for everything: the memory key on the retrieval tool does not match the "
   "one used at ingestion, so the agent is searching an empty store. This is the most common failure and it "
   "raises no error anywhere. Other causes: the ingestion workflow was never run, or n8n restarted and wiped "
   "the in-memory store.",
   "Diagnosing an invented instructor name: the agent did not call the retrieval tool, or called it and "
   "ignored the result. Check the execution log to confirm the tool actually ran. Fix the INSTRUCTION, not the "
   "documents — then ask what else it might invent that you have not thought to test.",
   "Also verify the ingestion and retrieval embedding models are IDENTICAL — a question embedded by one model "
   "cannot be compared against documents embedded by another; the comparison silently returns nonsense. And "
   "the store's dimension must match the model's output (gemini-embedding-001 = 3072).",
   "Grounding instructions: always call the tool before answering any factual question; base every factual "
   "claim on what the tool returned; say \"I don't have that in our course information\" when the documents "
   "are silent; never invent a fee, a date, a duration, a course code, an instructor name or a discount; and "
   "never mention the vector store or that you are searching documents.",
   "Test with deliberate traps: ask about a course that does not exist, a person no document names, and a "
   "discount never offered. Any confident answer is a failure, however fluent.",
   "(Slides: The Rules That Keep RAG Working · Grounding an Agent Against Hallucination. Lab 5, including the "
   "TC7–TC9 hallucination probes.)"]),
]

# ---------------------------------------------------------------- PRACTICAL (ACTIVITY-BASED) — A1..A3
SCENARIO = (
 "Meridian Business Services is a Singapore firm that runs events, handles customer enquiries through its "
 "website, and answers the same questions about its training courses all day long. Repetitive administrative "
 "work is slowing the team down and replies to customers take too long.\n\n"
 "You have been engaged to automate three of their processes with n8n. You will build a workflow that captures "
 "event sign-ups, deploy an AI agent behind their public website with a human approval step so that nothing "
 "reaches a customer unchecked, and stand up a Retrieval-Augmented Generation chatbot grounded in the firm's "
 "own course documents.\n\n"
 "Complete the three tasks below. Each mirrors a hands-on lab you built in class. For every task, paste a "
 "screenshot of your working n8n canvas and of the result (the email received, the approval message, or the "
 "chatbot's answer) as evidence.")

BOX_CAP = "Paste your n8n workflow screenshot and the result screenshot in the box below"

PRACTICAL = [
 ("Task 1", "A2",
  "Deploy an automated workflow according to plan (trigger and action). Meridian runs an evening networking "
  "event and needs sign-ups collected without anyone re-typing them. "
  "Part A — Build an n8n workflow with an n8n Form Trigger titled \"Meridian Event Signup\", carrying four "
  "fields: Name (Text), Email (Email), Phone (Number) and Message (Textarea), with Name and Email marked as "
  "required. "
  "Part B — Add a Gmail node using the \"Send a message\" operation. Set To to the event administrator's "
  "address and Subject to \"New Enquiry\", and build the message body from the submitted fields using "
  "expressions so the email shows the sign-up's name, email, phone and message. "
  "Part C — Save the workflow, set it Active, copy the Form's PRODUCTION URL, and generate a QR code for that "
  "URL that could be printed on the event flyer. State why the Production URL must be used here rather than "
  "the Test URL. "
  "Evidence: the canvas, the received email, and the QR code. (Lab 1 — n8n Trigger and Action.)",
  BOX_CAP,
  "Part A — Form Trigger:\n"
  "  • Workflows → Add workflow; add an 'n8n Form Trigger' node.\n"
  "  • Form Title: Meridian Event Signup (plus a short description).\n"
  "  • Add fields: Name (Text, required), Email (Email, required), Phone (Number), Message (Textarea).\n"
  "  • The field NAMES become the JSON keys the next node reads.\n\n"
  "Part B — Gmail action:\n"
  "  • Add a Gmail node after the trigger; operation = 'Send a message'.\n"
  "  • Connect the Gmail credential (OAuth2) via 'Sign in with Google'.\n"
  "  • To = the administrator's address; Subject = New Enquiry.\n"
  "  • Switch the Message field to EXPRESSION mode (not Fixed) and build the body, e.g.:\n"
  "      Name: {{ $json.Name }}\n"
  "      Email: {{ $json.Email }}\n"
  "      Tel: {{ $json.Phone }}\n"
  "      Message: {{ $json.Message }}\n"
  "  • In Fixed mode n8n prints the braces literally — this is the usual reason the email shows\n"
  "    {{ $json.Name }} instead of a value.\n\n"
  "Part C — Publish:\n"
  "  • Execute workflow, submit a test entry, confirm the email arrives.\n"
  "  • Save and toggle the workflow ACTIVE; copy the Form's Production URL.\n"
  "  • Paste it into a QR generator (e.g. alfredang.github.io/qrcodegenerator) and download the PNG.\n"
  "  • WHY the Production URL: the Test URL only answers while 'Listen for test event' is armed and\n"
  "    accepts exactly ONE request. A QR code encoding a Test URL scans perfectly and works once,\n"
  "    then returns 404 for everyone else. The Production URL works whenever the workflow is Active.\n\n"
  "Acceptable evidence: canvas showing Form Trigger → Gmail; the received email with real values;\n"
  "the QR code image."),

 ("Task 2", "A1",
  "Implement an AI agent application, in collaboration with the service provider's platform, with human "
  "oversight. Meridian wants an AI assistant to answer customer messages from its website — but the manager "
  "must approve every reply before a customer sees it. "
  "Part A — Build a workflow starting with a Webhook node (method POST, a named path, Allowed Origins set so a "
  "browser page may read the reply, and Respond set to use a 'Respond to Webhook' node). "
  "Part B — Add an AI Agent with a chat model attached. Write a system instruction that defines its role for "
  "Meridian, states its scope, and lists at least three explicit prohibitions. Configure it to return a "
  "structured output containing at least a draft reply and a priority or category field, and explain why "
  "structured output is used instead of prose. "
  "Part C — Add the human approval step: acknowledge the customer immediately, log the agent's draft, then use "
  "Gmail \"Send and Wait for Response\" to email the manager with Approve/Decline buttons. Add an IF node so "
  "that Approve sends the reply and logs it, while Decline sends nothing to the customer and instead reassigns "
  "the case to a named person. "
  "Evidence: the canvas, the approval email, and proof that a declined case sent nothing to the customer. "
  "(Labs 2, 3 and 4 — Webhook and AI Agent · Chatbot Webhook · Human in the Loop.)",
  BOX_CAP,
  "Part A — Webhook front door:\n"
  "  • Add a Webhook node. HTTP Method = POST; Path = e.g. meridian-customer-query.\n"
  "  • Respond = 'Using Respond to Webhook Node' so the agent's answer can be returned to the caller.\n"
  "  • Options → Allowed Origins (CORS) = * so the browser page is permitted to read the reply.\n"
  "    Without CORS the n8n execution succeeds but the browser reports 'Failed to fetch'.\n"
  "  • Use the Test URL with 'Listen for test event' while building; switch to the Production URL\n"
  "    (workflow Active) once the website must work for anyone else.\n"
  "  • Add a Set/Code node to normalise the incoming fields from $json.body.\n\n"
  "Part B — The agent:\n"
  "  • Add an AI Agent node; attach a Chat Model (Google Gemini or OpenAI) credential.\n"
  "  • System instruction must state the ROLE, the SCOPE and the PROHIBITIONS, e.g.:\n"
  "      'You are the customer-care assistant for Meridian Business Services. Answer only questions\n"
  "       about our events, courses and opening hours. Never quote a price that was not supplied to\n"
  "       you. Never promise a delivery date. Never give financial, legal or medical advice. If you\n"
  "       do not know, say so and offer to have a colleague follow up.'\n"
  "  • Attach a Structured Output Parser requiring named fields, e.g. draftReply, category, urgency.\n"
  "  • WHY structured output: prose cannot be branched on, sorted, logged into columns or coloured.\n"
  "    A named field lets the IF node route, the Sheets node log, and the page render the result.\n"
  "    Enumerate the allowed values (e.g. urgency = Low/Medium/High) so the field stays reliable.\n\n"
  "Part C — The human gate:\n"
  "  • Respond to Webhook immediately with a small acknowledgement (a reference and a status) so the\n"
  "    customer is not left waiting — do NOT return the internal classification fields.\n"
  "  • Google Sheets → append the agent's draft to a 'Drafts' tab BEFORE any human sees it.\n"
  "  • Gmail → 'Send and Wait for Response' addressed to the manager, approval type Approve/Decline,\n"
  "    body carrying the customer's own words and the drafted reply. The execution now PAUSES on the\n"
  "    canvas until a person clicks.\n"
  "  • IF node on the approval result:\n"
  "      true  → Gmail send the approved reply to the customer; append to 'Approved_Replies' with the\n"
  "              approver's NAME.\n"
  "      false → send NOTHING to the customer; append to a 'Handover_Queue' tab stamped with a named\n"
  "              assignee, and email that person to follow up.\n"
  "  • A decline is a REASSIGNMENT, not a deletion — someone must still owe the customer an answer,\n"
  "    and no accountability column may be left empty.\n\n"
  "Acceptable evidence: canvas showing Webhook → Agent → Acknowledge → Log → Send-and-Wait → IF →\n"
  "both branches; the approval email with both buttons; the Drafts/Approved/Handover rows; and proof\n"
  "that the declined case produced no customer email."),

 ("Task 3", "A3",
  "Identify and report issues with an AI application and its data (RAG deployment and troubleshooting). "
  "Meridian's website chatbot must answer questions about their courses using ONLY the firm's own course "
  "documents, and must never invent a fee. "
  "Part A — Build the ingestion workflow: read the course documents from a Google Drive folder, split them so "
  "that one document becomes one chunk, embed them, and insert them into a vector store. State the chunk size "
  "and overlap you used and justify that choice, and explain why Clear Store must be ON when re-running. "
  "Part B — Build the answering workflow: a Webhook, an AI Agent with the vector store attached as a retrieval "
  "tool, and a Respond to Webhook node. Write the grounding instructions that stop it inventing answers. "
  "Part C — Test and REPORT. Run at least one question that the documents answer correctly, and at least two "
  "deliberate traps — a course the firm does not offer, and a detail no document contains (such as an "
  "instructor's name). Record what the chatbot answered in each case. Then state, for each of the following "
  "symptoms, the most likely cause and the fix: (i) every question returns \"I don't have that\"; (ii) the "
  "chatbot quotes a fee that appears in no document; (iii) every document is returned twice in the results. "
  "Evidence: both canvases, the chatbot's answers to your test questions, and your written issue report. "
  "(Lab 5 — RAG Customer Care Chatbot, including the TC7–TC9 hallucination probes.)",
  BOX_CAP,
  "Part A — Ingestion (run once):\n"
  "  • Manual Trigger → Google Drive 'List files in folder' (point at YOUR documents folder) →\n"
  "    Google Drive 'Download file' → Vector Store (Insert).\n"
  "  • Attach a Default Data Loader and a Recursive Character Text Splitter.\n"
  "  • Chunk size 4000, overlap 0 → one brochure/document becomes exactly ONE vector.\n"
  "    JUSTIFICATION: the right chunk is the smallest text that still answers a question on its own.\n"
  "    A document is ~2.7 KB, so 4000 does not split it. The default 1000-character splitter would\n"
  "    slice it into three, and the fragment naming the course would not be the fragment carrying the\n"
  "    fee — retrieval would find one without the other and the bot would say it doesn't know the price.\n"
  "  • Attach an Embeddings node (e.g. Google Gemini gemini-embedding-001 → 3072 dimensions).\n"
  "  • Set a UNIQUE memory key / index name (e.g. meridian_<your-name>) — on a shared instance the key\n"
  "    is a global namespace, and the default would mix your documents with everyone else's.\n"
  "  • Clear Store = ON: re-running then REPLACES the documents instead of storing them twice. With it\n"
  "    off, a second run duplicates every document and every search returns each one twice.\n"
  "  • Execute the workflow once and confirm the expected number of vectors was inserted.\n\n"
  "Part B — Answering (runs per question):\n"
  "  • Webhook (POST, path set, CORS allowed) → AI Agent → Respond to Webhook.\n"
  "  • Attach the Vector Store as a RETRIEVAL TOOL to the agent, with the SAME memory key as ingestion\n"
  "    and the SAME embeddings model. Low temperature (e.g. 0.1) — fees are not creative writing.\n"
  "  • Grounding instructions:\n"
  "      – Always call the retrieval tool before answering any factual question.\n"
  "      – Base every factual claim on what the tool returned.\n"
  "      – If the documents do not answer it, say 'I don't have that in our course information.'\n"
  "      – Never invent a fee, a date, a duration, a course code, an instructor name or a discount.\n"
  "      – Never mention the vector store or that you are searching documents.\n"
  "  • Activate, copy the Production URL, and set it in the website's script.\n\n"
  "Part C — Test results and issue report:\n"
  "  • Correct case: a question the documents answer → the bot quotes the document's exact figure.\n"
  "  • Trap 1 (a course not offered) → must say it is not offered, and may suggest the closest courses\n"
  "    that ARE offered. A confident description of the non-existent course is a FAILURE.\n"
  "  • Trap 2 (an instructor's name no document contains) → must say it is not in the course\n"
  "    information. Inventing a plausible name is a FAILURE — fix the INSTRUCTION, not the documents.\n"
  "  (i) Every question returns 'I don't have that':\n"
  "      CAUSE — the memory key / index name on the retrieval tool does not match the one used at\n"
  "      ingestion, so the agent is searching an empty store. This is the most common failure and it\n"
  "      raises no error anywhere. Also check the ingestion workflow actually ran, and whether n8n\n"
  "      restarted and wiped the in-memory store.\n"
  "      FIX — make the two keys identical; re-run ingestion; for production use a persistent vector\n"
  "      database (Pinecone / Supabase / Qdrant) instead of the in-memory store.\n"
  "  (ii) A fee that appears in no document:\n"
  "      CAUSE — the agent did not call the retrieval tool, or called it and ignored the result; the\n"
  "      grounding instruction is missing or too weak. Confirm in the execution log whether the tool\n"
  "      actually ran.\n"
  "      FIX — instruct it to always call the tool first, to answer only from what came back, and to\n"
  "      say 'I don't have that' otherwise; then re-test the traps.\n"
  "  (iii) Every document returned twice:\n"
  "      CAUSE — Clear Store was off and the ingestion workflow was run more than once, so each\n"
  "      document is stored twice.\n"
  "      FIX — turn Clear Store ON and re-run the ingestion once to replace the contents.\n"
  "  • Also verify the ingestion and retrieval EMBEDDING MODELS are identical — a question embedded by\n"
  "    one model cannot be compared against documents embedded by another; the comparison silently\n"
  "    returns nonsense rather than failing. The store's dimension must equal the model's output.\n\n"
  "Acceptable evidence: both canvases; the chatbot's answers to the correct question and both traps;\n"
  "and a written report naming a cause and a fix for each of the three symptoms."),
]

# ---------------------------------------------------------------- doc helpers
def base_doc():
    doc = Document()
    n = doc.styles["Normal"]; n.font.name = "Arial"; n.font.size = Pt(11)
    return doc

def para(doc, text, size=11, bold=False, italic=False, color=None, after=6, before=0, align=None):
    p = doc.add_paragraph(); r = p.add_run(text)
    r.font.size = Pt(size); r.bold = bold; r.italic = italic
    if color: r.font.color.rgb = color
    p.paragraph_format.space_after = Pt(after); p.paragraph_format.space_before = Pt(before)
    if align is not None: p.alignment = align
    return p

def heading(doc, text, size=13):
    para(doc, text, size=size, bold=True, color=BRAND, after=6, before=8)

def _wrap_mono(lines, width=68):
    """Hard-wrap monospace model-answer lines, preserving each line's own indent so
    continuations align under their parent bullet instead of falling to column 0."""
    import textwrap
    out = []
    for ln in lines:
        if len(ln) <= width:
            out.append(ln); continue
        indent = len(ln) - len(ln.lstrip(" "))
        # continuation lines indent two extra spaces past the parent's text start
        cont = " " * (indent + 2)
        wrapped = textwrap.wrap(
            ln.strip(), width=width - indent,
            initial_indent="", subsequent_indent="",
            break_long_words=False, break_on_hyphens=False) or [""]
        out.append(" " * indent + wrapped[0])
        out.extend(cont + w for w in wrapped[1:])
    return out

def answer_box(doc, lines=None, code=None, height_pt=90):
    """1x1 bordered box. `lines` → bullet-style model answer; `code` → monospace
    code/YAML/command block (indentation preserved); neither → empty answer space."""
    t = doc.add_table(rows=1, cols=1); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.rows[0].cells[0]
    cell.paragraphs[0].text = ""
    if code:
        run = cell.paragraphs[0].add_run("Suggestive answers (not exhaustive):")
        run.bold = True; run.font.size = Pt(10.5)
        # Consolas 9pt fits ~68 chars in the cell once the box padding is taken off. Hard-wrap longer lines here
        # so Word never soft-wraps a continuation back to column 0 (which destroys the
        # indentation) or splits a token mid-word.
        for ln in _wrap_mono(code.split("\n")):
            b = cell.add_paragraph(style=None)
            b.paragraph_format.space_after = Pt(0); b.paragraph_format.space_before = Pt(0)
            rr = b.add_run(ln if ln else " ")
            rr.font.name = "Consolas"; rr.font.size = Pt(9)
            rr._element.rPr.rFonts.set(qn('w:cs'), "Consolas")
            wt = rr._element.find(qn('w:t'))
            if wt is not None: wt.set(qn('xml:space'), 'preserve')
    elif lines:
        run = cell.paragraphs[0].add_run("Suggestive answers (not exhaustive):")
        run.bold = True; run.font.size = Pt(10.5)
        for ln in lines:
            b = cell.add_paragraph(style=None); b.paragraph_format.left_indent = Inches(0.15)
            rr = b.add_run("•  " + ln); rr.font.size = Pt(10.5)
    else:
        # empty answer space
        tr = t.rows[0]._tr
        trPr = tr.get_or_add_trPr(); trh = OxmlElement('w:trHeight')
        trh.set(qn('w:val'), str(int(height_pt*20))); trh.set(qn('w:hRule'), 'atLeast'); trPr.append(trh)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

FILL_GAP = 6    # extra space below each fill-in line (paired with double line spacing for writing room)

def candidate_block(doc):
    heading(doc, "Trainee Information")
    for label in ["Trainee Name (as per NRIC): ______________________________________",
                  "Last 3 digits and alphabet of NRIC/FIN: ____________________",
                  "Date: ____________________"]:
        p = para(doc, label, size=11, after=FILL_GAP)
        p.paragraph_format.line_spacing = 2.0

# Assessment briefing (from the course slides — "Briefing for Assessment").
BRIEFING = [
    "Place phones and other materials under the table or on the floor.",
    "No photos or recording of assessment scripts.",
    "No discussion during the assessment.",
    "Use a black/blue pen for hard-copy assessments.",
    "No liquid paper / correction tape.",
    "Scripts are collected when time is up.",
]

LMS_URL = "https://lms-tms.tertiaryinfotech.com/"

def add_hyperlink(p, url, text):
    """Add a real clickable Word hyperlink (blue, underlined) to paragraph p."""
    r_id = p.part.relate_to(
        url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True)
    link = OxmlElement("w:hyperlink"); link.set(qn("r:id"), r_id)
    run = OxmlElement("w:r"); rPr = OxmlElement("w:rPr")
    sz = OxmlElement("w:sz"); sz.set(qn("w:val"), "22"); rPr.append(sz)  # 11pt
    color = OxmlElement("w:color"); color.set(qn("w:val"), "0563C1"); rPr.append(color)
    u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); rPr.append(u)
    run.append(rPr)
    t = OxmlElement("w:t"); t.text = text; run.append(t)
    link.append(run); p._p.append(link)
    return link

def instructions(doc, minutes_text):
    heading(doc, "Instructions to Candidate")
    # None marks the upload instruction, which carries a clickable LMS hyperlink.
    items = [
        "This is an individual exercise.",
        "This is an open-book assessment.",
        f"A total of {minutes_text} is given to complete this assessment.",
        None,
    ] + BRIEFING
    for i, s in enumerate(items, 1):
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(4)
        if s is None:
            p.add_run(f"{i}.  Complete your answers on the document provided and "
                      "upload the completed answers to the LMS at ").font.size = Pt(11)
            add_hyperlink(p, LMS_URL, LMS_URL)
            p.add_run(".").font.size = Pt(11)
        else:
            p.add_run(f"{i}.  {s}").font.size = Pt(11)

def grading(doc, what):
    heading(doc, "Grading")
    para(doc, what, size=11, after=12)
    for ln in ["Grade: _______  (C / NYC)",
               "Assessor Name: __________________________   Assessor NRIC: ________________",
               "Date: ________________________                    Signature: ____________________"]:
        p = para(doc, ln, size=11, after=FILL_GAP)
        p.paragraph_format.line_spacing = 2.0

def finish(doc, path):
    prodoc.add_page_numbers(doc); prodoc.enable_update_fields(doc)
    doc.save(path); print("  saved:", os.path.basename(path))

# ---------------------------------------------------------------- builders
def build_wa(answers):
    doc = base_doc()
    kind = "Written Assessment (SAQ) — Answer Key" if answers else "Written Assessment (SAQ)"
    prodoc.add_cover_page(doc, kind, TITLE, A_VER if answers else Q_VER,
                          org_logo=ORG_LOGO, course_logo=COURSE_LOGO)
    para(doc, TITLE, size=15, bold=True, color=DARK, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    para(doc, "Answers to Written Assessment (SAQ)" if answers else "Written Assessment (SAQ)",
         size=13, bold=True, color=BRAND, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    para(doc, f"Course Code: {COURSE_CODE}", size=11, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, after=12)
    if not answers:
        # Page 2 — candidate information, instructions and grading; questions begin on the next page.
        candidate_block(doc); instructions(doc, "1 hour")
        grading(doc, "Candidate has answered all written questions and demonstrated the underpinning "
                     "knowledge required for the course learning outcomes.")
        page_break(doc)
    para(doc, "Short-Answer Questions (Knowledge)", size=13, bold=True, color=BRAND, after=4)
    para(doc, "Answer all questions in your own words. Each question tests underpinning knowledge covered in the "
              "course slides.", size=10.5, italic=True, color=GREY, after=8)
    # Pagination is EXPLICIT — two questions to a page on the paper, one model answer to a
    # page in the key. Do not swap this for Word's keepNext/cantSplit: Word pushes an
    # oversized box to the next page, but Google Docs draws the border anyway and prints the
    # question text and the page footer straight THROUGH it. See SKILL.md → Pagination.
    per_page = 1 if answers else 2
    for i, (crit, ctx, q, pts) in enumerate(WRITTEN, 1):
        para(doc, f"Question {i}:", size=11.5, bold=True, after=2, before=6)
        para(doc, ctx, size=11, after=3)
        para(doc, f"{q}  ({crit})", size=11, bold=True, after=4)
        answer_box(doc, lines=pts if answers else None)
        if i % per_page == 0 and i < len(WRITTEN):
            page_break(doc)
    suffix = A_VER if answers else Q_VER
    name = (f"Answer to WA (SAQ) - {TITLE} - {suffix}.docx" if answers
            else f"WA (SAQ) - {TITLE} - {suffix}.docx")
    finish(doc, os.path.join(OUT, name))

def build_pp(answers):
    doc = base_doc()
    kind = "Practical Performance (PP) — Answer Key" if answers else "Practical Performance (PP)"
    prodoc.add_cover_page(doc, kind, TITLE, A_VER if answers else Q_VER,
                          org_logo=ORG_LOGO, course_logo=COURSE_LOGO)
    para(doc, TITLE, size=15, bold=True, color=DARK, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    para(doc, "Answers to Practical Performance Assessment" if answers else "Practical Performance Assessment",
         size=13, bold=True, color=BRAND, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    para(doc, f"Course Code: {COURSE_CODE}", size=11, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, after=12)
    if not answers:
        # Page 2 — candidate information, instructions and grading; the problem begins on the next page.
        candidate_block(doc); instructions(doc, "1 hour")   # matches the original TMS paper
        grading(doc, "Candidate has successfully completed all PP tasks and can explain the overall "
                     "functions and features used to achieve them.")
        page_break(doc)
    para(doc, "Practical Problem", size=13, bold=True, color=BRAND, after=4)
    para(doc, "Scenario", size=11.5, bold=True, after=2)
    para(doc, SCENARIO, size=11, after=8)
    # Practical tasks are long and their boxes are tall, so they get a page each — on the
    # paper AND in the key. Same rule as the WA: the page break is ours, not the renderer's.
    for i, (label, crit, prompt, cap, pts) in enumerate(PRACTICAL, 1):
        para(doc, f"{label} ({crit}):", size=11.5, bold=True, after=2, before=6)
        para(doc, prompt, size=11, after=3)
        para(doc, cap, size=10.5, italic=True, color=GREY, after=4)
        answer_box(doc, code=pts if answers else None, height_pt=150)
        if i < len(PRACTICAL):
            page_break(doc)
    suffix = A_VER if answers else Q_VER
    name = (f"Answer to PP Assessment - {TITLE} - {suffix}.docx" if answers
            else f"PP Assessment - {TITLE} - {suffix}.docx")
    finish(doc, os.path.join(OUT, name))

if __name__ == "__main__":
    print("Building WSQ assessment set…")
    build_wa(answers=False); build_wa(answers=True)
    build_pp(answers=False); build_pp(answers=True)
    print(f"Done. WA: {len(WRITTEN)} questions · PP: {len(PRACTICAL)} tasks.")
