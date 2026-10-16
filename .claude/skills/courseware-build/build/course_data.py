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
VERSION      = "v2.3"
VERSION_DATE = "16 October 2026"
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
         subtitle="Why agentic AI · Workflow first · Triggers & actions · LLM agents · Webhooks",
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

# ------------------------------------------------------------------ Topic 1 demo
# Demo prompt for AI-assisted workflow creation — used by the deck AND the Learner Guide.
DEMO_PROMPT=[
 "Create a workflow for a social media marketing campaign:",
 "1. Start from a form where I enter a campaign topic.",
 "2. Research the topic on the web and summarise 3 key points.",
 "3. Draft a LinkedIn post under 150 words from the research.",
 "4. Email me the draft and wait for my approval before posting.",
 "5. If approved, schedule the post for 9am the next weekday;",
 "    if rejected, log my feedback in a Google Sheet.",
 "Use Gateway credits for the AI model. Ask me before publishing."]

# ------------------------------------------------------------------ Topic 2 demo (before Lab 3)
# Telegram HR Policy Agent — labs/lab3-chatbot-webhook/Lab 3 Demo - Telegram HR Policy Agent.json.
# Used by the deck AND the Learner Guide. Each step is
# (short text for the deck's numbered strip, full instruction for the guide, why it matters).
TELEGRAM_DEMO = dict(
    file="Lab 3 Demo - Telegram HR Policy Agent.json",
    flow=[("Telegram Trigger", "an employee messages the bot"),
          ("HR Agent — Ava", "HR policies + memory"),
          ("Chat model", "Gateway credits, no API key"),
          ("Reply on Telegram", "back to the same chat")],
    flow_shot=dict(img="n8n-flow-telegram-demo.png", title="Demo: The Workflow n8n Assistant Builds",
        intro="Your canvas should look like this: trigger, agent, reply — with the chat model and memory hanging under the agent.",
        cards=[("BLUE","Telegram Trigger","Updates: message — every message sent to the bot starts one execution."),
               ("VIOLET","HR Agent","Ava's role, rules and sample HR policies live in the system instruction n8n Assistant wrote."),
               ("TEAL","Model and memory","Chat model on Gateway credits; memory keeps each employee's conversation, keyed on the Telegram chat ID."),
               ("AMBER","Reply out","Reply on Telegram sends back to the chat ID the trigger received, so the reply lands in the same chat.")],
        takeaway="Shown: the reference solution, which has no memory. Yours has a memory node — the prompt asked for one."),
    chat_shot=dict(img="telegram-chat-demo.png", title="Demo: Chatting with Ava on Telegram",
        bullets=["/start opens the chat — Ava introduces herself exactly as her system message tells her to.",
                 "Ask how many days of leave you get: the answer quotes the policy — 14, 18 or 21 days by length of service.",
                 "Ask a follow-up — memory keeps the context. Then ask about a colleague's salary: Ava must refer you to HR.",
                 "Every message is one workflow run — open Executions in n8n to watch it happen."],
        takeaway="The bot is only as safe as its system message. Lab 3 adds a contact gate and a refusal rule, behind a website."),
    botfather=[
        ("Open Telegram and search for BotFather (blue checkmark)",
         "Open the Telegram app and search for the verified account named BotFather (look for the blue checkmark).",
         "BotFather is Telegram's own bot for creating bots. Impostors exist, so check for the blue checkmark."),
        ("Start a chat and send /newbot",
         "Start a chat and send the command /newbot.",
         "Every Telegram bot, including the ones big companies run, starts with this one command."),
        ("Type a display name, e.g. My Free Helper Bot",
         "Type a display name for your bot (e.g., My Free Helper Bot).",
         "The display name is what people see in their chat list. It can contain spaces and can be changed later with /setname."),
        ("Choose a unique username ending in bot, e.g. my_free_helper_bot",
         "Choose a unique username that ends in bot (e.g., my_free_helper_bot).",
         "The username is the bot's permanent address — t.me/<username> — and must be unique across all of Telegram. If it is taken, try another."),
        ("Copy the HTTP API token BotFather sends back",
         "Copy the HTTP API token that BotFather replies with (it looks like 123456789:AAH…). You will paste it into n8n in Step 3.",
         "The token is the bot's password. Anyone holding it controls the bot; if it leaks, send /revoke to BotFather."),
    ],
    # Step 2 — learners build the workflow themselves with n8n Assistant (AI Assistant).
    prompt=[
        "Create a 3-node workflow:",
        "•  A user posts a message to a Telegram bot.",
        "•  Telegram sends the data to an HR agent.",
        "•  The HR agent responds to the user on the company HR policies. Create a system instruction for the HR agent with sample company policies in it. The HR agent has a memory.",
        "•  Respond to Telegram.",
    ],
    review=["Review the plan before it builds",
            "Read the system instruction it wrote — edit the sample policies if you like",
            "Check a memory node is attached to the HR agent",
            "Stuck? Import the reference solution instead"],
    connect=[
        ("Telegram Trigger → Credential → Create new → paste the token",
         "Open the Telegram Trigger node, choose Credential → Create new credential, paste the BotFather token as the Access Token and save.",
         "The trigger listens for messages with this credential."),
        ("Telegram reply node → select the same credential",
         "Open the Telegram node that sends the reply and select the same Telegram credential.",
         "Both Telegram nodes share one credential — one listens, the other answers."),
        ("Chat model → Use Gateway credits",
         "Open the chat model under the HR agent and choose Use Gateway credits as its credential.",
         "No OpenAI account or API key is needed on n8n Cloud — the same free credits used in Lab 2."),
        ("Publish — n8n registers its webhook with Telegram",
         "Click Publish. n8n registers the workflow's Production webhook with Telegram, so every message to the bot now starts the workflow.",
         "A Telegram bot has ONE webhook at a time. Testing in the editor swaps in the Test URL, so publish again when you are done."),
        ("Open t.me/<username>, tap Start, ask about annual leave",
         "Open t.me/<your bot username>, tap Start and ask: How many days of annual leave do I get? Ask a follow-up, then ask about a colleague's salary.",
         "The follow-up proves the memory works; the salary question must be referred to HR — the guardrail in the system instruction."),
    ],
)
