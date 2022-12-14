'''
Transform digits in a string
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Transform digits in a string
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import codecs
        import getopt
        import os
        from pathlib import Path as P
        from string import digits
        import sys
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
    if 1:   # Global variables
        ii = isinstance
        class g: pass
        t.err = t("redl")
        t.output = t("purl")
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] str1 [str2...]
          Transform the digits in the string(s) to "shrouded" values.
          Intended use is to lightly encode things like telephone numbers
          or lock combinations.
        Options:
            -a n    Choose the algorithm [{d['-a']}]
        '''))
        print("The algorithms are:")
        ListAlgorithms()
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = 0         # Choose the algorithm
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "a:h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-a":
                n, m = int(a), len(g.algorithms)
                if n not in range(m):
                    Error(f"-a option must be between 0 and {m - 1}")
                d[o] = n
            elif o == "-h":
                Usage(status=0)
        return args
    def IsOdd(n):
        assert(ii(n, int) and n > 0)
        return bool(n % 2 != 0)
    def Tminus(s):
        'In str s, change digit d to d - 5 except 0'
        if not ii(s, str):
            s = ''.join(s)
        return s.translate(Tminus.f)
    Tminus.f = ''.maketrans("0123456789", "0987654321")
    def ListAlgorithms():
        s = "12345"
        def f(n):
            return g.algorithms[n](s)
        for i, item in enumerate(g.algorithms):
            print(f"  {i} {item.name}")
            for j in item.descr.split("\n"):
                print(f"    {j}")
                print(f"    {s!r} --> {f(i)!r}")
if 1:   # Algorithms
    def TenRev(s):
        'Reverse string s, subtract each digit from 10, 0 -> 0'
        return Tminus(reversed(str(s)))
    TenRev.descr = dedent('''
        Reverse characters and subtract digits from 10.
    ''')
    TenRev.name = "TenRev"
    def TenTwin(s):
        'Reverse adjacent characters, Tminus on digits'
        # Convert string s to list so we can reverse adjacent characters
        lst = list(s)
        n = len(lst)
        # Reverse adjacent characters
        for i in range(0, n - IsOdd(n), 2):
            lst[i], lst[i + 1] = lst[i + 1], lst[i]
        # Tminus the digits
        return Tminus(''.join(lst))
    TenTwin.descr = dedent('''
        Reverse adjacent digits and subtract digits from 10.
        ''')
    TenTwin.name = "TenTwin"
if 1:   # Core functionality
    def PrintResults():
        # Get max column widths
        w0, w1 = 10, 10
        for s0, s1 in g.results:
            w0 = max(w0, len(s0))
            w1 = max(w1, len(s1))
        # Print the algorithm used
        f = g.algorithms[d["-a"]]
        print(f"Used algorithm {f.name!r}\n")
        # Print the header
        t.print(f"{'In':^{w0}s} {t.output}{'Out':^{w1}s}")
        t.print(f"{'-'*w0:s} {t.output}{'-'*w1:s}")
        # Print the data
        for input, output in g.results:
            t.print(f"{input!s:^{w0}s} {t.output}{output!s:^{w1}s}")
    def Transform(s):
        f = g.algorithms[d["-a"]]
        result = f(s)
        if result is not None:
            g.results.append((s, result))

if __name__ == "__main__":
    d = {}      # Options dictionary
    g.algorithms = [
        TenTwin,
        TenRev,
    ]
    g.results = []
    args = ParseCommandLine(d)
    for i in args:
        Transform(i)
    PrintResults()
