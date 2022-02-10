'''
Make a default .gitignore file in the current directory if one doesn't
exist.
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
    # Program description string
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Standard imports
    import getopt
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    # Default .gitignore content
    data = dedent(f'''
        *.swo
        *.swp
        *.pdf
        *.ps
        *.bak
        *.orig

        .local_profile
        .vi
        .z
        a
        a.py
        aa
        b
        bb
        z
    ''')
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] dir1 [dir2 ...]
          Make a default .gitignore directory in the indicated directories if 
          it doesn't exist.
        Options:
            -f      Force overwriting an existing .gitignore file
            -m      For Mercurial:  write a .hgignore
            -n f    Name the file f instead of .gitignore
            -o      Write contents to stdout
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-f"] = False     # Force an overwrite
        d["-m"] = False     # For Mercurial:  write .hgignore
        d["-n"] = None      # Change the filename
        d["-o"] = False     # Write contents to stdout
        try:
            opts, dirs = getopt.getopt(sys.argv[1:], "fmn:o")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("fmo"):
                d[o] = not d[o]
            elif o in ("-n",):
                d["-n"] = a
        if not dirs:
            Usage()
        return dirs
if 1:   # Core functionality
    def ProcessDirectory(dir):
        msg = lambda action, dest: print(f"Couldn't {action} '{dest}'",
                                   file=sys.stderr)
        if d["-n"] is not None:
            file = d["-n"]
        else:
            file = ".hgignore" if d["-m"] else ".gitignore"
        # Change to the directory
        try:
            os.chdir(dir)
        except Exception:
            msg("chdir to", str(dir))
            os.chdir(cwd)
            return
        # Ensure the file isn't present
        p = P(file)
        if not d["-f"] and p.exists():
            msg("overwrite (-f needed)", str(p.resolve()))
        # Write the file
        try:
            open(file, "w").write(data)
        except Exception as e:
            msg("write to", str(p.resolve()))
            return
        # Go back to starting directory
        os.chdir(cwd)

if __name__ == "__main__":
    d = {}      # Options dictionary
    dirs = ParseCommandLine(d)
    cwd = P(os.getcwd())
    for dir in dirs:
        ProcessDirectory(P(dir))
