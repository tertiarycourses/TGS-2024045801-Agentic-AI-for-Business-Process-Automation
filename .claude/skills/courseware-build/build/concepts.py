"""Teaching-concept content for the slide deck AND the Learner Guide.

SINGLE SOURCE for the conceptual material, so a concept explained on a slide is
explained in the Learner Guide in the same words. Slides render these as visual
components (cards, chevron flows, comparison panels, tables); the Learner Guide
renders the same structures as prose sections and tables.

Structure of a concept block:
    key      stable identifier, referenced by build_slides.py and build_learner_guide.py
    title    the slide/section heading
    intro    one-line framing sentence under the heading
    kind     how to render it: "cards" | "chev+cards" | "panels" | "table" | "image"
    ...      payload keys depending on kind
    takeaway the one-line band at the foot of the slide (also the LG's bold summary)
"""

# ---------------------------------------------------------------- TOPIC 1: n8n
WHAT_IS_N8N = dict(
    key="what_is_n8n", title="What Is n8n?",
    intro="A workflow-first agentic AI platform: the workflow owns the path, and AI and AI Agent nodes sit inside it.",
    kind="cards", cols=3,
    cards=[
        ("BLUE", "Build visually",
         "Drag nodes onto a canvas and wire them together. 400+ app integrations, plus HTTP and Code nodes when no integration exists."),
        ("TEAL", "Run anywhere",
         "Free cloud trial at n8n.io, or self-host with Docker. Webhooks, schedules and chat triggers work the same in both."),
        ("VIOLET", "AI-native",
         "AI Agent and LangChain nodes are built in — attach any LLM (Gemini, OpenAI, Claude), memory, tools and vector stores."),
    ],
    takeaway="n8n is workflow-first agentic AI — deterministic workflows with AI and agents built in, on one canvas.",
)

WORKFLOW_SHAPE = dict(
    key="workflow_shape", title="Every Workflow Is the Same Shape",
    intro="Trigger first, then actions in order, with data flowing left to right. Only the nodes change.",
    kind="chev+cards",
    chevrons=[("TRIGGER", "what starts it"), ("ACTION", "do the work"),
              ("ACTION", "do more work"), ("OUTPUT", "reply, store or notify")],
    cards=[
        ("BLUE", "One trigger",
         "A workflow has exactly one entry point. Change the trigger and you have a different workflow — the actions may not change at all."),
        ("TEAL", "Actions are ordered",
         "Each action runs after the one before it, and can read the output of every node that ran before it."),
        ("VIOLET", "Data flows as JSON",
         "Every node passes a list of JSON items to the next — the same structure in every lab of this course."),
    ], cols=3,
    takeaway="Trigger, actions, output. Learn this once in Lab 1 and every later lab is a variation.",
)

TRIGGER_NODES = dict(
    key="trigger_nodes", title="Trigger Nodes — What Is Allowed to Start a Workflow",
    intro="The trigger you choose is a statement about who or what may start the process.",
    kind="cards", cols=3,
    cards=[
        ("BLUE", "Manual Trigger",
         "Click Execute workflow. For building and testing, and for one-off jobs such as the Lab 5 ingestion run."),
        ("TEAL", "Schedule Trigger",
         "A clock starts the workflow — an interval or a cron expression. Nightly reports, reminders and syncs."),
        ("VIOLET", "Form Trigger",
         "n8n hosts a web form for you and each submission starts a run. This is Lab 1's front door."),
        ("AMBER", "Webhook",
         "An external system calls a URL you expose. Your own website, app or CRM — Labs 2, 3, 4 and 5."),
        ("GREEN", "Chat Trigger",
         "Each message in n8n's built-in chat window starts a run — the quickest way to talk to an agent while building."),
        ("RED", "App & Email Triggers",
         "On new Gmail, new Sheets row, new Drive file. React to changes in the apps you already use."),
    ],
    takeaway="Pick the trigger by asking: who or what should be allowed to start this process?",
)

TRIGGERS_IN_COURSE = dict(
    key="triggers_in_course", title="Triggers Used in This Course",
    intro="Every lab's trigger, and why that trigger is the right front door for that business process.",
    kind="table",
    widths=[3.0, 3.2, 5.43],
    header=["Trigger", "Where", "Why it fits"],
    rows=[
        ["Form Trigger", "Lab 1", "A visitor's event sign-up must start the workflow"],
        ["Webhook — POST", "Labs 2, 3, 4, 5", "A website sends JSON and waits for the agent's reply"],
        ["Manual Trigger", "Lab 5 ingestion", "A human loads the documents once, by hand"],
        ["Schedule Trigger", "Not used in class", "Nightly reports and reminders — same pattern, a clock instead"],
        ["Chat Trigger", "Optional while building", "Talk to an agent without building a website first"],
    ],
    takeaway="Swap the front door and keep the workflow — the trigger is the only part that has to change.",
)

