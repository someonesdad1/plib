'''
TODO:
    * Line 315 problem in report:  mass m is 1.1586435611491177e-08 kg
      and converted to galh20 is 3.0607267548685616e-09 galh2o.  But the
      line 315 gets an exception on str(var.to(unit)) where unit is
      galh20, but it shouldn't.
    * Use flt to get rid of sig.
    * Getting a number from the user should include the default unit
      string so that dimensions can be checked if the user enters a
      unit.  Example:  when prompted for pressure, enter a volume;
      currently, the program accepts it.

Performs ideal gas law calculations.  Prompts you for input.
    Notation
    --------

    Symbols used (all units internally will be SI):

        P = absolute pressure, Pa
        V = volume, m3
        n = number of moles of a substance, mol
        Vm = molar volume = V/n, m3/mol
        v = Vm = molar volume = V/n, m3/mol
        rho = density, kg/m3
        R = ideal gas constant = 8.3144621(75) J/(K*mol)
        T = absolute temperature, K
        Tc = critical temperature, K
        Pc = critical pressure, Pa
        Z = compressibility factor = Vm/(Vm for ideal gas) = P*Vm/(R*T)

    The critical temperature is the temperature at which it becomes
    impossible to form a liquid, regardless of the pressure (with
    sufficient pressure, it may become a solid).  Heat of vaporization is
    zero at and beyond Tc.

    The critical pressure is the vapor pressure at the critical
    temperature.

    Ideal Gas Law (Clapyron 1834)
    -----------------------------

        P*Vm = R*T

    where

        P = pressure
        Vm = molar volume = V/n
        n = number of moles of material
        R = ideal gas constant = 8.3144621(75) J/(K*mol)
        T = absolute temperature in K

    Simple and useful at high temperatures and lower pressures.  Key
    assumptions of the model are

        * The molecules occupy negligible volume.
        * There is no interaction between the molecules.
        * Collisions between the molecules are completely elastic,
          meaning no energy loss on collision.

    At low pressures (below about 2.7 MPa or 400 psi), most gases
    exhibit nearly ideal behavior.  At higher pressures, the above
    assumptions are no longer true.  Most gases compress more than an
    ideal gas at low pressures and the opposite is true at high
    pressures.

    At modest temperatures but high pressures, the molecules get close
    enough together that intermolecular attractive forces become
    significant.  This causes two things:

        * At low temperatures, the gas can turn into a liquid.
        * At higher temperatures, the gas stays a gas but can behave a
          lot like a fluid (called a supercritical fluid).

    Note the left-hand side of the ideal gas law has units Pa*m3/mol,
    which is an energy per mole of molecules.  The GNU units program
    shows it's 1 J/mol.  Thus, the equation is dimensionally
    consistent.

    The ideal gas law can also be expressed as

        P = rho*(gamma - 1)*e

    where

        gamma = Cp/Cv = ratio of specific heats
        e = Cv*T = internal energy per unit mass
        Cv = specific heat at constant volume
        Cp = specific heat at constant pressure
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
    # Ideal gas law calculations
    #∞what∞#
    #∞test∞# --test #∞test∞#
    pass
if 1:   # Imports
    import sys
    import os
    import getopt
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from get import GetNumber
    from f import flt
    from u import u, to, CT, ParseUnit
    from columnize import Columnize
    from lwtest import run, assert_equal
    if 1:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    # Set Debug to True to bypass prompting
    Debug = False
    R = 8.31432     # J/(mol*K)) ideal gas constant
    T0_K = 273.15   # 0 degC in K
    temperature_units = {
        # The function converts the indicated unit to K.
        "C" : lambda C: flt(C + T0_K),
        "c" : lambda C: flt(C + T0_K),
        "K" : lambda K: flt(K),
        "k" : lambda K: flt(K),
        "F" : lambda F: flt(5*(F - 32)/9 + T0_K),
        "f" : lambda F: flt(5*(F - 32)/9 + T0_K),
        "R" : lambda R: flt(5/9*R),
        "r" : lambda R: flt(5/9*R),
    }
    # Table of gas critical temperatures and pressures, page F-90, CRC Handbook
    # of Chemistry and Physics, 59th ed., 1978.
    #       Gas name
    #       Critical pressure in atm
    #       Critical temperature in degrees C
    #       Molecular weight in g/mol
    #       omega (acentric factor, dimensionless)
    # Except for air, molecular weights taken from MRC Periodic Table.
    #
    # Acentricity values from various locations on the web.
    #
    # Another table of critical values:
    # http://my.safaribooksonline.com/book/chemical-engineering/9780132441902/conversion-factors-and-constants/app10lev1sec3
    #
    # Molecular weights in g/mol
    H = flt(1.00797)
    C = flt(12.0111)
    O = flt(15.9994)
    N = flt(14.0067)
    Cl = flt(35.453)
    F = flt(18.9984)
    S = flt(32.064)
    Ar = flt(39.948)
    He = flt(4.0026)
    Ne = flt(20.183)
    Xe = flt(131.30)
    Kr = flt(83.80)
    #
    constants = [
        # Pc = critical pressure, atm
        # Tc = critical temperature, °C
        # MW = molecular weight, g/mol
        # w = acentric factor (mostly from wikipedia page)
        #                            Pc       Tc       MW            w
        ["Air",                     37.2,   -140,     28.9,          0],
        ["Acetylene (C2H2)",        61.6,     35.5,   2*C+2*H,       0.187],
        ["Ammonia (NH3)",          112.5,    132.5,   N+3*H,         0.252],
        ["Argon (Ar)",              48,     -122.3,   Ar,            0],
        ["Carbon dioxide (CO2)",    72.9,     31,     C+2*O,         0.228],
        ["Carbon monoxide (CO)",    34.5,   -140,     C+O,           0],
        ["Chlorine (Cl2)",          76.1,    144,     2*Cl,          0],
        ["Ethane (C2H6)",           48.2,     32.2,   2*C+6*H,       0.008],
        ["Fluorine (F2)",           55,     -129,     2*F,           0],
        ["Freon (CCl2F2)",          39.6,    111.5,   C+2*Cl+2*F,    0],
        ["Helium (He)",              2.26,  -267.9,   He,           -0.390],
        ["Hydrogen (H2)",           12.8,   -239.9,   2*H,          -0.22],
        ["Hydrogen cyanide (HCN)",  48.9,    183.5,   H+C+N,         0],
        ["Hydrogen sulfide (H2S)",  48.9,    183.5,   2*H+S,         0],
        ["Iodine (I2)",            116,      512,     2*126.904,     0],
        ["Isopr. alcohol (C3H8O)",  47,      235,     3*C+8*H+O,     0],
        ["Krypton (Kr)",            54.3,    -63.8,   Kr,            0],
        ["Methane (CH4)",           45.8,    -82.1,   C+4*H,         0.008],
        ["Neon (Ne)",               26.9,   -228.7,   Ne,            0],
        ["Nitrogen (N2)",           33.5,   -147,     2*N,           0.04],
        ["Oxygen (O2)",             50.1,   -118.4,   2*O,           0.022],
        ["Ozone (O3)",              67,       -5.16,  3*O,           0],
        ["Propane (C2H2)",          42,       96.8,   2*C+2*H,       0.008],
        ["Sulfur dioxide (SO2)",    77.7,    157.8,   S+2*O,         0],
        ["Toluene (C7H8)",          41.6,    320.8,   7*C+8*H,       0],
        ["Water (H2O)",            218.3,    374.1,   2*H+O,         0],
        ["Xenon (Kr)",              58,       16.6,   Xe,            0],
    ]
    del H, C, O, N, Cl, F, S, Ar, He, Ne, Xe, Kr
    # Convert critical temperature & pressure to SI units
    for i in range(len(constants)):
        c = constants[i]        # Change to flt with units
        c[1] = flt(c[1], units="atm")
        c[2] = flt(c[2])        # Degrees C, but no units for ease later
        c[3] = flt(c[3], units="g/mol")
        c[4] = flt(c[4])
        constants[i] = tuple(constants[i]) 
    constants = tuple(constants)
def ParseCommandLine(d):
    d["-d"] = 4         # Number of digits in report
    d["-t"] = False     # Run tests
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "d:ht", "test")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for o, a in optlist:
        if o == "-d":
            try:
                d["-d"] = int(a)
            except Exception:
                print("Bad input for -d option")
                exit(1)
            if not (1 <= d["-d"] <= 15):
                print("-d:  Number of digits must be between 1 and 15",
                      stream=sys.stderr)
                exit(1)
        elif o == "-h":
            Help(d)
            exit(0)
        elif o == "-t" or o == "--test":
            d["-t"] = not d["-t"]
    flt(0).n = d["-d"]
    return args
def Help(d):
    print(dedent(f'''
    Usage:  {sys.argv[0]}
      This script will calculate the properties of a gas using the ideal gas law.
      This law is a good approximation for pressures less than about 2.7 MPa (400
      psi) and higher temperatures; the basic physical assumption is that the
      molecules are sufficiently far apart that interaction effects are
      insignificant.
  
      You will be prompted for four variables:
  
          P   Pressure
          V   Volume
          m   Mass
          T   Temperature
  
      You should be able to use most common unit names, so use what you're
      accustomed to.  If you don't type in a unit string after the number, it
      will be given an SI unit (Pa for pressure, m3 for volume, kg for mass, and
      K for temperature).
  
      A report is printed in which the state variables are given in a variety of
      units.  While a purist would probably just want to stick with SI base units
      and those derived from them, practical problems often require seeing things
      in other units.  It's easy to change the output unit set -- just edit the
      appropriate string in the function PrintResults().
  
      The critical temperature is given as Tc.  This is the temperature above
      which it is impossible to form a liquid, regardless of the pressure (but it
      may become a solid).  The critical pressure Pc is the vapor pressure at the
      critical temperature.
  
      Options
        -d n      Set output number of significant figures [{d['-d']}]
        -h        Show this help
        -t        Run self tests
        --test    Run self tests
    '''))
def GetValue(name, entered, is_temperature=False):
    '''name contains the name of the parameter we're after.  Return
    the SI equivalent of the number the user entered.  entered is a
    dictionary that will contain the user's entered value and units.
    '''
    while True:
        num, unit = GetNumber(name + "? ", low=0, high=sys.float_info.max,
                              default=0, use_unit=True, allow_quit=True)
        entered[name] = (num, unit)
        try:
            if is_temperature:
                # The entry is a function to convert to K
                if not unit:
                    unit = "K"
                if unit not in temperature_units:
                    raise ValueError()
                f = temperature_units[unit]
                T_K = f(num)
                if T_K < 0:
                    print("Temperature must be >= 0")
                    continue
                return T_K
            else:
                return num*u(unit)
        except ValueError:
            print("Number and/or unit entered not recognized; try again.\n")
def PrintResults(d, indent=""):
    '''P is pressure in Pa, V is volume in m3, m is mass in kg, n is
    number of moles, T is temperature in K, gas_id is the string
    identifying the gas, and entered is the dictionary containing the
    user's entered values.  d is the options dictionary.
    '''
    P = flt(d["P"], units="Pa")
    V = flt(d["V"], units="m3")
    n = flt(d["n"])
    m = flt(d["m"], units="kg")
    T = flt(d["T"], units="K")
    OutputVariable(P, "Pressure:", "kPa atm psi mmHg")
    OutputVariable(V, "Volume:", "m3 liter cc gal ft3")
    OutputVariable(m, f"Mass ({n} moles):", "kg lbm galwater oz")
    OutputVariable(m/V, "Density:", "kg/m3 g/cc lb/inch3 lb/ft3")
    OutputTemperature(T)
def OutputVariable(var, label, units, indent=" "*4):
    s = []
    print()
    print(label)
    for unit in units.split():
        s.append(indent + str(var.to(unit))) # + " " + unit)
    for i in Columnize(s, sep=" "):
        print(i)
def OutputTemperature(T_K, indent=" "*4):
    '''Have to handle temperature specially.
    '''
    ip = flt("273.15 K")     # Ice point temperature in K
    with ip:
        ip.promote = True
        s = []
        print()
        print("Temperature:")
        s.append(indent + str(T_K.val) + " K")
        s.append(indent + str(flt((T_K - ip).val)) + " °C")
        degF = 9/5*(T_K - ip) + 32
        s.append(indent + str(flt(degF.val)) + " °F")
        s.append(indent + str((9/5*T_K).val) + " °R")
    for i in Columnize(s, sep=" "):
        print(i.rstrip(" ="))
def EOS_IdealGas(d):
    P = d["P"]
    V = d["V"]
    n = d["n"]
    m = d["m"]
    T = d["T"]
    name, pc, tc, mw, w = constants[d["gas_id"]]
    if not P:
        d["P"] = n*R*T/V
    elif not V:
        d["V"] = n*R*T/P
    elif not n:
        d["n"] = P*V/(R*T)
        d["m"] = d["n"]*mw/1000  # Convert moles to kg
    elif not T:
        d["T"] = P*V/(R*n)
    else:
        print("Need at least one variable to be zero")
        exit(1)
def PrintHeader(d):
    P = d["P"]
    V = d["V"]
    n = d["n"]
    m = d["m"]
    T = d["T"]
    name, pc, tc, mw, w = constants[d["gas_id"]]
    width = int(os.environ.get("COLUMNS", 79)) - 1
    s, f = f"Results for {name} (MW = {mw} g/mol)", "{0:^{1}}"
    print(f.format(s, width))
    print(f.format("-"*len(s), width))
    print("Ideal gas EOS")
    print("Critical values:")
    # Note that tc was set without units, but it's in °C
    print("    Tc = %s °C   = %s K   = %s °F   = %s °R" % (
        str(CT(tc, "C", "C")),
        str(CT(tc, "C", "K")),
        str(CT(tc, "C", "F")),
        str(CT(tc, "C", "R"))))
    print("    Pc = %s   = %s   = %s " % (
        pc.to("atm"),
        pc.to("MPa"),
        pc.to("psi")))
def GetRequirements(d):
    gas_id = 1
    print(dedent(f'''
                        Ideal Gas Law Calculation
                        -------------------------
    Enter zero for the variable you don't know.  Default units are SI if you
    don't enter a unit string (commonly-used units are supported; for
    example, cubic feet are represented by ft3).

    '''))
    # Print gas selections
    gases = []
    entered = {    # Keep track of what user enters
        # (value, unit)
        "Pressure"    : (0, ""),
        "Volume"      : (0, ""),
        "Mass"        : (0, ""),
        "Temperature" : (0, ""),
    }
    if not d["-t"]:
        # Show gases
        while True:
            for i in range(len(constants)):
                gases.append("%2d %s" % (i+1, constants[i][0]))
            for i in Columnize(gases, col_width=26, columns=3,
                                   trunc=1):
                print(i)
            msg = "\nGas type" % locals()
            gas_id = GetNumber(msg, numtype=int, default=1, low=1,
                               high=len(gases))
            gas_id -= 1  # Correct for zero-based list
            try:
                Pc = constants[gas_id][1]*u("MPa")
                Tc = constants[gas_id][2]
                mw = constants[gas_id][3]
                break
            except IndexError:
                print("Bad number -- try again")
        # Get user's input
        while True:
            P = GetValue("Pressure", entered)
            V = GetValue("Volume", entered)
            m = GetValue("Mass", entered)
            # The factor of 1000 is because m is in kg and we need it
            # in g.
            n = 1000*m/mw    # Convert mass to moles
            T = GetValue("Temperature (default units are K)", entered, is_temperature=True)
            # Check that we only have one zero variable
            f = lambda a, b: not a and not b
            if f(P, V) or f(P, n) or f(P, T) or f(V, n) or f(V, T) or f(n, T):
                print("Must have only one zero variable\nStart over...\n")
            else:
                break
        def f(s):
            v, u = entered[s]
            return str(v) + " " + u if u else str(v)
        print("\nYou entered:")
        print("  P =", f("Pressure"), "=", str(P), "Pa")
        print("  V =", f("Volume"), "=", str(V), "m3")
        print("  m =", f("Mass"), "=", str(m), "kg")
        print("  T =", f("Temperature"), "=", str(T), "K")
        print()
    d.update({"P": P, "V": V, "n": n, "m": m, "T": T, "gas_id": gas_id})
    d["entered"] = entered
if 1:   # Unit tests
    def TestGetTemperature():
        # Hydrogen at 1 atm, 1 mol, 1 kg
        gas_id = 11
        P = 1*u("atm")      # Pa
        V = 1               # Cubic meters
        n = 1               # moles
        mw = 2*1.00797      # MW of H2
        T = expected_T = P*V/(R*n)
        m = P*V/(R*T)*mw/1000
        d = {"P": P, "V": V, "n": n, "m": m, "T": 0, "gas_id": gas_id}
        EOS_IdealGas(d)
        assert_equal(d["T"], expected_T)
    def TestGetMass():
        # Total mass of air in house on Shamrock:  901.9 m3
        gas_id = 0          # Air
        P = 1*u("atm")      # Pa
        V = 901.9           # Cubic meters
        n = 0               # moles
        T = 293.15          # About room temperature
        name, pc, tc, mw, w = constants[gas_id]
        n = P*V/(R*T)
        expected_m = n*mw/1000  # kg
        d = {"P": P, "V": V, "n": 0, "m": 0, "T": T, "gas_id": gas_id}
        EOS_IdealGas(d)
        assert_equal(d["m"], expected_m)
        # Mass of air in 20 gallon air compressor at 100 psi
        gas_id = 0          # Air
        P = 100*u("psi")    # Pa
        V = 20*u("gal")     # Cubic meters
        n = 0               # moles
        T = 293.15          # About room temperature
        name, pc, tc, mw, w = constants[gas_id]
        n = P*V/(R*T)
        expected_m = n*mw/1000  # kg
        d = {"P": P, "V": V, "n": 0, "m": 0, "T": T, "gas_id": gas_id}
        EOS_IdealGas(d)
        assert(abs(d["m"] == expected_m))
    def TestGetPressure():
        # 1 mole of Hydrogen at 300 K in 1 m3
        gas_id = 11
        V = 1               # Cubic meters
        n = 1               # moles
        T = 300             # K
        P = expected_P = n*R*T/V
        name, pc, tc, mw, w = constants[gas_id]
        m = n*mw/1000       # kg
        d = {"P": 0, "V": V, "n": n, "m": m, "T": T, "gas_id": gas_id}
        EOS_IdealGas(d)
        assert_equal(d["P"], expected_P)
    def TestGetVolume():
        # 1 mole of Hydrogen at 300 K and 2500 Pa
        gas_id = 11
        P = 2500            # Pa
        n = 1               # moles
        T = 300             # K
        V = expected_V = n*R*T/P
        name, pc, tc, mw, w = constants[gas_id]
        m = n*mw/1000       # kg
        d = {"P": P, "V": 0, "n": n, "m": m, "T": T, "gas_id": gas_id}
        EOS_IdealGas(d)
        assert_equal(d["V"], expected_V)
if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if d["-t"]:
        run(globals())
    else:
        if 0:
            # Use for testing report format.  Should get room
            # temperature (293 K) for T.
            d["gas_id"] = 0  # Air
            d["P"] = 1*u("atm")
            d["V"] = 901.9  # m3
            d["m"] = 1083.5482834484887
            d["T"] = 0
            name, pc, tc, mw, w = constants[0]
            d["n"] = d["m"]*1000/mw
            print("\n*** T should be room temperature ***\n")
        else:
            GetRequirements(d)
        EOS_IdealGas(d)
        PrintHeader(d)
        PrintResults(d, "  ")
