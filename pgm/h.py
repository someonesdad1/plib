'''
Script to aid the H() shell function in getting the required directory.
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
    # Script aid for the H() shell function.
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Standard imports
    import getopt
    import os
    import pathlib
    import sys
    from collections import deque
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
    from color import C
    from edit import Edit
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    class g: pass
    g.c = C.lcyn
    g.n = C.norm
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] cmd arg
          Commands (cmd):
            e       Edit config file
            g [n]   Get line number n (n defaults to 0) (0-based numbers)
            p d     Push directory d onto top of stack
            P       Print config file's contents
          Defaults to {d["number"]}.
        Options:
          -c f    Specify the config file.  [{d["-c"]}]
          -d      Debug print the config file after reading it
          -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = P("/home/Don/.curdir")
        d["-d"] = False
        d["-e"] = False
        d["number"] = 1
        try:
            opts, args = getopt.getopt(sys.argv[1:], "c:deh")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("de"):
                d[o] = not d[o]
            elif o in ("-c",):
                d["-c"] = f = P(a)
                if not f.exists() or not f.is_file():
                    print("'{d['-c']}' doesn't exist")
            elif o in ("-h", "--help"):
                Usage(status=0)
        if not args:
            Usage()
        return args
def GetLines():
    'Return a deque of the lines in the config file, ignoring blank lines'
    keep = deque()
    lines = deque(open(d["-c"]).read().strip().split("\n"))
    while lines:
        line = lines.pop()
        if line:
            keep.append(line)
    if d["-d"]:
        if keep:
            print(f"{g.c}Config file lines:")
            for i, line in enumerate(keep):
                print(f"  {i}:  {line}")
            print(f"{g.n}")
        else:
            print(f"{g.c}No data in config file{g.n}")
    return keep
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    cmd = args[0]
    arg = args[1] if len(args) > 1 else ""
    lines = GetLines()
    if not lines and cmd != "p":
        print(f"Config file '{d['-c']}' is empty")
        exit(1)
    if cmd == "e":
        Edit(d["-c"])
    elif cmd == "g":
        n = int(arg)
        if n < 0:
            n = 0
        if n > len(lines) - 1:
            raise ValueError(f"Line number '{n}' out of range")
        print(lines[n])
    elif cmd == "p":
        if len(args) == 1:
            raise ValueError("Need a directory")
        dir, p = arg, P(arg)
        if not p.exists():
            raise ValueError("'{p}' doesn't exist")
        lines.insert(0, str(p.resolve()))
        open(d["-c"], "w").write('\n'.join(lines))
    elif cmd == "P":
        for line in lines:
            print(line)
    else:
        raise ValueError("Unrecognized command")
