'''
Decorate color specifications
    Forms that must be recognized:
        i = integer on [0, 255], 
        d = real on [0, 1]
            .123
            0.123

        Hex string form @#$xxyyzz
        Single integer on interval [0, 2**24)
        i i i    or    i, i, i     or   i; i; i
        d d d    or    d, d, d     or   d; d; d

Need a color difference metric.  

    - https://en.wikipedia.org/wiki/Color_difference
    - http://markfairchild.org/PDFs/PAP40.pdf is an academic paper that's
      pretty good.  However, I hate that they use a biased sample for color
      judging (typical of all lazy academics, they used students and staff
      members).
    - Explore the use of wavelength.  This has the advantage over hue of
      not wrapping around.  Empirically, I'd judge λls (wavelength,
      lightness, saturation) as a good starting point with suitable
      weighting factors.


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
    # Decorate color specifications
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

        Change interface:
            
            file1 [file2 ...]

        Examine lines for color specifiers.  Print out line in that color
        if found.  '-' means read stdin.

        -r regexp       regexp to search for.  Can have more than one (they
                        are OR'd together).
        -v regexp       Remove lines with this regexp         
        -@, -#, -$      Force usage of this color space except for hex strings
        -d              Print out details of color:  coordinates in various
                        color spaces, wavelength, name matches if -n used
        -n file         Name file to read in.  See -h for details.

        -s arg          Specify sort order:  rgb, hsv, hls.  When this
                        option is used, all lines are saved and sorted at
                        the end, so large amounts of data might run out of
                        memory.


        Usage:  {sys.argv[0]} [options] file1 [file2...]
          Search the lines of the files for color specifiers and print out
          those lines found in the color specified.  Use '-' to read from
          stdin.
        Options:
            -@      Force use of HSV color space
            -#      Force use of RGB color space [default]
            -$      Force use of HLS color space
            -d      Print color's details
            -h      More detailed help and examples
            -i      Prompt interactively for input lines
            -r x    Search for regexp x in lines (-r's OR'd)
            -s s    Sort order:  'rgb', 'hsv', or 'hls'
        '''))
        exit(status)
    def Manpage():
        n = sys.argv[0]
        print(dedent(f'''
 
        This script is a utility for recognizing and printing  typical
        color specifications.  For a simple example, run the script as
 
            python {n} '(199, 159, 239) This is some sample text'
  
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
    def Report(line, cn):
        if cn is None:
            print(f"'{line}' unrecognized", file=sys.stderr)
            return
        w, i = 15, " "*4
        # Print the input string in the line's color
        print(f"{c(cn.rgbhex)}{line}{c.n}")
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
    def GetRegularExpressions():
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
        regexps = (
            R(r"([@#$][0-9a-f]{6})", re.I|re.X),     # [@#$]xxyyzz form
            R(f"({s},\s*{s},\s*{s})", re.I|re.X),    # Three integers or floats
        )
        return regexps

if __name__ == "__main__":
    regexps = GetRegularExpressions()
    d = {"-e":"", "-m":""}      # Options dictionary
    if 0:  # Debugging code
        dbg = '''
        (9, 'cloudy blue', Color((172, 194, 217))),
        (9, 'dark pastel green', Color(( 86, 174,  87))),
        '''
        FromStdin(dbg=dbg)
        exit()
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
