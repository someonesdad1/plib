'''
Rename picture files
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2014, 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import subprocess
        import sys
    if 1:   # Custom imports
        from color import t
        from dpprint import PP
        pp = PP()   # Screen width aware form of pprint.pprint
        from get import GetLines
        from wrap import dedent
        from wsl import wsl     # wsl is True when running under WSL Linux
        from lwtest import Assert
        #from columnize import Columnize
    if 1:   # Global variables
        class G:    # Storage for global variables as attributes
            pass
        g = G()
        g.dbg = False
        ii = isinstance
        ext = '''
            jpeg jpg jfif exif
            gif png bmp webp tiff
            ppm pgm pbm pnm
            '''.split()
if 1:   # Utility
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def GetColors():
        t.dbg = t("cyn") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.err = t("redl")
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.N}", end="", file=Dbg.file)
    Dbg.file = sys.stdout
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(dedent(f'''
        '''.rstrip()).lstrip())
        exit(0)
    def Usage():
        print(dedent(f'''
 
        Usage:  {sys.argv[0]} [options] [dir1 [dir2...]]
          Rename picture files in the indicated directories.  The default behavior is to show
          which files will be renamed.
        Options:
            -@      Get files to be renamed from stdin
            -e      Perform the renaming
            -f f    Get files to be renamed from file f
            -h      Print a manpage
            -i e    Ignore extension e (can have multiple i options)
            -x s    Ignore indicated files (s is a regexp)
 
        '''.rstrip()).lstrip())
        exit(0)
    def ParseCommandLine(d):
        d["-x"] = False     # Perform the renaming
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "f:hx") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("x"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o == "-h":
                Usage(status=0)
        GetColors()
        g.W, g.L = GetScreen()
        return args
if 1:   # Core functionality
    def ProcessDirectory(dir, new_dir_name, ext):
        print("Processing", dir)
        currdir = os.getcwd()
        os.chdir(dir)
        files = glob.glob("*." + ext)
        numfiles = len(files)
        if numfiles < 10:
            fmt = "%d"
        elif numfiles < 100:
            fmt = "%02d"
        elif numfiles < 1000:
            fmt = "%03d"
        elif numfiles < 10000:
            fmt = "%04d"
        elif numfiles < 100000:
            fmt = "%05d"
        else:
            fmt = "%d"
        num = 1
        for file in files:
            p = os.path.splitext(file)
            name = p[0].lower()
            ex = p[1].lower()
            assert(ex[1:] == ext)
            newname = fmt % num + "." + ext
            while os.path.exists(newname):
                num = num + 1
                newname = fmt % num + "." + ext
            os.rename(file, new_dir_name + newname)
            num = num + 1
        os.chdir(currdir)

if __name__ == "__main__": 
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    dir = args[0]
    if len(args) == 2:
        new_dir_name = args[1]
    else:
        new_dir_name = ""
    ext = "jpg"
    if d["-p"]:
        ext = "png"
    if os.path.isdir(dir):
        ProcessDirectory(dir, new_dir_name, ext)
        exit(0)
    else:
        Error(f"{dir!r} not found")
        exit(1)
