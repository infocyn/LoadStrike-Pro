"""modes/har_playback.py v11 — HAR (HTTP Archive) playback mode.

Replays recorded browser sessions from .har files.
HAR format is the standard output of Chrome DevTools, Fiddler, Charles Proxy,
Postman, and most modern HTTP recording tools.

Usage:
    python loadstrike.py https://example.com -m har --har-file recording.har
    python loadstrike.py https://example.com --config test.yaml  # har.file in yaml

Why this matters:
    Instead of crafting synthetic requests, HAR playback replays real user
    journeys — including auth flows, API calls, and asset loading —
    giving much more realistic load patterns.
"""

import asyncio, json, time, random, os
from typing import List, Optional
from core.stats  import Stats, Rec
from core.config import Cfg, HarCfg


def _load_har(path: str) -> List[dict]:
    """Parse HAR file and return list of request entries."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    entries = data.get("log", {}).get("entries", [])
    return entries


def _har_rec(wid: int, url: str, method: str, ms: float,
              status: Optional[int] = None, bytes_in: int = 0,
              err: Optional[str] = None) -> Rec:
    return Rec(
        status=status, ms=ms,
        bytes_in=bytes_in, bytes_out=0,
        error=err, ts=time.time(),
        worker_id=wid, url=url, method=method, phase="main",
    )


async def har_playback_worker(wid: int, session, stats: Stats, cfg: Cfg):
    """
    Replays HAR entries sequentially, one full pass per loop iteration.
    Timing between requests is preserved (scaled by har.speed).
    """
    import aiohttp
    har_cfg = cfg.har
    path = har_cfg.file or cfg.har_file

    if not path or not os.path.exists(path):
        from core.colors import C
        print(f"  {C.RED}✗ HAR file not found: {path!r}{C.R}")
        return

    entries = _load_har(path)

    # Filter by URL substring if configured
    if har_cfg.filter_url:
        entries = [e for e in entries
                   if har_cfg.filter_url in e.get("request", {}).get("url", "")]

    if not entries:
        from core.colors import C
        print(f"  {C.YLW}⚠ No HAR entries to replay{C.R}")
        return

    speed = max(har_cfg.speed, 0.01)

    # Stagger workers so they don't all start at the same position
    if len(entries) > 1:
        start_idx = (wid * (len(entries) // max(1, (len(entries) // 10 + 1)))) % len(entries)
    else:
        start_idx = 0

    while True:
        prev_ts = None

        for i, entry in enumerate(entries[start_idx:] + entries[:start_idx]):
            req = entry.get("request", {})
            url = req.get("url", cfg.url)
            method = req.get("method", "GET").upper()

            # Reconstruct headers
            hdrs = {h["name"]: h["value"]
                    for h in req.get("headers", [])
                    if h["name"].lower() not in ("host", "content-length",
                                                  "transfer-encoding")}

            # Body
            post_data = req.get("postData", {})
            body: Optional[bytes] = None
            if post_data:
                raw = post_data.get("text", "")
                if raw:
                    body = raw.encode("utf-8")

            # Inter-request timing from HAR startedDateTime
            started = entry.get("startedDateTime")
            if prev_ts and started and har_cfg.speed > 0:
                try:
                    from datetime import datetime
                    fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
                    cur_ts = datetime.strptime(started, fmt).timestamp()
                    gap = (cur_ts - prev_ts) / speed
                    if 0 < gap < 30:
                        await asyncio.sleep(gap)
                except Exception:
                    pass
            try:
                from datetime import datetime
                started_str = entry.get("startedDateTime", "")
                if started_str:
                    prev_ts = datetime.strptime(started_str, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
            except Exception:
                pass

            t0  = time.perf_counter()
            err = None
            status = None
            bin_  = 0

            try:
                async with session.request(
                    method, url, headers=hdrs, data=body,
                    allow_redirects=cfg.redirects,
                    timeout=aiohttp.ClientTimeout(total=cfg.timeout_s),
                ) as resp:
                    rb = await resp.read()
                    status = resp.status
                    bin_   = len(rb)
            except asyncio.TimeoutError:
                err = "Timeout"
            except aiohttp.ClientConnectorError as e:
                err = "ConnectError"
            except Exception as e:
                err = type(e).__name__[:40]

            ms = (time.perf_counter() - t0) * 1000
            stats.record(_har_rec(wid, url, method, ms, status, bin_, err))

        if not har_cfg.loop:
            break

        # Small pause between loops to avoid thundering herd
        await asyncio.sleep(random.uniform(0.1, 0.5))
