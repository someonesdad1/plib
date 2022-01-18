'''
TODO:
 
* Add -L option to specify a length.  Then table should print resistance of
  that length.
* Change -i option to use u.py library so common units can be input.
* Finish MIL5088(gauge, ΔT) function.
 
----------------------------------------------------------------------
Output a copper wire table.  Other useful things are done too (use the 
-h option for help and -H for a manpage).
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Copper wire table and ancillary information
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import os
    import getopt
    from math import pi, log, sqrt, log10
if 1:   # Custom imports
    import color as C
    from wrap import dedent
    from fpformat import FPFormat
    from columnize import Columnize
    from roundoff import RoundOff
    from wire import AWG, Ampacity
    from sig import sig
    from u import u, ParseUnit
    from f import flt
    # Debugging
    from pdb import set_trace as xx
    if 0:
        import debug
        debug.SetDebugger()
    if 0:
        # For interactive use
        from pnumber import PhysicalNumber as PN, PhysicalNumberFactory as PNF
        from getinput import Choice
        from get import GetNumber, GetWireDiameter
if 1:   # Global variables
    # Copper properties
    resistivity = 17.241e-9     # Cu resistivity in Ω·m at 20 °C
    temp_coeff = 0.0039         # Temperature coefficient of resistivity, 1/K
    density = 8900              # kg/m³
    isatty = sys.stdout.isatty()
    no_color = False
    # Color of popular gauge sizes
    popular_sizes = {
        10: (C.lgreen, C.black),
        12: (C.yellow, C.blue),
        14: (C.brown, C.black),
        18: (C.lred, C.black),
        16: (C.yellow, C.lmagenta),
        20: (C.lmagenta, C.black),
        24: (C.yellow, C.black),
    }
    # Used for formatting numbers
    fp = FPFormat(4)
    fp.trailing_decimal_point(False)
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Manpage():
    rho = f"{resistivity*1e9:.5g}"
    print(dedent(f'''
                                Copper Wire Table
    
    The properties of commercial copper wire in this table are calculated
    from the density of copper ({density} kg/m³) and its room temperature
    resistivity of {rho} nΩ·m.
    
    AWG is American Wire Gauge [1].  Given an AWG number N, the diameter of
    a wire in inches is 92**((36 - N)/39)/200.  For 2/0, 3/0, or m/0 where
    m >= 2, use an N of 1 - m.
    
    Useful approximations to memorize are that 12 gauge wire is about 2 mm
    in diameter and 18 gauge wire is about 1 mm in diameter (if you want
    approximate inches, multiply mm by 2 twice and divide by 100).
    Changing 6 AWG gauge numbers changes the wire diameter by about 2.  Use
    the -e option to see areal relationships amongst the gauge sizes.
 
    Another useful tidbit is that a 1 foot long chunk of 10 gauge copper
    has a resistance of about 1 mΩ.
    
    To estimate the electrical behavior of copper as a function of
    temperature, you need to know:
    
        * The resistivity of copper as a function of absolute temperature
          is essentially linear to about 600 K and then slightly concave
          upwards (a power of T slightly above unity) up to the melting
          point of 1083 °C (1356 K). [6]
    
          A practical resistivity estimate for copper is 0.071*(T - 50)
          nΩ*m where T is absolute temperature in K or about 0.071*(Tc +
          223) nΩ*m where Tc is temperature in °C.  This is for T < 600 K
          or Tc < 327 °C.
    
        * The specific heat of copper (∂h(T, p)/∂T at constant p where h is
          the enthalpy) is described by a Shomate equation (a cubic
          polynomial in absolute temperature with another term of T**-2)
          that is approximately linear from 300 K (room temperature) to 900
          K with a slope of 5.4 mJ/(mol*K). [7]
    
        * The change in length of commercial copper from room temperature
          to the melting point is about 2%.  Thus, the change in volume for
          instrinsic specific physical quantities as a function of
          temperature will be about 6%. [8]
    
    Over the indicated temperature ranges, these linear relationships make
    integrations easier.
    
                                    Ampacity
    ----------------------------------------------------------------------
    
    Ampacity refers to the allowed current carrying ability of copper wire.
    In general, what is allowed physically is dependent on many things
    because it is ultimately a heat transfer problem where the Joule heat
    from the current in the wire needs to be removed by conduction,
    convection, and radiation at a sufficiently rapid rate to keep the
    temperature of the wire below a desired value.  For most practical
    electrical problems, convection and conduction are the most important
    for heat transfer and the orientation and bundling of wires can be
    important.
    
    The script prints a number of ampacity values when you use the -a option.  
    
    Chass
    -----
    
    The Chass (chassis) current is for a single wire in air (i.e., not in a
    bundle of wires) and is probably near the maximum current you would want to
    put through a copper wire for practical purposes.  I have tested these
    values on 18 gauge and smaller wires and found that the wires and their
    insulations are noticeably heated, but not hot enough to melt the
    insulation.  From [3].

    It appears to me that these estimates often come from the military
    standard MIL5088 [9], which covers the design of aerospace vehicles.
    This information was derived from experiments in the 1960's.  More
    modern comments are in [10].
    
        Experiment:  At a room temperature of about 20 °C, I connected an
        18 gauge solid copper wire 80 mm long clamped between two alligator
        clips to an HP 6033A DC power supply (supplies up to 30 A).  The
        current was set to the Chass current of 16 A and left on for 10
        minutes.  The wire was comfortably warm to the fingers, but one of
        the steel alligator clips was too hot to leave my fingers on it for
        more than 1 second.  My engineering judgment is that this wire's
        temperature rise would be fine in a project that wouldn't go over
        35 or 40 °C ambient temperature.  At a current of 20 A (50% higher
        power dissipation), the wire's insulation was hot enough that I
        wouldn't want to hold it for more than a second or two and one of
        the alligator clips was too hot to touch, even for 0.2 s or so.
        This "finger touch test" can indicate temperatures on the order of
        40 to 50 °C.
    
        More specific guidelines [5] give the continuously-held maximum
        temperature for all materials at 43 °C (if held for < 10 s, then 55
        °C for metals and 65 °C for non-metals; if touched for < 1 s, then
        65 °C for metals and 85 °C for non-metals).  Non-metals are higher
        because they conduct less heat to the skin per unit time.  Most of
        us learn we can coat our finger with saliva and touch things
        perhaps 100 to 150 °C quickly, feeling and hearing a hiss.  We're
        not burned because the heat of vaporization of the fluid keeps the
        heat from conducting to our skin (sometimes called the Leidenfrost
        effect).
    
        A second wire (about 21 gauge, pulled from a surplus military
        device) was run at 9 A, which is halfway between the two nearest
        Chass table values.  It also felt fine to my fingers, but
        sensitivity goes down on smaller wires.  I increased the current by
        1.25 times to 11.25 A (increased the dissipated power by 50%) and
        it was warmer after about 5 minutes, but not objectionably so.
        This excellent wire was likely more expensive than regular wire, as
        it was stranded and appeared to be tinned with solder.
    
        Rigging up some kind of temperature monitoring for this experiment
        would make it more quantitative, but measuring the temperature of a
        small wire without influencing the heat loss mechanisms is more
        work that I'd want to invest.  Still, the experiment provided me
        with enough of an engineering feel (no pun :^) that these current
        levels would be safe should I want to base a design on them.  I
        don't have a DC power supply capable of enough current to study
        wires at higher DC currents.
    
        A 24 gauge piece of copper wire held in alligator clips with 30 A
        through the wire will glow a faint red in a room with the curtains
        drawn during the daytime.  This should only be done for 10 or 20 s,
        as the alligator clips will get hot.  From past experiments with
        heated metals, I'd guess the temperature was around 550 to 600 °C.
    
    Note the current densities (j in A/mm²) for these Chass ratings are not
    constant:
    
            AWG  j         AWG  j          AWG  j
            --- ---        --- ---         --- ---
             0  4.5         14  15          28  17
             2  5.4         16  17          30  17
             4  6.6         18  19          32  17
             6  7.5         20  21          34  16
             8  8.7         22  22          36  17
            10   11         24  17          38  16
            12   12         26  17          40  18
    
    When plotted, these data make me think someone derived these numbers from
    an experiment.
    
    Pwr
    ---
    
    The Pwr (power transmission) current is based on a maximum current density
    of 2.82 A/mm² at DC conditions (this is quite conservative; compare it to
    the Chass current densities above).
    
    NEC Ratings
    -----------
    
    The NEC ratings are based on [2].  The values from 0 to 14 AWG are
    specified by the NEC.  For 10, 12, and 14 gauge copper wire, note the
    allowed currents in the table are higher than the circuit breaker rating
    for a circuit wired with that wire, which must be 30, 20, and 15 A,
    respectively, after corrections for ambient temperature and number of
    conductors have been applied.
    
    The NEC ratings are more conservative than e.g. the Chassis current rating
    because e.g. the wiring in a house must last for many decades and not cause
    a fire.  When a city inspector approves an electrical installation, the
    city (among others) is liable if that installation fails.  Thus,
    governments will choose conservative and well-established rules for
    construction to minimize their legal exposure.
    
                                    Fusing
    ----------------------------------------------------------------------
    
    At high currents, enough Joule heat is generated in a wire to raise its
    temperature; if the temperature is raised enough, the wire can melt.  To
    calculate the current necessary to melt the wire, you have to solve for the
    heat loss to the environment, the heat to raise the metal's temperature
    (using the metal's specific heat (enthalpy)), and the heat to cause the
    phase change from solid to liquid (heat of fusion).  
    
    Two treatments of this have been given in the literature:  Preece and
    Onderdonk (see [4]).  Preece's experiment in the 1880's resulted in a
    simple relationship:  the fusing current in A is proportional to the wire
    diameter in inches to the 3/2 power.  The constant for copper is 10244.
    
    Who Onderdonk was is unknown, but he has an equation named after him.  This
    equation relates the following physical quantities:
    
        * Fusing current
        * Cross-sectional area of wire
        * Time the current is applied to the wire
        * Rise in temperature from the ambient to e.g. the melting temperature
            of the wire
    
    The relevance of Onderdonk's work and the reason for the inclusion of time
    is that power transmission designs have to carry short circuit currents for
    a sufficient amount of time for the mechanical switching devices to open
    the circuit to protect the conductors.
    
    Reference [4] gives a derivation for Onderdonk's equation by relating the
    Joule heating of the wire to the temperature rise of the copper from the
    Joule heat.  Key assumptions are 1) copper's resistivity increases linearly
    with the temperature increase over ambient, 2) copper's specific heat is
    constant to the melting point, and 3) the time involved is short enough
    that heat losses to the environment can be ignored.  The treatment results
    in a first order linear differental equation for the wire temperature as a
    function of time.  The "short time" should probably no more than a few
    seconds.  The derivation ignores the heat of fusion of the conductor, which
    is probably reasonable, as once the conductor is at the melting point,
    mechanical disruption is likely due to the mass of the conductor (i.e., its
    own weight and loss of tensile strength could cause it to separate).
    
    If you're interested in seeing Onderdonk's equation, look at the
    Onderdonk() function in the script.
    
                                References
    ----------------------------------------------------------------------
    
    [1] https://en.wikipedia.org/wiki/American_wire_gauge
    
    [2] NEC is the National Electrical Code for the US.  It is a publication
        of the National Fire Protection Association and is the basic
        standard used for describing safe electrical practices.  See
        https://www.nfpa.org.
    
    [3] SAMS, Handbook of Electronics Tables and Formulas, various editions.
        The web page https://www.powerstream.com/Wire_Size.htm quotes this
        reference as the source for the Chassis wiring ampacity values (I don't
        have a copy of the original book).
    
    [4] https://pcdandf.com/pcdesign/index.php/magazine/10179-pcb-design-1507
    
    [5] ECMA-287 gives table 5.2 that specifies allowable touch temperatures
        based on time of contact and material type.  Referenced here:
        https://www.boydcorp.com/resources/resource-center/blog/
            237-maximum-touch-temperature.html
    
    [6] https://en.wikipedia.org/wiki/
        Electrical_resistivity_and_conductivity#Metals
    
    [7] See the plot at https://webbook.nist.gov/cgi/
        cbook.cgi?ID=C7440508&Units=SI&Mask=7&Type=JANAFS&Plot=on#JANAFS
    
    [8] "Metals Handbook", Vol. 1, 8th ed., American Society of Metals, 1961,
        copper graphs on page 1009.
    
    [9] MIL-W-5088L.  In particular, look at Figure 3 on page 46 and 47.
        The Chass ratings in this script come pretty close to the numbers 
        given in MIL-W-5088L for a ΔT of 60°C.  If you assume an ambient
        temperature of 30°C, then this means the insulation temperature
        will be around 90°C, a common insulation temperature rating.  
   [10] https://www.lectromec.com/maximum-harness-ampacity and
        https://www.lectromec.com/ampacity-improvements.
        '''.rstrip()))
    print(dedent(f'''
 
    Other information
    -----------------
    
    For copper wire with silicone rubber insulation rated to 150 to 200 °C,
    the approximate current density in A/mm² is 9.1 for 23 ga, 15 for 21
    ga, and 20 for 20 ga.
    
    Resistance per unit length is for solid copper.  Stranded wire of the
    same size can have a resistance up to 8% higher.  Twisting wires together
    can add 0.5% to 3% more resistance because of increased length.
    
    Resistivity of Cu is {rho} nΩ·m.  Factors for other materials (at 20 °C):
    Al: 1.6, Brass: 4.1, Graphite: 2-36, Constantan (55Cu-45Ni): 29.1, Fe: 5.8,
    Pb: 12.3, Manganin (86Cu-12Mn-2Ni): 25-27.9, Pt: 6.28, Ag: 0.950, W: 3.38,
    Zn: 3.54, Nichrome(~ 80Ni-20Cr, sometimes Fe): 58-87, Stainless steel: 40
    
    The 0.041" diameter stainless steel wire from Harbor Freight has a resistance
    of 0.1 Ω per 119 mm = 8.4 mΩ/cm = 21 mΩ/inch = 0.26 Ω/ft.
    
    RG-58/U coax has a 0.9 mm diameter inner conductor (19 gauge) and an outside
    diameter of 5 mm.  Capacitance is 90 ± 5 pF/m.
    
    1000·TCR in 1/K @ 20 °C:  annealed copper: 3.93, aluminum: 3.8, carbon:
    -0.25, iron: 5.0, lead: 4.3, Pt: 3.8, Ag: 4.0, W: 4.5, Zn: 3.7
    '''))
    exit(0)
def ParseCommandLine(d):
    d["-a"] = False     # Print the detailed ampacity data
    d["-C"] = False     # Emit color escape codes even if not a tty
    d["-c"] = False     # Emit color escape codes even if not a tty
    d["-e"] = False     # Print an equivalence table
    d["-i"] = False     # Interactive solution
    d["-F"] = False     # Print full table
    d["-f"] = False     # Print big stuff
    d["-t"] = False     # Print equivalence table
    d["-v"] = False     # Print voltage drop table
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "aCceFfhHitv")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in optlist:
        if o[1] in list("aCceFftv"):
            d[o] = not d[o]
        elif o == "-h":
            Usage(status=0)
        elif o == "-H":
            Manpage()
        elif o == "-i":
            Error("-i option not currently supported")
            Interactive()
    if args and len(args) not in (1, 2):
        Usage()
    if d["-c"]:
        global isatty
        isatty = True
    if d["-C"]:
        global no_color
        no_color = True
    return args
def Usage(status=1):
    name = sys.argv[0]
    print(dedent(f'''
    Usage:  {name} [options] [n_awg m_awg]
        With no arguments, print a copper wire table.  With one argument, 
        print out a table of needed wires of other sizes to get equal area.
        With two arguments, print the number of wires of the smaller wire
        to match the area of the larger wire.
    Options:
        -a  Print detailed ampacity data
        -C  Do not print in color
        -c  Include escape sequences for color if std out is not a terminal
        -e  Print out an equivalence table showing how many wires of a
            particular gauge size are equal to another
        -f  Print table of big sizes by 1 gauge steps
        -F  Print full table by 1 gauge steps
        -h  Print this help message
        -H  Print detailed help message
        -i  Interactively determine length, diameter, resistivity, or
            resistance
        -t  Show table for big wire equivalents
        -v  Show voltage drop table
    '''[1:-1]))
    exit(status)
def ShowResistivities():
    r = (
        ("Aluminum",        "1.6"),
        ("Graphite",        "2 to 36"),
        ("Constantan",      "29"),
        ("Iron",            "5.8"),
        ("Lead",            "12.3"),
        ("Manganin",        "25 to 28"),
        ("Platinum",        "6.3"),
        ("Silver",          "0.95"),
        ("Tungsten",        "3.4"),
        ("Zinc",            "3.5"),
        ("Nichrome",        "58 to 87"),
        ("St. steel", "40"),
    )
    print("Resistivities relative to copper at 20 °C:")
    f, items = "{:12s} {}", []
    for i in sorted(r):
        items.append(f.format(*i))
    for i in Columnize(items, indent="  "):
        print(i)
def Interactive():
    '''Prompt the user for three of (d, L, rho, R) and calculate the
    fourth.
    '''
    print("Solves for resistance, length, diameter, or resistivity:\n")
    lu = "mm"   # Default length unit
    rhoCu = PN(str(resistivity) + " ohm*m")  # Resistivity of copper
    PN.dimensions[u.dim("Ω")] = "Ω"
    PN.dimensions[u.dim("Ω*m")] = "nΩ*m"
    # Utility functions
    def Report(R, d, L, rho):
        r = rho*rhoCu
        print('''Results:
    R = {R}
    d = {d}
    L = {L}
    rho = {rho} (relative to copper) = {r}'''.format(**locals()))
    def GetVariable(ignore=""):
        '''Return R, d, L, or rho to indicate the variable of interest.  If
        you wish to ignore one variable, put it into ignore.
        '''
        choices = "R d L rho".split()
        choices.remove(ignore)
        if not choices:
            raise Exception("Bug in program")
        print("Select which variable:")
        i = Choice(choices, indent=" "*3)
        return choices[i]
    def fR(d, L, rho):
        return 4*L*rho/(pi*d**2)
    def fd(R, L, rho):
        return sqrt(4*L*rho/(pi*R))
    def fL(d, R, rho):
        return R*pi*d**2/(4*rho)
    def frho(d, R, L):
        return R*pi*d**2/(4*L)
    def GetLength(msg):
        while True:
            value, unit = GetNumber(msg, low=0, low_open=True,
                                    use_unit=True, default=1)
            try:
                return Length(value, lu if not unit else unit)
            except Exception:
                print("Not a proper length, try again.")
    # For testing, set testing to True
    testing = False
    # Get default length units
    if not testing:
        while True:
            s = input("What is default length unit [{}]? ".format(lu)).strip()
            if not s:
                break
            elif s == "q":
                exit(0)
            else:
                tmp = u.dim(s)
                if tmp is None or tmp != u.dim("m"):
                    print("You must input a length unit")
                    continue
                lu = s
                break
    Length = PN(1, lu)
    Length.low = 0
    Length.low_open = True
    # Choose problem to solve
    if not testing:
        choices = ("R       Resistance",
                   "d       Diameter",
                   "L       Length",
                   "rho     Resistivity")
        while True:
            try:
                print("Select which variable to solve for:")
                i, s = Choice(choices, indent=" "*3)
                break
            except Exception as e:
                print(e)
        print("Solving for", choices[i].split()[0])
        if i == 0:      # Resistance
            ShowResistivities()
            rho = GetNumber("What is resistivity relative to copper? ",
                            low=0, low_open=True, default="1")
            L = Length.get("What is length of wire? ")
            string, value = GetWireDiameter(default_unit=lu)
            d = PN(str(value) + " " + lu)
            R = fR(d, L, rho*rhoCu)
            R.units = "Ω"
        elif i == 1:    # Diameter
            ShowResistivities()
            rho = GetNumber("What is resistivity relative to copper? ",
                            low=0, low_open=True, default="1")
            L = Length.get("What is length of wire? ")
            value, unit = GetNumber("What is resistance in Ω? ", low=0,
                                    low_open=True, use_unit=True)
            R = PN(str(value) + "Ω")
            d = fd(R, L, rho*rhoCu)
            d.units = lu
        elif i == 2:    # Length
            string, value = GetWireDiameter(default_unit=lu)
            d = PN(str(value) + " " + lu)
            value, unit = GetNumber("What is resistance in Ω? ", low=0,
                                    low_open=True, use_unit=True)
            R = PN(str(value) + " " + unit)
            ShowResistivities()
            rho = GetNumber("What is resistivity relative to copper? ",
                            low=0, low_open=True, default="1")
            L = fL(d, R, rho*rhoCu)
            L.units = lu
        elif i == 3:    # Resistivity
            string, value = GetWireDiameter(default_unit=lu)
            d = PN(str(value) + " " + lu)
            value, unit = GetNumber("What is resistance in Ω? ", low=0,
                                    low_open=True, use_unit=True)
            R = PN(str(value) + " " + unit)
            L = Length.get("What is length of wire? ")
            rho = frho(d, R, L)/rhoCu  # Note it's dimensionless
        else:
            raise Exception("Bug in program")
        Report(R, d, L, rho)
        exit(0)
    else:
        rho = resistivity*PN(1, "ohm m")  # Copper resistivity
        # Solve for a 1 m piece of 12 gauge copper wire
        # Resistance
        L = PN("1 m")
        d = PN("2.053 mm")
        R = fR(d, L, rho)
        assert(abs(R - PN("0.005196 Ω")) < PN("0.0001 Ω"))
        # Diameter
        L = PN("1 m")
        R = PN("0.005196 Ω")
        d = fd(R, L, rho)
        assert(abs(d - PN("2.053 mm")) < PN("0.01 mm"))
        # Length
        R = PN("0.005196 Ω")
        d = PN("2.053 mm")
        L = fL(d, R, rho)
        assert(abs(L - PN("1 m")) < PN("0.003 m"))
        # Resistivity
        d = PN("2.053 mm")
        R = PN("0.005196 Ω")
        L = PN("1 m")
        xrho = frho(d, R, L)
        tgtrho = PN("17.2 nΩ m")
        assert(abs(xrho - tgtrho < PN("0.001 nΩ*m")))
        print("Interactive tests passed")
        exit(0)
def MaxCurrentDensity(diameter_m, temperature):
    '''This function returns the maximum allowed current density in A/mm²
    given the wire diameter in m and the temperature in °C.  The
    algorithm is from the resistor.ods Open Office spreadsheet I wrote and
    ultimately comes from a linear regression of a log-log plot of the NEC
    allowed ampacities.  The temperature is the insulation rating of the
    wire and must be 60, 75, or 90 °C.
 
    The code is from an Open Office macro in Basic.
    '''
    slope = -0.820  # Common to each curve
    assert diameter_m > 0
    assert temperature in (60, 75, 90)
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
        if temperature == 60:
            slope = (0.75 - y)/dx
        elif temperature == 75:
            slope = (0.82 - y)/dx
        else:
            slope = (0.87 - y)/dx
        jmax = 10**(y + ld*slope)
    else:
        if temperature == 60:
            b = 1.106  # y-intercept of fitted line
        elif temperature == 75:
            b = 1.203
        else:
            b = 1.264
        jmax = 10**(ld*slope + b)
    # Debug check of jmax
    if jmax > 10**0.93:  # Note:  max y value at ld = 0.41
        msg = ("Internal error:  bad current density: " +
               str(jmax) + " for " + str(temperature) +
               " and diameter in m = " + str(diameter_m))
        raise Exception(msg)
    return jmax
def Size(n):
    if n < 0:
        return {1: "2/0", 2: "3/0", 3: "4/0"}[abs(n)]
    else:
        return str(n)
def GetAmpacityData():
    '''Return a dictionary keyed by AWG size (as a string) with the
    values
        Diameter, inches
        Maximum current for chassis wiring, A
        Maximum current for power transmission, A
        Maximum frequency for 100% skin depth for solid copper, Hz
        Breaking force in lbf for annealed Cu (37 kpsi)
 
    The following data come from
    https://www.powerstream.com/Wire_Size.htm.
        Column 1:  AWG
        Column 2:  Diameter, inches
        Column 3:  Maximum current for chassis wiring, A
        Column 4:  Maximum current for power transmission, A
        Column 5:  Maximum frequency for 100% skin depth for solid copper
        Column 6:  Breaking force in lbf for annealed Cu (37 kpsi)
    '''
    data = '''
    -3,0.46,380,302,125 Hz,6120 lbs
    -2,0.4096,328,239,160 Hz,4860 lbs
    -1,0.3648,283,190,200 Hz,3860 lbs
    0,0.3249,245,150,250 Hz,3060 lbs
    1,0.2893,211,119,325 Hz,2430 lbs
    2,0.2576,181,94,410 Hz,1930 lbs
    3,0.2294,158,75,500 Hz,1530 lbs
    4,0.2043,135,60,650 Hz,1210 lbs
    5,0.1819,118,47,810 Hz,960 lbs
    6,0.162,101,37,1100 Hz,760 lbs
    7,0.1443,89,30,1300 Hz,605 lbs
    8,0.1285,73,24,1650 Hz,480 lbs
    9,0.1144,64,19,2050 Hz,380 lbs
    10,0.1019,55,15,2600 Hz,314 lbs
    11,0.0907,47,12,3200 Hz,249 lbs
    12,0.0808,41,9.3,4150 Hz,197 lbs
    13,0.072,35,7.4,5300 Hz,150 lbs
    14,0.0641,32,5.9,6700 Hz,119 lbs
    15,0.0571,28,4.7,8250 Hz,94 lbs
    16,0.0508,22,3.7,11 kHz,75 lbs
    17,0.0453,19,2.9,13 kHz,59 lbs
    18,0.0403,16,2.3,17 kHz,47 lbs
    19,0.0359,14,1.8,21 kHz,37 lbs
    20,0.032,11,1.5,27 kHz,29 lbs
    21,0.0285,9,1.2,33 kHz,23 lbs
    22,0.0253,7,0.92,42 kHz,18 lbs
    23,0.0226,4.7,0.729,53 kHz,14.5 lbs
    24,0.0201,3.5,0.577,68 kHz,11.5 lbs
    25,0.0179,2.7,0.457,85 kHz,9 lbs
    26,0.0159,2.2,0.361,107 kHz,7.2 lbs
    27,0.0142,1.7,0.288,130 kHz,5.5 lbs
    28,0.0126,1.4,0.226,170 kHz,4.5 lbs
    29,0.0113,1.2,0.182,210 kHz,3.6 lbs
    30,0.01,0.86,0.142,270 kHz,2.75 lbs
    31,0.0089,0.7,0.113,340 kHz,2.25 lbs
    32,0.008,0.53,0.091,430 kHz,1.8 lbs
    33,0.0071,0.43,0.072,540 kHz,1.3 lbs
    34,0.0063,0.33,0.056,690 kHz,1.1 lbs
    35,0.0056,0.27,0.044,870 kHz,0.92 lbs
    36,0.005,0.21,0.035,1100 kHz,0.72 lbs
    37,0.0045,0.17,0.0289,1350 kHz,0.57 lbs
    38,0.004,0.13,0.0228,1750 kHz,0.45 lbs
    39,0.0035,0.11,0.0175,2250 kHz,0.36 lbs
    40,0.0031,0.09,0.0137,2900 kHz,0.29 lbs'''[1:]
    wt = {}
    dbg = False
    if dbg:
        print("Column 1:  AWG")
        print("Column 2:  Diameter, inches")
        print("Column 3:  Maximum current for chassis wiring, A")
        print("Column 4:  Maximum current for power transmission, A")
        print("Column 5:  Maximum frequency in kHz for 100% skin depth for Cu wire")
        print("Column 6:  Breaking force in lbf for annealed Cu (37 kpsi)'''[1:])")
        #print("  AWG Dia, in      Chassis, A       Power, A")
        sig.digits = 2
        sig.rtz = True
    for line in data.split("\n"):
        f = line.split(",")
        awg = f[0].strip()
        dia_in = float(f[1])
        chassis_A = float(f[2])
        pwr_A = float(f[3])
        freq = f[4]
        if " kHz" in freq:
            freq = freq.replace(" kHz", "000")
        else:
            freq = freq.replace(" Hz", "")
        freq = float(freq)/1000
        if freq >= 100:
            freq_kHz = int(freq)
        else:
            freq_kHz = round(freq, 3)
        del freq
        # http://www.nessengr.com/technical-data/skin-depth/ gives the
        # formula for Cu as δ = 0.066/sqrt(f) for δ = skin depth in m
        # and f in Hz.  Then f = 0.00436/δ**2.
        δ = (dia_in*25.4/1000)/2  # Radius is the skin depth
        f_kHz = (0.066/δ)**2/1000
        # Check that calculated and table values are close
        alpha = 0.07
        if not (1 - alpha < freq_kHz/f_kHz < 1 + alpha):
            print(freq_kHz/f_kHz, awg)
            exit()
        # Note the tabulated breaking values aren't quite correct -- use
        # calculated value instead.
        brk = pi*dia_in**2/4*37e3
        if dbg:
            print(f"{int(awg):>4d} {dia_in:7.4f} {sig(chassis_A):>6s} "
                f"{sig(pwr_A):>6s} {sig(f_kHz):>7s} {sig(brk):>8s}")
        else:
            wt[awg] = (dia_in, chassis_A, pwr_A, int(f_kHz*1000), brk)
    return wt
