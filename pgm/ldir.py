"""
List the directories in the current directory
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # List directories in the current directory
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        import sys
        import os
        import getopt
        import glob
        import pathlib
    if 1:  # Custom imports
        from wrap import dedent
        import columnize
        from color import t

        _no_color = True
        if sys.stdout.isatty():
            try:
                import color as color

                _no_color = False
            except ImportError:
                pass
        if _no_color:

            class Color:  # Swallow function calls
                def fg(self, *p):
                    pass

                def __getattr__(self, a):
                    pass

            color = Color()
    if 1:  # Global variables
        P = pathlib.Path
        ii = isinstance
if 1:  # Utility

    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )

    def GetColors(on=True):
        t.dbg = t("cyn") if on else ""
        t.dir = t("lipl") if on else ""
        t.hdr = t("trql") if on else ""
        t.N = t.n if on else ""
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

    def Usage(d, status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} dir1 [dir2 ...]
          Print the directories under the given directories.  Defaults to
          '.' if no directories given.
        Options
          -a    Show hidden directories
          -c    Don't use color
          -F    Append / to the names
          -f    Fold the names in sorting
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False  # Show hidden directories
        d["-c"] = True  # Use color
        d["-F"] = False  # Append /
        d["-f"] = False  # Fold the sorting
        try:
            optlist, directories = getopt.getopt(sys.argv[1:], "acFfh")
        except getopt.GetoptError as e:
            msg, option = e
            print(msg)
            exit(1)
        for o, a in optlist:
            if o[1] in list("acFf"):
                d[o] = not d[o]
            elif o == "-h":
                Usage(d, status=0)
        GetColors(d["-c"])
        if not directories:
            directories = ["."]
        return directories


if 1:  # Core functionality

    def ProcessDir(dir, header=True):
        assert ii(dir, P)
        if not dir.is_dir():
            return
        # Get list of directories
        os.chdir(dir)  # Now directory list will be relative to dir
        dirs = []
        for i in P(".").glob("*"):
            if i.is_dir():
                if d["-a"]:
                    # Show all directories
                    dirs.append(i)
                else:
                    # Don't show hidden directories
                    if not str(i).startswith("."):
                        dirs.append(i)
        if dirs:
            # Decorate with ending '/' to help flag that they are directories.  Remember they are
            # PosixPath objects.
            if d["-F"]:
                dirs = [str(i) + "/" for i in dirs]
            else:
                dirs = [str(i) for i in dirs]
            dirs = sorted(dirs, key=str.lower) if d["-f"] else sorted(dirs)
            if header:
                print(f"{t.hdr}Directory {dir}:")
            s = columnize.Columnize(dirs)
            for line in s:
                t.print(f"{t.dir}{line}")


if __name__ == "__main__":
    d = {}  # Options dictionary
    directories = ParseCommandLine(d)
    for dir in directories:
        ProcessDir(P(dir), len(directories) > 1)
