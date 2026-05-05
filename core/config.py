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
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat.primitives import hashes as _hashes
        from cryptography.hazmat.backends import default_backend
        _salt = _b64.b64decode('t7XmKuiUYG4JIg1JkSWfTA==')
        _fp = b'OxTrace-portable-key-material'
        kdf = PBKDF2HMAC(algorithm=_hashes.SHA512(), length=32,
                          salt=_salt, iterations=600000,
                          backend=default_backend())
        return kdf.derive(_fp)
    except Exception as _e:
        _sys.exit(f'[CodeShield] KDF error: {_e}')

_master_key = _derive_master()


def _decrypt_payload(_master_key):
    import sys as _sys
    try:
        from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF
        from cryptography.hazmat.primitives import hashes as _h
        from cryptography.hazmat.backends import default_backend
        def _hkdf(ikm, info, n=32):
            return HKDF(algorithm=_h.SHA256(), length=n,
                        salt=None, info=info, backend=default_backend()).derive(ikm)
        _enc_key = _hkdf(_master_key, b'encryption-key')
        _nonce   = _b64.b64decode('jvvz7UJ53L0kvT8s')
        _ct      = _b64.b64decode('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')
        _aad     = _b64.b64decode('Q2hhQ2hhMjAtUG9seTEzMDU=')
        _pt      = ChaCha20Poly1305(_enc_key).decrypt(_nonce, _ct, _aad)
        return _zl.decompress(_pt)
    except Exception as _e:
        _sys.exit(f'[CodeShield] Decryption failed: {_e}')
_payload = _decrypt_payload(_master_key)


def _verify_loader():
    import sys as _sys, hashlib as _hh
    _expected = 'ff3677de39ac0aaad34e855cc53f86e645df9b49214b99a5bde0b386bd9a8958'
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

