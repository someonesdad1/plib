"""
Generate an HTML difference of two files and launch in browser
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # View diff between two files in browser
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        import difflib
        import getopt
        import sys
        import tempfile
        import time
        from pathlib import Path as P
    if 1:  # Custom imports
        from wrap import dedent
        from launch import Launch
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(d, status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] file1 file2
          Show an HTML difference between the two files in a browser.
        Options:
          -i   Ignore case
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-i"] = False
        try:
            opts, files = getopt.getopt(sys.argv[1:], "hi")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("i"):
                d[o] = not d[o]
            elif o == "-h":
                Usage(d, status=0)
        if len(files) != 2:
            Usage(d)
        return files


if 1:  # Core functionality

    def DiffFiles(file1, file2):
        f1, f2 = P(file1), P(file2)
        if not f1.exists():
            Error(f"{file1!r} does not exist")
        if not f2.exists():
            Error(f"{file2!r} does not exist")
        # Get the contents of the text files
        old = f1.open().read()
        new = f2.open().read()
        if d["-i"]:
            # Convert both to lowercase
            old = old.lower()
            new = new.lower()
        # Construct an HTML difference
        h = difflib.HtmlDiff()
        s = h.make_file(old.split("\n"), new.split("\n"))
        # Put the two files' differences into a temporary HTML file
        try:
            _, name = tempfile.mkstemp(suffix=".html", dir="/tmp")
            name = P(name)
            with open(name, "w") as fd:
                fd.write(s)
            # Open the temp file in a browser
            Launch(name)
            # Sleep for a while before deleting the file; otherwise, the file can be deleted before
            # the browser opens it
            time.sleep(0.25)
        finally:
            name.unlink()


if __name__ == "__main__":
    d = {}  # Options dictionary
    file1, file2 = ParseCommandLine(d)
    DiffFiles(file1, file2)
