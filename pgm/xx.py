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
        from collections import defaultdict
        import sys
        import os
        import getopt
        import pathlib
        import re
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        from columnize import Columnize
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
    if 1:   # Global variables
        class G:
            pass
        g = G()
        P = pathlib.Path
        ii = isinstance
        # There are some files that can be ignored:
        g.files_to_ignore = set((
                "word_syllables.py",
                "words.py",
                "words",
                "asciify_make.py",
                "xx.py",
                "bama.py",
            ))
        # File globbing expressions for the default files to search
        g.source = list(sorted(''' *.bas *.c *.cpp *.cxx *.f *.f90 *.h *.hxx *.ino
            *.java *.pro *.py ?akefile *.awk *.sh *.bash '''.split()))
if 1:  # Classes
    class Search:
        'Encapsulates the search results by file'
        def __init__(self, file):
            self.file = file
            self.lines = []
        def add(self, item):
            self.lines.append(item)
        def __str__(self):
            return f"Search<{self.file!s}>"
        def __repr__(self):
            return str(self)
if 1:  # Utility
    def Manpage():
        print(dedent(f'''
        As of 20 Jan 2026, my current marker policies are:
            '∞∞' is the default marker string
            '∞∞1' is a high priority task
            '∞∞2' is a medium priority task
            '∞∞3' is a low priority task

        Use -p to get a summary list of the files by the marker priority

        When working on a specific project, I'll use a marker with a suffix letter like
        '∞∞q' to mark a number of locations of specific files.  These should be
        considered temporary.

        However, long-term markers can be made with various strings.  For example, a
        future envisioned project named 'alpha' could have the marker '∞∞alpha'.
        '''))
        exit()
    def Usage(status=1):
        name = sys.argv[0]
        print(dedent(f'''
        Usage:  {name} [item1 [item2 ...]]
          Searches files or directories given on the command line for the marker string
          and prints out the lines of those that contain it.  If the item is a directory,
          typical source files are searched (use -s to see the source file types).
        Defaults for the marker string d["-x"]:
          ∞∞ is the default marker string.  Use -u to set a modifying suffix string.
          For example, priority markers could use the 1, 2, 3 suffixes.
        Options:
          -h    Show my current policies for my source files
          -L    Same as -l except print all on one line
          -l    Only print the file name if it contains the marker string
          -n    Include the line number
          -p    Print summary report of prioritized files
          -r    Recursively descend directories
          -s    Print source code file extensions examined
          -u s  Suffix string for the marker string
          -x x  Set the marker string to look for [{d["-x"]!r}]
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-L"] = False  # Only print file name if marker string is found, no newline
        d["-l"] = False  # Only print file name if marker string is found
        d["-n"] = False  # Print line number & line
        d["-p"] = False  # Print summary report of prioritized files
        d["-r"] = False  # Recursive for directories
        d["-s"] = False  # Print list of regexps used
        d["-u"] = 0      # Priority number
        d["-x"] = "∞∞"   # String to search for
        try:
            optlist, files = getopt.getopt(sys.argv[1:], "hLlnprsu:x:")
        except getopt.GetoptError as mystr:
            msg, option = mystr
            print(msg)
            sys.exit(1)
        for o, a in optlist:
            if o[1] in "Llnprs":
                d[o] = not d[o]
            if o == "-x":
                d[o] = a
            if o == "-u":
                d[o] = int(a)
            if o == "-h":
                Manpage()
        if d["-s"]:
            print("List of type of source code files searched:")
            for i in Columnize(g.source, indent=" " * 2):
                print(i)
            exit(0)
        if d["-u"]:
            s, priority = d["-x"], d["-u"]
            if 1 <= priority <= 3:
                d["-x"] = s + str(priority)
            else:
                Error("-u option must be 1, 2, or 3")
        if d["-x"]:
            g.s = rf"\b{d['-x']}\b"
            g.s = rf"{d['-x']}"
            g.r = re.compile(g.s)
            g.R = re.compile(g.s, re.M)
        if not files:
            Usage()
        GetColors()
        g.results = []  # This is used for -p option
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
    def GetColors():
        # Color highlighting
        t.file = t.yel      # -n file name
        t.name = t.gry      # Inline file name
        t.colon = t.redl
        t.ln = t.purl    # Line number
    def DirSearch(dir):
        assert ii(dir, P) and dir.is_dir()
        glb = dir.rglob if d["-r"] else dir.glob
        for glob_pattern in g.source:
            for file in glb(glob_pattern):
                if file.is_dir():
                    continue
                FileSearch(file, names=True)
    def FileSearch(file, names=False):
        assert ii(file, P) and file.is_file()
        if file.name in g.files_to_ignore:
            return
        s = file.read_text()
        # See if it's in the file at all
        if not g.R.search(s):
            return
        # Search each line
        results = []
        srch = Search(file)
        for i, line in enumerate(s.split("\n")):
            if Ignore(line):
                continue
            mo = g.r.search(line)
            if mo:
                srch.add((i + 1, line))     # Save it in the class for -p
                results.append((i + 1, line))
        if d["-p"]:
            g.results.append(srch)
        elif results:
            if d["-n"]:     # Number the lines
                t.print(f"{t.file}{file}{t.colon}:")
                for linenum, line in results:
                    print(f"  {t.ln}{linenum}{t.colon}:{t.n}{line}")
            elif d["-l"] or d["-L"]:
                # Just print the file name
                print(f"{file}", end=" " if d["-L"] else "\n")
            else:
                # Print each line
                name = f"{t.name}{file}{t.colon}:{t.n}" if names else ""
                for linenum, line in results:
                    print(f"{name}{line}")
    def PriorityReport():
        '''g.results contains the searched results.  Print out the files by their 
        priority.
        '''
        # Construct a dictionary of priority numbers with the files as values
        di = defaultdict(list)
        for srch in g.results:
            file = srch.file
            for ln, line in srch.lines:
                loc = line.find(d["-x"])
                if loc == -1:
                    t.print(f"{t.redl}Bug in PriorityReport:  {d['-x']!r} not in line:\n {line!r}")
                    breakpoint() 
                remainder = line[loc + len(d["-x"]):]
                if not remainder:
                    continue    # No integer
                # Priority is integer just past the marker string
                try:
                    priority = int(remainder[0])
                except Exception:
                    continue
                di[priority].append(str(file))
        # Print report
        c = {1: t.ornl, 2: t.sky, 3: t.gry}
        for i in sorted(di):
            if di[i]:
                print(f"{c[i]}Priority {i}")
                for j in Columnize(sorted(set(di[i])), indent=" "*2):
                    print(j)
                t.print(end="")
        exit() # ∞∞

if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    show_names = len(files) > 1
    for p in [P(i) for i in files]:
        FileSearch(p, names=show_names) if p.is_file() else DirSearch(p)
    if d["-L"] and files:
        print()
    if d["-p"]:
        PriorityReport()