def EquivalentArea(n, m):
    '''Given n ga wire, return how many m ga wires have the equivalent
    area.
    '''
    D, d = [round(AWG(i), 4) for i in (n, m)]     # Diameter in inches
    ratio = flt(D/d)**2
    return D, d, ratio
def SingleWireEquivalents(n):
    if n > 40:
        Error("Size must be <= 40")
    print(f"Number of wires of different sizes to match {n} gauge in area:")
    print(dedent(f'''
                 Num
    AWG         Wires
    ---      -----------
    '''))
    flt(0).n = 2
    flt(0).rtz = flt(0).rtdp = True
    for i in range(0, 41, 2):
        if i == n:
            continue
        D, d, ratio = EquivalentArea(n, i)
        print(f"{i:3d}        {flt(ratio)!s:^6s}")
    exit(0)
def ShowEquivalentAreas(args, d):
    '''args is [n_awg, m_awg].  Print out how many of the smaller size wires
    are needed to equal the area of the larger wire.
    '''
    if len(args) == 1:
        SingleWireEquivalents(int(args[0]))
    n, m = [int(i) for i in args]
    n, m = (n, m) if n < m else (m, n) # Make n the larger AWG size
    D, d, ratio = EquivalentArea(n, m)
    print(dedent(f'''    Larger  = {n} AWG      Diameter = {D} inches
    Smaller = {m} AWG      Diameter = {d} inches
    {ratio} of {m} gauge wires = same area as one {n} gauge wire
    '''))
    exit(0)
