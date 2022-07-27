'''

- Need a tool for git that lists files like lsh
    - Key states:  clean, modified (staged, not stages), ignored, not
      tracked, deleted, added but not checked in 
    - Color codes the states
    - Default report shows staged, not staged in current directory
        - Need -r to see at and below current directory
    - Branch and root of repository always shown at end
- Options

    - -a    Show all
    - -i    Show ignored
    - -c    Show unchanged but tracked
    - -r    Recursive
    - -w    Show whole repository state

- Also use output of 'git shortlog -sn' for repository names
- Primary use cases
    - Show the untracked files
    - Show directories that have no repository files (one of the
        easiest ways to do this is to put a .git directory in that
        directory; this also makes it trivial to find that it's not
        part of the parent repository).
    - Short listing of types:  M (modified), T (type changed), A
        (added), D (deleted), R (renamed), C (copied), U (updated but
        unmerged)
        - XY table:  M in X position means modified and staged for
            commit (in index); in Y means changed and not in index
- Root location of repository shown (must be in a subdirectory of
    the directory holding the repository .git directory)
- 'git status -u --porcelain' shows untracked files and directories
- 'git status --ignored --porcelain' shows ignored stuff
- Use --branch to get current branch headers in porcelain format 2
- Color code the different states
    - red:   deleted
    - orn:   untracked
    - grn:   tracked, unchanged
    - mag:   tracked, changed
    - gryl:  ignored

Script to list status of git repository's files

'''
if 1:   # Header
    # Copyright, license
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
    # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from pdb import set_trace as xx
    # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
    # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        return args
if 1:   # Core functionality
    pass

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
