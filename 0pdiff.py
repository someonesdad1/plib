'''
Identify file differences between /plib and /pylib.
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
    # <utility> Identify file differences between /plib and /pylib.  /pylib
    # was my old python directory for scripts I've written starting in
    # 1998.  There was over 1200 files in the /pylib directory tree, so I
    # had to do a lot of trimming (as of Mar 2022, it's down to 386 files.
    # Still too many.  :^)
    #∞what∞#
    #∞test∞# ignore #∞test∞#
    pass
if 1:   # Standard modules
    import getopt
    import os
    import pathlib
    import sys
if 1:   # Custom modules
    from cmddecode import CommandDecode
    from wrap import dedent
    from columnize import Columnize
    # Debugging stuff
    from pdb import set_trace as xx
    if 0:
        import debug
        debug.SetDebugger()  # Start debugger on unhandled exception
if 1:   # Global variables
    commands = "report details diff".split()
    P = pathlib.Path
if 1:   # Utility
    def eprint(*p, **kw):
        'Print to stderr'
        print(*p, **kw, file=sys.stderr)
    def Error(msg, status=1):
        eprint(msg)
        exit(status)
    def Usage(d, status=1):
        name = sys.argv[0]
        print(dedent(f'''
        Usage:  {name} [options] cmd [file1 ...]
          Analyze differences between /plib and /pylib.  cmd:
            diff               Show files in /plib that differ from /pylib
            report             Show summary report
            details files...   Explain how they differ
        Options:
          -a  Print a manpage.
        '''[1:-1]))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Show all
        try:
            opts, args = getopt.getopt(sys.argv[1:], "a")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
        if not args:
            Usage(d)
        return args
if 1:   # Core functionality
    def GetCommand(cmd):
        c = CommandDecode(commands)
        candidates = c(cmd)
        if len(candidates) == 1:
            return candidates[0]
        elif len(candidates) > 1:
            eprint(f"Ambiguous command:  {' '.join(candidates)}")
        else:
            eprint(f"Command '{cmd}' not recognized")
        exit(1)
    def GetFiles():
        'Return dictionaries keyed by file name (value is pathlib.Path)'
        pl = set(P("/plib").glob("*.py"))
        py = set(P("/pylib").glob("*.py"))
        plib, pylib = {}, {}
        for i in pl:
            plib[i.name] = i
        for i in py:
            pylib[i.name] = i
        return plib, pylib
if 1:   # Core functions
    def Details():
        pass
    def Missing():
        pass
    def Report():
        plib, pylib = GetFiles()
        common = set(plib) & set(pylib)
        if not common:
            m = f"No common files ({len(plib)} in plib, {len(pylib)} in pylib"
            print(m)
        print("Common: ", common)
    def Diff():
        plib, pylib = GetFiles()
        common = set(plib) & set(pylib)
        o = []
        for i in common:
            pl = plib[i].read_text()
            py = pylib[i].read_text()
            if pl != py:
                o.append(i)
        if o:
            print("Files that differ between /plib and /pylib:")
            for line in Columnize(o, indent="  "):
                print(line)
if __name__ == "__main__":
    d = {}      # Options dictionary
    dispatch = {
        "diff": Diff,
        "report": Report,
        "details": Details,
        "missing": Missing,
    }
    args = ParseCommandLine(d)
    cmd = GetCommand(args[0])
    dispatch[cmd]()
