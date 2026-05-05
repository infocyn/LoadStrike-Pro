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
        _salt = _b64.b64decode('mNIg64fW193eFBX+8tZaIA==')
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
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF
        from cryptography.hazmat.primitives import hashes as _h
        from cryptography.hazmat.backends import default_backend
        def _hkdf(ikm, info, n=32):
            return HKDF(algorithm=_h.SHA256(), length=n,
                        salt=None, info=info, backend=default_backend()).derive(ikm)
        _enc_key = _hkdf(_master_key, b'encryption-key')
        _nonce   = _b64.b64decode('gE+ky9S7vTlW188M')
        _ct      = _b64.b64decode('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')
        _aad     = _b64.b64decode('QUVTLTI1Ni1HQ00=')
        _pt      = AESGCM(_enc_key).decrypt(_nonce, _ct, _aad)
        return _zl.decompress(_pt)
    except Exception as _e:
        _sys.exit(f'[CodeShield] Decryption failed: {_e}')
_payload = _decrypt_payload(_master_key)


def _verify_loader():
    import sys as _sys, hashlib as _hh
    _expected = 'ea9b48da012deca07c53d1d34b05b88acb05066000048c8a117f52d9afa8a1e8'
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