def PrintBigTable():
    'This table is for getting big wires from smaller wires'
    N = range(0, 25, 2)
    m = 5
    print(dedent('''
    Number of equivalent wires for equal areas, rounded up
    Row and column headings are AWG sizes
 
    '''))
    # Print row of numbers
    print(" "*m, end="")
    for i in N:
        print(f"{i:^{m}d}", end="")
    print()
    # Print row of hyphens
    print(" "*m, end="")
    for i in N:
        t = " " + "-"*(m - 2) + " "
        print(f"{t:^{m}s}", end="")
    print()
    # Print table
    for i in N:
        print(f"{i:^{m}d}", end="")
        for j in N:
            D, d, ratio = EquivalentArea(i, j)
            if ratio < 1:
                print(f"{' ':{m}s}", end="")
            else:
                r = int(ratio + 0.5)
                print(f"{r:^{m}d}", end="")
        print()
def PrintEquivalenceTable():
    '''Print out a list of gauge sizes with the number of wires of smaller
    sizes that are equivalent in area.
    '''
    N, x, w = 10, flt(0), 12
    x.n = 3
    x.rtz = x.rtdp = True
    print("Areal equivalence of AWG gauge numbers")
    print("    Gauge n is equivalent to:")
    print("  Gauge     Area ratio       Diameter ratio")
    print(" -------    ----------       --------------")
    for i in range(1, 11):
        D, d, A_ratio = EquivalentArea(N, N + i)
        #print(f"    {A_ratio} of (n + {i}) gauge")
        s = f"n + {i}"
        D_ratio = flt(D/d)
        print(f"  {s:^6s}   {A_ratio!s:^{w}s}       {D_ratio!s:^{w}s}")