DATA_NODES = dict(
    key="data_nodes", title="Data-Processing Nodes — The Workhorses",
    intro="Between the trigger and the output, these nodes shape, route and transform the data.",
    kind="cards", cols=4,
    cards=[
        ("BLUE", "Edit Fields (Set)",
         "Add, rename or reshape fields — the node you reach for first when the data is the wrong shape. Used in Labs 2 and 4."),
        ("TEAL", "IF / Switch",
         "Branch the workflow. IF gives a true and a false path; Switch gives one path per case. Lab 4 routes Approve vs Decline."),
        ("VIOLET", "Filter",
         "Let only the matching items continue and drop the rest of the list."),
        ("AMBER", "Merge",
         "Combine two branches — append the rows, match them by key, or choose one side."),
        ("GREEN", "Split Out / Aggregate",
         "Turn one item holding a list into many items — and back again."),
        ("RED", "Code",
         "JavaScript or Python for the 5% a built-in node cannot do. Lab 3 uses it to normalise the chat message."),
        ("BLUE", "Loop / Wait",
         "Process items in batches, or pause a workflow for a period of time or an event."),
        ("TEAL", "HTTP Request",
         "Call any API on the internet — the universal escape hatch when no integration exists."),
    ],
    takeaway="Most workflows are: trigger → reshape (Set) → decide (IF) → act (app node). Reach for Code last.",
)

STORAGE_NODES = dict(
    key="storage_nodes", title="Where the Data Goes — Storage & App Actions",
    intro="Action nodes that write the result somewhere useful, or send it to a person.",
    kind="cards", cols=2,
    cards=[
        ("BLUE", "Google Sheets",
         "A real spreadsheet you keep, connected with OAuth2. Append Row is the workhorse — Labs 2 and 4 log every decision here."),
        ("TEAL", "Gmail / Outlook",
         "Send a message — and in Lab 4, Send and Wait for Response, which turns email into an approval gate."),
        ("VIOLET", "Vector Store",
         "Store embeddings for RAG. In-memory for class, Pinecone / Supabase / Qdrant for production — Lab 5."),
        ("AMBER", "Respond to Webhook",
         "Return data to whoever called the webhook, so a web page can render the agent's answer."),
    ],
    takeaway="Anything you must keep goes to external storage — an in-memory store vanishes when n8n restarts.",
)

JSON_EXPRESSIONS = dict(
    key="json_expressions", title="JSON and Expressions — How Data Moves",
    intro="Every node passes a list of items; each item is a JSON object of key/value pairs.",
    kind="json",
    bullets=[
        "JSON (JavaScript Object Notation) is a simple text format for data.",
        "Values can be text, numbers, true/false, lists [ ] or nested objects { }.",
        "Most APIs send and receive JSON — and so does every n8n node.",
        "Click any node to inspect the JSON going in and coming out.",
    ],
    code_title="ONE FORM SUBMISSION AS JSON",
    code=['{', '  "Name": "Alice Tan",', '  "Email": "alice@corp.com",',
          '  "Phone": "91234567",', '  "Message": "Please reserve 2 seats"', '}'],
    takeaway='Read any value later with an expression:  {{ $json.Name }}  →  "Alice Tan"',
)

TEST_VS_PROD_EXEC = dict(
    key="test_vs_prod_exec", title="Test vs Production Executions",
    intro="The same workflow runs in two modes — always know which one you are looking at.",
    kind="panels",
    left=("TEST — in the editor", "BLUE", [
        "Click Execute workflow to run it once.",
        "The data is shown live on the canvas, node by node.",
        "Pin a node's output to freeze it while you build downstream.",
        "Perfect while building — nothing needs to be Active.",
    ]),
    right=("PRODUCTION — Active toggle ON", "VIOLET", [
        "Runs automatically whenever the trigger fires.",
        "Nothing appears on the canvas — runs are logged under Executions.",
        "Every run records status, timing and the full data at each node.",
        "This is what your users actually experience.",
    ]),
    takeaway="The Executions list is the honest account of what happened — debug from there, not from memory.",
)

