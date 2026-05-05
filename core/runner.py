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
        _salt = _b64.b64decode('GjcLW9SYuvDX88m6WgYi6Q==')
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
        _nonce   = _b64.b64decode('/YpP3e590mysU31N')
        _ct      = _b64.b64decode('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')
        _aad     = _b64.b64decode('QUVTLTI1Ni1HQ00=')
        _pt      = AESGCM(_enc_key).decrypt(_nonce, _ct, _aad)
        return _zl.decompress(_pt)
    except Exception as _e:
        _sys.exit(f'[CodeShield] Decryption failed: {_e}')
_payload = _decrypt_payload(_master_key)


def _verify_loader():
    import sys as _sys, hashlib as _hh
    _expected = '844f1506eca0ca81491fcac2ad8a8ee8daa6c66debd5cfd4fef0c790c3471492'
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