def NEC():
    '''Return a dictionary containing NEC-allowed currents for copper
    conductors.  The three values are for 60, 75, and 90 °C rated
    insulations.
    '''
    return {
        18: (None, None, 14),
        16: (None, None, 18),
        14: (20, 20, 25),
        12: (25, 25, 30),
        10: (30, 35, 40),
        8: (40, 50, 55),
        6: (55, 65, 75),
        4: (70, 85, 95),
        3: (85, 100, 110),
        2: (95, 115, 130),
        1: (110, 130, 150),
        0: (125, 150, 170),
        -2: (145, 175, 195),
        -3: (165, 200, 225),
        -4: (195, 230, 260),
    }
def Print(*s, **kw):
    '''Normal print except don't emit a newline'''
    print(*s, **kw, end="")
def Strip(s):
    'Strip leading 0 from string in number representation'
    if s[0:2] == "0.":
        return s[1:]
    return s
def f(x):
    'Sig fig string'
    return Strip(fp.sig(x))
def g(x):
    'Cuddled eng string'
    return Strip(fp.engsic(x))
def PrintTable(n, m, step=1, others=[]):
    '''Print the copper wire table from AWG n to m in the indicated
    steps.'''
    print(dedent(f'''{" "*11} Diameter    Res/length    Length/mass  Area      Amps    Freq  Break
     AWG  mils    mm    Ω/ft    Ω/m   ft/lb   m/kg  mm²  Chass  Pwr   kHz   lbf
    ----  ----- ------ ------  -----  -----  ----- ----- ----- ----- ----- -----
    ''')[:-1].replace("!", " "))
    sizes = sorted(set(list(range(n, m, step)) + others))
    for n in sizes:
        PrintLine(n)
