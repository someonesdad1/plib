'''

Any arg, it turns into an interactive Ohm's Law calculator.  The goal is to help you understand
and select resistance values for given voltage, current, and power conditions.  The calculator's
state is saved in a file and it always starts where it left off, though you can reset the thing at
any time.

It will know EIA resistance values or the on-hand resistors.

Commands

    Numbers must be entered with units.  Entering '2w' is interpreted as '2 W', so is entered as a
    power.  SI prefixes are allowed.  Power can also be entered as 'p 2', in which case it's
    interpreted in the default power unit, which is W.  'p 2u' would let you enter 2 microwatts.
    '2 o' and '2 r' are both interpreted as 2 Ω.

    A number can be entered without a unit.  It is interpreted as the last type of number entered.
    Thus, if you enter '2w', then the last number entered was a power.  Entering '3' without a
    unit implies another power in W.  

Starting state

    The calculator remembers its state.  However, starting up for the first time or just
    after being reset, all values will be 1.

    The data file that stores state is ohm.state.  This will be read to set the current state.
    There is no locking and multiple processes can cause a race condition.  You can read the state
    from a saved state 'mine' with '<mine' (or save it as '>mine').  These saved states can be
    used for particular problems.

Numbers

    Internally, all numbers used in calculations are floats.  Expressions are allowed and the math
    module's symbols are in scope.  For display, the flt type is used to give the desired number
    of digits.

Units
    
    Units are base SI units of V, A, W, Ω and the following SI prefixes are allowed: m μ u n p f a
    z y r q k M G T P E Z Y R Q.

Clamping

    A common scenario is that you want to limit the calculated values to e.g. utilize the 2 W
    resistors you have.  Clamping power with the command '2w; cp' means power is clamped to 2 W.
    Further calculations will not proceed unless the power stays at 2 W.  

    You can let the power be < 2 W with the command '2w; c<p', which means the calculated power
    must be less than 2 W.  'c>p' works similarly.

    Remove clamping with 'C'.

    Example:  you want to use your on-hand resistors which are 1/4, 1/2, and 2 W types.  Use
    '2c<=p' to ensure subsequent calculations succeed only if the power is < 2 W.

A typical task is to be working with V, i, R and you'll want to clamp one of the values.  Then the
command would e.g. be 'cr' to clamp the resistance or (cp, cv, ci for power, voltage, resistance).
Then enter

    'i 12' or '12 mA' and you'd get the resulting  voltage.

Then you could enter 'i 12' and you'd get the resulting voltage.  The 'u' command lets you set the
working units.

Display

    V       i       R       P
    Displayed on one line.  Active value is in color.  Clamped values are underlined.

You can have one clamped value.  This value constrains the calculations when you enter new
numbers, as the calculations must have the result that's less than or equal to the clamped value.
For example, you might enter a power of 2 W, as you want to use your 1/4 W, 1/2 W, or 2 W
resistors.  When a variable is clamped, newly entered values may cause an impossible situation, so
you'll get an error message.

Command syntax

Commands (x is one of v i r p)

    Commands are separated by semicolons
    Use " characters to e.g. let a state name contain a space
        > "my name"

    Enter a physical number (they are identified by their SI unit)
        '3mv'   Enter 3 millivolts
        '3v'    Enter 3 volts
        '3 v'   Enter 3 volts
        'v3'    Enter a voltage in default voltage units
        'v 3'   Enter a voltage in default voltage units
        'v3m'   Enter a voltage in mV, overriding default units
        'v 3m'  Enter a voltage in mV, overriding default units
        'v 3 m' Enter a voltage in mV, overriding default units
    Enter a physical number with implied units
        '3'     Contains same units as last physical number entered.  This results in a
                re-calculation of the results and allows for faster numerical exploration.
    Clamping
        cx      Clamp the indicated variable to its current value
        c<x     Clamp the indicated variable to less than its current value
        c<=x    Clamp the indicated variable to less than or equal to its current value
        c>x     Clamp the indicated variable to greater than its current value
        c>=x    Clamp the indicated variable to greater than or equal to its current value
        uc      Unclamp

    u       Set a default unit.  'umv' sets voltage units to mV.
    U       Clear all defined units back to base SI

    Wire calculations (round and rectangular cross section)
        W(n=X, d=X, a=X, b=X, l=X, t=X, m=X)
            d=dia, a&b are width & height, l=length, t=temp, m=material, n=AWG
        W by itself shows help for the W command

    Configuration
        C(n=X, f, e, s, si)
            n is number of digits
            f/e/s/si means used fixed, eng, sci, SI
        C by itself shows help for the C command

    Enter numbers
        3 v     Enter 3 V
        3 mv    Enter 3 mV
        3       Enter 3 of last entered unit
    After entering, the new values will be calculated and displayed

    reset   Set to default state   
    s       Show current settings and values
    ?       Show help
    ??      Dump persisted state information
    save name       Save state to given name
    restore name    Recall saved state
    num >x  Store number in a named register x (register namespace local to state)
    <x      Recall number in a named register x
    ro x    Toggle read-only state of register x
    e       Edit current state in editor
    .       Print current values
    .n      Show current values with n more significant figures
            .. == .1
            ... == .2
            etc.
    =       Show on-hand resistors that meet constraints/values

Have        Use
V, i        R = V/i, P = V*i
V, R        i = V/R, P = V**2/R
V, P        i = P/V, R = V**2/P
i, R        V = i*r, P = i**2*R
i, P        V = P/i, R = P/i**2
R, P        V = sqrt(P*R), i = sqrt(P/R)

'''
 
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
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
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:   # Classes
    '''
    The basic architecture is MVC.
    '''
    class ZeroOrNegativeNotAllowed(Exception):
        'A variable must be > 0'
    class Model:
        def __init__(self):
            self._v = flt(1)
            self._i = flt(1)
            self._r = flt(1)
            self._p = flt(1)
            self._clamped = None
        def update(self, changed):
            'Update the other variables after the variable in changed was modified'
            if changed == "v":
                self._i = self._v/self._r
            elif changed == "i":
                pass
            elif changed == "r":
                pass
            elif changed == "p":
                pass
            elif changed == "clamped":
                pass
            else:
                raise RuntimeError(f"Bug:  changed is {changed!r} which is unrecognized")
        if 1:   # Properties
            @property
            def clamped(self):
                return self._clamped
            @clamped.setter
            def clamped(self, value):
                if not ii(value, str) and len(str) not in (0, 1):
                    raise TypeError(f"value must be a single character string or empty")
                value = value.lower().strip()
                if value and value not in "virp":
                    raise ValueError(f"value must be empty or one of 'v', 'i', 'r', or 'p'")
                self._clamped = value
                self.update("clamped")
            @property
            def v(self):
                return self._v
            @v.setter
            def v(self, value):
                x = flt(value)
                if x <= 0:
                    raise ZeroOrNegativeNotAllowed(f"Value for V = {value!r}")
                self._v = x
                self.update("v")
            @property
            def i(self):
                return self._i
            @i.setter
            def i(self, value):
                x = flt(value)
                if x <= 0:
                    raise ZeroOrNegativeNotAllowed(f"Value for i = {value!r}")
                self._i = x
                self.update("i")
            @property
            def r(self):
                return self._r
            @r.setter
            def r(self, value):
                x = flt(value)
                if x <= 0:
                    raise ZeroOrNegativeNotAllowed(f"Value for R = {value!r}")
                self._r = x
                self.update("r")
            @property
            def p(self):
                return self._p
            @p.setter
            def p(self, value):
                x = flt(value)
                if x <= 0:
                    raise ZeroOrNegativeNotAllowed(f"Value for P = {value!r}")
                self._p = x
                self.update("p")
    class View:
        def __init__(self):
            pass
    class Controller:
        def __init__(self):
            pass
if 1:   # Utility
    def GetColors():
        t.err = t("redl")
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Need description
        d["-d"] = 3         # Number of significant digits
        #if len(sys.argv) < 2:
        #    Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h") 
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
            elif o == "-h":
                Usage()
        return args
if 1:   # Core functionality
    def ShowEquations():
        print(dedent(f'''
            V = i*R = P/i  = sqrt(P*R)
            i = V/R = P/V  = sqrt(P/R)
            R = V/i = V²/P = P/i²
            P = V*i = i²*R = V²/R
        '''))

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    ShowEquations()
