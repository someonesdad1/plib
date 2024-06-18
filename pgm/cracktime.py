'''
Estimate crack time for a password
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
        # Estimate crack time for a password
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import subprocess
        import sys
    if 1:   # Custom imports
        from f import flt
        from u import u
        from si import GetSI
        from lwtest import Assert
        from color import t
        from dpprint import PP
        pp = PP()   # Screen width aware form of pprint.pprint
        from get import GetLines
        from wrap import dedent
        from wsl import wsl     # wsl is True when running under WSL Linux
        from timer import AdjustTimeUnits
        #from columnize import Columnize
    if 1:   # Global variables
        class G:    # Storage for global variables as attributes
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:   # Utility
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def GetColors():
        t.dbg = t("cyn") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.err = t("redl")
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.N}", end="", file=Dbg.file)
    Dbg.file = sys.stdout
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage():
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] N P op_Hz

          Estimates the time needed to crack a password made up from a set of N symbols and that
          uses between 1 and P symbols.  Hz is the number of computational operations that can
          be made per second, such as testing a generated password.  The formula for the total
          number of passwords is the sum of N**i terms where i runs from 1 to P.  The time is this
          total number divided by Hz.  You can cuddle the SI prefixes k, M, G, and T to Hz.

          Example:  modern hash checking machines might run at 100 GHz.  To crack a password made
          up of a set of 100 symbols with a length of up to 16 symbols, use a command line of '100
          16 100G'.  The result is a time of 1e19 s, about 23 times the estimated age of the
          universe. 
        Options:
            -h      Print a manpage
        '''))
        exit(0)
    def ParseCommandLine(d):
        d["-a"] = False     # Describe this option
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o == "-h":
                Usage()
        GetColors()
        g.W, g.L = GetScreen()
        return args
if 1:   # Core functionality
    def Calculate(N, P, Hz):
        Assert(ii(N, int) and N > 0)
        Assert(ii(P, int) and P > 0)
        Assert(ii(Hz, flt) and Hz > 0)
        num_passwds = 0
        for i in range(1, P):
            num_passwds += N**i
        crack_time_s = num_passwds/Hz
        age_of_universe = flt(13.8e9*u("years"))
        if crack_time_s > age_of_universe:
            crack_time = crack_time_s/age_of_universe
            aou = True
        else:
            crack_time = AdjustTimeUnits(crack_time_s, un=True)
            aou = False
        # Report
        print(f"N  = {N} = number of symbols in set")
        print(f"P  = {P} = maximum number of symbols in password")
        print(f"Hz = {P} computation operations per second")
        if aou:
            print(f"t = {crack_time_s} s = time to crack password in s")
            with crack_time:
                crack_time.u = True
                crack_time.N = 2
                print(f"  = {crack_time.sci} in units of the estimated age of the universe")
        else:
            print(f"t = {crack_time_s} s = time to crack password = {crack_time}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    N = int(args[0])
    P = int(args[1])
    Hz = args[2].strip()
    if Hz[-1] in "QRYZEPTGMk":
        Hz = flt(Hz[:-1])*GetSI(Hz[-1])
    else:
        Hz = flt(Hz)
    Calculate(N, P, Hz)
