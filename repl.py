'''

Prototype of my own REPL that can use color and respond to 'q' for
quitting, which I want.

* Search for some REPL projects with 'python repl implementation'
    * https://github.com/prompt-toolkit/ptpython    Looks powerful
    * https://pypi.org/project/py3repl/             Simplistic
      See below for his code.

* Read the docs on the code module, which is intended for providing your
  own REPL loops.  I learned about this from
  http://masnun.com/2014/01/09/embed-a-python-repl-in-your-program.html

  It appears that when you run python interactively, it's equivalent to
  running 'python code.py'.

* When a command's output will produce more than will fit on the screen,
  pipe it to less or open it with the editor.

* Use atexit to make sure the persistence dict is saved to disk.

* Now a beginning ! character calls Special().  Change this to a easy to
  type character like . that would otherwise be a syntax error.

    .h          Help on special commands

    .q          Quit if 'q' has been made a variable name

    .d name     Delete a named persistent location

    .D ns       Delete a namespace.  All keys in the dict that begin
                with 'ns.' will be deleted.

    .l [ns]     List all persisted names.  If namespace ns is given,
                only list those names.

    .> name     Writes the current buffer to a peristent storage location
                in a dict.  Won't overwrite an existing buffer.

    .> ns.name  Provides ns as a namespace.  You can use ns.name1.name2...

    .< name     Reads in name's text into current buffer

    .>> file    Writes the current buffer to a file 

    .<< file    Reads file into current buffer 

    .>>> file   Appends buffer to file

    .<<< file   Appends it to current buffer

    .! [name]   Execute current or named buffer

    .c          Loads and edits the current configuration, which will be
                documented python code

    .C          Toggle color and and off (flt/cpx color is independent)

    .L name     Load all symbols from module name

    .R name     Remove all symbols from module name


----------------------------------------------------------------------
The simplistic REPL:

    from colorama import Fore, init

    init(autoreset=True)

    success = lambda input: f"{Fore.GREEN}{input}"
    failure = lambda input: f"{Fore.RED}{input}"


    def info() -> None:
        print()
        print(f"{Fore.GREEN}Welcome to python nano-REPL")
        print(f"{Fore.BLUE}author: Amal Shaji")
        print(f"{Fore.BLUE}repo  : https://github.com/amalshaji/pyrepl")
        print(f"{Fore.YELLOW}crtl-c to quit")
        print()


    def repl() -> None:
        info()
        try:
            while True:
                try:
                    _in = input(">>> ")
                    try:
                        print(success(eval(_in)))
                    except:
                        out = exec(_in)
                        if out != None:
                            print(success(out))
                except Exception as e:
                    print(failure(f"Error: {e}"))
        except KeyboardInterrupt as e:
            print("\nExiting...")


    if __name__ == "__main__":
        repl()

----------------------------------------------------------------------

When run, you're dumped into an editor to write some strings.  When you
exit, the file's content will be run with the commands colorized and the
results in a plain color.  At the end, you're at a prompt; enter e to
edit the string again or q to quit (an exit() at the end of the file
automatically causes an exit.

The -k kwd option keeps the file's string so you can run it later if you
put the keyword on the command line.  Use -K to see a list of keywords.

Example:  You start the script and you're put into your editor.  Enter
the text you want evaluated, such as 

    d = {}
    pp(d)

When you exit the editor, this is run with common whitespace removed.
At the ending prompt, enter 

    'e'         to edit and run again
    'q'         to quit
    'k kwd'     to save under the indicated keyword
    
'''
 
if 1:  # Copyright, license
    pass
if 1:   # Standard imports
    import code
    import getopt
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
    from globalcontainer import Global, Variable, Constant
    import color as C
    if 0:
        import debug
        debug.SetDebugger()  # Start debugger on unhandled exception
    # Register a cleanup function to make sure no color is set for the
    # shell's prompts.
    from atexit import register
    def Clean():
        print(C.normal(s=1), end="")
    register(Clean)

if 0 and __name__ == "__main__":
    # Simplistic repl
    class G: pass
    Fo = G()
    Fo.norm = f"{C.normal(s=1)}"
    Fo.grn = f"{C.fg(C.lgreen, s=1)}"
    Fo.red = f"{C.fg(C.lred, s=1)}"
    Fo.blu = f"{C.fg(C.lblue, s=1)}"
    Fo.yel = f"{C.fg(C.yellow, s=1)}"
    def success(s):
        return f"{Fo.grn}{s}{Fo.norm}"
    def failure(s):
        return f"{Fo.red}{s}{Fo.norm}"
    def info() -> None:
        print(f"\n{Fo.grn}Welcome to python nano-REPL")
        print(f"{Fo.blu}author: Amal Shaji")
        print(f"{Fo.blu}repo  : https://github.com/amalshaji/pyrepl")
        print(f"{Fo.yel}crtl-c to quit{Fo.norm}\n")
    def repl() -> None:
        info()
        try:
            while True:
                try:
                    _in = input("》 ")
                    if _in == "q":
                        exit()
                    try:
                        print(success(eval(_in)))
                    except:
                        out = exec(_in)
                        if out != None:
                            print(success(out))
                except Exception as e:
                    print(failure(f"Error: {e}"))
        except KeyboardInterrupt as e:
            exit()
    repl()
    exit()

