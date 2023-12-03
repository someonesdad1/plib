'''
Print out descriptions of file name extensions
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
        # Print out descriptions of file name extensions
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        import re
        from pathlib import Path as P
        from sys import stdin, stdout, stderr, argv
    if 1:   # Custom imports
        from wrap import dedent
        from color import t, RegexpDecorate
        from extensions import extensions
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {argv[0]} [options] ext1 [ext2...]
          Print out descriptions of the given file name extensions.
        Examples:
          '{argv[0]} odt'
              Show file extensions for 'odt'
          '{argv[0]} -r openoffice'
              Show descriptions containing 'openoffice'
        Options:
          -c    Don't colorize
          -i    Don't ignore case in -r searches
          -r    Inverse search, where command line options are regexps
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = True      # Colorize output
        d["-i"] = True      # Don't ignore case
        d["-r"] = False     # Inverse search
        if len(argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(argv[1:], "cir") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cir"):
                d[o] = not d[o]
        return args
if 1:   # Core functionality
    def FindExt(ext):
        e = ext.lower()
        if not e.startswith("."):
            e = "." + e
        values = extensions.get(e, [])
        if values:
            if len(values) > 1:
                print(f"{t.ext}{ext}:{t.n}")
                for v in values:
                    print(f"  {v}")
            else:
                print(f"{t.ext}{ext}:{t.n} {values[0]}")
        else:
            t.print(f"{t.unk}{ext}: ?")
    def InverseSearch(regex):
        if not hasattr(InverseSearch, "data"):
            # Cache a list of (descr, ext) tuples
            InverseSearch.data = []
            for key in extensions:
                for item in extensions[key]:
                    InverseSearch.data.append((item, key))
        r = re.compile(regex, re.I if d["-i"] else 0)
        rd = RegexpDecorate()
        rd.register(r, t("yell"), t.n)
        matched = False
        for item, key in InverseSearch.data:
            mo = r.search(item)
            if mo:
                if d["-c"]:
                    s = f"{item} ({t.ext}{key}{t.n})"
                    rd(s)
                    print()
                else:
                    print(f"{item} ({key})")
                matched = True
        if not matched:
            t.print(f"{t.unk}No match for {regex!r}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    t.ext = t("ornl") if d["-i"] else ""
    t.unk = t("redl") if d["-i"] else ""
    for ext in args:
        if d["-r"]:
            InverseSearch(ext)
        else:
            FindExt(ext)
