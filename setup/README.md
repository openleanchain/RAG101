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
