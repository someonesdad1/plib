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
        # Program description string
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
          Transform the integer(s) in the string(s) to "shrouded" values.
        Options:
            -a n    Choose the algorithm [{d['-a']}]
            -l      List the algorithms
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = 0         # Choose the algorithm
        d["-l"] = False     # List the algorithms
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "a:hl") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("l"):
                d[o] = not d[o]
            elif o in ("-a",):
                n = int(a)
                m = len(g.algorithms)
                if n not in range(m):
                    Error(f"-a option must be between 0 and {m - 1}")
                d[o] = n
            elif o == "-h":
                Usage(status=0)
        if d["-l"]:
            ListAlgorithms()
        return args
    def AllDigits(s):
        if not s:
            t.print(f"{t.err}{s!r} is empty")
            return False
        for i in s:
            if i not in digits:
                t.print(f"{t.err}{s!r} is not all digits")
                return False
        return True
    def IsOdd(n):
        assert(ii(n, int) and n > 0)
        return bool(n % 2 != 0)
    def Tminus(s):
        'In str s, change digit d to d - 5 except 0'
        return s.translate(Tminus.f)
    Tminus.f = ''.maketrans("0123456789", "0987654321")
    def ListAlgorithms():
        for i, item in enumerate(g.algorithms):
            print(i, item.name)
            for j in item.descr.split("\n"):
                print(f"    {j}")
        exit(0)
if 1:   # Algorithms
    def TenRev(s):
        'Reverse string s, subtract each digit from 10, 0 -> 0'
        if not AllDigits(s):
            return
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
    def ROT13(s):
        return codecs.encode(s, encoding="rot13")
    ROT13.descr = dedent('''
        Caesar cipher:  rotate by 13 characters
            abcdefghijklmnopqrstuvwxyz
            nopqrstuvwxyzabcdefghijklm
    ''')
    ROT13.name = "ROT13"
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
        ROT13,
    ]
    g.results = []
    args = ParseCommandLine(d)
    for i in args:
        Transform(i)
    PrintResults()
