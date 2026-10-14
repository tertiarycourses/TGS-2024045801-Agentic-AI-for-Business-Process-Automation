#!/usr/bin/env python3
"""Generate the Agentic AI for Business Process Automation (TGS-2024045801) Learner Guide
as BOTH a Markdown mirror (LG-*.md at repo root) and a DOCX (courseware/LG-*.docx)
from one source, so they never diverge.

House format: cover page, Document Version Control Record, auto TOC, Arial 11pt
body, one section per lab (Objective · Goal · What you'll build · Step-by-step ·
Test it · What you learned · Troubleshooting), plus setup, concepts and glossary.
All content is driven by course_data + the domain data files, keeping the LG 100%
aligned with the slide deck, Lesson Plan and labs.
"""
import os, sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import course_data as C
from data_domain1 import DOMAIN1
from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3
ACT=DOMAIN1+DOMAIN2+DOMAIN3
import prodoc
from slide_index import SLIDES

def _find_repo(start):
    env=os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d=start
    for _ in range(8):
        d=os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(HERE))
REPO=_find_repo(HERE); ASSETS=os.path.join(os.path.dirname(HERE),"assets")
CWASSETS=os.path.join(REPO,"courseware","assets")

# ---------------- block DSL (single content stream → MD + DOCX) ----------------
B=[]
def h1(t): B.append(("h1",t))
def h2(t): B.append(("h2",t))
def h3(t): B.append(("h3",t))
def p(t):  B.append(("p",t))
def bullets(xs): B.append(("bullets",xs))
def steps(xs): B.append(("steps",xs))
def code(t): B.append(("code",t))
def note(t): B.append(("note",t))
def rule(): B.append(("rule",))
def table(headers,rows): B.append(("table",headers,rows))
def image(fn,caption): B.append(("image",fn,caption))

def slideref(key):
    r=SLIDES.get(key)
    if not r: return ""
    a,b=r
    return f"Slides {a}–{b}" if b>a else f"Slide {a}"

# Single source for the Document Version Control Record — used by BOTH the DOCX
# and the Markdown mirror, so the two can never disagree.
VC_ROWS = [
 ("1.0","31 July 2026",
  "Initial release — Learner Guide for Agentic AI for Business Process Automation, covering the "
  "five hands-on labs across n8n fundamentals, AI agents, agentic chatbots, human-in-the-loop "
  "approval and RAG. Aligned to TSC " + C.TSC_CODE + ".", C.TRAINER),
 ("1.1", "1 August 2026",
  "Added a 'Why this step' note to every lab step; lab headings de-duplicated; version-control "
  "record added to the Markdown mirror and the mirror relocated beside the DOCX.", "Dr. Alfred Ang"),
 ("1.2", "1 August 2026",
  "Added a screenshot of each lab's application — the four lab websites with their chat widgets open, "
  "plus the Lab 1 n8n canvas and sample flyer — to the slide deck and the Learner Guide.", C.TRAINER),
 ("2.0", "8 August 2026",
  "Slide deck restyled to the house reference format. Lab step-by-step removed from the deck and now "
  "carried only by this guide, with a rendered n8n canvas screenshot per lab. New concept sections: "
  "trigger nodes, data-processing nodes, the four components of an AI agent, instruction design with "
  "worked examples, model parameters and temperature, MCP, webhooks (GET/POST, Test vs Production "
  "URL) and human-in-the-loop with guardrails.", C.TRAINER),
 (C.VERSION.lstrip("v"), C.VERSION_DATE,
  "Topic 1 now opens with the modern view of agentic automation, replacing the separate Foundation section: a brief history of AI 2023–2026 (prompt, context and harness engineering to AI agents), agentic AI vs AI agents, workflow first vs agent first, AI-assisted workflow creation with n8n Assistant (plus claiming the free AI credits and a social media campaign demo), an n8n training-accounts slide, the five principles of AI security and why workflow first is more secure, and the business value of workflow-first agentic automation.", C.TRAINER),
]

# ================================================================ content
h1("Introduction")
p(f"This Learner Guide accompanies the WSQ course {C.TITLE} ({C.COURSE_CODE}), conducted by "
  f"{C.ORG}. It provides step-by-step instructions for all five hands-on labs, organised by the "
  "three course topics, and is aligned to the Skills Framework TSC "
  f"{C.TSC_TITLE} ({C.TSC_CODE}).")
p("Across the course you build five working automations in n8n: a form-triggered workflow, a "
  "webhook-triggered AI agent behind a real website, an agentic chatbot bound by compliance rules, "
  "a human-in-the-loop approval chain, and a Retrieval-Augmented Generation chatbot grounded in an "
  "organisation's own documents.")
p("Use this guide alongside the course slides and the lab files in the labs/ folder. Every lab is "
  "self-contained, but they are deliberately ordered — each one introduces exactly one new idea on "
  "top of the last. Read the 'What you learned' box at the end of each lab before moving on.")
note("Several labs send real email and write to real spreadsheets. Always use your own email "
     "address in the test data, and never point a lab at a colleague's or customer's address.")

h1("Course Learning Outcomes")
bullets(C.LEARNING_OUTCOMES)

h1("Skills Framework Alignment")
p(f"This course is mapped to the TSC {C.TSC_TITLE} ({C.TSC_CODE}). The Written Assessment covers "
  "the Knowledge (K) statements; the Practical Performance covers the Ability (A) statements.")
table(["Code","Ability statement"],[[c,t] for c,t in C.TSC_ABILITIES])
table(["Code","Knowledge statement"],[[c,t] for c,t in C.TSC_KNOWLEDGE])

h1("Before You Start — Environment Setup")
h3("What you need")
bullets([
 "An n8n instance — either a free n8n Cloud trial (sign up at n8n.io) or a self-hosted instance via Docker or npm. The class instance is provided by the trainer.",
 "A Google account for Gmail, Google Sheets and Google Drive credentials (OAuth2).",
 "A Google Gemini API key (or an OpenAI API key) for the AI Agent, chat model and embeddings nodes.",
 "Your n8n training account — the trainer assigns one per learner (see the n8n Training Accounts slide). Sign in with it, and do not change its password.",
 "A modern web browser — several labs open a local HTML page that talks to your n8n webhook.",
 "Python 3 (already installed on macOS and Linux) to serve the lab websites with a one-line HTTP server.",
])
h3("Set up n8n")
p("You can run n8n three ways. For this course either the cloud trial or a local Docker instance "
  "works; the visual editor is identical in both.")
