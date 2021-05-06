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
        d["-a"] = False
        d["-d"] = 3         # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h")
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
                Usage(d, status=0)
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
if 1:   # Core functions
    def Details():
        pass
    def Report():
        plib = set([i.name for i in P("/plib").glob("*.py")])
        pylib = set([i.name for i in P("/pylib").glob("*.py")])
        common = plib & pylib
        if not common:
            m = f"No common files ({len(plib)} in plib, {len(pylib)} in pylib"
            print(m)
        print("Common: ", common)

if __name__ == "__main__":
    d = {}      # Options dictionary
    dispatch = {
        "report": Report,
        "details": Details,
    }
    args = ParseCommandLine(d)
    cmd = GetCommand(args[0])
    dispatch[cmd]()
