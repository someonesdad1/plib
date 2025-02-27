"""
TODO
    -Trying to do integer conversion after a deliberate syntax error; the
    second conversion should have worked.

        ▶▶▶ int("12", 60)
        zz Got exception:  'file'
        Traceback (most recent call last):
        File "<console>", line 1, in <module>
        ValueError: int() base must be >= 2 and <= 36, or 0
        ▶▶▶ int("12", 6)
        zz Got exception:  'file'
        File "<console>", line 1
            int("12", 60)
                        ^
        SyntaxError: multiple statements found while compiling a single statement

    - Add an ls command (it will call external ls command) with my usual
      aliases
    - It would be nicer to have a central way of adding symbols and adding
      the special commands.  Ideally, it would be done in one function or
      class, making it easy to see what you're getting.
    - The help output should honor the COLUMNS setting if possible.  It does
      this at the start, but it should do it every time it prints the help
      message.  This is because I use it in a long terminal window of 80-150
      lines and I like to ctrl-Scroll the mouse wheel to dynamical change the
      size of things.
    - Stop printing out the command log.
    - Change from color.py to clr.py.
    - Common math symbols should be available:  pi, e, phi.
    - Persistence would be nice.  Invocations in multiple processes will be a
      problem; maybe a fix would be to use an easy-to-break lock that detects
      this but lets you overwrite things if you wish.
    - Is there a way to log all the commands so that they can be run again?  L
      would turn logging on, LL would turn it off.  Turning it on appends to
      the log file, which is emptied on each invocation.
    - Add the ability to separate commands with ';'.
    - e, <, and > are still used with the string buffer.  Now, x executes the
      buffer.
    - It would be nice to add the ability to load a special command package.
      For example, 'l barstock' would load an environment that would let you
      calculate properties of bar stock in the shop (see material.py scipt).  A
      special prompt would tell you that you're in this mode and you could quit
      it by exit.  But the mode's state would be saved so you could re-enter it
      as needed.

    A REPL that gives an interactive python calculator.  See repl.pdf for
    documentation.
"""

from wrap import dedent

__doc__ = dedent("""
    This module provides a REPL (read, evaluate, print, loop) construct that
    simulates the one in the python interactive interpreter.  This code is
    based on class code.InteractiveConsole in the code module.
    
    The origin of this module was my desire to be able to type 'q' to exit
    the standard python interpreter instead of 'quit()' or ctrl-D.  Once
    this was figured out, it was straightforward to add other features
    useful for a command-line calculator:
    
      * flt/cpx numbers:  These are classes derived from float/complex in
        the module f.py.  The module's features are:
    
        * flt/cpx objects:
            * The flt/cpx string interpolations show 3 significant figures. 
            * They "infect" calculations with their types.
            * You can instantiate flt/cpx with physical units.
            * They are intended to be used to perform floating point
            calculations with numbers derived from measurements.
            * Use the h attribute on flt/cpx instances to see supported
            attributes.
            * The f attribute can flip the outputs of str()/repr().  This is
            handy in the interpreter and debugger, which use repr() by default.
            * Set the c attribute to True to get colored output, which helps to
            identify flt/cpx types.
        * The math/cmath symbols are in scope and can take flt/cpx
          arguments.
    
      * Special added commands.  Type 'h' at the prompt to get a list.  If
        you assign a variable to the same name as a command, preface the
        command with one or more space characters.
    
      * User buffer (a string) that you can edit and run the code/commands
        in it.  Note it's not intended for loading/running python scripts,
        as the global environment will be different than the typical script.
    
      * Show the symbols that are in scope.
    
      * Access python's help text via help().
    
      * If you're in a UNIX-like environment, you'll have history and
        command completion available.  You can also send commands to the
        shell.
    
    The physical units in the flt/cpx types are provided by the u.py module.
    
    Here's an example.  Save the text to a file, read it in with the 
    'R file' command, and run it with the 'r' command.
    
        # Ideal gas law example calculation:  the oxygen cylinder on my
        # torch is about 7 inches in diameter and 33 inches long.  The
        # nominal internal volume is about 0.55 cubic feet per a table for
        # a "BL" type cylinder.  The gauge pressure of the tank is 1200
        # psi.  
    
        # Questions:
        #   1.  What is the mass of the remaining oxygen?
        #   2.  How many liters (at 1 atm) of oxygen remain in the tank?
    
        R = flt("8.314 J/(K*mol)")
        R.n = 3         # Show results to 3 figures
        R.f = False     # Don't interchange str() and repr()
        R.c = True      # Use ANSI escape sequences to color flt/cpx
        print(f"R = gas constant = {R}")
    
        # Gas cylinder internal volume
        V = flt("0.55 ft3")
        print(f"V = volume = {V} = {V.to('m3')} = {V.to('L')}")
    
        # This is the pressure reading from the regulator in psig
        # (i.e., gauge pressure with respect to atmospheric pressure),
        # which is corrected to an absolute pressure by adding 1 atm.  
        p = flt("1200 psi") + flt("1 atm")
        print(f"p = pressure = {p} = {p.to('MPa')}")
    
        T = flt("293 K")
        print(f"T = temperature = {T}")
    
        # Number of moles of oxygen
        n = p*V/(R*T)
        print(f"n = {n} = {n.toSI()} = {n.to('mol')}")
        print(f"Dimensions of n = {u.dim(n.u)}")
    
        # Molecular mass (standard atomic mass of oxygen is 16 and it's
        # a diatomic gas)
        molarmass = flt("32 g/mol")
        m = n*molarmass
        print(f"Mass of O₂ = {m} = {m.to('kg')}")
    
        # Since the tank volume is V, the volume Va at 1 atm is calculated
        # from p*V = pa*Va.  Thus, Va = V*p/pa.
        pa = flt("1 atm")
        Va = V*p/pa
        print(f"Volume of O₂ at 1 atm = {Va.to('liters')}")
    
    When you run the commands, you'll see the output
    
        R = gas constant = 8.31 J/(K·mol)
        V = volume = 0.550 ft³ = 0.0156 m³ = 15.6 L
        p = pressure = 1210. psi = 8.38 MPa
        T = temperature = 293. K
        n = 0.274 ft³·mol·psi/J = 53.5 mol = 53.5 mol
        Dimensions of n = Dim("N")
        Mass of O₂ = 8.78 ft³·g·psi/J = 1.71 kg
        Volume of O₂ at 1 atm = 1290. liters
    
    Note the ft³·mol·psi/J units for the number of moles.  A pressure times
    a volume is an energy, so ft³·psi/J is dimensionless, but the u.py
    module doesn't perform this calculation for you.  However, the flt/cpx
    method toSI() will convert a flt/cpx instance to another in the base SI
    units when needed.  The u.dim() method can show you the dimensional
    structure of a unit string; the next line shows n is in the dimensional
    unit "N", quantity of material.
 
    """)
