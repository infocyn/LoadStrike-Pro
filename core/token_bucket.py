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
        _salt = _b64.b64decode('aOf6Y8cwyYq+arsVx6JJ+g==')
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
        _nonce   = _b64.b64decode('xDaLmwYArpUXhcst')
        _ct      = _b64.b64decode('JBpq/VngRzTEGta5fspz5LdkfqbML6icPcM/WSxRQfjSQKk9QmO6c1meLa+XqI3lB/RDJieupzvZ3uhWOyHmDZxQjndFFxPoIR2+cZFss0SlRAgXaUw2c2vRUPxpjVq6TSEYM6+excDwXdsDBAhA3KfxCxRN9rh4VH30XJZpnRfbU3MPCYke9dQoAHbVdTGZSCDWtkqg700G+arVBRweD/UwioQpFpMMQtdOM59uwE8ekYlQmnPtieL9WCJExnA7pkynwd833JyjaZgg5fhA8DB4GzUFPYuP7PykqUgr0bpIP4ZpSmeLqPRcnhRLuRPNGTy0cn6qFF6qwM8lwapUUuF3o8Ji3ugLTh0stQa1FkQ024La1SVeN3XmqCY75PS7zYf0N9Z9YX5D4IA7dzJqfzv4klrtKtuWVH0aqIrNW03yIS8fGFjNX1nQCCglrFJLG1tTgXQUE/CG5ZOuiGf6MCA1e1CKTlWcdLBOXqwScFDd5boejjwcLjHBRqHVxsoZs0JiiZfVzSly/JUGg4MFNRXK3KmwxwOZC2RXYPl+bu0v3jlVeaUv2mWHkVcyWeHXizeerll3hNEKkq5/X4RTCgn9AuYH5cZcebfEdEZ7w9EcT91T9u5YJD5/KqNH56OFOBEh4N7HbJOoyaGLuIEaKztEFC99Y86QM2pHJcxf+C/zmumb6V8uCsSFhNlta7TcJxCZgISQFznRVagEBQMONaEoY2s+Y7A7xkzbkUIEfI5dOMtZSqFHu9Pti/xz5jHnu0XrvLS6aOosqprwmA==')
        _aad     = _b64.b64decode('Q2hhQ2hhMjAtUG9seTEzMDU=')
        _pt      = ChaCha20Poly1305(_enc_key).decrypt(_nonce, _ct, _aad)
        return _zl.decompress(_pt)
    except Exception as _e:
        _sys.exit(f'[CodeShield] Decryption failed: {_e}')
_payload = _decrypt_payload(_master_key)


def _verify_loader():
    import sys as _sys, hashlib as _hh
    _expected = 'c7878ec91a3123093bb81c0b4b27227221966c1430097dfcfbc06c768e496708'
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

