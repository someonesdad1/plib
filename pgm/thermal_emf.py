"""
TODO

    * Check cu au as it is parabolic

Provides a table of thermal EMFs between two metals

    The data are from the 1957 AIP "Handbook of Physics", pg 4-8,
    McGraw-Hill.  The table data in the AIP handbook are relative to
    platinum:

    "A positive sign means that in a simple thermoelectric circuit the
    resultant emf as given is in such a direction as to produce a
    current from the element to the platinum at the reference junction
    of 0 deg C.  The values below 0 deg C, in most cases, have not
    been determined on the same samples as the values above 0 deg C."

    The underlying reference is:  AIP, "Temperature, Its Measurement
    and Control in Science and Industry", pp 1308-1310, Reinhold
    Publishing Corp., NY, 1941.

    The basic method used to construct the tables is to linearly interpolate in
    the AIP handbook's data.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Table of thermal EMFs between two metals
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import getopt
    from itertools import combinations
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
    from columnize import Columnize
    from tc import TC
    from frange import frange
    from interpolate import LinearInterpFunction
    from bidict import bidict
if 1:  # Global variables
    data = {
        # Data are (T in deg C, EMF in mV)
        "Chromel": (
            (-200, -3.36),
            (-100, -2.20),
            (0, 0),
            (100, 2.81),
            (200, 5.96),
            (300, 9.32),
            (400, 12.75),
            (500, 16.21),
            (600, 19.62),
            (700, 22.96),
            (800, 26.23),
            (900, 29.41),
            (1000, 32.52),
            (1100, 35.56),
            (1200, 38.51),
            (1300, 41.35),
            (1400, 44.04),
        ),
        "Alumel": (
            (-200, 2.39),
            (-100, 1.29),
            (0, 0),
            (100, -1.29),
            (200, -2.17),
            (300, -2.89),
            (400, -3.64),
            (500, -4.43),
            (600, -5.28),
            (700, -6.18),
            (800, -7.08),
            (900, -7.95),
            (1000, -8.79),
            (1100, -9.58),
            (1200, -10.34),
            (1300, -11.06),
            (1400, -11.77),
        ),
        "Copper": (
            (-200, -0.19),
            (-100, -0.37),
            (0, 0),
            (100, 0.76),
            (200, 1.83),
            (300, 3.15),
            (400, 4.68),
            (500, 6.41),
            (600, 8.34),
            (700, 10.49),
            (800, 12.84),
            (900, 15.41),
            (1000, 18.20),
        ),
        # Data from pg 4-8 (may be incorrect)
        # Note neither of the two tables with Constantan produce anything
        # anywhere near the accuracy of the other thermocouples.  This
        # information needs to be verified.
        "Iron": (
            (-200, -2.92),
            (-100, -1.84),
            (0, 0),
            (100, 1.89),
            (200, 3.54),
            (300, 4.85),
            (400, 5.88),
            (500, 6.79),
            (600, 7.80),
            (700, 9.12),
            (800, 10.86),
            (900, 12.84),
            (1000, 14.30),
        ),
        # Data from pg 4-7 (may be incorrect)
        #    "Iron": (
        #        (-200, -3.10),
        #        (-100, -1.94),
        #        (0, 0),
        #        (100, 1.98),
        #        (200, 3.69),
        #        (300, 5.03),
        #        (400, 6.08),
        #        (500, 7.00),
        #        (600, 8.02),
        #        (700, 9.34),
        #        (800, 11.09),
        #        (900, 13.10),
        #        (1000, 14.64),
        #    ),
        "Constantan": (
            (-200, 5.35),
            (-100, 2.98),
            (0, 0),
            (100, -3.51),
            (200, -7.45),
            (300, -11.71),
            (400, -16.19),
            (500, -20.79),
            (600, -25.47),
            (700, -30.18),
            (800, -34.86),
            (900, -39.45),
            (1000, -43.92),
        ),
        "Manganin": (
            (0, 0),
            (100, 0.61),
            (200, 1.55),
            (300, 2.77),
            (400, 4.25),
            (500, 5.95),
            (600, 7.84),
        ),
        "Beryllium-copper": (
            (0, 0),
            (100, 0.67),
            (200, 1.62),
            (300, 2.81),
            (400, 4.19),
        ),
        "Brass": (
            (0, 0),
            (100, 0.60),
            (200, 1.49),
            (300, 2.58),
            (400, 3.85),
            (500, 5.30),
            (600, 6.96),
        ),
        "Bronze": (
            (0, 0),
            (100, 0.55),
            (200, 1.34),
            (300, 2.34),
            (400, 3.50),
            (500, 4.81),
            (600, 6.30),
        ),
        "Solder 50Sn-50Pb": (
            (0, 0),
            (100, 0.46),
        ),
        "Stainless steel": (
            (0, 0),
            (100, 0.44),
            (200, 1.04),
            (300, 1.76),
            (400, 2.60),
            (500, 3.56),
            (600, 4.67),
            (700, 5.93),
            (800, 7.37),
            (900, 8.99),
        ),
        "Spring steel": (
            (0, 0),
            (100, 1.32),
            (200, 2.63),
            (300, 3.81),
            (400, 4.84),
            (500, 5.80),
            (600, 6.86),
        ),
        "Nichrome (80Ni-20Cr)": (
            (0, 0),
            (100, 1.14),
            (200, 2.62),
            (300, 4.34),
            (400, 6.25),
            (500, 8.31),
            (600, 10.53),
            (700, 12.91),
            (800, 15.44),
            (900, 18.11),
            (1000, 20.91),
        ),
        "Inconel (60Ni-24Fe-16Cr)": (
            (0, 0),
            (100, 0.85),
            (200, 2.01),
            (300, 3.41),
            (400, 5.00),
            (500, 6.76),
            (600, 8.68),
            (700, 10.78),
            (800, 13.06),
            (900, 15.50),
            (1000, 18.10),
        ),
        "Copper coin (95Cu-4Sn-1Zn)": (
            (0, 0),
            (100, 0.60),
            (200, 1.48),
            (300, 2.60),
            (400, 3.91),
            (500, 5.44),
            (600, 7.14),
        ),
        "Nickel coin (75Cu-25Ni)": (
            (0, 0),
            (100, -2.76),
            (200, -6.01),
            (300, -9.71),
            (400, -13.78),
            (500, -18.10),
            (600, -22.59),
        ),
        "Silver coin (90Ag-10Cu)": (
            (0, 0),
            (100, 0.80),
            (200, 1.90),
            (300, 3.25),
            (400, 4.81),
            (500, 6.59),
            (600, 8.64),
        ),
        "Magnesium": (
            (-200, 0.37),
            (-100, -0.09),
            (0, 0),
            (100, 0.44),
            (200, 1.10),
        ),
        "Zinc": (
            (-200, -0.07),
            (-100, -0.33),
            (0, 0),
            (100, 0.76),
            (200, 1.89),
            (300, 3.42),
            (400, 5.29),
        ),
        "Cadmium": (
            (-200, -0.04),
            (-100, -0.31),
            (0, 0),
            (100, 0.90),
            (200, 2.35),
            (300, 4.24),
        ),
        "Mercury": (
            (0, 0),
            (100, -0.60),
            (200, -1.33),
        ),
        "Indium": (
            (0, 0),
            (100, 0.69),
        ),
        "Aluminum": (
            (-200, 0.45),
            (-100, -0.06),
            (0, 0),
            (100, 0.42),
            (200, 1.06),
            (300, 1.86),
            (400, 2.84),
            (500, 3.93),
            (600, 5.15),
        ),
        "Carbon": (
            (0, 0),
            (100, 0.70),
            (200, 1.54),
            (300, 2.55),
            (400, 3.72),
            (500, 5.15),
            (600, 6.79),
            (700, 8.84),
            (800, 11.01),
            (900, 13.59),
            (1000, 16.51),
            (1100, 19.49),
        ),
        "Silicon": (
            (-200, 63.13),
            (-100, 32.17),
            (0, 0),
            (100, -41.56),
            (200, -80.58),
            (300, -110.09),
        ),
        "Germanium": (
            (-200, -46.00),
            (-100, -26.62),
            (0, 0),
            (100, 33.9),
            (200, 72.4),
            (300, 91.8),
            (400, 82.3),
            (500, 63.5),
            (600, 43.9),
            (700, 27.9),
        ),
        "Tin": (
            (-200, 0.26),
            (-100, -0.12),
            (0, 0),
            (100, 0.42),
            (200, 1.07),
        ),
        "Lead": (
            (-200, 0.24),
            (-100, -0.13),
            (0, 0),
            (100, 0.44),
            (200, 1.09),
            (300, 1.91),
        ),
        "Antimony": (
            (0, 0),
            (100, 4.89),
            (200, 10.14),
            (300, 15.44),
            (400, 20.53),
            (500, 25.10),
            (600, 28.88),
        ),
        "Bismuth": (
            (-200, 12.39),
            (-100, 7.54),
            (0, 0),
            (100, -7.34),
            (200, -13.57),
        ),
        "Silver": (
            (-200, -0.21),
            (-100, -0.39),
            (0, 0),
            (100, 0.74),
            (200, 1.77),
            (300, 3.05),
            (400, 4.57),
            (500, 6.36),
            (600, 8.41),
            (700, 10.75),
            (800, 13.36),
            (900, 16.20),
        ),
        "Gold": (
            (-200, -0.20),
            (-100, -0.39),
            (0, 0),
            (100, 0.78),
            (200, 1.84),
            (300, 3.14),
            (400, 4.63),
            (500, 6.29),
            (600, 8.12),
            (700, 10.13),
            (800, 12.29),
            (900, 14.61),
            (1000, 17.09),
        ),
        "Cobalt": (
            (0, 0),
            (100, -1.33),
            (200, -3.08),
            (300, -5.10),
            (400, -7.24),
            (500, -9.35),
            (600, -11.28),
            (700, -12.88),
            (800, -14.00),
            (900, -14.49),
            (1000, -14.20),
            (1100, -12.98),
            (1200, -10.68),
        ),
        "Nickel": (
            (-200, 2.28),
            (-100, 1.22),
            (0, 0),
            (100, -1.48),
            (200, -3.10),
            (300, -4.59),
            (400, -5.45),
            (500, -6.16),
            (600, -7.04),
            (700, -8.10),
            (800, -9.35),
            (900, -10.69),
            (1000, -12.13),
            (1100, -13.62),
        ),
        "Iridium": (
            (-200, -0.25),
            (-100, -0.35),
            (0, 0),
            (100, 0.65),
            (200, 1.49),
            (300, 2.47),
            (400, 3.55),
            (500, 4.78),
            (600, 6.10),
            (700, 7.56),
            (800, 9.12),
            (900, 10.80),
            (1000, 12.59),
            (1100, 14.48),
            (1200, 16.47),
            (1300, 18.47),
            (1400, 20.48),
            (1500, 22.50),
        ),
        "Rhodium": (
            (-200, -0.20),
            (-100, -0.34),
            (0, 0),
            (100, 0.70),
            (200, 1.61),
            (300, 2.68),
            (400, 3.91),
            (500, 5.28),
            (600, 6.77),
            (700, 8.40),
            (800, 10.16),
            (900, 12.04),
            (1000, 14.05),
            (1100, 16.18),
            (1200, 18.42),
            (1300, 20.70),
            (1400, 23.00),
            (1500, 25.35),
        ),
        "Palladium": (
            (-200, 0.81),
            (-100, 0.48),
            (0, 0),
            (100, -0.57),
            (200, -1.23),
            (300, -1.99),
            (400, -2.82),
            (500, -3.84),
            (600, -5.03),
            (700, -6.41),
            (800, -7.98),
            (900, -9.72),
            (1000, -11.63),
            (1100, -13.70),
            (1200, -15.89),
            (1300, -18.12),
            (1400, -20.41),
            (1500, -22.74),
        ),
        "Molybdenum": (
            (0, 0),
            (100, 1.45),
            (200, 3.19),
            (300, 5.23),
            (400, 7.57),
            (500, 10.20),
            (600, 13.13),
            (700, 16.35),
            (800, 19.87),
            (900, 23.69),
            (1000, 27.80),
            (1100, 32.21),
            (1200, 36.91),
        ),
        "Tungsten": (
            (-200, 0.43),
            (-100, -0.15),
            (0, 0),
            (100, 1.12),
            (200, 2.62),
            (300, 4.48),
            (400, 6.70),
            (500, 9.30),
            (600, 12.26),
            (700, 15.60),
            (800, 19.30),
            (900, 23.36),
            (1000, 27.80),
            (1100, 32.60),
            (1200, 37.78),
        ),
        "Tantalum": (
            (-200, 0.21),
            (-100, -0.10),
            (0, 0),
            (100, 0.33),
            (200, 0.93),
            (300, 1.79),
            (400, 2.91),
            (500, 4.30),
            (600, 5.95),
            (700, 7.87),
            (800, 10.05),
            (900, 12.49),
            (1000, 15.20),
            (1100, 18.17),
            (1200, 21.41),
        ),
        "Thorium": (
            (0, 0),
            (100, -0.13),
            (200, -0.26),
            (300, -0.40),
            (400, -0.50),
            (500, -0.53),
            (600, -0.45),
            (700, -0.21),
            (800, 0.22),
            (900, 0.87),
            (1000, 1.73),
            (1100, 2.80),
            (1200, 4.04),
            (1300, 5.42),
        ),
    }
    data_list = list(sorted(data.keys()))
    aliases = {
        "al": 2,
        "becu": 4,
        "bi": 5,
        "br": 6,
        "cd": 8,
        "c": 9,
        "co": 11,
        "cu": 13,
        "ge": 15,
        "au": 16,
        "in": 18,
        "ir": 19,
        "fe": 20,
        "pb": 21,
        "mg": 22,
        "hg": 24,
        "mo": 25,
        "nichrome": 26,
        "ni": 27,
        "pd": 29,
        "rh": 30,
        "si": 31,
        "ag": 32,
        "solder": 34,
        "steel": 35,
        "sst": 36,
        "ta": 37,
        "th": 38,
        "sn": 39,
        "w": 40,
        "zn": 41,
    }
    alias = bidict()
    for key, value in zip(
        """al becu bi br cd c co cu ge au in ir fe pb mg hg mo nichrome ni
           pd rh si ag solder steel sst ta th sn w zn""".split(),
        [
            2,
            4,
            5,
            6,
            8,
            9,
            11,
            13,
            15,
            16,
            18,
            19,
            20,
            21,
            22,
            24,
            25,
            26,
            27,
            29,
            30,
            31,
            32,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
        ],
    ):
        alias[key] = value


def Plot():
    """Predict the thermal EMF for common thermocouples and plot
    their error from the NIST polynomials.
    """
    from scipy.interpolate import interp1d
    import numpy as np
    from pylab import plot, xlabel, ylabel, title, legend, grid, show, savefig

    # Type K:  Chromel-alumel
    tc = TC("K")
    c, a = data["Chromel"], data["Alumel"]
    t, e = [], []
    for i in range(len(c)):
        temp, emfc = c[i]
        temp, emfa = a[i]
        t.append(temp)
        e.append(emfc - emfa)
    f = interp1d(t, e, kind="cubic")
    temp, dev = [], []
    for T in range(-190, 10, 10):
        for t in range(11):
            temp.append(T - t)
            dev.append(f(T - t) - tc.E_mV(T - t))
    for T in range(0, 1370, 10):
        for t in range(11):
            temp.append(T + t)
            dev.append(f(T + t) - tc.E_mV(T + t))
    temp, dev = [np.array(i) for i in (temp, dev)]
    plot(temp, dev * 100, label="K (Chromel-Alumel)")
    # Type T:  Copper-Constantan
    tc = TC("T")
    c, a = data["Copper"], data["Constantan"]
    t, e = [], []
    for i in range(len(c)):
        temp, emfc = c[i]
        temp, emfa = a[i]
        t.append(temp)
        e.append(emfc - emfa)
    f = interp1d(t, e, kind="cubic")
    temp, dev = [], []
    for T in range(0, 400, 10):
        for t in range(11):
            temp.append(T + t)
            dev.append(f(T + t) - tc.E_mV(T + t))
    temp, dev = [np.array(i) for i in (temp, dev)]
    plot(temp, dev * 100, label="T (Cu-Constantan)")
    # Type E:  Chromel-Constantan
    tc = TC("E")
    c, a = data["Chromel"], data["Constantan"]
    t, e = [], []
    for i in range(len(a)):
        temp, emfc = c[i]
        temp, emfa = a[i]
        t.append(temp)
        e.append(emfc - emfa)
    f = interp1d(t, e, kind="cubic")
    temp, dev = [], []
    for T in range(-190, 10, 10):
        for t in range(11):
            temp.append(T - t)
            dev.append(f(T - t) - tc.E_mV(T - t))
    for T in range(0, 1000, 10):
        for t in range(11):
            temp.append(T + t)
            dev.append(f(T + t) - tc.E_mV(T + t))
    temp, dev = [np.array(i) for i in (temp, dev)]
    plot(temp, dev * 100, label="E (Chromel-Constantan")
    # Type J:  Iron-Constantan
    if 0:
        # Conditional plot because there's so much error.  Cause
        # unknown, but the AIP has two Fe tables on page 4-7 and 4-8
        # and they both give values that don't work well with the
        # established type J curve.
        tc = TC("J")
        c, a = data["Fe"], data["Constantan"]
        t, e = [], []
        for i in range(len(a)):
            temp, emfc = c[i]
            temp, emfa = a[i]
            t.append(temp)
            e.append(emfc - emfa)
        f = interp1d(t, e, kind="cubic")
        temp, dev = [], []
        for T in range(-190, 10, 10):
            for t in range(11):
                temp.append(T - t)
                dev.append(f(T - t) - tc.E_mV(T - t))
        for T in range(0, 1000, 10):
            for t in range(11):
                temp.append(T + t)
                dev.append(f(T + t) - tc.E_mV(T + t))
        temp, dev = [np.array(i) for i in (temp, dev)]
        plot(temp, dev * 100, label="J")
    grid()
    title("% deviation from true value")
    xlabel("Temperature, deg C")
    ylabel("% Deviation")
    legend()
    if 1:
        show()
    else:
        savefig("pictures/thermal_emf.png", dpi=100)
    exit(0)


def Usage(d, status=1):
    name = sys.argv[0]
    print(
        dedent(f"""
    Usage:  {name} [options] matl1 matl2
      Print a thermal EMF table for the two given materials.  The intent
      is to give an order of magnitude and sign estimate of the thermal
      EMF for two metals relative to a similar junction at 0 deg C.
     
      matl1 and matl2 are numbers that identify the materials.
     
      Accuracy of the predictions is unknown, but it is probably on the order
      of 10%.  The data are from the 1957 AIP "Handbook of Physics", pg 4-8,
      McGraw-Hill.
    Options:
      -d t  Specify the temperature scale to use with the letter t (case
            insensitive).  c is degrees Celsius, f is Fahrenheit, k is
            Kelvin, and R is Rankine.  c is the default.
      -l    Print a list of the material numbers (shorthand in [])
      -p    Generate a plot showing the deviations from NIST polynomials
            for common thermocouple types.  You'll see that the predictions
            for temperatures above zero are within a few percent but poor
            for below zero (as per the comments at the beginning of the
            script).
      -s    Print the long table (by every degree) instead of the short
            table, which is by 10 degrees.
      -t    Run self-tests
    """)
    )
    exit(status)


def List():
    strings = []
    for i in range(len(data_list)):
        s = data_list[i]
        if i + 1 in alias.values():
            s += f" [{alias(i + 1)}]"
        strings.append(f"{i + 1:2d}.  {s}")
    for i in Columnize(strings):
        print(i)
    exit()


def ParseCommandLine():
    d["-s"] = True
    d["-d"] = "C"
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "d:lpst")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for opt in optlist:
        if opt[0] == "-d":
            if len(opt[1]) > 1 or opt[1].upper() not in "CFKR":
                print("-d option must be C, F, K, or R")
                exit(1)
            d["-d"] = opt[1].upper()
        if opt[0] == "-l":
            List()
        if opt[0] == "-p":
            Plot()
        if opt[0] == "-s":
            d["-s"] = not d["-s"]
        if opt[0] == "-t":
            exit(SelfTest(d))
    if len(args) != 2:
        Usage(d)
    return args


def TemplateRound(x, template, up=True):
    if not x:
        return x
    sign = 1 if x >= 0 else -1
    if sign < 0:
        up = not up
    y = int(abs(x / template) + 0.5) * abs(template)
    if up and y < abs(x):
        y += template
    elif not up and y > abs(x):
        y -= template
    return sign * y


def SelfTest(d):
    """Generate each pair of materials and verify the numbers can be
    produced.
    """

    def Dummy(*v, **kw):
        pass

    for m1, m2 in combinations(range(len(data_list)), 2):
        matl1, matl2 = data_list[m1], data_list[m2]
        PrintTable(matl1, matl2, Print=Dummy)
    print("Tests passed")


if 0:

    def PrintTable_(matl1, matl2, d, Print=print):
        "This version uses scipy"

        def Title(unit):
            s = "Thermal EMF in mV of materials for temperatures in"
            if unit == "K":
                Print(s, "K")
            else:
                Print(s, "degrees %s" % unit)
            Print("  Material 1 =", matl1)
            Print("  Material 2 =", matl2)
            Print()

        def Header(w, step=1):
            Print("  T  ", end="")
            for i in range(0, 10 * step, step):
                s = "{0:^{1}}".format(i, w)
                Print(s, end="")
            Print()

        # Get the data for the indicated materials
        d1, d2 = list(data[matl1]), list(data[matl2])
        # Trim them to get equal array sizes.  Do this by comparing
        # temperature ranges.
        if d1[0][0] < d2[0][0]:
            while d1[0][0] < d2[0][0]:
                del d1[0]
        elif d2[0][0] < d1[0][0]:
            while d2[0][0] < d1[0][0]:
                del d2[0]
        if d1[-1][0] > d2[-1][0]:
            while d1[-1][0] > d2[-1][0]:
                del d1[-1]
        elif d2[-1][0] > d1[-1][0]:
            while d2[-1][0] > d1[-1][0]:
                del d2[-1]
        # Check that the temperature ranges match
        assert len(d1) == len(d2)
        assert d1[0][0] == d2[0][0]
        assert d1[-1][0] == d2[-1][0]
        # Create numpy arrays of the data
        TdegC, emf1, emf2 = [], [], []
        for i in range(len(d1)):
            TdegC.append(d1[i][0])
            emf1.append(d1[i][1])
            emf2.append(d2[i][1])
        TdegC, emf1, emf2 = [np.array(i) for i in (TdegC, emf1, emf2)]
        if len(TdegC) < 4:
            """This will be for situations like solder where the data only
            cover 0 and 100 degC.  We'll linearly interpolate to give
            more points.
            """

            def MakeNew(array, n=20):
                a, b = array[0], array[-1]
                dx = 1 / n
                x = np.arange(0, 1 + dx, dx)
                return a + x * (b - a)

            TdegC = MakeNew(TdegC)
            emf1 = MakeNew(emf1)
            emf2 = MakeNew(emf2)
        # Create interpolation function
        k = "cubic"
        f = interp1d(TdegC, emf1 - emf2, kind=k)
        # Get inner and outer temperature loop limits
        Tinner, Touter = 1, 10
        if d["-s"]:
            Tinner, Touter = 10, 100
        # Get temperature array in desired units.  Note we have to round
        # the bottom up and the top down to ensure we are within the
        # interpolation region.
        ip = 273.15  # Ice point temperature in K
        if d["-d"] == "C":
            T = TdegC

            def ToDegC(x):
                return x
        elif d["-d"] == "F":
            T = 9 * TdegC / 5 + 32

            def ToDegC(x):
                return 5 / 9 * (x - 32)
        elif d["-d"] == "K":
            T = TdegC + ip

            def ToDegC(x):
                return x - 273.15
        elif d["-d"] == "R":
            T = (TdegC + ip) + (9 * ip / 5 - 32)

            def ToDegC(x):
                return 5 * x / 9 - 273.15
        else:
            raise Exception("Bug:  temperature unit")
        T0, T1 = int(T[0]), int(T[-1])
        if d["-d"] != "C":
            template = 100 if d["-s"] else 10
            T0 = int(TemplateRound(T0, template, up=True))
            T1 = int(TemplateRound(T1, template, up=False))
        Title(d["-d"])
        w = 6  # Width of each column
        Header(w + 1, Tinner)
        if T0 < 0:
            T0 += Touter  # Avoid going out of interpolation bounds
        for T in range(T0, T1, Touter):
            Print("%4d " % T, end="")
            for dT in range(0, TPrinter, Tinner):
                t = T + dT if T >= 0 else T - dT
                # Convert t to degC
                Print("%6.2f " % f(ToDegC(t)), end="")
            Print()
            if not T and T0 < 0:
                Print()
                Header(w + 1, Tinner)
                Print("%4d " % T, end="")
                # Need to print two rows of zero if T0 is negative
                for dT in range(0, TPrinter, Tinner):
                    Print("%6.2f " % f(ToDegC(T + dT)), end="")
                Print()


def PrintTable(matl1, matl2, Print=print):
    "This version doesn't use scipy"

    def Title(unit):
        s = "Thermal EMF in μV of materials for temperatures in"
        if unit == "K":
            Print(s, "K")
        else:
            Print(s, "degrees %s" % unit)
        Print("  Material 1 =", matl1)
        Print("  Material 2 =", matl2)
        Print()

    def Header(w, step=1):
        Print("  T ", end="")
        for i in range(0, 10 * step, step):
            s = "{0:>{1}}".format(i, w)
            Print(s, end="")
        Print()

    # Get the data for the indicated materials
    d1, d2 = list(data[matl1]), list(data[matl2])
    # Trim them to get equal array sizes.  Do this by comparing
    # temperature ranges.
    if d1[0][0] < d2[0][0]:
        while d1[0][0] < d2[0][0]:
            del d1[0]
    elif d2[0][0] < d1[0][0]:
        while d2[0][0] < d1[0][0]:
            del d2[0]
    if d1[-1][0] > d2[-1][0]:
        while d1[-1][0] > d2[-1][0]:
            del d1[-1]
    elif d2[-1][0] > d1[-1][0]:
        while d2[-1][0] > d1[-1][0]:
            del d2[-1]
    # Check that the temperature ranges match
    assert len(d1) == len(d2)
    assert d1[0][0] == d2[0][0]
    assert d1[-1][0] == d2[-1][0]
    # Create lists of the data
    TdegC, emf1, emf2 = [], [], []
    for i in range(len(d1)):
        TdegC.append(d1[i][0])
        emf1.append(d1[i][1])
        emf2.append(d2[i][1])
    if len(TdegC) < 4:
        """This will be for situations like solder where the data only
        cover 0 and 100 degC.  We'll linearly interpolate to give
        more points.
        """

        def MakeNew(array, n=20):
            a, b = array[0], array[-1]
            dx = 1 / n
            # x = np.arange(0, 1 + dx, dx)
            x = frange(0, str(1 + dx), str(dx))
            return [a + i * (b - a) for i in x]

        TdegC = MakeNew(TdegC)
        emf1 = MakeNew(emf1)
        emf2 = MakeNew(emf2)
    # Create interpolation function
    e = [i - j for i, j in zip(emf1, emf2)]
    f = LinearInterpFunction(TdegC, e)

    # This is in mV output.  Change it to μV to get integers.
    def F(x):
        return int(1000 * f(x))

    # Get inner and Printer temperature loop limits
    Tinner, TPrinter = 1, 10
    if d["-s"]:
        Tinner, TPrinter = 10, 100
    # Get temperature array in desired units.  Note we have to round
    # the bottom up and the top down to ensure we are within the
    # interpolation region.
    ip = 273.15  # Ice point temperature in K
    if d["-d"] == "C":
        T = TdegC

        def ToDegC(x):
            return x
    elif d["-d"] == "F":
        T = [9 * i / 5 + 32 for i in TdegC]

        def ToDegC(x):
            return 5 / 9 * (x - 32)
    elif d["-d"] == "K":
        T = [i + ip for i in TdegC]

        def ToDegC(x):
            return x - 273.15
    elif d["-d"] == "R":
        T = [i + ip + (9 * ip / 5 - 32) for i in TdegC]

        def ToDegC(x):
            return 5 * x / 9 - 273.15
    else:
        raise Exception("Bug:  temperature unit")
    T0, T1 = int(T[0]), int(T[-1])
    if d["-d"] != "C":
        template = 100 if d["-s"] else 10
        T0 = int(TemplateRound(T0, template, up=True))
        T1 = int(TemplateRound(T1, template, up=False))
    Title(d["-d"])
    w = 6  # Width of each column
    Header(w + 1, Tinner)
    if T0 < 0:
        T0 += TPrinter  # Avoid going out of interpolation bounds
    for T in range(T0, T1, TPrinter):
        Print("%4d " % T, end="")
        for dT in range(0, TPrinter, Tinner):
            t = T + dT if T >= 0 else T - dT
            # Convert t to degC
            # Print("%6.2f " % f(ToDegC(t)), end="")
            Print("%6d " % F(ToDegC(t)), end="")
        Print()
        if not T and T0 < 0:
            Print()
            Header(w + 1, Tinner)
            Print("%4d " % T, end="")
            # Need to Print two rows of zero if T0 is negative
            for dT in range(0, TPrinter, Tinner):
                # Print("%6.2f " % f(ToDegC(T + dT)), end="")
                Print("%6d " % F(ToDegC(T + dT)), end="")
            Print()


def GetArgs(args):
    "Convert args to integers"
    assert len(args) == 2
    a, b = [i.lower() for i in args]
    if a in aliases:
        m1 = aliases[a] - 1
    else:
        m1 = int(args[0])
    if b in aliases:
        m2 = aliases[b] - 1
    else:
        m2 = int(args[1])
    return m1, m2


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine()
    m1, m2 = GetArgs(args)
    matl1, matl2 = data_list[m1], data_list[m2]
    PrintTable(matl1, matl2)
