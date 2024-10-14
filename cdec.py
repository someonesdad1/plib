'''
Decorate color specifications
    - Consider adding hex decorators to each line for convenience
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
        import math
        import os
        import re
        import sys
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, Trm
        from wl2rgb import rgb2wl, wl2rgb
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        ii = isinstance
        t = Trm()
        # The following makes the script's output always have escape codes for color, letting you
        # save the results to a file and view later with e.g. /usr/bin/less.
        t.on = True
        class g:
            pass   # Hold global variables
        t.dbg = t("wht", "blu")
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
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] file1 [file2...]
          Search the lines of the file(s) for color specifiers and print matching lines found in
          the color specified.  Use '-' to read from stdin.  Regular expressions (-r or -R) are
          OR'd together.

          Allowed color specifiers are:
            - #4169e1 (rgb), @9fb5e1 (hsv), $9f91b9 (HSL)
            - Three integers or floats separated by commas or whitespace
        Options:
            -d      Print details on the color
            -e      Eliminate duplicates
            -f      Use escape code even if terminal is not a tty
            -h      Show an example
            -r x    Search for case-insensitive regexp x in lines
            -R x    Search for case-sensitive regexp x in lines
            -s s    Sort output by letters s in "rgbhsvHSL"
            -x      Decorate each line with hex color notations: # = rgb, @ = hsv, $ = HSL.
                    The number in nm is the estimated spectral wavelength of the color.
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-D"] = False     # Debug printing
        d["-b"] = False     # Browse hues
        d["-d"] = False     # Show color details
        d["-e"] = False     # Eliminate duplicates
        d["-R"] = []        # Case-sensitive regexp
        d["-r"] = []        # Case-insensitive regexp
        d["-s"] = None      # How to sort output
        d["-x"] = False     # Decorate lines with hex values
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "bDdehR:r:s:x", "help")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("bDdex"):
                d[o] = not d[o]
            elif o == "-R":
                d[o].append(re.compile(a))
            elif o == "-r":
                d[o].append(re.compile(a, re.I))
            elif o == "-s":
                allowed = set("rgbhsvHLS")
                for i in a:
                    if i not in allowed:
                        Error(f"'{i}' for -s option not in {allowed.split()}")
                d[o] = a
            elif o == "-h":
                Example()
        return args
if 1:   # Nonworking Browse function (broken because less is broken)
    def Browse():
        '''This was an attempt to add a browsing feature, but it fails
        because of limitations of the less pager, which I need to view to
        decorated data.  The less display fails for terminal escape codes
        when it is called from subprocess() or os.system().

        The workaround would be to use a shell script with a directory of
        the subfiles somewhere already sorted.  Then a cdec|less call
        would work.
        '''
        import subprocess
        import tempfile
        from colorhues import colorhues
        from cmddecode import CommandDecode
        c, prompt = CommandDecode(colorhues.keys()), "> "
        print(". to list hue choices, q to exit")
        letters = "rgbhsvHSL"
        dl = "LHS"
        hue = "red"
        def GetInfo():
            nonlocal hue
            while True:
                cmd = input(f"Enter hue [{hue}]: ").strip()
                if cmd == "q":
                    exit(0)
                elif cmd == ".":
                    for i in sorted(c.commands):
                        print(i, end=" ")
                    print()
                    continue
                else:
                    if not cmd:
                        cmd = hue
                    x = c(cmd)
                    if not x:
                        print(f"'{cmd}' unrecognized")
                        continue
                    elif len(x) == 1:
                        hue = x[0]
                    else:
                        x.sort()
                        print(f"'{cmd}' is ambiguous:  {x}")
                        continue
                sl = input(f"Enter sorting letters [{dl!r}]: ").strip()
                if not sl:
                    sl = dl
                else:
                    for i in sl:
                        if i not in letters:
                            print(f"'{i}' is not a valid letter")
                            continue
                return hue, sl
        def Display(lst):
            '''lst is a list of colorized strings.  Store them in a temporary
            file and browse them with less.
            '''
            # This use of less doesn't work, as the escape codes don't
            # result in colors with less in a pipe
            try:
                tmp = P(tempfile.mkstemp(prefix="cdec.", suffix=".tmp")[1]).resolve()
                f = open(tmp, "w")
                for line in lst:
                    f.write(line + "\n")
                f.close()
                less = "c:/cygwin/bin/less.exe"
                cmd = [less, "--use-color", tmp]
                #subprocess.run(cmd)
                os.system(f"c:/cygwin/bin/less.exe {tmp}")
            finally:
                tmp.unlink()
        try:
            while 0 and True:
                hue, sl = GetInfo()
                print(hue, sl)
            di = colorhues["red"]
            for name in di:
                c = Color(di[name])
                s = f"{t(c)}{name:42s} {c.xrgb} {c.xhsv} {c.xhls}"
                g.out.append((s, c))
            def f(x):
                return x[1]
            g.out = Color.Sort(g.out, keys=dl, get=f)
            lst = [i[0] for i in g.out]
            Display(lst)
            #for i, j in g.out:
            #    print(i)
        finally:
            t.out()
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
            R(rf"({s},\s*{s},\s*{s})", flags),
            # Three integers or floats separated by whitespace
            R(rf"({s}\s+{s}\s+{s})", flags),
        )
        return regexps
    def GetColor(match):
        'Return a Color instance for the matching string'
        match = match.strip()
        if match[0] in "@#$":
            c = Color(match)
        elif "," in match:
            a = eval(f"({match})")
            c = Color(*a)
        else:
            if "." in match:
                a = [float(i) for i in match.split()]
            else:
                a = [int(i) for i in match.split()]
            c = Color(*a)
        return c
    def Search(file):
        '''Put lines to be decorated in the deque g.out.  The structure put into the deque is
        (line, Color).  The trailing whitespace of the line is stripped.
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
                c = GetColor(candidate)
                if c.xrgb in g.duplicates and d["-e"]:
                    continue
                g.duplicates.add(c.xrgb)
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
                # Need number of decimal places to show
                n = math.ceil(math.log10(c.N))
                return ', '.join([f"{i:{2 + n}.{n}f}" for i in seq])
        for line, c in g.out:
            s = ""
            if d["-x"]:
                wl = rgb2wl(c)
                raw_rgb = wl2rgb(wl)
                s = ' '.join([c.xrgb, c.xhsv, c.xhls, f"{t(raw_rgb)}{wl} nm{t.n}"])
            try:
                print(f"{t(c.xrgb)}{line}{t.n} {s}")
            except Exception:
                # Isn't a proper form, so ignore it
                continue
            if d["-d"]:
                # Print details
                i = " "*4
                print(f"{i}RGB: {c.xrgb} ({F(c.irgb)}) ({F(c.drgb)})")
                print(f"{i}HSV: {c.xhsv} ({F(c.ihsv)}) ({F(c.dhsv)})")
                print(f"{i}HLS: {c.xhls} ({F(c.ihls)}) ({F(c.dhls)})")
    def Sort():
        'Sort the data to be printed in g.out'
        # Set the sort order for the ColorNum instances
        if d["-s"] is None:
            return
        def f(x):
            return x[1]
        g.out = Color.Sort(g.out, keys=d["-s"], get=f)
    def Example():
        data = '''
            royal blue      #4169e1
            periwinkle      #8e82fe
            teal            #029386
            cyan            #00ffff
            blue            #0343df
            light blue      #b0e2ff
            sky blue        #729fff
            bright blue     #0165fc
            green           #00ff00
            light green     #96f97b
            forest green    #228b22
            Pea Soup        #b9b880
        '''
        print(dedent(f'''
        Suppose you had the following text in a file:
        {data}
        This script will decorate the lines of the file in the color indicated on each line as
        shown in the following output.
        '''))
        print()
        for line in data.split("\n"):
            if not line.strip():
                continue
            a, b = line.split("#")
            g.out.append((" "*4 + line.strip(), Color("#" + b)))
        Report()
        exit()

if __name__ == "__main__":
    g.color_regexps = GetColorRegexps()
    # Container for the lines to output; contents will be (line, Color).  The trailing whitespace
    # from line is stripped.
    g.out = deque()
    d = {}              # Options dictionary
    files = ParseCommandLine(d)
    if d["-b"]:
        Browse()
    else:
        for file in files:
            Search(file)
        Sort()
        Report()
