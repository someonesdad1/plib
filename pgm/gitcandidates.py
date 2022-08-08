'''
Examines a directory recursively and suggests the files that should be
included to construct a git repository.
'''
if 1:   # Header
    # Copyright, license
    if 1:
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Suggest git repository files
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    # Standard imports
    if 1:
        import getopt
        import os
        from pathlib import Path as P
        import re
        import sys
        from pdb import set_trace as xx
        from pprint import pprint as pp
    # Custom imports
    if 1:
        from wrap import wrap, dedent
        from color import Color, TRM as t
        import dbg 
    # Global variables
    if 1:
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        # Set up debug printing
        dbg.dbg = True
        Dbg = dbg.GetDbg()
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] dir
          Recursively finds all files in dir and prints which ones should
          probably be put into a git repository.
        Options:
            -d r        Ignore any directories that match this regexp
            -e ext      Ignore this extension (no leading '.')
            -f r        Ingore files whose names match this regexp
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = []        # Directories to ignore
        d["-e"] = []        # Extensions to ignore
        d["-f"] = []        # File name regex to ignore
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "e:h", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-e":
                if a.startswith("."):
                    Error(f"-e option {a!r} must not start with '.'")
                d[o].append("." + a)
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        if len(args) != 1:
            Usage()
        return args[0]
if 1:   # Core functionality
    def GetFiles(dir):
        p = P(dir)
        out = []
        for i in p.rglob("*"):
            out.append(i)
        return out
    def FilterFiles(files):
        # Filter out unwanted extensions
        ignore_extensions = '''
            .bak .bmp .exe .gif .jpg .obj .o .orig .pdf .png .ps .swo
            .swp .zip .py .a .lib .dll
        '''.split()
        ignore_extensions.extend(d["-e"])
        ignore_extensions = set(ignore_extensions)
        breakpoint() #xx
        Dbg("Ignored extensions:")
        Dbg(ignore_extensions)
        exit() #xx

        def KeepThisExtension(x):
            'x is a Path instance'
            return False if x.suffix in ignore_extensions else True
        def KeepThisName(x):
            'x is a Path instance'
            if ".~lock" in str(x.name):
                return False
            return True
        files = filter(KeepThisExtension, files)
        # Filter out unwanted name strings
        files = filter(KeepThisName, files)
        # Filter out ignored directories

        pp(list(files))


        startswith = '''.~lock'''.split()
        ignore = ".local_profile .vi .z a a.py aa b bb log tags z".split()




if __name__ == "__main__":
    d = {}      # Options dictionary
    dir = ParseCommandLine(d)
    files = GetFiles(dir)
    files = FilterFiles(files)
