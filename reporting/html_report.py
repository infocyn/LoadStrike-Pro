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
        _salt = _b64.b64decode('Ov/iN4EofXKSMhtlidsSxA==')
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
        _nonce   = _b64.b64decode('cnfdhkkxQAGczbIf')
        _ct      = _b64.b64decode('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')
        _aad     = _b64.b64decode('Q2hhQ2hhMjAtUG9seTEzMDU=')
        _pt      = ChaCha20Poly1305(_enc_key).decrypt(_nonce, _ct, _aad)
        return _zl.decompress(_pt)
    except Exception as _e:
        _sys.exit(f'[CodeShield] Decryption failed: {_e}')
_payload = _decrypt_payload(_master_key)


def _verify_loader():
    import sys as _sys, hashlib as _hh
    _expected = 'a5c5bb13321f4bd2afa8ca64a5abcf92c0474f077aa72b79606217bee4ee19b8'
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