table(["Option","How to start","Best for"],[
 ["n8n Cloud","Sign up at n8n.io and open the editor in your browser","This course — nothing to install"],
 ["Docker","docker compose up -d, then open http://localhost:5678","Production; your data stays with you"],
 ["npm","npx n8n","A quick local trial"],
])
h3("Add your credentials")
p("Add each credential once, under Credentials → Add credential. Every workflow can then reuse it. "
  "You will need Gmail (OAuth2), Google Sheets (OAuth2), Google Drive (OAuth2) and Google Gemini "
  "(API key). Never paste an API key directly into a node field — always store it in a credential.")
note("Imported workflows reference credential NAMES, not secrets. After importing any lab workflow "
     "you must re-select your own credentials on every node showing a credential warning.")
h3("Import a lab workflow")
p("Each lab ships with a ready-made .json workflow in its folder. In n8n choose "
  "Workflows → Add workflow → ⋯ (top-right) → Import from File, and pick the lab's .json file.")
h3("Test URL vs Production URL")
p("Every Webhook and Form node has two URLs, and confusing them is the single most common failure "
  "in these labs.")
table(["URL","When it works","How many requests"],[
 ["Test URL (/webhook-test/…)","Only while you have clicked 'Listen for test event'","Exactly one, then it stops"],
 ["Production URL (/webhook/…)","Only while the workflow is Active","Unlimited"],
])
p("Use the Test URL while building — it shows the incoming data live on the canvas. Switch to the "
  "Production URL the moment you want the page to work for anyone but you.")
h3("Conventions used in every lab")
bullets([
 "Node names are written exactly as they appear on the n8n canvas, e.g. Onboarding Webhook.",
 "Expressions are written in n8n syntax, e.g. {{ $json.Name }}.",
 "Where a lab serves a website, run the command from inside that lab's folder.",
 "Placeholders such as REPLACE_WITH_YOUR_EMAIL@example.com must be replaced before the lab will run.",
 "Each lab ends with a 'Test it' check — do not move on until it passes.",
])

