'''

* Bug:  asin(2) doesn't work; it should return
  1.5707963267948966+1.3169578969248166j

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
if 1:   # Standard imports
    # These "trigger strings" can be managed with trigger.py
    #∞version∞# 
    _version = "2Jun2021"
    #∞version∞#
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # This provides a REPL I use for an interactive python calculator.
    #∞what∞#
    from atexit import register
    import code
    import contextlib
    import getopt
    import io
    import os
    import pathlib
    import readline         # History and command editing
    import rlcompleter      # Command completion
    import subprocess
    import sys
    import tempfile
    import time
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import wrap, dedent, indent, Wrap
    from columnize import Columnize
    import color as C
if 1:   # Global variables
    class G: pass   # Container for global variables
    g = G()
    g.P = pathlib.Path
    # Color coding using ANSI escape codes
    g.blu = C.fg(C.lblue, s=1)
    g.brn = C.fg(C.brown, s=1)
    g.grn = C.fg(C.lgreen, s=1)
    g.cyn = C.fg(C.lcyan, s=1)
    g.red = C.fg(C.lred, s=1)
    g.yel = C.fg(C.yellow, s=1)
    g.wht = C.fg(C.lwhite, s=1)
    g.whtblu = C.fg(C.lwhite, C.blue, s=1)
    g.err = C.fg(C.red, s=1)
    g.norm = C.normal(s=1)
    g.name = sys.argv[0]
    g.editor = "vim"
    _ = sys.version_info
    g.pyversion = f"{_.major}.{_.minor}.{_.micro}"
if 1:   # Utility
    def eprint(*p, **kw):
        'Print to stderr'
        print(*p, **kw, file=sys.stderr)
    def Error(msg, status=1):
        eprint(msg)
        exit(status)
    def Usage(d, status=1):
        print(dedent(f'''
        Usage:  {g.name} [options]
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
        Print(C.normal(s=1), end="")
    register(Clean)
