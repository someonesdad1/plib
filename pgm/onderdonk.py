'''
Bare copper wire fusing estimates based on Onderdonk's equation
    This equation says that the square of the (constant) current density multiplied by the duration
    of the constant current is a constant, getting the copper wire from the ambient temperature to
    the melting temperature of copper.  The heat of fusion is ignored and no heat loss is assumed
    for the wire.  Thus, the estimates are most relevant for "short" times, perhaps on the order of
    1 s or less.

'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2020 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Bare copper wire fusing estimates based on Onderdonk's equation
    #∞what∞#
    #∞test∞# --test #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import os
    import sys
    from pathlib import Path as P
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from u import u, ParseUnit, Dim
    from util import AWG
    from f import flt, log10, sqrt
    from lwtest import run, raises, assert_equal, Assert
if 1:   # Global variables
    Cu_melting_point_degC = flt(1083)
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def ManPage():
    print(dedent(f'''

    The formula used here is the "Onderdonk" equation, an approximation that underestimates things
    but is based on a straightforward derivation.  Heat loss from the copper wire is ignored, as is
    the heat of fusion of copper.  The estimate made is for the copper to reach copper's melting
    point temperature.  The key assumption in the derivation is that the heating time is short
    enough to ignore heat transfer to the environment (i.e., adiabatic conditions).  This is
    probably typical of short-circuit conditions in electrical circuits.  Physical intuition will
    tell us to not trust the results much for times longer than on the order of one second because
    the heat loss mechanisms (conduction, radiation, and convection) may be significant.

    The reference [adam] did some searching for the original literature; it turns out no one knows
    who Onderdonk was.  The 1928 paper by Stauffacher (referenced in [adam]) appears to be the
    earliest reference to Onderdonk, but just gives his or her name as I. M. Onderdonk.  [bab]
    gives a reference to J. M. Onderdonk in 1944.

    The problem being solved in Onderdonk's equation is a constant current flowing through a round
    copper wire for a given period of time.  The equation's derivation comes from equating the gain
    of thermal energy in the copper material (using the specific heat, mass, and temperature
    change) to the Joule heating of the wire by the current (using the resistance, current, and
    time).  The linear dependence of the resistivity on temperature is also used.  The resulting
    equation to be solved is a first order initial value problem where dθ/dt is proportional to θ
    and θ is the temperature offset from ambient temperature (the integral is of course θ = exp(t),
    which is where the logarithm in the solution comes from).  At time t = 0, the temperature of
    the copper wire will be equal to the ambient temperature.

    The basic result is that the wire's current density squared multiplied by the duration of the
    current is a constant.

    The heat of fusion of copper is 13 kJ/mol (or 205 kJ/kg).  To include this in the calculation
    would require knowing the mass of the copper; in the derivation of Onderdonk's equation in
    [adam], the length of the wire is canceled out, meaning we can't know the wire's mass.  See
    [bab] for calculations that include the heat of fusion.

    Onderdonk's Equation
        The equation used in this script is equation 3a from [adam]:

            (i/A)**2*t = C = log10(T/(234 + Ta) + 1)/33

        where
            i = current through the wire in A
            A = cross-sectional area of wire in circular mils (a circular mil is the area of a wire 
                of 1 mil diameter)
            t = time in s the constant current is applied to wire
            C = constant for a given Ta
            Ta = ambient temperature in °C

    Example
        From the nomograph in reference [4] in [adam], a 12 gauge (AWG) copper wire will heat to
        the melting point of copper in 1 second for a current of about 950 A.  From figure 1 in
        Stauffacher's paper (reference [5] in [adam]), the value is about 940 A.

        The script also prints a current predicted by the Preece equation.  This is an estimate of
        the current that will cause the copper wire to glow because it's hot enough to radiate in
        the visible range.  It predicts 29 A for 24 ga copper wire, and this is pretty close, as
        I've run such wires at 30 A and they are glowing red.

    References
        [adam] J. Adam and D. Brooks, "In Search of Preece and Onderdonk", 2015.
               https://www.ultracad.com/articles/preece.pdf
               [Defunct URL as of Feb 2024]

        [bab]  V. Babrauskas and I. Wichman, "Fusing of Wires by Electrical 
               Current", Fire & Materials, 2011,
               https://www.ultracad.com/articles/reprints/babrauskas.pdf
    '''))
    exit(0)
def Usage(d, status=1):
    name = P(sys.argv[0]).name
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] [dia] [time] [current]
      Estimates the current in A, wire size in mm, or time in s of bare copper to reach copper's
      melting point due to an electrical current.  The arguments must have units with no space
      between the number and unit (the arguments can be in any order).  Two arguments are required
      and the third is estimated.  You can use diameter units of AWG by appending 'ga' to the
      diameter.
 
      The physical model is to equate the energy needed to raise the copper material with a
      linearly-increasing resistivity with temperature from ambient temperature to its melting
      point of 1083 °C to the Joule heating of the wire due to the current.  The approximation is
      adiabatic, meaning heat losses from the wire are ignored.  This is an initial-value
      differential equation problem which is straightforward to solve.
 
      Times much longer than the order of about 1 second start to be where the assumptions break
      down and heat transfer to the environment starts to be more important.

    Examples:       (MPCu = melting point of copper)
      '{name} 12ga 1s'
        12 gauge copper wire (about 2 mm in diameter) will reach MPCu in about 1 second with a
        current of around 950 A.
      '{name} 18ga 0.1s'
        18 gauge copper wire (about 1 mm in diameter) will reach MPCu in about 0.1 second with a
        current of around 750 A.
    Options:
      -a t      Ambient temperature in °C [{d["-a"]}]
      -d n      Number of significant figures [{d["-d"]}]
      -h        Print a man page
      --test    Run basic test cases
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-a"] = 40        # Ambient temperature in °C
    d["-d"] = 2         # Number of significant digits
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:d:ht", "test")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-a",):
            try:
                d["-a"] = float(a) 
                if not (-100 <= d["-a"] <= 1000):
                    Error(f"-a option must be ∊ [-100, 1000] °C")
            except ValueError:
                Error(f"-a option's argument '{a}' not a float")
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
            ManPage()
        elif o in ("--test",):
            exit(run(globals(), halt=True)[0])
    if len(args) != 2:
        Usage(d)
    flt(0).n = d["-d"]
    return args
def GetArgument(arg):
    '''There must be an appended physical unit to the number.  We'll
    return (number, unit) where the number will be a floating point
    number and unit will be 'm', 's', or 'A'.
    '''
    x, unit = ParseUnit(arg)
    if unit == "ga":
        # Diameter in AWG
        awg = AWG(int(x))
        return (flt(awg*u("inch")), "m")
    else:
        # Get dimensions of unit
        dim = u.dim(unit)
        if dim == Dim("L"):
            # It's a length
            return (flt(x)*u(unit), "m")
        elif dim == Dim("T"):
            # It's a time
            return (flt(x)*u(unit), "s")
        elif dim == Dim("A"):
            # It's a current
            return (flt(x)*u(unit), "A")
        else:
            Error(f"'{arg}' has an unrecognized unit '{unit}'")
def GetVariables(args):
    '''Return (a, b) where a is (dia, t, i) in m, s, and A and b
    contains the diameter, time, and current strings the user entered
    and the resulting (DIA, T, I) strings, one of which will be None.
    '''
    arg0, arg1 = GetArgument(args[0]), GetArgument(args[1])
    dia, t, i = None, None, None
    DIA, T, I = None, None, None
    if arg0[1] == "m":
        dia = arg0[0]
        mm = flt(dia*1000)
        inches = mm/25.4
        DIA = f"Diameter = '{args[0]}' = {mm} mm = {inches} inches"
        if arg1[1] == "m":
            Error("Second argument can't also be a diameter")
        elif arg1[1] == "s":
            t = flt(arg1[0])
            T = f"Time     = '{args[1]}' = {t} s"
        else:
            i = flt(arg1[0])
            I = f"Current  = '{args[1]}' = {i} A"
    elif arg0[1] == "s":
        t = flt(arg0[0])
        T = f"Time     = '{args[0]}' = {t} s"
        if arg1[1] == "m":
            dia = flt(arg1[0])
            DIA = f"Diameter = '{args[1]}' = {dia} m"
        elif arg1[1] == "s":
            Error("Second argument can't also be a time")
        else:
            i = flt(arg1[0])
            I = f"Current  = '{args[1]}' = {i} A"
    else:
        i = flt(arg0[0])
        I = f"Current  = '{args[0]}' = {i} A"
        if arg1[1] == "m":
            dia = flt(arg1[0])
            DIA = f"Diameter = '{args[1]}' = {dia} m"
        elif arg1[1] == "s":
            t = flt(arg1[0])
            T = f"Time     = '{args[1]}' = {t} s"
        else:
            Error("Second argument can't also be a current")
    return ((dia, t, i), (DIA, T, I))
def Test():
    # Basic test case is 12 ga wire for 1 s should give around 950 A.
    DIA, T, I = 2.052e-3, 1, 947.0422770650215
    global d
    d = {"-a": 40, "-d": 8}
    flt(0).n = d["-d"]
    # Wire diameter and time
    a, b = CalculateResults([f"{DIA}m", f"{T}s"])
    dia, t, i = a
    Assert(dia == DIA and t == T and i == I)
    # Wire diameter and current
    a, b = CalculateResults([f"{DIA}m", f"{I}A"])
    dia, t, i = a
    Assert(dia == DIA and t == T and i == I)
    # Time and current
    a, b = CalculateResults([f"{T}s", f"{I}A"])
    dia, t, i = a
    Assert(dia == DIA and t == T and i == I)
def DiameterToCircMils(dia_m):
    '''Convert dia_m, a diameter in m, to an area in circular mils.
    '''
    d_inches = dia_m/u("inch")
    d_mils = d_inches*1000
    return d_mils**2
def CircMilsToDiameter(cmil):
    '''Given an area cmil in circular mils, convert it to a circular
    diameter in meters.
    '''
    d = sqrt(cmil)      # Diameter in mils
    d = d/1000          # Diameter in inches
    return d*u("inch")  # Convert to m
def CalculateResults(args):
    '''The basic equation is
            (i/A)**2*t = log10(T/(234 + Ta) + 1)/33 = C
    where i is current in A, A is cross-sectional area of wire in
    circular mils, and t is time in seconds.  Ta is the ambient
    temperature in °C.  The equations for the independent variables are:
 
    Area:
        A = i*sqrt(t/C)    in circular mils
    Current:
        i = A*sqrt(C/t)
    Time:
        t = C*(A/i)**2
    '''
    a, b = GetVariables(args)
    dia, t, i = a
    DIA, T, I = b       # Input string information
    n = d["-d"] + 1     # Significant figures for diameter
    # Get the constant
    C = log10(Cu_melting_point_degC/(234 + d["-a"]) + 1)/33
    # Calculate results.  Note the physical units are base SI units of
    # m, s, and A.  Note to use the Onderdonk equation we change
    # diameter to circular mils and calculate the area of the wire as
    # the square of the diameter in circular mils.
    if dia is None:
        A_cmil = i*sqrt(t/C)
        dia = CircMilsToDiameter(A_cmil)
        mm = dia*1000
        inches = mm/25.4
        DIA = f"Diameter = {mm} mm = {inches} inches"
    elif t is None:
        A = DiameterToCircMils(dia)
        t = C*(A/i)**2
        T = f"Time     = {t} s"
    elif i is None:
        A = DiameterToCircMils(dia)
        i = A*sqrt(C/t)
        I = f"Current  = {i} A"
    else:
        raise Exception("Logic error")
    return ((dia, t, i), (DIA, T, I))
def Report(args):
    a, b = CalculateResults(args)
    dia, t, i = a
    DIA, T, I = b
    print(dedent(f'''    Estimated conditions from Onderdonk's equation for round copper 
    wire at {d["-a"]} °C ambient to reach the melting point of copper (1083 °C)
        {DIA}
        {T}
        {I}'''))
    # Preece's equation
    k = 10244*(dia/u("inch"))**1.5
    print(f"    Glow     = {k} A (Preece)")
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    Report(args)