CREDENTIALS = dict(
    key="credentials", title="Credentials — Connect Your Accounts Once",
    intro="Nodes reference credentials by NAME. Set each one up once under Credentials → Add credential.",
    kind="cards", cols=2,
    cards=[
        ("BLUE", "Gmail (OAuth2)",
         "Sign in with Google and grant access. Used from Lab 1 onward for sending mail and for the Lab 4 approval gate."),
        ("TEAL", "Google Gemini (API key)",
         "The LLM behind every agent in this course, and the embedding model in Lab 5."),
        ("VIOLET", "Google Sheets (OAuth2)",
         "The audit log in Labs 2 and 4 — customer records, decisions, drafts and approvals."),
        ("AMBER", "Google Drive (OAuth2)",
         "The brochure folder that Lab 5's ingestion workflow reads from."),
    ],
    takeaway="Imported workflows carry credential NAMES, not secrets — always re-select your own after importing.",
)

# ---------------------------------------------------------------- TOPIC 1/2: AGENTS
GEN_VS_AGENTIC = dict(
    key="gen_vs_agentic", title="Generative AI vs Agentic AI",
    intro="The difference is not how clever the model is — it is whether it can act.",
    kind="panels",
    left=("GENERATIVE AI — answers", "BLUE", [
        "You ask; it writes one answer.",
        "No access to your systems, and no actions.",
        "Quality depends on what you paste into the prompt.",
        "Stops the moment the answer is produced.",
        "Example: draft me an email to this customer.",
    ]),
    right=("AGENTIC AI — acts", "VIOLET", [
        "Works toward a goal, not just one reply.",
        "Calls tools: looks up data, calls APIs, writes records.",
        "Holds a conversation with memory.",
        "Continues until the goal is met.",
        "Example: read the enquiry, check the CRM, reply and log it.",
    ]),
    takeaway="Generative AI produces content. Agentic AI decides and does — which is exactly why it needs governance.",
)

AGENT_COMPONENTS = dict(
    key="agent_components", title="Components of an AI Agent",
    intro="Four parts around one hub: the AI Agent node wires them together, and every agent in this course is exactly these four.",
    kind="hub",
    hub=("THE AI AGENT", "plans · decides · calls tools"),
    parts=[
        ("BLUE",   "MODEL",
         "The LLM 'brain' — interprets language, reasons and chooses the next step. Google Gemini in this course."),
        ("TEAL",   "MEMORY",
         "Keeps the conversation so follow-up questions still make sense. Keyed on a session ID, per visitor."),
        ("AMBER",  "TOOLS",
         "The abilities it may use: look up a Sheets row, search a vector store, send an email, call an API."),
        ("GREEN",  "INSTRUCTIONS",
         "The system message — identity, scope, rules and refusals. Always in force, on every single turn."),
    ],
    takeaway="Model + Memory + Tools + Instructions. Change any one of the four and you have a different agent.",
)

MODEL_PROVIDERS = dict(
    key="model_providers", title="The Model — Popular LLM Providers",
    intro="Any chat model plugs into the same AI Agent node — swap the brain and keep the agent.",
    kind="table",
    widths=[3.0, 4.4, 4.23],
    header=["Provider", "Models", "Notes"],
    rows=[
        ["Google", "Gemini 2.5 Flash / Pro", "Course default — also supplies the embeddings in Lab 5"],
        ["OpenAI", "gpt-4.1, gpt-4.1-mini, gpt-4o", "Widely used; mini tier is cheap and fast"],
        ["Anthropic", "Claude (Opus, Sonnet, Haiku)", "Strong reasoning and long context"],
        ["Meta", "Llama 3.x", "Open weights — can be self-hosted"],
        ["Mistral", "Mistral / Mixtral", "Open weights — a European option"],
    ],
    takeaway="Pick by task: small fast models for classification and guardrails, larger models for reasoning.",
)

MODEL_PARAMS = dict(
    key="model_params", title="Model Parameters — Temperature and Friends",
    intro="Settings on the chat-model node shape HOW the model answers. The most important by far is temperature.",
    kind="cards2",
    cards=[
        ("BLUE", "Temperature 0 – 0.3",
         "Deterministic and repeatable. Use for classification, compliance decisions and data extraction — automation that must give the same answer twice."),
        ("TEAL", "Temperature ≈ 0.7",
         "Balanced. Natural-sounding conversation with some variety — the usual default for a customer-facing assistant."),
        ("AMBER", "Temperature 1.0 +",
         "Creative and surprising. Marketing copy and brainstorming — never for a decision that must be defended."),
    ],
    cards2=[
        ("VIOLET", "Top-p",
         "An alternative sampling control that limits the model to the most probable tokens. Tune temperature OR top-p, never both."),
        ("GREEN", "Max tokens",
         "Caps the length of the reply. Protects your cost and keeps chat answers short enough to read."),
        ("RED", "Frequency / presence penalty",
         "Discourage repetition and nudge the model onto new topics — useful for long generations, rarely for automation."),
    ],
    takeaway="For business automation keep the temperature LOW — Lab 3 uses 0.2 so the same question is refused the same way every time.",
)

