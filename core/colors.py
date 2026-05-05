"""core/colors.py — Single source of truth for all ANSI codes."""

class C:
    R    = "\033[0m"
    BOLD = "\033[1m"
    DIM  = "\033[2m"
    RED  = "\033[91m"
    GRN  = "\033[92m"
    YLW  = "\033[93m"
    BLU  = "\033[94m"
    MAG  = "\033[95m"
    CYN  = "\033[96m"
    WHT  = "\033[97m"
    UP   = "\033[F"
    CLR  = "\033[K"
    HC   = "\033[?25l"   # hide cursor
    SC   = "\033[?25h"   # show cursor
