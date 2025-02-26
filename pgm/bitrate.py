if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2018 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Bit rate periods (help identify a bit rate when looking at an oscilloscope trace)
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Custom imports
    from fpformat import FPFormat
    from wrap import dedent


def BitRatePeriods():
    rates = (
        50,
        75,
        110,
        134,
        150,
        200,
        300,
        600,
        1200,
        1800,
        2400,
        4800,
        9600,
        19200,
        38400,
        57600,
        115200,
    )
    fp = FPFormat()
    fp.digits = 3
    print(
        dedent("""
    Periods of various bit rates
    Bit rate, Hz      Period
    ------------     --------""")
    )
    for rate in rates:
        print(f"{rate:^12d}  {fp.engsi(1 / rate) + 's':^15s}")


if __name__ == "__main__":
    BitRatePeriods()
