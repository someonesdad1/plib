"""
Resistance of precision YSI thermistor versus temperature
    The data came from the calibration sheet that came with the thermistor.
    I got this thermistor from HP lab stock in the early 1980's.

    The method used is inefficient, but easy.  To convert from resistance
    to temperature, the resistance value is found that is <= the given
    resistance and such that the next resistance is > than the given
    resistance.  Then linear interpolation is done between these two
    values; this is an accurate technique because the curve doesn't change
    rapidly.

    The RegressionData() function prints out data to allow a regression of
    1/T to ln(R) where T is the temperature in K and R is the resistance in
    ohms.  The fitted function is

        T = 1e7/(9536.65 + 2154.49*lr + 5.68624*lr**2 + 1.08435*lr**3)
        lr = ln(R), R in ohms

    The maximum absolute residual is 0.02 degC.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Calculates resistance of precision YSI thermistor versus temperature
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import os
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
    from f import flt, log as ln
    from color import C
if 1:  # Global variables

    class g:
        pass

    g.c = C.lgrn
    g.k = C.lred
    g.f = C.lyel
    g.n = C.norm
    # The resistance in kΩ of the thermistor is given in the following list
    # from -40 °C to 150 °C; the step size is one °C.  Note there are 10
    # values per line.
    R_kohm = [
        flt(i)
        for i in (
            884.6,
            830.9,
            780.8,
            733.9,
            690.2,
            649.3,
            611,
            575.2,
            541.7,
            510.4,
            481,
            453.5,
            427.7,
            403.5,
            380.9,
            359.6,
            339.6,
            320.9,
            303.3,
            286.7,
            271.2,
            256.5,
            242.8,
            229.8,
            217.6,
            206.2,
            195.4,
            185.2,
            175.6,
            166.6,
            158,
            150,
            142.4,
            135.2,
            128.5,
            122.1,
            116,
            110.3,
            104.9,
            99.8,
            94.98,
            90.41,
            86.09,
            81.99,
            78.11,
            74.44,
            70.96,
            67.66,
            64.53,
            61.56,
            58.75,
            56.07,
            53.54,
            51.13,
            48.84,
            46.67,
            44.6,
            42.64,
            40.77,
            38.99,
            37.3,
            35.7,
            34.17,
            32.71,
            31.32,
            30,
            28.74,
            27.54,
            26.4,
            25.31,
            24.27,
            23.28,
            22.33,
            21.43,
            20.57,
            19.74,
            18.96,
            18.21,
            17.49,
            16.8,
            16.15,
            15.52,
            14.92,
            14.35,
            13.8,
            13.28,
            12.77,
            12.29,
            11.83,
            11.39,
            10.97,
            10.57,
            10.18,
            9.807,
            9.45,
            9.109,
            8.781,
            8.467,
            8.166,
            7.876,
            7.599,
            7.332,
            7.076,
            6.83,
            6.594,
            6.367,
            6.149,
            5.94,
            5.738,
            5.545,
            5.359,
            5.18,
            5.007,
            4.842,
            4.682,
            4.529,
            4.381,
            4.239,
            4.102,
            3.97,
            3.843,
            3.72,
            3.602,
            3.489,
            3.379,
            3.273,
            3.172,
            3.073,
            2.979,
            2.887,
            2.799,
            2.714,
            2.632,
            2.552,
            2.476,
            2.402,
            2.331,
            2.262,
            2.195,
            2.131,
            2.069,
            2.009,
            1.95,
            1.894,
            1.84,
            1.788,
            1.737,
            1.688,
            1.64,
            1.594,
            1.55,
            1.507,
            1.465,
            1.425,
            1.386,
            1.348,
            1.311,
            1.276,
            1.241,
            1.208,
            1.176,
            1.145,
            1.114,
            1.085,
            1.057,
            1.029,
            1.002,
            0.9763,
            0.9511,
            0.9267,
            0.903,
            0.88,
            0.8577,
            0.8361,
            0.815,
            0.7946,
            0.7748,
            0.7556,
            0.7369,
            0.7188,
            0.7012,
            0.6841,
            0.6675,
            0.6513,
            0.6356,
            0.6203,
            0.6055,
            0.5911,
            0.5771,
            0.5635,
            0.5502,
        )
    ]
    # Make sure we're not missing any elements
    assert len(R_kohm) == (150 - (-40) + 1)
    # Calculate the checksum
    checksum = 16200.156  # The array should sum to this value
    assert (sum(R_kohm) - checksum) < 1e-4
    # Amount to subtract from array index to get deg C
    t_offset = 40
    # These are the temperature/resistance data for a Radio Shack 271-110
    # thermistor from -50 degC to 110 degC in 5 degC steps.
    RS_kOhms = (
        329.2,
        247.5,
        188.4,
        144.0,
        111.3,
        86.39,
        67.74,
        53.39,
        42.45,
        33.89,
        27.28,
        22.05,
        17.96,
        14.68,
        12.09,
        10.00,
        8.313,
        6.941,
        5.828,
        4.912,
        4.161,
        3.537,
        3.021,
        2.589,
        2.229,
        1.924,
        1.669,
        1.451,
        1.266,
        1.108,
        0.9735,
        0.8575,
        0.7579,
    )
    # Constant to convert degC to K
    k = 273.15


def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)


def Usage(status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] [kohm1 [kohm2 ...]
      Convert a resistance in kΩ into a temperature in °C for the YSI 44008
      precision thermistor.  Resistance is 30 kΩ nominal at 25 °C.
    Options:
      -p    Plot the resistance versus temperature (requires pylab).
      -r    Print two columns of temperature in K and resistance in kohm.
      -t    Print a table converting resistance to temperature.
    """)
    )
    exit(status)


