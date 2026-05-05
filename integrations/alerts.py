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
        _salt = _b64.b64decode('hUez8SvYPKKTRZTIF/oWRg==')
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
        _nonce   = _b64.b64decode('67kFS6+qYJiiTgqKC+zvZEbXj5URpSsM')     # 24-byte XChaCha nonce
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
    _expected = '980fd1979189a48a5b123a510d15893f64d11346606f92ae588ef964d33bd488'
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

