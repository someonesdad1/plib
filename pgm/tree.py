'''
Print a directory tree
    The original idea came from a script in the original "UNIX Power Tools"
    book published by O'Reilly.

    5 May 2022 redesign
        - Options
            - Bug:  -l option doesn't work
            - -a option to show files
            - -h to include hidden directories
            - -H to only show hidden directories
            - -v to include VC directories
            - -V to only show VC directories
            - -c for compact file display
            - -L to follow soft links
            - -d n  Tree depth limit
            - -s Include size of each file
            - -p glob only show these files, can have more than one
            - -x glob exclude these files
        - Use modern color.py
            - Directories are red
            - Color files same as LS_COLORS
            - Resolve soft links
            - For directory listing, put size in MB in green and num files
              in yellow
            - Consider using attributes
                - Exponents for size numbers to make them less obtrusive
                    - Use 1 to 3 digits with SI prefix
                - Rapid blink for large directories (threshold with -t, 1
                  GB default)
                - Use resistor color code for multiplier and give 1 sig
                  figure for the size
                    - brn:1, red:2, orn:3, yel:4, grn:5, blu:6, vio:7,
                      gry:8, wht:9 and above.  Instead of gry and wht,
                      could use cyn and mag.
        - Use Unicode box drawing characters:

            │   │   └── gnome-applications.menu
            │   ├── systemd
            │   │   └── user -> ../../systemd/user
            │   ├── user-dirs.conf
            │   ├─
            Others:  ┋ ┇ ┃ ━ ┗ 

            - Consider making each of the vertical columns of | characters
              different colors to make it easier to trace them
        - Include count of directories and files
 
    TODO:
        - Change colors:  yellow is > 10 MB, lcyan > 100 MB, lred > 1 GB,

        - In section 3.2.1 of the book https://waf.io/book/, after "The
          execution output will be", the output shows a 'tree -a' command.
          This shows both directories and files.  This script should color
          the directory names and show the files when the -a option is
          used.  Special files can be colored like I do with ls:  lyel for
          C/C++, lcyn for python, etc.

'''
if 1:  # Header
    # Copyright, license
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
    # Imports
        from pathlib import Path as P
        import getopt
        import math
        import os
        import sys
        from pdb import set_trace as xx 
    # Custom imports
        from wrap import dedent
        from dppath import IsVCDir
        if 0:
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
        else:
            from color import TRM as t
    # Global variables
        ii = isinstance
if 1:   # Utility
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
if 1:   # Core functionality
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
    def GetFileSize(file):
        assert(ii(file, P))
    def GetDirSize(dir):
        'Return size of files in bytes'
        assert(ii(dir, P))
        size = 0
        for item in os.scandir(dir):
            size += os.path.getsize(item)
        return size
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
                    sz = GetDirSize(p)
                    Tree.size += sz if sz else 0
                    if sz:
                        # Color the size number
                        z = f"\t\t{sz}" if sz else ""
                        z = ShortSize(sz)
                        u = f"{'|   '*depth}"
                        out.append(f"{u}{t('ornl')}{p.name}{t.n} {t('yell', attr='sp')}{z}{t.n}")
                    else:
                        out.append(f"{u}{t('ornl')}{p.name}")
        return out
    def ShortSize(b):
        '''b is number of bytes.  Return a shortened version with an SI
        prefix as a suffix.
        '''
        assert(ii(b, int) and b >= 0)
        if not b:
            return "0"
        characteristic = int(math.log10(b))
        n, rem = divmod(characteristic, 3)
        ltr = {0:"", 1:"k", 2:"M", 3:"G", 4:"T", 5:"P", 6:"E",
               7:"Z", 8:"Y"}[n]
        s = f"{b:.6e}" 
        digits = s.split("e")[0]
        u = round(float(digits), rem)
        v = str(u).replace(".", "")
        return v[:rem + 1] + ltr

if 0:   # Test area
    b = 19478
    print(ShortSize(b))
    exit()
if 0:   # Test area
    # Demo getting size and printing exponents
    t.d = t("lip")
    t.e = t(None, None, "sp")
    t.s = t(None, None, "sb")
    print(f"{t.d}circular_imports{t.n}{t.e}23k{t.n}/{t.s}67{t.n}")
    exit()

if __name__ == "__main__":
    d = {}   # Options dictionary
    dirs = [P(i) for i in ParseCommandLine()]
    for dir in dirs:
        for dir in Tree(dir):
            print(dir)
        print(f"Size of files in above tree = {Tree.size} MB")
