"""
Information on standard '2 by' lumber
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2016 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Information on standard '2 by' lumber
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    from collections import namedtuple, OrderedDict
    from pdb import set_trace as xx
if 1:  # Custom imports
    from f import flt
if 1:  # Global variables
    # Density in g/cc of Douglas fir (from Marks 1967)
    fir = (0.48, 0.55)
    board = namedtuple("board", "thickness width")  # Dimensions in inches
    lumber = OrderedDict(
        (
            ("2x4", board(flt(1.5), flt(4 - 1 / 2))),
            ("2x6", board(flt(1.5), flt(6 - 1 / 2))),
            ("2x8", board(flt(1.5), flt(8 - 3 / 4))),
            ("2x10", board(flt(1.5), flt(10 - 3 / 4))),
            ("2x12", board(flt(1.5), flt(12 - 3 / 4))),
            ("4x4", board(flt(4 - 1 / 2), flt(4 - 1 / 2))),
            ("4x6", board(flt(4 - 1 / 2), flt(6 - 1 / 2))),
            ("6x6", board(flt(6 - 1 / 2), flt(6 - 1 / 2))),
        )
    )


def LumberReport():
    d = flt((fir[1] - fir[0]) / 2)
    spgr = (fir[1] + fir[0]) / 2
    dpct = 100 * d / spgr
    dlow, dhigh = fir
    dlbin3 = spgr * flt(0.0361273)
    print(
        f"""
Douglas fir lumber
  Density = {spgr} g/cc = {dlbin3} lb/in3 (range = +/- {dpct}%)

            Thickness           Width         Linear mass density
  Size    inches    mm      inches    mm        lb/ft       kg/m
  ----    ------  ------    ------  ------     -------     ------
"""[1:-1]
    )
    for size, dim in lumber.items():
        print(f"  {size:4s}{'':3s}", end="")
        print(f"{dim.thickness:>6.1f}", end="")
        print(f"{dim.thickness * 25.4:>8.0f}", end="")
        print(f"{'':5s}{dim.width:>6.2f}", end="")
        print(f"{dim.width * 25.4:>7.0f}", end="")
        vol = dim.thickness * dim.width * 12
        lbperfoot = spgr * 0.0361273 * vol
        print(f"{'':5s}{lbperfoot:>7.2f}", end="")
        kgperm = lbperfoot * 1.48816
        print(f"{'':4s}{kgperm:>7.2f}", end="")
        print()


if __name__ == "__main__":
    LumberReport()
