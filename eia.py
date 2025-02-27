"""
Module to provide EIA resistance values along with a custom set of
on-hand resistances.
"""

if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2010 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # <electrical> Provides EIA resistor values (based on IEC 60063
    # preferred numbers).
    ##∞what∞#
    ##∞test∞# ignore #∞test∞#
    # Custom imports
    from roundoff import RoundOff

    # Global variables
    __all__ = """EIA EIA_series OnHand """.split()
    # The following iterable defines the powers of 10 to use to get
    # commonly-available resistors.
    powers_of_10 = (-1, 0, 1, 2, 3, 4, 5, 6, 7)

    # EIA recommended resistor significand values.  From
    # https://en.wikipedia.org/wiki/E_series_of_preferred_numbers
    def f(x):
        return tuple([int(i) for i in x.split() if i.strip()])

    EIA_series = {
        3: f("""100 220 470"""),
        6: f("""100 150 220 330 470 680"""),
        12: f("""100 120 150 180 220 270 330 390 470 560 680 820"""),
        24: f("""100 110 120 130 150 160 180 200 220 240 270 300 330
                    360 390 430 470 510 560 620 680 750 820 910"""),
        48: f("""100 105 110 115 121 127 133 140 147 154 162 169 178
                    187 196 205 215 226 237 249 261 274 287 301 316 332
                    348 365 383 402 422 442 464 487 511 536 562 590 619
                    649 681 715 750 787 825 866 909 953"""),
        96: f("""100 102 105 107 110 113 115 118 121 124 127 130 133
                    137 140 143 147 150 154 158 162 165 169 174 178 182
                    187 191 196 200 205 210 215 221 226 232 237 243 249
                    255 261 267 274 280 287 294 301 309 316 324 332 340
                    348 357 365 374 383 392 402 412 422 432 442 453 464
                    475 487 499 511 523 536 549 562 576 590 604 619 634
                    649 665 681 698 715 732 750 768 787 806 825 845 866
                    887 909 931 953 976"""),
        192: f("""100 101 102 104 105 106 107 109 110 111 113 114 115
                    117 118 120 121 123 124 126 127 129 130 132 133 135
                    137 138 140 142 143 145 147 149 150 152 154 156 158
                    160 162 164 165 167 169 172 174 176 178 180 182 184
                    187 189 191 193 196 198 200 203 205 208 210 213 215
                    218 221 223 226 229 232 234 237 240 243 246 249 252
                    255 258 261 264 267 271 274 277 280 284 287 291 294
                    298 301 305 309 312 316 320 324 328 332 336 340 344
                    348 352 357 361 365 370 374 379 383 388 392 397 402
                    407 412 417 422 427 432 437 442 448 453 459 464 470
                    475 481 487 493 499 505 511 517 523 530 536 542 549
                    556 562 569 576 583 590 597 604 612 619 626 634 642
                    649 657 665 673 681 690 698 706 715 723 732 741 750
                    759 768 777 787 796 806 816 825 835 845 856 866 876
                    887 898 909 920 931 942 953 965 976 988"""),
    }
if 1:  # Utility

    def rtz(s):
        "Remove trailing zeros from string s"
        if "." not in s:
            return s
        while s and s[-1] == "0":
            s = s[:-1]
        return s

    def Int(x):
        """If the string form of the float x ends in ".0", return it as an
        integer; otherwise, return it unchanged.
        """
        x = RoundOff(x)
        return int(x) if str(x).endswith(".0") else x


def OnHand():
    "Return a list of on-hand resistors"
    return list(
        sorted(
            set(
                [
                    0.025,
                    0.2,
                    0.27,
                    0.33,
                    1,
                    2.2,
                    4.6,
                    8.3,
                    10.1,
                    12,
                    14.7,
                    15,
                    17.8,
                    22,
                    27,
                    28.4,
                    30,
                    31.6,
                    33,
                    35,
                    38.4,
                    46.3,
                    50,
                    55.5,
                    61.8,
                    67,
                    75,
                    78,
                    81,
                    100,
                    110,
                    115,
                    121,
                    150,
                    162,
                    170,
                    178,
                    196,
                    215,
                    220,
                    237,
                    268,
                    270,
                    287,
                    316,
                    330,
                    349,
                    388,
                    465,
                    500,
                    513,
                    546,
                    563,
                    617,
                    680,
                    750,
                    808,
                    822,
                    980,
                    1_000,
                    1_100,
                    1_180,
                    1_210,
                    1_330,
                    1_470,
                    1_500,
                    1_620,
                    1_780,
                    1_960,
                    2_160,
                    2_200,
                    2_370,
                    2_610,
                    2_720,
                    3_000,
                    3_160,
                    3_300,
                    3_470,
                    3_820,
                    4_640,
                    5_000,
                    5_530,
                    6_800,
                    6_840,
                    8_000,
                    8_300,
                    9_090,
                    10_000,
                    11_800,
                    12_100,
                    13_300,
                    15_000,
                    16_200,
                    17_800,
                    18_000,
                    19_500,
                    20_000,
                    22_000,
                    26_200,
                    33_000,
                    39_000,
                    42_400,
                    46_000,
                    51_000,
                    55_000,
                    67_000,
                    75_000,
                    82_000,
                    100_000,
                    120_000,
                    147_000,
                    162_000,
                    170_000,
                    180_000,
                    220_000,
                    263_000,
                    330_000,
                    390_000,
                    422_000,
                    460_000,
                    464_000,
                    560_000,
                    674_000,
                    820_000,
                    1_000_000,
                    1_200_000,
                    1_500_000,
                    1_700_000,
                    1_900_000,
                    2_200_000,
                    2_400_000,
                    2_600_000,
                    2_800_000,
                    3_200_000,
                    4_000_000,
                    4_800_000,
                    5_600_000,
                    6_000_000,
                    8_700_000,
                    10_000_000,
                    16_000_000,
                    23_500_000,
                ]
            )
        )
    )


def EIA(series, powers=(0, 1, 2, 3, 4, 5, 6)):
    """Return a sorted list of EIA resistors.  powers must be an
    iterable of integers giving the desired powers of 10 to use.
    """
    R = []
    for eia in EIA_series[series]:
        for power in powers:
            R.append(Int(eia * 10**power))
    return list(sorted(set(R)))


if __name__ == "__main__":
    from columnize import Columnize

    # On-hand resistances
    print("On-hand resistances in ohms:")
    # Convert to strings with thousands separator
    ii = isinstance
    oh = [f"{i:,d}" if ii(i, int) else rtz(f"{i:,f}") for i in OnHand()]
    for line in Columnize(oh, indent=" " * 2):
        print(line)
    # EIA resistances
    for n in (3, 6, 12, 24, 48, 96, 192):
        print(f"EIA {n} series:")
        for i in Columnize(EIA(n, (0,)), indent=" " * 2, horiz=True):
            print(i)
