'''

Interactive utility to calculate profit and markup
    - The basic use case is to estimate the order of magnitude of the
      profitability of a project.

    Problem variables (number in [] is default)
        c = cost = L + PS
            L = labor cost = dph*hr         [0]
                dph = $/hr of labor         [20]
                hr = hours of labor         [0]
            PS = cost of parts & supplies   [0]
        s = selling price
        p = profit as a fraction of s
        m = markup as a fraction of c
        u = multiplier = s/c

    Commands
        - ?             Help
        - ??            Detailed help
        - q or quit     Quit, writing registers to disk
        - QUIT          Force quit without rewriting to disk
        - reset         Set to default state
        - > 'name'      Save state to register 'name'
        - < 'name'      Restore state to register name
        - del name      Delete a variable
        - del 'name'    Delete a register
        - ls            Show listing of register names
        - k             Toggle colorizing
        - #             Enter editor for project's comments
        = ! cmd         Execute a python command

        At exit (but not if QUIT was used), the current state of the script is always saved in register
        'LAST' and this state will be restored at the next invocation.

    Local variables

        Any line input with '=' in it sets a variable.  Any variable that is
        not a problem variable is considered a local variable.
        
    Registers
        
        All registers are stored in an internal dictionary that is written to
        disk at exit.  A lockfile prevents another process from writing to this
        file if another process has it open.

    Equations
        c = s*(1 - p) = L + F
        s = c*(1 + m)
        p = m/(1 + m) = 1 - 1/u
        m = s/c = p/(1 - p)
        u = 1/(1 - p) = multiplier
        m = p*u

    The above variables are printed out when you start the program.  If they
    are not defined, the value is None.  Then you enter commands like 'c = 10'.
    When there are enough variables, all None variables are calculated and you
    can continue entering changes.  Expressions are allowed.

    This should also include the ability to let you enter '.' when
    you are prompted for cost.  You're then prompted for $/hr for labor (enter
    '.' to use a default value), number of hours labor, and parts cost.  This
    gives you a total cost and lets you put a cost on your time.


    Desired interface
        - Message prompts for 3 of c, s, p, m, or u
            - Need to solve given csp csm csu cpm cpu cmu spm spu smu pmu
        - Once got requisite set, it prints report in color
        - Then prompts you to enter changes to the variables such as
        'c *= .9'.  These are expressions that are evaluated with the
        above local variables.  You can also enter any other variables
        you want.  
        - Entering 'ns = "name"' defines a namespace and this problem's
        variables are saved under this name.  You can't overwrite an existing
        namespace without using 'del "name"'.

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
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        # Colors
        t.prompt = t("magl")
        t.cmdline = t("cynl")
        t.dbg = t("ornl")
        t.err = t("redl")
        prompt = f"{t.prompt}>> {t.n}"
        #
        class g: pass
        g.dbg = True
        g.vars = {}     # Dictionary for variables
        g.names = {     # Core variable names
            "c": "Cost = L + PS",
            "L": "Labor = dph*hr",
            "dph": "Labor cost $/hour",
            "hr": "Hours of labor", 
            "PS": "Cost of parts & supplies",
            "s": "Selling price", 
            "p": "Profit as a fraction of s",
            "m": "Markup as a fraction of c",
            "u": "Multiplier = s/c",
        }
        g.core = {}
        for i in g.names:
            g.core[i] = None
        g.cmds = set("? ?? q quit QUIT reset > < del ls k # !".split())
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = 3         # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h", 
                    ["help", "debug"])
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
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        return args
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.n}", end="")
    def Err(e):
        t.print(f"{t.err}Error:  {e}")
if 1:   # Core functionality
    def SetUpVariables():
        # Set up core variables
        for i in g.core_variables:
            g.vars[i] = None
        g.vars["dph"] = 20  # $/hr equivalent for labor
    def Variable(s):
        name, value = [i.strip() for i in s.split("=", 1)]
        try:
            val = eval(value, globals(), g.vars)
            g.vars[name] = val
            Dbg(f"name = {name!r}, value = {val}")
        except Exception as e:
            Err(e)
if 1:   # Command dispatch
    def Help(*p, **kw):
        pass
    def HELP(*p, **kw):
        pass
    def Quit(*p, **kw):
        pass
    def Reset(*p, **kw):
        pass
    def StoreRegister(*p, **kw):
        pass
    def RecallRegister(*p, **kw):
        pass
    def Delete(*p, **kw):
        pass
    def ShowState(*p, **kw):
        print(g.vars)
    def ToggleColorizing(*p, **kw):
        pass
    def EditNote(*p, **kw):
        pass
    def ToggleDbg(*p, **kw):
        g.dbg = not g.dbg
    def ExecutePythonCommand(*p, **kw):
        cmd = p[0]
        try:
            exec(cmd, globals(), g.vars)
        except Exception as e:
            Err(e)
if 1:   # Command loop
    def Command(s):
        if s == "ls":
            ShowState()
        elif s == "dbg":
            ToggleDbg()
        elif s.startswith("!"):
            cmd = s[1:].strip()
            ExecutePythonCommand(cmd)
    def CommandLoop():
        quit = False
        while not quit:
            print(prompt, end="")
            s = input().strip()
            t.out()     # Turn off prompt colorizing
            if s in "q quit".split():
                quit = True
            elif "=" in s:
                Variable(s)
            elif s:
                Command(s)
            if 1:
                print(f"{t('cyn')}vars:")
                pp(g.vars, compact=1)
                print(f"{t.n}", end="")
if __name__ == "__main__":
    # This variable has to be after the dispatch functions are defined
    g.dispatch = {
        "?": Help,
        "??": HELP,
        "q": Quit,
        "quit": Quit,
        "QUIT": Quit,
        "reset": Reset,
        "<": StoreRegister,
        ">": RecallRegister,
        "del": Delete,
        "ls": ShowState,
        "k": ToggleColorizing,
        "#": EditNote,
        "!": ExecutePythonCommand,
        "dbg": ToggleDbg,
    }
    d = {}          # Options dictionary
    args = ParseCommandLine(d)
    CommandLoop()
