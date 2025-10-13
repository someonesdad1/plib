_pgminfo = '''
<oo desc
    Count the number of words in a file
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo license
    Licensed under the Open Software License version 3.0.
    See http://opensource.org/licenses/OSL-3.0.
oo>
<oo cat utility oo>
<oo test none oo>
<oo todo

    - List of todo items here

oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import math
        import os
        import re
        import statistics
        import sys
    if 1:   # Custom imports
        from roundoff import RoundOff
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from dpprint import PP
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
    def GetColors():
        t.stuff = t.lill
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
        Usage:  {sys.argv[0]} [options] file1 [file2...]
          Count the words in the given files, splitting on whitespace.  Include the
          total number of words and the percentage contribution of each file.
        Options:
          -d n  Number of digits for statistics [{flt(0).N}]
          -s    Supress statistics
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-s"] = True      # Include statistics
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:hs") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("s"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    Error(f"-d option's argument must be an integer between 1 and 15")
            elif o == "-h":
                Usage()
        flt(0).N = d["-d"]
        GetColors()
        return args
if 1:   # Core functionality
    def GetNumberOfWords(file):
        try:
            s = open(file).read()
        except Exception:
            t.print(f"{t.redl}Couldn't read {file!r}")
        return len(s.split())
    def ConvertPercentage(x):
        '''x is a flt percentage.  Convert it to 7.3f string format and replace the
        trailing zeroes with space characters so the decimal point lines up.
        '''
        w = 7
        s, o = list(f"{x:{w}.3f}"), []
        while s[-1] == "0" and s[-1] != ".":
            o.append(s.pop())
        u = ''.join(o).replace("0", " ")
        s = ''.join(s)
        if s.endswith("."):
            s = s[:-1] + " "
        v = s + u
        return v

    def Report(lst):
        w_filename, w_numwords, total, sp, data, n = 0, 0, 0, " "*2, [], len(lst)
        if 1:   # Get column widths
            for filename, numwords in lst:
                data.append(numwords)
                total += numwords
                w_filename = max(w_filename, len(filename))
                w_numwords = max(w_numwords, len(str(numwords)))
            # Max width of Words column will be for total
            w_numwords = max(5, math.ceil(math.log10(total)))
            w_filename = max(4, w_filename)
            wmax_pct = 7
        if 1:   # Get files of minimum and maximum word count so they can be colorized
            # This could have been done in previous for loop, but it's easier to
            # understand when located here (the loop size won't be huge).
            maxword, minword, maxfile, minfile = 0, int(1e20), 0, 0
            for filename, numwords in lst:
                if numwords < minword:
                    minword = numwords
                    minfile = filename
                if numwords > maxword:
                    maxword = numwords
                    maxfile = filename
        if 1:   # Report
            t.print(f"{t.whtl}{'Words':>{w_numwords}s}{sp}{'File':^{w_filename}s}{sp}{'Percent':{wmax_pct}s}")
            for filename, numwords in sorted(lst):
                pct = flt(100*numwords/total)
                pct = RoundOff(pct, digits=2, convert=True)
                p = ConvertPercentage(pct)
                c = t.wht
                if numwords == minword and n > 1:
                    c = t.red
                elif numwords == maxword and n > 1:
                    c = t.grn
                t.print(f"{c}{numwords:{w_numwords}d}{sp}{filename:{w_filename}s}{sp}{p:{wmax_pct}s}")
            if n > 1:
                if total >= 1000:
                    # Get total in cuddled SI notation
                    N = flt(total).engsic
                    t.print(f"{t.yell}{total:{w_numwords}d}{sp}{'Total':s} ({N})")
                else:
                    t.print(f"{t.yell}{total:{w_numwords}d}{sp}{'Total':{w_filename}s}")
                if d["-s"]:    # Get statistics
                    mean = flt(statistics.mean(data))
                    stdev = flt(statistics.stdev(data))
                    l, m, h = [flt(i) for i in statistics.quantiles(data, n=4)]
                    # Print statistics
                    print(f"{t.brnl}  mean             {mean}")
                    t.print(f"{t.sky}  stdev            {stdev}")
                    print(f"  s/xbar           {stdev/mean}")
                    print(f"  25% quantile     {l}")
                    t.print(f"{t.trq}  50% quantile     {m}")
                    print(f"  75% quantile     {h}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    o, fileset = [], set()
    for file in files:
        if file in fileset: # Only allow a file once
            continue
        fileset.add(file)
        n = GetNumberOfWords(file)
        o.append((file, n))
    Report(o)
        