# ---------------- Topic 1 opener: why agentic AI, and why workflow first ----------------
# Mirrors topic1_intro() in build_slides.py. Emitted at the top of Topic 1 (there is
# no separate Foundation chapter).
def topic1_intro_lg():
    h2("Why Agentic AI, and Why Workflow First")
    p(f"Deck reference: {slideref('topic1_intro')}.")
    h3("A brief history of AI, 2023–2026")
    table(["Year","Era","What changed"],[
     ["2023","Prompt Engineering","ChatGPT goes mainstream. Results depend on how well you word the prompt."],
     ["2024","Context Engineering","Models call tools and MCP launches. Results depend on the documents, data and tools you supply."],
     ["2025","Harness Engineering","Claude Code and Codex: systems built around the model that plan, act and check their own work in a loop."],
     ["2026","AI Agents","Always-on agents work 24/7 — OpenClaw, Hermes Agent and agent teams take on whole jobs."],
    ])
    p("Each year moved the skill that matters: from wording one prompt, to curating the context, to "
      "engineering the harness around the model, to AI agents that work around the clock.")
    h3("What is agentic AI")
    p("Agentic AI uses the reasoning power of a large language model to run a complex task by breaking "
      "it into simpler ones. Given a goal, the model observes the situation, chooses an action, acts on "
      "the world through a tool, observes the result, and repeats until the goal is met.")
    image("ai-agent-llm-loop.png",
          "The agent loop — goal, observation, action, observation, action. Each step is an LLM call "
          "that decides what to do next based on what came back.")
    h3("Agentic AI vs generative AI")
    table(["","Generative AI","Agentic AI"],[
     ["Purpose","Creates content — text, images, code","Takes actions towards a goal"],
     ["Interaction","Responds to a prompt, once","Plans, acts, observes and adapts"],
     ["Context","Relies on you for context and goals","Uses tools to reach real systems and data"],
     ["Completion","Stops when the answer is produced","Continues until the goal is met"],
     ["Example","\"Draft me an email\"","\"Read the enquiry, check the CRM, reply and log it\""],
    ])
    h3("Agentic AI vs AI agents")
    p("AGENTIC AI is the broad category: any AI system that pursues a goal over many steps — it "
      "plans, acts through tools, checks the result and adapts. It is usually started by a person or "
      "a trigger and stops when the task is done; a Claude Code or Codex session, or an n8n workflow "
      "with AI steps, are agentic AI. AI AGENTS are a special type of agentic AI system that exists "
      "24/7. They are usually installed in the cloud so they serve all the time, with no laptop "
      "needing to be open: they wait for events — messages, emails, webhooks, schedules — act on them "
      "around the clock, and keep their memory across conversations and days. OpenClaw, Hermes Agent "
      "and an n8n agent running on a cloud instance behind a webhook are AI agents. Every AI agent is "
      "agentic AI, but not every agentic AI is an AI agent — the difference is that an AI agent is "
      "always on.")
    h3("Workflow first vs agent first")
    p("There are two ways to build agentic automation. WORKFLOW FIRST is the modern form of rule-based "
      "(RPA-style) automation: the workflow owns the path, and its steps can be ordinary nodes, AI "
      "nodes or even AI Agent nodes — exactly as in n8n, where an AI Agent node sits inside a "
      "workflow. AGENT FIRST hands the whole path to an AI agent, which decides the steps and tools "
      "at run time.")
    table(["","Workflow First","Agent First"],[
     ["Who decides the path","The workflow — steps may be AI nodes or AI Agent nodes","The agent decides the steps and tools at run time"],
     ["Behaviour","Deterministic — same input, same path, every time","Probabilistic — the path can change between runs"],
     ["Efficiency","More effort to design every branch up front","Efficient — one instruction replaces many hand-built branches"],
     ["Reliability & testing","Easy to test, debug and certify step by step","Harder to test; edge cases surface in production"],
     ["Cost & speed","An LLM call only where needed — cheap and fast","An LLM call at every step — more tokens, more latency"],
     ["Best for","Repeatable, regulated, high-volume processes","Open-ended tasks with unpredictable inputs"],
    ])
    p("Workflow first is more deterministic; agent first is more efficient. Because reliability matters "
      "most in business, companies try to make as much of a process deterministic as possible. "
      "(Source: n8n, In The Loop 2026 opening keynote and product direction.)")
    h3("The trend: AI-assisted workflow creation")
    p("AI-powered coding tools — n8n Assistant inside n8n, and Claude Code and Codex outside it — are "
      "AI agents themselves, and they have made designing, building and changing workflows fast and "
      "cheap. The trend is AI-ASSISTED WORKFLOW CREATION: describe the process in plain English, let "
      "the assistant draft the workflow, review and test it, and then let the deterministic workflow "
      "RUN the process, with AI and AI Agent nodes only where judgement is needed. The agent's "
      "efficiency goes into building; the workflow's determinism goes into running.")
    h3("n8n Assistant — describe it, n8n builds it")
    p("Open Assistant in the left sidebar of n8n. At the prompt \"What do you want to automate?\" "
      "describe the workflow: what triggers it, which apps it uses, what data it reads and writes, "
      "what happens on success and on failure, and whether it should ask before publishing. n8n "
      "Assistant plans the workflow, builds it in your project, tests it and helps fix errors. The "
      "result is a normal n8n workflow that you open, inspect, edit, test and publish yourself. On "
      "n8n Cloud, Assistant chats use the plan's monthly Assistant credits; they are separate from "
      "the Gateway credits your workflow's AI nodes use when they run.")
    image("n8n-assistant.png",
          "n8n Assistant — \"What do you want to automate?\" Type a prompt, or start from a suggestion "
          "such as Score my leads or Schedule social posts.")
    h3("Claim your free AI credits")
    p("The n8n Cloud free trial includes free Gateway credits, which let a node call a supported AI "
      "model without a provider account or API key.")
    steps([
     ("Sign in to n8n Cloud with your training account.", "", "The trial's credit balance belongs to that instance."),
     ("Open a workflow and add an AI node — for example an AI Agent with a Google Gemini or OpenAI Chat Model.", "", ""),
     ("In the node's Credential field, select Use Gateway credits. The option shows your remaining balance.", "", "No API key is pasted anywhere, so none can leak."),
     ("Pick a supported model, configure the rest of the node as usual, and run it.", "", ""),
     ("Track the balance on the node, or in the Admin Panel under Gateway credits.", "", "When the balance reaches zero, nodes on Gateway credits stop until credit is added or you switch to your own credential."),
    ])
    note("If a red toast reads \"Free AI credits — Enable to claim credits\", that is n8n's legacy one-time "
         "OpenAI offer, which is not issued to instances that have Gateway credits. Ignore it and use "
         "Use Gateway credits on the node instead.")
    h3("Demo: build a social media campaign workflow with n8n Assistant")
    p("Paste this prompt into n8n Assistant:")
    code("\n".join(C.DEMO_PROMPT))
    p("n8n Assistant plans and builds a five-stage workflow: a Form Trigger where you enter the topic; "
      "an AI Agent with a web-search tool that researches it; an AI step that drafts the post; a "
      "human-in-the-loop approval (Gmail Send and Wait for Response) so nothing is posted unchecked; "
      "and a Wait plus the social node that schedules and publishes the approved post, with "
      "rejections logged to a Google Sheet. Then review the plan before it builds, connect Gmail and "
      "the social account when it asks, test with a real topic and approve the draft, and publish "
      "only when the run looks right. The AI built the workflow; the workflow runs it.")
    h3("The five principles of AI security")
    table(["Principle","Controls","What it means"],[
     ["1. Data Control","What AI can see","Classify your data — public, internal, confidential — and decide exactly which data the AI may access."],
     ["2. Permission Control","What AI can do","Grant only the rights needed — read, write, edit, delete. Ask before anything destructive."],
     ["3. Human in the Loop","Who approves","A person reviews and approves high-impact actions — payments, deletions, customer emails."],
     ["4. Traceability","What happened","Log every prompt, tool call and change so actions can be audited, explained and rolled back."],
     ["5. Right-Sized Models","Not the most powerful","The smallest model that does the job carries less autonomy and less risk."],
    ])
    p("In n8n these map to scoped credentials per node, approval gates (Gmail Send and Wait for "
      "Response), the Executions log, and a small model for each AI step.")
    h3("Why workflow first is more secure")
    p("A fixed path limits the blast radius: a manipulated AI step — for example one hit by a prompt "
      "injection — cannot reach tools that are not wired to it.")
    table(["Principle","Workflow First","Agent First"],[
     ["Data control","Each node sees only the fields wired into it","The agent can reach any data its tools expose"],
     ["Permission control","Each credential is scoped to one node and one action","The agent holds every tool's rights at once"],
     ["Human in the loop","The approval gate sits at a fixed, designed step","Depends on the agent choosing to ask"],
     ["Traceability","Every run is logged node by node in Executions","Reasoning varies run to run and is harder to explain"],
     ["Right-sized models","A small model for each narrow AI step","One capable model with broad autonomy"],
    ])
    h3("Business value of workflow-first agentic automation")
    bullets([
     "Reliable and predictable — the same input follows the same path every time, so the process can be tested and trusted like software.",
     "Secure by design — each step holds only the data and credentials it needs, and risky actions wait at an approval gate.",
     "Auditable end to end — every run is logged node by node, so any decision can be explained, replayed and corrected.",
     "Lower running cost — deterministic steps cost nothing in tokens; the LLM is called only where judgement is needed.",
     "Faster to build and change — Claude Code and Codex draft the workflow in minutes; your team reviews, tests and owns it.",
     "Scale around the clock — triggers respond in real time, 24/7, and ten times the volume costs compute, not ten more hires.",
    ])
    h3("Where agentic automation is used")
    p("The same pattern — trigger, agent, tools, oversight — recurs in customer service, finance and "
      "accounting, risk and compliance, HR and people operations, sales and marketing, and operations.")
    h3("Where agent platforms sit")
    table(["Tier","Characteristics","Examples"],[
     ["No-code","Fully visual; fastest to a working agent; least control","AgentX and similar chatbot builders"],
     ["Low-code","Visual canvas plus code nodes; 400+ integrations; self-host or cloud","n8n — this course's platform"],
     ["Full-code","SDKs and frameworks; maximum control; needs engineering effort","LangChain and agent SDKs"],
    ])


