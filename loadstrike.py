#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════╗
# ║   Developed & Protected by Ox Trace                      ║
# ║   Secure Code Protection Enabled                         ║
# ║   Integrity: SHA-256 Verified                            ║
# ╚══════════════════════════════════════════════════════════╝

# ⚠ This file is cryptographically secured.
# ⚠ Unauthorized analysis, reverse engineering, or modification is strictly prohibited.
# ⚠ Do NOT use this tool on unauthorized systems, networks, or websites.

# ──────────────────────────────────────────────────────────
# Developer      : Ox Trace
# Website        : https://www.infocyn.com/
# Facebook       : https://www.facebook.com/0xTrace
# GitHub         : https://github.com/infocyn
# TikTok         : https://www.tiktok.com/@infocyn
# ──────────────────────────────────────────────────────────

# [ Penetration Tester ⚔️ ] [ Red Teamer ⭕ 🇷🇺 ] — infocyn.com — infocyn 🤝 0xTrace
import sys as _sys, os as _os, base64 as _b64, hashlib as _hl
import zlib as _zl, struct as _st, platform as _pl

def _shield_check():
    import sys as _s, os as _o, time as _t
    # Anti-debug: check for known debugger env vars
    _debug_vars = ['PYTHONDEBUG','PYTHONINSPECT','PYTHONBREAKPOINT']
    for _v in _debug_vars:
        if _o.environ.get(_v):
            raise RuntimeError("Protected: Debugger environment detected")
    # Anti-ptrace on Linux
    if _s.platform == 'linux':
        try:
            _status = open('/proc/self/status').read()
            for _line in _status.splitlines():
                if _line.startswith('TracerPid:'):
                    if int(_line.split(':')[1].strip()) != 0:
                        raise RuntimeError("Protected: Tracing detected")
        except (FileNotFoundError, PermissionError):
            pass
    # Timing check: trivial anti-sleep-patch
    _t0 = _t.perf_counter()
    _dummy = sum(range(1000))
    _elapsed = _t.perf_counter() - _t0
    if _elapsed > 5.0:
        raise RuntimeError("Protected: Execution timing anomaly")
_shield_check()

import hashlib as _hashlib
def _derive_master():
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC as _P
    from cryptography.hazmat.primitives import hashes as _hh
    from cryptography.hazmat.backends import default_backend as _db
    _salt = _b64.b64decode('Xc72r4jgOizap+3gbBxkyWp/dIfsTCFBI1ODW/tgBBQ=')
    _fp   = _b64.b64decode('UDqnAF2svRf/iWxBT2cqIfSb2XW3Xaf9jETsOL2IfH4=')
    _info = _b64.b64decode('+JyzGpPaZN7c/WQvfleINA==')
    _pwd  = _hashlib.sha256(_fp + _info).digest()
    _kdf  = _P(algorithm=_hh.SHA512(), length=32, salt=_salt,
               iterations=600000, backend=_db())
    return _kdf.derive(_pwd)

def _decrypt_payload(_master_key):
    from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305 as _CC
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF as _HK
    from cryptography.hazmat.primitives import hashes as _hh
    from cryptography.hazmat.backends import default_backend as _db
    _hkdf = _HK(algorithm=_hh.SHA256(), length=32, salt=None,
                 info=b'codeshield-payload-key', backend=_db())
    _key   = _hkdf.derive(_master_key)
    _nonce = _b64.b64decode('qCnfLS3EZ/ZzyPzo')
    _ct    = _b64.b64decode('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')
    _aad   = _b64.b64decode('xdlpg9jJYs6PeMMUfDPlvCM8G8KMMud0yAFNVNeXi4E=')
    _cc    = _CC(_key)
    try:
        _plain = _cc.decrypt(_nonce, _ct, _aad)
    except Exception:
        raise RuntimeError("Protected: Authentication failed — payload tampered or wrong runtime")
    _src = _zl.decompress(_plain).decode('utf-8')
    del _plain, _key, _master_key
    return _src

_PAYLOAD_HASH = '3372fd1e181b1fe7f359d761e64a1df40e9957be2e2c5091fa8fda7b98440844'
def _verify_loader():
    import inspect as _ins
    _frame = _ins.currentframe()
    _src   = _ins.getfile(_frame)
    try:
        _raw  = open(_src, 'rb').read()
        _marker = b'_PAYLOAD_HASH = '
        _idx  = _raw.find(_marker)
        if _idx == -1:
            raise RuntimeError("Protected: Loader integrity marker not found")
    except (OSError, IOError):
        pass  # In-memory execution — skip file check

_mk  = _derive_master()
_src = _decrypt_payload(_mk)
del _mk
_co  = compile(_src, '<protected>', 'exec')
del _src
exec(_co, {'__name__': '__main__', '__file__': __file__ if '__file__' in dir() else '<protected>'})
del _co
