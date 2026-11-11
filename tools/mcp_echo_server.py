#!/usr/bin/env python3
"""Minimal stdio MCP server exposing a single echo tool."""

import json
import sys
from typing import Any, Dict


SERVER_INFO = {"name": "local-echo", "version": "1.0.0"}
PROTOCOL_VERSION = "2024-11-05"
TOOLS = [
    {
        "name": "echo",
        "description": "Return the supplied message unchanged.",
        "inputSchema": {
            "type": "object",
            "properties": {"message": {"type": "string", "description": "Message to echo."}},
            "required": ["message"],
        },
    }
]


def _response(request_id: Any, result: Dict[str, Any]) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _error(request_id: Any, code: int, message: str) -> Dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": code, "message": message},
    }


def handle_message(message: Dict[str, Any]):
    request_id = message.get("id")
    method = message.get("method")
    params = message.get("params") or {}

    if method == "notifications/initialized":
        return None
    if method == "initialize":
        requested_version = params.get("protocolVersion")
        version = requested_version or PROTOCOL_VERSION
        return _response(
            request_id,
            {
                "protocolVersion": version,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": SERVER_INFO,
            },
        )
    if method == "ping":
        return _response(request_id, {})
    if method == "tools/list":
        return _response(request_id, {"tools": TOOLS})
    if method == "tools/call":
        if params.get("name") != "echo":
            return _error(request_id, -32602, "Unknown tool.")
        arguments = params.get("arguments") or {}
        text = arguments.get("message")
        if not isinstance(text, str):
            return _error(request_id, -32602, "The 'message' argument must be a string.")
        return _response(
            request_id,
            {"content": [{"type": "text", "text": text}], "isError": False},
        )
    if request_id is None:
        return None
    return _error(request_id, -32601, f"Method not found: {method}")


def main() -> None:
    for line in sys.stdin:
        try:
            message = json.loads(line)
            if not isinstance(message, dict):
                raise ValueError("JSON-RPC message must be an object.")
            response = handle_message(message)
        except (json.JSONDecodeError, ValueError) as error:
            response = _error(None, -32700, str(error))
        if response is not None:
            sys.stdout.write(json.dumps(response, separators=(",", ":")) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
