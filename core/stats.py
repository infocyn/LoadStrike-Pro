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
        _salt = _b64.b64decode('aFENqoQWyAX+F7hVq/8xnQ==')
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
        _nonce   = _b64.b64decode('xgQQ4DORhunorIDipcUDhzjgObNU41hl')     # 24-byte XChaCha nonce
        _ct      = _b64.b64decode('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')
        _aad     = _b64.b64decode('WENoYUNoYTIwLVBvbHkxMzA1')
        # XChaCha20: derive per-nonce subkey, use trailing bytes as inner nonce
        _subkey  = _hkdf(_enc_key, b'xchacha20-subkey-' + _nonce[:16], 32)
        _sub_n   = _nonce[16:] + bytes(4)             # 96-bit inner nonce
        _pt      = ChaCha20Poly1305(_subkey).decrypt(_sub_n, _ct, _aad)
        return _zl.decompress(_pt)
    except Exception as _e:
        _sys.exit(f'[CodeShield] XChaCha20 decryption failed: {_e}')
_payload = _decrypt_payload(_master_key)


def _verify_loader():
    import sys as _sys, hashlib as _hh
    _expected = '6705f25de4dbd9ddba40eb97e3301b035af8907fe290d13cecd222d6ddf7d310'
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

