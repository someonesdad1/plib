"""
Find files that use color.py
"""

if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Program description string
    # ∞what∞#
    # ∞test∞# none #∞test∞#
    # Standard imports
    import getopt
    import os
    from pathlib import Path as P
    import sys
    import re
    from pdb import set_trace as xx

    # Custom imports
    from get import GetLines
    from wrap import wrap, dedent

    # Global variables
    ii = isinstance
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ah")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args


if 1:  # Core functionality
    r = re.compile(
        r"from\s+color\s+import|"
        r"from\s+kolor\s+import|"
        r"import\s.*color|"
        r"import\s.*kolor"
    )
    print("Looking for 'kolor' only")
    r = re.compile(
        r"from\s+kolor\s+import|"
        r"import\s.*kolor"
    )

    def ProcessFile(file):
        "Return True if it has the regexp"
        lines = GetLines(file, script=True)
        for line in lines:
            if r.search(line):
                return True
        return False

    def ProcessDir(dir, recursive=False):
        print(f"{dir}: ", end=" ")
        old = os.getcwd()
        os.chdir(dir)
        p = P(".")
        s = "**/*.py" if recursive else "*.py"
        n = 0
        for file in p.glob(s):
            if ProcessFile(file):
                print(file, end=" ")
                n += 1
        print(f" <{n}>")
        os.chdir(old)


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    dirs = (".", "pgm", "rgb", "test")
    for dir in dirs:
        ProcessDir(dir)
