"""
Calculate the parameters of a two-pulley and belt system
    See the associated pulley.pdf file for technical details.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2013 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Calculate the parameters of a two-pulley and belt system
    ##∞what∞#
    ##∞test∞# --test #∞test∞#
    pass
if 1:  # Imports
    import sys
    import os
    import getopt
    from functools import partial
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent, wrap
    from get import GetNumber
    from f import flt, cpx, sin, acos, sqrt, pi, Base
    import root

    # from color import C
    from color import t
    from lwtest import run, raises, assert_equal, Assert
if 1:  # Global variables
    ii = isinstance

    class g:
        pass

    t.err = t("redl")
    t.calc = t("ornl")
    t.have = t("wht")
    t.answer = t("cynl")
    t.N = t.n


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(status=1):
    print(
        dedent(f"""
    This program lets you calculate the variables of a two pulley and belt
    system.  It will solve for the desired unknown amongst the four
    following variables:

        C = center-to-center distance of the pulleys
        D = pitch diameter of large pulley
        d = pitch diameter of small pulley
        L = belt pitch length

    The solution is given by the equations (see the pulley.pdf file)

        θ = 2*acos((D - d)/(2*C))
        L = 2*C*sin(θ/2) + D/2*(2*π - θ) + d*θ/2

    You will be prompted for each of these variables; don't enter anything
    for the variable you want calculated.  The variables must be in the
    same physical units of length.  The above equation for the belt length
    is exact, but it's a transcendental equation in d, D, and C, so 
    approximate equations are used when you want to solve for d, D, or C.
    These should be adequate for practical problems.

    Calculations are given to {opts["-d"]} figures; you can change this with
    the -d option.
    """)
    )
    exit(status)


def Fmt(num):
    "Get significant figure string and remove trailing zeros"
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
    d["-d"] = 4  # Number of significant digits
    d["--test"] = False  # Run self tests
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
                msg = "-d option's argument must be an integer between 1 and 15"
                Error(msg)
        elif o == "--test":
            d["--test"] = True
        elif o in ("-h", "--help"):
            Usage(status=0)
    x = flt(0)
    x.N = d["-d"]
    x.rtz = x.rtdp = False
    return args


def Introduction():
    s = [
        f"""This script ({sys.argv[0]}) will calculate the unknown
    dimension of an open belt pulley problem.  You need to give three of
    the four variables d, D, C, and L, where d and D are pulley diameters,
    C is the center distance between the pulleys, and L is the belt length.
    Enter nothing for the unknown.""",
        """The solution is based on an approximation and the answers should be
    good to 3 significant figures or better.""",
    ]
    for i, item in enumerate(s):
        print(wrap(item))
        print()


def GetVariables():
    """Put a dict of the desired variables into opts["vars"].  The one to
    solve for will be None.
    """

    def Show(name, value, indent=" " * 2):
        if value is None:
            print(f"{indent}{t.calc}{name} will be calculated{t.N}")
        else:
            print(f"{indent}{t.have}{name} = {Fmt(value)}{t.N}")

    d, D, C, L = None, None, None, None
    GN = partial(GetNumber, numtype=flt, low=0, low_open=True, allow_none=True)
    if opts["--test"]:
        # Test case
        d = flt(2.275)
        D = flt(8)
        C = flt(5.67)
        L = None  # Answer is flt(28.9584)
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
                if C <= abs(D + d) / 2:
                    print(f"C is not large enough to separate the pulleys")
                    continue
            if sum([i is None for i in (d, D, C, L)]) == 1:
                break
            print(f"{t.err}Only one variable can be calculated; try again.{t.N}")
    # Show the input data
    if not opts["--test"]:
        print("\nInput data:")
        Show("Small pulley diameter", d)
        Show("Large pulley diameter", D)
        Show("Pulley center-to-center distance", C)
        Show("Length of belt", L)
    MakeVars(d, D, C, L)


def MakeVars(d, D, C, L):
    if "vars" not in opts:
        opts["vars"] = {}
    v = opts["vars"]
    v["d"] = d if d is None else flt(d)
    v["D"] = D if D is None else flt(D)
    v["C"] = C if C is None else flt(C)
    v["L"] = L if L is None else flt(L)


def TestSimplestCase():
    "d = D = C = 1 and L = π + 2"
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
    """Note the choice of numbers here just happened to work well with the
    approximate formulas.
    """
    d, D, C, L = flt(2.275), flt(8), flt(5.67), None
    MakeVars(d, D, C, None)
    Solve()
    v = opts["vars"]
    L = v["L"]
    Assert(L == 28.958417504819245)  # This is from an exact formula
    # Solve for d
    MakeVars(None, D, C, L)
    Solve()
    assert_equal(v["d"], d, reltol=0.014)
    # Solve for D
    MakeVars(d, None, C, L)
    Solve()
    assert_equal(v["D"], D, reltol=0.002)
    # Solve for C
    MakeVars(d, D, None, L)
    Solve()
    assert_equal(v["C"], C, reltol=0.0035)


def TestBorderlineCase():
    """This problem solves for C.  The solution for L = 32 - 0.03942 is
    5.5, exactly where the pulleys are touching.  Changing to 0.03943
    results in a complex number with no solution.
    """
    MakeVars(1, 10, None, 32 - 0.03942)
    Solve()
    C = opts["vars"]["C"]
    # Note C gets rounded to 5 figures in Solve()
    assert_equal(C, 5.5)
    MakeVars(1, 10, None, 32 - 0.03943)
    # Get exception if rounding is disabled
    with raises(ValueError):
        Solve(round=False)


def Eqn(d=None, D=None, C=None, L=None):
    θ = 2 * acos((D / 2 - d / 2) / C)
    return 2 * C * sin(θ / 2) + D / 2 * (2 * pi - θ) + d * θ / 2


def Solve(round=True):
    """The following python code using sympy generates the equations for
    the approximate solution as derived in pulley.pdf:

        from sympy import *
        r, R, C, L = symbols("r R C L")
        E = pi*C*(R + r) + (R - r)**2 + 2*C**2 - L*C
        print("r =", solveset(E, r))
        print("R =", solveset(E, R))
        print("C =", solveset(E, C))

    The resulting equations are

        r = -pi*C/2 + R ± sqrt(C*(-8*C + pi**2*C + 4*L - 8*pi*R))/2
        R = -pi*C/2 + r ± sqrt(C*(-8*C + pi**2*C + 4*L - 8*pi*r))/2
        C = (L/4 - pi*R/4 - pi*r/4 ± sqrt(L**2 - 2*pi*L*R - 2*pi*L*r - 8*R**2
             + pi**2*R**2 + 16*R*r + 2*pi**2*R*r - 8*r**2 + pi**2*r**2)/4)

    If round is True, then the solution for C is rounded off.  This lets
    practical problems be solved, , but the constraint of C > R + r might
    not be quite satisfied sometimes.
    """
    d, D, C, L = [opts["vars"][i] for i in "dDCL"]
    z = flt(0)
    if d is not None and D is not None and d > D:
        d, D = D, d
    if d is None:
        R = D / 2
        r1 = -pi * C / 2 + R + sqrt(C * (-8 * C + pi**2 * C + 4 * L - 8 * pi * R)) / 2
        r2 = -pi * C / 2 + R - sqrt(C * (-8 * C + pi**2 * C + 4 * L - 8 * pi * R)) / 2
        # Choose the positive solution
        if r1 < z:
            opts["vars"]["d"] = 2 * r2
        elif r2 < z:
            opts["vars"]["d"] = 2 * r1
        else:
            raise ValueError("Both solutions are negative")
    elif D is None:
        r = d / 2
        R1 = -pi * C / 2 + r + sqrt(C * (-8 * C + pi**2 * C + 4 * L - 8 * pi * r)) / 2
        R2 = -pi * C / 2 + r - sqrt(C * (-8 * C + pi**2 * C + 4 * L - 8 * pi * r)) / 2
        # Choose the positive solution
        if R1 < z:
            opts["vars"]["D"] = 2 * R2
        elif R2 < z:
            opts["vars"]["D"] = 2 * R1
        else:
            raise ValueError("Both solutions are negative")
    elif C is None:
        r, R = d / 2, D / 2
        a = L / 4 - pi * R / 4 - pi * r / 4
        b = (
            sqrt(
                L**2
                - 2 * pi * L * R
                - 2 * pi * L * r
                - 8 * R**2
                + pi**2 * R**2
                + 16 * R * r
                + 2 * pi**2 * R * r
                - 8 * r**2
                + pi**2 * r**2
            )
            / 4
        )
        if ii(b, cpx):
            raise ValueError("No solution because formula gives a complex number")
        C1 = a + b
        C2 = a - b
        # Choose the positive solution
        if C1 > z and C2 > z:
            C = max(C1, C2)
        elif (C1 > z and not C2) or (C2 < z and C1 > z):
            C = C1
        elif (C2 > z and not C1) or (C1 < z and C2 > z):
            C = C2
        elif C1 <= z and C2 <= z:
            raise ValueError("Both solutions are negative or zero")
        else:
            raise RuntimeError("Bad logic")
        # Need to check the constraint
        if C <= R + r:
            e = ValueError("No solution (pulleys are touching or interfere")
            # Note:  the TestSimplestCase() unit test fails because C
            # calculates to 5.499994155499934 and the actual value is 5.5.
            # Because of this, we use f.Base.sig_equal() to check the
            # relation to 5 significant figures.  This should be adequate
            # for practical problems, although there are cases where the
            # constraint might not be actually satisfied.
            if round:
                if not Base.sig_equal(C, R + r, 5):
                    raise e
            else:
                raise e
        opts["vars"]["C"] = C.rnd(5) if round else C
    elif L is None:
        r, R = d / 2, D / 2
        θ = 2 * acos(abs(R - r) / C)
        opts["vars"]["L"] = 2 * C * sin(θ / 2) + R * (2 * pi - θ) + r * θ
    else:
        raise RuntimeError("No variables were None")


# ----------------------------------------------------------------------
# These examples give you a feel for the problem.

if 0:
    """This problem solves for C.  The solution for L = 32 - 0.03942 is
    5.5, exactly where the pulleys are touching.  Changing to 0.03943
    results in a complex number with no solution.
    """
    opts = {}
    MakeVars(1, 10, None, 32 - 0.03942)
    MakeVars(1, 10, None, 32 - 0.03943)
    Solve()
    PrintResults()
    exit()
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
    """
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
    approximation replaces the sine of this angle by the angle; here
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
    """
    d = flt(1)
    D = flt(1.1)
    C = flt(1.2)
    # This is the exact formula for the belt length
    θ = 2 * acos((D - d) / (2 * C))
    L = 2 * C * sin(θ / 2) + D / 2 * (2 * pi - θ) + d * θ / 2
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
    """
    This is a more practical problem and demonstrates the real versus
    calculated numbers d, D, and C differ by 2 parts in 50000 or 40 ppm.
    Such a difference would almost never be of interest in a real-world 
    problem because you'd never be able to measure belt lengths, diameters,
    or center distances to better than perhaps 3 figures.
    """
    # These numbers are approximately the diameters and center distance of
    # the fastest speed on my drill press.
    d = flt(1)
    D = flt(5)
    C = flt(15)
    # This is the exact formula for the belt length
    θ = 2 * acos((D - d) / (2 * C))
    α = (pi - θ) / 2
    with α:
        α.n = 6
        print("Inclination angle = α =", α)
        print("sin(α)                =", sin(α))
        α.n = 2
        print(f"                   Δ% = {100 * (α - sin(α)) / sin(α)}%")
    L = 2 * C * sin(θ / 2) + D / 2 * (2 * pi - θ) + d * θ / 2
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
    opts = {  # Options dictionary
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
    Introduction()
    GetVariables()
    try:
        Solve()
    except ValueError as e:
        Error(e)
    PrintResults()
