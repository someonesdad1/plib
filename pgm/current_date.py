#!/usr/bin/python
'''
Show current date/time
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Show current date/time
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from pathlib import Path as P
        from datetime import datetime, timedelta
        import getopt
        import os
        import re
        import subprocess
        import sys
        import time
    if 1:   # Custom imports
        from dpprint import PP
        pp = PP()
        from color import t
        from u import u
        from f import flt
        import julian
        from get import GetLines
        from wrap import dedent
        if 0:
            import debug
            debug.SetDebugger()
        #from columnize import Columnize
    if 1:   # Global variables
        class G:
            # Storage for global variables as attributes
            pass
        g = G()
        g.dbg = False
        t.dbg = t("lill")
        ii = isinstance
if 1:   # Utility
    def GetColors():
        'Colors for printed line'
        t.dow = t("lip")
        t.date = t("ornl")
        t.time = t("yell")
        t.ampm = t("yell")
        t.z = t("gryd")
        t.qtr = t("grn")
        t.sec = t("royl")
        t.jd = t("olv")
        t.wk = t("mag")
        t.doy = t("lipl")
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    g.W, g.L = GetScreen()
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.n}", end="", file=Dbg.file)
    Dbg.file = sys.stderr   # Debug printing to stderr by default
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(dedent(f'''
        Day, date and time should be as you expect.  Other fields are:

            - [....Z] is the HHMM offset from Universal Coordinated Time
            - Qx is the quarter of the year
            - x/365 is the day number of the indicated year
            - x/52 is the week number
            - x s is the number of seconds since the epoch (1 Jan 1970)
            - JDx is the astronomical Julian day

        The time units are those allowed by the /plib/u.py script.  Run
        'python /plib/u.py time' to see the supported time units:

        '''))
        cmd = [sys.executable, "/plib/u.py", "Time"]
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode:
            Error("Running u.py got an error")
        print(r.stdout.decode())
        print(dedent(f'''
         See?
        '''))
        exit(0)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [offset [unit]]
          Show the indicated date/time on one line.  If offset is given, it
          must be an integer or float.  unit is an optional time unit
          (defaults to day, use -h to see details).  offset is added to the
          current time.  The fields in the output are in different colors
          and are:
            Day of week (3 letters)
            Day, month (3 letters), year
            Time (am or pm)
            Local timezone's offset from GMT
            Quarter of the year
            Week number (out of 52)
            Day number (out of 365 or 366)
            Time in s from 1 Jan 1970
            Julian astronomical date
        Examples
          - '{sys.argv[0]} -- -3 wk' shows the time/date 3 weeks ago
          - '{sys.argv[0]} 0' shows the current time/date
          - Let x be the value in s printed out by the previous command.
            '{sys.argv[0]} -- -x s' should be within hours of the date of the
            epoch.
        Options
            -d      Turn on debugging
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False     # Turn on debug
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "dh") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("d"):
                d[o] = not d[o]
            elif o == "-h":
                Manpage()
        if len(args) not in (1, 2):
            Usage()
        if d["-d"]:
            g.dbg = True
        GetColors()
        return args
if 1:   # Core functionality
    def PrintDateTime(user_offset, units=None):
        '''Construct the single-line string representing the user's desired
        date/time.
 
        Note:  GNU units says there's 31556925.9746784 s in a year, as does
        the u("year") call.  This is a tropical year = 365.242198781 days.
        '''
        dt = datetime.now()  # datetime instance
        Dbg(f"now = {dt} = {time.time()} s")
        # Get a time_delta for the offset
        try:
            # Get factor to convert offset to SI (seconds).  If no units
            # are given, they default to days.
            factor = u(units) if units else u("day")
        except Exception as e:
            print(f"Exception:  {e}")
            Usage(1)
        offset_s = float(user_offset)*factor
        td = timedelta(seconds=offset_s)
        Dbg(f"user_offset = {user_offset}, units = {units}")
        # Add the offset
        dt += td
        Dbg(f"Time with offset = {dt}")
        # Get struct for strftime
        ts = dt.timestamp()         # ts is a float in s, same as returned by time.time()
        tm = time.localtime(ts)     # tm is a struct time 
        # Get string components
        if 1:
            weekday = time.strftime("%a", tm)       # Day as 3-letter string: Mon
            day = int(time.strftime("%d", tm))      # Day as an integer
            month = time.strftime("%b", tm)         # Abbreviated month:  Jan
            year = int(time.strftime("%Y", tm))     # Year as an integer
            hour = time.strftime("%I", tm)          # Hour as 12 hour, 2 digits
            minute = time.strftime("%M", tm)        # Minutes (2 digits)
            sec = time.strftime("%S", tm)           # Seconds (2 digits)
            ampm = time.strftime("%P", tm)          # am/pm in lowercase
            utc_offset = time.strftime("%z", tm)    # HHMM offset from Zulu
            seconds = ts                            # Time in seconds
            mo = int(time.strftime("%m", tm))       # Integer month
            wk = int(time.strftime("%U", tm))       # Week number with Sunday first day of week
            # Julian day
            jd = julian.JulianAstroDateTime(year, mo, day, int(hour),
                                            int(minute), int(sec))
            ly = julian.IsLeapYear(year)            # Boolean for leap year
            qtr = (mo // 3) + 1                     # Quarter of year
            doy = int(time.strftime("%j", tm))      # Day of the year
        if 0:
            pp(locals())
        # Print the string
        print(f"{t.dow}{weekday} ", end="")
        print(f"{t.date}{day:2d} ", end="")
        print(f"{t.date}{month:3s} ", end="")
        print(f"{t.date}{year:4d} ", end="")
        print(f"{t.time}{hour}:{minute}:{sec} {ampm} ", end="")
        print(f"{t.z}[{utc_offset}Z] ", end="")
        print(f"{t.qtr}Q{qtr} ", end="")
        print(f"{t.wk}{wk}/52 ", end="")
        print(f"{t.doy}{doy}/{365 + ly} ", end="")
        print(f"{t.sec}{int(seconds)} s ", end="")
        print(f"{t.jd}JD{jd:.2f} ", end="")
        t.print()

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if len(args) == 1:
        PrintDateTime(args[0])
    elif len(args) == 2:
        PrintDateTime(*args)
    else:
        Error("Only 1 or 2 arguments allowed (second must be a time unit)")