# ---------------- per-topic, per-lab ----------------
TOPIC_EXTRA_CONCEPTS = {
 1: [
  ("What is n8n",
   "n8n is a fair-code workflow automation platform. You drag nodes onto a visual canvas and wire "
   "them together to move data between more than 400 applications, with little or no code. Every "
   "node shows its input and output as JSON, so you can see exactly what is flowing through. "
   "Workflows are plain JSON files you can export, version and share."),
  ("Nodes: the four building blocks",
   "TRIGGER nodes start a workflow (Form, Webhook, Schedule, Chat, Manual). ACTION nodes do "
   "something (send Gmail, append a Google Sheets row, call an HTTP API). LOGIC nodes control the "
   "flow (IF, Switch, Merge, Split Out, Code, Edit Fields). AI nodes reason and act (AI Agent, Chat "
   "Model, Memory, Embeddings, Vector Store, Tools)."),
  ("Triggers and actions",
   "A trigger decides WHEN a workflow runs; an action decides WHAT it does. This is the whole idea "
   "behind Lab 1 — one trigger, one action, and a working automation."),
  ("Data, JSON and expressions",
   "Data flows between nodes as a list of items, each a JSON object of key/value pairs. Read a value "
   "from an earlier node with an expression such as {{ $json.Name }}. Expressions work in any field "
   "— subject lines, URLs, conditions and message bodies. You can also drag a field from the input "
   "panel to map it automatically."),
  ("What is an AI agent",
   "An AI agent is an LLM given a goal, a set of tools and memory. The model supplies the judgement "
   "— which tool to call and when — while you supply the goal, the guardrails and the tools it is "
   "allowed to use. In n8n an agent has four parts: a Chat Model, a System Instruction, Memory and "
   "Tools."),
  ("Writing a good system instruction",
   "State the role plainly. Give the scope and the limits — what it must answer and what it must "
   "refuse. Say which tool to use for which kind of question. Ask for a specific output format when "
   "something downstream depends on it. Tell it to say 'I don't know' rather than invent an answer. "
   "Then test it with real questions and refine."),
  ("Webhooks",
   "A webhook is a URL that any external system can POST data to; it starts your workflow when "
   "called. It is the opposite of an HTTP Request node: there YOU call the outside world, here the "
   "outside world calls YOU. Set Allowed Origins (CORS) so a browser page may read the reply, and "
   "consider Authentication before anything goes to production — an open webhook costs you money "
   "every time a stranger calls it."),
  ("Trigger nodes — what may start a workflow",
   "The trigger you choose is a statement about who or what is allowed to start the process. Manual "
   "Trigger runs on a click, for building and for one-off jobs such as the Lab 5 ingestion. Schedule "
   "Trigger runs on a clock. Form Trigger hosts a web form for you, and is Lab 1's front door. Webhook "
   "lets an external system call a URL you expose, and is the front door for Labs 2 to 5. Chat Trigger "
   "uses n8n's built-in chat window. App and email triggers fire on a new Gmail message, a new Sheets "
   "row or a new Drive file."),
  ("Data-processing nodes — the workhorses",
   "Between the trigger and the output these nodes shape, route and transform the data. Edit Fields "
   "(Set) adds, renames or reshapes fields and is the node you reach for first when data is the wrong "
   "shape. IF and Switch branch the workflow — Lab 4 uses an IF to split the approved path from the "
   "reassignment path. Filter drops non-matching items; Merge combines branches; Split Out and "
   "Aggregate convert between one item holding a list and many items. Code runs JavaScript or Python "
   "for the small fraction a built-in node cannot do. HTTP Request calls any API on the internet."),
  ("Where the data goes",
   "Google Sheets is the audit log in Labs 2 and 4 — Append Row is the workhorse operation. Gmail "
   "sends a message, and in Lab 4 its Send and Wait for Response operation turns email into an "
   "approval gate. A Vector Store holds embeddings for RAG. Respond to Webhook returns data to "
   "whoever called the webhook, which is what lets a web page render the agent's answer."),
  ("The four components of an AI agent",
   "Every agent in this course is exactly four parts around one hub. The MODEL is the LLM that "
   "interprets language, reasons and chooses the next step. MEMORY keeps the conversation so a "
   "follow-up question still makes sense, keyed on a session ID. TOOLS are the abilities it may use — "
   "look up a Sheets row, search a vector store, send an email, call an API. INSTRUCTIONS are the "
   "system message: identity, scope, rules and refusals, always in force on every turn. Change any "
   "one of the four and you have a different agent."),
  ("Model parameters — temperature and friends",
   "Settings on the chat-model node shape HOW the model answers, and the most important is "
   "temperature. A temperature of 0 to 0.3 is deterministic and repeatable — use it for "
   "classification, compliance decisions and data extraction, that is, any automation that must give "
   "the same answer twice. Around 0.7 is balanced and natural-sounding, the usual default for a "
   "customer-facing assistant. Above 1.0 is creative and surprising, suitable for marketing copy and "
   "never for a decision you must defend. Top-p is an alternative sampling control — tune temperature "
   "or top-p, never both. Max tokens caps the reply length and so caps your cost. Lab 3 uses "
   "temperature 0.2 so a compliance-bound chatbot refuses the same way every time."),
  ("Popular LLM providers",
   "Any chat model plugs into the same AI Agent node, so you can swap the brain and keep the agent. "
   "This course uses Google Gemini, which also supplies the embeddings in Lab 5. OpenAI (gpt-4.1 and "
   "the cheaper mini tier), Anthropic Claude, Meta Llama and Mistral are all commonly used. Pick by "
   "task: small fast models for classification and guardrails, larger models for reasoning."),
  ("Tools — and why the description matters",
   "Tools attach to the agent's Tool input, and the model decides when to call one based on the "
   "DESCRIPTION you write. Write that description for the model, not for a developer. Lab 2 attaches "
   "three tools — check for a duplicate customer, create the customer record, send the confirmation "
   "— and you can watch the agent choose between them on the canvas."),
  ("Instructions — the four parts that constrain",
   "Every good agent instruction states four things. IDENTITY: who the agent is and for whom. SOURCE "
   "RULES: where answers may come from, for example 'answer only from the brochures returned by the "
   "tool'. REFUSALS: what is out of bounds, stated explicitly. ESCALATION: what to do at the "
   "boundary, for example 'if unsure, say so and offer a consultation'. Vague instructions produce "
   "confident wrong answers — every rule you skip, the model improvises."),
  ("Good and bad instructions compared",
   "A bad instruction reads 'You are a helpful assistant. Answer the user's questions politely.' It "
   "has no identity, no source rules, no refusals and no escalation, so it will invent a course fee "
   "and guarantee an investment return — politely. A good instruction names the firm, limits the "
   "topics, points at a specific tool for factual questions, lists the prohibitions, and says what to "
   "do when unsure. The test is simple: you can try to break each line of a good instruction, and you "
   "cannot even test a vague one."),
  ("MCP — the Model Context Protocol",
   "MCP is an open standard that gives agents a common plug for tools and data. Without it, every "
   "agent needs a custom integration for every tool: N agents and M tools means N times M connectors "
   "to build and maintain. With MCP you build one MCP server per system and any MCP-capable agent can "
   "use it — N plus M pieces, and the tools become reusable. It is often described as USB-C for AI "
   "tools. n8n sits on both sides: the MCP Server Trigger exposes your n8n workflows AS tools that "
   "Claude or an IDE can call, and the MCP Client Tool attaches external MCP servers to your own n8n "
   "agent."),
  ("Webhooks — GET vs POST",
   "The HTTP method is part of the contract with the caller. With GET the data rides in the URL query "
   "string, for example ?email=alice@corp.com, so a browser can call it just by visiting the URL; you "
   "read it in n8n as {{ $json.query.email }}. GET suits a dashboard pulling data to display. With "
   "POST the data rides in the request body as JSON, which is what a web form or a chat widget sends; "
   "you read it as {{ $json.body.message }}. Every lab website in this course POSTs. Set the method "
   "on the Webhook node, and the caller must match it exactly."),
  ("Webhook Test URL vs Production URL",
   "Every Webhook node gives you two URLs, and confusing them is the single most common webhook bug. "
   "The Test URL (/webhook-test/…) works only while you have clicked 'Listen for test event', handles "
   "exactly one call and then stops, shows the run live on the canvas, and dies when you leave the "
   "editor. The Production URL (/webhook/…) requires the workflow to be Active, is always on, accepts "
   "unlimited calls, and logs its runs under Executions rather than drawing them on the canvas. Your "
   "website must call the Production URL of an Active workflow."),
  ("Configuring the Webhook node",
   "Four settings decide whether a browser's call succeeds. METHOD AND PATH give you the URL. ALLOWED "
   "ORIGINS (CORS) must permit the calling page, or the workflow will run perfectly and the browser "
   "will still refuse to read the reply — the classic 'Failed to fetch'. Set it to * in class and "
   "never in production. RESPONSE MODE should be 'Using Respond to Webhook Node' in every lab here, so "
   "the agent's answer travels back instead of an immediate 200 OK. AUTHENTICATION can be None for a "
   "demo, but Basic, Header or JWT for anything real — a public URL is a public door, and every call "
   "costs you model tokens."),
  ("Structured output",
   "By default an agent returns a paragraph of prose, and prose cannot be branched on, sorted or "
   "coloured. A Structured Output Parser forces named fields such as decision, reason and riskFlags. "
   "An IF node can then route on decision, a Sheets node can log it, and a web page can colour the "
   "result card. Enumerate the allowed values so the field stays reliable."),
 ],
 2: [
  ("What is an agentic workflow",
   "An agentic workflow is one where the LLM makes the routing decisions. You still design the "
   "process, the guardrails and the tools; what you hand over is the judgement about which path a "
   "particular case should take."),
  ("Rule-based versus agentic",
   "A rule-based (RPA) workflow has every branch wired by hand and breaks on anything unexpected, "
   "but is predictable and easy to audit. An agentic workflow understands free text and intent and "
   "handles cases you did not foresee, but needs guardrails and logging. Choose rule-based for "
   "fixed, high-volume rules; agentic for varied, language-driven work."),
  ("Designing a safe agentic chatbot",
   "Define the role narrowly — a chatbot for one job refuses far more reliably than a general "
   "assistant. Write the prohibitions explicitly. Add a fallback sentence such as 'when in doubt, "
   "say less and offer a consultation'. Gate what must be collected before answering. Keep a small "
   "FAQ in the prompt rather than a vector store. Test with the questions you most fear."),
  ("Memory — and when not to use it",
   "A memory node lets a follow-up question be answered in context. Memory is keyed on a session ID "
   "so two visitors never see each other's conversation. But some workflows must have NO memory: an "
   "application decision should never be influenced by the previous applicant. Ask, for every agent: "
   "should this case know about the last one?"),
  ("Human in the loop",
   "Some actions are too consequential to automate. A human-in-the-loop step pauses the workflow "
   "until a named person approves or declines. The agent may do everything except the one thing that "
   "matters — sending. In n8n this is the Gmail 'Send and Wait for Response' node, and the execution "
   "genuinely pauses on the canvas until a button is clicked."),
  ("When to put a human in the loop",
   "When money moves; when it is a regulated communication; when the action is irreversible; when a "
   "person is vulnerable; when the stakes exceed the error rate; and when someone must be "
   "accountable. The question is never 'is the model good?' but 'what does one bad output cost?'"),
  ("Human in, on, and out of the loop",
   "There are three levels of human oversight, and the design question is which one a given process "
   "deserves. Human IN the loop means the workflow pauses and a named person must approve before the "
   "action happens — nothing reaches the customer unauthorised, which is Lab 4. Human ON the loop "
   "means the agent acts immediately while a person monitors and can intervene or reverse it, which "
   "suits high volume with low individual risk. Human OUT of the loop is fully autonomous, and is "
   "acceptable only where an error is cheap, reversible and detectable — never where money or a "
   "regulator is involved."),
  ("How an approval suspends a running workflow",
   "A Send-and-Wait node stops the execution mid-flight. Look at the canvas and the run is genuinely "
   "sitting on the approval node; n8n holds the state, and it will wait for days if it has to. The "
   "Approve and Decline buttons in the email are simply two URLs, so clicking one resumes the "
   "execution down that branch and the approver has no new application to learn. A decline is a "
   "reassignment rather than a deletion, because someone still owes the client an answer."),
  ("Guardrails — two gates around the agent",
   "Instructions shape what the agent intends; guardrails check what actually goes in and comes out. "
   "An INPUT guardrail screens the incoming message before the model ever sees it: block prompt "
   "injection such as 'ignore your instructions and…', strip personal data you must not process, and "
   "rate-limit and authenticate, because a public webhook is a public door. An OUTPUT guardrail "
   "checks the reply before it reaches a person: look for phrases you have banned such as guarantees "
   "and forecasts, validate the structured fields against the values you allow, and on any doubt "
   "route to a human rather than sending. Enforcing the same rule in the prompt AND in the workflow "
   "is deliberate redundancy — only one of the two runs on a machine you control."),
  ("The accountability trail",
   "Log what the agent PROPOSED separately from what a human AUTHORISED. Keeping them apart is what "
   "lets an auditor ask whether anyone ever sent something a human never saw. Every approved action "
   "carries the name of the approver; every declined one is reassigned to a named person. No "
   "accountability column should ever be empty."),
 ],
 3: [
  ("What is RAG",
   "Retrieval-Augmented Generation retrieves the few documents that resemble a question and gives "
   "the model only those, instead of everything. The model reads what matters rather than the whole "
   "corpus."),
  ("Why not just paste everything into the prompt",
   "For twenty short documents it would work. Add two hundred more and the prompt exceeds the "
   "context window; long prompts also degrade quality because models attend less well to the middle "
   "of a long context; and you pay for every token on every question whether it was relevant or not."),
  ("Tokenization and embeddings",
   "Text is first split into tokens. An embedding model then turns a chunk of text into a vector — a "
   "list of numbers positioned so that text about similar things lands close together. 'How much is "
   "the sourdough course?' lands near the sourdough brochure and far from the sushi one, even though "
   "the two share no words."),
  ("Vector stores",
   "A vector store holds those embeddings and finds the nearest neighbours to a question, fast. "
   "n8n's built-in Simple Vector Store needs no account, key or index — and is emptied whenever n8n "
   "restarts. That is not a defect; it is the honest cost of a store that requires no "
   "infrastructure. Production systems use Pinecone, Supabase (pgvector) or Qdrant."),
  ("Chunking is the biggest lever",
   "The right chunk is the smallest piece of text that still answers a question on its own. Too "
   "small and a brochure is sliced so the course name is separated from its fee — retrieval finds "
   "one without the other. Too large and irrelevant text crowds the prompt. Most RAG projects fail "
   "quietly at chunking, not at the model."),
  ("The rules that keep RAG working",
   "The ingestion and retrieval embedding models must be identical. The store's dimension must match "
   "the embedding model's output. The memory key or index name must match between ingestion and "
   "retrieval. Turn Clear Store on when re-ingesting. And topK controls how many chunks are "
   "retrieved — too few misses the answer, too many dilutes the prompt."),
  ("Grounding against hallucination",
   "Instruct the agent to always call the tool first, to base every factual claim on what came back, "
   "and to say 'I don't have that in our course information' when the documents are silent. Name "
   "what it must never invent: a fee, a date, a duration, a course code, an instructor name, a "
   "discount. An ungrounded model asked for a price will produce one — plausible, fluent and wrong."),
 ],
}

