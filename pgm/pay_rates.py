"""
Print out a table of revenue in k$ vs time and pay rate.
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
    # Print out a table of revenue as function of hourly wage
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
if 1:  # Custom imports
    from wrap import dedent
if 1:  # Global variables
    rates = (30, 40, 50, 60, 70, 80, 90, 100, 110, 120)
    fmt_start_line = "%2d %2d "
    fmt_kdollars = "%5.1f "
    deduction_pct = 0
    total_weeks = 26


def Header(first_line):
    print(first_line)
    print(" " * 32, "Pay rate $/hr")
    print("Wk Mo", end=" ")
    for rate in rates:
        print("%6d" % rate, end=" ")
    print()


def GrossPay():
    Header("Gross Pay in k$\n")
    for weeks in range(1, total_weeks + 1):
        print(fmt_start_line % (weeks, int(weeks / 4.0)), end=" ")
        for rate in rates:
            dollars = rate * weeks * 40.0 / 1000.0
            print(fmt_kdollars % dollars, end=" ")
        print()
    print()


def NetPay():
    Header("Net Pay in k$ (deductions = %d%%)\n" % deduction_pct)
    for weeks in range(1, total_weeks + 1):
        print(fmt_start_line % (weeks, int(weeks / 4.0)), end=" ")
        factor = (100 - deduction_pct) / 100.0
        for rate in rates:
            dollars = factor * rate * weeks * 40.0 / 1000.0
            print(fmt_kdollars % dollars, end=" ")
        print()
    print()


def DiffPay():
    """This is the difference from making $50k/yr = $24/hr net."""
    Header("Differential Net Pay in k$ (deductions = %d%%)\n" % deduction_pct)
    for weeks in range(1, total_weeks + 1):
        print(fmt_start_line % (weeks, int(weeks / 4.0)), end=" ")
        factor = (100 - deduction_pct) / 100.0
        offset_rate = 24  # In $/hr
        for rate in rates:
            diff_dollars = weeks * 40.0 / 1000.0 * offset_rate
            dollars = factor * rate * weeks * 40.0 / 1000.0 - diff_dollars
            print(fmt_kdollars % dollars, end=" ")
        print()
    print()


def YearlyPay():
    print("Yearly pay in k$ (deductions = %d%%)\n" % deduction_pct)
    print("$/hr     Gross    Net")
    print("----     -----  -----")
    for rate in rates:
        gross = rate * 2.08
        net = gross * (100 - deduction_pct) / 100.0
        print("%3d      %5.1f  %5.1f" % (rate, gross, net))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} inc_tax_pct
          where inc_tax_pct is total withholding percentage you'll experience.
        Example:  
          If you are taxed at the 40% rate, then if you make $80/hr and
          work for 6 weeks, your net pay will be $11.5k.  Check:  6 weeks
          at 40 hours per week is 240 hours.  $80/hr time 240 hr is $19.2k.
          60% of this is $11.52k.
        """)
        )
        exit(1)
    deduction_pct = float(sys.argv[1])
    GrossPay()
    NetPay()
    # DiffPay()
    YearlyPay()
