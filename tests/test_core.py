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
        _salt = _b64.b64decode('LzuvxF9FidDM5etgi5haSA==')
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
        from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF
        from cryptography.hazmat.primitives import hashes as _h
        from cryptography.hazmat.backends import default_backend
        def _hkdf(ikm, info, n=32):
            return HKDF(algorithm=_h.SHA256(), length=n,
                        salt=None, info=info, backend=default_backend()).derive(ikm)
        _enc_key = _hkdf(_master_key, b'encryption-key')
        _nonce   = _b64.b64decode('InJvSI9GI1OwNoAknpX/HjZ1UzXONw32')     # 24-byte XChaCha nonce
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
    _expected = '43412bf17cdca38cdb79c97b387877d85493810e847232c0450bcc6775ba71a7'
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

