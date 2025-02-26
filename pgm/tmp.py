"""
Show temporary files in current directory
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Show temporary files in current directory
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import getopt
        import os
        import re
        from pathlib import Path as P
        import sys
    if 1:  # Custom imports
        from wrap import dedent
        from color import t
        from util import Unique
        from columnize import Columnize
    if 1:  # Global variables

        class G:
            pass

        g = G()
        dbg = False
        t.dbg = t("lill") if dbg else ""
        t.N = t.n if dbg else ""
        ii = isinstance
        g.W = int(os.environ.get("COLUMNS", "80")) - 1
        g.L = int(os.environ.get("LINES", "50"))
        g.tmp_names = set(
            """
        """.split()
        )
        g.glob = """
            *~ *.bak *.o *.obj *.pyc *.pyo *.orig
               *.BAK *.O *.OBJ *.PYC *.PYO *.ORIG
               tags [0-9] pnp
        """.split()
if 1:  # Utility

    def Dbg(*p, **kw):
        if dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] dir1 [dir2...]
          Show temporary files in the indicated directories.
        Options:
            -h      Print a manpage
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False  # Describe this option
        try:
            opts, dirs = getopt.getopt(sys.argv[1:], "h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-h":
                Usage(status=0)
        if not dirs:
            dirs = ["."]
        return dirs


if 1:  # Core functionality

    def FindTemp(dir, multiple=False):
        """Print out the temporary files in the indicated directory.  If
        multiple is True, then print the directory's name before printing
        the results.
        """
        found, p = [], P(dir)
        if not p.exists():
            print(f"{dir!r} doesn't exist", file=sys.stderr)
        for glb in g.glob:
            found.extend(p.glob(glb))
        if found:
            if multiple:
                print(f"{dir}:")
            ind = " " * 2 if multiple else ""
            for i in Columnize(sorted(found), indent=ind):
                print(i)


if __name__ == "__main__":
    d = {}  # Options dictionary
    dirs = ParseCommandLine(d)
    dirs = list(Unique(dirs))
    for dir in Unique(dirs):
        FindTemp(dir, multiple=len(dirs) > 1)
