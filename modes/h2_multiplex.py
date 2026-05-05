"""modes/h2_multiplex.py — True HTTP/2 multiplexing via httpx + h2.

aiohttp does NOT support HTTP/2 multiplexing. This module adds a dedicated
HTTP/2 mode that sends many requests over a single connection, leveraging
H2 stream multiplexing — the same technique used by browsers.

Why this matters:
  HTTP/1.1 keepalive:   1 request per connection at a time (head-of-line blocking)
  HTTP/2 multiplex:     N concurrent requests on 1 TCP connection, no blocking

Requirements:
    pip install httpx[http2] h2

Usage (via CLI):
    python loadstrike.py https://target.com -m h2_multiplex -c 50 -d 30

    -c sets the number of parallel H2 connections.
    Each connection runs --h2-streams requests concurrently (default: 100).
    Total in-flight = concurrency × h2_streams.
"""

import asyncio
import time
import random
from typing import Optional

from core.stats  import Stats, Rec
from core.config import Cfg

try:
    import httpx
    _HAS_HTTPX = True
except ImportError:
    _HAS_HTTPX = False


UA_POOL_H2 = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 "
    "Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
]


def _h2_headers(cfg: Cfg) -> dict:
    return {
        "user-agent":      random.choice(UA_POOL_H2),
        "accept":          "text/html,application/xhtml+xml,*/*;q=0.9",
        "accept-language": "en-US,en;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "cache-control":   "no-cache",
        **{k.lower(): v for k, v in cfg.headers.items()},
    }


async def h2_multiplex_worker(
    wid: int,
    stats: Stats,
    cfg: Cfg,
    streams_per_conn: int = 100,
    phase: str = "main",
):
    """
    One H2 connection that fires `streams_per_conn` requests in parallel.

    Each call to this coroutine represents one persistent HTTP/2 connection.
    The connection is reused for the entire duration of the test.
    """
    if not _HAS_HTTPX:
        from core.colors import C
        print(f"  {C.YLW}⚠ h2_multiplex requires: pip install 'httpx[http2]' h2{C.R}")
        # Graceful fallback to standard HTTP
        from modes.runners import http_keepalive_flood
        import aiohttp
        ssl_ctx = None
        if cfg.url.startswith("https"):
            import ssl
            ssl_ctx = ssl.create_default_context()
            if cfg.no_verify:
                ssl_ctx.check_hostname = False
                ssl_ctx.verify_mode    = ssl.CERT_NONE
        connector = aiohttp.TCPConnector(ssl=ssl_ctx, limit=0)
        async with aiohttp.ClientSession(connector=connector) as sess:
            await http_keepalive_flood(wid, sess, cfg, stats, phase=phase)
        return

    # Build httpx client with HTTP/2 enabled
    limits = httpx.Limits(
        max_connections=1,
        max_keepalive_connections=1,
        keepalive_expiry=cfg.duration + 10,
    )
    timeout = httpx.Timeout(
        connect=cfg.timeout_s,
        read=cfg.timeout_s,
        write=cfg.timeout_s,
        pool=cfg.timeout_s,
    )
    verify = not cfg.no_verify

    async with httpx.AsyncClient(
        http2=True,
        verify=verify,
        limits=limits,
        timeout=timeout,
        follow_redirects=cfg.redirects,
    ) as client:

        async def _one_stream() -> None:
            """Send a single request on the shared H2 connection."""
            hdrs  = _h2_headers(cfg)
            body  = cfg.body.encode() if cfg.body else None
            t0    = time.perf_counter()
            err   = None
            status = None
            bin_   = 0

            try:
                req = client.build_request(
                    cfg.method,
                    cfg.url,
                    headers=hdrs,
                    content=body,
                )
                resp   = await client.send(req)
                status = resp.status_code
                # Drain response to free H2 stream slot
                await resp.aread()
                bin_ = len(resp.content)
            except httpx.TimeoutException as e:
                err = "Timeout"
            except httpx.ConnectError as e:
                err = "ConnectError"
            except httpx.RemoteProtocolError as e:
                err = "ProtocolError"
            except Exception as e:
                err = type(e).__name__[:40]

            ms = (time.perf_counter() - t0) * 1000
            stats.record(Rec(
                status=status, ms=ms,
                bytes_in=bin_, bytes_out=len(body) if body else 0,
                error=err, ts=time.time(),
                worker_id=wid, url=cfg.url,
                method=cfg.method, phase=phase,
            ))

        # Run until the test ends — keep `streams_per_conn` in-flight at all times
        while True:
            # Launch a batch of parallel streams
            await asyncio.gather(*[_one_stream() for _ in range(streams_per_conn)])

            # Respect rate limit (token bucket handled upstream in runner)
            if cfg.delay_ms > 0:
                await asyncio.sleep(cfg.delay_ms / 1000)


async def run_h2_multiplex(cfg: Cfg, stats: Stats,
                           stop_event: asyncio.Event = None) -> None:
    """
    Entry point: spawns cfg.concurrency parallel H2 connections,
    each running h2_multiplex_worker.

    Called from core/runner.py when mode == 'h2_multiplex'.
    """
    if stop_event is None:
        stop_event = asyncio.Event()

    streams = getattr(cfg, "h2_streams", 100)
    tasks   = [
        asyncio.create_task(
            h2_multiplex_worker(i, stats, cfg, streams_per_conn=streams)
        )
        for i in range(cfg.concurrency)
    ]

    # Duration timer — sets stop_event when time is up
    async def _timer():
        await asyncio.sleep(cfg.duration)
        stop_event.set()

    timer = asyncio.create_task(_timer())

    try:
        await stop_event.wait()
    except asyncio.CancelledError:
        pass
    finally:
        timer.cancel()
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, timer, return_exceptions=True)
