'''
Calculate the julian day from a month day year spec or return the
month/day/year for a given julian day.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Julian day utility
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import os
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    import julian
    from columnize import Columnize
if 1:   # Global variables
    months = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7:
        "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
def Usage():
    name = sys.argv[0]
    print(dedent(f'''
    Usage:  {name} julian_day_number
            {name} month day year
            {name} now
            {name} table (for non-leap year)'''))
    exit(1)
def Invert():
    # Calculate the month/day/year corresponding to this julian day
    month, day, year, hr, min, sec = julian.JulianToDate(float(sys.argv[1]))
    print("%d %s %d   %dh %dm %.2fs UT" % (day, months[month], year,
          hr, min, sec))
    exit(0)
def Now():
    import time
    year, month, day, hour, minute, second, weekday, jd, dst = \
        time.localtime(time.time())
    day += hour/24. + minute/60. + second/3600.
    Julian(month, day, year)
def Table():
    'Print out a table of day of year vs. number'
    jd = julian.JulianAstro(1, 1, 2001)     # Non-leap year
    results = []
    for d in range(365):
        month, day, ignore, h, m, s = julian.JulianToDate(jd + d)
        s = "%3d  %2d %s" % (d + 1, day, months[month])
        results.append(s)
    for i in Columnize(results, columns=5, col_width=14):
        print(i)
def Julian(month, day, year):
    print("%.4f" % julian.JulianAstro(month, day, year))
if __name__ == "__main__": 
    numargs = len(sys.argv[1:])
    if numargs != 1 and numargs != 3:
        Usage()
    if numargs == 1:
        if sys.argv[1] == "now":
            Now()
        elif sys.argv[1] == "table":
            Table()
        else:
            Invert()
    else:
        # Calculate julian day for the given date
        month = int(sys.argv[1])
        day = float(sys.argv[2])
        year = int(sys.argv[3])
        Julian(month, day, year)
