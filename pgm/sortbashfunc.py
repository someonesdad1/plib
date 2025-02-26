"""
Sort bash function definitions

    NOTE:  This script is only intended to work with my bash initialization
    files, which use a specific form of function definitions:

        function name [()]
        {
            ## Description of function's purpose on one line
            function_body
        }

    The parenthese after the function name are optional.  The functions are
    put in alphabetical order and sent to stdout.
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Sort bash function definitions
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from collections import deque
        import getopt
        import os
        import re
        from pathlib import Path as P
        import sys
        from pprint import pprint as pp
    if 1:  # Custom imports
        from wrap import dedent
        from color import t
        from get import GetLines
        from columnize import Columnize

        if 1:
            import debug

            debug.SetDebugger()
    if 1:  # Global variables

        class G:
            # Storage for global variables as attributes
            pass

        g = G()
        g.dbg = False
        ii = isinstance
        # Regular expressions to find lines of interest
        g.funcname = re.compile(r"^function +([A-Za-z_][A-Za-z_0-9]*) *(\( *\))? *$")
        g.funcstart = re.compile(r"^{ *$")
        g.funcend = re.compile(r"^} *$")
        # Hold spurious lines, which are blank or comment lines between
        # functions
        g.spurious = []
if 1:  # Utility

    def GetColors():
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""

    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )

    g.W, g.L = GetScreen()

    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.N}", end="", file=Dbg.file)

    Dbg.file = sys.stderr  # Debug printing to stderr by default

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] file
          Read the files and sort their bash function definitions into
          alphabetical order.  Use - to read from stdin.
 
          The function definitions must of of the form
            function name
            {{
                ## One line summary of function's purpose
                function_body
            }}
          No comments are allowed on the function line or the {{ or }} lines.
          The function_body can have any form desired.
        Options:
            -c      Columnize the output
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-c"] = False  # Columnize the output
        d["-d"] = False  # Turn on debug printing
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
        return files[0]


if 1:  # Core functionality

    class Function:
        """Give the constructor a deque of lines to a text file.  When it
        encounters a line of the form 'function name', it will get
        remaining lines until it has the full functional form, ending on a
        line of '}'.

        The instance attributes are:
            name    = function name
            lines   = lines of the function body
            summary = description string
        """

        def __init__(self, dq):
            """The deque dq must be tuples of (int, str) where the integer
            is the 1-based line number in the file and str is the line's
            text without an ending newline.
            """
            # Regex to identify a starting line
            r = g.funcname
            lines, found = [], False
            start, end = "{", "}"
            while dq:
                n, line = dq.popleft()
                # print(f"{t('yel')}[{n}] {line!r}{t.n}")
                mo = r.match(line)
                if mo:
                    found = True
                    break
            if not found:
                Error("Start of function's lines not found")
            lines.append((n, line.strip()))
            # Get function name
            self.name = mo.groups()[0]
            # Next line must be '{'
            n, line = dq.popleft()
            if line.rstrip() != start:  # No leading whitespace
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
                if line.rstrip() == end:  # No leading whitespace
                    break
            if lines[-1][1] != end:
                Error(f"{self.name!r} missing ending {end!r}")
            self.lines = lines
            if g.dbg:
                Dbg(f"{t('grnl')}{self.name}: {self.summary}")
                for i, s in lines:
                    Dbg(f"  [{i}]: {s}")

        def __str__(self):
            return f"Function({self.name}: {self.summary})"

        def __repr__(self):
            return f"Function({self.name}: {self.summary})"

    def ProcessFile(file, definitions):
        """Read the file and parse out its function definitions.  Put them
        into the dictionary definitions keyed by the function's name.  Put
        the 'header' (lines before first function) into definitions[""].
        """
        if file == "-":
            file = sys.stdin
        lines = [(i + 1, ln) for i, ln in enumerate(GetLines(file, nonl=True))]
        dq = deque(lines)
        # Remove any empty lines at beginning or end
        while not dq[0][1].strip():
            dq.popleft()
        while not dq[-1][1].strip():
            dq.pop()
        # Remove the header
        header = []
        while dq:
            i = dq.popleft()
            linenum, line = i
            mo = g.funcname.match(line)
            if mo:
                dq.insert(0, i)
                break
            header.append(i)
        definitions[""] = header
        Dbg(f"{t('ornl')}Header:{t.n}")
        for ln, l in header:
            Dbg(f"[{ln}]: {l}")
        Dbg(f"{t('ornl')}Function definitions:{t.n}")
        # Process the functions
        mt = lambda x: not x[0][1].strip() or x[0][1].strip()[0] == "#"
        while dq:
            f = Function(dq)
            definitions[f.name] = f
            if not dq:
                break
            # Remove any blank lines or comments
            next_line = dq[0][1]
            while dq and mt(dq):
                ln, line = dq.popleft()
                if line.strip():
                    g.spurious.append((ln, line))

    def PrintResults(definitions):
        if g.spurious:
            print(f"{t('ornl')}Error{t.n}:  spurious line(s) in {g.file!r}")
            for ln, line in g.spurious:
                print(f"  [{t('trq')}{ln}{t.n}]: {line!r}")
            print(f"(spurious means an empty line or a comment between functions)")
            exit(1)
        for i in definitions[""]:
            ln, l = i
            print(l)
        for name in sorted(definitions.keys(), key=str.lower):
            if not name:
                continue
            # print(name)
            if 1:
                funcobj = definitions[name]
                for ln, l in funcobj.lines:
                    print(l)


if __name__ == "__main__":
    d = {}  # Options dictionary
    g.file = ParseCommandLine(d)
    definitions = {}
    ProcessFile(g.file, definitions)
    if 1:
        PrintResults(definitions)
