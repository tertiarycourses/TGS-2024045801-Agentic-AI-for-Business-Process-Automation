"""
SINGLE SOURCE OF TRUTH — Agentic AI for Business Process Automation (TGS-2024045801).

Every artifact (PPT, LP, LG, LG.md) is generated from this file plus
data_domain1.py … data_domain3.py so they stay 100% aligned.

Guiding principle: the course material must be 100% aligned to the WSQ TSC
(AER-TEM-3026-1.1) so learners who take the course can pass the assessment.
"""

# ------------------------------------------------------------------ metadata
TITLE        = "Agentic AI for Business Process Automation"
SHORT_TITLE  = "Agentic AI for Business Process Automation"   # used in output filenames
COURSE_CODE  = "TGS-2024045801"
VERSION      = "v2.0"
VERSION_DATE = "8 August 2026"
ORG          = "Tertiary Infotech Academy Pte Ltd"
UEN          = "UEN: 201200696W"
TRAINER      = "Dr. Alfred Ang"
DAYS         = 2
HOURS_PER_DAY = 8          # 16 training hours over 2 days
TRAINING_HOURS = 16

# ------------------------------------------------------------------ Skills Framework
TSC_TITLE = "Artificial Intelligence Application"
TSC_CODE  = "AER-TEM-3026-1.1"

TSC_ABILITIES = [
    ("A1", "Implement AI applications in collaboration with technology service providers"),
    ("A2", "Deploy AI workflows according to plan"),
    ("A3", "Identify and report any issues with the AI applications and data collected"),
]

TSC_KNOWLEDGE = [
    ("K1", "Background and basics of AI"),
    ("K2", "Fundamental concepts and methods of statistics and programming for data science"),
    ("K3", "Mathematics and computing theories"),
    ("K4", "Machine learning techniques and applications"),
    ("K5", "Principles of data management"),
    ("K6", "Software development methodologies"),
    ("K7", "Types of AI applications"),
    ("K8", "AI implementation procedures"),
]

# ------------------------------------------------------------------ outcomes
LEARNING_OUTCOMES = [
    "LO1: Explain what n8n and AI agents are, and build automated workflows using triggers and actions.",
    "LO2: Implement AI agent applications that are triggered by webhooks and integrated with business systems.",
    "LO3: Design agentic chatbot workflows that operate safely within business and regulatory constraints.",
    "LO4: Apply human-in-the-loop approval so that sensitive actions are authorised by a person.",
    "LO5: Deploy Retrieval-Augmented Generation (RAG) to ground an agent in an organisation's own documents.",
]

# ------------------------------------------------------------------ topics
# num, code, title, subtitle, concept bullets for the section
TOPICS = [
    dict(num=1, code="01",
         title="Overview of n8n and AI Agents",
         subtitle="Workflow automation · Triggers & actions · LLM agents · Webhooks",
         weighting="LO1 · LO2",
         concepts=[
            ("What is n8n", "A fair-code workflow automation platform: a visual canvas where nodes are wired together to move data between 400+ apps, with no code required."),
            ("Triggers and actions", "A trigger decides WHEN a workflow runs — form, webhook, schedule, chat. Actions are what happens next — send mail, write a row, call an API."),
            ("What is an AI agent", "An LLM given a goal, a set of tools and memory. It decides which tool to call and when, instead of following a fixed branch you wired by hand."),
            ("Agentic vs generative AI", "Generative AI produces content when asked. Agentic AI pursues a goal — it plans, acts on the world through tools, observes the result and adapts."),
            ("Webhooks as the front door", "A webhook is a URL any external system can POST to. It is what lets your own website, app or CRM start an n8n agent workflow."),
            ("Structured output", "Forcing the agent to return named fields (decision, reason, flags) instead of prose is what lets the rest of the workflow branch, log and act on the answer."),
         ]),
    dict(num=2, code="02",
         title="Agentic Chatbot and Human in the Loop",
         subtitle="Agentic workflows · Chatbots on webhooks · Approval gates · Accountability",
         weighting="LO3 · LO4",
         concepts=[
            ("What is an agentic workflow", "A workflow where an LLM makes the routing decisions. You supply the goal, the guardrails and the tools; the agent supplies the judgement."),
            ("System instructions", "The agent's role, scope, prohibitions and routing rules. In a regulated setting this is a compliance control, not a prompt-engineering flourish."),
            ("Memory", "Keyed on a session ID so a follow-up question keeps context — and so two users never see each other's conversation."),
            ("Guardrails in the prompt", "Explicit prohibitions ('never recommend a product, never guarantee a return') do more compliance work than any amount of clever wording."),
            ("Human in the loop", "The workflow pauses on a Send-and-Wait node until a named person clicks Approve or Decline. Nothing reaches the customer unauthorised."),
            ("Accountability trail", "Separate logs for what the agent proposed and what a human authorised. The audit question is not what the machine decided, but who is answerable."),
         ]),
    dict(num=3, code="03",
         title="Retrieval-Augmented Generation (RAG)",
         subtitle="Tokenization · Embeddings · Vector stores · Grounded answers",
         weighting="LO5",
         concepts=[
            ("What is RAG", "Retrieve the few documents that resemble the question, then let the LLM answer from those. The model reads what matters instead of everything."),
            ("Why not just paste everything", "Prompts have limits and costs. Twenty brochures fit; two hundred do not, and the model starts ignoring the middle of a long prompt."),
            ("Tokenization and embeddings", "Text is split into tokens, then an embedding model turns each chunk into a vector so that text about similar things lands close together."),
            ("Vector stores", "A database that finds nearest neighbours fast. n8n's Simple Vector Store needs no setup — and is wiped whenever n8n restarts."),
            ("Chunking is the biggest lever", "The right chunk is the smallest piece of text that still answers a question on its own. Split a brochure and the fee is separated from the course name."),
            ("Grounding against hallucination", "Instruct the agent to answer only from what the tool returned, and to say 'I don't have that' otherwise. An ungrounded model invents a plausible, wrong fee."),
         ]),
]

# ------------------------------------------------------------------ day themes
DAY_THEMES = {
    1: "n8n, AI Agents and Agentic Chatbots",
    2: "Human in the Loop, RAG and Assessment",
}

# ------------------------------------------------------------------ daily timing
# SINGLE SOURCE for the timing text. The deck's Lesson Plan slide and the LP's
# Course Information table both render these, so they can never contradict.
DAY_TIMES = {
    1: "9:30 am – 6:30 pm",
    2: "9:30 am – 6:30 pm instruction, assessment to 8:45 pm",
}
TIMING_NOTE = ("Each day is 8 instructional hours: a 1-hour lunch is excluded, and the two "
               "15-minute tea breaks are counted within the instructional time")

def timing_summary():
    """One-line timing description used on the deck's Lesson Plan slide."""
    return f"Day 1 {DAY_TIMES[1]} · Day 2 {DAY_TIMES[2]}"

# ------------------------------------------------------------------ assessment
ASSESSMENT = dict(
    written="Written Assessment (WA) — Short-Answer Questions (SAQ), 1 hour, open book.",
    practical="Practical Performance (PP) — hands-on n8n build tasks, 1 hour, open book.",
    note="A minimum of 75% attendance is required to be eligible for assessment and funding.",
)
