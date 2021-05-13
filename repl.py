'''

A REPL I use for an interactive python calculator.  See repl.pdf for
documentation.
'''
 
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
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
    import color as C
    if 0:
        import debug
        debug.SetDebugger()  # Start debugger on unhandled exception
if 1:   # Global variables
    # Escape strings for color coding
    class G: pass   # Container for global variables
    g = G()
    g.cyn = C.fg(C.lcyan, s=1)
    g.err = C.fg(C.lmagenta, s=1)
    g.norm = C.normal(s=1)
if 1:   # Core functionality
    def Clean():
        'Register a cleanup function to ensure no color for shell'
        print(C.normal(s=1), end="")
    register(Clean)

if __name__ == "__main__": 
    '''Use a code.InteractiveInterpreter object to get a REPL (read,
    evaluate, print, loop) construct, which is what the python
    interactive interpreter does).  This shows how to build your own
    REPl with custom commands.
    '''
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
        d2r = pi/180
        r2d = 1/d2r
        x, z = flt(pi/7), cpx(pi/7, 7/pi)
        z.i = True
        z.c = True
        z.f = True
        return locals().copy()
    def Special(s):
        assert s[0] == "."
        s = s[1:]
        if not s:
            return
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
            d2r converts radian to degrees; r2d is the reciprocal
            .c clears the screen
                '''[1:].rstrip()))
        else:
            print(f"{g.err}'{s}' not recognized as special command{g.norm}")
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
