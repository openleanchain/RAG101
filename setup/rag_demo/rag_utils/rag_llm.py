"""
rag_llm.py

Minimal LLM caller for the RAG demo.

Responsibility:
- Take an already-built list of messages (augmented prompt)
- Call Azure OpenAI chat completions
- Return:
    {
        "data":  <JSON parsed from model>,
        "usage": {
            "prompt_tokens": ...,
            "completion_tokens": ...,
            "total_tokens": ...
        }
    }

No saving to files.
No printing.
No knowledge of retrieval or knowledge cards.

All provider/model/client details are handled here, NOT in main().
Credentials and endpoint config are expected to be handled by:
    get_azure_openai_client()
in your common.azure_client module (or similar).
"""

from typing import Any, Dict, List, Optional
import json

from .rag_config import GPT_DEPLOYMENT_NAME

try:
    # Shared helper that returns a configured AzureOpenAI client.
    # You provide this in your own codebase.
    from common.azure_client import get_azure_openai_client
except ImportError as e:
    raise ImportError(
        "Please provide a 'get_azure_openai_client' helper in "
        "common.azure_client (or update the import in rag_llm.py) "
        "so we can create an AzureOpenAI client."
    ) from e


def call_llm_json(
    messages: List[Dict[str, str]],
    deployment_name: str = GPT_DEPLOYMENT_NAME,
    temperature: float = 0.2,
    max_tokens: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Call Azure OpenAI chat completions and return JSON + usage as Python dicts.

    Parameters
    ----------
    messages : list of {role, content}
        Already-built chat messages (system + user), e.g. from prompt_utils.
    deployment_name : str
        Azure OpenAI deployment name (NOT the base model name).
    temperature : float
        Sampling temperature for the model.
    max_tokens : Optional[int]
        Optional max tokens for the completion. If None, it is not passed.

    Returns
    -------
    Dict[str, Any]
        {
            "data":  <JSON parsed from model's content>,
            "usage": {
                "prompt_tokens": ...,
                "completion_tokens": ...,
                "total_tokens": ...
            }
        }
    """
    client = get_azure_openai_client()

    kwargs: Dict[str, Any] = {
        "model": deployment_name,          # Azure deployment name
        "messages": messages,
        "temperature": temperature,
        "response_format": {"type": "json_object"},
    }
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens

    response = client.chat.completions.create(**kwargs)

    # JSON content from the model (string → dict)
    content = response.choices[0].message.content
    data: Dict[str, Any] = json.loads(content)

    # Usage info (tokens) for cost tracking
    usage_obj = response.usage
    usage: Dict[str, Any] = {
        "prompt_tokens": getattr(usage_obj, "prompt_tokens", None),
        "completion_tokens": getattr(usage_obj, "completion_tokens", None),
        "total_tokens": getattr(usage_obj, "total_tokens", None),
    }

    return {
        "data": data,
        "usage": usage,
    }
