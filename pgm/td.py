"""
TODO
    - Another problem:  comments will be found in multiline strings
    - Sometimes comments are needed in the code.  Let these be indicated by
      the string "##".
    - Ignore empty comments or ones with only hyphens or '='
    - Use inspect to get comments, as the comments need to be associated
      with the function.  Just using a regexp finds situations like

                def A():
                    pass
                    # This is a comment in A
        def B()
            pass

      and the comment will be falsely coupled with B().

      clean.py:161 showed this problem.

      However, this is nontrivial if the found function/class is in a
      nested scope.

Highlights todo items in python scripts

    My standard way of composing python scripts is to never put comments
    before functions or classes.  Because of this convention, then an
    existing comment can be an indicator of something that needs to be done
    in that file.  This scripts finds and prints those items out.

"""

if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Highlights todo items in python scripts
    ##∞what∞#
    ##∞test∞# #∞test∞#
    # Standard imports
    import getopt
    import inspect
    import os
    import re
    from pathlib import Path as P
    import sys

    # from pdb import set_trace as xx
    from collections import deque
    from pprint import pprint as pp

    # Custom imports
    from wrap import wrap, dedent
    from color import Color, TRM as t
    from get import GetLines

    # Global variables
    ii = isinstance
    w = int(os.environ.get("COLUMNS", "80")) - 1
    L = int(os.environ.get("LINES", "50"))
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] [file1 [file2 ...]]
          Print out comments before functions and classes in python
          scripts, as they are interpreted as todo items.  If a file item
          is a directory, all python files in that directory are searched.
          Note:  A line beginning with '##' is NOT interpreted as a
          todo-comment, as sometimes source files need such lines and I
          don't want them to be marked as a todo item.
        Options:
            -c      Colorize the output
            -l      List files with todo items
            -s      Strip leading whitespace off the todo items
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-c"] = False
        d["-l"] = False
        d["-s"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "chls", ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cls"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug

                debug.SetDebugger()
                global dbg
                dbg = True
        if not args:
            Usage()
        return args


if 1:  # Core functionality

    def Colorize():
        c = d["-c"]
        t.file = t("yell") if c else ""
        t.linenum = t("grnl") if c else ""
        t.klass = t("purl") if c else ""
        t.func = t("royl") if c else ""
        t.todo = t("cynl") if c else ""

    def ProcessDirectory(dir):
        for file in dir.glob("*.py"):
            Process(file)

    def IsMatch(line):
        """Return matched string if there's a match; '' if not."""
        for r in R:
            mo = r.match(line)
            if mo:
                match = mo.groups()[0]
                return match
        return ""

    def IsComment(line):
        """The line is declared to be a comment if it begins with a single
        '#' character.  Because sometimes comments are wanted in source and
        I don't want them to be interpreted as a todo-comment, they will be
        introduced with '##' and will be ignored.
        """
        s = line.lstrip()
        if s.startswith("##"):
            return False
        return s and s[0] == "#"

    def DumpLines(file, name, linenum, out):
        """file is the file being processed, name is the class or function
        name that matched, linenum is the 1-based line number of the line
        in the file, and out is the set of comment lines.
        """
        if d["-l"]:
            print(file)
            return
        # Print header line
        print(f"{t.file}{file}:{t.linenum}{linenum}  ", end="")
        if "class" in name:
            print(f"{t.klass}{name}{t.n}")
        elif "def" in name:
            print(f"{t.func}{name}{t.n}")
        else:
            raise ValueError(f"'{name!r}' is a bad name")
        # Print comment contents
        for line in out:
            # Substitute ' ' for the first '#'
            line = line.replace("#", " ", 1)
            t.print(f"{t.todo}{line}")

    def Process(file):
        lines = GetLines(file, nonl=True)
        # Decorate with line numbers
        lines = [(i + 1, s) for i, s in enumerate(lines)]
        lines = deque(reversed(lines))
        # found will be a list of tuples of the form
        # (file, name, linenum, reversed(out)).  These are saved so they
        # can be sorted by line number before printing to stdout.
        found = []
        while lines:
            linenum, line = lines.popleft()
            if dbg:  # Show the line read in
                t.print(f"{t('gry')}{line!r}")
            name = IsMatch(line)
            if name:
                if dbg:
                    t.print(f"{t('yel')}Regexp match:  {line!r}")
                out = []
                while lines and IsComment(lines[0][1]):
                    if d["-s"]:
                        out.append(lines.popleft()[1].lstrip())
                    else:
                        out.append(lines.popleft()[1])
                if out:
                    found.append((file, name, linenum, reversed(out)))

        # Sort by line number
        def f(x):
            return x[2]

        for item in sorted(found, key=f):
            DumpLines(*item)


if __name__ == "__main__":
    dbg = False
    d = {}  # Options dictionary
    R = [
        re.compile(r"^\s*(def\s+[A-Za-z_][A-Za-z_0-9]*)(.*):.*$"),
        re.compile(r"^\s*(class\s+[A-Za-z_][A-Za-z_0-9]*)(\(.*\))?:.*$"),
    ]
    args = ParseCommandLine(d)
    Colorize()
    for arg in args:
        file = P(arg)
        if file.is_dir():
            ProcessDirectory(file)
        else:
            Process(file)
