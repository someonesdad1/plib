"""
Print monthly payment for mortgage loans
    Print out a table of factors to derive a monthly payment for a
    mortgage, given the interest rate in %/yr and the length of the
    mortgage in years.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2005 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Print monthly payment for mortgage loans
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import math
    import sys
    import getopt
if 1:  # Custom imports
    from wrap import dedent
if 1:  # Global variables
    interest_step = 0.5
    begin_interest = 0.5
    end_interest = 15.0
    years = [3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30]


def Usage(status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options]
      Prints out a mortgage table.
    Options
      -b i      Specify the beginning interest
      -e i      Specify the ending interest
      -s i      Specify the interest step
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-b"] = 0.5
    d["-e"] = 15
    d["-s"] = 0.5
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "b:e:hs:")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for opt in optlist:
        if opt[0] == "-b":
            d["-b"] = float(opt[1])
        if opt[0] == "-e":
            d["-e"] = float(opt[1])
        if opt[0] == "-h":
            Usage(0)
        if opt[0] == "-s":
            d["-s"] = float(opt[1])
    return args


def PrintHeader():
    print(
        dedent("""
    Monthly payment per $1000 principal (compounding period = 1 month)
                                       Years
    %/yr  """),
        end="",
    )
    for year in years:
        print(f"  {year:2d}  ", end="")
    print()
    print("-" * 6, end=" ")
    print("----- " * len(years))


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    PrintHeader()
    interest = d["-b"]
    end_interest = d["-e"]
    interest_step = d["-s"]
    factor_array = []
    while interest <= end_interest:
        # Calculate the current row's factors
        factor_array = []
        for i in range(len(years)):
            tmp = math.pow(1 + interest / 1200, -years[i] * 12)
            factor = 1000 * (interest / 1200) / (1 - tmp)
            factor_array.append(factor)
        # Now print the factors
        print("%5.1f  " % interest, end="")
        for i in range(len(years)):
            fmt = "%5.2f "
            if factor_array[i] < 10:
                fmt = "%5.3f "
            if factor_array[i] >= 100:
                fmt = "%5.1f "
            print(fmt % factor_array[i], end="")
        print()
        interest += interest_step
    print("""
    Use:  Divide the principal in dollars by 1000 and multiply it by the
    factor from the table. 

    Example:  A 10 year loan of $38000 at 5.0% per year will require
    a monthly payment of 38*10.61 = $403.
 
    Formula:  let i = yearly interest in %
                  T = time in years
                  A = (1 + i/1200)**(-T*12)
    Then factor = 1000*(i/1200)/(1 - A)""")
