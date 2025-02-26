"""
Calculate features of a circle's segment

    The method is to use the formulas from pg 51 of the Analytic Geometry document, as it has
    formulas for the independent variables in pairs.

    Alas, the symbols used in the document are poor, as I used s for the chord length and b for the
    arc length.  s is almost always used for arc length and it catches me every time I use the
    program, but it's too much work to change the document and its formulas.

    Check data from a drawing on an A size piece of paper in mm:
        r = 152.2       Radius of circle
        θ = 90°         Central angle of circle's sector
        d = 107.4       d + h == r
        h = 44.8        Height of segment
        b = 239.1       Arc length = r*θ
        s = 215.5       Chord length

    This tool solves a puzzle I remember someone gave me when I was a student:

        A train track rail is 10000 meters long and flat.  During the night, a prankster welds in
        another meter of rail, causing the rail to bow upwards in a circle (the ends of the rails
        were such that they couldn't move, only pivot).  How far above the ground is the rail if
        the circular arc is in a vertical plane?  Note the length of the rail only increased by a
        hundredth of a percent.

    If you enter into the script

        b 10001
        s 10000

    you'll get the output

        θ = 2.80681° = 0.0489881 radians
        r = 204152.
        h = 61.2382
        b = 10001.0
        s = 10000.0

    The thing that surprises folks is that the rail is 61.2 m (200 feet) over your head.  The root
    cause of this is that the circle is large.  If the circle were sitting on the Earth's surface
    and in a vertical plane, the other side of the circle would be well into outer space, as it's
    400 km away and outer space is approximately 100 km above the Earth's surface.

    This puzzle was given to beginning college students because a good way to solve it is to use
    the first two terms of the power series for the sine, which they would have learned in their
    basic calculus class -- and you can solve the problem easily with pencil and paper.  The final
    numerical answer can be gotten to three figures with a slide rule, which is how we did it when
    I was in college in the 1960's.  The script solves the problem to 15 figures with a
    Newton-Raphson root finder for the implicit equation for the angle θ.

    I sent this to a friend and he used the "obvious" approximation of the Pythagorean theorem,
    something that didn't occur to me even though I was looking right at the appropriate triangle.
    I looked at this problem again in 2024 to check the math, as I wrote this script about 25 years
    ago and remembered the table of equations in Machinery's Handbook had a number of errors in
    them, as I couldn't get the correct numerical answers and had to derive the equations myself.
    Thus, this rail track problem and the above drawing on paper are good checks of the numerical
    methods used.

"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Interactive script to calculate features of a circle's segment
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        from pathlib import Path as P
        import os
        import re
        import sys

        try:
            import readline  # History and command editing
            import rlcompleter  # Command completion

            have_readline = True
        except Exception:
            have_readline = False
    if 1:  # Custom imports
        from wrap import dedent
        from f import flt, pi, degrees, radians, sin, cos, tan, sqrt, asin, acos, atan
        from u import u, ParseUnit
        from cmddecode import CommandDecode
        from color import t
        from launch import Launch
        import root
        from wsl import wsl

        if 0:
            import debug

            debug.SetDebugger()
    if 1:  # Global variables

        class g:
            pass

        g.E = Exception("Not implemented")
        t.prompt = t("ornl")
        t.N = t.n
        g.vars = {}
        g.units = "mm"
        g.unc_short = re.compile(r"\(\d+\)")
        # Set the number of significant figures
        x = flt(0)
        x.rtz = x.rtdp = False
        g.digits = x.N = 6
if 1:  # Utility

    def GetNumber(value, vars=None):
        """The user has entered a number.  Interpret it as an expression
        evaluated as a flt.
        """
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
        "Return (command_string, arguments)"
        ok = False
        while not ok:
            s = ""
            while not s:
                s = input(f"{t.prompt}<seg>{t.n} ")
            if "=" in s:
                # Variable assignment
                exec(s, globals(), None)
                return ("", "")
            else:
                args = s.split()
                cmd = g.Cmd(args[0])
                if cmd == ["quit"]:
                    exit(0)
                if not cmd:
                    print(f"'{s}' not recognized as a command")
                elif len(cmd) > 1:
                    print(f"'{s}' ambiguous; could be:")
                    print(f"  {' '.join(cmd)}")
                else:
                    return (cmd[0], args[1:])

    def TestCase():
        """
        Check data from a drawing on an A size piece of paper:
            r = 152.2
            θ = 90°
            d = 107.4
            h = 44.8
            b = 239.1
            s = 215.5
        """
        Nlt(0).N = 6
        # r, θ
        g.vars["r"] = flt(152.2)
        g.vars["theta"] = pi / 2
        SolveProblem()
        g.vars.clear()
        # s, θ
        g.vars["s"] = flt(215.24)
        g.vars["theta"] = pi / 2
        SolveProblem()
        g.vars.clear()
        # h, θ
        g.vars["h"] = flt(44.578)
        g.vars["theta"] = pi / 2
        SolveProblem()
        g.vars.clear()
        # b, θ
        g.vars["b"] = flt(239.07)
        g.vars["theta"] = pi / 2
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
        print(
            dedent("""
        This test problem should give essentially the same answers for each of the
        test cases.""")
        )
        exit()


if 1:  # Solve the problems

    def Get_theta_r():
        r, theta = g.vars["r"], g.vars["theta"]
        s = flt(2 * r * sin(theta / 2))
        h = flt(r * (1 - cos(theta / 2)))
        b = flt(r * theta)
        g.vars.update(locals())

    def Get_theta_s():
        s, theta = g.vars["s"], g.vars["theta"]
        a = flt(2 * sin(theta / 2))
        r = flt(s / a)
        h = flt(s / 2 * tan(theta / 4))
        b = flt(s * theta / a)
        del a
        g.vars.update(locals())

    def Get_theta_h():
        h, theta = g.vars["h"], g.vars["theta"]
        a = flt(1 - cos(theta / 2))
        r = flt(h / a)
        s = flt(2 * h / tan(theta / 4))
        b = flt(h * theta / a)
        del a
        g.vars.update(locals())

    def Get_theta_b():
        b, theta = g.vars["b"], g.vars["theta"]
        r = flt(b / theta)
        s = flt(2 * b * sin(theta / 2) / theta)
        h = flt(b * (1 - cos(theta / 2)) / theta)
        g.vars.update(locals())

    def Get_r_s():
        r, s = g.vars["r"], g.vars["s"]
        theta = flt(2 * asin(s / (2 * r)))
        h = flt(r - sqrt(4 * r * r - s * s) / 2)
        b = flt(r * theta)
        g.vars.update(locals())

    def Get_r_h():
        r, h = g.vars["r"], g.vars["h"]
        theta = flt(2 * acos(1 - h / r))
        s = flt(2 * sqrt(h * (2 * r - h)))
        b = flt(r * theta)
        g.vars.update(locals())

    def Get_r_b():
        r, b = g.vars["r"], g.vars["b"]
        theta = flt(b / r)
        s = flt(2 * r * sin(b / (2 * r)))
        h = flt(r * (1 - cos(b / (2 * r))))
        g.vars.update(locals())

    def Get_s_h():
        h, s = g.vars["h"], g.vars["s"]
        theta = flt(4 * atan(2 * h / s))
        r = flt((s * s + 4 * h * h) / (8 * h))
        b = flt(r * theta)
        g.vars.update(locals())

    def Get_s_b():
        b, s = g.vars["b"], g.vars["s"]
        a = flt(2 * b / s)
        f, fd = lambda x: flt(x - a * sin(x / 2)), lambda x: flt(1 - a * cos(x / 2) / 2)
        g.vars["theta"] = flt(root.NewtonRaphson(f, fd, 1, eps=1e-15))
        del a, f, fd
        Get_theta_s()
        g.vars.update(locals())

    def Get_h_b():
        b, h = g.vars["b"], g.vars["h"]
        a = flt(h / b)
        f, fd = lambda x: flt(a * x + cos(x / 2) - 1), lambda x: flt(a - sin(x / 2) / 2)
        g.vars["theta"] = flt(root.NewtonRaphson(f, fd, 1, eps=1e-15))
        del a, f, fd
        Get_theta_h()
        g.vars.update(locals())


if 1:  # Core functionality

    def Help():
        def f(x):
            return f"[{g.vars[x]}]" if x in g.vars else ""

        print(
            dedent(f"""
    
        Enter two variables needed to solve for the properties of the segment of a circle.  The
        variables are (all lengths must be in the same units):
          r       Circle radius {f("r")}
          theta   Segment angle {f("theta")}(can also use 't')
          s       Chord width of segment {f("s")}
          h       Height of segment {f("h")}
          b       Arc length of segment {f("b")}
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
          digits n      Set the number of significant digits [{flt(0).N}]
          picture       Show the bitmap of the problem's variables
          .             Print the currently solved problem
          dbg           Enter the debugger
          clear         Remove problem's variable definitions 
        """)
        )

    def SolveProblem():
        "If g.vars is sufficient, print the solution"
        needed_pairs = p = dedent("""
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
        """).split("\n")
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
        i = " " * 4
        print(f"Results:")
        print(
            f"{i}θ = {flt(degrees(g.vars['theta']))}° = {flt(g.vars['theta'])} radians"
        )
        print(f"{i}r = {g.vars['r']}")
        print(f"{i}h = {g.vars['h']}")
        print(f"{i}b = {g.vars['b']}")
        print(f"{i}s = {g.vars['s']}")
        # Report area
        r, θ = g.vars["r"], g.vars["theta"]
        A = flt(r**2 * (θ - sin(θ)) / 2)
        print(f"{i}area = {A}")

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
            breakpoint()  # xx
            return
        elif cmd == "digits":
            if CheckArgs():
                return
            try:
                n = int(args[0])
                if 1 <= n <= 15:
                    flt(0).N = n
                else:
                    raise Exception()
            except Exception:
                print("'{args[0]}' not an integer")
        elif cmd == "picture":
            Launch(P("/plib/pgm/seg.png"))  # Open the file /plib/pgm/seg.png
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
            if not 0 < t <= pi:
                print("theta must be > 0 and <= pi")
                return
            if len(args) > 1:
                u = args[1]
                if u == "rad":
                    t = flt(args[0])
                elif u == "grad":
                    t = flt(args[0]) * pi / 200
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


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "-t":
        TestCase()
    flt(0).N = 4
    g.variables = {}
    g.commands = sorted(
        """clear ? . quit digits picture dbg dump
                  r theta s h b u
                  """.split()
    )
    g.Cmd = CommandDecode(g.commands, ignore_case=True)
    Help()
    while True:
        cmd, args = GetCommand()
        if cmd == "":
            continue
        Execute(cmd, args)
