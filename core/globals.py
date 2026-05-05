"""core/globals.py — Shared global state to avoid circular imports."""
from typing import Optional

# Token bucket — set by runner.py before workers start
_rate_bucket: Optional[object] = None
