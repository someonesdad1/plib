"""
List my shell functions
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # List my shell functions
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from collections import deque, defaultdict
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:  # Custom imports
        from lwtest import Assert
        from color import t
        from dpprint import PP

        pp = PP()  # Screen width aware form of pprint.pprint
        from get import GetLines
        from wrap import dedent
        from columnize import Columnize
    if 1:  # Global variables

        class G:
            # Storage for global variables as attributes
            pass

        g = G()
        g.dbg = False
        ii = isinstance
        # Core function definition files
        g.funcfiles = [
            P("/home/don/.0rc/dot_func"),
            P("/home/don/.0rc/dot_bin"),
        ]
        # Dictionary of function instances:  key = function name, value = Function instance
        g.funcs = {}
        # Dictionary of functions by category name
        g.categories = None
if 1:  # Classes

    class Function:
        """Encapsulate a shell function's source code.  Attributes:
        name    Name of the function
        file    File it came from
        lines   List of source lines
        num     Line number 'function' line starts in file (1-based)
        cat     Category of function
        descr   Description of the function's purpose
        """

        def __init__(self, lines, file):
            """lines will be a list of (linenumber, line) where linenumbers are 1-based.  file is a
            Path instance.
            """
            Assert(ii(file, P))
            Assert(ii(lines, (list, tuple)))
            # Get details.  The required first line form is
            # 'function name ## <category_string> Description'.
            num, first_line = lines[0]
            f = first_line.split()
            Assert(f[0] == "function")
            name = f[1]
            Assert(f[2] == "##")
            cat = f[3].replace("<", "").replace(">", "")
            descr = " ".join(f[4:])
            # Attributes
            self.name = name
            self.file = file
            self.lines = [j for i, j in lines]
            self.num = int(num)
            self.cat = cat
            self.descr = descr

        def __str__(self):
            "The string representation is used to print the function's source code"
            o = []
            for line in self.lines:
                o.append(f"{line}")
            return "\n".join(o)

        def __repr__(self):
            return f"Function<{self.name} [{self.file.name}:{self.num}]>"


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

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] [func1 [func2...]]
          List my shell functions.
        Options:
            -a      List all functions with description
            -h      Print a manpage
            -o      List other functions (from e.g., gawk, conda, git, etc.)
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False  # List all functions
        d["-o"] = False  # List non-DP functions
        try:
            opts, args = getopt.getopt(sys.argv[1:], "aho")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("ao"):
                d[o] = not d[o]
            elif o == "-h":
                Usage(status=0)
        GetColors()
        g.W, g.L = GetScreen()
        return args


if 1:  # Core functionality

    def GetFunctionInstance(dq, file):
        """dq is a deque of (linenum, line), file is the Path the function came from.  The first
        line of the function must start with the word "function.  The next line must start with
        "{".  Then any number of lines can follow until a line starts with "}", which ends the
        function.  Any number of blank lines can follow, then either another function starts or
        #END# is encountered.
        """
        Assert(dq[0][1].startswith("function "))
        lines = [dq.popleft()]
        Assert(dq[0][1].startswith("{"))
        lines.append(dq.popleft())
        while not dq[0][1].startswith("}"):
            lines.append(dq.popleft())
        Assert(dq[0][1].startswith("}"))
        lines.append(dq.popleft())
        # Ignore any blank lines
        while not dq[0][1].strip():
            dq.popleft()
        Assert(dq[0][1].startswith("function ") or dq[0][1] == "#END#")
        return Function(lines, file)

    def ReadFunctions():
        for file in g.funcfiles:
            # Create a deque of (n, line) where n is the 1-based number of the line in the source
            # file and line is that line's string.
            dq = deque((i + 1, j) for i, j in enumerate(GetLines(file, nonl=True)))
            # Position at #START#
            while dq and dq[0][1] != "#START#":
                n, line = dq.popleft()
            n, line = dq.popleft()
            # Now we're positioned on the first of the actual functions' code
            while dq and dq[0][1] != "#END#":
                func = GetFunctionInstance(dq, file)
                if func.name in g.funcs:
                    print(f"{func.name!r} defined more than once")
                    exit(1)
                g.funcs[func.name] = func
        # Get non-DP functions from environment dpother
        other = set(os.environ["dpother"].split("\n"))
        g.other = list(sorted(other - set(g.funcs)))
        # Get information needed for printing
        g.names = sorted(g.funcs.keys())
        g.w_names = max(len(i) for i in g.names)
        g.w_cat = max(len(g.funcs[i].cat) for i in g.names)

    def GetCategories():
        g.categories = defaultdict(list)
        for name in g.funcs:
            func = g.funcs[name]
            g.categories[func.cat].append(func.name)

    def ListCategory(cat):
        Assert(cat in g.categories)
        t.print(f"{t('ornl')}{cat}")
        for i in Columnize(sorted(g.categories[cat]), indent=" " * 2):
            print(i)

    def ListByCategory():
        for cat in sorted(g.categories):
            ListCategory(cat)

    def ListAllDPFunctions(category=None):
        for name in g.names:
            f = g.funcs[name]
            if category is not None and f.cat != category:
                continue
            print(f"{name:{g.w_names}s} {f.cat:{g.w_cat}s} {f.descr}")


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    ReadFunctions()
    GetCategories()
    if args:
        # List the source code of the given functions.  If the argument is a category, list the
        # functions in that category.
        for arg in args:
            if arg in g.categories:
                if d["-a"]:
                    ListAllDPFunctions(arg)
                else:
                    ListCategory(arg)
            elif arg in g.funcs:
                print(g.funcs[arg])
            else:
                print(f"{arg!r} not recognized")
    else:
        if d["-a"]:
            # List all my functions
            ListAllDPFunctions()
        elif d["-o"]:
            # List non-DP functions
            for i in Columnize(g.other):
                print(i)
        else:
            ListByCategory()
