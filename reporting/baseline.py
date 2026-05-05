"""reporting/baseline.py v9 — Baseline comparison, trend tracking, CI exit codes."""

import json, os, sys, glob
from core.stats import Stats
from core.config import Cfg
from core.colors import C


def load(path: str) -> dict:
    if not path or not os.path.exists(path):
        return {}
    with open(path) as f:
        d = json.load(f)
    return d.get("summary", d)


def load_multi(pattern: str, limit: int = 5) -> list:
    """Load last N baseline files matching a glob pattern."""
    files = sorted(glob.glob(pattern))[-limit:]
    results = []
    for f in files:
        try:
            with open(f) as fp:
                d = json.load(fp)
            results.append(d.get("summary", d))
        except Exception:
            pass
    return results


def compare(cur: dict, bl: dict) -> list:
    rt_c  = cur.get("rt_ms", {})
    rt_b  = bl.get("rt_ms", {})
    rps_c = cur.get("rps", {})
    rps_b = bl.get("rps", {})

    def d(a, b):
        return round((a - b) / b * 100, 1) if b else 0

    rows = [
        ("P50 latency ms", rt_c.get("p50",0),   rt_b.get("p50",0),  True),
        ("P95 latency ms", rt_c.get("p95",0),   rt_b.get("p95",0),  True),
        ("P99 latency ms", rt_c.get("p99",0),   rt_b.get("p99",0),  True),
        ("Avg latency ms", rt_c.get("avg",0),   rt_b.get("avg",0),  True),
        ("Error rate %",   cur.get("err_rate",0), bl.get("err_rate",0), True),
        ("Avg RPS",        rps_c.get("avg",0),  rps_b.get("avg",0), False),
        ("Peak RPS",       rps_c.get("peak",0), rps_b.get("peak",0),False),
    ]
    out = []
    for name, cv, bv, hiw in rows:
        if bv == 0:
            continue
        diff  = d(cv, bv)
        worse = (diff > 0 and hiw) or (diff < 0 and not hiw)
        out.append((name, cv, bv, diff, worse))
    return out


def print_comparison(rows: list):
    print(f"\n  {C.BOLD}Baseline Comparison{C.R}")
    print(f"  {'Metric':<22} {'Current':>10} {'Baseline':>10} {'Δ%':>8}")
    print(f"  {'─'*54}")
    for name, cv, bv, diff, worse in rows:
        col   = C.RED if worse else C.GRN
        arrow = "↑" if diff > 0 else "↓"
        print(f"  {name:<22} {cv:>10.1f} {bv:>10.1f} "
              f"{col}{arrow}{abs(diff):>5.1f}%{C.R}")


def print_trend(baselines: list, current: dict):
    """Print a sparkline trend over multiple baselines."""
    if len(baselines) < 2:
        return
    print(f"\n  {C.BOLD}Trend (last {len(baselines)} runs){C.R}")
    all_runs = baselines + [current]
    p95_vals = [r.get("rt_ms",{}).get("p95",0) for r in all_runs]
    rps_vals = [r.get("rps",{}).get("avg",0) for r in all_runs]
    max_p95  = max(p95_vals) or 1
    max_rps  = max(rps_vals) or 1
    BLOCKS = " ▁▂▃▄▅▆▇█"

    def spark(vals, mx):
        return "".join(BLOCKS[min(int(v/mx*8), 8)] for v in vals)

    print(f"  P95 ms  {C.YLW}{spark(p95_vals, max_p95)}{C.R}"
          f"  {p95_vals[-1]:.0f}ms (now)")
    print(f"  RPS     {C.CYN}{spark(rps_vals, max_rps)}{C.R}"
          f"  {rps_vals[-1]:.0f} (now)")


def ci_exit(stats: Stats, cfg: Cfg, baseline: dict = None) -> int:
    if not cfg.ci_mode:
        return 0
    t = cfg.thresholds
    breaches = []

    if stats.err_rate > t.max_err_pct:
        breaches.append(f"error_rate {stats.err_rate:.1f}% > {t.max_err_pct}%")
    if stats.p95 > t.max_p95_ms:
        breaches.append(f"p95 {stats.p95:.0f}ms > {t.max_p95_ms:.0f}ms")
    if stats.p99 > t.max_p99_ms:
        breaches.append(f"p99 {stats.p99:.0f}ms > {t.max_p99_ms:.0f}ms")
    if t.min_rps > 0 and stats.avg_rps < t.min_rps:
        breaches.append(f"avg_rps {stats.avg_rps} < {t.min_rps}")

    # Regression check vs baseline
    if baseline and t.regression_pct > 0:
        bl_p95 = baseline.get("rt_ms",{}).get("p95",0)
        if bl_p95 > 0 and stats.p95 > bl_p95 * (1 + t.regression_pct/100):
            delta = (stats.p95/bl_p95 - 1)*100
            breaches.append(
                f"regression: p95 {stats.p95:.0f}ms is {delta:.0f}% above "
                f"baseline {bl_p95:.0f}ms (threshold {t.regression_pct}%)"
            )

    if breaches:
        print(f"\n  {C.RED}{C.BOLD}✗ CI/CD — THRESHOLD BREACHES{C.R}")
        for b in breaches:
            print(f"    {C.RED}• {b}{C.R}")
        print(f"  {C.RED}Exit 1{C.R}\n")
        return 1
    print(f"\n  {C.GRN}✓ CI/CD — all thresholds passed{C.R}\n")
    return 0