MEMORY_CONCEPT = dict(
    key="memory_concept", title="Memory — Why the Agent Remembers",
    intro="Without memory every message is from a stranger; with it, 'what about next month?' still makes sense.",
    kind="chev+cards",
    chevrons=[("Msg 1: 'What courses do you run?'", "agent answers from its tools"),
              ("Stored in memory", "keyed by session ID"),
              ("Msg 2: 'How much is that one?'", "agent knows which course"),
              ("Window slides", "only the last N turns are kept")],
    cards=[
        ("BLUE", "Window buffer memory",
         "Keeps the last N exchanges of THIS conversation. It is n8n's default and it is what Lab 3's chatbot uses."),
        ("TEAL", "Session key",
         "Memory is per session ID, so two visitors on the same website never see each other's conversation."),
        ("RED", "Sometimes you want NO memory",
         "Lab 2's onboarding agent deliberately has none — one applicant's details must never influence the next decision."),
    ], cols=3,
    takeaway="Memory is conversation context, NOT long-term knowledge. Facts belong in tools and documents (RAG).",
)

TOOLS_CONCEPT = dict(
    key="tools_concept", title="Tools — What the Agent May Do",
    intro="Attach tools to the agent's Tool input. The model decides WHEN to call one, based on the description you write.",
    kind="cards", cols=2,
    cards=[
        ("BLUE", "Google Sheets tool",
         "Look up or write structured records. Lab 2 attaches three: check for a duplicate, create the customer, send the confirmation."),
        ("TEAL", "Vector Store tool",
         "Retrieve document chunks for a grounded answer — the Query Data Tool in Lab 5."),
        ("VIOLET", "HTTP Request tool",
         "Call any external API in the middle of a conversation — prices, stock levels, a CRM record."),
        ("AMBER", "Sub-workflow tool",
         "Wrap an entire n8n workflow as one callable tool, so your own logic becomes something the agent can invoke."),
    ],
    takeaway="The tool DESCRIPTION is how the agent knows when to call it — write it for the model, not for a developer.",
)

INSTRUCTIONS_FOUR = dict(
    key="instructions_four", title="Instructions — The Four Parts That Constrain",
    intro="The system message is always in force. Every good agent instruction in this course states four things.",
    kind="cards", cols=2,
    cards=[
        ("BLUE", "Identity",
         "Who the agent is, and for whom. 'You are the onboarding assistant for Marina Trust Bank.' Narrow roles refuse far more reliably than general assistants."),
        ("GREEN", "Source rules",
         "Where answers may come from. 'Answer ONLY from the brochures returned by the tool — never from general knowledge.'"),
        ("RED", "Refusals",
         "What is out of bounds, stated explicitly. 'Never recommend a product, predict a return, or guarantee an outcome.'"),
        ("AMBER", "Escalation",
         "What to do at the boundary. 'If you are not sure, say so and offer a consultation with a licensed adviser.'"),
    ],
    takeaway="Vague instructions produce confident wrong answers — every rule you skip, the model improvises.",
)

GOOD_BAD_INSTRUCTIONS = dict(
    key="good_bad_instructions", title="Examples of Good and Bad Instructions",
    intro="The same chatbot, two system messages — one is testable, the other is a hope.",
    kind="goodbad",
    bad_title="✗  TOO VAGUE",
    bad_quote='"You are a helpful assistant. Answer the user\'s questions politely."',
    bad_notes=["No identity · no source rules · no refusals · no escalation.",
               "It will happily invent a course fee and guarantee an investment return — politely."],
    good_title="✓  CONSTRAINED AND TESTABLE",
    good_lines=[
        '"You are the enquiry assistant for Meridian Asset Management.',
        'Answer only questions about our services, fees and appointment booking.',
        'Use the brochure search tool for any factual question — never answer from general knowledge.',
        'Never recommend a product, predict a return, or guarantee an outcome.',
        'If you are not sure, say so and offer a call with a licensed adviser."',
    ],
    takeaway="Identity · source rules · refusals · escalation — you can test each line by trying to break it.",
)

MCP_CONCEPT = dict(
    key="mcp", title="MCP — Model Context Protocol",
    intro="An open standard that gives agents a common plug for tools and data, instead of one custom integration per pair.",
    kind="chev+cards",
    chevrons=[("AI Agent", "any MCP-capable client"), ("MCP Client", "speaks the protocol"),
              ("MCP Server", "exposes tools + data"), ("Your Systems", "databases, APIs, files")],
    cards=[
        ("RED", "Without MCP",
         "Every agent × every tool needs its own custom integration. N agents and M tools means N × M connectors to build and to maintain."),
        ("GREEN", "With MCP",
         "Build ONE MCP server per system and any MCP-capable agent can use it. N + M pieces, and the tools become reusable across agents."),
    ], cols=2, numbered=False,
    takeaway="MCP is like USB-C for AI tools — one connector, many devices.",
)

