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
        import atexit
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
        d["-d"] = False     # Debugging: runs SetUp() to define a state
        d["-e"] = False     # Turns off catching exceptions so you can see
                            # where error occurs
        d["-h"] = False     # Introductory help
        d["-n"] = 2         # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "den:h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("edh"):
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
if 1:   # Classes
    class Model(object):
        'Contains the model for the equation p = 1 - c/s'
        def __init__(self):
            self.inf = "∞"
            self.infm = "-∞"
            self.names = set("cspmu")
            self.reset(hard=True)
        def reset(self, hard=False):
            z = flt(0)
            z.n = d["-n"]   # Number of significant figures
            z.rtz = z.rtdp = True   # Make str(flt) look like integer when possible
            self.c = z  # Cost
            self.s = z  # Selling price
            self.p = z  # Profit
            self.n = z.n    # Number of significant figures
            self.ok = False         # If True, self.update() returned valid numbers
            self.pct = True         # If True, show m and p in %
            self.color = False      # If True, use colors in output
            # When to use scientific notation
            self.low = 1e-3
            self.high = 1e6
            z.low, z.high = self.low, self.high
            # The following container keeps the last two variables entered,
            # telling you variable is the dependent one.
            self.dq = deque([], maxlen=2)
            if hard:
                self.vars = {}
        def append(self, name):
            "Append if name isn't already in deque"
            if name in self.dq:
                # A fine point is that if name is in the deque and it's not
                # at the back (last entered), we'll want it there to see a
                # correct colorized display.
                if self.dq[-1] != name:
                    # Rotate the deque 1 unit
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
                    m = f"{value!r} could not be evaluated:\n{e}"
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
                    if x < 0:
                        raise ValueError("Markup must be >= 0")
                    if self.pct:
                        x /= 100
                    self.p = flt(x/(1 + x))
                    self.append("p")
                elif name == "u":
                    if x <= 0:
                        raise ValueError("Multiplier must be > 0")
                    self.p = flt(1 - 1/x)
                    self.append("p")
                self.update()
            else:
                self.vars[name] = value
        def update(self):
            if len(self.dq) != 2:
                self.ok = False
                return
            have = set(self.dq)
            assert(self.dq[0] != self.dq[1])
            if set("cs") == have:       # Get p
                if self.s:
                    self.p = flt(1 - self.c/self.s)
                else:
                    self.p = -float("inf")
            elif set("cp") == have:     # Get s
                self.s = flt(self.c/(1 - self.p))
            elif set("sp") == have:     # Get c
                self.c = flt(self.s*(1 - self.p))
            self.ok = True
            # Add these variables to self.vars so they can be used in
            # expressions.  These overwrite values defined by user.
            c, s, p = self.c, self.s, self.p
            self.vars["c"] = c
            self.vars["s"] = s
            self.vars["p"] = p
            self.vars["m"] = p/(1 - p)
            self.vars["u"] = s/c
        def __str__(self):
            Colors(self.color)
            s, c, p = self.s, self.c, self.p
            m, u = self.m, self.u
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
            last = self.dq[1].upper() if len(self.dq) == 2 else None
            for i in O:
                letter = i[0][0]
                w = max(len(i[1]), minw)
                a = f"{i[0]:^{w}s}"
                b = f"{i[1]:^{w}s}"
                # If P or M are negative, colorize them
                if letter in ("P", "M"):
                    if flt(b) < 0:
                        b = f"{t.neg}{b}{t.nn}"
                elif letter == "U":
                    if U != "0/0":
                        tmp = b
                        if u >= 2:
                            tmp = f"{t.u2}{b}{t.nn}"
                        if u >= 3:
                            tmp = f"{t.u3}{b}{t.nn}"
                        if u >= 4:
                            tmp = f"{t.u4}{b}{t.nn}"
                        if u >= 5:
                            tmp = f"{t.u5}{b}{t.nn}"
                        b = tmp
                # Colorize last changed
                if last is not None and last == letter:
                    a = f"{t.last}{a}{t.nn}"
                out.append([a, b])
            # Transpose the out array to the two output lines
            o = Transpose(out)
            me = ' '.join(o[0]) + "\n"
            me += ' '.join(o[1])
            if not self.ok:
                me += f"\n Model values are not valid yet"
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
            # Note:  the variables m and u are provided as a convenience, but
            # they are expressible as functions of p.
            @property
            def m(self):
                return flt(self.p/(1 - self.p))
            @property
            def u(self):
                if not self.p and not self.c:
                    return "0/0"
                if not self.c:
                    return self.inf
                return flt(self.s/self.c)
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
        t.msg  = t("yelb")  if on else none
        t.neg  = t("redl") if on else none
        t.last = t("trq")  if on else none
        t.u2   = t('grnl') if on else none
        t.u3   = t('yell') if on else none
        t.u4   = t('ornl') if on else none
        t.u5   = t('magl') if on else none
        t.nn   = t.n       if on else none
    def Intro():
        print(f"{t.msg}", end="")
        print(dedent(f'''
        Interactive utility to calculate a project's profit.  Use ? for commands.
        Variables are:
            c = cost
            s = selling price
            p = profit in % based on selling price
            m = markup in % based on cost
            u = multiplier = s/c
        Enter a variable's value after its letter.  Expressions are allowed and
        the math module is in scope.  Responses like "a = 3" will be
        assignments to local variables.  You can assign to local variables with
        the same name as the above five primary variables, but they will be
        overwritten when the model's values are calculated (this is necessary
        to allow you to use the variables in expressions).

        Note:  if you don't like seeing p and m in percentages, use the %
        command to change to regular decimal fractions.  Then you also
        enter them as decimal fractions.
    
        Example:
            > a = 1     # Local variable assigment
            > c a       # cost is now equal to 1
            > s 2       # Selling price is 2
        will print
            S    C    P%   M%   U
            2    1    50  100   2
        '''))
        print(f"{t.nn}", end="")
    def Help():
        print(f"{t.msg}", end="")
        print(dedent(f'''
        Interactive utility to calculate a project's profit.  Enter s for
        selling price, c for cost, and p for profit followed by the desired
        value.  Use -h on command line for introductory help.
        q       Quit
        .       Print the results again
        C       Clear the screen
        k       Use colorized text [{mdl.color}]
        l       List local variables
        n num   Set the number of significant figures [{mdl.n}]
        %       Toggle percent mode (show profit and markup in %) [{mdl.pct}]
        > file  Save state to a file (won't overwrite existing file)
        >> file Save state to a file (overwrites existing file)
        < file  Load state from a file
        /       Reset model
        //      Reset and clear all local variables
        '''))
        print(f"{t.nn}", end="")
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
    def Command(cmd):
        cmd = RemoveComment(cmd)
        if cmd == "q":
            Save(modelfile)
            exit(0)
        elif cmd[0] == ".":
            print(mdl)
        elif cmd == "b":
            breakpoint()
        elif cmd == "C":
            os.system("clear")
        elif cmd == "k":
            mdl.color = not mdl.color
            print(mdl)
        elif cmd == "K":
            ColorKey()
        elif cmd == "l":
            print(f"{t.msg}Local variables:")
            if mdl.vars:
                for i in mdl.vars:
                    print(f"  {i} = {mdl.vars[i]}")
            print(f"{t.nn}", end="")
        elif cmd[0] == "n":
            if not cmd[1:]:
                t.print(f"{t.msg}Need an argument for n command")
                return
            sf = GetN(cmd[1:])
            if sf is None:
                return
            x = flt(0)
            x.n = sf
            print(mdl)
        elif cmd[0] == ">":
            if len(cmd) == 1:
                t.print(f"{t.msg}Must give a file name to save to")
                return
            overwrite = False
            if cmd[1] == ">":
                overwrite = True
                if len(cmd) == 2:
                    t.print(f"{t.msg}Must give a file name to save to")
                    return
                name = P(cmd[2:].strip())
            else:
                name = P(cmd[1:].strip())
            if name.exists() and not overwrite:
                t.print(f"{t.msg}Can't overwrite existing file")
                return
            try:
                Save(name)
            except Exeption as e:
                t.print(f"{t.msg}[{Lineno()}] Save exception: {e}")
        elif cmd[0] == "<":
            if len(cmd) == 1:
                t.print(f"{t.msg}Must give a file name to read from")
                return
            name = P(cmd[1:].strip())
            if not name.exists():
                t.print(f"{t.msg}File '{name}' doesn't exist")
                return
            rv = Load(name)
            if rv is None:
                t.print(f"{t.msg}Couldn't read file '{name}'")
        elif cmd == "%":
            mdl.pct = not mdl.pct
            print(mdl)
        elif cmd == "/":
            mdl.reset()
        elif cmd == "//":
            mdl.reset(hard=True)
        elif cmd == "?":
            Help()
        else:
            t.print(f"{t.msg}{cmd!r} is an unrecognized command")
    def SetUp():
        'Use to set the model to a desired state for testing/debugging'
        mdl.sto("c", "tau")
        mdl.sto("s", "14.227")
    def Lineno():
        'Return line number of last exception'
        typ, val, tb = sys.exc_info()
        return tb.tb_lineno
    def Loop(mdl):
        if d["-h"]:
            Intro()
        if d["-d"]:
            SetUp()
        Colors(mdl.color)
        while True:
            e = input(f"> ").strip()
            if not e:
                continue
            cmds = e.split(";")
            for cmd in cmds:
                bad = ProcessCommand(cmd)
                if bad:
                    break
    def ProcessCommand(cmd):
        'Return True if command fails'
        name = cmd[0]
        if name == "#":
            # It's a comment
            pass
            return False
        elif "=" in cmd:
            # Local variable assignment
            name, value = cmd.split("=", 1)
            try:
                x = eval(value, globals(), mdl.vars)
            except Exception as e:
                if edbg: raise
                t.print(f"{t.msg}[{Lineno()}] Local variable exception:\n {e}")
                return True
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
                if edbg: raise
                t.print(f"{t.msg}[{Lineno()}] Primary variable exception:\n {e}")
                return True
            if mdl.ok:
                print(mdl)
        else:
            # It must be a command
            try:
                Command(cmd)
            except Exception as e:
                if edbg: raise
                t.print(f"{t.msg}[{Lineno()}] Command exception:\n {e}")
                return True
        return False

if __name__ == "__main__":
    # Note:  there's no locking, so if you run this script in two different
    # processes, you'll have a race condition for the persisted data.
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    edbg = d["-e"]
    modelfile = GetFile()
    mdl = Load(modelfile)
    if mdl is None:
        mdl = Model()
    if args or d["-d"]:
        SetUp()
    Loop(mdl)
