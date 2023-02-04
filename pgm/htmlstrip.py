'''
Return the relevant text from an HTML file.  Note this is a heuristic for
certain wikipedia files.
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
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
    if 1:   # Global variables
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
    def RemoveHead(s):
        return re.sub("^.*?</head>", "", s, flags=re.S)
    def RemoveScript(s):
        return re.sub("<script>.*</script>", "", s, flags=re.S)
    def RemoveComment(s):
        return re.sub("<!--.*?-->", "", s, flags=re.S)
    def RemoveStyle(s):
        return re.sub("<style.*?/style>", "", s, flags=re.S)
    def RemoveDiv(s):
        return re.sub("<div>.*?</div>", "", s, flags=re.S)
    def RemoveBrackets(s):
        return re.sub("<.*?>", "", s, flags=re.S)
    def ProcessFile(file):
        s = open(file).read()
        u = RemoveHead(s)
        u = RemoveScript(u)
        u = RemoveComment(u)
        u = RemoveStyle(u)
        u = RemoveDiv(u)
        u = RemoveBrackets(u)
        print(u)

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        ProcessFile(file)

