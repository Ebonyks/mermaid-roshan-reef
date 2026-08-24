"""Minimal client for the loopback-only Resolve bridge installed on this PC.

The authentication secret is read from Resolve's private runtime config and is
never logged or copied into this repository.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import socket
import time
from pathlib import Path
from typing import Any


CONFIG_PATH = Path.home() / (
	"AppData/Roaming/Blackmagic Design/DaVinci Resolve/Support/Fusion/"
	".davinci_mcp_runtime/bridge.json"
)


class ResolveBridgeError(RuntimeError):
	pass


class ResolveBridgeClient:
	def __init__(self, config_path: Path = CONFIG_PATH) -> None:
		config = json.loads(config_path.read_text(encoding="utf-8"))
		self.host = str(config["host"])
		self.port = int(config["port"])
		self._token = str(config["token"])

	@staticmethod
	def _canonical(request: dict[str, Any]) -> bytes:
		unsigned = {key: value for key, value in request.items() if key != "signature"}
		return json.dumps(
			unsigned,
			sort_keys=True,
			separators=(",", ":"),
			ensure_ascii=True,
		).encode("utf-8")

	def request(self, operation: str, arguments: dict[str, Any] | None = None) -> Any:
		request: dict[str, Any] = {
			"protocol": "1.0",
			"id": secrets.token_hex(8),
			"timestamp": int(time.time()),
			"nonce": secrets.token_urlsafe(18),
			"operation": operation,
			"arguments": arguments or {},
		}
		request["signature"] = hmac.new(
			self._token.encode("utf-8"), self._canonical(request), hashlib.sha256
		).hexdigest()
		payload = (json.dumps(request, separators=(",", ":")) + "\n").encode("utf-8")
		with socket.create_connection((self.host, self.port), timeout=15.0) as sock:
			sock.sendall(payload)
			sock.shutdown(socket.SHUT_WR)
			chunks: list[bytes] = []
			while True:
				chunk = sock.recv(65536)
				if not chunk:
					break
				chunks.append(chunk)
		response = json.loads(b"".join(chunks).decode("utf-8"))
		if not response.get("ok"):
			raise ResolveBridgeError(json.dumps(response.get("error"), sort_keys=True))
		return response.get("result")

	@staticmethod
	def handle(value: Any) -> str:
		if isinstance(value, dict) and isinstance(value.get("__handle__"), str):
			return value["__handle__"]
		if isinstance(value, str):
			return value
		raise ResolveBridgeError(f"Expected Resolve handle, got {value!r}")

	def call(self, method: str, *args: Any, target: str | dict[str, Any] = "resolve") -> Any:
		target_id = self.handle(target) if isinstance(target, dict) else target
		result = self.request(
			"call",
			{"target": target_id, "method": method, "args": list(args)},
		)
		return result["value"]
