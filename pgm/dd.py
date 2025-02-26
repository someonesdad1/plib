"""
Thread double depths
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Thread double depths
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import os
if 1:  # Custom imports
    from wrap import dedent
    from columnize import Columnize
if 1:  # Global variables
    tpi_lathe = set(
        (
            4,
            4.5,
            5,
            5.5,
            5.75,
            6,
            6.5,
            6.75,
            7,
            8,
            9,
            10,
            11,
            11.5,
            12,
            13,
            13.5,
            14,
            16,
            18,
            20,
            22,
            23,
            24,
            26,
            27,
            28,
            32,
            36,
            40,
            44,
            46,
            48,
            52,
            54,
            56,
            64,
            72,
            80,
            88,
            92,
            104,
            108,
            112,
            128,
            144,
            160,
            176,
            184,
            192,
            208,
            216,
            224,
        )
    )
    tpi_lathe = sorted(list(tpi_lathe))
    oq, oh, tq = "¼ ½ ¾".split()
    s = "20 30 35 40 45 50 60 70 80 100 125 150 175 200 250 300 400"
    metric_pitches = [int(i) / 100 for i in s.split()]


def DD(tpi):
    "Return double depth of vee thread in inches for given tpi"
    return round(3**0.5 / tpi, 3)


def TPI(tpi):
    "Return a string representing the tpi; substitute for fractions"
    fp, f = tpi - int(tpi), ""
    if fp == 0.25:
        f = oq
    elif fp == 0.5:
        f = oh
    elif fp == 0.75:
        f = tq
    return str(int(tpi)) + f


def FP(tpi):
    return f"{tpi:.4f}"


def Metric():
    print("\nMetric threads:")
    s = []
    for p in metric_pitches:
        tpi = 25.4 / p
        s.append((str(p), FP(DD(tpi))))
    t = ["p,mm  DD_vee"]
    fmt = "{:^4s} {:5s}"
    for i in s:
        t.append(fmt.format(*i))
    for i in Columnize(t, indent=" " * 2, sep=" " * 4):
        print(i)


def Clausing():
    print("Clausing 5914 lathe threads:")
    s = []
    for tpi in tpi_lathe:
        s.append((TPI(tpi), FP(DD(tpi))))
    t = ["tpi  DD_vee"]
    fmt = "{:^4s} {:5s}"
    for i in s:
        t.append(fmt.format(*i))
    for i in Columnize(t, indent=" " * 2, sep=" " * 4):
        print(i)


def ClausingMetricPitch():
    print(f"""\n{"Clausing lathe threads, pitch in mm":^{w}s}""")
    s = []
    for tpi in tpi_lathe:
        p = 25.4 / tpi
        s.append((TPI(tpi), f"{p:.3f}"))
    t = ["tpi  p, mm"]
    fmt = "{:^4s} {:5s}"
    for i in s:
        t.append(fmt.format(*i))
    for i in Columnize(t, indent=" " * 2, sep=" " * 4):
        print(i)


if __name__ == "__main__":
    w = int(os.environ.get("COLUMNS", 80)) - 1
    print(f"{'Double Depths of Vee Threads (in inches)':^{w}s}")
    Clausing()
    Metric()
    print("\nUN double depths are 3/4 of vee thread DD")
    ClausingMetricPitch()
