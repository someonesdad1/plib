"""
Driving costs given $/gallon fuel cost and miles/gallon of car
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Print the cost of driving
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import os
    import sys
    import getopt
    from pdb import set_trace as xx
if 1:  # Custom imports
    from f import flt
    from frange import Sequence
    from wrap import dedent
if 1:  # Global variables
    width = int(os.environ.get("COLUMNS", 80)) - 1
    MPG = Sequence("10:20:1 22:30:2 35:50:5")  # Miles per gallon
    DPG = Sequence("2.8:3.8:0.1")  # Dollars per gallon


def Usage(status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] dist1 [dist2...]
      Calculate the cost of driving a stated distance in miles.
      -t and -r print tables for various $/gal and miles/gal.
    Options:
      -c dpg    Cost of gas in dollars per gallon [{d["-c"]}]
      -m mpg    Car mileage in miles per gallon [{d["-m"]}]
      -t max    Print cost tables to max miles
      -r max    Print range tables to max cost in $
    """)
    )
    exit(status)


def ParseCommandLine():
    d["-c"] = flt(3.5)  # Cost of a gallon of gas
    d["-m"] = flt(20)  # Mileage of car in miles per gallon
    if len(sys.argv) < 2:
        Usage()
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "c:m:r:t:")
    except getopt.GetoptError as str:
        msg, option = str
        out(msg + nl)
        sys.exit(1)
    for o, a in optlist:
        if o == "-c":
            d["-c"] = abs(flt(a))
        elif o == "-m":
            d["-m"] = abs(flt(a))
        elif o == "-r":
            Range(flt(a))
            exit(0)
        elif o == "-t":
            Miles(flt(a))
            exit(0)
    if len(args) < 1:
        Usage()
    return args


def Cost(mi, dpg, mpg, integer=True):
    if integer:
        return str(int(mi * dpg / mpg))
    cost = str(mi * dpg / mpg)
    if cost[-1] == ".":
        return cost[:-1]
    return cost


def Distance(distance, dpg, mpg):
    dist_mi = flt(distance)
    print(f"{dist_mi!s:>7s}       {Cost(dist_mi, dpg, mpg):^6s}")


def Miles(maxdist):
    for mpg in MPG:
        print("-" * width)
        for dpg in DPG:
            MilesTable(maxdist, flt(dpg), flt(mpg))
            print()


def Range(maxcost):
    for mpg in MPG:
        print("-" * width)
        for dpg in DPG:
            RangeTable(maxcost, flt(dpg), flt(mpg))
            print()


def MilesTable(maxdist, dpg, mpg):
    row, Cols = 0, range(0, 100, 10)
    s = f"Gas cost for miles driven (${dpg}/gal, {mpg} mi/gal)"
    print(f"{s:^{width}s}")
    print(" " * 6, end="")
    for col in Cols:
        print(f"{col:^6d}", end=" ")
    print()
    print(" " * 5, end="")
    for i in Cols:
        print(f"{'-' * 4:>6s}", end=" ")
    print()
    while row <= maxdist:
        print(f"{row:4d}  ", end="")
        for col in Cols:
            dist_mi = row + col
            print(f"{Cost(dist_mi, dpg, mpg):^6s} ", end="")
        row += 100
        print()


def RangeTable(maxcost, dpg, mpg):
    row, Cols = 0, range(0, 10, 1)
    s = f"Range in miles for a given gas cost (${dpg}/gal, {mpg} mi/gal)"
    print(f"\n{s:^{width}s}")
    print(" " * 7, end="")
    for i in Cols:
        print(f"{'$' + str(i):>6s}", end=" ")
    print()
    print(" " * 7, end="")
    for i in Cols:
        print(f"{'-' * 4:>6s}", end=" ")
    print()
    while row <= maxcost:
        print(f"{'$' + str(row):>5s}  ", end="")
        for col in Cols:
            cost = row + col
            miles = str(int(mpg / dpg * cost))
            print(f"{miles:>6s} ", end="")
        row += 10
        print()


if __name__ == "__main__":
    d = {}  # Options dictionary
    distances = ParseCommandLine()
    print(f"Costs for gas:  ${d['-c']}/gallon, car gets {d['-m']} mpg")
    print("  Miles       Cost, $")
    print("  -----       -------")
    for distance in distances:
        Distance(distance)
