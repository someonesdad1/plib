'''

Calculate pythagorean triples

'''
_pgminfo = '''
<oo 
    desc
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat oo>
<oo test none oo>
<oo todo oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from primes import FactorList
        from wrap import dedent
        from color import t
        from lwtest import Assert
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
        t.warn = t.ornl
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
        f = sys.stderr
        print(f"{t.warn}", end="", file=f)
        t.print(*msg, file=f)
    def Error(*msg, status=1):
        Warn(*msg)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] n [n1...]
          Calculate the unique Pythagorean triples up to n.
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Need description
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
                    Error(f"-d option's argument must be an integer between 1 and 15")
            elif o == "-h":
                Usage()
        GetColors()
        return args
if 1:   # Core functionality
    def IsATriple(a, b, c):
        if a == b == c:
            return False
        hyp = max(a, b, c)
        l = [a, b, c]
        l.remove(hyp)
        x, y = l
        return x*x + y*y == hyp*hyp
    def Reduce(a, b, c):
        'Remove any common factors from a, b, c and return them in sorted order'
        factors = set(FactorList(a)) & set(FactorList(b)) & set(FactorList(c))
        if factors:
            for factor in factors:
                a, b, c = [i//factor for i in (a, b, c)]
        return tuple(sorted([a, b, c]))
    def PrintTriples(arg):
        try:
            n = int(arg)
            if n < 2:
                raise(Exception())
        except Exception:
            Warn(f"{n!r} is a bad integer")
            return
        triples = set()
        for i in range(1, n + 1):
            for j in range(i, n + 1):
                for k in range(j, n + 1):
                    triple = Reduce(i, j, k)
                    if triple in triples:
                        continue
                    if IsATriple(*triple):
                        triples.add(triple)
        for i in sorted(triples):
            print(*i)
        print("Number of triples =", len(triples))

if __name__ == "__main__":
    d = {}      # Options dictionary
    if 0:
        PrintTriples("100")
        exit()
    args = ParseCommandLine(d)
    for arg in args:
        PrintTriples(arg)
