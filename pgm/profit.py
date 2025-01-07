'''

ToDo
    - Spread out the printout a bit
    - Color the values too (neg p or m red, u's goodness by color)
    - Instead of scientific notation use engsic

Interactive utility to calculate the profit of a project
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
        # Interactive tool for project profit
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import pickle
        import sys
        import traceback
        from math import *
        from pprint import pprint as pp
        from collections import deque 
        import readline
    # Custom imports
        from color import Color, TRM as t
        from f import flt
        from transpose import Transpose
        from lwtest import Assert
        from wrap import dedent
    # Global variables
        ii = isinstance
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def ParseCommandLine(d):
        d["-e"] = False     # Turns off catching exceptions so you can see
                            # where error occurs
        d["-h"] = True      # Introductory help
        d["-i"] = False     # Don't read persisted data
        d["-n"] = 2         # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "en:hi") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("ehi"):
                d[o] = not d[o]
            elif o in ("-n",):
                try:
                    d["-n"] = int(a)
                    if not (1 <= d["-n"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-n option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
        return args
    def Lineno():
        'Return line number of last exception'
        typ, val, tb = sys.exc_info()
        return tb.tb_lineno
    def LN(brackets=True):
        'Return line number where this was called'
        s = traceback.extract_stack()[-2:][0][1]
        if brackets:
            return f"[{s}]"
        else:
            return f"{s}"
if 1:   # Classes
    class Model(object):
        'Contains the model for the equation p = 1 - c/s'
        def __init__(self):
            # We put colorizing here so that it isn't affected by a reset.
            self.color = False      # If True, use colors in output
            self.reset(hard=True)
        def reset(self, hard=False):
            self.names = set("cspmu")   # Names of model variables
            z = flt(0)
            z.N = d["-n"]           # Number of significant figures
            z.rtz = z.rtdp = True   # Make str(flt) look like integer when possible
            # Primary model attributes
            self.c = z              # Cost
            self.s = z              # Selling price
            self.p = z              # Profit
            self.m = z              # Markup
            self.u = z              # Multiplier
            # Other attributes
            self.n = z.n            # Number of significant figures
            self.ok = False         # If True, self.update() returned valid numbers
            self.pct = True         # If True, show m and p in %
            # When to use scientific notation
            self.low = 1e-3
            self.high = 1e6
            z.low, z.high = self.low, self.high
            # This container keeps the last two variables the user entered,
            # telling you which variable is the dependent one.
            self.dq = deque([], maxlen=2)
            # User's local variables
            if not hasattr(self, "vars") or hard:
                self.vars = {}
        def normalize(self):
            'Divide s and c by c'
            if not self.c:
                print("Can't normalize with zero cost")
            else:
                self.s /= self.c
                self.c /= self.c
        def append(self, name):
            "Append if name isn't already in deque"
            if name in self.dq:
                # A fine point is that if name is in the deque and it's not
                # at the back (last entered), we'll want it there to see a
                # correct colorized display because the user is entering it
                # again.
                if self.dq[-1] != name:
                    self.dq.rotate()
                return
            self.dq.append(name)
        def sto(self, name, value):
            '''Store the financial variable name and its value after
            vetting.  Also works for local variables, but there's no
            vetting or concern with type.
            '''
            if name in self.names:
                try:
                    x = flt(eval(value, globals(), self.vars))
                except Exception as e:
                    m = f"[{LN()}] {value!r} for variable {name!r}could not be evaluated:\n{e}"
                    raise ValueError(m)
                if name == "c":
                    if x <= 0:
                        raise ValueError("Cost must be > 0")
                    self.c = flt(x)
                    self.append(name)
                elif name == "s":
                    if x <= 0:
                        raise ValueError("Selling price must be > 0")
                    self.s = flt(x)
                    self.append(name)
                elif name == "p":
                    if self.pct:
                        if x >= 100:
                            raise ValueError("Profit must be less than 100%")
                        self.p = flt(x/100)
                    else:
                        if x >= 1:
                            raise ValueError("Profit must be less than 1")
                        self.p = x
                    self.append(name)
                elif name == "m":
                    self.m = flt(x/100) if self.pct else x
                    self.append(name)
                elif name == "u":
                    if x <= 0:
                        raise ValueError("Multiplier must be greater than 0")
                    self.u = x
                    self.append(name)
                self.update()
            else:
                self.vars[name] = value
        def update(self):
            '''To be able to get a unique numerical solution, either 1) c and
            one other variable or 2) s and one other variable must be
            given.
            '''
            # See if we can solve this problem
            if len(self.dq) != 2:
                # Cannot solve
                self.ok = False
                return
            if not ("c" in self.dq or "s" in self.dq):
                self.ok = False
                return
            # Solution is possible
            have = set(self.dq)
            Assert(len(have) == 2)
            c, s, p, m, u = self.c, self.s, self.p, self.m, self.u
            if have == set("cs"):       # Get p
                p = flt(1 - c/s)
                m = p/(1 - p)
                u = s/c
            elif have in (set("cp"), set("cm"), set("cu")):  # Get s
                if have == set("cm"):
                    p = m/(1 + m)
                    u = 1/(1 - p)
                elif have == set("cu"):
                    p = 1 - 1/u
                    m = p/(1 - p)
                else:   # cp
                    u = 1/(1 - p)
                    m = p*u
                s = flt(c/(1 - p))
            elif have in (set("sp"), set("sm"), set("su")):  # Get c
                if have == set("sm"):
                    p = m/(1 + m)
                    u = 1/(1 - p)
                elif have == set("su"):
                    p = 1 - 1/u
                    m = p/(1 - p)
                else:   # sp
                    u = 1/(1 - p)
                    m = p*u
                c = flt(s*(1 - p))
            self.c, self.s, self.p, self.m, self.u = c, s, p, m, u 
            self.ok = True
            # Add these variables to self.vars so they can be used in
            # expressions.  These overwrite values defined by user.
            c, s, p = self.c, self.s, self.p
            self.vars["c"] = c
            self.vars["s"] = s
            self.vars["p"] = p
            self.vars["m"] = m
            self.vars["u"] = u
        def __str__(self):
            'Print the instance produces the report'
            Colors(self.color)
            s, c, p, m, u = self.s, self.c, self.p, self.m, self.u
            # Note there are two behaviors:  if self.pct is True (toggled
            # by the 'p' command), then display m and p in %.
            minw = 4
            pct, mult = ("%", 100) if self.pct else ("", 1)
            out = []
            # Get variable's value strings
            C = f"{c}"
            S = f"{s}"
            P = f"{mult*p}"
            M = f"{mult*m}"
            U = f"{u}"
            # Get first and second variables to colorize
            first, second = None, None
            if len(self.dq) == 2:
                second, first = self.dq
            elif len(self.dq) == 1:
                first = self.dq[0]
            for heading, value in (("s", S), ("c", C), (f"p{pct}", P), (f"m{pct}", M), ("u", U)):
                letter = heading[0].lower()
                w = max(len(value), minw)
                # Format them centered to indicated column width
                if not self.ok and heading in ("s", "c"):
                    hdr = f"{heading:^{w}s}"
                    val = f"{'-':^{w}s}"
                else:
                    hdr = f"{heading:^{w}s}"
                    val = f"{value:^{w}s}"
                # If p or m are negative, colorize them
                if letter in ("p", "m"):
                    if flt(val) < 0:
                        val = f"{t.neg}{val}{t.nn}"
                elif letter == "u":
                    if U != "0/0":
                        # Colorize u's val
                        if u <= 1:
                            val = f"{t.u1}{val}{t.nn}"
                        elif u >= 5:
                            val = f"{t.u5}{val}{t.nn}"
                        elif u >= 4:
                            val = f"{t.u4}{val}{t.nn}"
                        elif u >= 3:
                            val = f"{t.u3}{val}{t.nn}"
                        elif u >= 2:
                            val = f"{t.u2}{val}{t.nn}"
                # Colorize the two last changed variables
                if first == letter:
                    hdr = f"{t.first}{hdr}{t.nn}"
                elif second == letter:
                    hdr = f"{t.second}{hdr}{t.nn}"
                out.append([hdr, val])
            # Transpose the out array to the two output lines
            o = Transpose(out)
            me = ' '.join(o[0]) + "\n"
            me += ' '.join(o[1])
            if not self.ok:
                me += f"\n Not enough information for a solution"
            return me
        def test(self):
            'Verify basic numerical correctness and functionality'
            x = flt(0)
            x.n = 3
            x.rtz = x.rtdp = True
            self.reset(hard=True)
            Assert(len(mdl.dq) == 0)
            # c and s
            mdl.sto("c", "1")
            Assert(len(mdl.dq) == 1)
            mdl.sto("s", "2")
            Assert(len(mdl.dq) == 2)
            Assert(mdl.p == flt(1 - 1/2))
            mdl.sto("s", "3")
            Assert(mdl.p == flt(1 - 1/3))
            mdl.sto("s", "100")
            Assert(mdl.p == flt(1 - 1/100))
            mdl.sto("c", "480")
            mdl.sto("s", "1400")
            Assert(mdl.p == flt(1 - 480/1400))
            # p and s
            mdl.sto("s", "1")
            mdl.sto("p", "50")
            Assert(mdl.c == flt(1/2))
            # p and c
            mdl.sto("c", "1")
            mdl.sto("p", "50")
            Assert(mdl.s == flt(2))
            # vars
            a = 44
            mdl.sto("x", a)
            Assert(mdl.vars["x"] == a)
            Assert(len(mdl.vars) == 1)
            self.reset(hard=True)
            Assert(mdl.vars == {})
        if 1:   # Properties
            @property
            def d(self):
                'Debug dump of state'
                print(dedent(f'''
                Model state:
                  c = {self.c}  s = {self.s}  p = {self.p}  m = {self.m}  u = {self.u}
                  ok = {self.ok}  dq = {self.dq} vars = {self.vars}
                '''))
if 1:   # Persistence
    def GetFile():
        '''Return the name of the file we should use to persist our
        Model object.  It will be in the same directory as the script.
        '''
        f = P(sys.argv[0])
        dir = f.parent
        name = f.stem + ".data"
        return P(dir/name)
    def Save(file):
        Assert(ii(file, P))
        try:
            with open(file, "wb") as f:
                s = pickle.dumps(mdl)
                f.write(s)
        except Exception as e:
            t.print(f"{t.msg}[{Lineno()}]Save exception: {e}")
    def Load(file):
        'Return a Model instance or None'
        global mdl
        if not file.exists():
            return None
        try:
            with open(file, "rb") as f:
                b = f.read()
            mdl = pickle.loads(b)
            if not ii(mdl, Model):
                return None
            # Reset flt state
            x = flt(0)
            x.N = mdl.n
            x.rtz = x.rtdp = True
            x.low, x.high = mdl.low, mdl.high
            return mdl
        except Exception as e:
            t.print(f"{t.msg}[{Lineno()}]Could not read previous state from disk")
            return None
if 1:   # Core functionality
    def Colors(on):
        '''If on is False, all of these are empty strings so that no escape
        codes wind up in the output.
        '''
        none = ""
        t.msg = t("#dff1d6") if on else none    # Hint of green
        t.msg = t("#a1a894") if on else none    # Half Washed Green
        t.neg = t("redl") if on else none
        t.first = t("ornl") if on else none
        t.second = t("trq") if on else none
        t.last = t("royl") if on else none
        t.u1 = t('redl') if on else none        # u < 1
        t.u2 = t('olv') if on else none         # u >= 2
        t.u3 = t('yel') if on else none         # u >= 3
        t.u4 = t('royl') if on else none        # u >= 4
        t.u5 = t('magl') if on else none        # u >= 5
        t.nn = t.n if on else none
    def ColorKey():
        'Print a color key'
        if not mdl.color:
            t.print(f"{t.msg}Must turn colorizing on first")
            return
        Colors(True)
        print("Meanings of color:")
        t.print(f"{t.first}    Last variable changed")
        t.print(f"{t.second}    Next to last variable changed")
        t.print(f"{t.u2}    u >= 2, {t.u3}u >= 3, {t.u4}u >= 4, {t.u5}u >= 5")
        t.print(f"{t.neg}    p or m are negative, u < 1")
        t.print(f"{t.msg}    Informational message")
        Colors(False)
    def Intro():
        print(dedent(f'''
        Interactive utility to calculate a project's profit.  Use h for list of commands.
        Variables are:
            c = cost                                = s*(1 - p)
            s = selling price                       = c/(1 - p)
            p = profit based on selling price       = 1 - s/c
            m = markup based on cost                = p/(1 - p)
            u = multiplier                          = s/c
        Enter a variable's value after its letter.  Expressions are allowed and the math module is
        in scope.  Example:
            > a = 1     # Local variable assignment
            > c a       # cost is now equal to 1
            > s 2       # Selling price is 2
        will print
            S    C    P%   M%   U
            2    1    50  100   2
        Profit and markup can be in either % or decimal fractions (use the % command to switch
        between them).
        
        Use the h command at the '>' prompt for help.

        '''.rstrip()))
    def Help():
        print(f"{t.msg}", end="")
        x = flt(0)
        print(dedent(f'''
        Interactive utility to calculate a project's profit.  Enter s for selling price, c for
        cost, and p for profit followed by the desired value.  Commands:
            q       Quit (state is persisted)
            .       Print the results again
            b       Enter debugger
            C       Clear the screen
            e       Show equations
            H       Manpage
            k       Use colorized text [{mdl.color}]
            K       Show color meanings
            l       List local variables
            N       Normalize c to 1
            n num   Set number of digits [{x.N}]
            %       Toggle p and m in %
            > file  Save state (no overwrite)
            >> file Save state (overwrites)
            < file  Load state from a file
            * x     Multiply s and c by x
            / x     Divide s and c by x
            !       Reset model
            !!      Reset and clear all local variables
        '''))
        print(f"{t.nn}", end="")
    def SetUp():
        'Use to set the model to a desired state for testing/debugging'
        choice = 1
        if not choice:
            return
        cmds = ""
        su = t("magl")
        t.print(f"{su}Running commands from SetUp")
        if choice == 1:
            cmds = dedent('''
            /
            k
            c1
            m200
            ''')
        for i in cmds.split("\n"):
            t.print(f"{t('magl')}>>> {i}")
            ProcessCommand(i.strip(), off=True)
        t.print(f"{su}Finished SetUp()")
    def Manpage():
        print(dedent(f'''
        This script helps assess the profit of a project.  Example:

        Suppose you plan to sell widgets for 2 and they cost you 1.  Start the program and define
        these two variables as follows

            > s2
            > c 1
            s    c    p%   m%   u
            2    1    50  100   2

        The 's2' shows that the number can be cuddled next to the symbol for the primary variables
        s, c, p, m, and u.  p and m are shown in % by default; use the command '%' to toggle this.

        The script's purpose is to let you make adjustments to the variables and see the results.
        For example, if you wanted 77.3% profit, enter 'p 77.3' and you'll see the selling price
        needs to be 4.4.  I like to keep the model's display to 2 digits (use the n command)
        because this makes the overall numerical state easy to grasp and see 1%-ish changes.
        Contrast this to most tools like spreadsheets where you see too many digits which obscure
        the overall behavior.

        When I worked at HP in the 1980's, R&D projects had a corporate mandate to develop new
        products with a multiplier of 5.  The multiplier u is defined as s/c.  If you enter the
        command 'c1;u5' (a semicolon can separate commands on one line) you'll find this is
        equivalent to 80% profit.  I'm a fan of using multipliers because you can do the rough
        calculation in your head.

        If colorizing is on (toggle with k), you can see the last two entered variables and you'll
        see negative values of p or m in red and u's magnitude will be colorized at various integer
        levels (red means u < 1).  Use the command K to see the colorizing rules.  For an important
        calculation, use a command like 'script' to capture all your interaction with the script
        and be able to replay it later.  Use '#' on lines to act as comments for documentation.

        A model with unit cost is easy to visualize.  To work with a unit cost, save the current
        cost in a local variable with 'cost = c', then type the command N.  The c variable will be
        set to 1.  Get back to where you were with the command 'c cost'.

        '''.rstrip()))
        print(f"{t.nn}", end="")
    def ShowEquations():
        print(dedent(f'''
        Equations
            p = 1 - c/s     = m/(1 + m)    = 1 - 1/u        Profit
            s = c/(1 - p)   = u*c                           Selling price
            c = s*(1 - p)   = s/u                           Cost
            m = p/(1 - p)   = u - 1                         Markup based on cost
            u = s/c         = m + 1        = 1/(1 - p)      Multiplier
        '''))
    def GetN(s):
        'Return int(s) between 1 and 15 or None if problem'
        try:
            n = int(s)
            if not (1 <= n <= 15):
                raise Exception("Integer must be between 1 and 15")
            return n
        except Exception as e:
            t.print(f"{t.msg}[{Lineno()}] Exception: {e}")
            return None
    def RemoveComment(s):
        if "#" not in s:
            return s
        loc = s.find("#")
        return s[:loc].trim()
    def DumpState():
        '''Print program's state for debugging help
        '''

    def DoCommand(cmd):
        '''Return values:
            0   Command completed successfully
            1   Command failed
            2   Command was to quit
        '''
        cmd = RemoveComment(cmd)
        if cmd == "q":          # Quit
            if not d["-i"]:
                Save(modelfile)
            return 2
        elif cmd == "h":        # Show help
            Help()
        elif cmd[0] == ".":     # Print results again
            x = flt(0)
            if set(cmd) != set("."):
                t.print(f"{t.msg}'.' command can only be composed of '.' characters")
                return 1
            numdots = len(cmd)
            if numdots == 1:
                print(mdl)
            else:
                with x:
                    x.n += 2
                    mdl.update()
                    print(mdl)
        elif cmd == "b":        # Start debugger
            breakpoint()
        elif cmd == "C":        # Clear the screen
            os.system("clear")
        elif cmd == "D":        # Dump model's state for debugging
            DumpState()
        elif cmd == "e":        # Show the model's equations
            ShowEquations()
        elif cmd == "H":        # Show manpage
            Manpage()
        elif cmd == "k":        # Toggle color display
            mdl.color = not mdl.color
            print(mdl)
        elif cmd == "K":        # Show color key
            ColorKey()
        elif cmd == "l":        # Show local variables
            print(f"{t.msg}Local variables:")
            if mdl.vars:
                for i in mdl.vars:
                    if i not in mdl.names:
                        print(f"  {i} = {mdl.vars[i]}")
            print(f"{t.nn}", end="")
        elif cmd == "N":        # Normalize cost to 1
            mdl.normalize()
            print(mdl)
        elif cmd[0] == "n":     # Set number of digits
            if not cmd[1:]:
                t.print(f"{t.msg}Need an argument for n command")
                return 1
            sf = GetN(cmd[1:])
            if sf is None:
                return 1
            x = flt(0)
            x.N = mdl.n = sf
            print(mdl)
        elif cmd[0] == "*":     # Multiply c & s by a constant
            if len(cmd) == 1:
                t.print(f"{t.msg}Need an argument for * command")
            try:
                x = eval(cmd[1:], globals(), mdl.vars)
            except Exception as e:
                t.print(f"{t.msg}[{Lineno()}] * command exception: {e}")
                return 2
            mdl.c *= x
            mdl.s *= x
            mdl.update()
            print(mdl)
        elif cmd[0] == "/":     # Divide c & s by a constant
            if len(cmd) == 1:
                t.print(f"{t.msg}Need an argument for / command")
            try:
                x = eval(cmd[1:], globals(), mdl.vars)
            except Exception as e:
                t.print(f"{t.msg}[{Lineno()}] / command exception: {e}")
                return 2
            mdl.c /= x
            mdl.s /= x
            mdl.update()
            print(mdl)
        elif cmd[0] == ">":     # Save state to a file; overwrite if '>>'
            if len(cmd) == 1:
                t.print(f"{t.msg}Must give a file name to save to")
                return 1
            overwrite = False
            if cmd[1] == ">":
                overwrite = True
                if len(cmd) == 2:
                    t.print(f"{t.msg}Must give a file name to save to")
                    return 1
                name = P(cmd[2:].strip())
            else:
                name = P(cmd[1:].strip())
            if name.exists() and not overwrite:
                t.print(f"{t.msg}Can't overwrite existing file")
                return 1
            try:
                Save(name)
            except Exception as e:
                t.print(f"{t.msg}[{Lineno()}] Save() exception: {e}")
        elif cmd[0] == "<":     # Load state from file
            if len(cmd) == 1:
                t.print(f"{t.msg}Must give a file name to read from")
                return 1
            name = P(cmd[1:].strip())
            if not name.exists():
                t.print(f"{t.msg}File '{name}' doesn't exist")
                return 1
            rv = Load(name)
            if rv is None:
                t.print(f"{t.msg}Couldn't read file '{name}'")
        elif cmd == "%":        # Toggle % display
            mdl.pct = not mdl.pct
            print(mdl)
        elif cmd == "!":        # Reset model variables
            mdl.reset()
        elif cmd == "!!":       # Reset model variables and remove local variables
            mdl.reset(hard=True)
        else:
            t.print(f"{t.msg}{cmd!r} is an unrecognized command")
        return 0
    def ProcessCommand(cmd, off=False):
        '''Return values:
            0   Command completed successfully
            1   Command failed
            2   Quit
        Commands are:
            #   A comment
            Local variable assignment  (contains '=')
            Set primary variable c, s, p, m, or u
            Other commands
        '''
        name = cmd[0]
        if name == "#":
            # It's a comment
            pass
        elif "=" in cmd:
            # Local variable assignment
            name, value = cmd.split("=", 1)
            name = name.strip()
            if name in "c s p m u".split():
                print("You cannot assign to c, s, p, m, or u")
            else:
                try:
                    x = eval(value, globals(), mdl.vars)
                except Exception as e:
                    if edbg: 
                        raise
                    t.print(f"{t.msg}[{Lineno()}] Local variable exception:\n {e}")
                    return 1
                mdl.vars[name] = x
        elif name in mdl.names:
            # Set primary variable
            if len(cmd) < 2:
                t.print(f"{t.msg}Need a value for the variable")
            else:
                value = cmd[1:].strip()
            try:
                mdl.sto(name, value)
            except Exception as e:
                if edbg:
                    raise
                t.print(f"{t.msg}[{Lineno()}] Primary variable exception:\n {e}")
                return 1
            if mdl.ok and not off:
                print(mdl)
        else:
            # It must be a command
            try:
                retval = DoCommand(cmd)
                if retval == 2:
                    return 2
            except Exception as e:
                if edbg:
                    raise
                t.print(f"{t.msg}[{Lineno()}] Command exception:\n {e}")
                return 1
        return 0
    def Loop(setup=False):
        if d["-h"]:
            Intro()
        Colors(mdl.color)
        finished = False 
        if setup:
            SetUp()
        if mdl.ok:
            print(mdl)
        while not finished:
            e = input(f"> ").strip()    # Get command
            if not e:
                continue
            cmds = e.split(";")         # Multiple commands separated by ';'
            for cmd in cmds:
                retval = ProcessCommand(cmd)
                if retval == 1:
                    break
                elif retval == 2:
                    finished = True
                    break

if __name__ == "__main__":
    # Note:  there's no locking, so if you run this script in two different
    # processes, you'll have a race condition for the persisted data.
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    edbg = d["-e"]
    # Get the model instance
    if d["-i"]:
        # No persistence
        mdl = Model()
    else:
        modelfile = GetFile()
        mdl = Load(modelfile)
        if mdl is None:
            mdl = Model()
    Loop(setup=True) if False else Loop()
