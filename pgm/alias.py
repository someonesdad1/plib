'''
Show current shell aliases.  Assumes stdin contains list of 'alias' commands.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Print shell aliases
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Standard imports
    import getopt
    import pathlib
    import sys
    import os
    from pdb import set_trace as xx
    if 1:
        import debug
        debug.SetDebugger()
if 1:   # Custom imports
    from columnize import Columnize
    from wrap import dedent
    from color import C
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [a1 [a2...]]
          Show shell aliases.  Output is in columns unless -d is used.  If any
          aliases are given on the command line, their definitions are printed.
        Options:
            -d      Include definitions
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False     # Include definitions
        try:
            opts, names = getopt.getopt(sys.argv[1:], "dh")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("d"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        return names
if 1:   # Core functionality
    def GetAliasNames():
        '''Read stdin; lines are of the form
            alias vimrc='$EDITOR ~/.vimrc'
        so parse out the pieces.
        '''
        aliases = {}
        if 0:
            lines = open("a").readlines()
        else:
            lines = sys.stdin.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            line = line[6:] # Get rid of leading 'alias '
            loc = line.find("=")
            key, value = line[:loc], line[loc:]
            aliases[key] = value
        return aliases
    def ShowList(a):
        names = sorted(a.keys())
        for i in Columnize(names):
            print(i)

if __name__ == "__main__":
    d = {}      # Options dictionary
    names = ParseCommandLine(d)
    alias_dict = GetAliasNames()
    if names:
        for name in names:
            if name in alias_dict:
                val = alias_dict[name][1:].strip("'")
                print(f"{name} = {C.lgrn}{val}{C.norm}")
            else:
                print(f"'{name}' not found")
    else:
        ShowList(alias_dict)
