'''
Lump a group of files' contents together and send to stdout.
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        from pprint import pprint as pp
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        if 1:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        class G:
            pass
        g = G()
        # The following set keeps tracks of which files have been included.
        g.filelist = set()
        # This list will be the files whose contents we concatenate and
        # send to stdout.  The list keeps the file order as they are found
        # and g.filelist ensures the file is only included once.
        g.files = []
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [glob1 [glob2 ...]]
          For the current directory and below, find all filenames matching
          the given globbing expressions and concatenate their contents to
          stdout.  Each file's contents are only included once.  The files 
          are assumed to be text files.
        Example:
          'cd /plib; lump.py -r i\*\.py| char -' shows the characters used in
          the python scripts in /plib staring with 'i'.
        Options:
            -h      Print a manpage
            -r      Act recursively at and below the current directory
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-r"] = False     # Act recursively
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, regexps = getopt.getopt(sys.argv[1:], "hr") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("r"):
                d[o] = not d[o]
            elif o == "-h":
                Usage(status=0)
        return regexps
if 1:   # Core functionality
    def GetFileList(globs):
        'Put files to be processed into g.files.'
        p = P(".")
        list_of_files = []
        for glob in globs:
            list_of_files.extend(p.rglob(glob) if d["-r"] else p.glob(glob))
        got = set()     # Keep track of files we've seen
        for i in list_of_files:
            if i in got:
                continue
            else:
                got.add(i)
                g.files.append(i)
    def GetFileData():
        for file in g.files:
            sys.stdout.write(open(file).read())

if __name__ == "__main__":
    d = {}      # Options dictionary
    globs = ParseCommandLine(d)
    GetFileList(globs)
    GetFileData()