def PrintLine(awg):
    fp.digits(3)
    if awg in popular_sizes and isatty and not no_color:
        C.fg(*popular_sizes[awg])
    Print(f"{Size(awg):>4s}  ")
    dia_in = AWG(awg)
    # Diameter
    Print(f"{f(1000*dia_in):5s} ")
    Print(f"{f(dia_in*25.4):>6s}")
    dia_m = dia_in/39.37
    area_m2 = pi*(dia_m/2)**2
    r_ohm_per_m = resistivity/area_m2
    # Resistance/length
    fp.digits(3)
    Print(f"{g(0.3048*r_ohm_per_m):>7s}")
    Print(f"{g(r_ohm_per_m):>7s}")
    m_per_kg = 1/(density*area_m2)
    # Mass/length
    Print(f"{g(1.4881639*m_per_kg):>7s}")
    Print(f"{g(m_per_kg):>7s} ")
    # Area
    Print(f"{g(area_m2*1e6):>5s}")
    # Ampacity data
    fp.digits(2)
    wt = GetAmpacityData()
    if str(awg) in wt:
        dia_in, chassis_A, pwr_A, f_Hz, brk = wt[str(awg)]
        Print(f"{g(chassis_A):>5s} ")
        Print(f"{g(pwr_A):>5s} ")
        Print(f"{g(f_Hz/1000):>5s} ")
        Print(f"{g(brk):>5s}")
    if awg in popular_sizes and isatty and not no_color:
        C.normal()
    print()
