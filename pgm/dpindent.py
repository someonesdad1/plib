"""
Indenting script for text files used as outlines

    The basic idea is that vim can fold these files while being used as a fast
    editor.  This script will do the indenting that should be easy in vim, but
    is not.  Here are the things I'm looking for:

    * I use bulleted lists a lot, especially for outlines.  The script should
    allow lists to start with the following items

        * Popular single characters:  *, -, +, o, some Unicode like ★, ☒, etc.
        * (1), (1.1), etc.
        * 1), 1.1)etc.
        * 1., 1.1, etc.  These are more problematic because they are often in
          plain text.
        * Ignore bare numbers like '1', as such things are in text too much.

Prototype

    Get working with *-+ only.

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
    # Indents bulleted lists for outlines
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Standard imports
    import getopt
    import os
    import pathlib
    import re
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import wrap, dedent
    from color import C, PrintMatch
if 1:  # Global variables
    P = pathlib.Path
    ii = isinstance
if 1:  # Regular expressions
    # Match bullets
    relem = re.compile(r"^\s*[\*\-+]\s")
    # Matches beginning whitespace
    rws = re.compile(r"^(\s+)")
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Manpage():
        print(
            dedent(f"""
        This script will indent and format to-do lists.  
        """)
        )
        exit(0)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] [file]
          Indents the to-do list in file.  Use - to read from stdin.  The
          indented information is sent to stdout.
        Options:
            -h      Print a manpage
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = 3  # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o in ("-h", "--help"):
                Manpage()
        if len(args) > 1:
            Error("Only one argument allowed")
        return args


if 1:  # Core functionality
    pass
if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    lines = [i.rstrip("\n") for i in open(args[0]).readlines()]
    for line in lines:
        if 0:
            # Use for debugging
            PrintMatch(line, relem)
        else:
            mo = relem.match(line)
            if mo:
                s = mo.group()
                print(repr(s))
