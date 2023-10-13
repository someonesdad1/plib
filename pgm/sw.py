'''

Wed 16 Aug 2023 11:13:27 AM

    - Update to running with winpython 
    - Print out the starting time of the script
    - The key commands don't work, probably because they are bytestrings
    - Option to change time resolution
    - Option to change the date/time display.  I'd like to see s, min, hr,
      days as units besides the date.
    - Add countdown feature?


Python script to provide stopwatch like behavior.  It is specific to the 32
bit Windows environment.
 
Instructions for use:
    1.  Start the program
    2.  When you press a key, the split time, total elapsed time,
        time/date and key pressed are printed on a line.
 
Special keys are:
 
    q        Quit
    Z        Rezero the timer
    C        Get prompted for a comment
 
If a file is included on the command line, the data are also logged to
that file.
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
        import time
        import string
    if 1:   # Custom imports
        import msvcrt
        from wrap import wrap, dedent
        from color import t
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        # Colors
        t.s = t("purl")
        t.m = t("cynl")
        t.h = t("ornl")
        t.d = t("redl")
        # Holder for global variables
        class G:
            pass
        g = G()
        g.n = 15    # Num spaces for decimal time
        g.display_unit = "s"
        g.allowed_display_units = "smhd"
        g.start = 0         # Integer start time in ns
        g.now = 0           # Integer now in ns
        g.last = 0          # Integer last time in ns
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(spc=False):
        if spc:
            print(f"{t.n}")
        print(dedent(f'''
        {t.n}Commands:
            q       Quit
            ? or /  This help
            Z       Zero time
            C       Enter a comment
            {t.s}s       Display in seconds{t.n}
            {t.m}m       Display in minutes{t.n}
            {t.h}h       Display in hours{t.n}
            {t.d}d       Display in days{t.n}
        Any other keys take a split.  Start with a filename on the command
        line to also have the data appended to that file.  A state summary
        report will be written to the file.
        '''))
        if spc:
            print()
    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = 3         # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        return args
if 1:   # Core functionality
    def Header():
        a = f"{'Diff time':^{g.n}s}"
        b = f"{'Total time':^{g.n}s}"
        c = "-"*g.n
        return dedent(f'''
        Times are in seconds
 
        {a} {b}
        {c} {c}''')
    def Log(str, quiet=0):
        if not quiet:
            print(str)
        if log_stream:
            log_stream.write(str + "\n")
    def Print(key):
        def tof(t):
            'Change t in ns to float in s'
            return float(t)/1e9
        g.now = time.time_ns()   # Integer current time in ns
        # Print split and total time in chosen units.  The decimal
        # resolution is chosen so that holding the space bar down lets you
        # see the last digit change.
        if g.display_unit == "s":
            c = 1
            dt1 = tof(g.now - g.last)/c
            dt2 = tof(g.now - g.start)/c
            s1 = f"{t.s}{dt1:{g.n}.2f}"
            s2 = f"{t.s}{dt2:{g.n}.2f}"
        elif g.display_unit == "m":
            c = 60
            dt1 = tof(g.now - g.last)/c
            dt2 = tof(g.now - g.start)/c
            s1 = f"{t.m}{dt1:{g.n}.4f}"
            s2 = f"{t.m}{dt2:{g.n}.4f}"
        elif g.display_unit == "h":
            c = 3600
            dt1 = tof(g.now - g.last)/c
            dt2 = tof(g.now - g.start)/c
            s1 = f"{t.h}{dt1:{g.n}.5f}"
            s2 = f"{t.h}{dt2:{g.n}.5f}"
        elif g.display_unit == "d":
            c = 24*3600
            dt1 = tof(g.now - g.last)/c
            dt2 = tof(g.now - g.start)/c
            s1 = f"{t.d}{dt1:{g.n}.7f}"
            s2 = f"{dt2:{g.n}.7f}{t.n}"
        else:
            raise RuntimeError("{g.display_unit!r} is bad display unit")
        # Get current time string
        loc = time.localtime(tof(g.now) - 7*3600.)
        s = time.strftime("%d%b%Y %H:%M:%S", loc)
        Log(f"{s1} {s2} {s} {key}")
        g.last = g.now
    def GetKey():
        '''Return a string that represents the key pressed.  If the first
        getch() returns a '\000' character, then we call getch() again to
        get the second character and then perform a lookup in the Keys
        dictionary to get the string which represents the key pressed.
        '''
        key = msvcrt.getch().decode()
        if key == '\003':  # Always exit on a ctrl-C
            sys.exit(0)
        if key == '\000':
            key = msvcrt.getch()
            key = "+" + key
        return key

if __name__ == "__main__":
    done = 0
    g.start = time.time_ns()
    g.last = g.start
    log_stream = None

    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    Usage()
    if len(sys.argv) > 1:
        log_stream = open(sys.argv[1], "w")
    Log(Header())
    Print("")
    while True:
        while not msvcrt.kbhit():
            pass
        key = GetKey()
        if key == "q":
            Print("Quitting")
            if log_stream:
                log_stream.close()
            sys.exit(0)
        elif key in "?/":
            Usage(spc=True)
        elif key == "Z":
            start = time.time()
            g.last_time = start
            Log("Time reset")
            Print("Time reset to 0")
        elif key == "C":
            # Prompt the user for a string
            str = input("Enter comment string, '.<cr>' to finish:\n")
            while str != ".":
                Log("+ " + str)
                str = input("")
            Print(key)
        elif len(key) == 1 and key in g.allowed_display_units:
            g.display_unit = key
            Print(key)
        else:
            Print(key)