def ParseCommandLine():
    d["-d"] = 4  # Number of significant figures
    d["-p"] = False  # Plot resistance
    d["-r"] = False  # Print two columns
    d["-t"] = False  # Print table
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:hprt")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("cprt"):
            d[o] = not d[o]
        elif o == "-d":
            d[o] = int(a)
        elif o in ("-h", "--help"):
            Usage(status=0)
    x = flt(0)
    x.n = d["-d"]
    x.rtz = x.rtdp = False
    if d["-t"]:
        PrintTable()
        exit(0)
    elif d["-p"]:
        PlotData()
        exit(0)
    elif d["-r"]:
        RegressionData()
        exit(0)
    if not args:
        Usage()
    return args


class Thermistor:
    def C_to_R(self, degC):
        """Return the resistance in kOhms given the temperature in degrees C."""
        if degC < -t_offset or degC >= len(R_kohm) - t_offset:
            raise Exception("Temperature out of range:  " + str(degC))
        # Get the table entry
        T0 = int(degC) + t_offset
        T1 = T0 + 1  # Assumes table entries are 1 degC apart
        R0 = R_kohm[T0]
        R1 = R_kohm[T1]
        alpha = ((degC + t_offset) - T0) / (T1 - T0)
        R = R0 + alpha * (R1 - R0)
        return R

    def R_to_C(self, R_kohms):
        "Return the temperature in degrees C given a resistance"
        if R_kohms < min(R_kohm) or R_kohms > max(R_kohm):
            Error("Resistance out of range:  " + str(R_kohms))
        # We will calculate the value using two different polynomial
        # fits
        #
        # The function is based on the Steinhart-Hart equation and
        # was fitted in thermistor_fit.py.
        a, b, c, d = 9.503704e-04, 2.163135e-04, 4.939487e-07, 1.105645e-07
        t = ln(1000 * R_kohms)
        T1 = 1 / (a + b * t + c * t * t + d * t * t * t) - k
        # Use the fit found via RegressionData()
        lr = ln(R_kohms * 1000)
        T2 = 1e7 / (9536.65 + 2154.49 * lr + 5.68624 * lr**2 + 1.08435 * lr**3) - k
        # They should agree within 0.1 degC
        if abs(T1 - T2) > 0.1:
            raise RuntimeError(f"Bad fits:  {T1} != {T2}")
        # We'll return T2, as we know it fits within 0.02 degC
        return T2


def PrintTable():
    "Print a table of resistance vs. temperature in °C"
    offset = 40
    print(
        dedent("""
    YSI Precision Thermistor
    °C                           Resistance in kΩ
    """)
    )
    for j in range(0, 10):
        print(f"{j:7d}", end="")
    print()
    for i in range(-40, 150, 10):
        print(f"{i:3d} ", end=" ")
        for j in range(0, 10):
            T = i + j
            R = str(R_kohm[T + offset])
            if R[0] == "0":
                R = R[1:]
            print(f"{R:7s}", end="")
        print()


