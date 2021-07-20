'''
Calculate the parameters of a two-pulley and belt system
    A derivation for the belt length L is exact and results in a formula L
    = f(d, D, C).  Alas, f is a transcendental function and you cannot
    solve for the variables d, D, or C.  Thus, we must resort to
    approximation, root finding, or iteration.

    The typical handbooks (Marks, Machinery's Handbook) give approximate
    formulas that use 3 significant figures.  After studying these for a
    while and comparing the results to an exact formula, you'll find that
    typical problems can be solved to better than 1 part in 1000 with
    these approximate formulas.  These approximations are based on
    appoximating the sine of an angle with the angle itself.  This angle is
    α, the inclination angle (see first web page below for a picture) and
    it's the key to the whole derivation, as it determines the fundamental
    geometry.  It's the half-angle of the long sides of the belt tangent to
    the pulleys.  The fundamental relation is sin(α) = (R - r)/C where R is
    the large pulley radius, r is the small pulley radius, and C is the
    distance separating the center of the pulleys.  

    To give a feel for this, my drill press on fastest speed uses pulley
    diameters of 1 and 5, separated by 15.  Then
        sin(α) = (R - r)/C = (2.5 - 0.5)/15 = 2/15 = 0.13333
    and α = 0.13373, so the approximation is to about 4 parts in 1335 or 
    about 0.3%.  The approximate formula solves this problem to better
    than this, so it would handle this case just fine.

    I originally felt that I'd solve the transcentdental exact equation
    using a root finder.  On reflection about real-world problems, it's
    probably not worth the extra horsepower, since you'll probably be
    dealing with a system whose final settings will be adjusted anyway and
    you'll need to have adjustment to take up slack as the belt loosens
    over time.

    This, as of this writing, the algorithm for the belt length given the
    pulley diameters and center spacing is exact, the solving for the
    pulley diameters or center spacing given a belt length is given by
    approximate equations that will likely be good enough for practical
    problems.  The Marks book goes back to 1916 and on page 745 has the
    belt length equation, but the Google copy has the edge missing, so I
    can't read the whole equation.  The pictures showed in my copy of Marks
    (60 years later) are identical, so I suspect the equation is the same
    and it has stood the test of time for practical problems.  

    Thus, I felt no strong motivation to use more exact equation solving
    methods.

    https://www.tec-science.com/mechanical-power-transmission/belt-drive/calculation-of-the-belt-length/
        Has a good diagram and makes it clear that the core calculation for
        the problem is finding the inclination angle α.  Note that the wrap
        angles at each side is ±α, which is used to calculate the wrap
        angles π - 2*α and π + 2*α; these wrap angles multiplied by the
        pulley's radius gives the belt length around the pulley, making
        contact with the pulley.  The other two portions are l = sqrt(C**2
        - (R - r)**2) from the Pythagorean theorem.  We have

            α = asin((R - r)/C)
            where 
                R, r are the large and small pulley radii 
                C = center distance

        Once you have α, you can calculate the span length l = C*cos(α).  Then
        the belt length is

            L = 2*C*cos(α) + r*(pi - 2*α) + R*(pi + 2*α)

        He makes the good point that α in radians is often fairly small,
        meaning that it can be replaced by its sine, which is (R - r)/C,
        making the equations algebraically simpler.

        Let's look at a practical example.  On my drill press, the
        approximate diameters of the pulleys for the fastest speed (biggest
        diameter difference) are 
            
            d = 1, D = 4.8, C = 15
            α = asin((R - r)/C) = 0.12700
            (R - r)/C = 0.12667
            Δ% = 0.26%
            Thus, the approximation is good to about 1 part in 400.

            α ≅ (R - r)/C
            cos(α) ≅ 1 - α**2/2

        He then derives the approximate equation

            L ≅ 2*C + pi*(R + r) + (R - r)**2/(4*C)

        Multiplying through by C gives a quadratic equation for C:

            C ≅ b + sqrt(b**2 - 0.5*(R - r)**2)
            where
                b = L/4 - pi*(R + r)/4
        
        He also recommends (without attribution) that the center distance
        for a flat belt should be 
            
            1.4*(R + r) <= C <= 4(R + r)

    Marks 7th edition (1967) page 8-71 gives the formulas
        L = 2*C + pi*(D + d)/2 + (D - d)**2/(4*C)
        C = b/4 + 0.25*sqrt(b**2 - 2*(D - d)**2)
            where b = L - pi/2*(D + d)
        These are the same as derived at the previous web page link.  Marks
        makes the interesting point that for crossed belts the sum of the
        pulley diameters needs to be constant, but for non-crossed belts
        (open belts), the belt length is a function of both the sum and the
        difference of the pulley diameters, so no simple rule can be made.

        On page 8-73 is the comment:  For an open belt, the arc of contact on
        the smaller of two pulleys is approximately 
            
            180 - 60*(D - d)/C, in degrees

        The error is stated to be 1 part in 200 or less.

    Machinery's Handbook, 19th edition (1973, 5th printing) gives on page
        1050 the the same formulas that Marks gives.  

        Recommended center distance C:
            1.  Speed ratio < 3:  C = d + (D + d)/2
            2.  Speed ratio > 3:  C = D

    https://www.vcalc.com/wiki/MichaelBartmess/Two+Pulley+Belt+Length
        Gives a derivation of the length formula (note he writes a*sin(...)
        when he obviously meant the arc sine asin):

            R, r = large, small pulley radii
            C = distance between centers of pulleys
            a = R - r
            L = pi*(R + r) + 2*a*asin(a/C) + 2*sqrt(C**2 - a**2)
            Must have C >= R - r (otherwise the pulleys touch)
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2013 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Calculate the parameters of a two-pulley and belt system
    #∞what∞#
    #∞test∞# --test #∞test∞#
    pass
if 1:   # Imports
    import sys
    import os
    import getopt
    from functools import partial
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from get import GetNumber
    from f import flt, sin, acos, sqrt, pi
    import root
    from color import C
    from lwtest import run, raises, assert_equal, Assert
if 1:   # Global variables
    class g: pass
    g.err = C.lred
    g.calc = C.lwht
    g.have = C.wht
    g.answer = C.lcyn
    g.n = C.norm
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage():
    print(dedent(f'''
    This program lets you calculate the variables of a two pulley and belt
    system.  It will solve for the desired unknown amongst the four
    following variables:
        C = center-to-center distance of the pulleys
        D = pitch diameter of large pulley
        d = pitch diameter of small pulley
        L = belt pitch length
    The solution is given by the equations
    (https://en.wikipedia.org/wiki/Belt_problem#Pulley_problem)
        L = 2*C*sin(θ/2) + D/2*(2*π - θ) + d*θ/2
        θ = 2*acos((D - d)/(2*C))
    You will be prompted for each of these variables; don't enter anything
    for the variable you want calculated.  The variables must be in the
    same physical units of length.
    '''))
def Fmt(num):
    'Get significant figure string and remove trailing zeros'
    s = str(num)
    while s[-1] == "0":
        s = s[:-1]
    if s[-1] == ".":
        s = s[:-1]
    return s
def PrintResults():
    v = opts["vars"]
    d, D, C, L = [v[i] for i in "dDCL"]
    d.n = 6
    print("Results:")
    print("  C =", Fmt(C))
    print("  D =", Fmt(D))
    print("  d =", Fmt(d))
    print("  L =", Fmt(L))
def ParseCommandLine(d):
    d["-d"] = 4             # Number of significant digits
    d["--test"] = False     # Run self tests
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:h", "test")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-d",):
            try:
                d["-d"] = int(a)
                if not (1 <= d["-d"] <= 15):
                    raise ValueError()
            except ValueError:
                msg = ("-d option's argument must be an integer between "
                    "1 and 15")
                Error(msg)
        elif o == "--test":
            d["--test"] = True
        elif o in ("-h", "--help"):
            Usage(d, status=0)
    flt(0).n = d["-d"]
    return args
def GetVariables():
    '''Put a dict of the desired variables into opts["vars"].  The one to
    solve for will be None.
    '''
    def Show(name, value, indent=" "*2):
        if value is None:
            print(f"{indent}{g.calc}{name} will be calculated{g.n}")
        else:
            print(f"{indent}{g.have}{name} = {Fmt(value)}{g.n}")
    d, D, C, L = None, None, None, None
    GN = partial(GetNumber, numtype=flt, low=0, low_open=True, allow_none=True)
    if opts["--test"]:
        # Test case
        d = flt(2.275)
        D = flt(8)
        C = flt(5.67)
        L = None    # Answer is flt(28.9584)
    else:
        while True:
            msg = "C = center-to-center distance of the pulleys? "
            C = GN(msg, default=C)
            msg = "D = diameter of large pulley? "
            D = GN(msg, default=D)
            msg = "d = diameter of small pulley? "
            d = GN(msg, default=d)
            msg = "L = belt length? "
            L = GN(msg, default=L)
            # Check that pulleys aren't touching
            if C is not None and d is not None and D is not None:
                if C <= abs(D + d)/2:
                    print(f"C is not large enough to separate the pulleys")
                    continue
            if sum([i is None for i in (d, D, C, L)]) == 1:
                break
            print(f"{g.err}Only one variable can be calculated; try again.{g.n}")
    # Show the input data
    if not opts["--test"]:
        print("\nInput data:")
        Show("Small pulley diameter", d)
        Show("Large pulley diameter", D)
        Show("Pulley center-to-center distance", C)
        Show("Length of belt", L)
    MakeVars(d, D, C, L)
def MakeVars(d, D, C, L):
    opts["vars"] = {"d": d, "D": D, "C": C, "L": L}
def TestSimplestCase():
    'd = D = C = 1 and L = π + 2'
    # L is unknown
    d = D = C = flt(1)
    MakeVars(d, D, C, None)
    Solve()
    Assert(opts["vars"]["L"] == pi + 2)
    # d is unknown
    D = C = flt(1)
    MakeVars(None, D, C, pi + 2)
    Solve()
    Assert(opts["vars"]["d"] == 1)
    # D is unknown
    d = C = flt(1)
    MakeVars(d, None, C, pi + 2)
    Solve()
    Assert(opts["vars"]["D"] == 1)
    # C is unknown
    d = D = flt(1)
    MakeVars(d, D, None, pi + 2)
    Solve()
    Assert(opts["vars"]["C"] == 1)
def TestPracticalCase():
    '''Note the choice of numbers here just happened to work well with the
    approximate formulas.
    '''
    d, D, C, L = flt(2.275), flt(8), flt(5.67), None
    MakeVars(d, D, C, None)
    Solve()
    v = opts["vars"]
    L = v["L"]
    Assert(L == 28.958417504819245) # This is from an exact formula
    # Solve for d
    MakeVars(None, D, C, L)
    Solve()
    Assert(v["d"] == d)
    # Solve for D
    MakeVars(d, None, C, L)
    Solve()
    Assert(v["D"] == D)
    # Solve for C
    MakeVars(d, D, None, L)
    Solve()
    Assert(v["C"] == C)
def Eqn(d=None, D=None, C=None, L=None):
    θ = 2*acos((D/2 - d/2)/C)
    return 2*C*sin(θ/2) + D/2*(2*pi - θ) + d*θ/2
def Solve():
    '''The following code solves the equation given in Machinery's Handbook
    for the center distance of two pulleys, given their diameters and the
    belt length:
        from sympy import *
        d, D, C, L, b = symbols("d D C L b")
        # Equation at bottom of page 1050 in MH 19th ed.
        b = 4*L - 2*pi*(d + D)
        E = C - (b + sqrt(b**2 - 32*(D - d)**2))/16
        print(solveset(E, d))
        print()
        print(solveset(E, D))
        # Gives answers (note its same equations with d & D interchanged)
        # d = -pi*C + D ± sqrt(C*(-8*C + pi**2*C - 4*pi*D + 4*L))
        # D = -pi*C + d ± sqrt(C*(-8*C + pi**2*C - 4*pi*d + 4*L))
    Thus, this gives explicit equations for each of the problem's
    variables.  Thus, no implicit equation needs to be solved.
    '''
    d, D, C, L = [opts["vars"][i] for i in "dDCL"]
    if d is not None and D is not None and d > D:
        d, D = D, d
    if d is None:
        a = -pi*C + D 
        b = sqrt(C*(-8*C + pi**2*C - 4*pi*D + 4*L))
        x1 = a - b
        x2 = a + b
        # Choose the positive solution
        if x1 < 0:
            opts["vars"]["d"] = x2
        elif x2 < 0:
            opts["vars"]["d"] = x1
        else:
            raise ValueError("Both solutions are negative")
    elif D is None:
        a = -pi*C + d
        b = sqrt(C*(-8*C + pi**2*C - 4*pi*d + 4*L))
        x1 = a - b
        x2 = a + b
        # Choose the positive solution
        if x1 < 0:
            opts["vars"]["D"] = x2
        elif x2 < 0:
            opts["vars"]["D"] = x1
        else:
            raise ValueError("Both solutions are negative")
    elif C is None:
        # Equation from bottom of 8-71 in Marks 7th ed (gives same result
        # as equation from MH 19th ed., bottom of pg 1050)
        b = L - pi/2*(d + D)
        opts["vars"]["C"] = (b + sqrt(b**2 - 2*(D - d)**2))/4
    elif L is None:
        # Exact solution from 
        # https://en.wikipedia.org/wiki/Belt_problem#Pulley_problem
        r1, r2 = D/2, d/2   # r1 is radius of larger pulley
        assert(r1 >= r2)
        θ  = 2*acos((r1 - r2)/C)
        opts["vars"]["L"] = 2*C*sin(θ/2) + r1*(2*pi - θ) + r2*θ
    else:
        raise RuntimeError("No variables were None")
#----------------------------------------------------------------------
# These examples give you a feel for the problem.
if 0:
    # The simplest case is where d = D = C = 1 and L = π + 2.
    one = flt(1)
    one.n = 15
    opts = {}
    if 1: 
        MakeVars(1, 1, 1, None)
        Solve()
        print("Got for L    ", opts["vars"]["L"])
        print("Should equal ", pi + 2)
    if 1: 
        MakeVars(None, 1, 1, pi + 2)
        Solve()
        print("Got for d    ", opts["vars"]["d"])
        print("Should equal ", one)
    if 1: 
        MakeVars(1, None, 1, pi + 2)
        Solve()
        print("Got for D    ", opts["vars"]["D"])
        print("Should equal ", one)
    if 1: 
        MakeVars(1, 1, None, pi + 2)
        Solve()
        print("Got for C    ", opts["vars"]["C"])
        print("Should equal ", one)
    exit()
if 0:
    '''
    This case has the variables changed by about 10% from the simplest
    case.  This example demonstrates that the MH formula isn't correct,
    though the difference is small (to 9 figures) because the formula is an
    approximation.
 
    Note:  this calculation was repeated with mpmath numbers to 40 places;
    this repeat calculation demonstrated that these differences shown are
    real -- and probably due to the approximations used.
 
    The wikipedia page
    https://en.wikipedia.org/wiki/Belt_problem#Pulley_problem gives the
    exact solution.  The angle θ is 3.0582351887446375, meaning the 
    inclination angle α is (π - θ)/2 or 0.0416787324225778.  The
    approximation relaces the sine of this angle by the angle; here
        θ      = 0.0416787324225778
        sin(θ) = 0.0416666666666666
        Δ% = 0.29% or about 1 part in 350
 
    The formulas for d and D have a term with L under the square root.
    Thus, as a crude estimate, a 1 in 350 effect under the square root
    should have about a 1 in 350**2 effect, which works out to be about 
    8 ppm.  This is still about 2 orders of magnitude larger than the 
    effect, where e.g. 1.20000015091364 was gotten for C when 1.2 was the
    exact answer.
 
    The next example uses a much larger difference between the large and
    small pulleys.
    '''
    d = flt(1)
    D = flt(1.1)
    C = flt(1.2)
    # This is the exact formula for the belt length 
    θ = 2*acos((D - d)/(2*C))
    L = 2*C*sin(θ/2) + D/2*(2*pi - θ) + d*θ/2
    # Results in L = 5.70075592116790
    d.n = 15
    d.rtz = 1
    opts = {}
    if 1: 
        MakeVars(d, D, C, None)
        Solve()
        print("Got for L    ", opts["vars"]["L"])
        print("Should equal ", L)
        # This result is exact, but the following are only exact to about 7
        # figures.
    if 1: 
        MakeVars(None, D, C, L)
        Solve()
        print("Got for d    ", opts["vars"]["d"])
        print("Should equal ", d)
    if 1: 
        MakeVars(d, None, C, L)
        Solve()
        print("Got for D    ", opts["vars"]["D"])
        print("Should equal ", D)
    if 1: 
        MakeVars(d, D, None, L)
        Solve()
        print("Got for C    ", opts["vars"]["C"])
        print("Should equal ", C)
    exit()
if 0: 
    '''
    This is a more practical problem and demonstrates the real versus
    calculated numbers d, D, and C differ by 2 parts in 50000 or 40 ppm.
    Such a difference would almost never be of interest in a real-world 
    problem.
    '''
    # These numbers are approximately the diameters and center distance of
    # the fastest speed on my drill press.
    d = flt(1)
    D = flt(5)
    C = flt(15)
    # This is the exact formula for the belt length 
    θ = 2*acos((D - d)/(2*C))
    α = (pi - θ)/2
    with α:
        α.n = 6
        print("Inclination angle = α =", α)
        print("sin(α)                =", sin(α))
        α.n = 2
        print(f"                   Δ% = {100*(α - sin(α))/sin(α)}%")
    L = 2*C*sin(θ/2) + D/2*(2*pi - θ) + d*θ/2
    # Results in L = 39.6918418130462
    d.n = 15
    d.rtz = 1
    opts = {}
    if 1: 
        MakeVars(d, D, C, None)
        Solve()
        print("Got for L    ", opts["vars"]["L"])
        print("Should equal ", L)
    if 1: 
        MakeVars(None, D, C, L)
        Solve()
        print("Got for d    ", opts["vars"]["d"])
        print("Should equal ", d)
    if 1: 
        MakeVars(d, None, C, L)
        Solve()
        print("Got for D    ", opts["vars"]["D"])
        print("Should equal ", D)
    if 1: 
        MakeVars(d, D, None, L)
        Solve()
        print("Got for C    ", opts["vars"]["C"])
        print("Should equal ", C)
    exit()
if __name__ == "__main__":
    opts = {       # Options dictionary
        "vars": {
            "d": None,
            "D": None,
            "C": None,
            "L": None,
        },
    }
    args = ParseCommandLine(opts)
    if opts["--test"]:
        exit(run(globals(), halt=True, nomsg=1))
    GetVariables()
    Solve()
    PrintResults()
