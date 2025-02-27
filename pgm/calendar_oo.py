"""
This script will generate text output that can be imported into an
Open Office document and formatted as a calendar.  The output has the
numbers and days separated by tab characters.  This allows you to
import the data into OO Writer or OO Calc.
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
    # Generate text that can be imported into an Open Office document
    # and formatted as a calendar
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import getopt
    import calendar
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(d, status=1):
    name = sys.argv[0]
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] from_year [to_year]
      Generate text output separated by spaces that can be imported into
      Open Office Writer or Calc to create a calendar.  By default, the
      week begins with Sunday.  Use the -m option to begin the week with
      Monday.
    Options:
        -1      Include only first letter of weekday names
        -3      Print only first 3 letters of weekday names
        -m      Begin week with Monday
        -s      Use only the first 3 letters of the month names
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-m"] = False
    d["-1"] = False
    d["-3"] = False
    d["-s"] = False
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "13ms")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for opt in optlist:
        if opt[0] == "-1":
            d["-1"] = True
        if opt[0] == "-3":
            d["-3"] = True
        if opt[0] == "-m":
            d["-m"] = True
        if opt[0] == "-S":
            d["-S"] = True
        if opt[0] == "-s":
            d["-s"] = True
    if len(args) not in (1, 2):
        Usage(d)
    return args


def PrintMonth(year, month, d):
    months = (
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    )
    weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    if d["-1"]:
        weekdays = [i[0] for i in weekdays]
    elif d["-3"]:
        weekdays = [i[:3] for i in weekdays]
    if d["-s"]:
        months = [i[:3] for i in months]
    print(months[month - 1], str(year))
    if not d["-m"]:
        weekdays.insert(0, weekdays.pop())
    print("\t".join(weekdays))
    c = calendar.Calendar(0 if d["-m"] else 6)
    for week in c.monthdatescalendar(year, month):
        wk = []
        for date in week:
            wk.append("" if date.month != month else str(date.day).strip())
        print("\t".join(wk))
    print


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    start = int(args[0])
    end = start if len(args) == 1 else int(args[1])
    if start > end:
        Error("Starting year must be <= ending year")
    for year in range(start, end + 1):
        for month in range(1, 13):
            PrintMonth(year, month, d)
