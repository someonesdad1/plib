'''
Reverse the lines in a file
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
    # Reverse the lines in a file
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] file1 [file2...]
      Reverse the line order of one or more files and print them to stdout.
      Use "-" to read from stdin.
    Options:
      -c    Reverse the characters on each line
      -o    Don't reverse the line order
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-c"] = False     # Reverse characters on each line
    d["-o"] = False     # Don't reverse line order
    try:
        opts, args = getopt.getopt(sys.argv[1:], "cho")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in "co":
            d[o] = not d[o]
        elif o in ("-h",):
            Usage(0)
    if not args:
        Usage()
    return args
def Rev(line):
    return ''.join(list(reversed(line)))
def GetData(files):
    r = lambda x: Rev(x) if d["-c"] else x
    f = lambda x: [r(i.rstrip("\n")) for i in x]
    lines = []
    for file in files:
        if file == "-":
            lines +=  f(sys.stdin.readlines())
        else:
            lines += f(open(file).readlines())
    return lines
if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    lines = GetData(args)
    f = lambda x: x if d["-o"] else reversed(x)
    for line in f(lines):
        print(line)