def Preece(awg):
    '''Return the current in A at which a copper conductor of AWG size awg
    will fuse.
    '''
    wt = GetAmpacityData()
    dia_in, chassis_A, pwr_A, f_Hz, brk = wt[str(awg)]
    A = pi*dia_in**2/4
    return 12277*A**0.75
def Onderdonk(awg, time_s):
    '''Return the current in A at which a copper conductor of AWG size awg
    will fuse in a time time_s seconds.
    '''
    wt = GetAmpacityData()
    dia_in, chassis_A, pwr_A, f_Hz, brk = wt[str(awg)]
    A = pi*dia_in**2/4  # Area in square inches
    A *= 1.27324e+06    # Convert to circular mils
    return A*sqrt(log10(1053/274 + 1)/(33*time_s))
def PrintAmpacityLine(awg):
    def h(x):
        if x is None:
            return ""
        else:
            return g(x)
    fp.digits(4)
    if awg in popular_sizes and isatty and not no_color:
        C.fg(*popular_sizes[awg])
    Print(f"{Size(awg):>4s}  ")
    dia_in = AWG(awg)
    nec = NEC()
    # Ampacity data
    fp.digits(2)
    wt = GetAmpacityData()
    if str(awg) in wt:
        dia_in, chassis_A, pwr_A, f_Hz, brk = wt[str(awg)]
        dia_m = dia_in/39.37
        area_m2 = pi*dia_m**2/3
        Print(f"{g(chassis_A):>5s} ")
        Print(f"{g(pwr_A):>5s} ")
        # Note we use the NEC-mandated values when the wire size fits
        if int(awg) in nec:
            a60, a75, a90 = nec[int(awg)]
            Print(f"{h(a60):>7s}  ")
            Print(f"{h(a75):>7s}  ")
            Print(f"{h(a90):>7s}  ")
        else:
            if 1:
                for i in range(3):
                    Print(f"{'':>7s}  ")
            else:
                Print(f"{g(1e6*MaxCurrentDensity(dia_m, 60)*area_m2):>7s}  ")
                Print(f"{g(1e6*MaxCurrentDensity(dia_m, 75)*area_m2):>7s}  ")
                Print(f"{g(1e6*MaxCurrentDensity(dia_m, 90)*area_m2):>7s}  ")
        Print(f"{g(Preece(awg)):>7s}")
        Print(f"{g(Onderdonk(awg, 1)):>8s}")
        Print(f"{g(Onderdonk(awg, 0.032)):>8s}")
    if awg in popular_sizes and isatty and not no_color:
        C.normal()
    print()
