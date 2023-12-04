'''
Trim characters from the lines of files and print them to stdout
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
        # Trim characters from the lines of files and print them to stdout
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import fileinput
        import getopt
        import os
        from pathlib import Path as P
        import string
        from sys import stdin, stdout, stderr, argv
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
    if 1:   # Global variables
        class G:
            pass
        g = G()  # Storage for global variables as attributes
        g.dbg = False
        ii = isinstance
        g.W = int(os.environ.get("COLUMNS", "80")) - 1
        g.L = int(os.environ.get("LINES", "50"))
if 1:   # Utility
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
            
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {argv[0]} [options] file1 [file2...]
          Trim characters from the lines read from the files and print them
          to stdout.  Use '-' to read from stdin.  If -c is not given, the
          script only removes space characters.
        Options:
            -c set  Define the set of characters to trim
            -l      Trim from the left side only
            -r      Trim from the right side only
            -w      Trim whitespace
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = ""        # Characters to trim
        d["-d"] = False     # Turn on debug printing
        d["-l"] = False     # Trim from left side only
        d["-r"] = False     # Trim from right side only
        d["-w"] = False     # Include whitespace characters
        if len(argv) < 2:
            Usage()
        try:
            opts, files = getopt.getopt(argv[1:], "c:dhlrw") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("dlrw"):
                d[o] = not d[o]
                if o == "-l":
                    d["-r"] = False
                elif o == "-r":
                    d["-l"] = False
            elif o == "-c":
                d[o] += a
            elif o == "-h":
                Usage(status=0)
        if d["-w"]:
            d["-c"] += string.whitespace
        if d["-d"]:
            g.dbg = True
            t.dbg = t("skyl") if g.dbg else ""
            t.norm = t("redl") if g.dbg else ""
            t.N = t.n if g.dbg else ""
        if not files:
            Usage()
        Dbg(f"Files: {' '.join(files)}")
        Dbg(f"  -c = {Escape(d['-c'])!r}")
        Dbg(f"  -l = {d['-l']!r}")
        Dbg(f"  -r = {d['-r']!r}")
        Dbg(f"  -w = {d['-w']!r}")
        return files
if 1:   # Core functionality
    def Escape(s):
        'Escape the characters in the string s and return it'
        def esc(c):
            if ord(c) == 8:
                return r'\t'    # backspace
            elif ord(c) == 9:
                return r'\t'    # horizontal tab
            elif ord(c) == 10:
                return r'\n'    # newline
            elif ord(c) == 11:
                return r'\v'    # vertical tab
            elif ord(c) == 12:
                return r'\f'    # formfeed
            elif ord(c) == 13:
                return r'\r'    # carriage return
            elif ord(c) == 0x5c:
                return r'\\'  # backslash
            return c
        return ''.join([esc(i) for i in s])
    def ProcessLine(line, where):
        Dbg(f"Processing {where} {line!r}")
        # Remove trailing newline
        if line[-1] == "\n":
            line = line[:-1]
        chars = ''.join(set(d["-c"] if d["-c"] else " "))
        # Partition line into L, M, R pieces so that line == L + M + R
        MR = line.lstrip(chars)
        LM = line.rstrip(chars)
        M = line.strip(chars)
        m = len(M)
        L = LM[:len(LM) - m]
        R = MR[m:]
        Dbg(f"  left   = '{Escape(L)}'")
        Dbg(f"  middle = '{Escape(M)}'")
        Dbg(f"  right  = '{Escape(R)}'")
        if g.dbg:
            # Validate invariant
            assert(L + M + R == line)
        if d["-l"]:
            print(f"{t.norm}{M + R}{t.n}")
        elif d["-r"]:
            print(f"{t.norm}{L + M}{t.n}")
        else:
            print(f"{t.norm}{M}{t.n}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        g.line = 1
        with fileinput.input(file) as f:
            for line in f:
                ProcessLine(line, f"[{file}:{g.line}]")
                g.line += 1