if 0 and __name__ == "__main__":
    '''This version uses a simple loop. 
    '''
    def Execute(s, vars):
        if s.startswith("!"):
            Special(s[1:])
            return
        if "=" in s:    # Assignment
            exec(s, globals(), vars)
        else:
            try:
                s = eval(s, globals(), vars)
                print(s)
            except Exception as ee:
                # Try exec
                try:
                    exec(s, globals(), vars)
                except Exception as e:
                    print(f"{red}Exception: {e}{norm}")
    d = {}      # Options dictionary
    x, z = flt(pi), cpx(pi, 1/pi)
    z.i = True
    z.c = True
    args = ParseCommandLine(d)
    # Define some color escape codes
    red = C.fg(C.lred, s=1)
    cyn = C.fg(C.lcyan, s=1)
    norm = C.normal(s=1)
    # Note:  set sys.ps1 and sys.ps2 to the desired prompt strings
    # instead
    prompt = f"{cyn}》 "
    vars = {}
    s = input(prompt)
    print(norm, end="")
    while s != "q":
        Execute(s, vars)
        s = input(prompt)
        print(norm, end="")

if 0 and __name__ == "__main__": 
    def GetSymbols():
        'Return a dict of symbols I want'
        from u import u
        from pprint import pprint as pp
        from decimal import Decimal as D
        from pathlib import Path as P
        from fractions import Fraction as F
        x, z = flt(pi), cpx(pi, 1/pi)
        z.i = True
        z.c = True
        z.f = True
        return locals().copy()
    class Console(code.InteractiveConsole):
        def interact(self):
            v = sys.version_info
            ver = f"{v.major}.{v.minor}.{v.micro}"
            banner = dedent(f'''
            My REPL [python {ver}]
              Enter 'q' to quit or '.q' if q is a defined symbol
            '''[1:].rstrip())
            super(Console, self).interact(
                banner=banner,
                exitmsg=C.normal(s=1),
            )
        def raw_input(self, prompt=""):
            'Customize the prompt'
            cyn = C.fg(C.lcyan, s=1)
            if 1:
                prompt = f"{cyn}》 "
                s = input(prompt)
                print(C.normal(s=1), end="")
            else:
                s = input()
            if s == "q" and "q" not in self.locals:
                exit()
            # This shows how to add special commands that are trapped
            # before the interpreter gets them
            if s == ".q":
                exit()
            return s
    cyn = C.fg(C.lcyan, s=1)
    sys.ps1 = f"{cyn}》 "
    sys.ps2 = f"{cyn}... "
    console = Console(locals=GetSymbols())
    console.interact()

if 1 and __name__ == "__main__": 
    '''Use a code.InteractiveInterpreter object to get a REPL (read,
    evaluate, print, loop) construct, which is what the python
    interactive interpreter does).  This shows how to build your own
    REPl with custom commands.
    '''
    # Escape strings for color coding
    class G: pass   # Container for global variables
    g = G()
    g.cyn = C.fg(C.lcyan, s=1)
    g.err = C.fg(C.lmagenta, s=1)
    g.norm = C.normal(s=1)
    def GetSymbols():
        'Return a dict of symbols I want'
        from u import u
        from pprint import pprint as pp
        from decimal import Decimal as D
        from pathlib import Path as P
        from fractions import Fraction as F
        from uncertainties import ufloat as uf
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
        return locals().copy()
    def Special(s):
        assert s[0] == "."
        s = s[1:]
        if s == "cls" or s == "c":
            os.system("clear")
        elif s == "h":
            print(dedent(f'''
            Things in scope:
            u:  units      xx:  debug      pp:  pretty print
            D as Decimal, F as Fraction
            flt, cpx number types with math/cmath symbols:
                x and z as examples, use .h attributes for help
                Try sin(x) and sin(z)
            .c clears the screen
                '''[1:].rstrip()))
        else:
            print(f"{glerr}'{s}' not recognized as special command{norm}")
    class Console(code.InteractiveConsole):
        def start_message(self):
            v = sys.version_info
            ver = f"{v.major}.{v.minor}.{v.micro}"
            from util import Time
            print(dedent(f'''
            someonesdad's REPL [python {ver}] {Time()}
              Enter 'q' to quit or '.q' if q is a defined symbol
              Enter '.h' for help
            '''[1:].rstrip()))
        def write(self, data):
            'Generate an error message to stdout'
            print(f"{g.err}{data}{g.norm}", end="")
        def raw_input(self, prompt=""):
            'Customize the prompt'
            s = input(self.ps)
            print(g.norm, end="")
            # Handle special stuff before the interpreter sees it
            if s == "q" and "q" not in self.locals:
                exit()
            elif s and s[0] == ".":
                Special(s)
                return ""
            return s
    # Set up system prompts
    n = 3
    sys.ps1 = f"{'»'*n} "
    sys.ps2 = f"{'.'*n} "
    console = Console(locals=GetSymbols())
    console.ps = sys.ps1
    console.start_message()
    while True:
        try:
            line = console.raw_input()
        except EOFError:
            exit()
        while line and line[-1] == "\n":
            line = line[:-1]
        if not line:
            console.ps = sys.ps1
        # Handle special commands
        rv = console.push(line)
        if rv:
            # Need more input
            console.ps = sys.ps2
            continue
        else:
            console.ps = sys.ps1
