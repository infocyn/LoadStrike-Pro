"""core/dashboard.py v11."""

from core.colors import C
from core.stats  import Stats
from core.config import Cfg

BANNER = (
    C.CYN + C.BOLD + "\n"
    "  ██╗      ██████╗  █████╗ ██████╗ ███████╗████████╗██████╗ ██╗██╗  ██╗███████╗\n"
    "  ██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║██║ ██╔╝██╔════╝\n"
    "  ██║     ██║   ██║███████║██║  ██║███████╗   ██║   ██████╔╝██║█████╔╝ █████╗  \n"
    "  ██║     ██║   ██║██╔══██║██║  ██║╚════██║   ██║   ██╔══██╗██║██╔═██╗ ██╔══╝  \n"
    "  ███████╗╚██████╔╝██║  ██║██████╔╝███████║   ██║   ██║  ██║██║██║  ██╗███████╗\n"
    "  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝\n"
    + C.R + "\n"
    + C.YLW + "  Pro v11.0  |  Self-Learning L4/L7 Load Testing\n" + C.R
    + C.DIM + "  ⚠  Authorized testing only\n" + C.R
)

SEP    = C.CYN + "─" * 66 + C.R
BLOCKS = " ▁▂▃▄▅▆▇█"


def _spark(vals, w=40):
    if not vals: return C.DIM + "─"*w + C.R
    vs = list(vals[-w:])
    if len(vs) < w: vs = [0.0]*(w-len(vs)) + vs
    mx = max(vs) or 1
    return C.CYN + "".join(BLOCKS[int(v/mx*8)] for v in vs) + C.R


def _bar(v, mx, w=24, col=C.GRN):
    f = min(int((v/mx)*w), w) if mx else 0
    return col + "█"*f + C.DIM + "░"*(w-f) + C.R


def _rt_col(ms):
    if ms > 5000: return C.RED
    if ms > 2000: return C.YLW
    return C.GRN


def _ec(r):
    if r > 50: return C.RED
    if r > 20: return C.YLW
    return C.GRN


_PH = {
    "warmup": (C.BLU,  "◉ WARM-UP"),
    "rampup": (C.YLW,  "◉ RAMP-UP"),
    "main":   (C.GRN,  "◉ RUNNING"),
    "done":   (C.DIM,  "◉ DONE"),
    "l4":     (C.MAG,  "◉ L4 MODE"),
}


class Dashboard:
    def __init__(self, stats: Stats, cfg: Cfg):
        self.stats   = stats
        self.cfg     = cfg
        self.phase   = "main"
        self.running = True
        self._alerts: list = []

    def alert(self, msg: str):
        self._alerts.append(msg[-80:])
        if len(self._alerts) > 3: self._alerts.pop(0)

    def _render(self):
        st  = self.stats
        cfg = self.cfg
        el  = st.elapsed
        rem = max(0, cfg.duration - el)
        col, lbl = _PH.get(self.phase, (C.WHT, self.phase.upper()))
        L = []
        L.append(SEP)
        L.append(f"  {C.BOLD}⚡ LoadStrike Pro v11{C.R}  {col}{lbl}{C.R}"
                 f"  {C.DIM}elapsed {el:.0f}s  remain {rem:.0f}s{C.R}")
        L.append(f"  {C.DIM}▸ {cfg.url}  mode={cfg.mode}"
                 f"  workers={st.active_workers}/{cfg.concurrency}{C.R}")
        L.append(SEP)
        L.append(f"  {C.BOLD}Requests{C.R}")
        L.append(f"    Total  {C.WHT}{st.total:>9,}{C.R}"
                 f"   ✓ {C.GRN}{st.success:,}{C.R}"
                 f"   ✗ {C.RED}{st.failed:,}{C.R}"
                 f"   Timeout {C.YLW}{st.timeouts:,}{C.R}")
        L.append(f"    Err    {_ec(st.err_rate)}{st.err_rate:>5.1f}%{C.R}"
                 f"   ConnErr {C.RED}{st.conn_errors:,}{C.R}"
                 f"   Data↓ {C.MAG}{st.mb_in:.2f} MB{C.R}")
        L.append(f"  {C.BOLD}Throughput{C.R}  (last 40s)")
        L.append(f"  {_spark(st.rps_hist)}  {C.BOLD}{C.WHT}{st.cur_rps:.0f} rps{C.R}")
        L.append(f"  avg {C.CYN}{st.avg_rps}{C.R} rps"
                 f"   peak {C.YLW}{st.peak_rps}{C.R} rps")
        L.append(f"  {C.BOLD}Latency (ms){C.R}")
        L.append(f"  P95 {_bar(st.p95, max(st.p95, 2000), 24, _rt_col(st.p95))}"
                 f" {_rt_col(st.p95)}{st.p95}{C.R}")
        L.append(f"  min {C.GRN}{st.min_rt}{C.R}"
                 f"  avg {_rt_col(st.avg_rt)}{st.avg_rt}{C.R}"
                 f"  p50 {C.GRN}{st.p50}{C.R}"
                 f"  p90 {C.YLW}{st.p90}{C.R}"
                 f"  p99 {C.RED}{st.p99}{C.R}"
                 f"  max {C.RED}{st.max_rt}{C.R}")
        if st.status_codes:
            sc = "  ".join(
                f"{(C.GRN if k < 400 else C.RED)}{k}{C.R}:{C.WHT}{v}{C.R}"
                for k, v in sorted(st.status_codes.items()))
            L.append(f"  {C.BOLD}Status{C.R}  {sc}")
        else:
            L.append(f"  {C.DIM}No responses yet{C.R}")
        if st.errors:
            top = sorted(st.errors.items(), key=lambda x: -x[1])[:2]
            L.append(f"  {C.BOLD}Errors{C.R}  " +
                     "  ".join(f"{C.RED}{k[:35]}{C.R}:{v}" for k, v in top))
        else:
            L.append("")
        for a in self._alerts:
            L.append(f"  {C.RED}{C.BOLD}⚠{C.R}  {a}")
        L.append(SEP)
        L.append(f"  {C.DIM}Ctrl+C to stop   mode={cfg.mode}   "
                 f"proxy={'on' if cfg.proxy.url else 'off'}{C.R}")
        return L

    def stop(self):
        self.running = False