if 1:  # Header
    # Copyright, trigger strings
    # These "trigger strings" can be managed with trigger.py
    ##∞version∞#
    _version = "2 Jun 2021"
    ##∞version∞#
    ##∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # <utility> This provides a REPL I use for an interactive python
    # calculator.  By default it uses flt and cpx number types from
    # f.py, along with units from u.py, letting you do physical
    # calculations with numbers derived from measurements.  An advantage
    # of these types is that they by default only show 3 decimal places
    # in their interpolated strings (you can set the number of digits
    # you want to see), so you don't see all the annoying digits common
    # in floating point calculations.
    ##∞what∞#
    ##∞test∞# ignore #∞test∞#
    # Standard imports
    from atexit import register
    from collections import defaultdict
    import code
    import contextlib
    import getopt
    import io
    import os
    import pathlib
    import readline  # History and command editing
    import rlcompleter  # Command completion
    import subprocess
    import sys
    import tempfile
    import time
    from pdb import set_trace as xx

    # Custom imports
    from wrap import wrap, dedent, indent, Wrap
    from columnize import Columnize

    # import kolor as C
    from color import TRM as t

    # Global variables
    _ = sys.version_info

    class G:  # Container for global variables
        pass

    g = G()
    g.P = pathlib.Path
    g.name = g.P(sys.argv[0])
    g.datafile = g.P(g.name.stem + ".data")
    g.editor = os.environ["EDITOR"]
    g.pyversion = f"{_.major}.{_.minor}.{_.micro}"
    g.ii = isinstance
    # Color coding using ANSI escape codes
    g.blu = t("blul")
    g.brn = t("brn")
    g.grn = t("grnl")
    g.cyn = t("cynl")
    g.red = t("redl")
    g.yel = t("yel")
    g.wht = t("whtl")
    g.whtblu = t("whtl", "blu")
    g.err = t("redl")
    g.ital = t(attr="it")
    g.n = t.n