MCP_IN_N8N = dict(
    key="mcp_in_n8n", title="MCP in n8n",
    intro="n8n sits on both sides of the protocol — it can serve tools to other agents, and borrow tools for its own.",
    kind="panels",
    left=("MCP SERVER TRIGGER — n8n serves tools", "VIOLET", [
        "Expose your own n8n workflows AS tools over MCP.",
        "Claude, an IDE or another agent can then call your workflows directly.",
        "n8n becomes the tool layer for any MCP client.",
        "Secured with a bearer token on the server URL.",
    ]),
    right=("MCP CLIENT TOOL — n8n consumes tools", "BLUE", [
        "Attach an external MCP server to your n8n AI Agent.",
        "The agent gains all of that server's tools with no custom node.",
        "Mix MCP tools and native n8n tools freely on the same agent.",
        "Same agent loop — simply more reach.",
    ]),
    takeaway="Two directions, one protocol. Build the tool once and every agent you own can use it.",
)

STRUCTURED_OUTPUT = dict(
    key="structured_output", title="Structured Output — Making an Agent's Answer Usable",
    intro="By default an agent returns a paragraph of prose. Prose cannot be branched on, sorted, counted or coloured.",
    kind="cards", cols=2,
    cards=[
        ("BLUE", "Attach an Output Parser",
         "A Structured Output Parser forces named fields instead of free text — Labs 2 and 4 both use one."),
        ("TEAL", "Name the fields you will act on",
         "Lab 2 returns decision, reason and riskFlags. The website colours its result card from decision alone."),
        ("VIOLET", "Enumerate the allowed values",
         "APPROVED / REJECTED / REVIEW / DUPLICATE. A closed list is what makes an IF node reliable."),
        ("AMBER", "Everything downstream depends on it",
         "An IF node routes on it, a Sheets node logs it, and a queue is sorted by it. Prose supports none of that."),
    ],
    takeaway="If something downstream must act on the answer, make the answer a field — not a sentence.",
)

# ---------------------------------------------------------------- TOPIC: WEBHOOKS
WHAT_IS_WEBHOOK = dict(
    key="what_is_webhook", title="What Is a Webhook?",
    intro="A URL your workflow listens on. When the outside world calls it, your workflow runs — the reverse of you calling an API.",
    kind="chev+cards",
    chevrons=[("Event happens", "a visitor submits the form"),
              ("HTTP request to your URL", "the website POSTs JSON"),
              ("Workflow runs", "n8n receives the data as its input"),
              ("Respond to Webhook", "your reply returns to the caller")],
    cards=[
        ("BLUE", "Push, not pull",
         "No polling and no schedule — the caller notifies you the moment something happens."),
        ("TEAL", "Any caller",
         "Websites, payment providers, forms, CRMs, mobile apps — anything that can send an HTTP request."),
        ("VIOLET", "A paired node",
         "The Webhook node starts the workflow; Respond to Webhook sends the answer back on the same connection."),
    ], cols=3,
    takeaway="A webhook is the reverse of an API call — the outside world calls YOU when an event happens.",
)

WEBHOOK_VS_HTTP = dict(
    key="webhook_vs_http", title="Webhook vs HTTP Request — Which Way the Call Goes",
    intro="Both are plain HTTP. The only difference is who dials.",
    kind="panels",
    left=("WEBHOOK — inbound", "TEAL", [
        "An external service calls YOUR workflow.",
        "You react the moment the event happens.",
        "It is the TRIGGER — always the first node.",
        "Labs 2–5: the lab website calls your agent.",
    ]),
    right=("HTTP REQUEST — outbound", "BLUE", [
        "YOUR workflow calls an external service.",
        "You pull the data at a moment you choose.",
        "It is an ACTION inside the workflow.",
        "Use it to reach any API with no dedicated n8n node.",
    ]),
    takeaway="Same HTTP underneath — a webhook receives a call, an HTTP Request makes one.",
)

