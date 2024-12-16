'''

Any arg, it turns into an interactive Ohm's Law calculator.  The goal is to help you understand
and select resistance values for given voltage, current, and power conditions.  The calculator's
state is saved in a file and it always starts where it left off, though you can reset the thing at
any time.

It will know EIA resistance values or the on-hand resistors.

A typical task is to be working with V, i, R and you'll want to clamp one of the values.  Then the
command would e.g. be 'cr' to clamp the resistance or (cp, cv, ci for power, voltage, resistance).
Then enter

    'i 12' or '12 mA' and you'd get the resulting  voltage.

Then you could enter 'i 12' and you'd get the resulting voltage.  The 'u' command lets you set the
working units.

Display

    V       i       R       P
    Displayed on one line.  Active value is in color.  Clamped values are underlined.

Commands

    'v 3'   Enter 3 volts
    '3 v'   Enter 3 volts
    c       Clamp the following variable v i r p (can clamp two out of 4)
            'cc v' means clear the clamped variable
    u       Unit for v i r p  'u v m' means mV
    w d=xxx l=xxx   Calculate resistance for copper wire
    t       Set temperature for copper wire calculations 
                't 44 f' or t 44 c'
    !t      Reset t to 20 °C
    m       Set wire material (you're prompted for supported material)
    !m      Reset wire to copper
    n 4     Set fix & number of digits
    e 4     Set eng & number of digits
    s 4     Set sci & number of digits
    o virp  Set the order of printing on result line

    Enter numbers
        3 v     Enter 3 V
        3 mv    Enter 3 mV
        3       Enter 3 of last entered unit
    After entering, the new values will be calculated and displayed

    reset   Set to default state   
    s       Show current settings and values
    ?       Show help
    > name  Save current state to given name
    < name  Recall saved state
    e       Edit current state in editor
    <cr>    Print current values

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
    class ZeroOrNegativeNotAllowed(Exception):
        'A variable must be > 0'
    class Model:
        def __init__(self):
            self._v = flt(1)
            self._i = flt(1)
            self._r = flt(1)
            self._p = flt(1)
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
            else:
                raise RuntimeError(f"Bug:  changed is {changed!r} which is unrecognized")
        if 1:   # Properties
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
