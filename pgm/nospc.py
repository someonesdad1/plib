"""
Replace empty lines from stdin with '^ $'.  The basic use case is to remove
empty lines of a file in the editor.
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
        # Replace empty lines with one space
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
    if 1:  # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
    if 1:  # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] [file1 ...]
          Read stdin as text and replace lines that match '^$' with one
          space character.  Any files on command line are included.
        Options:
            -h      Print a manpage
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        try:
            opts, files = getopt.getopt(sys.argv[1:], "h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o == "-h":
                Usage(status=0)
        return files


if 1:  # Core functionality

    def Process(string):
        for line in string.split("\n"):
            if not line:
                print(" ")
            else:
                print(line)


if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    Process(sys.stdin.read())
    for file in files:
        Process(open(file).read())
