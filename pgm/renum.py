"""
- Todo
    - Colorize picture type

Rename picture files
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2014, 2024 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Program description string
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import glob
        import math
        import os
        import re
        import subprocess
        import sys
    if 1:  # Custom imports
        from color import t
        from dpprint import PP

        pp = PP()  # Screen width aware form of pprint.pprint
        from get import GetLines
        from wrap import dedent
        from wsl import wsl  # wsl is True when running under WSL Linux
        from lwtest import Assert
        # from columnize import Columnize
    if 1:  # Global variables

        class G:  # Storage for global variables as attributes
            pass

        g = G()
        g.dbg = False
        ii = isinstance
        extensions = "bmp gif jpg jpeg png".split()
if 1:  # Utility

    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )

    def GetColors():
        t.dbg = t("cyn") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.err = t("redl")
        t.warn = t("ornl")

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
        print(
            dedent(
                f"""
        """.rstrip()
            ).lstrip()
        )
        exit(0)

    def Usage(status=0):
        print(
            dedent(
                f"""
        Usage:  {sys.argv[0]} [options]
          Rename picture files in the current directory.  The file extensions processed are bmp,
          gif, jpg, and png.  The default behavior is to show which files will be renamed (use -x
          to perform the renaming).
        Options:
            -@      Get files to be renamed from stdin
            -h      Print a manpage
            -i e    Ignore extension e (e.g., '.jpg')
                    (can have multiple i options)
            -n n    Starting number for file numbers [0]
            -p p    New prefix for file names ['']
            -s s    New suffix for file names ['']
            -x      Perform the renaming
 
        """.rstrip()
            ).lstrip()
        )
        exit(status)

    def ParseCommandLine(d):
        d["-@"] = False  # Get files to be renamed from stdin
        d["-i"] = []  # Ignored extensions
        d["-n"] = 0  # Starting number
        d["-p"] = ""  # Prefix for renaming
        d["-s"] = ""  # Suffix for renaming
        d["-x"] = False  # Perform the renaming
        try:
            opts, args = getopt.getopt(sys.argv[1:], "@hi:p:s:x")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("x"):
                d[o] = not d[o]
            elif o == "-i":
                d[o].append(a)
            elif o in ("-p", "-s"):
                d[o] = a
            elif o == "-h":
                Usage()
        GetColors()
        g.W, g.L = GetScreen()
        return args


if 1:  # Core functionality

    def GetWidth(numfiles):
        """Return the number of digits to give the renaming integer to.  This ensures the new file
        names are all the same length.
        """
        Assert(numfiles > 0)
        # Method:  generate all the numbers needed and get the largest string
        sz, start = 0, d["-n"]
        for i in range(start, start + numfiles + 1):
            sz = max(sz, len(str(i)))
        return sz

    def Process():
        """Return (old, new).  old is a tuple of the files to rename.  new is a tuple of their new
        names.  In the new names, the first letter is to be removed after the first renaming pass.

        Algorithm: To avoid a naming collision, the set of file names is used to get the set of
        all characters used in naming the files.  Then a character x not in this set is gotten.
        The new names are constructed by renumbering, adding the desired prefix and suffix, then
        making the character x the first character of the new names.  Renaming can then take place
        in two passes:  the first pass the naming is done as given by (old, new).  The second pass
        removes the leading character x from the names.
        """
        currdir = P(os.getcwd())
        print(f"Current directory = {currdir.resolve()}")
        # Get list of file names to process
        old = []
        for ext in extensions:
            if ext not in d["-i"]:
                l = list(glob.glob(f"*.{ext}"))
                old.extend(l)
        old = list(sorted(old))
        # Get set of characters making up these names
        chars = set("".join(old))
        Assert(chars)
        # Find a character not in chars (start at 'A')
        i, count = 65, 0
        while True:
            count += 1
            if count > 1000:
                Error("Too many attempts to find a character")
            x = chr(i)
            if x not in chars:
                break
            i += 1
        # Make list of new names
        new = []
        w = GetWidth(len(old))
        for i, name in enumerate(old):
            p = P(name)
            prefix, suffix = d["-p"], d["-s"]
            new.append(f"{x}{prefix}{i:0{w}d}{suffix}{p.suffix}")
        if 0:  # Print old and new names
            for i, j in zip(old, new):
                print(i, j)
            exit()
        Assert(len(old) == len(new))
        return old, new

    def Show(old, new):
        """old is tuple of existing file names, new is tuple of new names.  Print out what will
        happen, removing the first letter of each name in new.
        """
        temp = tuple([i[1:] for i in new])
        if set(old) == set(temp):
            print("No renaming needed")
        else:
            w = max(len(i) for i in old)
            for i, j in zip(old, new):
                print(f"{i:{w}s} --> {j[1:]}")

    def Rename(old, new):
        """Renaming is done in two passes.  The first pass renames corresponding elements in old
        to those in new.  The second pass then renames each element in new to the same name
        without the first letter.
        """
        # Use deques so we can undo if get exception
        Old, New = deque(old), deque(new)
        oldu, newu = deque(), deque()  # Capture renames to undo
        # First pass:  old to new name with leading unique letter
        count = 0
        while Old:
            o, n = Old.popleft(), New.popleft()
            op, np = P(o), P(n)
            count += 1
            try:
                op.rename(np)
            except Exception:
                break
            else:
                # Store undo information
                oldu.append(o)
                newu.append(n)
        # If Old is not empty, we must undo
        if Old:
            t.print(f"{t.warn}Error, need to undo (run script undo.renum):")
            fp = open("undo.renum", "w")
            for i, j in zip(oldu, newu):
                print(f"mv {j} {i}")
                print(f"mv {j} {i}", file=fp)
            exit(1)
        # Success:  Do second pass:  Remove leading letter.  We'll assume these renames can't fail.
        New = deque(new)
        while New:
            n = New.popleft()
            op = P(n)
            np = P(n[1:])
            op.rename(np)


if __name__ == "__main__":
    d = {}  # Options dictionary
    ParseCommandLine(d)
    old, new = Process()
    Rename(old, new) if d["-x"] else Show(old, new)
