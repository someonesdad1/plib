_pgminfo = '''
<oo desc
    Compact calendar
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo license
    Licensed under the Open Software License version 3.0.
    See http://opensource.org/licenses/OSL-3.0.
oo>
<oo cat Put_category_here oo>
<oo test none oo>
<oo todo

    - Use up existing screen space to provide a compact calendar

oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import datetime as DT
        import calendar
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from dpprint import PP
        from util import Len
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:   # Utility
    def GetGlobals():
        GetColors()
        g.lines, g.columns = GetScreen()
        g.oneday = DT.timedelta(days=1)
        g.oneweek = DT.timedelta(days=7)
        g.daysheader = deque("Mo Tu We Th Fr Sa Su".split())
        g.months = "xxx Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
        for i in range(d["-s"]):
            g.daysheader.rotate(-1)
        GetScreen()
    def GetColors():
        t.satsun = t.gryd
        t.satsun = t("#303030")
        t.satsun = t("#404040")
        t.daynames = t.brnl
        t.day1 = t.magl
        t.day = t.wht
        t.today = t("whtl", "blu")
        t.date = t.sky
        t.err = t.redl
        t.dbg = t.lill if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Warn(*msg, status=1):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warn(*msg)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [increment]
          Print a compact calendar to the screen, utilizing as much space as possible
          without scrolling.  The increment can be an integer with cuddled suffixes of w
          for weeks, m for months, or y for years.  Weeks are the default.
        Examples:
            -3w     Start the calendar 3 weeks before the current week
            3y      Start the calendar 3 years ahead
        Options:
            -h      Print a manpage
            -s n    Start day (0 = Monday, 6 = Sunday) [{d["-s"]}]
            -w n    Limit display to this many weeks
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-2"] = False # Use 2 columns
        d["-s"] = 5     # Start day
        d["-w"] = 0     # How many weeks
        #if len(sys.argv) < 2:
        #    Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "2hs:w:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        GetGlobals()
        for o, a in opts:
            if o[1] in list("2"):
                d[o] = not d[o]
            elif o == "-s":
                d[o] = int(a)
                if not (0 <= d[o] <= 6):
                    Error("-s option must be an integer between 0 and 6")
            elif o == "-w":
                try:
                    d[o] = min(abs(int(a)), g.lines - 2)
                except Exception:
                    Error(f"-w option must be an integer")
            elif o == "-h":
                Usage()
        return args
if 1:   # Core functionality
    def add_months(sourcedate, months):
        # From https://stackoverflow.com/questions/4130922/how-to-increment-datetime-by-custom-months-in-python-without-using-library
        # David Webb's 9 Nov 2010 answer
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month//12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year, month)[1])
        return DT.date(year, month, day)
    def PrintCompactCalendar(dt):
        def GetWeeks(lines):
            'lines is number of lines, dt is starting date'
            nonlocal dt, col_width
            o, hdr = [], f"{t.daynames}{' '.join(g.daysheader)}{t.n}"
            while Len(hdr) < col_width:
                hdr = hdr + " "
            o.append(hdr)
            lines -= 1
            while lines:
                has_one = False
                ln = []
                for i in range(7):
                    if dt == today:
                        ln.append(f"{t.today}{dt.day:2d}{t.n}")
                        if dt.day == 1:
                            has_one = True
                    elif dt.day == 1:
                        has_one = True
                        ln.append(f"{t.day1}{dt.day:2d}{t.n}")
                    elif dt.weekday() in (5, 6):
                        ln.append(f"{t.satsun}{dt.day:2d}{t.n}")
                    else:
                        ln.append(f"{t.day}{dt.day:2d}{t.n}")
                    dt += g.oneday
                if has_one:
                    ln.append(f"{t.date}{g.months[dt.month]} {dt.year}{t.n}")
                s = ' '.join(ln)
                while Len(s) < col_width:
                    s = s + " "
                o.append(s)
                lines -= 1
            return o

        dow, lines = dt.weekday(), g.lines - 1
        col_width = 29
        today = DT.date.today()
        if d["-w"]:
            lines = d["-w"] + 1
        # If the day of the week of dt is not at the proper starting day, decrement it
        # until it is
        while dt.weekday() != d["-s"]:
            dt -= g.oneday
        o1 = GetWeeks(lines) # Weeks for column 1
        o2 = GetWeeks(lines) # Weeks for column 2
        if d["-2"]:
            sep = " "*10
            sep = [sep]*len(o1)
            for a, b, c in zip(o1, sep, o2):
                print(a + b + c)
        else:
            for i in o1:
                print(i)

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if not args:
        args = ["0"]
    increment = args[0].strip()
    duration = "w"
    dt = DT.date.today()
    if increment[-1] in "wmy":
        duration = increment[-1]
        increment = increment[:-1]
    increment = int(increment)
    if increment:
        if duration == "w":
            dt += DT.timedelta(weeks=increment)
        elif duration == "m":
            dt = add_months(dt, increment)
        elif duration == "y":
            dt = DT.date(year=dt.year + increment, month=dt.month, day=dt.day)
        else:
            raise TypeError("Duration bug")
    Dbg(f"Starting on date {dt}")
    PrintCompactCalendar(dt)
