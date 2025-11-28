
# Function Calling-Based Decision Making with Multi-Turn Logic
"""
Features:
- LLM function calling (tool_choice="auto")
- Automatic tool invocation for CRISIS severity
- Multi-turn logic: after tool execution, send result back to LLM for full JSON
- Includes real chat history (system + user + assistant + tool)
"""
print("=================Loading tools and libraries, may take 1-2 minutes, please wait...")
import json
import sys
import uuid
from typing import List, Dict, Any
from openai import AzureOpenAI
from common.bc_config import get_api_credentials, get_model_deployment_name
from workshop2.incident_rag import triage_prompt
from workshop2.incident_rag.policy_retriever import search_policies
from workshop2.incident_rag.triage_schema import PolicyChunkSchema

# -------------------------
# Configuration
# -------------------------

DEPLOYMENT_NAME = get_model_deployment_name()
DEFAULT_TEMPERATURE = 0.1
DEFAULT_MAX_TOKENS = 500

client = AzureOpenAI(**get_api_credentials())

# -------------------------
# Tool definitions
# -------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "escalate_crisis",
            "description": "Escalate a CRISIS-level incident to on-call team. Generates ticket ID automatically.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string"},
                    "severity": {
                        "type": "string",
                        "enum": ["NORMAL", "ALERT", "CRISIS"]
                    },
                    "actions": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["summary", "severity", "actions"]
            }
        }
    }
]

# -------------------------
# Tool implementation
# -------------------------

def escalate_crisis(summary: str, severity: str, actions: List[str]) -> Dict[str, Any]:
    ticket_id = f"TICKET-{uuid.uuid4().hex[:6].upper()}"
    print(f"\n[TOOL] escalate_crisis called")
    print(f"       Ticket ID: {ticket_id}")
    print(f"       Severity : {severity}")
    print(f"       Summary  : {summary}")

    subject = f"[{severity}] {ticket_id} - {summary}"
    print("[EMAIL] Alert:")
    print(f"        Subject: {subject}")
    for i, action in enumerate(actions, start=1):
        print(f"         {i}. {action}")

    return {"success": True, "ticket_id": ticket_id, "severity": severity}


def process_tool_call(tool_name: str, tool_input: Dict[str, Any]) -> str:
    if tool_name == "escalate_crisis":
        result = escalate_crisis(
            summary=tool_input.get("summary", ""),
            severity=tool_input.get("severity", ""),
            actions=tool_input.get("actions", [])
        )
    else:
        result = {"error": f"Unknown tool: {tool_name}"}
    return json.dumps(result)

# -------------------------
# Multi-turn LLM logic
# -------------------------

def call_triage_llm_with_tools(description: str,
                               temperature: float,
                               max_tokens: int) -> Dict[str, Any]:
    # Retrieve policies
    policy_results = search_policies(description, top_k=3)
    policy_chunks: List[PolicyChunkSchema] = [pr[0] for pr in policy_results]

    # Build messages
    messages = triage_prompt.build_triage_messages(
        incident_text=description, policy_chunks=policy_chunks
    )

    # First LLM call
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
        temperature=temperature,
        max_tokens=max_tokens
    )

    msg = response.choices[0].message
    print("\n[DEBUG] First LLM Response:", msg.content)
    print("[DEBUG] Tool Calls:", msg.tool_calls)

    result_data: Dict[str, Any] = {}

    if msg.tool_calls:
        # CRISIS path: execute tool
        tool_call = msg.tool_calls[0]
        tool_name = tool_call.function.name
        tool_input = json.loads(tool_call.function.arguments)

        print(f"\n[CALLING TOOL] {tool_name}")
        tool_result_json = process_tool_call(tool_name, tool_input)

        # Append assistant message with tool_calls
        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": msg.tool_calls
        })

        # Append tool result
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": tool_result_json
        })

        # Second LLM call for full JSON
        response2 = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        final_msg = response2.choices[0].message
        print("\n[DEBUG] Final LLM Response After Tool:", final_msg.content)

        try:
            llm_json = json.loads(final_msg.content)
            result_data.update({
                "summary": llm_json.get("summary", ""),
                "severity": llm_json.get("severity", ""),
                "actions": llm_json.get("actions_now", []),
                "next_steps": llm_json.get("next_steps", []),
                "estimated_time_hours": llm_json.get("estimated_time_hours", 0),
                "requires_policy_update": llm_json.get("requires_policy_update", False),
                "policy_refs": llm_json.get("policy_refs", []),
                "ticket_id": json.loads(tool_result_json).get("ticket_id")
            })
        except json.JSONDecodeError:
            result_data["message"] = final_msg.content

    else:
        # NORMAL/ALERT path: parse JSON from first response
        try:
            llm_json = json.loads(msg.content)
            result_data.update({
                "summary": llm_json.get("summary", ""),
                "severity": llm_json.get("severity", ""),
                "actions": llm_json.get("actions_now", []),
                "next_steps": llm_json.get("next_steps", []),
                "estimated_time_hours": llm_json.get("estimated_time_hours", 0),
                "requires_policy_update": llm_json.get("requires_policy_update", False),
                "policy_refs": llm_json.get("policy_refs", [])
            })
        except json.JSONDecodeError:
            result_data["message"] = msg.content or "(no tool call, text response only)"

    return result_data

# -------------------------
# Workflow
# -------------------------

def run_workflow_with_function_calling(description: str,
                                       temperature: float,
                                       max_tokens: int) -> None:
    print("\n=== Calling LLM with Function Calling ===")
    data = call_triage_llm_with_tools(description, temperature, max_tokens)

    print("\n=== Workflow Results ===")
    print(f"Summary : {data.get('summary', '(none)')}")
    print(f"Severity: {data.get('severity', '(none)')}")

    print("\nActions Now:")
    for i, action in enumerate(data.get("actions", []), start=1):
        print(f"  {i}. {action}")

    print("\nNext Steps:")
    for i, step in enumerate(data.get("next_steps", []), start=1):
        print(f"  {i}. {step}")

    print(f"\nEstimated Time (hours): {data.get('estimated_time_hours', '(none)')}")

    print("\nPolicy References:")
    for ref in data.get("policy_refs", []):
        print(f"  - {ref}")

    if data.get("ticket_id"):
        print(f"\n✓ Crisis escalated - Ticket: {data.get('ticket_id')}")
    else:
        print("\nIncident triaged and logged (no escalation tool used).")

    print("\n=== Workflow Complete ===")

# -------------------------
# Main entry point
# -------------------------

def main() -> None:
    print("=== Incident Triage with Function Calling ===")
    description = input("Describe the incident: ").strip()
    if not description:
        print("No description provided. Exiting.")
        return
    run_workflow_with_function_calling(description, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS)


if __name__ == "__main__":
    main()
