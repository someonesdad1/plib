'''
Collapse multiple blank lines to one blank line
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Collapse multiple blank lines to one blank line.
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        from pprint import pprint as pp
        import re
        import sys
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
    if 1:   # Global variables
        ii = isinstance
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Remove whitespace on empty lines and collapse multiple empty
          lines into one line.  Leading empty lines are removed also.
          Use '-' for stdin.
        Options:
            -h      Show help
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "dh") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("d"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        return args
if 1:   # Core functionality
    def ProcessFile(file):
        # Get string
        s = sys.stdin.read() if file == "-" else open(file).read()
        s = s.strip()
        if 1:   # First step:  lines with ws only to empty lines
            lines = s.split("\n")
            # Change all lines with only whitespace to empty lines
            lines = [re.sub(r"^[ \t\r\f\v]+$", r"", i) for i in lines]
            # Change multiple newlines to one
            s = '\n'.join(lines)
        if 1:   # Second step:  Change 3+ newlines to two
            s = re.sub(r"\n\n\n+", r"\n\n", s)
        print(s)

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        ProcessFile(file)
