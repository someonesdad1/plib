'''
Todo
    - Allow the variables to have 1, 2, or 3 values entered, which lets you
      print a table.  Very handy to see the effects of a change.
        - 2 numbers:  start and end with default increment of 1
        - 3 numbers:  start and end with increment 

Interactive utility to calculate the profit of a project
 
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
          1     c s    p m u      p = e0(); m = e3(); u = e5()
          2     c m    s p u      s = e1(); p = e4(); u = e5()
          3     c p    m s u      m = e3(); s = e1(); u = e5()
          4     c u    s p m      s = e6(); p = e0(); m = e3()
          5     s m    p c u      p = e4(); c = e2(); u = e6()
          6     s p    c m u      c = e2(); m = e3(); u = e6()
          7     s u    c p m      c = e7(); p = e0(); m = e3()
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
        from transpose import Transpose
        from dpstr import Len
    # Global variables
        ii = isinstance
        inf = float('inf')
        infs = "∞" 
        sf = 2  # Default number of significant figures
        class g: pass
        g.dbg = False
        g.w = int(os.environ.get("COLUMNS", "80")) - 1
        g.last_changed = None
        prompt = ">> "
        # Problem's variables
        c, s, p, m, u = [None]*5
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
        d["-d"] = sf        # Number of significant digits
        d["-v"] = False     # Verbose/debug printing
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:hv") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("v"):
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
            elif o in ("-h", "--help"):
                Usage(status=0)
        g.dbg = d["-v"]
        if 1:   # Set up flt characteristics
            x = flt(0)
            x.n = d["-d"]
            x.rtz = x.rtdp = True
            # Where to switch to scientific notation
            x.high, x.low = 1e3, 1e-3
        return args
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.n}", end="")
    def Err(e):
        t.print(f"{t.err}Error:  {e}")
if 1:   # Command loop
    def ToStr(val, pct=False):
        'Always return a string suitable for display'
        if val is not None:
            if val == inf or isnan(val):
                return infs
            else:
                try:
                    return str(100*val) if pct else str(val)
                except Exception:
                    breakpoint() #xx
        else:
            return "-"
    def PrintSolution():
        global c, s, p, m, u
        inf = float('inf')
        inft = "∞"
        w = g.w//5  # Width of each column to fill screen
        found_solution = True
        def Prt(seq):
            print(''.join(f"{i:^{w}s}" for i in seq))
        if 1:   # Functions for solution
            def e0(): 
                try:
                    return flt((s - c)/s)
                except ZeroDivisionError:
                    return inf
            def e1():
                return flt(c*(1 + m))
            def e2():
                return flt(s*(1 - p))
            def e3():
                try:
                    return flt(p/(1 - p))
                except ZeroDivisionError:
                    return inf
            def e4(): 
                try:
                    return flt(m/(1 + m))
                except ZeroDivisionError:
                    return inf
            def e5():
                try:
                    return flt(s/c)
                except ZeroDivisionError:
                    return inf
            def e6():
                return flt(u*c)
            def e7():
                try:
                    return flt(s/u)
                except ZeroDivisionError:
                    return inf
        if 1:   # Calculate solution
            if (c is not None and s is not None) and g.last_changed is None:
                found_solution = True
                p = e0(); m = e3(); u = e5()    # Case 1
            elif (not c and not s) or g.last_changed is None:
                found_solution = False
            elif g.last_changed == "c":
                if s:   
                    p = e0(); m = e3(); u = e5()    # Case 1
                elif m: 
                    s = e1(); p = e4(); u = e5()    # Case 2
                elif p:
                    m = e3(); s = e1(); u = e5()    # Case 3
                elif u:
                    s = e6(); p = e0(); m = e3()    # Case 4
                else:
                    found_solution = False
            elif g.last_changed == "s":
                if c:
                    p = e0(); m = e3(); u = e5()    # Case 1
                elif m:
                    p = e4(); c = e2(); u = e6()    # Case 5
                elif p:
                    c = e2(); m = e3(); u = e6()    # Case 6
                elif u:
                    c = e7(); p = e0(); m = e3()    # Case 7
                else:
                    found_solution = False
            elif g.last_changed == "m":
                # Assume c is fixed
                s = e1(); p = e4(); u = e5()
            elif g.last_changed == "p":
                # Assume s is fixed
                m = e3(); s = e1(); u = e5()
            elif g.last_changed == "u":
                # Assume c is fixed
                s = e6(); p = e0(); m = e3()
            else:
                raise Exception(f"{g.last_changed!r} is bad value for g.last_changed")
        if 1:   # Print the results
            C = ToStr(c)
            S = ToStr(s)
            P = ToStr(p, pct=True)
            M = ToStr(m, pct=True)
            U = ToStr(u)
            # Construct each column of the table
            out = [["S", S], ["C", C], ["P%", P], ["M%", M], ["U", U]]
            # Format each column width to the width of the widest member
            # and with n spaces on either side
            n = 1
            for i, item in enumerate(out):
                cw = max(Len(j) for j in item)
                out[i] = [f"{' '*n}{j:^{cw}s}{' '*n}" for j in item]
            for i in Transpose(out):
                print(''.join(i))
    def Variable(name, value):
        global c, s, m, p, u
        class Oops(Exception): pass
        try:
            if name == "c":
                c = flt(eval(value, globals(), vars))
                if c < 0:
                    print("Absolute value for cost was used")
                    c = abs(c)
            elif name == "s":
                s = flt(eval(value, globals(), vars))
                if s < 0:
                    print("Absolute value for selling price was used")
                    s = abs(s)
            elif name == "m":
                m = flt(eval(value, globals(), vars))
                m /= 100    # Convert from % to fraction
            elif name == "p":
                p = flt(eval(value, globals(), vars))
                p /= 100    # Convert from % to fraction
            elif name == "u":
                u = flt(eval(value, globals(), vars))
                if u < 0:
                    print("Absolute value for multiplier was used")
                    u = abs(u)
            else:
                raise Oops("Programming bug")
        except Oops:
            raise
        except Exception as e:
            print(f"{e}")
        g.last_changed = name
    def Expression(cmd):
        try:
            print(exec(cmd, globals(), vars))
        except Exception as e:
            print(e)
    def DetailedHelp():
        p = flt(10**(2 - sf))
        with p:
            p.n = 1
            q = f"{p}%"
        print(dedent(f'''
                        Cost/selling price calculator
        Variables and equations
            c = cost
            s = selling price
            p = profit in % based on selling price
              = 100*(s - c)/s
            m = markup in % based on cost
              = 100*(s - c)/m
            u = multiplier
              = s/c
        Example:  
            Type the following commands followed by the Enter key:
                c1
                s2
            You'll get the result
             S  C  P%  M%   U
             2  1  50  100  2
        The default number of significant figures shown is {sf}.  This means your
        answers will be to about {q}.
        '''))
    def Help():
        print(dedent(f'''
        v expr      Enter a problem variable where v is c, s, p, m, or u
        x = expr    Define a local variable named x
        q           Quit
        .           Show results again
        ..          Show defined variables
        : n         Set number of significant figures to n
        ! expr      Evaluate expression
        clr         Reset to starting state
        ?           Commands
        ??          Help
        '''))
    def Reset():
        global c, s, p, m, u
        c, s, p, m, u = [None]*5
    def Command(x):
        'Return True if results should be printed'
        if x == ".":        # Show results again
            return True
        elif x == "?":      # Help
            Help()
        elif x == "??":     # More detailed help
            DetailedHelp()
        elif x == "..":     # Show defined variables
            if vars:
                pp(vars)
        elif x == "dbg":    # Toggle verbose mode
            g.dbg = not g.dbg
            print(f"Verbose turned {'on' if g.dbg else 'off'}")
        elif x.startswith("!"):     # Return an expression
            cmd = x[1:].strip()
            Expression(cmd)
        elif x == "reset":  # Reset variables to 0
            Reset()
            return True
        elif x.startswith(":"):     # Set number of significant figures
            try:
                n = int(x[1:])
                flt(0).n = min(15, max(1, n))
            except Exception:
                print("You must enter an integer between 1 and 15")
            return True
        return False
    def CommandLoop():
        while True:
            show_results = False
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
                    show_results = True
                else:
                    show_results = Command(s)
                if show_results:
                    PrintSolution()

if __name__ == "__main__":
    d = {}          # Options dictionary
    args = ParseCommandLine(d)
    if 1:   # Start with testing example
        c = 2500
        s = 6500
    CommandLoop()