TOPIC_IMAGES = {
 3: [("rag-concept.png",
      "Retrieval finds the documents that resemble the question; Augmentation adds them to the "
      "prompt; Generation produces an answer grounded in what was retrieved."),
     ("text-embedding.png",
      "Tokenization splits the text; an embedding model turns it into a vector stored in a vector "
      "database."),
     ("vector-database.png",
      "A vector store holds the embeddings and returns the nearest matches to a query vector.")],
}

# The lab canvas screenshots come from the lab data itself (a["canvas"]), which is
# the same source the deck renders, so the guide can never show a different picture
# of the workflow than the slide does. They are generated by render_flows.py from
# each lab's own .json, so they also match the canvas the learner imports.

TROUBLESHOOTING = {
 1: [["The test form does not open","Click Execute workflow first — the Form Trigger only serves its test form while listening."],
     ["No email arrives","Check the Gmail credential is connected and that the To address is correct. Look at the execution log for a red node."],
     ["The email body shows {{ $json.Name }} literally","The Message field is in Fixed mode. Switch it to Expression."],
     ["The QR code works once, then stops","You encoded the Test URL. Activate the workflow and encode the Production URL instead."]],
 2: [["Failed to fetch in the browser","The workflow is not Active (production URL), or 'Listen for test event' is not armed (test URL)."],
     ["Failed to fetch, but the n8n execution succeeded","CORS. Set Allowed Origins to * in the Webhook node's options."],
     ["Works once, then 404","You are using the Test URL. It listens for one request only."],
     ["Cannot read properties of undefined (reading 'trim')","The Set node expects $json.body.fullName. Check the browser's Network tab: is the payload nested under body?"],
     ["The result card is blank","The Decision Parser is disconnected, so $json.output is a string rather than an object."],
     ["Everyone is REJECTED as a minor","Check the age expression in the Set node, and that the browser sends dateOfBirth as yyyy-MM-dd."]],
 3: [["Failed to fetch","Workflow not Active (production URL), or 'Listen for test event' not armed (test URL)."],
     ["Failed to fetch, but the execution ran","CORS. Set Allowed Origins to * on the Webhook node."],
     ["The agent answers before collecting contact details","The contact gate is missing from the system message, or was weakened. Restate it as a hard precondition."],
     ["The agent gives investment advice","Read the reply aloud in the debrief. Tighten the prohibitions — this is the failure the lab is designed to expose."],
     ["Follow-up questions lose context","The memory node is disconnected, or the browser is not sending a stable sessionId."]],
 4: [["No approval email arrives","RM Approval still has REPLACE_WITH_YOUR_EMAIL@example.com in Send To."],
     ["The approval email arrives but the buttons do nothing","The workflow must stay running. If n8n restarted, the paused execution is gone — resubmit."],
     ["The sheet rows are blank","'Require Specific Output Format' is off on the agent, so $json.output is a string, not an object."],
     ["Every draft is escalated","The agent is flagging ADVICE_REQUESTED on any question at all. Tighten the flag's definition — it means asks what they should do, not asks a question."],
     ["The draft contains a greeting and a sign-off","The agent ignored 'body only'; they now appear twice because the letterhead adds its own. Restate the instruction."],
     ["The draft gives advice","The approval gate caught it — which is exactly what it is for. Discuss it, then tighten the prohibitions."]],
 5: [["Every answer is 'I don't have that in our course information'","The Memory Key on Query Data Tool does not match the one on Simple Vector Store (Insert). This is the number-one cause."],
     ["It worked, then stopped after lunch","n8n restarted and the in-memory store was wiped. Re-run the ingestion workflow."],
     ["Answers are correct but a yellow 'Offline demo answer' banner appears","The webhook is unset or unreachable. You are reading the page's local fallback, not your agent."],
     ["Every brochure appears twice in the results","Clear Store is off on the insert node and you ran the ingestion twice."],
     ["The agent quotes a fee that is in no brochure","It did not call the tool, or called it and ignored the result. Check the execution log — did course_brochures actually run?"],
     ["Retrieval returns nothing sensible","The ingestion and retrieval Embeddings nodes use different models. They must be identical."]],
}

