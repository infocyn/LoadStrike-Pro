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
    import sys as _s, os as _o, time as _t, platform as _pl
    # Anti-debug: ptrace detection
    if _pl.system() == 'Linux':
        try:
            status = open('/proc/self/status').read()
            if 'TracerPid:\t0' not in status:
                _s.exit(77)
        except Exception:
            pass
    # Timing check (debugger slows execution)
    t0 = _t.perf_counter()
    _ = sum(range(10000))
    if _t.perf_counter() - t0 > 2.5:
        _s.exit(77)
    # Suspicious env vars
    for _v in ('PYTHONDONTWRITEBYTECODE','PYTHONINSPECT','PYTHONBREAKPOINT'):
        if _o.environ.get(_v,'') not in ('','0'):
            pass   # Allow in dev — just log
_shield_check()


def _get_fp():
    import platform as _pf, hashlib as _hh
    p = [_pf.node(), _pf.machine(), _pf.system()]
    try: p.append(str(__import__('os').getuid()))
    except: p.append('user')
    return _hh.sha256('|'.join(p).encode()).digest()

def _derive_master():
    import sys as _sys
    try:
        from argon2.low_level import hash_secret_raw, Type as _AT
        _salt = _b64.b64decode('VDP9njsAdejqgh6lby5FAw==')
        _fp = b'OxTrace-portable-key-material'
        return hash_secret_raw(
            secret=_fp, salt=_salt,
            time_cost=3, memory_cost=65536, parallelism=4,
            hash_len=32, type=_AT.ID)
    except Exception as _e:
        _sys.exit(f'[CodeShield] KDF error: {_e}')

_master_key = _derive_master()


def _decrypt_payload(_master_key):
    import sys as _sys
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF
        from cryptography.hazmat.primitives import hashes as _h
        from cryptography.hazmat.backends import default_backend
        def _hkdf(ikm, info, n=32):
            return HKDF(algorithm=_h.SHA256(), length=n,
                        salt=None, info=info, backend=default_backend()).derive(ikm)
        _enc_key = _hkdf(_master_key, b'encryption-key')
        _nonce   = _b64.b64decode('KnJDiE7M7zNnkIit')
        _ct      = _b64.b64decode('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')
        _aad     = _b64.b64decode('QUVTLTI1Ni1HQ00=')
        _pt      = AESGCM(_enc_key).decrypt(_nonce, _ct, _aad)
        return _zl.decompress(_pt)
    except Exception as _e:
        _sys.exit(f'[CodeShield] Decryption failed: {_e}')
_payload = _decrypt_payload(_master_key)


def _verify_loader():
    import sys as _sys, hashlib as _hh
    _expected = '1a006d09b39872166bf3a504def98e6d62f4bb616a8e7e5146a23b9b76980268'
    _actual   = _hh.sha256(_payload).hexdigest()
    if _actual != _expected:
        _sys.exit(f'[CodeShield] Integrity check FAILED (expected {_expected[:16]}...)')
_verify_loader()


try:
    import sys as _sys, os as _os
    _file = __file__ if '__file__' in dir() else '<protected>'
    _ns = {
        '__builtins__' : __builtins__,
        '__file__'     : _file,
        '__spec__'     : __spec__    if '__spec__'    in dir() else None,
        '__package__'  : __package__ if '__package__' in dir() else None,
        '__loader__'   : __loader__  if '__loader__'  in dir() else None,
    }
    if __name__ == '__main__':
        _ns['__name__'] = '__main__'
        exec(compile(_payload, _file, 'exec'), _ns)
    else:
        _ns['__name__'] = __name__
        _mod = _sys.modules.get(__name__)
        if _mod is not None:
            _ns = vars(_mod)
            _ns.setdefault('__builtins__', __builtins__)
        exec(compile(_payload, _file, 'exec'), _ns)
except SystemExit:
    raise
except Exception as _xe:
    import sys as _sys, traceback as _tb
    _sys.stderr.write('[CodeShield] Runtime error:\n')
    _tb.print_exc()
    _sys.exit(1)

