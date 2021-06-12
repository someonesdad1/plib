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
    from pdb import set_trace as xx
if 1:   # Custom imports
    from roundoff import RoundOff
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
 
    The code is from an Open Office macro in BASIC.
 
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
    return jmax
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
    return b*10**(m*n)
def EquivalentArea(n, m):
    '''Given a size n in AWG of a wire, return (D, d, ratio) where D is the
    first wire's area in inches, d is the second wire's diameter in inches,
    and ratio is (D/d)**2, which is the ratio of their cross-sectional
    areas (the ratio is rounded to 4 figures).
    '''
    if n > m:
        raise ValueError("n must be <= m")
    D, d = [AWG(i) for i in (n, m)]     # Diameter in inches
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
        return RoundOff(d, 4) if n <= 30 else RoundOff(d, 5)
    else:
        return RoundOff(92.**((36 - n)/39)/200, 4)
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
    i = 10244*AWG(n)**1.5
    return RoundOff(i, 3)
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
    A = (AWG(n)*1000)**2
    K = log10((1083 - Ta)/(234 + Ta) + 1)
    i = A*sqrt(K/(33*t))
    return RoundOff(i, 2)
if __name__ == "__main__": 
    import sys
    from lwtest import run, raises, assert_equal, Assert
    from wire import MaterialData, MaxCurrentDensity, Ampacity
    from wire import EquivalentArea, AWG, Preece, Onderdonk
    from pdb import set_trace as xx
    def TestMaterialData():
        d = MaterialData(material="copper")
        cus = 58e6  # Copper conductivity in S/m
        assert_equal(d["conductivity"], cus)
        assert_equal(d["resistivity"], 1/cus)
        assert_equal(d["temp_coeff"], 0.0039)
        assert_equal(d["density"], 8960)
        assert_equal(d["units"]["conductivity"], "S")
        assert_equal(d["units"]["resistivity"], "ohm*m")
        assert_equal(d["units"]["temp_coeff"], "1/K")
        assert_equal(d["units"]["density"], "kg/m3")
    def TestMaxCurrentDensity():
        assert_equal(MaxCurrentDensity(1, 60), 0.04425883723626271)
        assert_equal(MaxCurrentDensity(1, 75), 0.05533501092157374)
        assert_equal(MaxCurrentDensity(1, 90), 0.06367955209079165)
    def TestAmpacity():
        assert_equal(Ampacity(12, 60), 23.233252533606738)
        assert_equal(Ampacity(12, 75), 27.879903040328085)
        assert_equal(Ampacity(12, 90), 31.597223445705165)
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
        assert_equal(AWG(-3), 0.46)
        assert_equal(AWG(12), 0.0808)
        assert_equal(AWG(18), 0.0403)
        assert_equal(AWG(24), 0.0201)
        assert_equal(AWG(40), 0.00314)
        assert_equal(AWG(56), 0.0004919)
        # Check that we get exceptions for bad values
        raises(ValueError, AWG, -4)
        raises(ValueError, AWG, 1.1)
        raises(ValueError, AWG, 57)
    def TestPreece():
        assert_equal(Preece(0), 1900)
        assert_equal(Preece(10), 333)
        assert_equal(Preece(12), 235)
        assert_equal(Preece(18), 82.9)
        assert_equal(Preece(24), 29.2)
    def TestOnderdonk():
        t, Ta = 1, 20
        assert_equal(Onderdonk(0, t, Ta), 16000)
        assert_equal(Onderdonk(12, t, Ta), 960)
        assert_equal(Onderdonk(18, t, Ta), 240)
        assert_equal(Onderdonk(24, t, Ta), 59)
    exit(run(globals(), halt=1)[0])
