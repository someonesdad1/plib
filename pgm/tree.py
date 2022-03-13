'''
Print a directory tree
    The original idea came from a script in the original "UNIX Power Tools"
    book published by O'Reilly.
 
    TODO:
        - Change colors:  yellow is > 10 MB, lcyan > 100 MB, lred > 1 GB,

        - In section 3.2.1 of the book https://waf.io/book/, after "The
          execution output will be", the output shows a 'tree -a' command.
          This shows both directories and files.  This script should color
          the directory names and show the files when the -a option is
          used.  Special files can be colored like I do with ls:  lyel for
          C/C++, lcyn for python, etc.

'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2005 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Print a directory tree
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    from pathlib import Path as P
    import getopt
    import os
    import sys
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
    from dppath import IsVCDir
    try:
        import color as Co
        _have_color = True
    except ImportError:
        # Make a dummy color object to swallow function calls
        class Dummy:
            def fg(self, *p, **kw): pass
            def normal(self, *p, **kw): pass
            def __getattr__(self, name): pass
        Co = Dummy()
        _have_color = False
def Usage(status=1):
    name = sys.argv[0]
    char = d["-l"]
    size = d["-t"]
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] dir1 [dir2...]
      Print a directory tree for each directory given on the command line.
      The colored numbers after the directory name are the size of the files
      in that directory in MB.
    Options:
      -l x    Indentation string for level.  [{d["-l"]!r}]
              On a dense listing, '|' can help your eye with alignment
      -d n    Limit tree depth to n (default is to show all of tree)
      -t n    Don't print dir size if < n MB  [{d["-t"]} MB]
      -v      Include version control directories (they are ignored by default)
    '''))
    exit(status)
def ParseCommandLine():
    d["-d"] = 0         # Depth limit
    d["-l"] = "|   "    # Indentation string
    d["-t"] = 1         # Threshold in MB for printing size
    d["-v"] = False     # Include version control directories
    if len(sys.argv) < 2:
        Usage()
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "d:hl:vt:")
    except getopt.GetoptError as msg:
        print(msg)
        exit(1)
    for o, a in optlist:
        if o == "-d":
            d["-d"] = int(a)
        elif o == "-h":
            Usage(0)
        elif o == "-l":
            d["-l"] = a
        elif o == "-t":
            try:
                d["-t"] = float(a)
            except ValueError:
                print(f"'{a}' is not a valid floating point number",
                      file=sys.stderr)
                exit(1)
        elif o == "-v":
            d["-v"] = True
    if not len(args):
        Usage()
    return args
if 0:
    def IsVCDir(dir):
        'Return True if dir is in a version control directory tree'
        if d["-v"]:
            return False
        if not hasattr(IsVCDir, "vc"):
            IsVCDir.vc = set((".bzr", ".git", ".hg", ".svn", "RCS"))
        for i in dir.parts:
            if i in IsVCDir.vc:
                return True
        return False
def GetSize(dir):
    'Return size of files in MB'
    size = 0
    for item in os.scandir(dir):
        size += os.path.getsize(item)
    size = int(size/1e6)
    return size if size >= d["-t"] else None
def Tree(dir):
    Tree.size = 0
    out, limit = [str(dir)], d["-d"]
    for p in sorted(dir.rglob("*")):
        if p.is_dir():
            if IsVCDir(p) and not d["-v"]:
                # It's a version control directory; ignore unless -v was set
                continue
            depth = len(p.relative_to(dir).parts)
            if not limit or (limit and depth <= limit):
                sz = GetSize(p)
                Tree.size += sz if sz else 0
                if sz:
                    # Color the size number
                    t = f"\t\t{sz}" if sz else ""
                    c = Co.fg(Co.lgreen, s=True)
                    n = Co.normal(s=True)
                    out.append(f"{'|   '*depth + p.name}{c}{t}{n}")
                else:
                    out.append(f"{'|   '*depth + p.name}")
    return out
if __name__ == "__main__":
    d = {}   # Options dictionary
    dirs = [P(i) for i in ParseCommandLine()]
    for dir in dirs:
        for dir in Tree(dir):
            print(dir)
        print(f"Size of files in above tree = {Tree.size} MB")