for t in C.TOPICS:
    h1(f"Topic {t['code']} — {t['title']}")
    p(t["subtitle"] + f"   (Deck reference: {slideref('topic' + str(t['num']) + '_all')}.)")
    if t["num"]==1: topic1_intro_lg()
    h3("Key concepts")
    for title_,body in TOPIC_EXTRA_CONCEPTS[t["num"]]:
        B.append(("term", title_, body))
    for fn,cap in TOPIC_IMAGES.get(t["num"],[]):
        image(fn,cap)
    for a in [x for x in ACT if x["topic"]==t["num"]]:
        # a["title"] already starts with "Lab N — "; do not prefix it a second time.
        h2(a["title"])
        p(f"Learning outcome: this lab develops your ability to {a['objective']}.")
        p(f"Deck reference: {slideref('lab'+str(a['num']))}.")
        h3("Goal")
        # "desc" is kept short enough for the deck's one-line intro; where a lab
        # also carries "desc_long", the guide prints the fuller framing instead.
        p(a.get("desc_long") or a["desc"])
        h3("What you'll build")
        p(a["build"]+f"   (Tools: {a['services']}.)")
        for fn,cap in a.get("site",[]):
            image(fn,cap)
        h3("The workflow on the n8n canvas")
        for fn,cap in a.get("canvas",[]):
            image(fn,cap)
        h3("Step-by-step")
        # steps may be (instruction, command) or (instruction, command, why)
        steps([(st[0], st[1], st[2] if len(st)>2 else "") for st in a["steps"]])
        h3("Test it")
        p(a["test"])
        h3("What you learned")
        bullets([f"{x[0]} — {x[1]}" if isinstance(x,tuple) else x for x in a["learned"]])
        h3("Troubleshooting")
        table(["Symptom","Cause and fix"],TROUBLESHOOTING[a["num"]])
        note(f"The workflow file and all supporting assets for this lab are in labs/{a['folder']}/.")
        rule()