GET_VS_POST = dict(
    key="get_vs_post", title="HTTP Methods on a Webhook — GET vs POST",
    intro="The method is part of the contract with the caller: where the data rides, and what the call means.",
    kind="panels",
    left=("GET — read", "BLUE", [
        "The data rides in the URL query string:",
        "   ?email=alice@corp.com",
        "A browser can call it just by visiting the URL.",
        "Read it in n8n as {{ $json.query.email }}.",
        "Right for: a dashboard pulling data to display.",
    ]),
    right=("POST — send", "VIOLET", [
        "The data rides in the request body as JSON:",
        '   { "message": "How much is the course?" }',
        "This is what a web form or a chat widget sends.",
        "Read it in n8n as {{ $json.body.message }}.",
        "Right for: Labs 2–5, where the site submits data.",
    ]),
    takeaway="GET reads, POST sends. Set the method on the Webhook node — and the caller must match it exactly.",
)

TEST_VS_PROD_URL = dict(
    key="test_vs_prod_url", title="Webhook Test URL vs Production URL",
    intro="Every Webhook node gives you TWO URLs. They behave differently, and confusing them is the single most common webhook bug.",
    kind="panels",
    left=("TEST URL —  /webhook-test/…", "AMBER", [
        "Works only while you have clicked 'Listen for test event'.",
        "Handles exactly ONE call, then stops listening.",
        "The run appears live on the canvas — ideal for debugging.",
        "Dies the moment you leave the editor.",
    ]),
    right=("PRODUCTION URL —  /webhook/…", "GREEN", [
        "Requires the workflow to be toggled Active.",
        "Always on — every call starts a run.",
        "Runs are logged under Executions, not drawn on the canvas.",
        "This is the URL you give to a website, an app or a QR code.",
    ]),
    takeaway="Your website must call the PRODUCTION URL of an ACTIVE workflow — the Test URL is spent after one request.",
)

WEBHOOK_CONFIG = dict(
    key="webhook_config", title="Configuring the Webhook Node",
    intro="Four settings decide whether the browser's call actually succeeds.",
    kind="cards", cols=2,
    cards=[
        ("BLUE", "Method + Path",
         "GET or POST, and the path that ends your URL — for example POST /webhook/marina-trust-onboarding."),
        ("TEAL", "Allowed Origins (CORS)",
         "Browsers block cross-site calls unless you allow them. Set * in class so a local HTML page can call n8n; never leave * in production."),
        ("VIOLET", "Response mode",
         "Immediately (a bare acknowledgement), when the workflow finishes, or via a Respond to Webhook node — every lab here uses the last one."),
        ("AMBER", "Authentication",
         "None for a classroom demo; Basic, Header or JWT for anything real. A public URL is a public door, and every call costs you model tokens."),
    ],
    takeaway="'Failed to fetch' in the browser is almost always CORS or a dead Test URL — check those two first.",
)

# ---------------------------------------------------------------- TOPIC: HITL
HITL_LEVELS = dict(
    key="hitl_levels", title="Human In, On, and Out of the Loop",
    intro="Three levels of human oversight. The design question is which one this particular process deserves.",
    kind="cards", cols=3,
    cards=[
        ("GREEN", "Human IN the loop",
         "The workflow PAUSES and a named person must approve before the action happens. Nothing reaches the customer unauthorised. This is Lab 4."),
        ("AMBER", "Human ON the loop",
         "The agent acts immediately, but a person monitors and can intervene or reverse it. Suited to high volume and low individual risk."),
        ("RED", "Human OUT of the loop",
         "Fully autonomous. Acceptable only where an error is cheap, reversible and detectable — never where money or a regulator is involved."),
    ],
    takeaway="The question is never 'is the model good enough?' but 'what does one bad output cost, and who answers for it?'",
)

HITL_PATTERN = dict(
    key="hitl_pattern", title="How an Approval Suspends a Running Workflow",
    intro="A Send-and-Wait node stops the execution mid-flight and holds it until a person decides.",
    kind="chev+cards",
    chevrons=[("Event arrives", "a client message"), ("Agent drafts", "classify, flag, propose"),
              ("Draft is logged", "before any human sees it"), ("Human decides", "Approve or Decline"),
              ("Only then", "send and log the outcome")],
    cards=[
        ("BLUE", "The execution really is paused",
         "Look at the canvas and the run is sitting on the approval node. It waits days if it has to — n8n holds the state."),
        ("TEAL", "Approve and Decline are just links",
         "The email carries two URLs. Clicking one resumes the execution down that branch — no app for the approver to learn."),
        ("AMBER", "A decline is a reassignment",
         "Declining is not deleting. The ticket moves to a named person, because someone still owes the client an answer."),
    ], cols=3,
    takeaway="The agent may do everything except the one thing that matters. That pause is the whole control.",
)

