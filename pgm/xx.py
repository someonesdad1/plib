'''
Utility to find ∞∞'s in files.  I use '∞∞' to flag temporary code or
bugs that need to be fixed.
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Find files with '∞∞' strings to indicate To Do items
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        import sys
        import os
        import getopt
        import pathlib
        import re
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        from columnize import Columnize
    if 1:   # Global variables
        class G:
            pass
        g = G()
        P = pathlib.Path
        ii = isinstance
        # Color highlighting
        t.file = t.yel
        # There are some files that can be ignored:
        g.files_to_ignore = set(
            (
                "word_syllables.py",
                "words.py",
                "words",
                "asciify_make.py",
                "xx.py",
                "bama.py",
            )
        )
        # File globbing expressions for the default files to search
        g.source = list(
            sorted(
                '''
                
                *.bas *.c *.cpp *.cxx *.f *.f90 *.h *.hxx *.ino *.java *.pro
                *.py ?akefile *.awk *.sh *.bash
                
            '''.split()
            )
        )
        if 0:
            # This is the string we'll search for
            g.s = r"\b∞∞\b"
            # Regular expression to find '∞∞'.
            g.r = re.compile(g.s)
            # Regular expression to find '∞∞' in string with newlines.  This is
            # quickly used to scan a whole file.
            g.R = re.compile(g.s, re.M)
if 1:  # Utility
    def Usage(status=1):
        name = sys.argv[0]
        print(
            dedent(
                f'''
        Usage:  {name} [item1 [item2 ...]]
          Searches files or directories given on the command line for the string
          {d["-x"]!r} and prints out the name of those that contain it.  If the item is
          a directory, typical source files are printed if they contain {d["-x"]!r}.
        Options:
          -n    Print the line number and line where {d["-x"]!r} occurs
          -r    Recursively descend directories
          -s    Print source code file extensions examined
          -x x  Set the trigger string to look for [{d["-x"]!r}]
        '''[1:-1]
            )
        )
        exit(status)
    def ParseCommandLine(d):
        d["-n"] = False  # Print line number & line
        d["-r"] = False  # Recursive for directories
        d["-s"] = False  # Print list of regexps used
        d["-x"] = "∞∞"   # String to search for
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
                d[o] = a
            if o == "-h":
                Usage()
        if d["-s"]:
            print("List of type of source code files searched:")
            for i in Columnize(g.source, indent=" " * 2):
                print(i)
            exit(0)
        if d["-x"]:
            g.s = rf"\b{d['-x']}\b"
            g.s = rf"{d['-x']}"
            g.r = re.compile(g.s)
            g.R = re.compile(g.s, re.M)
        if not files:
            Usage()
        return files
if 1:  # Core functionality
    def Ignore(line):
        '''Return True if this line should be ignored.'''
        line = line.strip()
        if line.find("from pdb import set_trace as xx") != -1:
            return True
        elif line.find("xxrmxx") != -1 or line.find("xxmrxx") != -1:
            return True
        elif line.find("xx()") != -1:
            return True
        return False
    def SearchFile(file, dir, d):
        "Search the given file for d['-x']"
        assert ii(file, P)
        if str(file) in g.files_to_ignore:
            return
        s = open(file).read()
        # Parse into lines and search each line.  If a match is found,
        # print out the line number and line.
        lines, results = s.split("\n"), []
        for i, line in enumerate(lines):
            if Ignore(line):
                continue
            mo = g.r.search(line)
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
        assert ii(dir, P) and dir.is_dir()
        glb = dir.rglob if d["-r"] else dir.glob
        for glob_pattern in g.source:
            for file in glb(glob_pattern):
                if file.is_dir():
                    continue
                FileSearch(file)
    def FileSearch(file):
        assert ii(file, P) and file.is_file()
        if file.name in g.files_to_ignore:
            return
        s = file.read_text()
        # See if it's in the file at all
        if not g.R.search(s):
            return
        # Search each line
        results = []
        for i, line in enumerate(s.split("\n")):
            if Ignore(line):
                continue
            mo = g.r.search(line)
            if mo:
                results.append((i + 1, line))
        if results:
            if d["-n"]:
                print(f"{t.file}{file}:{t.n}")
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
