'''

ToDo
    - Problems to add
        - Inverse problem:  given an orifice diameter and height, calculate the volume
          of the tank if you know the time it takes to drain.
        - Right frustum
            - Specify A1 = A(h1) and A2 = A(h2), h1 != h2 (areas at two heights)
            - Volume is then Δh/3*(A1 + A1 + sqrt(A1*A2))
            - Examples
                - Conical
                - Rectangular:  water tank in our RV, pond
                - Regular polygon
        - Elliptical horizontal tank like tanker truck (includes horizontal cylinder)
            - Dished or flat ends
        - Numerical integration with numpy should be straightforward
        - Plumbing connected to drain, such as in our trailer.  This will require
          estimating the friction losses for each of the components.  This problem
          solution is needed, as our trailer's tank drains much more slowly than if
          there was a 12 mm hole in the bottom (the diameter of the tubing).
            - The trailer's tank calculation is for a cylinder and given a volume of 26
              gal, height of 3 inches, hole diameter of 12 mm, and default coefficient
              of discharge gives 15.4 minute to drain.  I'd guess it takes more like 45
              minutes, though I haven't measured this on one fell swoop.  First 5
              gallons took about 5.5 minute to drain; as the water drops, the head also
              drops and each unit volume will take longer.

Time to drain a tank of water
    Ref. https://en.wikipedia.org/wiki/Torricelli%27s_law
'''
if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright © 2022 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Time to drain a tank of water
    ##∞what∞#
    ##∞test∞# #∞test∞#
    # Standard imports
    import getopt
    import os
    from pathlib import Path as P
    import sys
    from pdb import set_trace as xx
    # Custom imports
    from wrap import wrap, dedent
    from color import t
    from f import flt, pi, sqrt
    import u
    # Global variables
    class G:
        pass
    g = G()
    g.g = 9.81  # Acceleration of gravity
    g.Vs = 0    # Volume input string
    g.V = 0     # Volume in m³
    g.hs = 0    # Height input string
    g.h = 0     # Height of fluid level in m
    g.Ds = 0    # Hole diameter input string
    g.D = 0     # Hole diameter in m
    g.Cs = 0    # Coefficient of discharge input string
    g.μ = 0     # Coefficient of discharge 
    g.msg = ""  # Test case message

if 1:  # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(
            dedent(f'''
        Usage:  {sys.argv[0]} [options]
          Interactive script to calculate the time it takes to drain a tank.
        Options:
            -h      Print a manpage
        ''')
        )
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 3  # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:h", ["help"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
        x = flt(0)
        x.n = d["-d"]
        return args
if 1:  # Core functionality
    def PrintMessage():
        print(dedent('''
        Calculate the time to drain a cylindrical tank of water (or fluids with viscosities
        near water) through a hole.  You'll be asked for a tank volume in m³, a height in m,
        and a drain hole diameter in m.  If you want to use other units, append them to the
        number you type in.
        
        The discharge coefficient is the fraction of the ideal mass flow capable through the
        hole; it's a fraction of ρ*dV/dt with typical values for sharp holes around 0.6 to
        0.65.  Some other values are:
            Smoothly rounded    0.98
            Short tube          0.8
            Sharp               0.6 to 0.65
            Borda               0.51 (short tube protruding inside tank)
        
        Example:  a 50 gallon drum of water 1 m high with a 1 inch hole hole in the bottom
        will take 1.83 minutes.
        '''))
        print()
    def GetNumber(prompt, units, default=None):
        "Return (input, value_in_SI)"
        while True:
            s = input(prompt)
            if not s.strip() and default is not None:
                t, un = default, units
                return ("", flt(t) * u.u(un))
            else:
                t, un = u.ParseUnit(s, allow_expr=True)
                try:
                    needed_units = u.dim(units)
                    got_units = u.dim(un)
                    if needed_units != got_units:
                        raise ValueError(
                            f"Must enter units with dimensions '{u.dim(units)}'"
                        )
                    return (s, flt(t) * u.u(un))
                except Exception as e:
                    print(e)
                    print("Try again")
    def TimeToDrain(hole_diameter, coeff_of_discharge, volume, height):
        'Return the time to drain the tank in seconds'
        d = hole_diameter
        μ = coeff_of_discharge
        V = volume
        h = height
        g = 9.81  # Acceleration of gravity in m/s²
        A = pi*d**2/4  # Hole area in m²
        t = μ*V/A*sqrt(2/(h*g))  # Time to drain tank in s
        return t
    def GetProblem():
        # All units are SI
        #   V = Volume of tank
        #   h = Height of fluid at start of discharge
        #   D = Drain hole diameter
        #   μ = Coefficient of discharge
        problem = 0
        if problem == 0:
            g.Vs, g.V = GetNumber("What is volume? ", "m³")
            g.hs, g.h = GetNumber("What is height? ", "m")
            g.Ds, g.D = GetNumber("What is hole diameter? ", "m")
            g.Cs, g.μ = GetNumber("What is coefficient of discharge [0.65]?  ", "", 0.65)
        elif problem == 1:
            # 50 gal drum 1 m high with 1 inch hole
            g.Vs, g.V = "50 gal", flt(50) * u.u("gal")
            g.hs, g.h = "1 m", flt(1) * u.u("m")
            g.Ds, g.D = "1 in", flt(1) * u.u("in")
            g.Cs, g.μ = "0.65", flt(0.65)
            g.msg = "50 gallon drum test case"
            # Gives 1.83 minutes
        elif problem == 2:
            # This estimate was made for our sprayer draining through a chunk
            # of 1-1/4 inch pipe and it feels about right.
            g.Vs, g.V = "15 gal", flt(15) * u.u("gal")
            g.hs, g.h = "10 in", flt(10) * u.u("in")
            g.Ds, g.D = "1.38 in", flt(1.38) * u.u("in")
            g.Cs, g.μ = "0.65", flt(0.65)
            g.msg = "15 gallon sprayer tank test case"
            # Gives 34.3 s
        else:
            print("Unsupported problem number")
            exit(1)
    def PrintResults():
        A = pi*g.D**2/4  # Area in m²
        T = TimeToDrain(g.D, g.μ, g.V, g.h)
        # Colors
        t.title = t.ornl
        t.result = t.yel
        t.testcase = t.magl
        # Print report
        t.print(f"{t.title}Input data            User                 SI")
        print(f"  Volume              {g.Vs:20s} {g.V} m³")
        print(f"  Height              {g.hs:20s} {g.h} m")
        print(f"  Hole dia            {g.Ds:20s} {g.D} m")
        print(f"  Coeff of discharge  {g.Cs:20s} {g.μ}")
        print()
        if g.msg:
            t.print(f"{t.testcase}{g.msg}")
        if T >= 3600:
            t.print(f"{t.result}Drain time  {T/3600} hours")
        elif T >= 60:
            t.print(f"{t.result}Drain time  {T/60} minutes")
        else:
            t.print(f"{t.result}Drain time  {T} s")

if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    PrintMessage()
    GetProblem()
    PrintResults()