HITL_WHEN = dict(
    key="hitl_when", title="When to Put a Human in the Loop",
    intro="Six tests. If a process meets any one of them, it needs an approval gate.",
    kind="cards", cols=2,
    cards=[
        ("BLUE", "Money moves",
         "Payments, refunds, credit and lending decisions — anything with a direct financial consequence."),
        ("TEAL", "It is a regulated communication",
         "A licensed firm writing to a client about their money, health or legal position."),
        ("VIOLET", "The action is irreversible",
         "A sent email, a deleted record or published content cannot be recalled."),
        ("AMBER", "A person is vulnerable",
         "Distress, illness, bereavement, or savings that someone cannot afford to lose."),
        ("RED", "The stakes exceed the error rate",
         "A 2% error rate is fine for tagging tickets and unacceptable for approving loans."),
        ("GREEN", "Someone must be accountable",
         "A regulator asks which licensed person is answerable — not what the machine decided."),
    ],
    takeaway="Automate the drafting, not the deciding, wherever any of these six is true.",
)

GUARDRAILS = dict(
    key="guardrails", title="Guardrails — Two Gates Around the Agent",
    intro="Instructions shape what the agent intends. Guardrails check what actually goes in and comes out.",
    kind="panels",
    left=("INPUT GUARDRAIL — before the agent", "BLUE", [
        "Screen the incoming message before the model ever sees it.",
        "Block prompt injection: 'ignore your instructions and…'.",
        "Strip or reject personal data you must not process.",
        "Rate-limit and authenticate — a public webhook is a public door.",
    ]),
    right=("OUTPUT GUARDRAIL — after the agent", "VIOLET", [
        "Check the reply before it reaches a human being.",
        "Look for the phrases you have banned: guarantees, forecasts, advice.",
        "Validate the structured fields against the values you allow.",
        "On any doubt, route to a person rather than sending it.",
    ]),
    takeaway="Defence in depth: the same rule in the prompt AND in the workflow — only one of the two runs on a machine you control.",
)

# ---------------------------------------------------------------- TOPIC: RAG
WHY_RAG = dict(
    key="why_rag", title="Why Retrieval, Rather Than a Bigger Prompt",
    intro="For twenty short documents, pasting them all would genuinely work. The problem starts at two hundred.",
    kind="cards", cols=2,
    cards=[
        ("RED", "Prompts have a ceiling",
         "Add enough documents and you exceed the model's context window — the request simply fails."),
        ("AMBER", "Long prompts degrade quality",
         "Models attend less reliably to the middle of a very long context. The answer is in there and is still missed."),
        ("VIOLET", "You pay for every token",
         "Every question re-sends every document, whether or not it was relevant to that question."),
        ("GREEN", "Retrieval turns it around",
         "Fetch only the few documents that resemble the question, and send just those. Cheaper, shorter and more accurate."),
    ],
    takeaway="RAG is not a bigger prompt — it is a smaller, better-chosen one.",
)

RAG_PIPELINE = dict(
    key="rag_pipeline", title="The RAG Pipeline — Ingest Once, Retrieve Every Question",
    intro="Two separate workflows. You run ingestion once; retrieval runs on every single question.",
    kind="chev+cards",
    chevrons=[("Collect", "the source documents"), ("Split", "into chunks"),
              ("Embed", "each chunk into a vector"), ("Store", "in the vector store"),
              ("Retrieve", "the nearest chunks"), ("Answer", "from what came back")],
    cards=[
        ("BLUE", "Ingestion — run by hand",
         "Lab 5's first workflow: list 20 brochures on Drive, download, split, embed, insert. A Manual Trigger, run once."),
        ("TEAL", "Retrieval — runs per question",
         "Lab 5's second workflow: embed the question with the SAME model, find the nearest brochures, answer only from those."),
        ("RED", "The models must match",
         "A question embedded by one model cannot be compared against documents embedded by another. It fails silently, returning nonsense."),
    ], cols=3,
    takeaway="Ingest once, retrieve thousands of times — and use the identical embedding model on both sides.",
)

CHUNKING = dict(
    key="chunking", title="Chunking — the Biggest Lever on RAG Quality",
    intro="Most RAG projects fail quietly at chunking, not at the model.",
    kind="cards", cols=2,
    cards=[
        ("GREEN", "The rule",
         "The right chunk is the smallest piece of text that still answers a question on its own."),
        ("RED", "Too small",
         "A brochure sliced into thirds separates the course name from its fee. Retrieval then finds one without the other."),
        ("AMBER", "Too large",
         "Irrelevant text crowds the prompt and dilutes what actually matters."),
        ("BLUE", "Overlap",
         "A small overlap between chunks stops a sentence being cut in half at the boundary."),
        ("VIOLET", "In Lab 5",
         "Chunk size 4000 with overlap 0 — one brochure becomes exactly one vector, so the fee is never separated from the course."),
        ("TEAL", "topK",
         "How many chunks come back. Too few misses the answer; too many dilutes the prompt with noise."),
    ],
    takeaway="Tune the chunking before you blame the model — that is where the answer was lost.",
)