def AmpacityData():
    print(dedent(f'''
    Ampacity data for copper wire (currents in amperes, ambient temperature
    around normal room temperatures of 20 °C)
     
                        --------- NEC ---------   -------- Fusing -------
                         Insulation rating, °C               Onderdonk     
     AWG  Chass  Pwr      60       75       90    Preece    1 s     32 ms
    ----  ----- -----   -----    -----    -----   ------   -----    -----
    '''[1:]))
    for awg in range(0, 41, 2):
        PrintAmpacityLine(awg)
    print(dedent(f'''
    Chass is the maximum current for a single isolated wire in air.  Pwr uses a
    current density of 2.82 A/mm².  Freq is the AC frequency where the skin
    depth equals the wire's radius.  Use the -H option for more details.'''))
def MIL5088(gauge, ΔT):
    '''Return the allowed current for a wire of size AWG gauge.  The
    temperature differenct ΔT is the wire's rating minus the ambient
    temperature in K.
 
    From MIL-W-5088L dated 10 May 1991.  This is a specification for the
    wiring of aerospace vehicles such as airplanes, helicopters, and
    missles.  The formula is estimated from the graphs on pages 46 and 47.
 
    Since the graphs are log-log and the lines are straight, I used a model 
    of ΔT = b*i**m.  Taking the log of both sides, we get
 
            ln(ΔT) = m*ln(i) + ln(b)
 
    The slope m is estimated from page 46 as 2.09 and as 2.07 on page 47,
    so I'll use 2.08.  The y-intercepts read from the graph at the 100 K
    line in A are
    
        AWG      i0
        4/0     535
        3/0     480
        2/0     400
        0       352
        1       303
        2       260
        4       189
        6       140
        8       103
        10      68
        12      51.8
        14      39.6
        16      28.7
        18      24.6
        20      18.4
        22      14
        24      10.7
        26      8
 
    For a plot y = m*x + b, if a point x0 has a value k, then we can solve
    for b as b = k - m*x0.  Changing things for the ln expressions, we get
 
        ln(b) = ln(ΔT) - m*ln(i0)
        b = exp(ln(ΔT) - m*ln(i0))
 
    It's easier to work with wire diameter than AWG.  Plotting the above
    data as i0 vs wire diameter in mm, the graph is approximated by two
    straight lines (and the plot shows that the MIL spec graphs were
    probably gotten from empirical data).  If d is the diameter in mm of
    the wire, then the two lines are:
 
        ΔT = 27*d             d < 2.6
        ΔT = 51*d - 58        d >= 2.6
    '''
    if not (25 <= ΔT <= 250):
        raise ValueError("ΔT must be between 25 and 250 K")
    if not (-3 <= gauge <= 26):
        raise ValueError("gauge must be between -3 and 26")
    if 0:
        intercept = {
            -3: 535,
            -2: 480,
            -1: 400,
            0: 352,
            1: 303,
            2: 260,
            4: 189,
            6: 140,
            8: 103,
            10: 68,
            12: 51.8,
            14: 39.6,
            16: 28.7,
            18: 24.6,
            20: 18.4,
            22: 14,
            24: 10.7,
            26: 8
        }
        from util import AWG
        for n in intercept:
            mm = round(AWG(n)*25.4, 3)
            print(mm, intercept[n])
        exit()