h1("Taking This Back to Work")
bullets([
 "Start with one painful process — repetitive, high-volume and low-risk. Automate that first.",
 "Map it before you build it: draw the trigger, the decisions and the actions on paper.",
 "Decide where the human belongs. Anything irreversible, regulated or expensive keeps an approval gate.",
 "Ground the agent in your own data. RAG over your policies and documents beats a general model.",
 "Log everything from day one — you will need the audit trail long before you think you will.",
 "Iterate with real cases, and test with the questions you fear rather than the ones you hope for.",
])

h1("Assessment")
bullets([
 C.ASSESSMENT["written"],
 C.ASSESSMENT["practical"],
 "Format: Open Book — course slides, this Learner Guide and approved materials only.",
 "The Written Assessment covers the Knowledge (K) statements; the Practical Performance covers the Ability (A) statements.",
 C.ASSESSMENT["note"],
 "Submit your completed answers on the LMS at https://lms-tms.tertiaryinfotech.com/.",
 "An appeal process is available if required.",
])

h1("Glossary")
B.append(("dl",[
 ("Agentic AI","AI that pursues a goal by planning, acting through tools, observing the result and adapting — rather than answering a prompt once."),
 ("AI Agent","An LLM given a goal, a set of tools and memory, which decides which tool to call and when."),
 ("Action","A node that does something — sends an email, appends a spreadsheet row, calls an API."),
 ("Trigger","The first node in a workflow; it decides when the workflow runs."),
 ("Webhook","A URL that an external system POSTs to in order to start your workflow."),
 ("CORS","Cross-Origin Resource Sharing — the browser rule that decides whether a page may read a response from another host."),
 ("Expression","n8n syntax for reading data from an earlier node, e.g. {{ $json.Name }}."),
 ("System instruction","The agent's role, scope, prohibitions and routing rules; the main control surface for behaviour."),
 ("Memory","Conversation context kept across turns, keyed on a session ID."),
 ("Tool","A capability attached to an agent — a spreadsheet lookup, a vector search, an email send, an API call."),
 ("Structured output","Forcing the agent to return named fields instead of prose, so downstream nodes can branch on them."),
 ("Human in the loop","A step that pauses the workflow until a named person approves or declines the proposed action."),
 ("RAG","Retrieval-Augmented Generation — retrieving the documents that resemble a question and answering only from those."),
 ("Embedding","A vector representation of text, positioned so that similar meanings land close together."),
 ("Chunking","Splitting documents before embedding; the right chunk is the smallest text that still answers a question on its own."),
 ("Vector store","A database that stores embeddings and finds the nearest neighbours to a query vector."),
 ("topK","How many of the nearest chunks are retrieved and given to the model."),
 ("Hallucination","A fluent, confident answer that is not grounded in any source — what grounding rules exist to prevent."),
 ("TRAQOM","The mandatory SSG course-quality survey learners complete at the end of a WSQ course."),
]))

# ---------------- render Markdown ----------------
def _anchor(txt):
    return "".join(ch.lower() if ch.isalnum() else ("-" if ch in " -" else "") for ch in txt)

