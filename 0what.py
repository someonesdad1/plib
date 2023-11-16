'''
Show the what strings for python scripts
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <utility> Show the 'what' strings for python scripts.  These are
    # the strings in each script describing the purpose of the script.
    #∞what∞#
    #∞test∞# ignore #∞test∞#
    pass
if 1:   # Imports
    # Standard library modules
    from collections import deque, defaultdict, namedtuple
    import getopt
    import os
    import pathlib
    import re
    import subprocess
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    import trigger
    from wrap import wrap, dedent, indent, Wrap
    from lwtest import run, raises, assert_equal, Assert
    from color import TRM as t
    from columnize import Columnize
if 1:   # Global variables
    P = pathlib.Path
    rcat = re.compile(r"<(.*?)>")  # Find category strings
    categories = set()
    EntryType = namedtuple("EntryType", "p what category")
    t.sep = t("yell")
    t.py = t("grn")
    # Generate escape codes even if stdout isn't a TTY
    t.always = True
if 1:   # Utility
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        name = sys.argv[0]
        print(dedent(f'''
        Usage:  {name} [options] [files...]
          Show the 'what' trigger string for each python file.  A command line
          argument can also be a directory, in which case all python files in
          that directory are queried.
        Options:
          -c    Show categories
          -d    Show debug output
          -m    Show files missing a category
          -r    Act recursively
          -s    Ignore category and sort by filename
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = False             # Show categories
        d["-d"] = False             # Show debug output
        d["-m"] = False             # Show missing categories
        d["-r"] = False             # Act recursively
        d["-s"] = False             # Sort by filename
        try:
            opts, args = getopt.getopt(sys.argv[1:], "cdhmrs")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cdmrs"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(d, status=0)
        if not args:
            Usage(d)
        return args
if 1:   # Core functionality
    def FormatWhat(what, indent=" "*2):
        '''Return (what, category) where what is the wrapped string
        without '#' leaders and category is the category string or None.
        '''
        s = what.strip() 
        lines = s.split("\n")
        # Remove beginning '#'
        o = deque()
        for line in lines:
            line = line.strip()
            if line and line[0] == "#":
                line = line[1:].strip()
            o.append(line)
        s = ' '.join(o)
        # Remove category string if present
        mo = rcat.search(s)
        category = mo.groups()[0] if mo else None
        if category is not None:
            categories.add(category)
        s = rcat.sub("", s).strip()
        return (s, category)
    def ProcessFile(file):
        '''Return (file, ts, category) where ts is the trigger string
        for 'what'.  If there is no trigger string, ts is None.  If
        there was a category in the trigger string, it is returned in
        the string category or is None.
        '''
        if not hasattr(ProcessFile, "tr"):
            ProcessFile.tr = trigger.Trigger()
        di = ProcessFile.tr
        try:
            di(file)
        except Exception:
            return None
        if "what" in di:
            what, category = FormatWhat(di["what"])
            return EntryType(file, what, category)
        else:
            return None
    def GetDirectoryFiles(dir):
        glb = dir.rglob if d["-r"] else dir.glob
        files = []
        for file in glb("*.py"):
            data = ProcessFile(file)
            if data is not None:
                files.append(data)
        return files
    def DumpFiles(seq):
        for file in seq:
            f, tr, cat = file
            n = 35
            if tr is not None:
                s = (f"{C.fg(C.lgreen, s=1)}{cat}{C.normal(s=1)}" if cat
                     is not None else "")
                print(f"{f!s:20s} {tr[:n]:<{n}s}      {s}")
        print("Categories:")
        for i in sorted(categories):
            print(f"  {i.capitalize()}")
    def GetFiles(args):
        '''Return a sequence of files from the files/directories given on
        the command line.  args is a sequence of file or directory names
        The returned sequence will be of the form:
            (filename, what_string)
        where filename is a pathlib.Path object and what_string is the
        what string for that file or None if there wasn't a what string.
        '''
        files = []
        for item in args:
            p = P(item)
            if p.is_dir():
                files.extend(GetDirectoryFiles(p))
            elif p.is_file():
                data = ProcessFile(p)
                if data is not None:
                    files.append(data)
            else:
                raise TypeError(f"'{p}' is not a file or directory")
        tu = tuple(sorted(files))
        if d["-d"]:
            DumpFiles(tu)
        return tu
    def ReportByCategory(files):
        def Header(s):
            width = int(os.environ.get("COLUMNS", 79)) - 5
            h = "-"*((width - len(s) - 1)//2)
            return f"{t.sep}{h} {s.capitalize()} {h}{t.n}"
        di = defaultdict(list)
        for item in files:
            di[item.category] += [item]
        wrap.i = " "*4
        for key in sorted(categories):
            print(Header(key))
            for item in di[key]:
                p = item.p
                print(f"{t.py}{p!s}{t.n}")
                print(wrap(item.what))
    def ShowMissingCategory(files):
        missing = []
        for item in files:
            if item.category is None:
                missing.append(str(item.p))
        if missing:
            print("Files missing a category:")
            for line in Columnize(sorted(missing), indent=" "*4):
                print(line)
    def ShowCategories(files):
        categories = []
        for item in files:
            if item.category is not None:
                categories.append(item.category)
        categories = set(categories)
        print("List of categories:")
        for line in Columnize(sorted(categories), indent=" "*4):
            print(line)
if __name__ == "__main__": 
    d = {}      # Options dictionary
    import color as C
    args = ParseCommandLine(d)
    files = GetFiles(args)
    if d["-m"]:
        ShowMissingCategory(files)
    elif d["-c"]:
        ShowCategories(files)
    else:
        ReportByCategory(files)
