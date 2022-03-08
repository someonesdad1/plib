'''
Wire information
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2019 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <electrical> Wire information:  size, equivalent areas. ampacity,
    # and fusing current estimates.
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Imports
    from math import sqrt, log10, log
    from collections import namedtuple
    from pdb import set_trace as xx
if 1:   # Custom imports
    from roundoff import RoundOff
    try:
        from f import flt, pi
        have_flt = True
    except ImportError:
        have_flt = False
if 1:   # Global variables
    ii = isinstance
def MaterialData(material="copper"):
    '''Returns a dictionary containing the physical properties of the
    indicated material in SI units.
    '''
    # The following is the conductivity from the note (#6, but the number
    # can change) to the page
    # http://en.wikipedia.org/wiki/American_wire_gauge#cite_note-6.  The
    # value given on that web page is 58.0 MS/m at 68 deg F.  This also
    # agrees to 5 figures with the International Annealed Copper Standard
    # of 1.7241 μohm*cm.
    if have_flt:
        Cu_conductivity = flt("58.0e6 S/m")     # S/m at 20 deg C
        data = {
            "conductivity": Cu_conductivity,    # In S/m
            "resistivity": 1/Cu_conductivity,   # In ohm*m
            "temp_coeff": flt("0.0039 K-1"),    # In 1/K
            "density": flt("8960 kg/m3"),       # kg/m3
            "units": {
                "conductivity": "S",
                "resistivity": "ohm*m",
                "temp_coeff": "1/K",
                "density": "kg/m3",
            }
        }
    else:
        Cu_conductivity = 58.0e6 # S/m at 20 deg C
        data = {
            "conductivity": Cu_conductivity,   # In S/m
            "resistivity": 1/Cu_conductivity,  # In ohm*m
            "temp_coeff": 0.0039,              # In 1/K
            "density": 8960,                   # kg/m3
            "units": {
                "conductivity": "S",
                "resistivity": "ohm*m",
                "temp_coeff": "1/K",
                "density": "kg/m3",
            }
        }
    if material == "copper" or material == "Cu":
        return data
    # Factors to scale resistivity of copper to get resistivity of other
    # materials; all at 20 deg C.  The second number is used to scale 
    # the other material's density from copper's density.
    matl = {
        "aluminum": (1.6, 0.301),
        "Al": (1.6, 0.301),
        "Constantan": (29, 0.993),
        "iron": (5.8, 0.979),
        "Fe": (5.8, 0.979),
        "lead": (12.3, 1.27),
        "Pb": (12.3, 1.27),
        "Manganin": (27.5, 0.914),
        "platinum": (6.3, 2.39),
        "Pt": (6.3, 2.39),
        "silver": (0.95, 1.17),
        "Ag": (0.95, 1.17),
        "tungsten": (3.4, 2.15),
        "W": (3.4, 2.15),
        "zinc": (3.5, 0.796),
        "Zn": (3.5, 0.796),
        "Nichrome": (72.5, 0.938),
        "stainless steel": (40, 0.88),
    }
    if material not in matl:
        raise ValueError(f"Material '{material}' not recognized")
    factor, density_factor = matl[material]
    data[conductivity] = data[conductivity]/factor
    data[resistivity] = data[resistivity]*factor
    data[resistivity] = data[resistivity]*factor
    data[density] = data[density]*density_factor
    return data
def MaxCurrentDensity(diameter_m, insul_temp_rating_degC):
    '''This function returns the maximum allowed current density in
    A/mm2 given the wire diameter in m.  insul_temp_rating_degC is the
    insulation's temperature rating in deg C.  The algorithm is from the
    resistor.ods Open Office spreadsheet I wrote and ultimately comes
    from a linear regression of a log-log plot of the NEC allowed
    ampacities.  insul_temp_rating_degC must be 60, 75, or 90 deg C.
 
    The code is from an Open Office macro I wrote in BASIC.
 
    xx Update this to use the chassis current values from
    pgm/cu_wire.py.
    '''
    slope = -0.820  # Common to each curve
    if diameter_m <= 0:
        raise ValueError("diameter_m must be > 0")
    if insul_temp_rating_degC not in (60, 75, 90):
        raise ValueError("insul_temp_rating_degC must be 60, 75, or 90")
    ld = log(diameter_m*1000)/log(10)
    if ld < 0.21:
        # Constant current density
        jmax = 10**0.85
    elif ld < 0.315:
        # One curve in this region
        jmax = 10**(slope*ld + 1.032)
    elif ld < 0.41:
        ld = ld - 0.315
        dx = 0.095
        y = 0.775
        if insul_temp_rating_degC == 60:
            slope = (0.75 - y)/dx
        elif insul_temp_rating_degC == 75:
            slope = (0.82 - y)/dx
        else:
            slope = (0.87 - y)/dx
        jmax = 10**(y + ld*slope)
    else:
        if insul_temp_rating_degC == 60:
            b = 1.106  # y-intercept of fitted line
        elif insul_temp_rating_degC == 75:
            b = 1.203
        else:
            b = 1.264
        jmax = 10**(ld*slope + b)
    # Debug check of jmax
    if jmax > 10**0.93:  # Note:  max y value at ld = 0.41
        msg = ("Internal error:  bad current density: " +
               str(jmax) + " for " + str(insul_temp_rating_degC) +
               " and diameter in m = " + str(diameter_m))
        raise Exception(msg)
    return flt(jmax, units="A/mm2") if have_flt else jmax
def Ampacity(n, insul_temp_rating_degC):
    '''Return the allowed current in A for copper wire of size n in AWG.
    The insulation's temperature rating must be 60, 75, or 90 deg C.  The
    data are from the NEC for three or less wires in a raceway, cable, or
    earth for wire sizes larger than 16 AWG or for single unbundled wires
    of 16 AWG and smaller.
 
    The table data are incomplete from the wikipedia page.  I plotted the
    data that were given and interpolated the other values using my
    engineering judgment.  See the /pylib/pgm/ampacity.py script for the
    plot of the data and the fitted piecewise-linear models.  Note the
    models are conservative with respect to the wikipedia tabulation.
 
    xx Update this to use the chassis current values from
    pgm/cu_wire.py.
    '''
    # Data from
    # https://en.wikipedia.org/wiki/American_wire_gauge#Tables_of_AWG_wire_sizes
    # which attributes the table data.
    if not (-3 <= n <= 34):
        raise ValueError("AWG value n must be between -3 and 34 inclusive")
    if insul_temp_rating_degC not in (60, 75, 90):
        raise ValueError("insul_temp_rating_degC must be 60, 75, or 90")
    if n < 18:
        m, b = -0.0609, 170
        if insul_temp_rating_degC == 60:
            b = 125
        elif insul_temp_rating_degC == 75:
            b = 150
    else:
        m, b = -0.1068, 1150
        if insul_temp_rating_degC == 60:
            b = 840
        elif insul_temp_rating_degC == 75:
            b = 1000
    i = b*10**(m*n)
    return flt(i, units="A") if have_flt else i
def EquivalentArea(n, m):
    '''Given a size n in AWG of a wire, return (D, d, ratio) where D is the
    first wire's area in inches, d is the second wire's diameter in inches,
    and ratio is (D/d)**2, which is the ratio of their cross-sectional
    areas (the ratio is rounded to 4 figures).
    '''
    if n > m:
        raise ValueError("n must be <= m")
    D, d = [AWG(i) for i in (n, m)]     # Diameter in inches
    if have_flt:
        D = flt(D, units="inch")
        d = flt(d, units="inch")
    return D, d, RoundOff((D/d)**2, digits=4)
def AWG(n):
    '''Returns the wire diameter in inches given the AWG (American Wire
    Gauge) number (also known as the Brown and Sharpe gauge).  Use negative
    numbers as follows:  -1 means 2/0, -2 means 3/0, and -3 means 4/0.
 
    n must be an integer in the closed interval [-3, 56].
    '''
    if not hasattr(AWG, "data"):
        AWG.data = (
            # Diameter in 1e5 inch units of AWG wire sizes from -3 (4/0) to
            # 40 AWG.
            46000, 40960, 36480, 32490, 28930, 25760, 22940, 20430, 18190,
            16200, 14430, 12850, 11440, 10190, 9070, 8080, 7199, 6410,
            5710, 5080, 4530, 4030, 3590, 3200, 2850, 2530, 2260, 2010,
            1790, 1590, 1420, 1260, 1130, 1000, 893, 795, 708, 630, 561,
            500, 445, 396, 353, 314
        )
    if not ii(n, int) or (n > 56) or (n < -3):
        raise ValueError("n must be an integer in [-3, 56]")
    # We use a table lookup for 40 gauge or larger and a formula for 41 to
    # 56 gauge.
    try:
        data = getattr(AWG, "data")
    except AttributeError:
        pass
    if n <= 40:
        d = AWG.data[n + 3]/1e5
        d = RoundOff(d, 4) if n <= 30 else RoundOff(d, 5)
    else:
        d = RoundOff(92.**((36 - n)/39)/200, 4)
    return flt(d) if have_flt else float(d)
def Preece(n):
    '''Returns the fusing current in A to 3 figures for copper wire in size
    n AWG.  The formula used is Preece's formula, which estimates how much
    current a copper wire can handle before the conductor reaches the
    melting point of copper.  The wire won't actually melt, as the formula
    doesn't include the enthalpy of fusion.  The formula is 
 
        i = 10244*d**1.5
      
    where 
        d = wire diameter in inches 
        i = current in A
 
    Reference:
    https://pcdandf.com/pcdesign/index.php/magazine/10179-pcb-design-1507
  
    Example:  For 12 gauge copper wire (d = 0.08081 inches), the fusing
    current is 235 A.
    '''
    d = AWG(n)  # Diameter in inches as a dimensionless flt
    i = 10244*d**1.5
    i = RoundOff(i, 3)
    return flt(i) if have_flt else float(i)
def Onderdonk(n, t, Ta):
    '''Fusing current in A for copper wire
 
    n = AWG size of wire
    t = time in s (limited to 10 s or less)
    Ta = ambient temperature in °C
 
    Returns the current in amperes to 2 significant figures for copper
    wire of size n AWG to reach the melting point of copper (1083 °C) in
    a given time t seconds for an ambient temperature of Ta in °C using
    Onderdonk's equation:
 
        i = A*sqrt(K/(33*t))
     
    This is taken from
    https://pcdandf.com/pcdesign/index.php/magazine/10179-pcb-design-1507
    and is slightly more general than the original form of Onderdonk's
    equation, which was given for Ta = 40 °C in E. R. Stauffacher (June
    1928), "Short-time Current Carrying Capacity of Copper Wire", General
    Electric Review, 31 (6) (a copy can be found at
    http://ultracad.com/articles/reprints/stauffacher.pdf).  The variables
    are:
        
        i = current in A
        A = cross-sectional area of wire in circular mils (square the 
            diameter of the wire in mils)
        t = time in seconds the current is applied 
        Ta = ambient temperature in °C
        K = log10((1083 - Ta)/(234 + Ta) + 1)
 
    Example:  4/0 AWG wire has a diameter of 460 mils.  At Ta = 25 °C,
    what current can be applied to the wire for 1 s?
 
        K = log10((1083 - 25)/259 + 1) = log10(1058/259 + 1) = 0.7063
        A = 460*460 = 211600 circular mils
        t = 1 second
 
    Therefore
 
        i = 211600*sqrt(0.7063/(33*1)) = 30956 amperes
 
    This function would round this off to 31 kA.  The table on the
    wikipedia page https://en.wikipedia.org/wiki/American_wire_gauge gives
    33 kA, but the page doesn't say how its computation was done.
 
    The time t in seconds is arbitrarily limited to a maximum of 10
    because the derivation ignores heat losses from the wire due to
    convection, conduction, and radiation.  In reality, it's probably
    only appropriate to consider times on the order of a second or so.
    '''
    if t > 10:
        raise ValueError("Time t must be <= 10 seconds")
    d = AWG(n)  # Diameter in inches as a flt
    A = (d*1000)**2
    K = log10((1083 - Ta)/(234 + Ta) + 1)
    i = A*sqrt(K/(33*t))
    i = RoundOff(i, 2)
    return flt(i) if have_flt else float(i)
def GetAmpacityData(dbg=False):
    '''Return a dictionary keyed by AWG size (as a string) with the
    values
        Diameter, inches
        Maximum current for chassis wiring, A
        Maximum current for power transmission, A (based on the
            conservative rule of j = 2.8 A/mm² = 1.43 mA/cmil)
        Maximum frequency for 100% skin depth for solid copper, Hz
        Breaking force in lbf for annealed Cu (37 kpsi)
 
    The following data come from
    https://www.powerstream.com/Wire_Size.htm
        Column 1:  AWG
        Column 2:  Diameter, inches
        Column 3:  Maximum current for chassis wiring, A
        Column 4:  Maximum current for power transmission, A
        Column 5:  Maximum frequency for 100% skin depth for solid copper
        Column 6:  Breaking force in lbf for annealed Cu (37 kpsi)
    '''
    Ampac = namedtuple("Ampac", "AWG dia chass pwr freq brk")
    data = '''
    -3, 0.46  , 380 , 302   , 125 Hz  , 6120 lbs
    -2, 0.4096, 328 , 239   , 160 Hz  , 4860 lbs
    -1, 0.3648, 283 , 190   , 200 Hz  , 3860 lbs
     0, 0.3249, 245 , 150   , 250 Hz  , 3060 lbs
     1, 0.2893, 211 , 119   , 325 Hz  , 2430 lbs
     2, 0.2576, 181 , 94    , 410 Hz  , 1930 lbs
     3, 0.2294, 158 , 75    , 500 Hz  , 1530 lbs
     4, 0.2043, 135 , 60    , 650 Hz  , 1210 lbs
     5, 0.1819, 118 , 47    , 810 Hz  , 960 lbs
     6, 0.162 , 101 , 37    , 1.1 kHz , 760 lbs
     7, 0.1443, 89  , 30    , 1.3 kHz , 605 lbs
     8, 0.1285, 73  , 24    , 1.65 kHz, 480 lbs
     9, 0.1144, 64  , 19    , 2.05 kHz, 380 lbs
    10, 0.1019, 55  , 15    , 2.6 kHz , 314 lbs
    11, 0.0907, 47  , 12    , 3.2 kHz , 249 lbs
    12, 0.0808, 41  , 9.3   , 4.15 kHz, 197 lbs
    13, 0.072 , 35  , 7.4   , 5.3 kHz , 150 lbs
    14, 0.0641, 32  , 5.9   , 6.7 kHz , 119 lbs
    15, 0.0571, 28  , 4.7   , 8.25 kHz, 94 lbs
    16, 0.0508, 22  , 3.7   , 11 kHz  , 75 lbs
    17, 0.0453, 19  , 2.9   , 13 kHz  , 59 lbs
    18, 0.0403, 16  , 2.3   , 17 kHz  , 47 lbs
    19, 0.0359, 14  , 1.8   , 21 kHz  , 37 lbs
    20, 0.032 , 11  , 1.5   , 27 kHz  , 29 lbs
    21, 0.0285, 9   , 1.2   , 33 kHz  , 23 lbs
    22, 0.0253, 7   , 0.92  , 42 kHz  , 18 lbs
    23, 0.0226, 4.7 , 0.729 , 53 kHz  , 14.5 lbs
    24, 0.0201, 3.5 , 0.577 , 68 kHz  , 11.5 lbs
    25, 0.0179, 2.7 , 0.457 , 85 kHz  , 9 lbs
    26, 0.0159, 2.2 , 0.361 , 107 kHz , 7.2 lbs
    27, 0.0142, 1.7 , 0.288 , 130 kHz , 5.5 lbs
    28, 0.0126, 1.4 , 0.226 , 170 kHz , 4.5 lbs
    29, 0.0113, 1.2 , 0.182 , 210 kHz , 3.6 lbs
    30, 0.01  , 0.86, 0.142 , 270 kHz , 2.75 lbs
    31, 0.0089, 0.7 , 0.113 , 340 kHz , 2.25 lbs
    32, 0.008 , 0.53, 0.091 , 430 kHz , 1.8 lbs
    33, 0.0071, 0.43, 0.072 , 540 kHz , 1.3 lbs
    34, 0.0063, 0.33, 0.056 , 690 kHz , 1.1 lbs
    35, 0.0056, 0.27, 0.044 , 870 kHz , 0.92 lbs
    36, 0.005 , 0.21, 0.035 , 1.1 MHz , 0.72 lbs
    37, 0.0045, 0.17, 0.0289, 1.35 MHz, 0.57 lbs
    38, 0.004 , 0.13, 0.0228, 1.75 MHz, 0.45 lbs
    39, 0.0035, 0.11, 0.0175, 2.25 MHz, 0.36 lbs
    40, 0.0031, 0.09, 0.0137, 2.9 MHz , 0.29 lbs'''[1:]
    wt = {}
    if dbg:
        print("Column 1:  AWG")
        print("Column 2:  Diameter, inches")
        print("Column 3:  Maximum current for chassis wiring, A")
        print("Column 4:  Maximum current for power transmission, A")
        print("Column 5:  Maximum frequency in kHz for 100% skin depth for Cu wire")
        print("Column 6:  Breaking force in lbf for annealed Cu (37 kpsi)")
        #print("  AWG Dia, in      Chassis, A       Power, A")
    for line in data.split("\n"):
        f = line.split(",")
        awg = int(f[0].strip())
        dia_in = flt(f[1])
        chassis_A = flt(f[2])
        pwr_A = flt(f[3])
        freq = flt(f[4])
        if 0:
            # http://www.nessengr.com/technical-data/skin-depth/ gives the
            # formula for Cu as δ = 0.066/sqrt(f) for δ = skin depth in m
            # and f in Hz.  Then f = 0.00436/δ**2.
            δ = (dia_in*25.4/1000)/2  # Radius is the skin depth
            f_kHz = flt((0.066/δ)**2/1000)
            # Check that calculated and table values are close
            alpha = 0.07
            alpha = 0.5  #xx Temp to see table
            if not (1 - alpha < freq/f_kHz < 1 + alpha):
                print(freq/f_kHz, awg)
                exit()
        # Note the tabulated breaking values aren't quite correct -- use
        # calculated value instead.
        area = pi*dia_in**2/4
        uts = flt(37000)    # In psi
        brk = area*uts      # In lbf
        if dbg:
            print(f"{awg:>2d}, {dia_in!s:>15s}, {chassis_A!s:>10s}, "
                f"{pwr_A!s:>10s}, {freq!s:>12s}, {brk!s:>12s}")
        else:
            wt[awg] = Ampac(awg, dia_in, chassis_A, pwr_A, freq, brk)
    return wt
def PlotAmpacityData():
    '''Plot chass and pwr data to derive a formula.

    The results show that the chassis ampacity data can be modeled by
    two power functions imax = a*dia_mm**e:
        For dia < 1.3 mm:  a = 13, e = 2
        For dia >= 1.3 mm:  a = 16, e = 1.3
    '''
    w, x = GetAmpacityData(), flt(0)
    Dia, Chass, Pwr = [], [], []
    for i in w:
        item = w[i]
        Dia.append(item.dia.to("mm").val)
        Chass.append(item.chass.val)
        Pwr.append(item.pwr.val)
    from pylab import plot, loglog, xlabel, ylabel, title, text
    from pylab import legend, grid, show, array, savefig, axvline
    from f import pi
    dia, chass, pwr = [array(i) for i in (Dia, Chass, Pwr)]
    p = plot
    p = loglog
    p(dia, pwr, "b-", label="j = 2.8 A/mm²")
    p(dia, chass, "r.", label="Chassis data")
    if 1:
        # Fit a power function i = a*d**e to the chassis data.  From the
        # scatter plot, it's clear that two linear approximations on a
        # log-log plot are adequate.
        #
        # Choose the exponent e and fit the constant a to a chosen data
        # point:  a = i*d**-e
        #
        # Cutoff point for the two straight line approximation
        m = len(dia) - 25
        n = 0
        i, d = chass[n], dia[n]
        e = 1.3
        a = i*d**-e
        D = dia[:m + 1]
        # Calculate j at point m//2
        di, i = dia[m//2], chass[m//2]
        with x:
            x.n = 2
            p(D, a*D**e, "g", label=f"a={flt(a)}, e={e}")   # Green line
        # The smaller diameters are at a larger slope.  Make it go
        # through the 0.3 mm diameter point
        n = -11
        i, d = chass[n], dia[n]
        e = 2
        a = i*d**-e
        D = dia[m - 3:]
        # Calculate j at point 3*m//2
        di, i = dia[3*m//2], chass[3*m//2]
        with x:
            x.n = 2
            p(D, a*D**e, "k", label=f"a={flt(a)}, e={e}")   # Black line
            bp = flt(Dia[m], "mm")
            text(1.1*Dia[m], 225, f"d = {bp}")
            axvline(x=bp.val, color="k", linestyle="--")
    xlabel("d = wire diameter, mm")
    ylabel("i = maximum current, A")
    title("Copper wire ampacities\nRef:  https://www.powerstream.com/Wire_Size.htm")
    text(2, 0.02, "DP 14 Jun 2021")
    text(2, 0.05, "Model:  i = a*d**e")
    legend()
    grid()
    if 0:
        show()
    else:
        savefig("wire.png")
def ChassisAmpacity(dia):
    '''Return the maximum chassis current for copper wire near room
    temperature for a given diameter dia.  If dia is an integer, it 
    will be interpreted as AWG.  If it is a float, it will be
    interpreted as diameter in mm.  Or, set it to a flt with suitable
    length units.

    The PlotAmpacityData() function shows that a suitable model is
    imax = a*dia_mm**e where
        a = 13, e = 2 for dia < 1.3 mm
        a = 16, e = 1.3 for dia >= 1.3 mm
    '''
    if ii(dia, int):
        D = AWG(dia)
        if not have_flt:
            D *= 25.4   # Convert to mm
    elif ii(dia, flt):
        if dia.u is None:
            D = flt(float(dia), "mm")
        else:
            D = dia.to("mm")
    else:
        D = flt(float(dia), "mm")
    assert(ii(D, flt))
    Dmax = flt(AWG(-3)*25.4, "mm")
    if D > Dmax:
        raise ValueError(f"Wire diameter must be <= {Dmax}")
    if D >= flt("1.3 mm"):
        imax = flt(16*D.val**1.3, "A")
    else:
        imax = flt(13*D.val**2, "A")
    return imax
if 0:
    PlotAmpacityData()
    exit()
if __name__ == "__main__": 
    import sys
    from lwtest import run, raises, assert_equal, Assert
    from pdb import set_trace as xx
    x = flt(0)
    def TestMaterialData():
        d, x = MaterialData(material="copper"), flt(0)
        cus = 58e6  # Copper conductivity in S/m
        with x:
            x.promote = 1
            assert_equal(d["conductivity"], cus)
            assert_equal(d["resistivity"], 1/cus)
            assert_equal(d["temp_coeff"], 0.0039)
            assert_equal(d["density"], 8960)
            assert_equal(d["units"]["conductivity"], "S")
            assert_equal(d["units"]["resistivity"], "ohm*m")
            assert_equal(d["units"]["temp_coeff"], "1/K")
            assert_equal(d["units"]["density"], "kg/m3")
    def TestMaxCurrentDensity():
        if have_flt:
            f = lambda x: flt(x, units="A/mm2")
        else:
            f = lambda x: x
        assert_equal(MaxCurrentDensity(1, 60), f(0.04425883723626271))
        assert_equal(MaxCurrentDensity(1, 75), f(0.05533501092157374))
        assert_equal(MaxCurrentDensity(1, 90), f(0.06367955209079165))
    def TestAmpacity():
        if have_flt:
            f = lambda x: flt(x, units="A")
        else:
            f = lambda x: x
        assert_equal(Ampacity(12, 60), f(23.233252533606738))
        assert_equal(Ampacity(12, 75), f(27.879903040328085))
        assert_equal(Ampacity(12, 90), f(31.597223445705165))
    def TestEquivalentArea():
        dn, dm, r = EquivalentArea(12, 14)
        assert_equal(r, 1.589)
        dn, dm, r = EquivalentArea(12, 16)
        assert_equal(r, 2.53)
        dn, dm, r = EquivalentArea(12, 18)
        assert_equal(r, 4.02)
        dn, dm, r = EquivalentArea(12, 30)
        assert_equal(r, 65.29)
    def TestAWG():
        assert_equal(AWG(-3), flt(0.46))
        assert_equal(AWG(12), flt(0.0808))
        assert_equal(AWG(18), flt(0.0403))
        assert_equal(AWG(24), flt(0.0201))
        assert_equal(AWG(40), flt(0.00314))
        assert_equal(AWG(56), flt(0.0004919))
        # Check that we get exceptions for bad values
        raises(ValueError, AWG, -4)
        raises(ValueError, AWG, 1.1)
        raises(ValueError, AWG, 57)
    def TestPreece():
        with x:
            x.promote = 1
            assert_equal(Preece(0), 1900)
            assert_equal(Preece(10), 333)
            assert_equal(Preece(12), 235)
            assert_equal(Preece(18), 82.9)
            assert_equal(Preece(24), 29.2)
    def TestOnderdonk():
        t, Ta = 1, 20
        with x:
            x.promote = 1
            assert_equal(Onderdonk(0, t, Ta), 16000)
            assert_equal(Onderdonk(12, t, Ta), 960)
            assert_equal(Onderdonk(18, t, Ta), 240)
            assert_equal(Onderdonk(24, t, Ta), 59)
    def TestChassisAmpacity():
        for d in (0.1, 0.2, 0.5, 0.75, 1):
            got = ChassisAmpacity(flt(d, "mm"))
            expected = flt(13*d**2, "A")
            assert_equal(got, expected)
        for d in (1.3, 1.5, 2, 3, 5, 7.5, 10):
            got = ChassisAmpacity(flt(d, "mm"))
            expected = flt(16*d**1.3, "A")
            assert_equal(got, expected)
    exit(run(globals(), halt=1)[0])
