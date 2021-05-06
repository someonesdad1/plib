'''
Identify file differences between /plib and /pylib.
'''
 
# Copyright (C) 2021 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Academic Free License version 3.0.
# See http://opensource.org/licenses/AFL-3.0.
#

if 1:   # Standard modules
    import getopt
    import os
    import pathlib
    import sys
if 1:   # Custom modules
    from cmddecode import CommandDecode
    from wrap import dedent
    # Debugging stuff
    from pdb import set_trace as xx
    if 0:
        import debug
        debug.SetDebugger()  # Start debugger on unhandled exception
if 1:   # Global variables
    commands = "report details".split()
    P = pathlib.Path
if 1:  # Utility
    def eprint(*p, **kw):
        'Print to stderr'
        print(*p, **kw, file=sys.stderr)
    def Error(msg, status=1):
        eprint(msg)
        exit(status)
    def Usage(d, status=1):
        name = sys.argv[0]
        print(dedent(f'''
        Usage:  {name} [options] cmd
          Analyze differences between /plib and /pylib.  cmd:
            report             Show summary report
            details files...   Explain how they differ
        Options:
          -h  Print a manpage.
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

if __name__ == "__main__":
    d = {}      # Options dictionary
    dispatch = {
        "report": Report,
        "details": Details,
        "missing": Missing,
    }
    args = ParseCommandLine(d)
    cmd = GetCommand(args[0])
    dispatch[cmd]()
