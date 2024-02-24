'''
Script to aid the j() shell function in getting the required directory.
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Script aid for the j() shell function
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard imports
        import getopt
        import os
        import pathlib
        import sys
        from collections import deque
        from pdb import set_trace as xx
    # Custom imports
        from wrap import dedent
        from color import TRM as t
        from edit import Edit
    # Global variables
        P = pathlib.Path
        ii = isinstance
        t.c = t("lilb")
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] cmd arg
        Commands (cmd):
        e       Edit config file
        [n]     Get line number n (0-based numbers)
        p d     Push directory d onto top of stack
        l       List config file's contents
        Defaults to {d["number"]}.
    Options:
        -c f    Specify the config file.  [{d["-c"]}]
        -d      Debug print the config file after reading it
        -h      Print a manpage
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-c"] = P("/home/don/.curdir")
    d["-d"] = False
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
def DumpConfigFile(start=None, end=None):
    'start and end can be colorizing strings'
    if start is not None:
        print(start, end="")
    if lines:
        print("Config file lines:")
        for i, line in enumerate(lines):
            print(f"  {i}:  {line}")
    else:
        print("** No data in config file **")
    if end is not None:
        print(end, end="")
def GetLines():
    'Return a deque of the lines in the config file, ignoring blank lines'
    keep = deque()
    lines = deque(open(d["-c"]).read().strip().split("\n"))
    while lines:
        line = lines.popleft()
        if line:
            keep.append(line)
    if d["-d"]:
        DumpConfigFile(start=t.c, end=t.n)
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
    if cmd == "e":      # Edit config file
        Edit(d["-c"])
    elif cmd == "g":    # Show line n (0-based)
        n = int(arg)
        if n < 0:
            n = 0
        if n >= len(lines):
            Error(f"Line number '{n}' out of range")
        print(lines[n])
    elif cmd == "p":    # Push the arg into the directory stack
        if len(args) == 1:
            Error("Need a directory")
        dir, p = arg, P(arg)
        if not p.exists():
            Error("'{p}' doesn't exist")
        lines.insert(0, str(p.resolve()))
        open(d["-c"], "w").write('\n'.join(lines))
    elif cmd == "l":    # List the config file
        for i, line in enumerate(lines):
            t.print(f"  {t.c}{i}:  {line}")
    elif cmd == "h":    # Help
        print(dedent(f'''
        e       Edit the config file
        g n     Go to line n (n is an integer >= 0)
        p d     Push the directory d onto the stack
        l       List the config file
        '''))
    else:
        s = "\n"
        msg = f"{s}  Command line: {sys.argv}{s}  Unrecognized command"
        Error(msg)
