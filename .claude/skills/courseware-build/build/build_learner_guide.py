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
 (C.VERSION.lstrip("v"), C.VERSION_DATE,
  """Added a screenshot of each lab's application — the four lab websites with their chat widgets open, plus the Lab 1 n8n canvas and sample flyer — to the slide deck and the Learner Guide.""", C.TRAINER),
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

# ---------------- foundation concepts ----------------
h1("Foundation — Agentic AI in Business Process Automation")
h3("The evolution of AI")
p("Artificial Intelligence began in the 1950s with Turing's test and rule-based symbolic systems. "
  "Machine Learning in the 1990s shifted the field from hand-written rules to learning patterns from "
  "data. Deep Learning in the 2000s added neural networks trained on large datasets. The 2017 "
  "Transformer architecture and its attention mechanism produced the Generative AI of the 2020s. "
  "Agentic AI, from around 2024, is the current step: models given goals, tools and memory, which "
  "plan and act rather than answer once.")
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
h3("From RPA to Agentic Process Automation")
p("Robotic Process Automation (RPA) follows a rigid path that a person constructs by hand — every "
  "branch is wired in advance, and anything unforeseen breaks it. Agentic Process Automation (APA) "
  "lets an agent orchestrate the workflow, so it can handle both rigid and flexible tasks.")
image("rpa-to-apa.png",
      "RPA constructs the workflow manually and can only handle rigid tasks; APA orchestrates it "
      "automatically and handles flexible ones too.")
h3("Business value")
bullets([
 "Free people from repetitive administrative work — scheduling, form processing, data entry, report generation and email routing.",
 "Shift human effort to judgement, relationships and strategy.",
 "React to events in real time — a form submission, a payment, a customer message.",
 "Operate around the clock, with the same care at 2am as at 2pm.",
 "Reduce human error by applying the same rules to every case and logging every decision.",
 "Scale volume without proportional headcount.",
])
h3("Where agent platforms sit")
table(["Tier","Characteristics","Examples"],[
 ["No-code","Fully visual; fastest to a working agent; least control","AgentX and similar chatbot builders"],
 ["Low-code","Visual canvas plus code nodes; 400+ integrations; self-host or cloud","n8n — this course's platform"],
 ["Full-code","SDKs and frameworks; maximum control; needs engineering effort","LangChain and agent SDKs"],
])
rule()

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

LAB_FLOW_IMAGES = {
 1: [("flow-lab1.png","Lab 1 — Form Trigger to Gmail.")],
 2: [("flow-lab2.png","Lab 2 — webhook, agent and its three Google Sheets / Gmail tools.")],
 3: [("flow-lab3.png","Lab 3 — chat webhook, agent with memory, reply.")],
 4: [("flow-lab4.png","Lab 4 — the agent drafts (top row); a human approves or declines (bottom row).")],
 5: [("flow-lab5-ingest.png","Lab 5 — ingestion: list, download, split, embed and store the brochures."),
     ("flow-lab5-agent.png","Lab 5 — answering: retrieve the nearest brochures, then answer from them.")],
}

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
        p(a["desc"])
        h3("What you'll build")
        p(a["build"]+f"   (Tools: {a['services']}.)")
        for fn,cap in a.get("site",[]):
            image(fn,cap)
        for fn,cap in LAB_FLOW_IMAGES.get(a["num"],[]):
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
