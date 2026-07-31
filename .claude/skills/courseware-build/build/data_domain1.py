"""Topic 1 — Overview of n8n and AI Agents. Labs 1 and 2."""

DOMAIN1 = [
    dict(
        num=1,
        topic=1,
        title="Lab 1 — n8n Trigger and Action (Event Flyer with QR Code)",
        short="Lab 1 — n8n Trigger and Action",
        objective="build an automated workflow in n8n using a trigger and an action (A2, K7, K8)",
        desc=("Build your first n8n workflow end to end. An n8n Form Trigger collects a visitor's "
              "details, and a Gmail action emails them to the event administrator. You then turn the "
              "form's public URL into a QR code and place it on an event flyer, so anyone can sign up "
              "by scanning it with a phone."),
        build="Form Trigger  →  Gmail (Send a message)",
        services="n8n Form Trigger, Gmail (OAuth2), Smart QR Code Generator",
        folder="lab1-trigger-actions",
        site=[("site-lab1.png",
                "The finished Lab 1 workflow on the n8n canvas — the Form Trigger fires on each "
                "submission and the Gmail node sends the details to the administrator."),
               ("site-lab1-flyer.png",
                "A sample event flyer from a previous class. The QR code encodes the form's "
                "Production URL, so anyone can sign up by scanning it with a phone.")],
        flows=[("flow-lab1.png",
                "Two nodes. The Form Trigger decides WHEN the workflow runs; the Gmail node decides WHAT it does.")],
        steps=[
            ("In n8n, click Workflows → Add workflow, and give it a name such as 'Lab 1 — Event Signup'.", "",
             "Name it now. On a shared instance a canvas called 'My workflow 7' is impossible to find again."),
            ("Add an n8n Form Trigger node. Set a Form Title (e.g. 'Event Signup') and a short description.", "",
             "The trigger is always the first node — it is what decides WHEN this workflow runs."),
            ("Add four form fields: Name (Text), Email (Email), Phone (Number) and Message (Textarea). Mark Name and Email as required.", "",
             "Field names become the JSON keys the next node reads, so Name here is what makes {{ $json.Name }} work later."),
            ("Add a Gmail node after the trigger and choose the 'Send a message' operation.", "",
             "This is the action: the trigger decided when, the action decides what actually happens."),
            ("Connect your Gmail account under Credential to connect with → Sign in with Google, and grant access.", "",
             "Credentials are stored once and reused by every workflow. Never paste a key into a node field."),
            ("Set To = the administrator's address and Subject = New Enquiry.", "",
             "Fixed values are fine here — only the body needs to change per submission."),
            ("Switch the Message field to Expression and build the body from the form fields, e.g. Name: {{ $json.Name }} and Email: {{ $json.Email }}.", "",
             "In Fixed mode n8n prints the braces literally. Expression mode is what evaluates them against the incoming item."),
            ("Click Execute workflow to open the test form, submit a sample entry, and confirm the email arrives.", "",
             "Test before activating. The canvas shows the data at every node, so you can see exactly what the Gmail node received."),
            ("Save the workflow and toggle it Active, then copy the Form's Production URL.", "",
             "The Test URL answers exactly one request. Only the Production URL, with the workflow Active, works for everyone."),
            ("Open the Smart QR Code Generator at alfredang.github.io/qrcodegenerator, paste the Production URL, and download the QR code as PNG.", "",
             "The generator runs entirely in your browser — nothing about your form is uploaded to a third party."),
            ("Group activity: design an event flyer (for example a bowling night or a networking evening) with the QR code on it, then present it to the class.", "",
             "This is the whole point: a two-node workflow becomes a real sign-up channel anyone can use from a phone."),
        ],
        test=("Scan the QR code on your flyer with your phone, submit the form, and confirm the "
              "administrator's inbox receives the email with the details you typed. A reference "
              "solution is provided as labs/lab1-trigger-actions/lab-trigger-actions.json — build "
              "yours by hand first, then import it to compare."),
        learned=[
            ("Triggers and actions",
             "A trigger decides when a workflow runs; an action decides what it does."),
            ("Expressions",
             "Expressions such as {{ $json.Name }} carry data from one node to the next."),
            ("Test vs Production URL",
             "The Test URL works only while you are listening; the Production URL works once the workflow is Active."),
        ],
    ),
    dict(
        num=2,
        topic=1,
        title="Lab 2 — Webhook and AI Agent (Marina Trust Bank Onboarding)",
        short="Lab 2 — Webhook and AI Agent",
        objective="deploy an AI agent that is triggered by a webhook from an external website (A1, A2, K7, K8)",
        desc=("Replace the n8n form with a real bank website. A customer applies for an account on your "
              "own HTML page, which POSTs to an n8n Webhook. An AI Agent applies the bank's onboarding "
              "rules, calls Google Sheets tools to check for duplicates and create the customer record, "
              "emails a confirmation, and returns a structured decision that the page renders as a "
              "coloured card."),
        build="Webhook  →  Normalise  →  AI Agent (+3 tools)  →  Log Decision  →  Respond to Website",
        services="n8n Webhook, AI Agent, Google Gemini, Google Sheets, Gmail, Structured Output Parser",
        folder="lab2-webhook-agent",
        site=[("site-lab2.png",
                "The Marina Trust Bank site the webhook sits behind. The applicant submits here, the "
                "AI Agent decides, and the page renders the decision as a coloured card.")],
        flows=[("flow-lab2.png",
                "The main chain runs left to right; the three tools below are attached to the agent's Tool input — "
                "the agent decides which to call, and when.")],
        steps=[
            ("Create a Google Sheet named 'Retail Banking Onboarding' with a Customers tab and an Onboarding_Log tab, and seed a few existing customers.", "",
             "The seeded rows are what make the duplicate test (TC2) meaningful — without them every applicant looks new."),
            ("In n8n choose Workflows → Import from File and select lab2-webhook-agent.json.", "",
             "Importing lets you study a finished agent. You will still re-point every credential and sheet to your own."),
            ("Open the Onboarding Webhook node. Confirm HTTP Method = POST, Path = marina-trust-onboarding, and Respond = Using 'Respond to Webhook' Node.", "",
             "POST carries a JSON body, which is what a web form sends. 'Respond to Webhook' is what lets the agent's decision travel back to the browser instead of an immediate 200 OK."),
            ("Under the webhook's Options, set Allowed Origins (CORS) to * so a browser page is permitted to read the reply.", "",
             "Without CORS the n8n execution succeeds but the browser refuses to read the response — the classic 'Failed to fetch'."),
            ("Open check_duplicate_customer, create_customer_record and Log Decision, and re-select YOUR spreadsheet in each Document dropdown.", "",
             "These three point at the author's sheet until you change them. Miss one and the agent reads or writes the wrong file."),
            ("Re-select your own Google Gemini, Google Sheets and Gmail credentials on every node that shows a credential warning.", "",
             "Imported workflows carry credential NAMES, not secrets — nothing of the author's account came with the file."),
            ("Open the Onboarding AI Agent and read the system message: the eligibility rules, the age check, and the four possible decisions.", "",
             "The system message is where the bank's policy actually lives. Change this and you change the lending decision."),
            ("Open the Decision Parser and note the required fields — decision, reason, riskFlags — this is what lets the website colour the result card.", "",
             "A paragraph of prose could not be coloured, counted or branched on. decision is a field precisely so something downstream can act on it."),
            ("Click Listen for test event, then open index.html in your browser.", "",
             "Listening arms the Test URL for exactly one request and streams the incoming data onto the canvas."),
            ("In the page's Lab configuration panel, paste the webhook Test URL, choose TC1 from the Trainer demo data dropdown, enter your own email, and submit.", "",
             "The demo data deliberately clears the email field so you cannot send a stranger a bank decision by accident."),
            ("Watch the request land on the n8n canvas and follow it through Normalise into the agent; confirm the agent calls check_duplicate_customer.", "",
             "This is the moment the agent stops being a black box — you can see it CHOOSE to call a tool."),
            ("Save, toggle the workflow Active, copy the Production URL and paste it into the panel so the page works from any device.", "",
             "Only now does the page work for anyone but you. The Test URL has already been spent."),
        ],
        test=("Run TC1 (a new applicant) and confirm a green APPROVED card, a new row in the Customers "
              "sheet and a confirmation email. Then run TC2 (an already-seeded NRIC) and confirm an "
              "amber DUPLICATE card with no new row."),
        learned=[
            ("Webhooks",
             "A webhook lets any external system — your website, an app, a CRM — start an agent workflow."),
            ("Tools make an agent",
             "Tools are what turn an LLM into an agent: it decides when to look up a customer and when to create one."),
            ("Structured output",
             "Structured output (decision, reason, riskFlags) is what lets downstream nodes branch, log and colour a result."),
            ("The front door is separate",
             "The agent is unchanged from a form-triggered version — only the front door differs."),
        ],
    ),
]
