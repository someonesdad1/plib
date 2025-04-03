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
        from f import flt, log2
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
        Usage:  {sys.argv[0]} [options] m n Hz
          Calculates the worst-case time needed to guess a password of length m symbols
          made up from a set of n symbols by brute force (testing all the combinations
          of symbols).  Hz is the number of computational operations that can be made
          per second.  The total number of passwords is n**m; the time is n**m/Hz.  You
          can cuddle the SI prefixes k, M, G, and T to op_Hz (e.g., '1k').

          Suppose you use the 10 digit characters only and allow passwords of 3 digits.
          You can test passwords at 1000 per s.  For the command line arguments '3 10
          1k', the script reports
                Command line '3 10 1k'
                    10 number of symbols in set (n)
                    3 length of password (m)
                    1000 computations per second
                    1e3 = P = number of possible passwords
                    10.0 password entropy = log2(P)
                    Time to crack password 1 s 
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
    def Calculate(m, n, Hz):
        Assert(ii(m, int) and m > 0)
        Assert(ii(n, int) and n > 0)
        Assert(ii(Hz, flt) and Hz > 0)
        # Set up flt characteristics
        x = flt(0)
        x.high = 9999.999
        x.low = 0.001
        P = n**m
        crack_time_s = ct = flt(P/Hz)
        aoe = flt(13.8e9*u("years"))    # Age of univers
        # Report
        print(f"Command line {' '.join(sys.argv[1:])!r}")
        print(f"    {n} number of symbols in set (n)")
        print(f"    {m} length of password (m)")
        print(f"    {Hz} computations per second")
        print(f"    {flt(P).sci} = P = number of possible passwords")
        print(f"    {log2(P):.1f} password entropy = log2(P)")
        print(f"    Time to crack password {crack_time_s.engsi}s", end=" ")
        # If necessary, user larger time units
        if ct > aoe:
            s = ct/aoe
            print(f"\n       = {s} in units of age of the universe")
        elif ct > 31556926:
            print(f"= {ct/31556926} yr")
        elif ct > 2629743.8:
            print(f"= {ct/2629743.8} months")
        elif ct > 86400:
            print(f"= {ct/86400} days")
        elif ct > 3600:
            print(f"= {ct/3600} hours")
        elif ct > 60:
            print(f"= {ct/60} minutes")
        else:
            print()

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    m = int(args[0])
    n = int(args[1])
    Hz = args[2].strip()
    if Hz[-1] in "QRYZEPTGMk":
        Hz = flt(Hz[:-1])*GetSI(Hz[-1])
    else:
        Hz = flt(Hz)
    Calculate(m, n, Hz)