if 1:   # Core functionality
    def EditString(data):
        if not isinstance(data, str):
            raise TypeError("data must be a str object")
        with tempfile.NamedTemporaryFile() as temp:
            file = g.P(temp.name)
            file.write_text(data)
            subprocess.call([g.editor, str(file)])
            data = file.read_text()
        return data
    def GetSymbols():
        'Return a dict of favorite symbols'
        from u import u, dim
        from pprint import pprint as pp
        from decimal import Decimal as D
        from pathlib import Path as P
        from fractions import Fraction as F
        from uncertainties import ufloat as uf
        from matrix import Matrix, vector
        from pdb import set_trace as xx 
        from f import acos, acosh, asin, asinh, atan, atan2, atanh
        from f import ceil, cmath, constants, copysign, cos, cosh
        from f import cpx, decimal, dedent, degrees, e, erf, erfc
        from f import exp, expm1, fabs, factorial, floor, flt, fmod
        from f import frexp, fsum, gamma, gcd, hypot, inf, infj
        from f import isclose, isfinite, isinf, isnan, ldexp, lgamma
        from f import log, log10, log1p, log2, modf, nan, nanj, phase
        from f import pi, polar, pow, radians, rect, remainder, sin
        from f import sinh, sqrt, tan, tanh, tau, trunc
        from f import Delegator
        z = cpx(0)
        z.i = True
        z.f = True
        loc = locals().copy()
        del loc["z"]
        return loc
    def Help():
        cmds = (
            ("!", "Send command to shell"),
            ("< f", "Read buffer from file f"),
            ("> f", "Write buffer to file f"),
            ("CS", "Clear symbols"),
            ("c", "Clear screen"),
            ("d", "Enter debugger"),
            ("e", "Edit buffer"),
            ("f", "Load favorite symbols (edit GetSymbols())"),
            ("H", "Shorthand to run help()"),
            ("q", "Quit"),
            ("r", "Run buffer"),
            ("s", "Print symbols in scope"),
            ("v", "Show version"),
        )
        Print("Commands:")
        for cmd, meaning in cmds:
            s = f"{g.brn}{cmd:^5s}{g.norm}  {meaning}"
            s = f"{cmd:^5s}  {meaning}"
            Print(s)
        Print(wrap(f'''
        If a command is defined as a symbol, then preface it with a
        space character to execute it as a command.
 
        The buffer is used to let you compose code and run it as needed.
        It persists only while {g.name} is running, so save it in the
        editor or with the '>' command to a file.  If you define a
        function, include a blank line after the function's end so that
        the interpreter recogizes the end properly.
 
        You can customize most of the behavior of {g.name} by editing the
        script.  If you are running in a UNIX-like environment or
        cygwin, you should have history and command completion available
        via readline.
        '''))
    def IsCommand(cmd):
        'Return True if the string cmd is a special command'
        cmd = cmd.strip()
        if not cmd:
            return False
        first_char = cmd[0]
        if len(cmd) == 1:
            if first_char in "cCdefHhqrsv":
                return True
        else:
            if first_char in "!<>":
                return True
            elif cmd in "CS".split():
                return True
        return False
    def BreakPoint():
        '''Find the line number of the input routine, which lets you set
        a debugger breakpoint at the input line.
        '''
        def Find(s):
            c = [(i, t) for i, t in enumerate(lines) if t.strip() == s]
            bp = c[-1][0] + 1
            return bp
        s = "s = input(self.ps).rstrip()"
        t = "returnvalue = console.push(line)"
        lines = g.P(sys.argv[0]).read_text().split("\n")
        Print(dedent(f'''
        Set a breakpoint at line {Find(s)} to stop before each input
        Set a breakpoint at line {Find(t)} to stop before execution
        If you use the latter breakpoint, press n or c to continue
        To stop at an imported function named A, issue the command
            b console.locals["A"]
        Note you'll have subsequent problems with stdout, so the best
        strategy is to use 'c' to continue and set another breakpoint.
        '''))
    def FixShellArgument(arg):
        '''Some shell commands like ls and grep are better with color
        output enabled.  This also lets me get the aliases I like to
        use for ls-type commands.
        '''
        args = arg.split()
        cmd = args[0]
        if cmd in "grep egrep fgrep ls ll lll lrt lsr lz".split():
            c = args.pop(0)
            t = "--group-directories-first"
            args.insert(0, "--color=auto")
            if c == "ls":
                args.insert(0, f"ls {t}")
            elif c == "ll":
                args.insert(0, f"ls -l {t}")
            elif c == "lll":
                args.insert(0, f"ls -lh --si {t}")
            elif c == "lrt":
                args.insert(0, f"ls -lrt {t}")
            elif c == "lsf":
                args.insert(0, f"ls -F  {t}")
            elif c == "lsr":
                args.insert(0, f"ls -R {t}")
            elif c == "lz":
                args.insert(0, f"ls -lSr {t}")
            else:
                args.insert(0, c)
        return ' '.join(args)
    def Print(*p, **kw):
        'Print to stdout and log'
        print(*p, **kw)
        print(*p, **kw, file=log)
