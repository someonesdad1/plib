"""
TODO
    - Change {1} to <1> to quantify differences
    - Mute the colors a bit

Compare the contents of two directories
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Compare the contents of two directories
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Standard imports
    import getopt
    import hashlib
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import wrap, dedent
    from color import Color, TRM as t
    from columnize import Columnize
    import strdiff

    if 0:
        import debug

        debug.SetDebugger()
if 1:  # Global variables
    P = pathlib.Path
    ii = isinstance
    t.l = t("purl")  # Only in left directory
    t.r = t("cynl")  # Only in right directory
    t.d = t("yel")  # Common, but different
    t.dbg = t("brnl")  # Debug
    t.nr = t("magl")  # Couldn't read
    t.di = t("lip")  # Difference metric
    debug = False
if 1:  # Utility

    def Debug(*p, **kw):
        if debug:
            k = kw.copy()
            k["end"] = ""
            print(f"{t.dbg}", **k)
            print(*p, **kw)
            print(f"{t.n}", **k)

    def Error(*p, status=1):
        print(*p, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] dir1 dir2
          Compare the two directories and print out the file differences.
          The file comparisons are first made by size, then by a hash if
          they are the same size.
 
          For files that are the same size but different, the notation
          <n> appended to the file name quantifies how different they
          are.  <1> means they are close (perhaps one to a few bytes are
          different), whereas <9> means nearly all the bytes are
          different.  With no <n> decoration, the two files are different
          sizes.
        Options:
            -1      Don't print out files only in dir1
            -2      Don't print out files only in dir2
            -c      Don't print out common files
            -k      Don't use color in printout to a terminal
            -d      Print debug information
            -r      Recursive compare
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-1"] = True  # Print out dir1 stuff
        d["-2"] = True  # Print out dir2 stuff
        d["-c"] = True  # Print out common stuff
        d["-d"] = False  # Debug output
        d["-k"] = True  # Use color
        d["-r"] = False  # Recurse
        try:
            opts, dirs = getopt.getopt(sys.argv[1:], "12cdhkr")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("12cdkr"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        if len(dirs) != 2:
            Usage()
        if d["-d"]:
            global debug
            debug = True
        if not d["-k"]:
            t.l = t.r = t.d = t.dbg = t.nr = t.di = ""
        return dirs

    def CleanUp():
        "Make sure ANSI colors are off"
        if d["-k"]:
            print(f"{t.n}", end="")


if 1:  # Core functionality

    def GetFiles(dir):
        p = P(dir)
        s = p.rglob("*") if d["-r"] else p.glob("*")
        s = [i.relative_to(dir) for i in s]
        s = [i for i in s if (dir / i).is_file()]
        return s

    def Hash(file):
        "Return a hash string or None if couldn't read"
        h = hashlib.sha256()
        try:
            h.update(open(file, "rb").read())
            return h.hexdigest()
        except Exception as e:
            if 0:
                print(f"Error on file '{file}'", file=sys.stderr)
                print(f"  {e}", file=sys.stderr)
            return None

    def Diffs(common, dirleft, dirright):
        """Return a set of the files that are in both directories, but
        differ.
        """
        diffs, noread = [], []
        for file in common:
            left = dirleft / file
            assert left.is_file()
            right = dirright / file
            assert right.is_file()
            # Compare by sizes
            sz_left = left.stat().st_size
            sz_right = right.stat().st_size
            if sz_left != sz_right:
                Debug(f"{file} size:  left={sz_left}   right={sz_right}")
                diffs.append(file)
                continue
            # Compare by hash
            left_hash = Hash(left)
            oops = False
            if left_hash is None:
                noread.append(str(file) + "[L]")
                oops = True
            right_hash = Hash(right)
            if right_hash is None:
                noread.append(str(file) + "[R]")
                oops = True
            if oops:
                continue
            if left_hash != right_hash:
                n = 8
                Debug(f"{file} differences in hashes ({n} chars):")
                Debug(f"  left :  {left_hash[:n]}")
                Debug(f"  right:  {right_hash[:n]}")
                diffs.append(file)
        return set(diffs), set(noread)

    def GetDecorator(item):
        left = open(dirleft / item, "rb").read()
        right = open(dirright / item, "rb").read()
        if len(left) != len(right):
            return ""
        frac = strdiff.DiffFrac(left, right)
        digit = strdiff.DiffDigit(frac, len(left))
        return f"{t.di}<{digit}>{t.n}"

    def Report(only_in_left, only_in_right, diffs, noread):
        indent = " " * 2

        def P(title, myset, decorate=False):
            print(title)
            items = sorted(list(myset))
            if decorate:
                items = [str(i) + GetDecorator(i) for i in items]
            for i in Columnize(items, indent=indent):
                print(i)
            print(f"{t.n}", end="")

        if noread:
            P(f"{t.nr}Files that couldn't be read", noread)
        if d["-1"] and only_in_left:
            P(f"{t.l}Files only in {dirleft}", only_in_left)
        if d["-2"] and only_in_right:
            P(f"{t.r}Files only in {dirright}", only_in_right)
        if d["-c"] and diffs:
            GetDecorator.color = t.d
            P(
                f"{t.d}Common files that differ ({t.di}<1>{t.d} to "
                f"{t.di}<9>{t.d} quantify differences)",
                diffs,
                decorate=True,
            )


if __name__ == "__main__":
    d = {}  # Options dictionary
    dirleft, dirright = ParseCommandLine(d)
    left, right = [set(GetFiles(i)) for i in (dirleft, dirright)]
    only_in_left = left - right
    only_in_right = right - left
    common = left & right
    diffs, noread = Diffs(common, dirleft, dirright)
    Report(only_in_left, only_in_right, diffs, noread)
