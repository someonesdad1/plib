'''
Remove blank lines from python scripts
'''
 
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <utility> Removes empty lines from python scripts.
    #∞what∞#
    #∞test∞# --test #∞test∞#
    pass
if 1:   # Standard imports
    from collections import deque
    from io import BytesIO
    import getopt
    import os
    import pathlib
    import subprocess
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
    from fel import GetEmptyLines
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [file1 [file2...]]
          Remove empty lines from python files.  The files are modified in
          place.  Use "-" to process stdin and send to stdout.
 
          Warning:  before using this script, you should convince yourself
          that it does the task you expect of it.  This script modifies the
          file with no backup made unless the -b option is used.
        Options:
            -b      Make a backup file before overwriting the original
            -d      Turn on debugging to see tokenizing details to stderr
            -n      Dry run:  show files' line numbers that will be deleted 
            -v      Verbose:  print out the files processed
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-b"] = False     # Write a backup file
        d["-d"] = False     # Debug sent to stderr
        d["-n"] = False     # Dry run:  show what files will be modified
        d["-v"] = False     # Verbose:  print processed file names
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "bdhnv", "test")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("bdnv"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o == "--test":
                Test()
        return args
if 1:   # Testing code
    def Test():
        '''Test stratgy:  
            - Make a copy of this file
            - Get its hash
            - Reformat it with black
            - Run this script on it
            - Reformat it again with black
            - Get its hash
            - Verify the two hashes match
        This will help ensure this script didn't change the source file
        significantly.
        '''
class RemoveEmptyLines:
    '''Remove empty lines from a file.  An empty line is one that
    contains only whitespace.  Usage:
        rbl = RemoveEmptyLines(file)    # Tokenizes the file 
        bool(rbl)    --> True means there are blank lines to remove
        rbl.remove() --> Removes blank lines and writes file
    '''
    def __init__(self, file, debug=None):
        '''file is either a pathlib.Path object or "-" for stdin.  If debug
        is not None, it should be a stream to write the tokenizer's output
        to (line number, token name, and token string).
        '''
        self.file = file
        if file == "-":
            self.stdin = True
            s = sys.stdin.read()            # Read stdin as a string
            self.lines = s.split("\n")
            stream = BytesIO(s.encode())    # Make it a bytes stream
        else:
            if not file.exists() and not file.is_file():
                raise ValueError(f"'{file}' is bad file")
            stream = open(self.file, 'rb')
            self.stdin = False
        self.empty_lines = GetEmptyLines(stream, debug)
    def __bool__(self):
        return bool(self.empty_lines)
    def __str__(self):
        return f"RemoveEmptyLines('{self.file}', {self.empty_lines})"
    def process(self):
        '''Remove the indicated lines from the file and write it back to the
        file.
        '''
        # Get the lines of the file
        if self.stdin:
            # Already got the lines in the constructor
            lines = self.lines
        else:
            lines = open(self.file).read().split("\n")
        n = len(lines)
        # Write backup file if needed
        if d["-b"] and not self.stdin:
            newname = str(self.file) + ".bak"
            backup_file = P(str(self.file) + ".bak")
            n = 0
            while backup_file.exists():
                backup_file =  P(newname + str(n))
            open(backup_file, "w").write('\n'.join(lines))
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
        s = '\n'.join(lines)
        if self.stdin:
            print(s, end="")
        else:
            open(self.file, "w").write('\n'.join(lines))
if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    stdout = True if "-" in files else False
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
