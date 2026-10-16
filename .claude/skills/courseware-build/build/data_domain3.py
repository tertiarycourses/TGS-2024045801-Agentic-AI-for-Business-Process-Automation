"""Topic 3 — Retrieval-Augmented Generation (RAG). Lab 5."""

DOMAIN3 = [
    dict(
        num=5,
        topic=3,
        title="Lab 5 — RAG Customer Care Chatbot (Cook & Bake Academy)",
        short="Lab 5 — RAG Customer Care Chatbot",
        objective="deploy a RAG application that grounds an agent in the organisation's own documents (A1, A2, A3, K5, K7, K8)",
        desc=("Cook & Bake Academy's customer care team retypes the same answers all day, and every "
              "answer is already written in the course brochures."),
        desc_long=("Cook & Bake Academy runs 20 courses across two campuses, and its two-person customer "
              "care team retypes the same answers all day. Every answer is already written in the course "
              "brochures. You build the full RAG loop: an ingestion workflow that embeds all 20 brochures "
              "into a vector store, and a chatbot that retrieves only the brochures resembling each "
              "question and answers strictly from those."),
        build="Ingestion: Drive → Split → Embed → Vector Store   ·   Answering: Webhook → Agent + Retriever → Respond",
        services="n8n Simple Vector Store, Google Gemini Embeddings, Google Drive, AI Agent, Webhook",
        folder="lab5-rag",
        site=[("site-lab5.png",
                "The Cook & Bake Academy site with the course assistant open. Every answer it gives "
                "is grounded in the 20 brochures you ingested into the vector store.")],
        canvas=[("canvas-lab5-ingest.png",
                 "The ingestion workflow on the n8n canvas — run ONCE by hand. Twenty brochures are listed, "
                 "downloaded, split, embedded and inserted into the vector store."),
                ("canvas-lab5-agent.png",
                 "The answering workflow on the n8n canvas — runs on EVERY question. The Query Data Tool and "
                 "its embedding model hang below the agent.")],
        # the real n8n canvases, one per workflow — each follows its own workflow slide
        n8n_shot=[
            dict(img="n8n-flow-lab5-ingest.png", layout="side",
                 title="Lab 5 — The Ingestion Workflow in n8n",
                 intro="Part 1 as it looks after import. You run it once, by hand, to load all 20 brochures into the vector store.",
                 cards=[("BLUE","Fetch the brochures",
                         "When clicking 'Execute workflow' starts the run. List Brochures in Folder finds the 20 files "
                         "in YOUR Drive folder, and Download Each Brochure pulls each one down."),
                        ("VIOLET","Split and embed",
                         "Default Data Loader reads each file, Whole-Brochure Splitter keeps one brochure as one chunk, "
                         "and the Embeddings node turns every chunk into a vector."),
                        ("TEAL","Insert into the store",
                         "Simple Vector Store (Insert) saves the 20 vectors under your memory key, cookbake_<your-name>. "
                         "Clear Store is ON, so a re-run replaces instead of duplicating.")],
                 takeaway="Ingestion is a batch job: re-run it when a brochure changes — and after every n8n restart."),
            dict(img="n8n-flow-lab5-agent.png", layout="side",
                 title="Lab 5 — The Answering Workflow in n8n",
                 intro="Part 2 runs on every question. The agent must search the brochures before it is allowed to answer.",
                 cards=[("BLUE","Question in, answer out",
                         "Webhook receives the visitor's question from the website as a POST. Respond to Webhook sends "
                         "the agent's reply back to the chat window."),
                        ("VIOLET","The agent and its model",
                         "AI Agent reasons with the chat model. Its system message says: call the tool first and never "
                         "invent a fee. No Memory is attached, so each question stands alone."),
                        ("TEAL","The retrieval tool",
                         "Query Data Tool searches YOUR memory key and returns the 5 closest brochures. Shown here with "
                         "OpenAI; the lab file ships with Gemini — swap one, swap both.")],
                 takeaway="Same embedding model and same memory key in both workflows — or retrieval silently finds nothing."),
        ],
        extras=[
            ("annotated","Lab 5 — The Course Assistant in Action",
             dict(img="lab5-site-chat.png", layout="side",
                  intro="A real conversation on the Cook & Bake Academy site. Every fee in the reply came from a retrieved brochure.",
                  cards=[("BLUE","A typo still finds it",
                          "The visitor typed 'patries'. Embeddings match meaning, not spelling, so the pastry "
                          "brochures BAK-102 and BAK-109 still come back."),
                         ("VIOLET","Facts quoted, not invented",
                          "Fees and durations are quoted exactly: BAK-102 is SGD $1480 for 8 weeks / 48 hours — the "
                          "same S$1480 shown on the course card behind the chat."),
                         ("AMBER","It admits a gap",
                          "It did not give BAK-104's fee and said so instead of guessing. The brochure does list "
                          "SGD $420, so check what the tool returned: that is a retrieval gap.")],
                  takeaway="'I don't have that' is grounding working — fix gaps in retrieval, never by loosening the prompt."),
             None),
        ],
        chev=[[("Manual Trigger","you run ingestion once"),("Drive — list + download","20 brochures"),("Splitter","1 brochure = 1 chunk"),("Embeddings","3072-dim vectors"),("Vector Store — Insert","stored, ready to search")],
              [("Webhook — POST","a visitor asks a question"),("AI Agent","+ Query Data Tool"),("Retrieve","nearest brochures only"),("Respond","answer grounded in those")]],
        steps=[
            ("In Google Drive create a folder named 'brochures' and upload all 20 .txt files from the lab's brochures/ folder.", "",
             "That folder becomes the academy's single source of truth. When a fee changes, it changes here and nowhere else."),
            ("Open one brochure and read it — everything the chatbot will ever say comes from files like this one.", "",
             "If a fact is not in these files, a correctly-grounded chatbot cannot say it. That is the point of RAG."),
            ("Import Lab 5 - Part 1 Ingest Brochures.json — this is the ingestion workflow you run once.", "",
             "Ingestion and answering are separate workflows: you ingest once, then answer thousands of questions."),
            ("Open List Brochures in Folder, select YOUR brochures folder, and set your Google Drive credential.", "",
             "Point it at your own folder, or you will be answering questions from the author's copy of the documents."),
            ("Open Simple Vector Store (Insert) and change the Memory Key from cookbake_brochures to cookbake_<your-name>, because the whole class shares one namespace.", "",
             "The memory key is a global namespace on a shared instance. Leave the default and you will be answering questions from each other's brochures."),
            ("Confirm Clear Store is ON so that re-running replaces the 20 brochures instead of storing them twice.", "",
             "Turn it off and run twice, and every search returns each brochure twice."),
            ("Open Whole-Brochure Splitter and note chunk size 4000 with overlap 0 — one brochure becomes exactly one vector, so the fee is never separated from the course name.", "",
             "The default 1000-character splitter would slice a brochure into three: the fragment mentioning sourdough would not be the fragment with the price."),
            ("Open Embeddings Google Gemini, select your credential, and note the model gemini-embedding-001 produces 3072-dimensional vectors.", "",
             "Remember this number. The store's dimension must equal the embedding model's output, and a mismatch is the top cause of failed inserts."),
            ("Click Execute workflow. Twenty files are listed, downloaded, embedded and stored in about thirty seconds.", "",
             "Confirm exactly twenty vectors were inserted. More than twenty means Clear Store was off and you have duplicates."),
            ("Import Lab 5 - Part 2 Cook and Bake RAG Chatbot.json — the answering agent.", "",
             "This is the half that runs on every question. It never sees nineteen of the twenty brochures."),
            ("Open Query Data Tool and set its Memory Key to the SAME cookbake_<your-name> you used during ingestion. A mismatch here is the most common failure in this lab.", "",
             "If the keys differ, the agent searches an empty store and answers 'I don't have that' to everything — with no error anywhere."),
            ("Confirm the retrieval Embeddings node uses the identical model to ingestion — a question embedded by one model cannot be compared against brochures embedded by another.", "",
             "The numbers mean different things between models. The comparison silently returns nonsense rather than failing."),
            ("Open AI Agent and read the grounding rules: always call the tool first, never invent a fee or an instructor, and say 'I don't have that in our course information' when the brochures are silent.", "",
             "An ungrounded model asked for a price will produce one. It will be plausible, it will be wrong, and the customer will quote it back to you."),
            ("Save, Activate, copy the Production URL, then serve the website folder and paste the URL into Lab configuration.", "python3 -m http.server 8000",
             "If the webhook is unset the page silently falls back to a local keyword search and looks like it works — watch for the yellow warning banner."),
            ("Click the chat button and ask 'How much is the sourdough course?', then work through all ten rows of sample-questions.csv.", "",
             "TC7, TC8 and TC9 each plant something false and invite the model to agree. Any confident answer is a failure, however fluent."),
        ],
        test=("TC1 must quote BAK-101's exact fee from the brochure. Then run the three hallucination "
              "probes: TC7 (a course that does not exist), TC8 (an instructor name no brochure contains) "
              "and TC9 (a discount that was never offered). Any confident answer to these is a failure, "
              "however fluent."),
        learned=[
            ("What RAG does",
             "RAG retrieves the few documents that resemble the question instead of pasting everything into the prompt."),
            ("Embeddings",
             "An embedding places similar meanings close together, so retrieval works even when no words match."),
            ("Chunking",
             "Chunking is the single biggest lever on RAG quality — the right chunk answers a question on its own."),
            ("Match model and key",
             "The ingestion and retrieval embedding models must be identical, and the memory keys must match."),
            ("In-memory is temporary",
             "n8n's Simple Vector Store is wiped when n8n restarts — fine for learning, unacceptable in production."),
        ],
    ),
]
