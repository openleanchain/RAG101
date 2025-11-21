# 🧠📚 RAG Demo – AI Knowledge Library

In this mini project we turn a PDF into an **AI Knowledge Library** and let an
AI “Librarian” answer questions about it.

You will see:

1. PDF → text → **knowledge cards** (chunks)
2. Each card gets a **secret number code** (embedding)
3. The computer **finds the best cards** for your question (Retrieval)
4. We build an **augmented prompt** and ask the AI (Generation)
5. We save a **long-term memory log** of each question + answer

You only need to run one file: `rag_main.py`.

---

## 1. Folder structure

When you open the project in VS Code, you should see something like:

```text
rag_demo/
  ├─ rag_main.py                 # 🚀 main script you will run
  ├─ rag_utils/                  # helper modules used by main
  │   ├─ __init__.py
  │   ├─ rag_config.py           # paths, model names, constants
  │   ├─ pdf_utils.py            # PDF → pages → knowledge cards
  │   ├─ knowledge_library.py    # build & load AI Knowledge Library
  │   ├─ retrieval.py            # find top-k best knowledge cards
  │   ├─ prompt_utils.py         # build augmented messages from templates
  │   ├─ rag_llm.py              # call the LLM and return JSON + usage
  │   └─ memory_store.py         # save long-term memory log
  └─ data/
      ├─ data_sources/
      │   └─ book.pdf            # the PDF we will use
      ├─ knowledge_base/
      │   └─ knowledge_library.json   # created on first run
      ├─ outputs/
      │   └─ conversation_log.jsonl   # long-term memory (one JSON per line)
      ├─ prompts/
      │   ├─ system_prompt.txt   # tells the AI its role
      │   └─ user_prompt.txt     # how we show snippets + question
      └─ models/
          └─ ... MiniLM files go here (see next section)
```
You will mostly touch:
- data/data_sources/book.pdf
- rag_main.py
 - the two prompt files in data/prompts/ (if you want to change how the AI talks)

## 2. MiniLM model (local copy from a zip)

In this project we use a small helper model called **MiniLM**.

- MiniLM is a **“mini language model”**.
- Its job is **not** to answer questions.
- Its job is to turn each piece of text into a long list of numbers called an **embedding**.

You can think of an **embedding** as a **secret number code** for a sentence:

- Texts with **similar meaning** get **similar codes**.
- Texts with **different meaning** get **very different codes**.
- This makes it easy for the computer to answer:  
  > “Which text chunks are closest to this question?”

We use these number codes to:

1. Turn all the knowledge cards from the PDF into embeddings.
2. Turn the student’s question into an embedding.
3. Compare the codes and find the **closest cards** (Retrieval step in RAG).

To keep things fast for class, your teacher will provide a **separate zip file**
that contains the MiniLM embedding model.  
(We do **not** store this big model inside the GitHub repo.)

> **Download link (to be added by teacher):**  
> `<< MINI_LM_MODEL_ZIP_URL_HERE >>`

### Steps for students

1. Download the zip file from the link your teacher gives you.
2. Unzip it into the `data/models/` folder inside this project.

When you finish, it should look like:

```text
rag_demo/
  └─ data/
      └─ models/
          └─ sentence-transformers_all-MiniLM-L6-v2_...   (and other files)


## 2. MiniLM model (local copy from a zip)
We will use the MiniLM embedding model that you can download from hugging face or get from your team lead.
1. Get the model zip file from your team lead.
2. Unzip it into the `data/models/` folder inside this project.

When you finish, it should look like:

```text
rag_demo/
  └─ data/
      └─ models/
          └─ models--sentence-transformers--all-MiniLM-L6-v2/

## 3. Running the demo

1. Open the `rag_demo` folder in **VS Code**.
2. Make sure the correct **Python environment** is selected (your teacher will
   have set this up).
3. Open the **terminal** in VS Code  
   (menu: **View → Terminal**).
4. In the terminal, run:

```bash
   python rag_main.py
```
You’re now running the full RAG pipeline:
- Build or reuse the AI Knowledge Library
- Ask a question
- Retrieve the best knowledge cards
- Build an augmented prompt
- Call the language model
- Save the conversation into long-term memory
