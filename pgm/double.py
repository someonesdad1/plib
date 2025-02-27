"""
Script to double-space text files and insert a line of hyphens between each
file on the command line.

    The use case is when I convert a group of Open Office Writer documents
    to plain text so I can convert them to LaTeX.  The first step is to
    save the *.odt files as UTF-8-encoded text files, then coalesce them
    into one document with this script.

"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Script to double-space text files
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import re
        import sys
        from pdb import set_trace as xx
    if 1:  # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
    if 1:  # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        nl = "\n"
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] file1 [file2...]
          Print the lines of the text files to stdout with every newline
          replaced by two newlines.  A line of hyphens will separate the
          files.  All sequences of multiple newlines will first be replaced
          by one newline unless -v is used.
        Options:
            -h      Print a manpage
            -v      Treat the files verbatim
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-v"] = False  # Treat files verbatim
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, files = getopt.getopt(sys.argv[1:], "hv", ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("v"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        return files


if 1:  # Core functionality

    def ProcessFile(file, hyphens=True):
        s = open(file, "r").read()
        if d["-v"]:
            s = s.replace(nl, nl * 2)
        else:
            s = r.sub(nl * 2, s)
        s = s.rstrip() + nl
        print(s)
        if hyphens:
            print("-" * 70, end=nl * 2)


if __name__ == "__main__":
    d = {}  # Options dictionary
    r = re.compile(r"\n+", re.S)
    files = ParseCommandLine(d)
    n = len(files)
    for i in range(n):
        if i == n - 1:
            ProcessFile(files[i], hyphens=False)
        else:
            ProcessFile(files[i])
