"""
prompt_utils.py

Builds the augmented chat messages using:
- a system prompt template (system_prompt.txt)
- a user prompt template (user_prompt.txt)

The user prompt template can contain placeholders:
- {snippets}  → all retrieved text snippets
- {question}  → the student's question
"""

from typing import List, Dict, Any
from pathlib import Path

from .rag_config import SYSTEM_PROMPT_PATH, USER_PROMPT_PATH


def _load_text(path: Path) -> str:
    """
    Load a text file as UTF-8.

    If the file is missing, this will raise an error,
    which is fine for teaching (we want them to see it).
    """
    with path.open("r", encoding="utf-8") as f:
        return f.read().strip()


def build_snippets_text(top_cards: List[Dict[str, Any]]) -> str:
    """
    Build a readable text block from the retrieved cards.

    Example format:
        Snippet 1 (page 2):
        ...

        Snippet 2 (page 3):
        ...
    """
    lines: List[str] = []
    for i, card in enumerate(top_cards, start=1):
        lines.append(f"Snippet {i} (page {card['page']}):")
        lines.append(card["text"])
        lines.append("")  # blank line
    return "\n".join(lines).strip()


def build_augmented_messages(
    question: str,
    top_cards: List[Dict[str, Any]],
) -> List[Dict[str, str]]:
    """
    Create the messages list for the GPT chat completion, using
    external prompt templates.

    - System prompt text comes from SYSTEM_PROMPT_PATH.
    - User prompt text comes from USER_PROMPT_PATH and is formatted
      with {snippets} and {question}.
    """
    system_prompt = _load_text(SYSTEM_PROMPT_PATH)
    user_template = _load_text(USER_PROMPT_PATH)

    snippets_text = build_snippets_text(top_cards)

    # Fill in the template placeholders
    user_content = user_template.format(
        snippets=snippets_text,
        question=question,
    )

    messages: List[Dict[str, str]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]
    return messages
