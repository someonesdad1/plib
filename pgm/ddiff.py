'''
Compare the contents of two directories
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
    # Compare the contents of two directories
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Standard imports
    import getopt
    import hashlib
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
    from clr import Clr
    from columnize import Columnize
    import strdiff
    if 1:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    c = Clr()
    c.l = c("lgrn")     # Only in left directory
    c.r = c("lred")     # Only in right directory
    c.d = c("lyel")     # Common, but different
    c.dbg = c("cyn")    # Debug
    c.nr = c("lmag")    # Couldn't read
    c.di = c("lyel", "lred")  # Difference metric
    debug = False
if 1:   # Utility
    def Debug(*p, **kw):
        if debug:
            k = kw.copy()
            k["end"] = ""
            print(f"{c.dbg}", **k)
            print(*p, **kw)
            print(f"{c.n}", **k)
    def Error(*p, status=1):
        print(*p, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] dir1 dir2
          Compare the two directories and print out the file differences.
          The file comparisons are first made by size, then by an SHA-256
          hash if they are the same size.
 
          For files that are the same size but different, the notation
          {{n}} appended to the file name quantifies how different they
          are.  {{1}} means they are close (perhaps one to a few bytes are
          different), whereas {{9}} means nearly all the bytes are
          different.  With no {{n}} decoration, the two files are different
          sizes.
        Options:
            -c      Use color in printout to a terminal
            -d      Print debug information
            -r      Recursive compare
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = False         # Use color
        d["-d"] = False         # Debug output
        d["-r"] = False         # Recurse
        try:
            opts, dirs = getopt.getopt(sys.argv[1:], "cdhr")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cdr"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        if len(dirs) != 2:
            Usage()
        if d["-d"]:
            global debug
            debug = True
        if not d["-c"]:
            c.reset()
            c.l = c.r = c.d = c.dbg = c.nr = c.di = ""
        return dirs
if 1:   # Core functionality
    def GetFiles(dir):
        p = P(dir)
        s = p.rglob("*") if d["-r"] else p.glob("*")
        s = [i.relative_to(dir) for i in s]
        s = [i for i in s if (dir/i).is_file()]
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
        '''Return a set of the files that are in both directories, but
        differ.
        '''
        diffs, noread = [], []
        for file in common:
            left = dirleft/file
            assert(left.is_file())
            right = dirright/file
            assert(right.is_file())
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
        left  = open(dirleft/item, "rb").read()
        right = open(dirright/item, "rb").read()
        if len(left) != len(right):
            return ""
        frac = strdiff.DiffFrac(left, right)
        digit = strdiff.DiffDigit(frac, len(left))
        return f"{{{digit}}}"
    def Report(only_in_left, only_in_right, diffs, noread):
        indent = " "*2
        def P(title, myset, decorate=False):
            print(title)
            items = sorted(list(myset))
            if decorate:
                items = [str(i) + GetDecorator(i) for i in items]
            for i in Columnize(items, indent=indent):
                print(i)
            print(f"{c.n}", end="")
        if noread:
            P(f"{c.nr}Files that couldn't be read", noread)
        if only_in_left:
            P(f"{c.l}Files only in {dirleft}", only_in_left)
        if only_in_right:
            P(f"{c.r}Files only in {dirright}", only_in_right)
        if diffs:
            GetDecorator.color = c.d
            P(f"{c.d}Common files that differ ({{1}} to {{9}} quantify differences)",
              diffs, decorate=True)
if __name__ == "__main__":
    d = {}      # Options dictionary
    dirleft, dirright = ParseCommandLine(d)
    left, right = [set(GetFiles(i)) for i in (dirleft, dirright)]
    only_in_left = left - right
    only_in_right = right - left
    common = left & right
    diffs, noread = Diffs(common, dirleft, dirright)
    Report(only_in_left, only_in_right, diffs, noread)
