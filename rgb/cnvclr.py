'''
Convert color specifications
'''
 
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Convert color specifications
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Standard imports
    import getopt
    import os
    from pathlib import Path as P
    import re
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
    from clr import Clr
    from rgb import ColorNum
    from rgbdata import color_data
if 1:   # Global variables
    ii = isinstance
    c = Clr(override=True)
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [c1 [c2...]]
          Convert color specifications.  The default report is a statement
          of the string read in the color it represents.  If '-' is the
          only argument on the command line, read the specifications from
          stdin.
        Options:
            -a      Show all report data
            -e      Show equivalent RGB, HSV, HLS data
            -f file Read data from this file for -s option (implies -s)
            -h      More detailed help and examples
            -i      Prompt interactively for input (implies -a)
            -m      Show matching names in rgbdata.py
            -s      c1 ... are regexps; search for them in rgbdata.py
            -w      Show estimated wavelength of light in nm
        '''))
        exit(status)
    def Manpage():
        n = sys.argv[0]
        print(dedent(f'''
        This script is a utility for dealing with typical color specifications.
        For a simple example, run the script as

            python {n} '(199, 159, 239)'

        and you'll see the input string printed in the RGB color it represents.  

        You can examine a number of lines in a file in the color they represent.
        Using the rgbdata.py file which has thousands of color names defined in it,
        we can get a colorized listing of some of the lines at the beginning of the
        file:

            head -50 rgbdata.py | python {n} -

        The '-' as the single argument means to read the lines from stdin.

        We can do something similar but more specific by using the -f option to
        specify an input file.  In this case, the arguments on the command line
        become case-insensitive regular expressions to search for in the input file;
        when a color specification is found, it is printed out in its color.  For
        example:

            python {n} -f rgbdata.py lilac

        shows the lines in rgbdata.py that use the string 'lilac' in the color.

        
        '''.rstrip()))
        exit(0)

    def ParseCommandLine(d):
        d["-a"] = False     # Show all report data
        d["-e"] = False     # Show equivalent RGB, HSV, HLS data
        d["-f"] = None      # Input file
        d["-i"] = False     # Interactive
        d["-m"] = False     # Show matching names
        d["-s"] = False     # Search for regexps
        d["-w"] = False     # Show wavelength
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "@aef:himsw", "help")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("@aeimsw"):
                d[o] = not d[o]
            elif o == "-f":
                d[o] = a
            elif o in ("-h", "--help"):
                Manpage()
        if d["-a"]:
            d["-e"] = d["-m"] = d["-w"] = True
        if d["-f"] is not None:
            d["-s"] = True
        if d["-s"]:
            d["-e"] = d["-m"] = d["-w"] = False
        return args
if 1:   # Core functionality
    def Convert(s):
        try:
            cn = ColorNum(s)
            return cn
        except Exception:
            # See if it's a string form of a sequence
            try:
                t = eval(s)
                cn = ColorNum(t)
                return cn
            except Exception:
                return None
    def Report(s, cn):
        if cn is None:
            print(f"'{s}' unrecognized", file=sys.stderr)
            return
        w, i = 15, " "*4
        # Print the input string in the line's color
        print(f"Input:  {c(cn.rgbhex)}{s}{c.n}")
        if d["-e"]:
            print(dedent(f'''
                {i}RGB:  {cn.rgbhex} {cn.RGB!s:{w}s} {cn.rgb}
                {i}HSV:  {cn.hsvhex} {cn.HSV!s:{w}s} {cn.hsv}
                {i}HLS:  {cn.hlshex} {cn.HLS!s:{w}s} {cn.hls}
            ''', n=15))
        # See if we can find a name match in color_data
        if d["-m"]:
            rgb = cn.RGB
            matches = []
            for attr, name, color in color_data:
                cndata = [i for i in list(color._rgb)]
                if tuple(cndata) == tuple(rgb):
                    matches.append(name)
            if matches:
                print(f"{i}Matching color names in rgbdata.py:")
                for m in sorted(set(matches)):
                    print(f"{i*2}{m}")
        return 0
    def Interactive():
        while True:
            s = input("Color specifier? ")
            if s == "q":
                exit(0)
            cn = Convert(s)
            Report(s, cn)
            print()
        exit()
    def ExamineLine(line):
        "Inspect the line; if there's a valid expression, return it"
        for r in regexps:
            mo = r.search(line)
            if mo:
                s = mo.groups()[0]
                if s[0] in "@#$":
                    return s
                else:
                    return f"({s})"
        return None
    def FromStdin(dbg=None):
        '''Look for three integer numbers, 3 floats, or hex strings
        beginning with @, #, or $.
        '''
        if dbg:
            lines = dbg.split("\n")
        else:
            lines = sys.stdin.readlines()
        for line in lines:
            if not line:
                continue
            ln = line.strip()
            s = ExamineLine(ln)
            if s:
                cn = Convert(s)
                Report(ln, cn)
    def Search(s):
        'Find s in rgbdata and print out line if found'
        r = re.compile(r"{}".format(s), re.I)
        lines = [i.strip() for i in open("rgbdata.py").readlines()]
        for line in lines:
            mo = r.search(line)
            if not mo:
                continue
            s = ExamineLine(line)
            if s:
                cn = Convert(s)
                Report(line, cn)

if 0:
    R = re.compile
    r = R(r"([@#$][0-9a-f]{6})", re.I)  # [@#$]xxyyzz form
    # Expression to recognize integers and floats
    s = r"([+-]?\.\d+([eE][+-]?\d+)?|[+-]?\d+\.?\d*([eE][+-]?\d+)?)"
    r = R(f"({s},\s*{s},\s*{s})", re.I) # Three integers or floats
    s = "105, 216, 79"
    s = "105, 216, 79e-3"
    mo = r.search(s)
    if mo:
        print(mo.groups()[0])
    exit()

if __name__ == "__main__":
    R = re.compile
    s = r"([+-]?\.\d+([eE][+-]?\d+)?|[+-]?\d+\.?\d*([eE][+-]?\d+)?)"
    # Regular expressions to help identify data in strings
    regexps = (
        R(r"([@#$][0-9a-f]{6})", re.I),     # [@#$]xxyyzz form
        R(f"({s},\s*{s},\s*{s})", re.I),    # Three integers or floats
    )
    del s, R
    if 0:  # Debugging code
        dbg = '''
        (9, 'cloudy blue', Color((172, 194, 217))),
        (9, 'dark pastel green', Color(( 86, 174,  87))),
        '''
        FromStdin(dbg=dbg)
        exit()
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if len(args) == 1 and args[0] == "-":
        FromStdin()
        exit(0)
    if d["-i"]:
        Interactive()
    elif d["-s"]:
        for i in args:
            Search(i)
    else:
        for i in args:
            cn = Convert(i)
            Report(i, cn)
