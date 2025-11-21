"""
rag_main.py

Entry point for the RAG demo.

High-level teaching steps:
1) Build the AI Knowledge Library once (if needed).
2) Ask the user for a question.
3) Retrieval: find top-k knowledge cards.
4) Augmented Prompt: build messages (system + user) using templates.
5) LLM Call (short-term memory): send the augmented prompt to a language model.
6) Long-Term Memory: save this conversation turn into a log file.

Note:
- This file does NOT know anything about OpenAI, Azure, API keys,
  or model deployment names. It only calls a generic LLM helper
  that returns JSON data + usage as Python dictionaries.
"""
print("=== Start RAG demo... loading all the libraries and AI brain. It may take 1-2 minutes, please wait... ===")

import os

from rag_utils.rag_config import PDF_PATH, KNOWLEDGE_LIBRARY_PATH
from rag_utils.knowledge_library import build_and_save_knowledge_library, load_knowledge_library
from rag_utils.retrieval import retrieve_top_k_cards
from rag_utils.prompt_utils import build_augmented_messages
from rag_utils.rag_llm import call_llm_json
from rag_utils.memory_store import append_conversation_record


def main() -> None:
    print("=== RAG Demo: AI Knowledge Library ===")
    print()

    # Step 1: Build the AI Knowledge Library only if it doesn't exist yet
    print("=== Step 1: Build the AI Knowledge Library only if it doesn't exist yet ===")
    if not os.path.exists(KNOWLEDGE_LIBRARY_PATH):
        print("\tKnowledge Library not found. Building it now...")
        build_and_save_knowledge_library(PDF_PATH, KNOWLEDGE_LIBRARY_PATH)
    else:
        print("\tKnowledge Library already exists. Skipping build step.")

    # Ask for a question
    print()
    print("Now let's ask the AI Librarian a question about the book.")
    user_question = input("Type your question here: ")

    if not user_question.strip():
        print("No question entered. Exiting.")
        return

    # Step 2: Load library
    print("=== Step 2: Load the AI Knowledge Library from disk ===")
    print("\nLoading AI Knowledge Library from disk...")
    library = load_knowledge_library(KNOWLEDGE_LIBRARY_PATH)

    # Step 3: RETRIEVAL (R in RAG)
    print("=== Step 3: Retrieval - finding best knowledge cards for the question ===")
    top_cards = retrieve_top_k_cards(user_question, library=library)
    for i, card in enumerate(top_cards, start=1):
        content = card.get("text", "<no text>")
        preview = (content[:75] + "...") if len(content) > 75 else content
        print(
            f"  Top {i}: card_id={card.get('id')}, "
            f"page={card.get('page')}, similarity={card['similarity']:.3f}, "
            f"content='{preview}'"
        )

    # Step 4: AUGMENTED PROMPT (A in RAG)
    print("=== Step 4: Augmented Prompt - building messages from templates ===")
    messages = build_augmented_messages(user_question, top_cards)
    print("\n--- Augmented Messages ---")
    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        print(f"[{role}]: {content[:100]}{'...' if len(content) > 100 else ''}")

    # Step 5: LLM CALL (G in RAG = Generation, using short-term memory only)
    print("=== Step 5: LLM Call - sending augmented prompt to the language model ===")
    # This function hides ALL model/provider details.
    # It just returns Python dictionaries: {"data": ..., "usage": ...}
    llm_result = call_llm_json(messages=messages)

    if llm_result:
        # The LLM module has already parsed the JSON content for us.
        answer_data = llm_result["data"]   # e.g. {"answer": "...", "sources": [...]}
        usage = llm_result["usage"]       # e.g. {"prompt_tokens": ..., "total_tokens": ...}

        # Show answer & usage to students (teaching: how much "cost"/tokens)
        print("\n--- Model Answer ---")
        print(answer_data.get("answer", ""))
        print("Sources (page numbers):", answer_data.get("sources", []))

        print("\n--- Token Usage (for cost awareness) ---")
        print("Prompt tokens:    ", usage.get("prompt_tokens"))
        print("Completion tokens:", usage.get("completion_tokens"))
        print("Total tokens:     ", usage.get("total_tokens"))

        # Step 6: LONG-TERM MEMORY (app-side memory, not the model's)
        print("=== Step 6: Long-Term Memory - saving this conversation turn ===")
        append_conversation_record(
            question=user_question,
            top_cards=top_cards,
            llm_data=answer_data,
            usage=usage,
        )
        print("This question & answer were saved into the long-term memory log.")


if __name__ == "__main__":
    main()
