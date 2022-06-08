'''

To Do
    - Each variable will be None, an expression string, int, or flt
    - Once basics are working

Interactive utility to calculate the profit of a project

    Basic operation
        - Program starts with all variables set to 0
        - You enter cost by a command such as 'c3'.  You can use
          expressions too, such as 'c 33*1.25'.
        - You can define local variables with 'x = expr'.  This works for
          any x that's not one of the basic names of 'c s p m u'.
        - As soon as the problem can be solved, you'll see the solution.
        - Enter a changed variable to see a new solution.
        - The state is remembered on exit.

    Commands
        x expr      Enter a variable where x is a variable name
        v = expr    Define a local variable
        q           Quit
        .           Show defined variables
        ! expr      Evaluate expression
        clr         Reset to starting state
 
    Problem variables
        c = cost 
        s = selling price
        p = profit as a fraction of s
        m = markup as a fraction of c
        u = multiplier = s/c

    Equations
        e0:  p = (s - c)/s
        e1:  s = c*(1 + m)
        e2:  c = s*(1 - p)
        e3:  m = p/(1 - p)
        e4:  p = m/(1 + m)
        e5:  u = s/c
        e6:  s = u*c
        e7:  c = s/u
 
    Solutions
        To solve the problem, you must have either c or s and one of any of
        the other variables.

        Case    Have   Need       Solution
        ----    ----   ----       --------
        1     c s    p m u      p = e0, m = e3, u = e5
        2     c m    s p u      s = e1, p = e4, u = e5
        3     c p    m s u      m = e3, s = e1, u = e5
        4     c u    s p m      s = e6, p = e0, m = e3

        5     s m    p c u      p = e4, c = e2, u = e6
        6     s p    c m u      c = e2, m = e3, u = e6
        7     s u    c p m      c = e7, p = e0, m = e3
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        from pprint import pprint as pp
        import sys
        import readline         # History and command editing
        import rlcompleter      # Command completion
    # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from f import *
    # Global variables
        ii = isinstance
        class g: pass
        g.dbg = False
        g.w = int(os.environ.get("COLUMNS", "80")) - 1
        g.last_changed = None
        prompt = ">> "
        # Problem's variables
        c, s, p, m, u = [0]*5
        # User's local variables
        vars = {}
        # Hold solution strings
        class sol: pass
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Need to write Usage statement
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False
        d["-n"] = 3         # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "dn:h", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("d"):
                d[o] = not d[o]
            elif o in ("-n",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        global dbg
        dbg = d["-d"]
        x = flt(0)
        x.n = d["-n"]
        x.rtz = x.rtdp = True
        return args
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.n}", end="")
    def Err(e):
        t.print(f"{t.err}Error:  {e}")
if 1:   # Command loop
    def PrintSolution():
        global c, s, p, m, u
        notyet = "-"
        def NotYet():
            sol.c = str(c) if c else notyet
            sol.s = str(s) if s else notyet
            sol.m = f"{100*m}%" if m else notyet
            sol.p = f"{100*p}%" if p else notyet
            sol.u = str(u) if u else notyet
        def e0(): return (s - c)/s
        def e1(): return c*(1 + m)
        def e2(): return s*(1 - p)
        def e3(): return p/(1 - p)
        def e4(): return m/(1 + m)
        def e5(): return u/c
        def e6(): return u*c
        def e7(): return s/u
        # Get the solution strings
        if (not c and not s) or g.last_changed is None:
            NotYet()
        elif g.last_changed == "c":
            if s:
                p, m, u = e0(), e3(), e5()
            elif m:
                s, p, u = e1(), e4(), e5()
            elif p:
                m, s, u = e3(), e1(), e5()
            elif u:
                s, p, m = e6(), e0(), e3()
            else:
                NotYet()
        elif g.last_changed == "s":
            if c:
                p, m, u = e0(), e3(), e5()
            elif m:
                p, c, u = e4(), e2(), e6()
            elif p:
                c, m, u = e2(), e3(), e6()
            elif u:
                c, p, m = e7(), e0(), e3()
            else:
                NotYet()
        elif g.last_changed == "m":
            # Assume c is fixed
            s, p, u = e1(), e4(), e5()
        elif g.last_changed == "p":
            # Assume s is fixed
            m, s, u = e3(), e1(), e5()
        elif g.last_changed == "u":
            # Assume c is fixed
            s, p, m = e6(), e0(), e3()
        else:
            raise Exception(f"{g.last_changed!r} is bad value for g.last_changed")

        # Print the results
        ncols = 5
        w = g.w//ncols
        out, ln = [], []
        # Title line
        for i in "Sell Cost Profit Markup Mult".split():
            ln.append(f"{i:^{w}s}")
        out.append(''.join(ln))

        print(dedent(f'''
        Cost    SellingPrice   Profit    Markup     Multiplier
        cost = {c}    selling price = {s}
        profit {pr}    markup {mr}       multiplier {u}
        '''))
    def Variable(name, value):
        global c, s, m, p, u
        class Oops(Exception): pass
        try:
            if name == "c":
                c = flt(eval(value, globals(), vars))
            elif name == "s":
                s = flt(eval(value, globals(), vars))
            elif name == "m":
                m = flt(eval(value, globals(), vars))
            elif name == "p":
                p = flt(eval(value, globals(), vars))
            elif name == "u":
                u = flt(eval(value, globals(), vars))
            else:
                raise Oops("Programming bug")
        except Oops:
            raise
        except Exception as e:
            print(f"{e}")
        g.last_changed = name
        if dbg:
            print("    c =", c)
            print("    s =", s)
            print("    m =", m)
            print("    p =", p)
            print("    u =", u)
    def Command(s):
        if s == "ls":
            ShowState()
        elif s == "dbg":
            ToggleDbg()
        elif s.startswith("!"):
            cmd = s[1:].strip()
            ExecutePythonCommand(cmd)
    def CommandLoop():
        while True:
            s = input(prompt).strip()
            if s:
                first_character = s[0]
                remainder = s[1:] if len(s) > 1 else ""
                if first_character == "q":
                    break
                elif first_character in "cspmu":
                    if not remainder:
                        print("Must include a value")
                        continue
                    Variable(first_character, remainder)
                else:
                    Command(s)
                PrintSolution()
if 1:
    dbg = 1
    c = 1 
    Variable("s", "sqrt(2)**2")
    PrintSolution()
    exit()

if __name__ == "__main__":
    d = {}          # Options dictionary
    args = ParseCommandLine(d)
    CommandLoop()
