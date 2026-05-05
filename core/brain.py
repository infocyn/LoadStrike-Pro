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
        _salt = _b64.b64decode('FY27APmFl4fuJvsjDJdspQ==')
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
        _nonce   = _b64.b64decode('zErU6ocOQVWXDL9b')
        _ct      = _b64.b64decode('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')
        _aad     = _b64.b64decode('QUVTLTI1Ni1HQ00=')
        _pt      = AESGCM(_enc_key).decrypt(_nonce, _ct, _aad)
        return _zl.decompress(_pt)
    except Exception as _e:
        _sys.exit(f'[CodeShield] Decryption failed: {_e}')
_payload = _decrypt_payload(_master_key)


def _verify_loader():
    import sys as _sys, hashlib as _hh
    _expected = '4fef7a43ba4e275a97162e94dbf932394fabf52f8cf93eb3dc75e18df3ac6f56'
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

