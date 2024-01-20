'''
Sort bash function definitions

    NOTE:  This script is only intended to work with my bash initialization
    files, which use a specific form of function definitions:
        
        function name
        {
            ## Description of function's purpose on one line
            function_body
        }

    The functions are put in alphabetical order and sent to stdout.
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Sort bash function definitions
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import deque
        import getopt
        import os
        import re
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        from get import GetLines
        #from columnize import Columnize
    if 1:   # Global variables
        class G:
            # Storage for global variables as attributes
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:   # Utility
    def GetColors():
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    g.W, g.L = GetScreen()
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] file
          Read the files and sort their bash function definitions into
          alphabetical order.  Use - to read from stdin.
 
          The function definitions must of of the form
            function name
            {{
                ## One line summary of function's purpose
                function_body
            }}
          Otherwise, the script will exit.
        Options:
            -c      Columnize the output
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = False     # Columnize the output
        d["-d"] = False     # Turn on debug printing
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, files = getopt.getopt(sys.argv[1:], "cdh") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cd"):
                d[o] = not d[o]
            elif o == "-h":
                Usage(status=0)
        if len(files) > 1:
            Error("Can only have one file on command line")
        if d["-d"]:
            g.dbg = True
        GetColors()
        return files
if 1:   # Core functionality
    def ProcessFile(file, definitions):
        '''Read the file and parse out its function definitions.  Put them
        into the dictionary definitions keyed by the function's name.  Put
        the 'header' (lines before first function) into definitions[""].
        '''
        if file == "-":
            file = sys.stdin
        lines = [(i + 1, ln) for i, ln in enumerate(GetLines(file, nonl=True))]
        dq = deque(lines)
        foundfuncs = False     # Flags when '^function' found
        funcname =re.compile(r"^function +[A-Za-z_][A-Za-z_0-9]* $")
        funcstart =re.compile(r"^{ *$")
        funcend =re.compile(r"^} *$")
        # Remove the header
        header = []
        while dq:
            linenum, line = dq.popleft()
            if funcname.match(line):
                dq.insert(0, line)
                break
            header.append((linenum, line))
        definitions[""] = header
        Dbg(f"{t('ornl')}Header:{t.n}")
        for ln, l in header:
            Dbg(f"[{ln}]: {l}")
        Dbg(f"{t('ornl')}Function definitions:{t.n}")
        # Process the functions
        breakpoint() #xx
        while dq:
            linenum, line = dq.popleft()
            Dbg(f"[{linenum + 1}] {line}")
            if funcname.match(line):
                foundfuncs = True
                infunc = True
                name = line.replace("function", "").strip()
                funclines = [line.strip()]
            elif funcstart.match(line):
                if not infunc:
                    Error(f"[{file}:{linenum + 1}]:  {line!r} not in function")
                funclines.append(line.strip())
            elif funcend.match(line):
                infunc = False
                funclines.append(line.strip())
            else:
                funclines.append(line.strip())
        if not foundfuncs:
            Error("No functions found")


if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    definitions = {}
    for file in files:
        ProcessFile(file, definitions)