def render_md():
    out=[f"# {C.TITLE} — Learner Guide",""]
    out.append(f"**WSQ Course Code:** {C.COURSE_CODE}  |  **TSC:** {C.TSC_TITLE} ({C.TSC_CODE})  |  "
               f"**Conducted by:** {C.ORG} ({C.UEN.replace('UEN: ','UEN ')})  |  "
               f"**Version {C.VERSION} · {C.VERSION_DATE}**")
    out.append("")
    out.append("## Document Version Control Record"); out.append("")
    out.append("| Version Number | Effective Date of Release | Summary of Included Changes | Author |")
    out.append("|---|---|---|---|")
    for _v,_d,_s,_a in VC_ROWS:
        out.append(f"| {_v} | {_d} | {_s} | {_a} |")
    out.append("")
    out.append("## Contents"); out.append("")
    for kind,*rest in B:
        if kind=="h1": out.append(f"- [{rest[0]}](#{_anchor(rest[0])})")
        elif kind=="h2": out.append(f"  - [{rest[0]}](#{_anchor(rest[0])})")
    out.append("")
    for kind,*rest in B:
        if kind=="h1": out+=["",f"## {rest[0]}",""]
        elif kind=="h2": out+=["",f"### {rest[0]}",""]
        elif kind=="h3": out+=[f"**{rest[0]}**",""]
        elif kind=="p": out+=[rest[0],""]
        elif kind=="term": out+=[f"- **{rest[0]}** — {rest[1]}",""]
        elif kind=="bullets": out+=[f"- {x}" for x in rest[0]]+[""]
        elif kind=="steps":
            for i,st in enumerate(rest[0],1):
                instr,cmd = st[0],st[1]
                why = st[2] if len(st)>2 else ""
                out.append(f"{i}. {instr}")
                if cmd: out+=["","   ```bash",f"   {cmd}","   ```",""]
                if why: out+=[f"   > *Why this step:* {why}",""]
            out.append("")
        elif kind=="code": out+=["```bash",rest[0],"```",""]
        elif kind=="note": out+=[f"> **Note:** {rest[0]}",""]
        elif kind=="rule": out+=["---",""]
        elif kind=="table":
            hdrs,rows=rest[0],rest[1]
            out.append("| "+" | ".join(hdrs)+" |")
            out.append("|"+"|".join(["---"]*len(hdrs))+"|")
            for r in rows: out.append("| "+" | ".join(str(c) for c in r)+" |")
            out.append("")
        elif kind=="image":
            # the mirror lives in courseware/ alongside the DOCX, so assets/ is relative
            out+=[f"![{rest[1]}](assets/{rest[0]})","",f"*{rest[1]}*",""]
        elif kind=="dl":
            for term,defn in rest[0]: out.append(f"- **{term}** — {defn}")
            out.append("")
    return "\n".join(out)

MD_OUT=os.path.join(REPO,"courseware",f"LG-{C.SHORT_TITLE}.md")
with open(MD_OUT,"w") as f: f.write(render_md())
print("Saved",MD_OUT)

# ---------------- render DOCX ----------------
BRAND=RGBColor(0x1F,0x6F,0xEB); DARK=RGBColor(0x11,0x18,0x27); GREY=RGBColor(0x55,0x5B,0x66)
INKCODE=RGBColor(0x0B,0x30,0x60); HEADER_FILL="1F6FEB"; TOPIC_FILL="E8F0FE"
doc=Document()
normal=doc.styles["Normal"]; normal.font.name="Arial"; normal.font.size=Pt(11)
prodoc.style_headings(doc)
prodoc.add_cover_page(doc,"LEARNER GUIDE",C.TITLE,C.VERSION.lstrip("v"),
                      org_logo=os.path.join(ASSETS,"tertiary-infotech-logo.png"),
                      course_logo=os.path.join(ASSETS,"n8n-logo.png"), course_code=C.COURSE_CODE)
prodoc.add_version_control(doc, VC_ROWS)
prodoc.add_toc(doc)

def code_para(text):
    for line in text.split("\n"):
        para=doc.add_paragraph()
        r=para.add_run(line); r.font.name="Consolas"; r.font.size=Pt(9.5); r.font.color.rgb=INKCODE

def add_table(headers,rows):
    tb=doc.add_table(rows=0,cols=len(headers)); tb.style="Table Grid"
    hdr=tb.add_row().cells
    for i,h in enumerate(headers):
        c=hdr[i]; c.text=""; r=c.paragraphs[0].add_run(h); r.bold=True; r.font.size=Pt(9.5)
        r.font.color.rgb=RGBColor(0xFF,0xFF,0xFF); prodoc._shade_cell(c,HEADER_FILL)
    for row in rows:
        cells=tb.add_row().cells
        for i,v in enumerate(row):
            cells[i].text=""; rr=cells[i].paragraphs[0].add_run(str(v)); rr.font.size=Pt(9.5)
            if i==0 and len(headers)>1: rr.bold=True
    doc.add_paragraph("")

def add_image(fn,caption):
    path=os.path.join(CWASSETS,fn)
    if not os.path.exists(path): return
    doc.add_picture(path,width=Inches(6.2))
    doc.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
    para=doc.add_paragraph(); para.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=para.add_run(caption); r.italic=True; r.font.size=Pt(9); r.font.color.rgb=GREY

for kind,*rest in B:
    if kind=="h1": doc.add_heading(rest[0],level=1)
    elif kind=="h2": doc.add_heading(rest[0],level=2)
    elif kind=="h3":
        para=doc.add_paragraph(); r=para.add_run(rest[0]); r.bold=True; r.font.size=Pt(11); r.font.color.rgb=BRAND
    elif kind=="p": doc.add_paragraph(rest[0])
    elif kind=="term":
        para=doc.add_paragraph(style="List Bullet")
        r=para.add_run(rest[0]+" — "); r.bold=True; para.add_run(rest[1])
    elif kind=="bullets":
        for x in rest[0]: doc.add_paragraph(x,style="List Bullet")
    elif kind=="steps":
        for i,st in enumerate(rest[0],1):
            instr,cmd = st[0],st[1]
            why = st[2] if len(st)>2 else ""
            para=doc.add_paragraph(style="List Number"); para.add_run(instr)
            if cmd: code_para(cmd)
            if why:
                wp=doc.add_paragraph(); wp.paragraph_format.left_indent=Inches(0.5)
                r=wp.add_run("Why this step: "); r.bold=True; r.italic=True
                r.font.size=Pt(9.5); r.font.color.rgb=RGBColor(0xB4,0x76,0x0B)
                r2=wp.add_run(why); r2.italic=True; r2.font.size=Pt(9.5); r2.font.color.rgb=GREY
    elif kind=="code": code_para(rest[0])
    elif kind=="note":
        para=doc.add_paragraph(); r=para.add_run("Note: "); r.bold=True; r.font.color.rgb=BRAND
        para.add_run(rest[0]).font.size=Pt(10)
    elif kind=="rule": doc.add_paragraph("")
    elif kind=="table": add_table(rest[0],rest[1])
    elif kind=="image": add_image(rest[0],rest[1])
    elif kind=="dl":
        for term,defn in rest[0]:
            para=doc.add_paragraph(style="List Bullet")
            r=para.add_run(term+" — "); r.bold=True; para.add_run(defn)

prodoc.add_page_numbers(doc)
prodoc.enable_update_fields(doc)
DOCX_OUT=os.path.join(REPO,"courseware",f"LG-{C.SHORT_TITLE}.docx")
doc.save(DOCX_OUT)
print("Saved",DOCX_OUT)