if 1:   # Special commands
    def Special(cmd, console):
        first_char = cmd[0]
        arg = "" if len(cmd) == 1 else cmd[1:].strip()
        if first_char == "!":
            # Shell command
            if arg:
                newarg = FixShellArgument(arg)
                os.system(newarg)
            return
        elif first_char == "<":  
            # Read buffer
            if arg:
                file = g.P(arg)
                console.userbuffer = file.read_text()
        elif first_char == ">":  
            # Write buffer
            if arg:
                file = g.P(arg)
                file.write_text(console.userbuffer)
        elif cmd == "c" or cmd == "cls":
            # Clear the screen
            os.system("clear")
        elif cmd == "CS":  
            # Clear the local variables
            console.locals.clear()
        elif cmd == "d":  
            # Enter debugger
            BreakPoint()
            breakpoint()
        elif cmd == "e":  
            # Edit buffer
            console.userbuffer = EditString(console.userbuffer)
        elif cmd == "f":  
            # Load favorite symbols
            console.locals.update(GetSymbols())
            Print("Loaded favorite symbols")
        elif cmd == "h":
            # Print help info
            Help()
        elif cmd == "q":  
            t = console.time
            Print(f"{t}")
            exit(0)
        elif cmd == "r":  
            # Run buffer
            fn = "<userbuffer>"
            for line in console.userbuffer.split("\n"):
                rv = console.push(line)
                console.ps = sys.ps2 if rv else sys.ps1
        elif cmd == "s":  
            # Print symbols
            d = console.locals
            symbols = sorted(d.keys())
            if symbols:
                lquote, rquote = "", ""
                if "Delegator" in symbols:
                    lquote = d["Delegator"]._left
                    rquote = d["Delegator"]._right
                o = []
                for symbol in symbols:
                    if symbol == "Delegator":
                        if symbol == "Delegator":
                            continue
                        continue
                    item = d[symbol]
                    s = str(item)
                    if s.startswith(lquote):
                        s = s.replace(lquote, "").replace(rquote, "")
                        o.append(f"{g.brn}{s}{g.norm}")
                    else:
                        o.append(symbol)
                try:
                    for line in Columnize(o):
                        Print(line)
                    if lquote:
                        Print("Wrapped math/cmath functions are in color.  Thus, you can use expressions")
                        Print("like cos(1) and cos(1j) directly.")
                except ValueError:
                    pass
                if "Delegator" in symbols:
                    del d["Delegator"]
        elif cmd == "v":  
            # Print repl.py version
            Print(f"{sys.argv[0]} version:  {_version}   "
                  f"[running python {g.pyversion}]")
        else:
            Print(f"{g.err}'{cmd}' not recognized{g.norm}")
if 1:   # class Console
    class Console(code.InteractiveConsole):
        @property
        def time(self):
            def rlz(s):     # Remove leading zero
                if s[0] == "0":
                    s = s[1]
                return s
            T = time.strftime
            ampm = T("%p").lower()
            day = rlz(T("%d"))
            date = T(f"{day} %b %Y")
            hr = rlz(T("%I"))
            tm = T(f"{hr}:%M:%S {ampm} %a")
            return f"{date} {tm}"
        @property
        def msg(self):
            return f"{self.time}"
        def start_message(self):
            print(self.msg)
        def write(self, data):
            'Write colorized data to stdout'
            Print(f"{g.err}{data}{g.norm}", end="", file=sys.stderr)
        def raw_input(self, prompt=""):
            s = input(self.ps).rstrip()
            Print(g.norm, end="")   # Turn off any colorizing
            if not s:
                return s
            # Handle special commands before the interpreter sees them
            if s == "H":
                return "help()"
            if s not in self.locals and IsCommand(s.strip()):
                Special(s.strip(), self)
                return ""
            return s
if 1:   # Setup
    '''Use a code.InteractiveInterpreter object to get a REPL (read,
    evaluate, print, loop) construct, which simulates what the python
    interactive interpreter does.  The code module lets you build your
    own REPl with custom commands.
    '''
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    # System prompts (some possible characters are >˃⪢➔⇉⇶⮞▶⯈).  It's
    # handy to choose characters other than those used by the default
    # python REPL code so that you know this isn't a standard python
    # interpreter prompt (color can help with this too).
    sys.ps1 = f"{'▶'*3} "
    sys.ps2 = f"{'·'*3} "
if 1:   # Run the console REPL
    stdout, stderr = io.StringIO(), io.StringIO()
    console = Console()
    console.ps = sys.ps1
    console.userbuffer = ""
    file = d["-l"] if d["-l"] is not None else "/dev/null"
    log = open(file, "w")
    console.start_message()
    console.locals.clear()
    console.locals.update(GetSymbols())
    returnvalue = None
    if not stdout.getvalue():
        with contextlib.redirect_stdout(stdout):
            print(console.msg, file=log)
        stdout = io.StringIO()
    while True:     # REPL loop
        try:
            while args:
                # Execute any commands on command line (note 'H' won't
                # be recognized
                s = args.pop(0).strip()
                if s not in console.locals and IsCommand(s):
                    Special(s, console)
            else:
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
                Print(s, end="")
            if e:
                if d["-l"]:
                    # Decorate with escape codes to color (they aren't
                    # present, even though write() uses them)
                    Print(f"{g.err}{e}{g.norm}", end="")
                else:
                    Print(e, end="")
