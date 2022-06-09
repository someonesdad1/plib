'''
Todo
    - Try changing to an MVC architecture; it may make more sense.
    - Allow the problem variables to have 1, 2, or 3 values, which lets you
      print a table.
    - Goals:  add -p and -m options to set profit goals.  When the goal is
      reached, the associated variable's column prints in green.
    - Colorizing
        - Show ∞ and errors in red
        - Green u or p when desired goal is reached
        - If no u goal specified, it will print in purl when >= 2

Interactive utility to calculate the profit of a project
 
    Problem variables
        c = cost 
        s = selling price
        p = profit as a fraction of s
        m = markup as a fraction of c
        u = multiplier = s/c

    Equations
        e0:  p(s, c) = (s - c)/s
        e1:  s(c, m) = c*(1 + m)
        e2:  c(s, p) = s*(1 - p)
        e3:  m(p)    = p/(1 - p)
        e4:  p(m)    = m/(1 + m)
        e5:  u(s, c) = s/c
        e6:  s(c, u) = u*c
        e7:  c(s, u) = s/u

        Other equations:
            u = 1/(1 - p) = 1 + m
            p = 1 - 1/u
            m = u - 1
 
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
        prompt = "mkup> "
        # Problem's variables
        c, s, p, m, u = [None]*5
        names = "c s p m u".split()
        # User's local variables
        vars = {}
        # Colors
        t.err = t("redl")
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
if 1:   # Classes
    class Model:
        "Financial model's code"
        def __init__(self):
            self.reset()
        def reset(self):
            self._c = None
            self._s = None
            self._p = None
            self._m = None
            self._u = None
            self._last_changed = None
            self._inf = float('inf')
            self._nan = float('nan')
        def getval(self, value):
            '''Return the indicated value.  If it is nan, return nan.  If
            it is float('inf'), return this.  Otherwise, convert it to a 
            flt instance.
            '''
            if isnan(value):
                return float(nan)
            elif value == self._inf:
                return self._inf
            elif value == -self._inf:
                return -self._inf
            else:
                return flt(value)
        def update(self):
            "Calculate the current model's values"
            if (self._c is not None and self._s is not None) and self._.last_changed is None:
                found_solution = True
                self._p = self.e0(); self._m = self.e3(); self._u = self.e5()    # Case 1
            elif (not self._c and not self._s) or self._last_changed is None:
                found_solution = False
            elif self._last_changed == "c":
                if self._s:     # Case 1
                    self._p = self.e0()
                    self._m = self.e3()
                    self._u = self.e5()
                elif self._m:   # Case 2
                    self._s = self.e1()
                    self._p = self.e4()
                    self._u = self.e5()
                elif self._p:   # Case 3
                    self._m = self.e3()
                    self._s = self.e1()
                    self._u = self.e5()
                elif self._u:   # Case 4
                    self._s = self.e6()
                    self._p = self.e0()
                    self._m = self.e3()
                else:
                    found_solution = False
            elif self._last_changed == "s":
                if self._c:     # Case 1
                    self._p = self.e0()
                    self._m = self.e3()
                    self._u = self.e5()
                elif self._m:   # Case 5
                    self._p = self.e4()
                    self._c = self.e2()
                    self._u = self.e6()
                elif self._p:   # Case 6
                    self._c = self.e2()
                    self._m = self.e3()
                    self._u = self.e6()
                elif self._u:   # Case 7
                    self._c = self.e7()
                    self._p = self.e0()
                    self._m = self.e3()
                else:
                    found_solution = False
            elif self._last_changed == "m":
                # Assume c is fixed
                self._s = self.e1()
                self._p = self.e4()
                self._u = self.e5()
            elif self._last_changed == "p":
                # Assume s is fixed
                self._m = self.e3()
                self._s = self.e1()
                self._u = self.e5()
            elif self._last_changed == "u":
                # Assume c is fixed
                self._s = self.e6()
                self._p = self.e0()
                self._m = self.e3()
            else:
                raise Exception(f"{self._last_changed!r} is bad value for self._last_changed")
        if 1:   # Functions for solution
            def e0(self): 
                try:
                    return flt((self._s - self._c)/self._s)
                except ZeroDivisionError:
                    return self._inf
            def e1(self):
                return flt(self._c*(1 + self._m))
            def e2(self):
                return flt(self._s*(1 - self._p))
            def e3(self):
                try:
                    return flt(self._p/(1 - self._p))
                except ZeroDivisionError:
                    return self._inf
            def e4(self): 
                try:
                    return flt(self._m/(1 + self._m))
                except ZeroDivisionError:
                    return self._inf
            def e5(self):
                try:
                    return flt(self._s/self._c)
                except ZeroDivisionError:
                    return self._inf
            def e6(self):
                return flt(self._u*self._c)
            def e7(self):
                try:
                    return flt(self._s/self._u)
                except ZeroDivisionError:
                    return self._inf
        if 1:   # Properties
            @property
            def c(self):
                return self._c
            @c.setter
            def c(self, value):
                self._c = self.getval(value)
                self._last_changed = "c"
            @property
            def s(self):
                return self._s
            @s.setter
            def s(self, value):
                self._s = self.getval(value)
                self._last_changed = "s"
            @property
            def p(self):
                return self._p
            @p.setter
            def p(self, value):
                self._p = self.getval(value)
                self._last_changed = "p"
            @property
            def m(self):
                return self._m
            @m.setter
            def m(self, value):
                self._m = self.getval(value)
                self._last_changed = "m"
            @property
            def u(self):
                return self._u
            @u.setter
            def u(self, value):
                self._u = self.getval(value)
                self._last_changed = "u"
    class View:
        '''Determines how the model's information is to be displayed.
        '''
        def __init__(self, model):
            self.model = model
        def __call__(self, width=None, n=1):
            '''Returns a suitably formatted line for the solution.  width is
            the desired width each field.  When width is None, then the basic
            string with no padding is returned.  Since the returned strings can
            contain escape sequences, using Len() on them is necessary.
            '''
            M, w = self.model, width
            c, s, p, m, u = M.c, M.s, M.p, M.m, M.u
            inf = float('inf')
            inft = "∞"
            # Generate the results string
            C = self.ToStr(c)
            S = self.ToStr(s)
            P = self.ToStr(p, pct=True)
            M = self.ToStr(m, pct=True)
            U = self.ToStr(u)
            # Get the output line
            out = (C, S, P, M, U))
            if not width:
                # Column width is the width of the widest member
                w = max(Len(i) for i in out)
            sp = " "*n
            for i, item in enumerate(out):
                out[i] = f"{sp}{item:^{w}s}{sp}"
            return ''.join(out)
        def header(self, width):
            'Return the table header'
        def Err(self, e):
            t.print(f"{t.err}Error:  {e}")
        def ToStr(self, val, pct=False):
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
    class Controller:
        '''Has a model and view instance.
        '''
        def __init__(self):
            self.model = Model()
            self.view = View(self.model)
            self.Loop()
        def Loop(self):
            while True:
                show_results = False
                s = input(prompt).strip()
                if s:
                    first_character = s[0]
                    remainder = s[1:] if len(s) > 1 else ""
                    if first_character == "q":
                        break
                    elif "=" in s:
                        # Local variable assignment
                        name, value = s.split("=", 1)
                        if name in names:
                            print("Cannot assign to primary variables")
                        else:
                            self.Variable(name, value)
                    elif first_character in "cspmu" or "=" in s:
                        if not remainder:
                            print("Must include a value")
                            continue
                        self.Variable(first_character, remainder)
                        show_results = True
                    else:
                        show_results = self.Command(s)
                    if show_results:
                        self.view.PrintSolution()
        def Variable(self, name, value):
            mdl = self.model
            vars = mdl.vars
            if name in "c s m p u".split():
                g.last_changed = name
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
                else:
                    u = flt(eval(value, globals(), vars))
                    if u < 0:
                        print("Absolute value for multiplier was used")
                        u = abs(u)
            else:
                try:
                    vars[name] = eval(value, globals(), vars)
                except Exception as e:
                    self.view.Err(e)
        def Command(self, x):
            'Return True if results should be printed'
            if x == ".":        # Show results again
                return True
            elif x == "..":     # Show defined variables
                self.PrintLocals(vars)
            elif x == "?":      # Help
                self.Help()
            elif x == "??":     # More detailed help
                self.DetailedHelp()
            elif x == "/":      # Reset problem variables
                self.Reset()
            elif x == "dbg":    # Toggle verbose mode
                g.dbg = not g.dbg
                print(f"Verbose turned {'on' if g.dbg else 'off'}")
            elif x.startswith("!"):     # Return an expression
                cmd = x[1:].strip()
                self.Expression(cmd)
            elif x == "reset":  # Reset variables to 0
                self.Reset()
                return True
            elif x.startswith(":"):     # Set number of significant figures
                try:
                    n = int(x[1:])
                    flt(0).n = min(15, max(1, n))
                    return True
                except Exception:
                    print("You must enter an integer between 1 and 15")
            return False
        def PrintLocals(self):
            vars = self.model.vars
            if not vars:
                return
            w = max(len(i) for i in vars)
            print("Local variables:")
            for i in vars:
                print(f"  {i:{w}s} = {vars[i]}")
        def Expression(self, cmd):
            try:
                print(exec(cmd, globals(), vars))
            except Exception as e:
                print(e)
        def DetailedHelp(self):
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
                S  C  P %  M %   U
                2  1  50   100  2
            The default number of significant figures shown is {sf}.  This means your
            answers will be to about {q}.
            '''))
        def Help(self):
            print(dedent(f'''
            v expr      Enter a problem variable where v is c, s, p, m, or u
            x = expr    Define a local variable named x
            q           Quit
            .           Show results again
            ..          Show defined variables
            : n         Set number of significant figures to n
            ! expr      Evaluate expression
            /           Reset to starting state
            ?           Commands
            ??          Help
            '''))
        def Reset(self):
            self.model.reset()

    a = Controller()
    breakpoint() #xx 
    exit()
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
            out = [["S", S], ["C", C], ["P,%", P], ["M,%", M], ["U", U]]
            # Format each column width to the width of the widest member
            # and with n spaces on either side
            n = 1
            for i, item in enumerate(out):
                cw = max(Len(j) for j in item)
                out[i] = [f"{' '*n}{j:^{cw}s}{' '*n}" for j in item]
            for i in Transpose(out):
                print(''.join(i))
    def PrintLocals(vars):
        if not vars:
            return
        w = max(len(i) for i in vars)
        print("Local variables:")
        for i in vars:
            print(f"  {i:{w}s} = {vars[i]}")
    def Variable(name, value):
        global c, s, m, p, u
        if name in "c s m p u".split():
            g.last_changed = name
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
            else:
                u = flt(eval(value, globals(), vars))
                if u < 0:
                    print("Absolute value for multiplier was used")
                    u = abs(u)
        else:
            try:
                vars[name] = eval(value, globals(), vars)
            except Exception as e:
                Err(e)
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
             S  C  P %  M %   U
             2  1  50   100  2
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
        /           Reset to starting state
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
        elif x == "..":     # Show defined variables
            PrintLocals(vars)
        elif x == "?":      # Help
            Help()
        elif x == "??":     # More detailed help
            DetailedHelp()
        elif x == "/":      # Reset problem variables
            Reset()
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
                return True
            except Exception:
                print("You must enter an integer between 1 and 15")
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
                elif "=" in s:
                    # Local variable assignment
                    name, value = s.split("=", 1)
                    if name in names:
                        print("Cannot assign to primary variables")
                    else:
                        Variable(name, value)
                elif first_character in "cspmu" or "=" in s:
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
# vim: tw=100
