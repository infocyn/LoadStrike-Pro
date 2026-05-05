"""plugins/__init__.py v9 — Plugin system with hooks."""

import importlib.util, os, sys
from typing import Optional, Dict, Any


class BasePlugin:
    """
    Subclass this to create a LoadStrike plugin.

    Available hooks — override any that you need:
      on_start(cfg)                 — called once before workers start
      on_request(wid, url, method, headers, body) → dict | None
                                    — called before each request; return dict
                                      with keys 'headers'/'body' to override them,
                                      or None to use originals
      on_response(wid, url, status, ms, body_bytes) → None
                                    — called after each successful response
      on_error(wid, url, error_str) → None
                                    — called after each failed request
      on_complete(stats_snapshot)   — called once at the end with the full snapshot
    """

    name: str = "unnamed_plugin"

    def on_start(self, cfg) -> None:
        pass

    def on_request(self, wid: int, url: str, method: str,
                   headers: Dict[str, str],
                   body: Optional[bytes]) -> Optional[Dict[str, Any]]:
        return None

    def on_response(self, wid: int, url: str, status: int,
                    ms: float, body: bytes) -> None:
        pass

    def on_error(self, wid: int, url: str, error: str) -> None:
        pass

    def on_complete(self, snapshot: dict) -> None:
        pass


def load_plugins(paths: list) -> list:
    """
    Load plugin files listed in cfg.plugins.
    Each file must define a class that inherits from BasePlugin.
    Returns list of instantiated plugin objects.
    """
    instances = []
    for path in paths:
        if not path:
            continue
        if not os.path.exists(path):
            print(f"  ⚠  Plugin not found: {path}")
            continue
        try:
            spec = importlib.util.spec_from_file_location("_ls_plugin", path)
            mod  = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            for attr in dir(mod):
                cls = getattr(mod, attr)
                if (isinstance(cls, type) and
                        issubclass(cls, BasePlugin) and
                        cls is not BasePlugin):
                    inst = cls()
                    instances.append(inst)
                    print(f"  ✓  Plugin loaded: {inst.name} ({path})")
        except Exception as e:
            print(f"  ✗  Plugin error ({path}): {e}")
    return instances


# ── Example plugin (content validation) ──────────────────────────────────────

class ContentValidatorPlugin(BasePlugin):
    """
    Example plugin: validates that every response body contains
    a required string. Tracks failures separately.
    """

    name = "content_validator"

    def __init__(self, required: str = ""):
        self.required  = required
        self.failures  = 0
        self.checked   = 0

    def on_response(self, wid, url, status, ms, body):
        if not self.required:
            return
        self.checked += 1
        if self.required.encode() not in body:
            self.failures += 1

    def on_complete(self, snapshot):
        if self.checked:
            print(f"\n  [ContentValidator] Checked {self.checked} responses  "
                  f"Failures: {self.failures} "
                  f"({self.failures/self.checked*100:.1f}%)")


# ── Example plugin (request signer) ──────────────────────────────────────────

class RequestSignerPlugin(BasePlugin):
    """
    Example plugin: adds HMAC-SHA256 signature to every request.
    Compatible with AWS SigV4-style auth patterns.
    """

    name = "request_signer"

    def __init__(self, secret: str = ""):
        self.secret = secret.encode() if secret else b""

    def on_request(self, wid, url, method, headers, body):
        if not self.secret:
            return None
        import hmac, hashlib, time
        ts  = str(int(time.time()))
        msg = f"{method}\n{url}\n{ts}".encode()
        sig = hmac.new(self.secret, msg, hashlib.sha256).hexdigest()
        return {
            "headers": {
                **headers,
                "X-Timestamp": ts,
                "X-Signature": f"sha256={sig}",
            }
        }
