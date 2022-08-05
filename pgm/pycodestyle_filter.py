'''

TODO
    - Add -a option to see all issues, not just important or notable.

Filter output of pycodestyle to a more compact representation.  
    Note the color coding is always done, even if stdout is not a TTY.
    This lets you capture the results to a file and view it e.g. with less
    in color.
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Filter output of pycodestyle to a more compact representation
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from pdb import set_trace as xx
        xx()
        #from pprint import pprint as pp
        from collections import defaultdict
    # Custom imports
        from get import GetLines
        from wrap import wrap, dedent, HangingIndent
        from lwtest import Assert
        from color import Color, TRM as t
        t.always = True
    # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        # Colorizing errors & warnings
        errors_important = set("E401 E402 E701 E702 E704 E722 E901 E902".split())
        errors_notable = set("E703 E711 E712 E713 E714 E731 E741 E742 E743".split())
        warnings_important = set("W191".split())
        warnings_notable = set("W601 W602 W603 W604 W605 W606".split())
        # Make a dict of errors/warnings that need colorizing
        clr = {}
        for i in errors_important:
            clr[i] = t("redl")
        for i in errors_notable:
            clr[i] = t("ornl")
        for i in warnings_important:
            clr[i] = t("purl")
        for i in warnings_notable:
            clr[i] = t("royl")
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [files]
          Filter the output of pycodestyle to make it more compact.
          Use '-' to filter stdin.
        Options:
            -a      Show all issues
            -c      Include the column numbers in the output lines
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Show all issues
        d["-c"] = False     # Include column numbers
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ach", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("ac"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        return args
if 1:   # Core functionality
    def ProcessLines(lines):
        'Return a dict of the lines keyed by error/warning number'
        global names
        di = defaultdict(list)
        for line in lines:
            line = line.strip()
            if not line:
                continue
            f = line.split(":")
            Assert(len(f) > 3)
            file = f[0]
            linenum = f"{int(f[1])}:{int(f[2])}"
            # Get error/warning and description
            g = ''.join(f[3:]).strip().split()
            errn = g[0].strip()
            descr = ' '.join(g[1:]).strip()
            names[errn] = descr
            if 0:
                print(file, linenum, errn, repr(descr))
            # Add to dict
            di[errn].append((file, linenum, descr))
        # Get rid of duplicates by making each entry a set
        for errn in di:
            di[errn] = list(set(di[errn]))
        # Collapse data so that each errnum has a dict keyed by filename
        # and a list of line numbers the error was on
        for errn in di:
            tup = di[errn]
            di[errn] = defaultdict(list)
            linenums = []
            for i in tup:
                file, linenum = i[0], i[1]
                di[errn][file].append(linenum)
        if 0:
            pp(di, compact=1)
        return di
    def Report(di):
        def RemoveColumnNumbers(lst, uniq=False):
            for i, item in enumerate(lst):
                if ":" in item:
                    lst[i] = item.split(":")[0]
            if uniq:
                lst = list(sorted(set(lst)))
            return lst
        fl_ind = " "*2
        for err in sorted(di):
            if err in clr:
                print(f"{clr[err]}", end="")
            elif d["-a"]:
                print(f"{t('skyl')}", end="")
            else:
                continue
            print(f"{err} {names[err]}")
            t.out()
            for i in sorted(di[err]):
                if d["-c"]:
                    # Include the column number
                    f = lambda x: int(x.split(":")[0])
                    items = list(sorted(di[err][i], key=f))
                else:
                    f = lambda x: int(x)
                    items = list(sorted(RemoveColumnNumbers(di[err][i], 
                                               uniq=True), key=f))
                hdr = f"{fl_ind}{i}:  "
                line = f"{hdr}{' '.join(items)}"
                ind = len(hdr)
                s = HangingIndent(line, indent=" "*ind, first_line_indent=" "*2)
                print(s)

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    if files == ["-"]:
        lines = GetLines(sys.stdin)
    else:
        lines = []
        for file in files:
            lns = GetLines(file)
            lines.extend(lns)
    if 0:
        for i in lines:
            print(i)
    # Dict for error/warning num: description
    names = {}
    di = ProcessLines(lines)
    Report(di)
