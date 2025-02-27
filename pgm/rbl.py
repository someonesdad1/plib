"""
Remove blank lines from python scripts

    Motivation:  vertical real estate on a terminal screen is precious and
    I like to see as much information as possible when editing code.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # <utility> Remove whitespace-only lines from python scripts
    ##∞what∞#
    ##∞test∞# --test #∞test∞#
    pass
if 1:  # Standard imports
    from collections import deque
    from io import BytesIO
    import getopt
    import hashlib
    import os
    import re
    from pathlib import Path as P
    import subprocess
    import sys
if 1:  # Custom imports
    from wrap import wrap, dedent
    from fel import GetEmptyLines
    from lwtest import Assert
    from color import t

    if 0:
        import debug

        debug.SetDebugger()
if 1:  # Global variables
    ii = isinstance
    t.err = t("redl")
    bup_ext = ".rblbak"
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] [file1 [file2...]]
          Remove lines of only whitespace from python files (empty lines in
          comments and multiline strings are not removed).  The files are
          modified in place.  Use "-" to process stdin and send to stdout.
          A backup file will be made with the extension ".rblbak".
 
          The script by default works on python files, using the tokenizer
          to identify blank lines.  It may also work on plain text files,
          but to be sure, use the -t option, which uses regular expressions
          instead.
        Options:
            -b      Don't make a backup file before overwriting the original
            -d      Turn on debugging to see tokenizing details to stderr
            -n      Dry run:  show files' line numbers that will be deleted 
                    (only works for python files)
            -t      Process files as plain text
            -v      Verbose:  print out the files processed
                    (only works for python files)
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-b"] = True  # Write a backup file
        d["-d"] = False  # Debug sent to stderr to see tokenizing
        d["-n"] = False  # Dry run:  show what files will be modified
        d["-t"] = False  # Process plain text files
        d["-v"] = False  # Verbose:  print processed file names
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "bdhnTtv")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("bdnTtv"):
                d[o] = not d[o]
            elif o == "-h":
                Usage(status=0)
        return args


if 1:  # Core functionality

    class RemoveEmptyLines:
        """Remove empty lines from a file.  An empty line is one that
        contains only whitespace.  Usage:
            rbl = RemoveEmptyLines(file)    # Tokenizes the file
            bool(rbl)    --> True means there are blank lines to remove
            rbl.remove() --> Removes blank lines and writes file
        """

        def __init__(self, file, debug=None):
            """file is either a pathlib.Path object or "-" for stdin.  If debug
            is not None, it should be a stream to write the tokenizer's output
            to (line number, token name, and token string).
            """
            self.file = file
            self.stdin = True if file == "-" else False
            if self.stdin:
                s = sys.stdin.read()  # Read stdin as a string
                self.lines = s.split("\n")
                stream = BytesIO(s.encode())  # Make it a bytes stream
            else:
                if not file.exists() and not file.is_file():
                    raise ValueError(f"'{file}' is bad file")
                stream = open(self.file, "rb")
            self.empty_lines = GetEmptyLines(stream, debug)

        def __bool__(self):
            return bool(self.empty_lines)

        def __str__(self):
            return f"RemoveEmptyLines('{self.file}', {self.empty_lines})"

        def process(self):
            """Remove the indicated lines from the file and write it back to the
            file.
            """
            # Get the lines of the file
            if self.stdin:
                # Already got the lines in the constructor
                lines = self.lines
            else:
                lines = open(self.file).read().split("\n")
            n = len(lines)
            # Write backup file if needed
            if d["-b"] and not self.stdin:
                newname = str(self.file) + ".rblbak"
                backup_file = P(str(self.file) + ".rblbak")
                n = 0
                # Add an integer when the backup file already exists
                while backup_file.exists():
                    backup_file = P(newname + str(n))
                open(backup_file, "w").write("\n".join(lines))
            # Insert an empty line so that our list of line numbers to be
            # removed can be used directly
            lines.insert(0, "")
            # Remove lines starting from the back so we don't mess up our
            # indexes
            for i in reversed(self.empty_lines):
                del lines[i]
            # Remove the front line we added
            lines.pop(0)
            # Write back to the file
            s = "\n".join(lines)
            if self.stdin:
                print(s, end="")
            else:
                open(self.file, "w").write("\n".join(lines))

    def ProcessTextFile(file):
        """Process the indicated file using a regular expression to
        identify blank lines.
        """
        r = re.compile(r"^\s*$")
        if file == "-":
            # Note stdin is simply sent to stdout since it doesn't come
            # from a file in the file system.
            for line in sys.stdin.readlines():
                mo = r.match(line)
                if not mo:
                    print(line, end="")  # end needed because \n is in line
        else:
            Assert(ii(file, P))
            # Get the file's lines.  This is the lazy programmer's way of
            # doing this, but could run out of memory for large files.
            # However, virtually no python script will be large enough for
            # this to happen (my biggest python files are under 5 MB).
            try:
                lines = open(file).readlines()
            except Exception:
                print(f"{t.err}Couldn't read {file!r}", file=sys.stderr)
                return
            # Move the file to the backup file
            if not d["-b"]:
                newname = file.name + bup_ext
                if P(newname).exists():
                    print(
                        f"{t.err}Backup file {newname!r} already exists",
                        file=sys.stderr,
                    )
                    return
                try:
                    file.rename(newname)
                except Exception:
                    print(
                        f"{t.err}Couldn't rename {file!r} to {newname!r}",
                        file=sys.stderr,
                    )
                    return
            # Write the processed file
            with open(file, "w") as f:
                for line in lines:
                    mo = r.match(line)
                    if not mo:
                        print(line, file=f)


if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    stdout = True if "-" in files else False
    if d["-t"]:
        for file in files:
            ProcessTextFile(P(file) if file != "-" else file)
    else:
        for file in files:
            f = P(file) if file != "-" else "-"
            if d["-v"] and not stdout:
                # Don't print the file name if stdin is one of the files, as
                # we'll mess up the stream
                print(file)
            rbl = RemoveEmptyLines(f, sys.stderr if d["-d"] else None)
            if d["-n"] and rbl:
                print(rbl)
            else:
                rbl.process()
