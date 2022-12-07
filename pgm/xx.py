'''
Utility to find xx's in files.  I use 'xx' to flag temporary code or
bugs that need to be fixed. 
'''
if 1:  # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Find files with 'xx' strings to indicate To Do items.
        #∞what∞#
        #∞test∞# #∞test∞#
    # Imports
        import sys
        import os
        import getopt
        import pathlib
        import re
        from glob import glob
        from pdb import set_trace as xx
    # Custom imports
        from wrap import dedent
        import color as C
        from columnize import Columnize
    # Global variables
        class G: pass
        P = pathlib.Path
        ii = isinstance
        # Color highlighting
        G.file = C.fg(C.brown, s=1)
        G.norm = C.normal(s=1)
        # There are some files that can be ignored:
        G.files_to_ignore = set((
            "word_syllables.py",
            "words.py",
            "words",
            "asciify_make.py",
            "xx.py",
        ))
        # File globbing expressions for the default files to search
        G.source = list(sorted('''

            *.bas *.c *.cpp *.cxx *.f *.f90 *.h *.hxx *.ino *.java *.pro
            *.py ?akefile *.awk *.sh *.bash

        '''.split()))
        # This is the string we'll search for
        G.s = r"\bxx\b"
        # Regular expression to find 'xx'.
        G.r = re.compile(G.s)
        # Regular expression to find 'xx' in string with newlines.  This is
        # quickly used to scan a whole file.
        G.R = re.compile(G.s, re.M)
if 1:   # Utility
    def Usage(status=1):
        name = sys.argv[0]
        print(dedent(f'''
        Usage:  {name} [item1 [item2 ...]]
          Searches files or directories given on the command line for the
          string {d["-x"]!r} and prints out the name of those that contain it.  If
          the item is a directory, typical source files are printed if they
          contain {d["-x"]!r}.

          If no files are given on the command line, then the program
          searches files that are typical source code file names.
        Options:
          -n    Print the line number and line where {d["-x"]!r} occurs
          -r    Recursively descend directories
          -s    Print source code file extensions examined
          -x x  Set the trigger string to look for [{d["-x"]!r}]
        '''[1:-1]))
        exit(status)
    def ParseCommandLine(d):
        d["-n"] = False     # Print line number & line
        d["-r"] = False     # Recursive for directories
        d["-s"] = False     # Print list of regexps used
        d["-x"] = "xx"      # String to search for
        try:
            optlist, files = getopt.getopt(sys.argv[1:], "hnrsx:")
        except getopt.GetoptError as str:
            msg, option = str
            print(msg)
            sys.exit(1)
        for o, a in optlist:
            if o[1] in "nrs":
                d[o] = not d[o]
            if o == "-x":
                d["-x"] = a
                global G
                G.s = fr"\b{a}\b"
                G.r = re.compile(G.s)
                G.R = re.compile(G.s, re.M)
            if o == "-h":
                Usage()
        if d["-s"]:
            print("List of type of source code files searched:")
            for i in Columnize(G.source, indent=" "*2):
                print(i)
            exit(0)
        if not files:
            Usage()
        return files
if 1:   # Core functionality
    def Ignore(line):
        '''Return True if this line should be ignored.
        '''
        line = line.strip()
        if line.find("from pdb import set_trace as xx") != -1:
            return True
        elif line.find("xxrmxx") != -1 or line.find("xxmrxx") != -1:
            return True
        elif line.find("xx()") != -1:
            return True
        return False
    def SearchFile(file, dir, d):
        "Search the given file for 'xx'"
        assert(ii(file, P))
        if str(file) == script or str(file) in files_to_ignore:
            return
        s = open(file).read()
        # Parse into lines and search each line.  If a match is found,
        # print out the line number and line.
        lines, results = s.split("\n"), []
        for i, line in enumerate(lines):
            if Ignore(line):
                continue
            mo = r.search(line)
            if mo:
                results.append(f"  {i + 1:5d}:  {line.strip()}")
        pth = file
        if dir != ".":
            pth = os.path.join(dir, pth)
        if not d["-v"] and results:
            print(pth)
            return
        if results:
            print(pth)
            print("\n".join(results))
    def DirSearch(dir):
        assert(ii(dir, P) and dir.is_dir())
        glb = dir.rglob if d["-r"] else dir.glob
        for glob_pattern in G.source:
            for file in glb(glob_pattern):
                if file.is_dir():
                    continue
                FileSearch(file)
    def FileSearch(file):
        assert(ii(file, P) and file.is_file())
        if file.name in G.files_to_ignore:
            return
        s = file.read_text()
        if not G.R.search(s):
            return
        # Search each line
        results = []
        for i, line in enumerate(s.split("\n")):
            if Ignore(line):
                continue
            mo = G.r.search(line)
            if mo:
                results.append((i + 1, line))
        if results:
            if d["-n"]:
                print(f"{G.file}{file}:{G.norm}")
                for linenum, line in results:
                    print(f"{linenum:6d}:  {line}")
            else:
                # Just print the file name
                print(f"{file}")

if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    for p in [P(i) for i in files]:
        FileSearch(p) if p.is_file() else DirSearch(p)
