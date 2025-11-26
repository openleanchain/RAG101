# workshop2/incident_rag/triage_llm.py

from __future__ import annotations

import json
import os
from typing import Any, Dict, List
from openai import AzureOpenAI
from common.bc_config import get_api_credentials, get_model_deployment_name
from .triage_config import TRIAGE_LLM_MODEL


def _get_azure_client() -> AzureOpenAI:
    """Create and return an AzureOpenAI client using credentials from config."""
    creds = get_api_credentials()   

    return AzureOpenAI(**creds)


def call_triage_llm(
    messages: List[Dict[str, Any]],
    temperature: float = 0.2,
    max_tokens: int = 512,
) -> Dict[str, Any]:
    """
    Call the LLM with JSON-only output to get a structured triage result.

    Returns:
        {
          "data": <parsed JSON object from the model>,
          "usage": {
             "prompt_tokens": ...,
             "completion_tokens": ...,
             "total_tokens": ...
          }
        }
    """
    client = _get_azure_client()

    response = client.chat.completions.create(
        model=get_model_deployment_name(),  # Azure deployment name
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        response_format={"type": "json_object"},
    )

    choice = response.choices[0]
    content = choice.message.content or "{}"
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # Fallback: wrap raw content
        data = {"raw_content": content}

    usage = {
        "prompt_tokens": getattr(response.usage, "prompt_tokens", None),
        "completion_tokens": getattr(response.usage, "completion_tokens", None),
        "total_tokens": getattr(response.usage, "total_tokens", None),
    }

    return {"data": data, "usage": usage}
