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
        _salt = _b64.b64decode('9z03E06SbVn+1ZDAwl8pLQ==')
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
        _nonce   = _b64.b64decode('BH/B61iSov51yS75lP6/1JKOuxuDZJyb')     # 24-byte XChaCha nonce
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
    _expected = '355afe67ccae3208d47364c208de80983cc1c20ecb64762798caaacbb5aac5f9'
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

