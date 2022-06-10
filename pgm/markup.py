'''
Todo

    - Note:  this has become overly complicated.  Consider a) leaving out
      u, as it's the same as m + 1 and then there are just 4 variables; b)
      removing the sequence behavior (if you need it, write a script).  I
      would like to see the model's values and locals persisted to a file
      (~/.mrkup.rc).  Then the problem has a solution if you have two
      variables and one of them is s or c.  
        - Actually, the current code should be simplified this way, as if
          you enter u, it means you've really just entered m.  

    - c=1, s=-0.1, get p=1100%.  The math is correct from (s-c)s, but this
      will be confusing to folks.  One option is to raise an exception when
      a negative number is entered if no_negative is True or just take the
      absolute value.
    - Set s=2, m=200, get problem in Model.update at line 223 because it
      assumes c is fixed.  There has to be a check to make sure both
      s and c are defined; if only onem then use it.
    - Get seq working
    - Regular prints should be delegated to View instance
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
        from pdb import set_trace as xx 
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
        sf = 3  # Default number of significant figures
        class g: pass
        g.dbg = False
        g.w = int(os.environ.get("COLUMNS", "80")) - 1
        g.last_changed = None
        prompt = "mkup> "
        # Problem's variables
        c, s, p, m, u = [None]*5
        names = set("c s p m u".split())
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
    class BadNumberOfExpressions(Exception): pass
    class Model:
        "Financial model's code"
        def __init__(self):
            x = flt(0)
            x.n = 3
            x.rtz = x.rtdp = True
            self.reset()
            self.vars = {}
        def __str__(self):
            return (f"Model(c={self._c}, s={self._s}, p={self._p}, "
                    f"m={self._m}, u={self._u})")
        def __repr__(self):
            return str(self)
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
            if (self._c is not None and self._s is not None) and self._last_changed is None:
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
            # The following number is added to flt.n to get the width of
            # a column.  The offset allows for the decimal point and
            # switching to scientific notation.
            self.width_offset = 7
            self.column_width = flt(0).n + self.width_offset
        def __call__(self, n=1, width=None, hdr=False):
            '''Prints a formatted line for the model's solution.
              n         Number of spaces to print between columns
              width     Width of each column (overrides self.column_width)
              hdr       Print header if True
            '''
            mdl = self.model
            # Generate the results string
            C = self.ToStr(mdl.c)
            S = self.ToStr(mdl.s)
            P = self.ToStr(mdl.p, pct=True)
            M = self.ToStr(mdl.m, pct=True)
            U = self.ToStr(mdl.u)
            results = [S, C, P, M, U]
            w = width if width else self.column_width
            sp = " "*n
            if hdr:
                out = "S C P M U".split()
                for i, item in enumerate(out):
                    out[i] = f"{sp}{item:^{w}s}{sp}"
                print(''.join(out))
            for i, item in enumerate(results):
                results[i] = f"{sp}{item:^{w}s}{sp}"
            print(''.join(results))
        def Err(self, e):
            t.print(f"{t.err}Error:  {e}")
        def ToStr(self, val, pct=False):
            '''Return a string suitable for display.  If pct is True,
            display as an integer percent.
            '''
            if val is None:
                return "-"
            if val == float('inf'):
                return "∞"
            elif val == -float('inf'):
                return "-∞"
            elif isnan(val):
                return "nan"
            else:
                try:
                    return str(flt(round(100*val, 0))) + "%" if pct else str(val)
                except Exception as e:
                    t.print(f"{t('lip')}Unexpected exception!")
                    t.print(f"{t('lip')}  {e}")
                    breakpoint() #xx
    class Controller:
        'Has a model and view instance'
        def __init__(self):
            self.model = Model()
            self.view = View(self.model)
            self.Loop()
        def EvalModelVariable(self, name, value):
            'Evaluate model variable (one of c s m p u)'
            assert(name in names)
            assert(ii(value, flt))
            m = self.model
            m._last_changed = name
            # Set to True to disallows some negative numbers
            no_negative = False
            if name == "c":
                m.c = value
                if no_negative:
                    if m.c < 0:
                        print("Absolute value for cost was used")
                        m.c = abs(m.c)
            elif name == "s":
                m.s = value
                if no_negative:
                    if m.s < 0:
                        print("Absolute value for selling price was used")
                        m.s = abs(m.s)
            elif name == "m":
                m.m = value
                m.m /= 100    # Convert from % to fraction
            elif name == "p":
                m.p = value
                m.p /= 100    # Convert from % to fraction
            else:
                m.u = value
                if no_negative:
                    if m.u < 0:
                        print("Absolute value for multiplier was used")
                        m.u = abs(m.u)
        def PrintLocals(self, vars):
            if not vars:
                print("No local variables")
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
            print(dedent(f'''
                            Cost/selling price calculator
            Variables
                c = cost
                s = selling price
                p = profit in % based on selling price
                  = 100*(s - c)/s
                m = markup in % based on cost
                  = 100*(s - c)/m
                u = multiplier
                  = s/c
            Equations
                c = s*(1 - p)       c = s/u
                s = c*(1 + m)       s = u*c
                p = (s - c)/s       p = 1 - 1/u         p = m/(1 + m)
                m = p/(1 - p)       m = u - 1
                u = s/c             u = 1/(1 - p)       u = 1 + m
            Example:  
                Type the following commands followed by the Enter key:
                    c1
                    s2
                You'll get the result
                     S           C           P           M           U
                     2           1          50%         100%         2
            The percentages P and M are only shown to two signicant
            figures.
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
        def Command(self, x):
            'Return True if results should be printed'
            if x == ".":        # Show results again
                return True
            elif x == "..":     # Show defined variables
                self.PrintLocals(self.model.vars)
            elif x == "?":      # Help
                self.Help()
            elif x == "??":     # More detailed help
                self.DetailedHelp()
            elif x == "/":      # Reset problem variables
                self.Reset()
            elif x == "dbg":    # Toggle verbose mode
                g.dbg = not g.dbg
                print(f"Verbose turned {'on' if g.dbg else 'off'}")
            elif x[0] == "!":   # Return an expression
                cmd = x[1:].strip()
                self.Expression(cmd)
            elif x == "reset":  # Reset variables to 0
                self.Reset()
                return True
            elif x[0] == "n":  # Set the number of significant digits
                try:
                    n = int(x[1:])
                    if not (1 <= n <= 15):
                        print("Must be between 1 and 15")
                        return False
                    flt(0).n = n
                    return True
                except Exception:
                    print(f"{x!r} is not a proper integer")
                    return False
            elif x.startswith(":"):     # Set number of significant figures
                try:
                    n = int(x[1:])
                    flt(0).n = min(15, max(1, n))
                    return True
                except Exception:
                    print("You must enter an integer between 1 and 15")
            else:
                print(f"{x!r} is not a valid command")
            return False
        def Variable(self, name: str, value: str):
            '''name contains a financial variable name and value this
            variable's value.  Return either None or a sequence of strings.
            name can also be the name of a local variable to assign to.
 
            value is a string that can be 1 to 3 expressions separated by
            whitespace.  With one expression, evaluate the variable and
            return None.  
 
            With two or three, return a sequence of other 
            values to evaluate at; this lets the user get table.  With
            2 expressions, the interval is 1.  With three, the numbers
            are start, stop, and step.  The last value of stop is always
            included in the sequence unlike range().
            '''
            vars = self.model.vars
            if name in names:
                # See if value is more than one expression
                values = value.split()
                seq, start, stop, step = None, None, None, None
                if len(values) not in (1, 2, 3):
                    raise BadNumberOfExpressions("Must have 1 to 3 expressions")
                start = flt(eval(values[0], globals(), vars))
                if len(values) > 1:
                    stop = flt(eval(values[1], globals(), vars))
                    step = flt(1)
                if len(values) == 3:
                    step = flt(eval(values[2], globals(), vars))
                if len(values) > 1:     # Get sequence
                    e = ValueError
                    if stop < start:
                        raise e("stop is less than start")
                    if step <= 0:
                        raise e("step must be greater than zero")
                    elif stop == start:
                        pass     # Single sequence already in model instance
                    else:
                        n = (stop - start)/step
                        if n > 1:
                            # Start with next element from start, as start
                            # is already in model instance
                            seq = [start + step]
                            while seq[-1] + step <= stop:
                                seq.append(seq[-1] + step)
                self.EvalModelVariable(name, start)
                return [str(i) for i in seq] if seq else None
            else:
                # Evaluate as a local variable
                try:
                    self.model.vars[name] = eval(value, globals(), vars)
                except Exception as e:
                    self.view.Err(e)
        def Loop(self):
            if 0:   # xx debug testing
                self.model._c = flt(112.8)
                self.model._s = flt(200.1)
                self.model._last_changed = "s"
                self.model.update()
 
            while True:
                show, seq = False, []
                s = input(prompt).strip()
                if not s:
                    continue
                first_character = s[0]
                remainder = s[1:] if len(s) > 1 else ""
                if first_character == "q":
                    break
                elif "=" in s: # Local variable assignment
                    name, value = s.split("=", 1)
                    if name in names:
                        print("Cannot assign to primary variables")
                    else:
                        self.Variable(name, value)
                elif first_character in names: # Financial variable assignment
                    if not remainder:
                        print("Must include a value")
                        continue
                    try:
                        seq = self.Variable(first_character, remainder)
                        self.model.update()
                    except Exception as e:
                        print(e)
                        continue
                    show = True
                else:   # It must be a command
                    show = self.Command(s)
                if show:    # Print the output
                    self.view(hdr=True)
                    if seq:
                        breakpoint() #xx

    if 1: #xx
        a = Controller()
        exit()

if 0:   # Command loop #xx
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
    def Variable(name, value):
        global c, s, m, p, u
        if name in "c s m p u".split():
            g.last_changed = name
            if name == "c":
                c = flt(eval(value, globals(), vars))
                if 0:  # Enable to disallow negative numbers
                    if c < 0:
                        print("Absolute value for cost was used")
                        c = abs(c)
            elif name == "s":
                s = flt(eval(value, globals(), vars))
                if 0:  # Enable to disallow negative numbers
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
                if 0:  # Enable to disallow negative numbers
                    if u < 0:
                        print("Absolute value for multiplier was used")
                        u = abs(u)
        else:
            try:
                vars[name] = eval(value, globals(), vars)
            except Exception as e:
                Err(e)
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
                #if show_results:
                if 1 or show_results: #xx
                    PrintSolution()

if __name__ == "__main__":
    d = {}          # Options dictionary
    args = ParseCommandLine(d)
    if 1:   # Start with testing example
        c = 2500
        s = 6500
    CommandLoop()
# vim: tw=100
