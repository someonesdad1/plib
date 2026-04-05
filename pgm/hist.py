'''
Categorize output of bash history command (this script analyzes stdin)
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Summarize bash history
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Standard imports
    from collections import defaultdict
    import getopt
    import os
    import sys
if 1:  # Custom imports
    from columnize import Columnize
    from wrap import dedent
    from dputil import PP
    pp = PP()   # Get pprint with current screen width
    if 0:
        import debug
        debug.SetDebugger()  # Start debugger on unhandled exception
if 1:  # Global variables
    ii = isinstance
    class G:
        pass
    g = G()
    g.total = 0     # Count number of lines of input
    g.max_token_length = 25    # Maximum token length allowed
if 1:  # Utility
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def eprint(*p, **kw):
        "Print to stderr"
        print(*p, **kw, file=sys.stderr)
    def Error(msg, status=1):
        eprint(msg)
        exit(status)
    def Usage(d, status=0):
        name = sys.argv[0]
        print(dedent(f'''
        Usage:  {name} [options] [file]
          Summarizes the output of the bash history command.  Reads stdin if
          file is '-'.
        Options:
          -c    Include counts
          -n n  Limit report to top n items
    ''')
        )
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = False     # Include counts
        d["-n"] = None      # Limit to top n items
        if len(sys.argv) < 2:
            Usage(d, status=1)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "chn:")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in "c":
                d[o] = not d[o]
            elif o == "-h":
                Usage(d)
            elif o == "-n":
                try:
                    d["-n"] = abs(int(a))
                except Exception:
                    Error("{a!r} must be an integer")
        if len(args) > 1:
            Error("Put only one file on command line")
        GetScreen()
        return args[0]
if 1:  # Core functionality
    def Classify(lines):
        '''The command lines are processed to get the first command by splitting on
        whitespace, dropping the first field (which is the integer number of the
        command), then getting the first token.  Any token over 25 characters is
        ignored.
        '''
        rd = defaultdict(int)
        for line in lines:
            g.total += 1
            f = line.split()
            if len(f) < 2:
                continue
            f.pop(0)    # Get rid of history number
            cmd = f.pop(0)  # First token
            if len(cmd) > g.max_token_length:
                continue
            if cmd[0] == "#":
                continue
            if cmd.startswith("c;"):
                cmd = cmd[2:]
            # Now split on ';' and only keep first element
            cmd = cmd.split(";")[0]
            rd[cmd] += 1
        if 0:
            for i in Columnize(sorted(rd.keys())):
                print(i)
            exit()
        return rd
    def Report(rd, maxnum=None):
        items = list(reversed(sorted([(int(j), i) for i, j in rd.items()])))
        out = []
        if maxnum is None:
            m = max([len(cmd) for count, cmd in items])
        else:
            m = max([len(cmd) for count, cmd in items[:maxnum]])
            items = items[:maxnum]
        for count, cmd in items:
            if d["-c"]:
                out.append(f"{cmd:{m}s} {count:6d}")
            else:
                out.append(f"{cmd}")
        print("Most heavily-used commands in shell history:")
        for line in Columnize(out):
            print(line)
        print("Total commands in history =", g.total)

if __name__ == "__main__":
    d = {}  # Options dictionary
    file = ParseCommandLine(d)
    stream = sys.stdin if file == "-" else open(file)
    lines = stream.read().split("\n")
    report_dict = Classify(lines)
    Report(report_dict, maxnum=d["-n"])
