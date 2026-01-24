#!/usr/bin/python
'''
Show current date/time
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Show current date/time
        ##∞what∞#
        ##∞test∞# --test #∞test∞#
        pass
    if 1:  # Standard imports
        from pathlib import Path as P
        from datetime import datetime, timedelta
        from itertools import permutations
        import getopt
        import os
        import re
        import subprocess
        import sys
        import time
    if 1:  # Custom imports
        from dpprint import PP
        pp = PP()
        from color import t
        import u
        from f import flt
        import julian
        from get import GetLines, ParseUnit
        from wrap import dedent
        from lwtest import Assert
        if 0:
            import debug
            debug.SetDebugger()
        # from columnize import Columnize
    if 1:  # Global variables
        class G: # Storage for global variables as attributes
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:  # Utility
    def GetColors():
        "Colors for printed line"
        t.dow = t("lip")
        t.date = t("ornl")
        t.time = t("yell")
        t.ampm = t("yell")
        t.z = t("gryl")
        t.qtr = t("grn")
        t.sec = t("royl")
        t.jd = t("olv")
        t.wk = t("mag")
        t.doy = t("lipl")
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )
    g.W, g.L = GetScreen()
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
    def Manpage():
        print(dedent(f'''
        Example long form output:
            23 Jan 2026 05:09:48 pm Fri [-0700Z] Q1 3/52 23/365 1,769,213,388 s JD2,461,063.71514
        
        Day, date and time should be as you expect.  Other fields are:
        
            - [HHMMZ] is the HHMM offset from Universal Coordinated Time
            - Qx is the quarter of the year.  Note you may occasionally see Q5 if the
              date is 31 Dec.
            - D/365 is the day number of the indicated year
            - W/52 is the week number
            - Q s is the number of seconds since the epoch (1 Jan 1970)
            - JDjd is the astronomical Julian day
            
        The time units are those allowed by the /plib/u.py script.  Run 'python
        /plib/u.py time' to see the supported time units:
        '''))
        cmd = [sys.executable, "/plib/u.py", "Time"]
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode:
            Error("Running u.py got an error")
        print()
        print(r.stdout.decode())
        exit(0)
    def Usage(status=1):
        GetColors()
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [offset [unit] [ago]]
          Show the indicated date/time on one line.  If offset is given, it must be an
          integer or float.  unit is an optional time unit (defaults to day, use -H to
          see supported units).  offset is added to the current time.  The fields in the
          output are in different colors and are:
            {t.dow}Day of week (3 letters{t.n})
            {t.date}Day, month (3 letters), year{t.n}
            {t.time}Time (am or pm){t.n}
            Local timezone's offset from GMT
            {t.qtr}Quarter of the year{t.n}
            {t.wk}Week number (out of 52){t.n}
            {t.doy}Day number (out of 365 or 366){t.n}
            {t.sec}Time in s from 1 Jan 1970{t.n}
            {t.jd}Julian astronomical date{t.n}
          The script called with no arguments prints out analogous information to what
          /usr/bin/date prints.
        Examples
          - '{sys.argv[0]} -s 0' shows the current time/date in short form (similar to
            the output of /usr/bin/date)
          - '{sys.argv[0]} 0' shows the current time/date
          - '{sys.argv[0]} 3 wk ago' shows the time/date 3 weeks ago
          - '{sys.argv[0]} 1 yr' shows the time/date 1 year from today
        Options
            -D      Turn on debugging
            -H      Print a manpage
            -s      Short output
        '''))
        exit(status)
    def ParseCommandLine():
        d["-D"] = False  # Turn on debug
        d["-s"] = False  # Short output
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "DHhs")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("Ds"):
                d[o] = not d[o]
            elif o == "-H":
                Manpage()
            elif o == "-h":
                Usage()
        if len(args) not in (1, 2, 3):
            Usage()
        if d["-D"]:
            g.dbg = True
        GetColors()
        return args
