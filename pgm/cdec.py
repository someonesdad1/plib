'''
TODO
    - Use the Sort classmethod of kolor.py

Decorate color specifications
    - Forms that must be recognized:
        - i = integer on [0, 255], 
        - d = real on [0, 1]
            - .123
            - 0.123
        - Hex string form @#$xxyyzz
        - Single integer on interval [0, 2**24)
            - i i i    or    i, i, i     or   i; i; i
            - d d d    or    d, d, d     or   d; d; d
    - Need a color difference metric  
        - https://en.wikipedia.org/wiki/Color_difference
        - http://markfairchild.org/PDFs/PAP40.pdf is an academic paper
          that's pretty good.  However, I hate that they use a biased
          sample for color judging (typical of all lazy academics, they
          used students and staff members).
        - Explore the use of wavelength.  This has the advantage over hue
          of not wrapping around.  Empirically, I'd judge λls (wavelength,
          lightness, saturation) as a good starting point with suitable
          weighting factors.

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
        # Decorate color specifications.  Handy tool to e.g. browse an
        # X11 rgb.txt file.
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        from pdb import set_trace as xx
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from clr import Clr
        from rgb import ColorNum
        from rgbdata import color_data
        from wl2rgb import rgb2wl
    if 1:   # Global variables
        ii = isinstance
        c = Clr(always=True)
        class g: pass   # Hold global variables
        c.dbg = c("wht", "blu")
        g.duplicates = set()
if 1:   # Utility
    def Dbg(*p, **kw):
        'Print in debug colors if d["-D"] is True'
        if not d["-D"]:
            return
        print(f"{c.dbg}", end="")
        k = kw.copy()
        if "end" in k:
            k["end"] += c.n
        else:
            k["end"] = c.n + "\n"
        print(*p, **k)
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        n = sys.argv[0]
        print(dedent(f'''
        Basic use
        ---------

        The primary use case of this script is to browse color files in your
        terminal program.  To examine the colors in an XWindows rgb.txt file, use

            {n} rgb.txt | less

        assuming your less program recognizes ANSI escape sequences and you have a
        24-bit color terminal program.  To limit the lines to a subset, you can use
        one or more regular expressions with the -r option.  For example, to see
        only lines with 'lilac' or 'purple' in them, use

            {n} -r lilac -r purple rgb.txt | less
 
        How it works
        ------------

        If you want to see how the program works, use the following example.  Put
        the following line in a file 'test':

            dark pink  203 65 107

        Insert a suitable breakpoint() call and invoke the program

            {n} test

        and the line should be printed to stdout in the color the RGB numbers that
        (203, 65, 107) represent.

        '''.rstrip()))
        exit(0)
    def Usage(status=1):
        c.t = c("mag") #xx Current ToDo item
        c.i = c("lblk") #xx Ignored for the moment
        c.d = c("blk") #xx Done
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] file1 [file2...]
          Search the lines of the file(s) for color specifiers and print matching
          lines found in the color specified.  Use '-' to read from stdin.  Regular
          expressions are OR'd together.
        Options:
            -d      Print details on the color
            -e      Eliminate duplicates
            -h      More help and examples
            -r x    Search for case-insensitive regexp x in lines
            -R x    Search for case-sensitive regexp x in lines
            -s s    Sort output by 'rgb', 'hsv', or 'hls'
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-D"] = False     # Debug printing
        d["-d"] = False     # Show color details
        d["-e"] = False     # Eliminate duplicates
        d["-R"] = []        # Case-sensitive regexp
        d["-r"] = []        # Case-insensitive regexp
        d["-s"] = None      # How to sort output
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "DdeR:r:s:", "help")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("Dde"):
                d[o] = not d[o]
            elif o == "-R":
                d[o].append(re.compile(a))
            elif o == "-r":
                d[o].append(re.compile(a, re.I))
            elif o == "-s":
                allowed = "rgb hsv hls wl"
                if a not in allowed.split():
                    Error(f"'{a}' not in {allowed.split()}")
                d[o] = a
            elif o in ("-h", "--help"):
                Manpage()
        return args
if 1:   # Core functionality
    def GetColorRegexps():
        'Return tuple of regexps to use to recognize color identifiers'
        R = re.compile
        # Recognize an integer or float
        s = r'''
                (                               # Group
                    # First is for numbers like .234
                    [+-]?                       # Optional sign
                    \.\d+
                    ([eE][+-]?\d+)?             # Optional exponent
                  |                             # or
                    # This is for integers or 2.3 or 2.3e4
                    [+-]?                       # Optional sign
                    \d+\.?\d*                   # Number:  2.345
                    ([eE][+-]?\d+)?             # Optional exponent
                )                               # End group
        '''
        flags = re.I | re.X
        regexps = (
            # [@#$]xxyyzz form
            R(r"([@#$][0-9a-f]{6})", flags),
            # Three integers or floats separated by commas
            R(f"({s},\s*{s},\s*{s})", flags),
            # Three integers or floats separated by whitespace
            R(f"({s}\s+{s}\s+{s})", flags),
        )
        return regexps
    def GetColor(match):
        'Return a ColorNum instance for the matching string'
        match = match.strip()
        if match[0] in "@#$":
            cn = ColorNum(match)
        elif "," in match:
            a = eval(f"({match})")
            cn = ColorNum(a)
        else:
            if "." in match:
                a = [float(i) for i in match.split()]
            else:
                a = [int(i) for i in match.split()]
            cn = ColorNum(a)
        return cn
    def Search(file):
        '''Put lines to be decorated in the deque g.out.  The structure put
        into the deque is (line, ColorNum).  The trailing whitespace
        of the line is stripped.
        '''
        keep = deque()
        if file == "-":
            lines = sys.stdin.readlines()
        else:
            lines = open(file).readlines()
        for line in lines:
            line = line.rstrip()
            Dbg(f"Read '{line}'")
            candidate = ''
            for r in g.color_regexps:
                mo = r.search(line)
                if mo:
                    candidate = mo.groups()[0]
                    Dbg(f"  Matched '{candidate}'")
                    break
            if candidate:
                # This line contains a color specifier
                cn = GetColor(candidate)
                if cn.rgbhex in g.duplicates and d["-e"]:
                    continue
                g.duplicates.add(cn.rgbhex)
                keep.append((line, GetColor(candidate)))
        # If -R or -r given, filter out lines that don't match
        regexps = d["-R"] + d["-r"]
        if regexps:
            while keep:
                line, candidate = keep.popleft()
                for r in regexps:
                    found = False
                    mo = r.search(line)
                    if mo:
                        found = True
                        Dbg(f"  Matched -r or -R regexp, so keep")
                        break
                if found:
                    g.out.append((line, candidate))
                    continue
        else:
            g.out = keep
    def Report():
        def F(seq):
            if ii(seq[0], int):
                return ', '.join([f"{i:3d}" for i in seq])
            else:
                n = ColorNum.n
                return ', '.join([f"{i:{2 + n}.{n}f}" for i in seq])
        for line, cn in g.out:
            print(f"{c(cn.rgbhex)}{line}{c.n}")
            if d["-d"]:
                # Print details
                i = " "*4
                print(f"{i}RGB: {cn.rgbhex} ({F(cn.RGB)}) ({F(cn.rgb)})")
                print(f"{i}HSV: {cn.hsvhex} ({F(cn.HSV)}) ({F(cn.hsv)})")
                print(f"{i}HLS: {cn.hlshex} ({F(cn.HLS)}) ({F(cn.hls)})")
                print(f"{i}λ = {rgb2wl(cn)} nm")
    def Sort():
        'Sort the data to be printed in g.out'
        # Set the sort order for the ColorNum instances
        if d["-s"] is None:
            return
        for i in g.out:
            i[1].sort = d["-s"]
        f = lambda x: x[1]
        g.out = sorted(g.out, key=f)

if __name__ == "__main__":
    g.color_regexps = GetColorRegexps()
    g.out = deque()     # Container for the lines to output
    d = {}              # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        Search(file)
    Sort()
    Report()
