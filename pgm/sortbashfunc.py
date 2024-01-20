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
        from columnize import Columnize
        if 1:
            import debug
            debug.SetDebugger()
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
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.N}", end="", file=Dbg.file)
    Dbg.file = sys.stderr   # Debug printing to stderr by default
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
    class Function:
        '''Give the constructor a deque of lines to a text file.  When it
        encounters a line of the form 'function name', it will get
        remaining lines until it has the full functional form, ending on a
        line of '}'.

        An instances attributes are:
            name    = function name
            lines   = lines of the function body
            summary = description string
        '''
        def __init__(self, dq):
            '''The deque dq must be tuples of (int, str) where the integer
            is the 1-based line number in the file and str is the line's
            text without an ending newline.
            '''
            # Regex to identify a starting line
            r =re.compile(r"^function +[A-Za-z_][A-Za-z_0-9]* $")
            lines, found = [], False
            start, end = "{", "}"
            while dq:
                n, line = dq.popleft()
                if r.match(line):
                    found = True
                    break
            if not found:
                Error("Start of function's lines not found")
            lines.append((n, line.strip()))
            # Get function name
            f = line.split()
            if len(f) != 2:
                Error(f"[{n}]: {line!r} is a bad function starting line")
            self.name = f[1]
            # Next line must be '{'
            n, line = dq.popleft()
            if not line.strip() == start:
                Error(f"[{n}]: {line!r} should be '{start}'")
            lines.append((n, line))
            # Next line must be a comment with leading '##'
            n, line = dq.popleft()
            if not line.strip().startswith("##"):
                Error(f"[{n}]: {line!r} missing '##'")
            lines.append((n, line))
            self.summary = line.strip().replace("##", "", 1).strip()
            # Get lines until we get a "}"
            while dq:
                n, line = dq.popleft()
                lines.append((n, line))
                if line.strip() == end:
                    break
            if lines[-1][1] != end:
                Error(f"{self.name!r} missing ending {end!r}")
            self.lines = lines
            if g.dbg:
                Dbg(f"{t('grnl')}{self.name}: {self.summary}")
                for i, s in lines:
                    Dbg(f"  [{i}]: {s}")

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
            i = dq.popleft()
            linenum, line = i
            if funcname.match(line):
                dq.insert(0, i)
                break
            header.append(i)
        definitions[""] = header
        Dbg(f"{t('ornl')}Header:{t.n}")
        for ln, l in header:
            Dbg(f"[{ln}]: {l}")
        Dbg(f"{t('ornl')}Function definitions:{t.n}")
        # Process the functions
        if 0:
            while dq:
                i = dq.popleft()
                linenum, line = i
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
        else:
            while dq:
                f = Function(dq)
                definitions[f.name] = f

        pp(definitions) #xx


if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    definitions = {}
    for file in files:
        ProcessFile(file, definitions)