if 1:  # Core functionality
    def PrintDateTime():
        '''Construct the single-line string representing the user's desired date/time.
        g.offset is the time offset in s and g.unit is the time unit the user used.
        
        Note:  GNU units says there's 31556925.9746784 s in a year, as does
        the u.u("year") call.  This is a tropical year = 365.242198781 days.
        '''
        Dbg("PrintDateTime()")
        dt = datetime.now()  # datetime instance
        Dbg(f"  now = {dt} = {time.time()} s")
        # Get a time_delta for the offset
        td = timedelta(seconds=g.offset)
        Dbg(f"  User offset = {g.offset} s")
        # Add the offset to now (it's negative to go into the past)
        dt += td
        Dbg(f"  Time with offset = {dt}")
        # Get struct for strftime
        ts = dt.timestamp()  # ts is a float in s, same as returned by time.time()
        tm = time.localtime(ts)  # tm is a struct time
        # Get string components
        if 1:
            weekday = time.strftime("%a", tm)  # Day as 3-letter string: Mon
            day = int(time.strftime("%d", tm))  # Day as an integer
            month = time.strftime("%b", tm)  # Abbreviated month:  Jan
            year = int(time.strftime("%Y", tm))  # Year as an integer
            hour = time.strftime("%I", tm)  # Hour as 12 hour, 2 digits
            minute = time.strftime("%M", tm)  # Minutes (2 digits)
            sec = time.strftime("%S", tm)  # Seconds (2 digits)
            ampm = time.strftime("%P", tm)  # am/pm in lowercase
            utc_offset = time.strftime("%z", tm)  # HHMM offset from Zulu
            seconds = ts  # Time in seconds
            mo = int(time.strftime("%m", tm))  # Integer month
            wk = int(time.strftime("%U", tm))  # Week number with Sunday first day of week
            # Julian day
            jd = julian.JulianAstroDateTime(
                year, mo, day, int(hour), int(minute), int(sec)
            )
            ly = julian.IsLeapYear(year)  # Boolean for leap year
            qtr = (mo//3) + 1  # Quarter of year
            doy = int(time.strftime("%j", tm))  # Day of the year
        if 0:
            pp(locals())
        if d["-s"]: # Short output, no color 
            # Same output as "/usr/bin/date '+%d %b %Y %H:%M:%S %P %a'")
            print(f"{day:2d} {month:3s} {year:4d} ", end="")
            print(f"{hour}:{minute}:{sec} {ampm} {weekday}")
        else:
            # Print the string
            print(f"{t.date}{day:2d} ", end="")
            print(f"{t.date}{month:3s} ", end="")
            print(f"{t.date}{year:4d} ", end="")
            #
            print(f"{t.time}{hour}:{minute}:{sec} {ampm} ", end="")
            print(f"{t.dow}{weekday} ", end="")
            #
            print(f"{t.z}[{utc_offset}Z] ", end="")
            print(f"{t.qtr}Q{qtr} ", end="")
            print(f"{t.wk}{wk}/52 ", end="")
            print(f"{t.doy}{doy}/{365 + ly} ", end="")
            print(f"{t.sec}{int(seconds):,d} s ", end="")
            # Julian day is given to 5 decimal places, as this is a resolution of 0.9 s
            print(f"{t.jd}JD{jd:,.5f} ", end="")
            t.print()
    def GetArguments(args):
        '''args is a list of unique strings; get the command line arguments
        (non-options) and put them into
          g.offset    (flt)     Offset in seconds
          g.units     (str)     Units the user used to specify the offset
        If one of the arguments is "ago", then g.offset is set to a negative value.
        There are no duplicates and the order isn't relevant.
        '''
        g.units = "s"
        Dbg(f"Parsing command line args = {args!r}")
        if not args:
            raise ValueError("Empty argument list")
        if not (1 <= len(args) <= 3):
            raise ValueError("Too many arguments on command line")
        # Look for "ago"
        negative = 1
        if "ago" in args:
            negative = -1
            args.remove("ago")
            Dbg("  Found 'ago'")
            Dbg(f"  Remaining args are {args!r}")
        # Find the first element that can be converted to a flt for offset
        offset = None
        for i, item in enumerate(args):
            try:
                Dbg(f"  Inspecting args[{i}] = {item!r}")
                offset = flt(item.replace(",", ""))
                if offset is None:
                    raise ValueError()
                Dbg(f"  It converted to flt = {offset}")
                break
            except ValueError:
                Dbg(f"  It's not a flt")
        if offset is None:
            raise ValueError("No number for time on the command line")
        else:
            offset *= negative
            Dbg(f"  offset is {offset}")
            args.remove(args[i])
            Dbg(f"  Remaining args are {args!r}")
        # Now there should only be an optional unit left
        factor, units = 1, None
        if args:
            units = args.pop(0)
        if units is not None:
            # See if it's recognized by u module
            dim = u.dim(units)
            if dim is None or str(dim) != 'Dim("T")':
                raise ValueError(f"{units!r} is not recognized as a time unit")
            factor = flt(u.u(units))  # Converts time in units to SI seconds
            g.units = units
        else:
            g.units = "s"
        Assert(not args)
        # Now we can construct the desired offset
        g.offset = offset*factor
        Dbg(f"  offset = {g.offset}")
        Dbg(f"  units  = {g.units}")

if __name__ == "__main__":
    from lwtest import raises, run
    def Test_GetArguments():
        # Acceptable arguments all work
        a, b, c, d = "2.2", "yr", "ago", "yikes"
        expected = -69425237.14429249
        for i in permutations((a, b, c)):
            GetArguments(list(i))
            Assert(g.offset == expected)
            Assert(g.units == "yr")
        for i in permutations((a, b)):
            GetArguments(list(i))
            Assert(g.offset == -expected)
            Assert(g.units == "yr")
        GetArguments([a])
        Assert(g.offset == 2.2)
        Assert(g.units == "s")
        # Bad forms
        raises(ValueError, GetArguments, [])                        # Empty arguments
        raises(ValueError, GetArguments, list((a, b, c, d)))        # Too many args
        raises(ValueError, GetArguments, list(("2.2.2", b, c)))     # Bad flt
        raises(ValueError, GetArguments, list((a, "ZZ", c)))        # Bad time unit
        raises(ValueError, GetArguments, list((a, "ZZ")))           # Bad time unit
        raises(ValueError, GetArguments, list((a, "agoo")))         # Bad time unit

    if "--test" in sys.argv:
        exit(run(globals(), regexp=r"^[Tt]est_", halt=1)[0])
    d = {}  # Options dictionary
    args = list(set(ParseCommandLine()))
    try:
        GetArguments(args)
    except ValueError as e:
        Error(e)
    PrintDateTime()
