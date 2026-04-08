'''
Print out color names with a regex in the name
'''
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
        import collections
        import getopt
        import os
        import re
        import sys
    if 1:  # Custom imports
        import cdec
        import color
        import dpcolornames
        import trm
        import wrap
    if 1:  # Import symbols
        defaultdict = collections.defaultdict
        #
        t = trm.TrmDP()
        dedent = wrap.dedent
    if 1:  # Global variables
        t.always = True     # Always print escape sequences
if 1:  # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] regex1 [regex2 ...]
          Print out color names that match the given regular expressions.
        Options:
            -a      Include attribution
            -i      Don't ignore case in regular expressions
            -s      Sort key (letters from rgbhsvHLS) [{d["-s"]}]
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False  # Show attributions
        d["-i"] = True  # Ignore case in searches
        d["-s"] = "hsv"  # Color sorting method
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
        '''In dpcolornames.colornames, search for names that match regex and put them
        into the data dict indexed by Color instance.
         
        Note:  dpcolornames.colornames is a dict of str: list(ColorName) where ColorName
        is a namedtuple("ColorName", "hex name key").  Search on the name attribute.
        '''
        case = re.I if d["-i"] else 0
        r = re.compile(regex, case)
        for name in dpcolornames.colornames:
            for colorname in dpcolornames.colornames[name]:
                hex, orig_name, key = colorname
                if r.search(orig_name):
                    clr = color.Color(hex)
                    data[clr].append(colorname)
    def Report(data: dict) -> None:
        "Print the colors sorted by the default color.Sort() method (uses 'hL')"
        if not data:
            return
        # Get the sequence of color keys sorted as the user wants them
        seq = data.keys()   # These are color.Color instances
        seq = color.Color.Sort(seq, keys=d["-s"])  # type: ignore
        for clr in seq:
            items = data[clr]
            if len(items) == 1:
                item = items[0]
                t.print(f"{t(clr)}{clr.xrgb} {clr.xhsv} {clr.xhls}    {item.name} ({item.key})")
            else:
                for i, item in enumerate(items):
                    if not i:
                        t.print(f"{t(clr)}{clr.xrgb} {clr.xhsv} {clr.xhls}    {item.name} ({item.key})")
                    else:
                        t.print(f"    {t(clr)}{item.name} ({item.key})")
        if d["-a"]:     # Print attributions
            print("Attribution numbers:")
            for num in dpcolornames.attributions:
                s = dpcolornames.attributions[num].strip().split("\n")
                print(f"  {num:2d}  {s[0]}")
        return

        breakpoint() # ∞∞ 
        seq = data.values()
        def get(x):     # Predicate to get the Color instance
            return x[2]
        seq = color.Color.Sort(seq, keys=d["-s"], get=get)  # type: ignore
        # Get maximum name length
        w = max(len(i[1]) for i in seq)
        for attr, name, clr in seq:
            if d["-a"]:
                t.print(f"{t(clr)}{clr.xrgb} {clr.xhsv} {clr.xhls} {attr}    {name:{w}s}")
            else:
                t.print(f"{t(clr)}{clr.xrgb} {clr.xhsv} {clr.xhls}    {name:{w}s}")
        if d["-a"]:
            # Print attributions
            print("Attribution numbers:")
            for i in dpcolornames.attributions:
                s = dpcolornames.attributions[i].split("\n")
                print(i)
                for j in s:
                    print(f"  {j}")

if __name__ == "__main__":
    d = {}  # type: ignore
    regexps = ParseCommandLine(d)
    # data will be a dict with keys that are color.Color instances.  The values will be the
    # ColorName namedtuples that matched the regex on the command line.
    data: defaultdict[str, list[color.Color]] = defaultdict(list)
    for regex in regexps:
        GetData(regex, data)
    Report(data)
