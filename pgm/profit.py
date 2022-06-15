'''

Interactive utility to calculate the profit of a project
    Type ? for help at prompt
 
    Equations
        p = 1 - c/s     = m/(1 + m) = 1 - 1/u
        s = c/(1 - p)   = u*c
        c = s*(1 - p)   = s/u
 
        m = p/(1 - p)   = u - 1
        u = s/c         = m + 1 = 1/(1 - p)
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
        d["-h"] = False     # Introductory help
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
            z.n = d["-n"]           # Number of significant figures
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
            Colors(self.color)
            s, c, p, m, u = self.s, self.c, self.p, self.m, self.u
            # Note there are two behaviors:  if self.pct is True (toggled
            # by the 'p' command), then display m and p in %.
            n, minw = 1, 4
            pct, mult = ("%", 100) if self.pct else ("", 1)
            out = []
            # Get variable's value strings
            C = f"{c}"
            S = f"{s}"
            P = f"{mult*p}"
            M = f"{mult*m}"
            U = f"{u}"
            # Build output array
            O = (
                ("S", S),
                ("C", C),
                (f"P{pct}", P),
                (f"M{pct}", M),
                ("U", U)
            )
            # Get first and second variables to colorize
            first, second = None, None
            if len(self.dq) == 2:
                second, first = self.dq
            elif len(self.dq) == 1:
                first = self.dq[0]
            for heading, value in O:
                letter = heading[0].lower()
                w = max(len(value), minw)
                # Format them centered to indicated column width
                if not self.ok and heading in ("S", "C"):
                    hdr = f"{heading:^{w}s}"
                    val = f"{'-':^{w}s}"
                else:
                    hdr = f"{heading:^{w}s}"
                    val = f"{value:^{w}s}"
                # If P or M are negative, colorize them
                if letter in ("P", "M"):
                    if flt(val) < 0:
                        val = f"{t.neg}{val}{t.nn}"
                elif letter == "U":
                    if U != "0/0":
                        tmp = val
                        if u >= 2:
                            tmp = f"{t.u2}{val}{t.nn}"
                        if u >= 3:
                            tmp = f"{t.u3}{val}{t.nn}"
                        if u >= 4:
                            tmp = f"{t.u4}{val}{t.nn}"
                        if u >= 5:
                            tmp = f"{t.u5}{val}{t.nn}"
                        val = tmp
                # Colorize last changed
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
                me += f"\n The values are not sufficient for a unique solution"
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
            x.n = mdl.n
            x.rtz = x.rtdp = True
            x.low, x.high = mdl.low, mdl.high
            return mdl
        except Exception as e:
            t.print(f"{t.msg}[{Lineno()}]Could not read previous state from disk")
            return None
if 1:   # Core functionality
    def ColorKey():
        'Print a color key'
        if not mdl.color:
            t.print(f"{t.msg}Must turn colorizing on first")
            return
        Colors(True)
        print("Meanings of color:")
        t.print(f"{t.last}    Last variable changed")
        t.print(f"{t.u2}    U >= 2, {t.u3}U >= 3, {t.u4}U >= 4, {t.u5}U >= 5")
        t.print(f"{t.neg}    P or M are negative")
        t.print(f"{t.msg}    Informational message")
        Colors(False)
    def Colors(on):
        '''If on is False, all of these are empty strings so that no escape
        codes wind up in the output.
        '''
        none = ""
        t.msg  = t("wht")  if on else none
        t.neg  = t("redl") if on else none
        t.first = t("ornl")  if on else none
        t.second = t("trq")  if on else none
        t.u2   = t('grnl') if on else none
        t.u3   = t('yell') if on else none
        t.u4   = t('ornl') if on else none
        t.u5   = t('magl') if on else none
        t.nn   = t.n       if on else none
    def Intro():
        print(dedent(f'''
        Interactive utility to calculate a project's profit.  Use h for list of 
        commands.  Variables are:
            c = cost                                = s*(1 - p)
            s = selling price                       = c/(1 - p)
            p = profit based on selling price       = 1 - s/c
            m = markup based on cost                = p/(1 - p)
            u = multiplier                          = s/c
        Enter a variable's value after its letter.  Expressions are allowed and
        the math module is in scope.  Example:
            > a = 1     # Local variable assigment
            > c a       # cost is now equal to 1
            > s 2       # Selling price is 2
        will print
            S    C    P%   M%   U
            2    1    50  100   2
        Profit and markup can be in either % or decimal fractions (use the %
        command to switch between them).
        '''))
    def Help():
        print(f"{t.msg}", end="")
        print(dedent(f'''
        Interactive utility to calculate a project's profit.  Enter s for
        selling price, c for cost, and p for profit followed by the desired
        value.  Use -h on command line for introductory help.  Commands:
        q       Quit
        .       Print the results again (.. adds 2 significant figures)
        C       Clear the screen
        e       Show equations
        k       Use colorized text [{mdl.color}]
        l       List local variables
        n num   Set the number of significant figures [{mdl.n}]
        %       Toggle percent mode (show profit and markup in %) [{mdl.pct}]
        > file  Save state to a file (won't overwrite existing file)
        >> file Save state to a file (overwrites existing file)
        < file  Load state from a file
        * x     Multiply s and c by x
        / x     Divide s and c by x
        R       Reset model
        R!      Reset and clear all local variables
        '''))
        print(f"{t.nn}", end="")
    def ShowEquations():
        print(dedent(f'''
        p = 1 - c/s     = m/(1 + m)    = 1 - 1/u
        s = c/(1 - p)   = u*c
        c = s*(1 - p)   = s/u
        m = p/(1 - p)   = u - 1
        u = s/c         = m + 1        = 1/(1 - p)
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
    def DoCommand(cmd):
        '''Return values:
            0   Command completed successfully
            1   Command failed
            2   Command was to quit
        '''
        cmd = RemoveComment(cmd)
        if cmd == "q":
            if not d["-i"]:
                Save(modelfile)
            return 2
        elif cmd == "h":
            Help()
        elif cmd[0] == ".":
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
        elif cmd == "b":
            breakpoint()
        elif cmd == "C":
            os.system("clear")
        elif cmd == "e":
            ShowEquations()
        elif cmd == "k":
            mdl.color = not mdl.color
            print(mdl)
        elif cmd == "K":
            ColorKey()
        elif cmd == "l":
            print(f"{t.msg}Local variables:")
            if mdl.vars:
                for i in mdl.vars:
                    if i not in mdl.names:
                        print(f"  {i} = {mdl.vars[i]}")
            print(f"{t.nn}", end="")
        elif cmd[0] == "n":
            if not cmd[1:]:
                t.print(f"{t.msg}Need an argument for n command")
                return 1
            sf = GetN(cmd[1:])
            if sf is None:
                return 1
            x = flt(0)
            x.n = sf
            print(mdl)
        elif cmd[0] == "*":
            if len(cmd) == 1:
                t.print(f"{t.msg}Need an argument for * command")
            try:
                x = eval(cmd[1:], globals(), mdl.vars)
            except Exeption as e:
                t.print(f"{t.msg}[{Lineno()}] * command exception: {e}")
                return 2
            mdl.c *= x
            mdl.s *= x
            mdl.update()
            print(mdl)
        elif cmd[0] == "/":
            if len(cmd) == 1:
                t.print(f"{t.msg}Need an argument for / command")
            try:
                x = eval(cmd[1:], globals(), mdl.vars)
            except Exeption as e:
                t.print(f"{t.msg}[{Lineno()}] / command exception: {e}")
                return 2
            mdl.c /= x
            mdl.s /= x
            mdl.update()
            print(mdl)
        elif cmd[0] == ">":
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
            except Exeption as e:
                t.print(f"{t.msg}[{Lineno()}] Save() exception: {e}")
        elif cmd[0] == "<":
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
        elif cmd == "%":
            mdl.pct = not mdl.pct
            print(mdl)
        elif cmd == "R":
            mdl.reset()
        elif cmd == "R!":
            mdl.reset(hard=True)
        else:
            t.print(f"{t.msg}{cmd!r} is an unrecognized command")
        return 0
    def ProcessCommand(cmd, off=False):
        '''Return values:
            0   Command completed successfully
            1   Command failed
            2   Command was to quit
        '''
        name = cmd[0]
        if name == "#":
            # It's a comment
            pass
        elif "=" in cmd:
            # Local variable assignment
            name, value = cmd.split("=", 1)
            name = name.strip()
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
        while not finished:
            e = input(f"> ").strip()
            if not e:
                continue
            cmds = e.split(";")
            for cmd in cmds:
                retval = ProcessCommand(cmd)
                if retval == 1:
                    break
                elif retval == 2:
                    finished = True
                    break
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
    if 0:
        Loop(setup=True)
    else:
        Loop()
