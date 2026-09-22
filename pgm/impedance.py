'''
Given a measured impedance in polar coordinates, prints out the
associated parameters that can be calculated.
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Calculates various measures from a complex electrical impedance
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        import getopt
        import os
        import sys
    if 1:  # Custom imports
        from wrap import dedent
        from f import flt, tan, sin, cos, pi, isinf, radians
        from fpformat import FPFormat
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        ii = isinstance
if 1:  # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        print(
            dedent(f'''
        Usage:  {sys.argv[0]} [options] Z theta
          Given a measured impedance with magnitude Z in ohms and phase angle
          theta in degrees, prints out the associated parameters.  You can use
          a cuddled SI prefix after the number for Z if you wish (example:
          1.23k means 1230 ohms).
        Options
          -d n      Use n significant digits for output [{d["-d"]}]
          -f f      Specify measurement frequency in Hz.  You can use a cuddled SI 
                    prefix after the number.  [{d["-f"]} Hz]
        ''')
        )
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 3  # Number of significant digits
        d["-f"] = 1000  # Measurement frequency in Hz
        if len(sys.argv) < 2:
            Usage(d)
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "d:f:")
        except getopt.GetoptError as e:
            msg, option = e
            print(msg)
            exit(1)
        for o, a in optlist:
            if o == "-d":
                try:
                    d["-d"] = int(a)
                except ValueError:
                    Error("-d option invalid")
                if not (1 <= d["-d"] <= 15):
                    Error("-d option must be between 1 and 15")
            if o == "-f":
                try:
                    d["-f"] = Interpret(a)
                except ValueError:
                    Error("-f option invalid")
                if d["-f"] <= 0:
                    Error("-f option must be > 0")
        # sig.digits = d["-d"]
        flt(0).n = d["-d"]
        if len(args) != 2:
            Usage(d)
        return args
def Interpret(s):
    '''Return the value given in the string s as a float.  A single
    trailing character may be an optional SI prefix.
    '''
    prefix = {
        "y": -24,
        "z": -21,
        "a": -18,
        "f": -15,
        "p": -12,
        "n": -9,
        "u": -6,
        "m": -3,
        "c": -2,
        "d": -1,
        "h": 2,
        "k": 3,
        "M": 6,
        "G": 9,
        "T": 12,
        "P": 15,
        "E": 18,
        "Z": 21,
        "Y": 24,
    }
    if not s:
        raise ValueError("Empty string in Interpret()")
    m = 1
    if s[-1] in prefix:
        m = 10** prefix[s[-1]]
        s = s[:-1]
    return flt(s)*m
def CheckAngle(theta_d):
    if not (-90 <= theta_d <= 90):
        Error("Impedance angle must be between -90° and 90°")
def CalculateDependentVariables():
    #   Rs = Equivalent series resistance   
    #   Rp = Equivalent parallel resistance 
    #   X  = Reactance                      
    #   Cs = Equivalent series capacitance  
    #   Cp = Equivalent parallel capacitance
    #   Ls = Equivalent series inductance   
    #   Lp = Equivalent parallel inductance 
    #   Q  = Quality factor                 
    #   D  = Dissipation factor             
    global a, theta, Rs, Rp, X, Cs, Cp, Ls, Lp, Q, D
    if t == 90:
        Rs = 0
        Rp = inf
        Q = inf
        D = 0
        Cs = a/sin(theta)
    elif t == -90:
        Rs = 0
        Rp = -inf
        Q = -inf
        D = 0
        Cs = a/sin(theta)
    else:
        theta = radians(flt(theta_d))
        Rs = Z*cos(theta)
        Rp = Z/cos(theta)
        Q = tan(abs(theta))
        D = inf if not Q else 1/Q
        Cs = inf if not theta else a/sin(theta)
    Cp = a*sin(theta)
    a = Z/w
    Ls = a*sin(theta)
    Lp = inf if not theta else a/sin(theta)
    # Correct capacitances to get conventional sign
    Cs *= -1
    Cp *= -1
def PrintReport():
    global theta, Rs, Rp, X, Cs, Cp, Ls, Lp, Q, D
    # Print report
    E = fp.engsi
    fr = E(float(d["-f"])) + "Hz"
    o = "Ω"
    Rs = "∞ {o}" if isinf(Rs) else f"{E(Rs)}{o}"
    Rp = f"∞ {o}" if isinf(Rp) else f"{E(Rp)}{o}"
    X = E(Z*sin(theta)) + o
    Cs = f"∞ F" if isinf(Cs) else f"{E(Cs)}F"
    Cp = f"{E(Cp)}F"
    Ls = ("-∞ H" if Ls == -inf else "∞ H") if isinf(Ls) else f"{E(Ls)}H"
    Lp = ("-∞ H" if Lp == -inf else "∞ H") if isinf(Lp) else f"{E(Lp)}H"
    Q = ("-∞" if Q == -inf else "∞") if isinf(Q) else f"{Q}"
    D = ("-∞" if D == -inf else "∞") if isinf(D) else f"{D}"
    n = 22
    print(dedent(f'''
    Impedance({fr}) = {z} Ω @ {theta_d}°
        {Rs:>{n}s}    Rs = Equivalent series resistance
        {Rp:>{n}s}    Rp = Equivalent parallel resistance
        {X:>{n}s}    X  = Reactance
        {Cs:>{n}s}    Cs = Equivalent series capacitance
        {Cp:>{n}s}    Cp = Equivalent parallel capacitance
        {Ls:>{n}s}    Ls = Equivalent series inductance
        {Lp:>{n}s}    Lp = Equivalent parallel inductance
        {Q:>{n}s}    Q  = Quality factor
        {D:>{n}s}    D  = Dissipation factor'''))

if __name__ == "__main__":
    d = {}  # Options dictionary
    # Get global variables
    z, theta_d = ParseCommandLine(d)
    theta = radians(flt(theta_d))
    fp = FPFormat(d["-d"])
    inf = flt(float("inf"))
    t = flt(theta_d)
    CheckAngle(t)
    w = 2*pi*d["-f"]  # Angular frequency in radians/s
    Z = Interpret(z)  # Magnitude of impedance in ohms
    a = 1/(w*Z)
    # Calculate and report
    CalculateDependentVariables()
    PrintReport()