def PlotData():
    from pylab import plot, grid, xlabel, ylabel, title, show
    from pylab import semilogy, exp, array, legend, log as ln

    t = array([i + k for i in range(-40, 151)])
    if 0:
        # Plot the resistance as a function of temperature
        plot(t, R_kohm)
        grid()
        xlabel("Temperature, degC")
        ylabel("Resistance, kohm")
        title("YSI 44008 Thermistor")
        show()
    if 0:
        # Semilog plot
        semilogy(t, R_kohm)
        grid()
        xlabel("Temperature, degC")
        ylabel("Resistance, kohm")
        title("YSI 44008 Thermistor")
        show()
    if 1:
        """
        Compare to the beta equation using R0 = 30 kohm at 25 degC.  The
        equations are
            
            r = R0*exp(-β/T0)
            R = r*exp(β/T)
 
        which solves to give
 
            T = β/ln(R/r)
        """
        F = semilogy
        F = plot
        R0 = 30
        T0 = 25 + k
        T = array(range(-40, 151))  # Temp in degC
        T_K = array([i + k for i in T])
        # Plot R actual vs. R predicted
        β = 3650
        r = R0 * exp(-β / T0)
        R = array(R_kohm)
        t = β / ln(R / r) - k  # Predicted temp in degC
        plot(T, t - T)
        grid()
        xlabel("Temperature, °C")
        ylabel("Difference from predicted, °C")
        legend()
        title(
            dedent(f"""
        YSI 44008 Thermistor
        β = {β}, R0 = {R0} kΩ, T0 = {T0 - k} °C""")
        )
        show()
    exit()


def RegressionData():
    """Print columns of temperature in K and resistance in kohms.  This
    will allow the reg utility to perform a linear regression fit to a
    cubic equation.  The columns are:
        1/T in 1/K
        ln(R)
        ln(R)**2
        ln(R)**3

    Putting the output in file a and using the command line 'reg -y c1
    c2 c3 c4 <a' results in

        ANOVA Table

        Source of
        Variation                   SS          df                MS
        --------------------------------------------------------------
        Regression      SSR =  5.69848e-05       3  MSR =  1.89949e-05
        Error           SSE =  9.87938e-13     187  MSE =  5.28309e-15
        --------------------------------------------------------------
        Total          SSTO =  5.69848e-05     190

        Adjusted R^2 = 100.00
                R^2 = 100.00

        F statistic with df=(3,187) = 3.595e+09

        Covariance matrix:
        [[ 3.80e-13 -1.21e-13  1.25e-14 -4.17e-16]
        [-1.21e-13  3.88e-14 -4.01e-15  1.35e-16]
        [ 1.25e-14 -4.01e-15  4.17e-16 -1.41e-17]
        [-4.17e-16  1.35e-16 -1.41e-17  4.75e-19]]

        Model parameters:    Estimate        StdDev    100*StdDev/Est
            b0            0.000953665     6.162e-07              0.06
            b1            0.000215449     1.969e-07              0.09
            b2            5.68624e-07     2.043e-08              3.59
            b3            1.08435e-07     6.894e-10              0.64

    Thus, the fitted equation is

        T = 1e7/(9536.65 + 2154.49*lr + 5.68624*lr**2 + 1.08435*lr**3)
        lr = ln(R), R in ohms

    The maximum absolute residual is 0.02 K.
    """
    print("# YSI 44008 thermistor data")
    print("# The columns are:")
    print("#    1/T, T in K")
    print("#    ln(R), R in ohms")
    print("#    ln(R)**2")
    print("#    ln(R)**3")
    resid = []
    b0, b1, b2, b3 = 9536.65, 2154.49, 5.68624, 1.08435
    flt(0).n = 6
    for t, R in zip(range(-40, 151), R_kohm):
        lr = ln(1000 * R)
        T = flt(t + k)
        Tpred = 1e7 / (b0 + b1 * lr + b2 * lr**2 + b3 * lr**3)
        print(f"{1 / T}    {lr}    {lr**2}    {lr**3}")
        r = t - Tpred + k
        resid.append(r)
    print(
        f"# Min/max residuals for regression fit in K:  {min(resid):.2f}, {max(resid):.2f}"
    )


if __name__ == "__main__":
    d = {}  # Options dictionary
    th = Thermistor()
    args = ParseCommandLine()
    print("YSI Precision thermistor:  temperature vs. resistance in kΩ:")
    for r in args:
        R = flt(r)
        Tc = th.R_to_C(R)
        Tf = 1.8 * Tc + 32
        Tk = Tc + 273.15
        res = r + " kΩ"
        print(
            f"{res:8s}      T = {g.c}{Tc:.1f} °C{g.n} = "
            f"{g.f}{Tf:.1f} °F{g.n} = {g.k}{Tk:.1f} K{g.n}"
        )
