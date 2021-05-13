'''

* help() doesn't work with stdout/stderr redirected

* Add Matrix/vector support.  Look at an auxiliary library for linear
  regression.

* Search for 'python units library' and there are numerous choices.
    Maybe it would make more sense to integrate one of them.

    * https://pint.readthedocs.io/en/stable/
    * https://pypi.org/project/siunits/
    * https://github.com/connorferster/forallpeople
    * https://fangohr.github.io/blog/physical-quantities-numerical-value-with-units-in-python.html

----------------------------------------------------------------------
A REPL I use for an interactive python calculator.  See repl.pdf for
documentation.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞version∞# None #∞version∞#
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # This provides a REPL I use for an interactive python calculator.
    #∞what∞#
    pass
if 1:   # Standard imports
    from atexit import register
    import code
    import contextlib
    import getopt
    import io
    import os
    import pathlib
    import pickle
    import readline
    import rlcompleter
    import subprocess
    import sys
    import tempfile
    import time
    from pdb import set_trace as xx
if 1:   # Custom imports
    from util import EditData
    from wrap import wrap, dedent, indent, Wrap
    from columnize import Columnize
    import color as C
    if 0:
        import debug
        debug.SetDebugger()  # Start debugger on unhandled exception
if 1:   # Global variables
    # Escape strings for color coding
    class G: pass   # Container for global variables
    g = G()
    g.P = pathlib.Path
    g.cyn = C.fg(C.lcyan, s=1)
    g.wht = C.fg(C.lwhite, s=1)
    g.err = C.fg(C.lmagenta, s=1)
    g.norm = C.normal(s=1)
if 1:   # Utility
    def eprint(*p, **kw):
        'Print to stderr'
        print(*p, **kw, file=sys.stderr)
    def Error(msg, status=1):
        eprint(msg)
        exit(status)
    def Usage(d, status=1):
        name = sys.argv[0]
        print(dedent(f'''
        Usage:  {name} [options]
          Run a python REPL with some added features.  See repl.pdf.
        Options:
            -h          Print a manpage
            -l file     Log output to a file
    '''))
        exit(status)
    def ParseCommandLine(d):
        d["-l"] = None      # Name of file to log to
        try:
            opts, args = getopt.getopt(sys.argv[1:], "l:h", "help")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-l":
                d[o] = a
            elif o in ("-h", "--help"):
                Usage(d, status=0)
        return args
    def Clean():
        'Register a cleanup function to ensure no color for shell'
        print(C.normal(s=1), end="")
    register(Clean)
if 1:   # Core functionality
    def GetSymbols():
        'Return a dict of symbols I want'
        from u import u
        from pprint import pprint as pp
        from decimal import Decimal as D
        from pathlib import Path as P
        from fractions import Fraction as F
        from uncertainties import ufloat as uf
        from matrix import Matrix, vector
        from f import acos, acosh, asin, asinh, atan, atan2, atanh
        from f import ceil, cmath, constants, copysign, cos, cosh
        from f import cpx, decimal, dedent, degrees, e, erf, erfc
        from f import exp, expm1, fabs, factorial, floor, flt, fmod
        from f import frexp, fsum, gamma, gcd, hypot, inf, infj
        from f import isclose, isfinite, isinf, isnan, ldexp, lgamma
        from f import log, log10, log1p, log2, modf, nan, nanj, phase
        from f import pi, polar, pow, radians, rect, remainder, sin
        from f import sinh, sqrt, tan, tanh, tau, trunc
        x, z = flt(pi/7), cpx(pi/7, 7/pi)
        z.i = True
        z.c = True
        z.f = True
        symbols = locals().copy()
        return symbols
    def Special(s, console):
        if not s.strip():
            return
        char, cmd = s[0], s[1:].strip()
        if char == "!":
            # Shell command
            os.system(s[1:])
            return
        elif cmd[0] == "<":  
            # Read buffer
            file = g.P(cmd[1:].strip())
            console.userbuffer = file.read_text()
        elif cmd[0] == ">":  
            # Write buffer
            file = g.P(cmd[1:].strip())
            file.write_text(console.userbuffer)
        elif cmd in "cls c".split():
            # Clear the screen
            os.system("clear")
        elif cmd == "C":  
            # Clear the local variables
            console.locals.clear()
        elif cmd == "d":  
            # Enter debugger
            breakpoint()
        elif cmd == "e":  
            # Edit buffer
            console.userbuffer = EditData(console.userbuffer)
        elif cmd == "f":  
            # Load favorite symbols
            console.locals.update(GetSymbols())
        elif cmd == "h":
            # Print help info
            help = sorted([i.strip() for i in '''
              .c clear screen, .C clear symbols, .d debugger,
              .e edit buffer, .r run buffer (echo), .x execute buffer,
              .s symbols, .q quit
              .< file (read), '.> file' (write),
            '''.replace("\n", " ").split(",") if i.strip()])
            for i in Columnize(help):
                print(i)
                if d["-l"]:
                    print(i, file=log)
        elif cmd == "r":  
            # Run buffer
            fn = "<userbuffer>"
            for line in console.userbuffer.split("\n"):
                rv = console.push(line)
                console.ps = sys.ps2 if rv else sys.ps1
        elif cmd == "s":  
            # Print symbols
            sym = sorted(console.locals.keys())
            for line in Columnize(sym):
                Print(line)
        else:
            Print(f"{g.err}'{s}' not recognized as special command{g.norm}")
    class Console(code.InteractiveConsole):
        @property
        def msg(self):
            v = sys.version_info
            ver = f"{v.major}.{v.minor}.{v.micro}"
            ampm = time.strftime("%p")
            tm = time.strftime(f"%d%b%Y %I:%M:%S {ampm.lower()} %a")
            s = dedent(f'''
            [python {ver} {tm}]  .q quit, .h help
            '''[1:].rstrip())
            return s
        def start_message(self):
            print(self.msg)
        def write(self, data):
            'Write colorized data to stdout'
            print(f"{g.err}{data}{g.norm}", end="", file=sys.stderr)
        def raw_input(self, prompt=""):
            s = input(self.ps)
            print(g.norm, end="")   # Turn off any colorizing
            # Handle special commands before the interpreter sees them
            if s == "q" and "q" not in self.locals:
                exit()
            elif s and s[0] in ".!":
                Special(s, self)
                return ""
            return s

if __name__ == "__main__": 
    '''Use a code.InteractiveInterpreter object to get a REPL (read,
    evaluate, print, loop) construct, which is what the python
    interactive interpreter does).  This shows how to build your own
    REPl with custom commands.
    '''
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    # Set up system prompts
    if 0:
        n = 3
        sys.ps1 = f"{'»'*n} "
        sys.ps2 = f"{'.'*n} "
    else:
        n = 2
        sys.ps1 = f"{'>'*n} "
        sys.ps2 = f"{'.'*n} "
    # Run the console REPL
    stdout, stderr = io.StringIO(), io.StringIO()
    console = Console()
    console.ps = sys.ps1
    console.userbuffer = ""
    console.start_message()
    console.locals.clear()
    returnvalue = None
    file = d["-l"] if d["-l"] is not None else "/dev/null"
    log = open(file, "w")
    if not stdout.getvalue():
        with contextlib.redirect_stdout(stdout):
            print(console.msg, file=log)
        stdout = io.StringIO()
    while True:     # REPL loop
        try:
            line = console.raw_input().rstrip()
        except EOFError:
            exit()
        if not returnvalue and returnvalue is not None:
            stdout, stderr = io.StringIO(), io.StringIO()
        if line.startswith("help(") or line == "help":
            # No plumbing so pager works
            returnvalue = console.push(line)
        else:
            with contextlib.redirect_stderr(stderr):
                with contextlib.redirect_stdout(stdout):
                    returnvalue = console.push(line)
        if returnvalue:
            console.ps = sys.ps2    # Need more input
        else:
            console.ps = sys.ps1    # Command finished
            s, e = stdout.getvalue(), stderr.getvalue()
            if s:
                print(s, end="")
                print(s, end="", file=log)
            if e:
                if d["-l"]:
                    # Decorate with escape codes to color (they aren't
                    # present, even though write() uses them)
                    print(f"{g.err}{e}{g.norm}", end="")
                    print(f"{g.err}{e}{g.norm}", end="", file=log)
                else:
                    print(e, end="")
                    print(e, end="", file=log)