if 1:  # Utility

    def eprint(*p, **kw):
        "Print to stderr"
        print(*p, **kw, file=sys.stderr)

    def Error(msg, status=1):
        eprint(msg)
        exit(status)

    def Usage(d, status=1):
        print(
            dedent(f"""
        Usage:  {g.name} [options] [cmd1 [cmd2...]]
          Run a python REPL with some added features.  See repl.pdf.
          You can include some starting commands on the command line,
          but some like 'H' won't be recognized.
        Options:
            -h          Print a manpage
            -l file     Log output to a file
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-l"] = "/dev/null"  # Name of file to log to
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
        Print(t.n, end="")

    # Make sure we have no color set at exit
    register(Clean)
if 1:  # Core functionality

    def EditString(string, console):
        if not isinstance(string, str):
            raise TypeError("string must be a str object")
        # We'll edit this string in a new temporary file in the
        # current directory.
        cwd = console.cwd
        tempname = tempfile.mkstemp(
            prefix="repl", suffix=".py", dir=console.cwd, text=True
        )[1]
        file = g.P(tempname)
        file.write_text(string)
        subprocess.call([g.editor, str(file)])
        newstring = file.read_text()
        file.unlink()
        return newstring

    def GetSymbols():
        "Return a dict of favorite symbols"
        from pprint import pprint as pp
        from decimal import Decimal as D, getcontext as ctx
        from dpdecimal import dec
        from pathlib import Path as P
        from fractions import Fraction as F
        from pdb import set_trace as xx

        try:
            from u import u, dim, to
        except ImportError:
            pass
        try:
            from uncertainties import ufloat as uf
        except ImportError:
            pass
        try:
            from matrix import Matrix, vector
        except ImportError:
            pass

        # NOTE:  Edit Special() to change the built-in commands.  You also
        # need to edit IsCommand() for the command to be recognized as
        # special.

        try:
            from f import acos, acosh, asin, asinh, atan, atan2, atanh
            from f import ceil, copysign, cos, cosh
            from f import cpx, dedent, degrees, erf, erfc
            from f import exp, expm1, fabs, factorial, floor, flt, fmod
            from f import frexp, fsum, gamma, gcd, hypot, inf, infj
            from f import isclose, isfinite, isinf, isnan, ldexp, lgamma
            from f import log, log10, log1p, log2, modf, nan, nanj, phase
            from f import pi, polar, pow, radians, rect, remainder, sin
            from f import sinh, sqrt, tan, tanh, tau, trunc

            # I comment this out because it overshadows the edit command
            from f import e

            i = cpx(0, 1)
            i.i = True
            i.f = True
            i.nz = True
            i.c = True
            one = flt(1)
            ii = isinstance
        except ImportError:
            pass
        loc = locals().copy()
        if "z" in loc:
            del loc["z"]
        return loc

    def Help():
        cmds = (
            ("!", "Send command to shell"),
            ("< f", "Read string buffer from file f"),
            ("> f", "Write string buffer to file f"),
            ("CS", "Clear symbols"),
            ("c", "Clear screen"),
            ("d", "Enter debugger"),
            ("E", "Edit buffer"),
            ("f", "Load favorite symbols (edit GetSymbols())"),
            ("H", "Shorthand to run help()"),
            ("q", "Quit"),
            ("R f", "Get file f to run with 'r' command"),
            ("r", "Run file buffer"),
            ("ri", "Run file buffer with 'python -i'"),
            ("s", "Print symbols in scope"),
            ("v", "Show version"),
            ("x", "Execute string buffer"),
        )
        Print("Commands:")
        for cmd, meaning in cmds:
            s = f"{cmd:^5s}  {meaning}"
            Print(s)
        Print(
            wrap(f"""
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
        """)
        )

    def IsCommand(cmd):
        "Return True if the string cmd is a special command"
        if not cmd:
            return False
        if len(cmd) == 1:
            return cmd[0] in "?cCdEfHhqrsvx"
        else:
            return (cmd[0] in "!<>R") or (cmd in "CS ri".split())

    def BreakPoint():
        """Find the line number of the input routine, which lets you set
        a debugger breakpoint at the input line.
        """

        def Find(s):
            c = [(i, u) for i, u in enumerate(lines) if u.strip() == s]
            bp = c[-1][0] + 1
            return bp

        s = "s = input(self.ps).rstrip()"
        u = "returnvalue = console.push(line)"
        lines = g.P(sys.argv[0]).read_text().split("\n")
        Print(
            dedent(f"""
        Set a breakpoint at line {Find(s)} to stop before each input
        Set a breakpoint at line {Find(u)} to stop before execution
        If you use the latter breakpoint, press n or c to continue
        To stop at an imported function named A, issue the command
            b console.locals["A"]
        Note you'll have subsequent problems with stdout, so the best
        strategy is to use 'c' to continue and set another breakpoint.
        """)
        )

    def Columns(seq, indent=""):
        for line in Columnize(seq, indent=" " * 2):
            print(line)

    def FixShellArgument(arg):
        """Some shell commands like ls and grep are better with color
        output enabled.  This also lets me get the aliases I like to
        use for ls-type commands.
        """
        args = arg.split()
        cmd = args[0]
        if cmd in "grep egrep fgrep ls ll lll lrt lsr lz".split():
            c = args.pop(0)
            u = "--group-directories-first"
            args.insert(0, "--color=auto")
            if c == "ls":
                args.insert(0, f"ls {u}")
            elif c == "ll":
                args.insert(0, f"ls -l {u}")
            elif c == "lll":
                args.insert(0, f"ls -lh --si {u}")
            elif c == "lrt":
                args.insert(0, f"ls -lrt {u}")
            elif c == "lsf":
                args.insert(0, f"ls -F  {u}")
            elif c == "lsr":
                args.insert(0, f"ls -R {u}")
            elif c == "lz":
                args.insert(0, f"ls -lSr {u}")
            else:
                args.insert(0, c)
        return " ".join(args)

    def PrintSymbols(console):
        def IsFunc(item):
            return str(type(item)) == "<class 'function'>"

        def IsModule(item):
            return str(type(item)) == "<class 'module'>"

        def IsClass(item):
            return str(type(item)) == "<class 'type'>"

        from f import Delegator, flt, cpx

        Delegator._left = g.brn
        Delegator._right = g.n
        d = console.locals.copy()
        for i in "__name__ __doc__ Delegator constants".split():
            if i in d:
                del d[i]
        symbols = sorted(d.keys())
        if not symbols:
            return
        # Classify into different types
        things = defaultdict(set)
        for symbol in symbols:
            item = d[symbol]
            if g.ii(item, Delegator):
                things["math/cmath functions"].add(symbol)
            elif g.ii(item, (flt, float)):
                things["float/flt"].add(symbol)
            elif g.ii(item, (cpx, complex)):
                things["complex/cpx"].add(symbol)
            elif g.ii(item, list):
                things["list"].add(symbol)
            elif g.ii(item, tuple):
                things["tuple"].add(symbol)
            elif IsFunc(item):
                things["function"].add(symbol)
            elif IsModule(item):
                things["module"].add(symbol)
            elif IsClass(item):
                things["class"].add(symbol)
            else:
                things["other"].add(symbol)
        # Print the symbols
        for category in things:
            print(category)
            o = []
            for i in sorted(things[category]):
                o.append(i)
            Columns(o, " " * 2)

    def Print(*p, **kw):
        "Print to stdout and logfile"
        print(*p, **kw)
        if logfile is not None:
            print(*p, **kw, file=logfile)

    def DumpCmdLog():
        print("Command log:")
        print(cmdlog.getvalue())


if 1:  # Special commands

    def Special(cmd, console):
        cmdlog.write(cmd)
        try:
            first_char = cmd[0]
            arg = "" if len(cmd) == 1 else cmd[1:].strip()
            if first_char == "!":
                # Shell command
                if arg:
                    newarg = FixShellArgument(arg)
                    os.system(newarg)
                return
            elif first_char == "<":
                # Read stringbuffer
                if arg:
                    file = g.P(arg)
                    console.stringbuffer = file.read_text()
            elif first_char == ">":
                # Write stringbuffer
                if arg:
                    file = g.P(arg)
                    file.write_text(console.stringbuffer)
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
            elif cmd == "E":
                # Edit stringbuffer
                console.stringbuffer = EditString(console.stringbuffer, console)
            elif cmd == "f":
                # Load favorite symbols
                console.locals.update(GetSymbols())
                Print("Loaded favorite symbols")
            elif cmd == "h" or cmd == "?":
                # Print help info
                Help()
            elif cmd == "q":
                u = console.time
                Print(f"{u}")  # Print the exit time
                # DumpCmdLog()
                exit(0)
            elif first_char == "R":
                # Set or clear console.file
                console.file = None
                console.args = None
                if arg:
                    args = arg.split()
                    console.file = args[0]
                    if len(args) > 1:
                        console.args = " ".join(args[1:])
            elif cmd in "r ri".split():
                # Run console.file
                if console.file is None:
                    Print("No file set with R command")
                    return
                # Run it as a script
                try:
                    p = g.P(console.file).resolve()
                    if cmd == "ri":
                        c = [sys.executable, "-i", str(p)]
                    else:
                        c = [sys.executable, str(p)]
                    if console.args:
                        c.append(console.args)
                    r = subprocess.call(" ".join(c), shell=True)
                except Exception as e:
                    print(f"Exception:  {e}")
                else:
                    print(f"Script returned {r}")
            elif cmd == "s":
                # Print symbols
                PrintSymbols(console)
            elif cmd == "v":
                # Print repl.py version
                Print(
                    f"{sys.argv[0]} version:  {_version}   "
                    f"[running python {g.pyversion}]"
                )
            elif cmd == "x":
                # Run stringbuffer
                fn = "<stringbuffer>"
                if not console.stringbuffer:
                    Print("String buffer is empty")
                    return
                for line in console.stringbuffer.split("\n"):
                    rv = console.push(line)
                    console.ps = sys.ps2 if rv else sys.ps1
            else:
                Print(f"{g.err}'{cmd}' not recognized{g.n}")
        except Exception as e:
            print(f"{g.brn}Exception in Special():\n{e}{g.n}")


if 1:  # class Console

    class Console(code.InteractiveConsole):
        def __init__(self, locals=None):
            super().__init__(locals=locals)
            self.locals.update(GetSymbols())
            self.cwd = g.P(".").cwd()
            self.stringbuffer = ""
            self.filebuffer = ""

        @property
        def time(self):
            def rlz(s):  # Remove leading zero
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
            return f"{self.time}   Use h for help"

        def start_message(self):
            print(self.msg)

        def write(self, data):
            "Write colorized data to stdout"
            Print(f"{g.err}{data}{g.n}", end="", file=sys.stderr)

        def raw_input(self, prompt=""):
            s = input(self.ps).rstrip()
            Print(g.n, end="")  # Turn off any colorizing
            if not s:
                return s
            # Handle special commands before the interpreter sees them
            if s == "H":
                return "help()"
            if s not in self.locals and IsCommand(s.strip()):
                print(f"{sys.ps1}{s}", file=logfile)
                Special(s.strip(), self)
                return ""
            print(f"{sys.ps1}{s}", file=logfile)
            return s


if 1:  # Setup
    """Use a code.InteractiveInterpreter object to get a REPL (read,
    evaluate, print, loop) construct, which simulates what the python
    interactive interpreter does.  The code module lets you build your
    own REPl with custom commands.
    """
    logfile = None
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    # System prompts
    if 0:  # Plain
        sys.ps1 = f"{'▶' * 3} "
    else:  # Colored
        sys.ps1 = f"{g.whtblu}{'▶' * 3}{g.n} "
    sys.ps2 = f"{g.whtblu}{'·' * 3}{g.n} "
if __name__ == "__main__":  # Run the console REPL
    stdout, stderr = io.StringIO(), io.StringIO()
    cmdlog = io.StringIO()  # Used to log commands
    console = Console()
    console.ps = sys.ps1
    nl = "\n"
    file = d["-l"] if d["-l"] is not None else "/dev/null"
    logfile = open(file, "w")
    console.start_message()
    returnvalue = None
    # Show starting message
    if not stdout.getvalue():
        with contextlib.redirect_stdout(stdout):
            print(console.msg, file=logfile)
        stdout = io.StringIO()
    while True:  # REPL loop
        try:
            while args:
                # Execute any commands on command line (note 'H' won't
                # be recognized
                s = args.pop(0).strip()
                if s not in console.locals and IsCommand(s):
                    cmdlog.write(s + nl)
                    Special(s, console)
            else:
                line = console.raw_input().rstrip()
        except EOFError:
            exit()
        if not returnvalue:
            stdout, stderr = io.StringIO(), io.StringIO()
        if line.startswith("help(") or line == "help":
            # No plumbing so pager works
            returnvalue = console.push(line)
        else:
            # Capture stdout & stderr to StringIO objects
            try:
                with contextlib.redirect_stderr(stderr):
                    with contextlib.redirect_stdout(stdout):
                        cmdlog.write(line + nl)
                        returnvalue = console.push(line)
            except Exception as e:
                print("zz Got exception: ", e)
        if returnvalue:  # Need more input
            console.ps = sys.ps2
        else:  # Command finished
            console.ps = sys.ps1
            s, e = stdout.getvalue(), stderr.getvalue()
            if s:
                Print(s, end="")
            if e:
                # Decorate with escape codes to color
                Print(f"{g.err}{e}{g.n}", end="")
