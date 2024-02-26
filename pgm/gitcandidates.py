'''
Examines a directory recursively and suggests the files that should be
included to construct a git repository.

To be more useful, this needs to ignore those files that are already in the
repository.

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
        from itertools import filterfalse as remove
        import re
        import sys
        from pprint import pprint as pp
    # Custom imports
    if 1:
        from wrap import wrap, dedent
        from color import Color, TRM as t
        import dbg 
    # Global variables
    if 1:
        ii = isinstance
        Dbg = None
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
            -f r        Ignore files whose names match this regexp
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = [".git", ".hg"]  # Directories to ignore
        d["-e"] = []        # Extensions to ignore
        d["-f"] = []        # File name regex to ignore
        d["-v"] = False     # Turn on debug printing
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:e:f:hv", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("v"):
                d[o] = not d[o]
            elif o == "-d":
                d[o].append(a)
            elif o == "-e":
                if a.startswith("."):
                    Error(f"-e option {a!r} must not start with '.'")
                d[o].append("." + a)
            elif o == "-f":
                d[o].append(a)
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        if len(args) != 1:
            Usage()
        if d["-v"]:
            # Set up debug printing
            global Dbg
            dbg.dbg = True
            Dbg = dbg.GetDbg()
        Dbg("Option dict:", d)
        return args[0]
    def Dummy(*p, **kw):
        pass
    Dbg = Dummy
if 1:   # Core functionality
    def GetFiles(dir):
        p = P(dir)
        out = []
        for i in p.glob("**/*"):
            if i.is_file():
                out.append(i)
        return out
    def FilterFiles(files):
        if True:
            # Filter out unwanted extensions
            ignore_extensions = '''
                .bak .bmp .exe .gif .jpg .obj .o .orig .pdf .png .ps .swo
                .swp .zip .a .lib .dll
            '''.split()
            ignore_extensions.extend(d["-e"])
            ignore_extensions = set(ignore_extensions)
            Dbg("Ignored extensions:")
            Dbg(ignore_extensions)
            def RemoveThisExtension(x):
                'x is a Path instance'
                y = x.resolve()
                return True if y.suffix in ignore_extensions else False
            files = list(remove(RemoveThisExtension, files))
        if True:
            names = set('''.vi .z a b z tags'''.split())
            # Filter out unwanted name strings
            def RemoveThisName(x):
                'x is a Path instance'
                y = x.resolve()
                if str(y.name) in names:
                    return True
                return False
            files = list(remove(RemoveThisName, files))
        if d["-d"]:
            # Filter out ignored directories
            def RemoveThisDir(x):
                'x is a Path instance'
                nonlocal r
                y = x.resolve()
                parent = y.parent
                return any(r.search(i) for i in parent.parts)
            for regex in d["-d"]:
                r = re.compile(regex)
                files = list(remove(RemoveThisDir, files))
        if d["-f"]:
            # Filter out ignored files
            def RemoveThisFile(x):
                'x is a Path instance'
                # Show the name and True if we had a match
                r = RemoveThisFile.r
                match = bool(r.search(x.name))
                c = t("redl") if match else t("grnl")
                Dbg(f"{' '*20}{x.name}:  {bool(r.search(x.name))} {r}", color=c)
                return bool(r.search(x.name))
            for regex in d["-f"]:
                RemoveThisFile.r = re.compile(regex)
                Dbg(f"{' '*10}", regex, color=t('lip'))
                files = list(remove(RemoveThisFile, files))
        return files
    def PrintFiles(files):
        for i in sorted(files):
            print(i)

if __name__ == "__main__":
    d = {}      # Options dictionary
    dir = ParseCommandLine(d)
    files = GetFiles(dir)
    files = FilterFiles(files)
    PrintFiles(files)
