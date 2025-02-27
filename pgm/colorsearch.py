"""

Fix
    -

Print out color names with a regex in the name
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Print out color names with a regex in the name
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import getopt
        import os
        import re
        from pathlib import Path as P
        import sys
    if 1:  # Custom imports
        from wrap import wrap, dedent
        from color import Color, t
        from rgbdata import color_data, attr_data
        import cdec
    if 1:  # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        # Make sure escape sequences are always printed even if output
        # isn't a TTY
        t.always = True
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] regex1 [regex2 ...]
          Print out color names with the given regular expressions.
        Options:
            -a      Include attribution
            -h      Print a manpage
            -i      Don't ignore case in regular expressions
            -s      Sort key (letters from rgbhsvHLS) [{d["-s"]}]
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False  # Show attributions
        d["-i"] = True  # Ignore case in searches
        d["-s"] = "svh"  # Color sorting method
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, regexps = getopt.getopt(sys.argv[1:], "ahis:")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("ai"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o == "-s":
                d[o] = a
        return regexps


if 1:  # Core functionality

    def GetData(regex: str, data: dict) -> None:
        """In color_data, search for names that match regex and put them
        into the data dict indexed by Color instance.
        """
        case = re.I if d["-i"] else 0
        r = re.compile(regex, case)
        for item in color_data:
            attr, name, color = item
            if r.search(name):
                data[color] = item

    def Report(data: dict) -> None:
        """Print the colors sorted by the default color.Sort() method (uses
        'hL').
        """
        if not data:
            return
        seq = data.values()
        get = lambda x: x[2]  # Predicate to get the Color instance
        seq = Color.Sort(seq, keys=d["-s"], get=get)
        # Get maximum name length
        w = max(len(i[1]) for i in seq)
        for attr, name, color in seq:
            if d["-a"]:
                t.print(
                    f"{t(color)}{color.xrgb} {color.xhsv} {color.xhls} {attr}    {name:{w}s}"
                )
            else:
                t.print(
                    f"{t(color)}{color.xrgb} {color.xhsv} {color.xhls}    {name:{w}s}"
                )
        if d["-a"]:
            # Print attributions
            print("Attribution numbers:")
            for i in attr_data:
                s = attr_data[i].split("\n")
                print(i)
                for j in s:
                    print(f"  {j}")


if __name__ == "__main__":
    d = {}  # Options dictionary
    regexps = ParseCommandLine(d)
    data = {}
    for regex in regexps:
        GetData(regex, data)
    Report(data)
