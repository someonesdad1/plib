'''
Calculate features of a circle's segment
    The method is to use the formulas from pg 51 of the Analytic Geometry
    document, as it has formulas for the independent variables in pairs.
 
    Check data from a drawing on an A size piece of paper:
        r = 152.2
        θ = 90°
        d = 107.4
        h = 44.8
        b = 239.1
        s = 215.5
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Interactive script to calculate features of a circle's segment
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import os
    import re
    import subprocess
    import sys
    try:
        import readline         # History and command editing
        import rlcompleter      # Command completion
        have_readline = True
    except Exception:
        have_readline = False
    from pdb import set_trace as xx
    from pprint import pprint as pp
if 1:   # Custom imports
    from wrap import dedent
    from f import *
    from u import u, ParseUnit
    from cmddecode import CommandDecode
    from color import C
    import root
    if 0:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    class g:
        pass
    g.E = Exception("Not implemented")
    g.prompt = C.lred
    g.n = C.norm
    g.digits = flt(0).n
    g.vars = {}
    g.units = "mm"
    g.unc_short = re.compile(r"\(\d+\)")
def GetNumber(value, vars=None):
    '''The user has entered a number.  Interpret it as an expression
    evaluated as a flt.
    '''
    try:
        x = flt(eval(value, globals(), vars))
        return x
    except Exception:
        try:
            # Assume it's a number
            x = flt(value)
            return x
        except Exception:
            print(f"Couldn't evaluate '{value}'")
            return None
def GetCommand():
    'Return (command_string, arguments)'
    ok = False
    while not ok:
        s = ""
        while not s:
            s = input(f"{g.prompt}<seg>{g.n} ")
        if "=" in s:
            # Variable assignment
            exec(s, globals(), None)
            return ("", "")
        else:
            args = s.split()
            cmd = g.Cmd(args[0])
            if cmd == ["quit"]:
                exit()
            if not cmd:
                print(f"'{s}' not recognized as a command")
            elif len(cmd) > 1:
                print(f"'{s}' ambiguous; could be:")
                print(f"  {' '.join(cmd)}")
            else:
                return (cmd[0], args[1:])
if 1:   # Solve the problems
    def Get_theta_r():
        r, theta = g.vars["r"], g.vars["theta"]
        s = flt(2*r*sin(theta/2))
        h = flt(r*(1 - cos(theta/2)))
        b = flt(r*theta)
        g.vars.update(locals())
    def Get_theta_s():
        s, theta = g.vars["s"], g.vars["theta"]
        a = flt(2*sin(theta/2))
        r = flt(s/a)
        h = flt(s/2*tan(theta/4))
        b = flt(s*theta/a)
        del a
        g.vars.update(locals())
    def Get_theta_h():
        h, theta = g.vars["h"], g.vars["theta"]
        a = flt(1 - cos(theta/2))
        r = flt(h/a)
        s = flt(2*h/tan(theta/4))
        b = flt(h*theta/a)
        del a
        g.vars.update(locals())
    def Get_theta_b():
        b, theta = g.vars["b"], g.vars["theta"]
        r = flt(b/theta)
        s = flt(2*b*sin(theta/2)/theta)
        h = flt(b*(1 - cos(theta/2))/theta)
        g.vars.update(locals())
    def Get_r_s():
        r, s = g.vars["r"], g.vars["s"]
        theta = flt(2*asin(s/(2*r)))
        h = flt(r - sqrt(4*r*r - s*s)/2)
        b = flt(r*theta)
        g.vars.update(locals())
    def Get_r_h():
        r, h = g.vars["r"], g.vars["h"]
        theta = flt(2*acos(1 - h/r))
        s = flt(2*sqrt(h*(2*r - h)))
        b = flt(r*theta)
        g.vars.update(locals())
    def Get_r_b():
        r, b = g.vars["r"], g.vars["b"]
        theta = flt(b/r)
        s = flt(2*r*sin(b/(2*r)))
        h = flt(r*(1 - cos(b/(2*r))))
        g.vars.update(locals())
    def Get_s_h():
        h, s = g.vars["h"], g.vars["s"]
        theta = flt(4*atan(2*h/s))
        r = flt((s*s + 4*h*h)/(8*h))
        b = flt(r*theta)
        g.vars.update(locals())
    def Get_s_b():
        b, s = g.vars["b"], g.vars["s"]
        a = flt(2*b/s)
        f, fd = lambda x: flt(x - a*sin(x/2)), lambda x: flt(1 - a*cos(x/2)/2)
        g.vars["theta"] = flt(root.NewtonRaphson(f, fd, 1, eps=1e-15))
        del a, f, fd
        Get_theta_s()
        g.vars.update(locals())
    def Get_h_b():
        b, h = g.vars["b"], g.vars["h"]
        a = flt(h/b)
        f, fd = lambda x: flt(a*x + cos(x/2) - 1), lambda x: flt(a - sin(x/2)/2)
        g.vars["theta"] = flt(root.NewtonRaphson(f, fd, 1, eps=1e-15))
        del a, f, fd
        Get_theta_h()
        g.vars.update(locals())
def Help():
    def f(x):
        return f"[{g.vars[x]}]" if x in g.vars else ""
    print(dedent(f'''

    Enter two variables needed to solve for the properties of the segment of a circle.  The
    variables are (all lengths must be in the same units):
      r       Circle radius {f("r")}
      theta   Sector angle {f("theta")}(can also use 't')
      s       Chord width of sector {f("s")}
      h       Height of sector {f("h")}
      b       Arc length of sector {f("b")}
      u       Default length units to use [{g.units}]
    Entries should be like
        r 4.2 
    The angle theta is in degrees unless you include the unit 'rad' for radians (include a space).
    The number can be an expression like '4.2*sin(radians(12))' (the math module's symbols are in
    scope).

    A circular sector is the pie-shaped piece composed of a given angle.  The segment associated
    with this sector is the portion with the triangle removed, leaving only the arc and straight
    line.  It's the form of what you would get if you used scissors to make a straight cut through
    a disk.  If the cut goes through the center, you wind up with a semicircle.
 
    The solution will be given for the pairs of numbers
        r, θ        s, θ        h, θ        b, θ
        r, s        r, h        r, b        s, h
        b, s        b, h
    You can also make variable assignments like 
        y = 34.5
    These variables are put in the global namespace and you can use them in expressions.
 
    Other commands are (they can be abbreviated as needed):
      quit          Exit the script
      digits n      Set the number of significant digits [{flt(0).n}]
      picture       Show the bitmap of the problem's variables
      .             Print the currently solved problem
      dbg           Enter the debugger
      clear         Remove problem's variable definitions 
    '''))
def SolveProblem():
    'If g.vars is sufficient, print the solution'
    needed_pairs = p = dedent('''
        theta r
        theta s
        theta h
        theta b
        r s
        r h
        r b
        s h
        s b
        h b
    ''').split("\n")
    solved = False
    for i in needed_pairs:
        v1, v2 = i.split()
        if v1 in g.vars and v2 in g.vars:
            exec(f"Get_{i.replace(' ', '_')}()")
            solved = True
            break
    if solved:
        Report()
    else:
        print("Need more variables")
def Report():
    i = " "*4
    print(f"Results:")
    print(f"{i}θ = {flt(degrees(g.vars['theta']))}° = {flt(g.vars['theta'])} radians")
    print(f"{i}r = {g.vars['r']}")
    print(f"{i}h = {g.vars['h']}")
    print(f"{i}b = {g.vars['b']}")
    print(f"{i}s = {g.vars['s']}")
def Execute(cmd, args):
    def CheckArgs():
        if not args:
            print("Need argument for variable")
        return not bool(args)
    if args:
        value, unit = args[0], None
        if len(args) > 1:
            unit = args[1]
    if cmd == ".":
        pass
    elif cmd == "dbg":
        xx()
        return
    elif cmd == "digits":
        if CheckArgs():
            return
        try:
            n = int(args[0])
            if 1 <= n <= 15:
                flt(0).n = n
            else:
                raise Exception()
        except Exception:
            print("'{args[0]}' not an integer")
    elif cmd == "picture":
        p = P(sys.argv[0])
        f = p.resolve().parent
        os.chdir(f)
        subprocess.call(['c:/cygwin/home/Don/bin/app.exe', p.stem + ".png"])
        return
    elif cmd == "clear":
        g.vars.clear()
        return
    elif cmd == "quit":
        exit(0)
    elif cmd == "?":
        Help()
    elif cmd == "r":
        if CheckArgs():
            return
        g.vars["r"] = GetNumber(value, vars=None)
    elif cmd == "theta":
        if CheckArgs():
            return
        # Need to convert to radians.  It's assumed to be degrees unless
        # "rad" or "grad" are given for the units.
        t = flt(radians(flt(args[0])))
        if not 0 < t < pi:
            print("theta must be > 0 and < pi")
            return
        if len(args) > 1:
            u = args[1]
            if u == "rad":
                t = flt(args[0])
            elif u == "grad":
                t = flt(args[0])*pi/200
        g.vars["theta"] = flt(t)
    elif cmd == "s":
        if CheckArgs():
            return
        g.vars["s"] = GetNumber(value, vars=None)
    elif cmd == "h":
        if CheckArgs():
            return
        g.vars["h"] = GetNumber(value, vars=None)
    elif cmd == "b":
        if CheckArgs():
            return
        g.vars["b"] = GetNumber(value, vars=None)
    SolveProblem()
def TestCase():
    '''
    Check data from a drawing on an A size piece of paper:
        r = 152.2
        θ = 90°
        d = 107.4
        h = 44.8
        b = 239.1
        s = 215.5
    '''
    flt(0).n = 6
    # r, θ
    g.vars["r"] = flt(152.2)
    g.vars["theta"] = pi/2
    SolveProblem()
    g.vars.clear()
    # s, θ
    g.vars["s"] = flt(215.24)
    g.vars["theta"] = pi/2
    SolveProblem()
    g.vars.clear()
    # h, θ
    g.vars["h"] = flt(44.578)
    g.vars["theta"] = pi/2
    SolveProblem()
    g.vars.clear()
    # b, θ
    g.vars["b"] = flt(239.07)
    g.vars["theta"] = pi/2
    SolveProblem()
    g.vars.clear()
    # r, s
    g.vars["r"] = flt(152.2)
    g.vars["s"] = flt(215.24)
    SolveProblem()
    g.vars.clear()
    # r, h
    g.vars["r"] = flt(152.2)
    g.vars["h"] = flt(44.577)
    SolveProblem()
    g.vars.clear()
    # r, b
    g.vars["r"] = flt(152.2)
    g.vars["b"] = flt(239.07)
    SolveProblem()
    g.vars.clear()
    # s, h
    g.vars["s"] = flt(215.24)
    g.vars["h"] = flt(44.577)
    SolveProblem()
    g.vars.clear()
    # s, b
    g.vars["s"] = flt(215.24)
    g.vars["b"] = flt(239.07)
    SolveProblem()
    g.vars.clear()
    # h, b
    g.vars["h"] = flt(44.577)
    g.vars["b"] = flt(239.07)
    SolveProblem()
    g.vars.clear()
    print(dedent('''
    This test problem should give essentially the same answers for each of the
    test cases.'''))
    exit()
if __name__ == "__main__": 
    if len(sys.argv) == 2 and sys.argv[1] == "-t":
        TestCase()
    flt(0).n = 4
    g.variables = {}
    g.commands = sorted('''clear ? . quit digits picture dbg dump
                  r theta s h b u
                  '''.split())
    g.Cmd = CommandDecode(g.commands, ignore_case=True)
    Help()
    while True:
        cmd, args = GetCommand()
        if cmd == "":
            continue
        Execute(cmd, args)
