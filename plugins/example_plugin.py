"""
plugins/example_plugin.py — Example LoadStrike Pro v9 plugin

To use: python loadstrike.py https://example.com --plugin plugins/example_plugin.py

This plugin demonstrates:
1. Content validation — every response must contain a required string
2. Request signing   — adds HMAC-SHA256 signature to every request
3. Custom metrics    — tracks and prints its own stats at the end
"""

import hmac, hashlib, time, re
from plugins import BasePlugin


class ContentValidatorPlugin(BasePlugin):
    """
    Validates that responses contain expected content.
    Configurable via environment variable LOADSTRIKE_EXPECTED_BODY.
    """
    name = "content_validator"

    def __init__(self):
        import os
        self.required  = os.environ.get("LOADSTRIKE_EXPECTED_BODY", "")
        self.checked   = 0
        self.failures  = 0
        self.errors    = {}

    def on_start(self, cfg):
        if self.required:
            print(f"  [ContentValidator] Will check responses for: '{self.required}'")

    def on_response(self, wid, url, status, ms, body):
        if not self.required:
            return
        self.checked += 1
        if self.required.encode() not in body:
            self.failures += 1
            # Track which URLs fail
            self.errors[url] = self.errors.get(url, 0) + 1

    def on_complete(self, snapshot):
        if not self.checked:
            return
        rate = self.failures / self.checked * 100
        print(f"\n  ✔ [ContentValidator] {self.checked} responses checked  "
              f"Failures: {self.failures} ({rate:.1f}%)")
        if self.errors:
            top = sorted(self.errors.items(), key=lambda x: -x[1])[:3]
            for url, n in top:
                print(f"      {n}× {url}")


class RequestSignerPlugin(BasePlugin):
    """
    Adds HMAC-SHA256 signature to every request.
    Configurable via environment variable LOADSTRIKE_SIGNING_SECRET.
    """
    name = "request_signer"

    def __init__(self):
        import os
        secret = os.environ.get("LOADSTRIKE_SIGNING_SECRET", "")
        self.secret = secret.encode() if secret else b""
        self.signed = 0

    def on_start(self, cfg):
        if self.secret:
            print(f"  [RequestSigner] HMAC-SHA256 signing enabled")

    def on_request(self, wid, url, method, headers, body):
        if not self.secret:
            return None
        ts  = str(int(time.time()))
        msg = f"{method}\n{url}\n{ts}".encode()
        sig = hmac.new(self.secret, msg, hashlib.sha256).hexdigest()
        self.signed += 1
        return {
            "headers": {
                **headers,
                "X-Timestamp": ts,
                "X-Signature": f"sha256={sig}",
            }
        }

    def on_complete(self, snapshot):
        if self.signed:
            print(f"\n  ✔ [RequestSigner] Signed {self.signed} requests")


class LatencyTrackerPlugin(BasePlugin):
    """
    Tracks per-URL latency separately from the main stats engine.
    Useful when testing a scenario with multiple endpoints.
    """
    name = "latency_tracker"

    def __init__(self):
        self.url_ms   = {}   # url -> list of ms values
        self.max_urls = 20   # track at most this many unique URLs

    def on_response(self, wid, url, status, ms, body):
        # Normalize URL (strip query string for grouping)
        base = url.split("?")[0]
        if base not in self.url_ms and len(self.url_ms) >= self.max_urls:
            return
        bucket = self.url_ms.setdefault(base, [])
        bucket.append(ms)
        if len(bucket) > 10000:
            self.url_ms[base] = bucket[-5000:]

    def on_complete(self, snapshot):
        if not self.url_ms:
            return
        print(f"\n  ✔ [LatencyTracker] Per-endpoint latency:")
        print(f"  {'URL':<55} {'N':>7} {'avg':>8} {'p95':>8}")
        print(f"  {'─'*80}")
        for url, ms_vals in sorted(self.url_ms.items()):
            srt = sorted(ms_vals)
            avg = sum(srt) / len(srt)
            p95 = srt[min(int(len(srt)*0.95), len(srt)-1)]
            print(f"  {url[:55]:<55} {len(ms_vals):>7,} "
                  f"{avg:>7.1f}ms {p95:>7.1f}ms")
