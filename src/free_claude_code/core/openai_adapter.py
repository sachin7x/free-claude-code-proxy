"""OpenAI-compatible request/response adapters for FCC server."""

from typing import Any, Dict, List


def openai_to_anthropic_request(openai_request: Dict[str, Any]) -> Dict[str, Any]:
    """Convert OpenAI chat request to Anthropic Messages API format"""
    # Convert OpenAI messages to Anthropic format
    messages = []
    system_message = None
    
    for msg in openai_request.get("messages", []):
        if msg.get("role") == "system":
            system_message = msg.get("content")
        elif msg.get("role") == "user":
            messages.append({
                "role": "user",
                "content": msg.get("content")
            })
        elif msg.get("role") == "assistant":
            messages.append({
                "role": "assistant",
                "content": msg.get("content")
            })
    
    anthropic_request = {
        "model": openai_request.get("model"),
        "max_tokens": openai_request.get("max_tokens", 1024),
        "messages": messages,
    }
    
    if system_message:
        anthropic_request["system"] = system_message
    
    if openai_request.get("temperature"):
        anthropic_request["temperature"] = openai_request.get("temperature")
    
    return anthropic_request


def anthropic_to_openai_response(anthropic_response: Dict[str, Any]) -> Dict[str, Any]:
    """Convert Anthropic Messages API response to OpenAI chat format"""
    # Extract content from Anthropic response
    content = ""
    if "content" in anthropic_response:
        for block in anthropic_response["content"]:
            if block.get("type") == "text":
                content += block.get("text", "")
            elif block.get("type") == "thinking":
                # Skip thinking blocks for OpenAI compatibility
                pass
    
    openai_response = {
        "id": anthropic_response.get("id", ""),
        "object": "chat.completion",
        "created": anthropic_response.get("created", 0),
        "model": anthropic_response.get("model", ""),
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": content
            },
            "finish_reason": anthropic_response.get("stop_reason", "stop")
        }],
        "usage": {
            "prompt_tokens": anthropic_response.get("usage", {}).get("input_tokens", 0),
            "completion_tokens": anthropic_response.get("usage", {}).get("output_tokens", 0),
            "total_tokens": anthropic_response.get("usage", {}).get("input_tokens", 0) + anthropic_response.get("usage", {}).get("output_tokens", 0)
        }
    }
    
    return openai_response