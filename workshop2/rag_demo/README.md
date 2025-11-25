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

## 1. Download 
Go to https://github.com/openleanchain/RAG101 to download the repository as a ZIP file, then unzip it. Next, copy the **workshop2** folder to your VS Code workspace where you built workshop1.

When you open the project in VS Code, you should see a new folder structure like:

```text
workshop2/rag_demo/
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
      ├─ knowledge_base/         # auto created on first run
      │   └─ knowledge_library.json   
      ├─ outputs/                # auto created on first run
      │   └─ conversation_log.jsonl   # long-term memory (one JSON per line) 
      ├─ prompts/                
      │   ├─ system_prompt.txt   # system prompt template: tells the AI its role
      │   └─ user_prompt.txt     # user prompt template: how we show snippets + question
      └─ models/                 # auto created on first run or get zip from team lead
          └─ ... MiniLM files go here (see next section)
```
You will mostly touch:
- data/data_sources/book.pdf
- rag_main.py
 - the two prompt template files in data/prompts/ (if you want to change how the AI talks)

## 2. MiniLM model (local copy from a zip)
⚠️ You may **skip this step initially** and only perform it if you encounter issues with sentence transformer models in Step 4.

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
2. Turn the user’s question into an embedding.
3. Compare the codes and find the **closest cards** (Retrieval step in RAG).

### How to setup
1. Get the model zip file from your team lead.
2. Unzip it into the `data/models/` folder inside this project.

When you finish, it should look like:

```text
rag_demo/
  └─ data/
      └─ models/
          └─ models--sentence-transformers--all-MiniLM-L6-v2/
```

Note: If you want to downloae this model by yourself. On the first run, if the MiniLM model is not already in data/models/,
the sentence-transformers library may automatically download the model from Hugging Face and put it in a cache folder, which maybe in your user account (for example under .cache/huggingface/hub), or inside this project folder. This may take a few minutes the very first time, but later runs will reuse the cached copy.

## 3. Install required Python libraries

Before running the demo, you need to install a few Python libraries in your **virtual environment**.

1. Open the VS Code terminal  
   (menu: **View → Terminal**).
2. Make sure your virtual environment is activated.
3. Run this command **once**:

```bash
   pip install pypdf sentence-transformers scikit-learn openai numpy
```

## 4. Running the demo
1. Open the `rag_demo` folder in **VS Code**.
2. Make sure the correct **Python environment** is selected.
3. Open the **terminal** in VS Code  
   (menu: **View → Terminal**).
4. Open a new terminal and **click the triangle run button**, or run the following script manually:

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