def PrintVoltageDropTable():
    w, wc = 79, 6
    print(f"{'Voltage Drop Table for Copper Wire':^{w}s}")
    print(f"{'Drop in mV/m for given % of chassis current in A':^{w}s}\n")
    print(f"AWG    Chass ", end="")
    pct = (5, 10, 20, 30, 40, 50, 60, 80, 100)
    for p in pct:
        print(f"{str(p) + '%':^{wc}s} ", end="")
    print()
    print(f"---    ----- ", end="")
    for p in pct:
        print(f"{'-'*(wc - 2):^{wc}s} ", end="")
    print()
    sizes = sorted(set(list(range(0, 41, 2))))
    amp_data = GetAmpacityData()
    x = flt(0)
    x.n = 3
    x.rtz = x.rtdp = True
    for n in sizes:
        item = amp_data[str(n)]
        dia_in, i_chass = item[0:2]
        dia_m = dia_in/39.37
        area_m2 = pi*(dia_m/2)**2
        r_ohm_per_m = flt(resistivity/area_m2)
        if n in popular_sizes and not d["-C"]:
            C.fg(*popular_sizes[n])
        print(f"{n:2d}     ", end="")
        print(f"{flt(i_chass)!s:^5s} ", end="")
        for p in pct:
            i = p/100*i_chass
            V = int(i*r_ohm_per_m*1000)
            print(f"{V:^{wc}d} ", end="")
        if n in popular_sizes and not d["-C"]:
            C.normal()
        print()
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["-a"]:
        AmpacityData()
    elif d["-e"]:
        PrintEquivalenceTable()
    elif d["-t"]:
        PrintBigTable()
    elif d["-v"]:
        PrintVoltageDropTable()
    else:
        if args:
            if args[0] == "a":
                AmpacityData()
                PrintBigTable()
            else:
                ShowEquivalentAreas(args, d)
        elif d["-F"]:
            PrintTable(-3, 57, step=1)
        elif d["-f"]:
            PrintTable(-3, 25, step=1)
        else:
            PrintTable(0, 31, step=2, others=[-3, -2, -1])
# vim: wm=1