VECTOR_STORES = dict(
    key="vector_stores", title="Choosing a Vector Store",
    intro="Where the embeddings live, and whether they are still there tomorrow.",
    kind="panels",
    left=("SIMPLE VECTOR STORE — built in", "TEAL", [
        "No account, no API key, no index to create.",
        "Running RAG within ten minutes — this is what Lab 5 uses.",
        "WIPED whenever n8n restarts.",
        "Right for: learning, demos and prototypes.",
    ]),
    right=("A REAL VECTOR DATABASE", "VIOLET", [
        "Pinecone, Supabase (pgvector), Qdrant, Weaviate.",
        "An account, an index and a matching dimension to set up.",
        "Persists, scales, and is shared across n8n instances.",
        "Right for: anything that goes into production.",
    ]),
    takeaway="Prototype on the in-memory store; move to a hosted database the moment anyone else depends on the answers.",
)

GROUNDING = dict(
    key="grounding", title="Grounding an Agent Against Hallucination",
    intro="An ungrounded model asked for a price will produce one. It will be plausible, it will be wrong, and the customer will quote it back to you.",
    kind="cards", cols=2,
    cards=[
        ("BLUE", "Always call the tool first",
         "Instruct the agent to search the documents before answering any factual question at all."),
        ("TEAL", "Answer only from what came back",
         "Every factual claim must trace to a retrieved document, not to the model's general knowledge."),
        ("GREEN", "Give it permission to fail",
         "'I don't have that in our course information' is a far better answer than a confident invention."),
        ("RED", "Name what it must never invent",
         "A fee, a date, a duration, a course code, an instructor's name, a discount."),
        ("VIOLET", "Hide the machinery",
         "Never mention the vector store or that it is searching documents — the customer does not care."),
        ("AMBER", "Test the traps",
         "Ask about a course you do not run, a person who does not exist, and a discount never offered."),
    ],
    takeaway="Grounding is an instruction problem as much as a retrieval one — retrieval finds it, the prompt makes it stick.",
)

# ---------------------------------------------------------------- registry
ALL = [WHAT_IS_N8N, WORKFLOW_SHAPE, TRIGGER_NODES, TRIGGERS_IN_COURSE, DATA_NODES,
       STORAGE_NODES, JSON_EXPRESSIONS, TEST_VS_PROD_EXEC, CREDENTIALS,
       GEN_VS_AGENTIC, AGENT_COMPONENTS, MODEL_PROVIDERS, MODEL_PARAMS,
       MEMORY_CONCEPT, TOOLS_CONCEPT, INSTRUCTIONS_FOUR, GOOD_BAD_INSTRUCTIONS,
       MCP_CONCEPT, MCP_IN_N8N, STRUCTURED_OUTPUT,
       WHAT_IS_WEBHOOK, WEBHOOK_VS_HTTP, GET_VS_POST, TEST_VS_PROD_URL, WEBHOOK_CONFIG,
       HITL_LEVELS, HITL_PATTERN, HITL_WHEN, GUARDRAILS,
       WHY_RAG, RAG_PIPELINE, CHUNKING, VECTOR_STORES, GROUNDING]

BY_KEY = {c["key"]: c for c in ALL}

# Which concepts belong to which topic, in teaching order. build_slides.py and
# build_learner_guide.py both read this, so a concept can never appear on a slide
# without appearing in the Learner Guide.
# what_is_n8n and workflow_shape open Topic 1 inside the opener (build_slides.topic1_intro),
# just before the training-accounts slide, so they are not listed here.
TOPIC1_OPENER_CONCEPTS = ["what_is_n8n", "workflow_shape"]

TOPIC_CONCEPTS = {
    1: ["trigger_nodes", "triggers_in_course",
        "data_nodes", "storage_nodes", "json_expressions", "test_vs_prod_exec",
        "credentials", "gen_vs_agentic", "agent_components", "model_providers",
        "model_params", "memory_concept", "tools_concept", "instructions_four",
        "good_bad_instructions", "mcp", "mcp_in_n8n",
        "what_is_webhook", "webhook_vs_http", "get_vs_post", "test_vs_prod_url",
        "webhook_config", "structured_output"],
    2: ["hitl_levels", "hitl_pattern", "hitl_when", "guardrails"],
    3: ["why_rag", "rag_pipeline", "chunking", "vector_stores", "grounding"],
}
