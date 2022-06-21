'''
Print tables for the pressure drop and velocity through standard US pipe
sizes for PVC and steel pipes.

Quick validation 21 Jun 2022
    Table at https://www.irrigationtutorials.com/pipe-and-tube-pressure-loss-tables/
    gives 1.06 psi pressure drop per 100 ft of 1" sch. 40 PVC at 6 gpm.
    This script gives 2.73 psi/100 m for 0.7 m/s velocity.  Linear
    interpolation in the web page's data gives agreement to < 1%.

    https://www.engineeringtoolbox.com/pressure-loss-steel-pipes-d_307.html
    for 1 m/s nom in 1 inch sch 40 steel pipe gives about 58 kPa per 100 m;
    this script gives around 54-66, depending on cleanliness of pipe.

'''
if 1:  # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2016 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Print pressure drop and velocity tables for fluid flow through
        # standard US pipe sizes for PVC and steel pipes.
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard imports
        import getopt
        import os
        import sys
        from fractions import Fraction
        import bisect
        import math
    # Custom imports
        from wrap import dedent
        from u import u
        from f import flt
        use_sig = False
        if use_sig:
            from sig import sig
        from water import FrictionFactor, WaterDensity, WaterDynamicViscosity
        from water import GetQuantity
    # Global variables
        # Allowed fluid velocities in m/s
        velocities = [flt(round(flt(x), 3)) for x in '''
            .1 .2 .3 .4 .5 .6 .7 .8 .9 1 1.1 1.2 1.3 1.4 1.5 1.6 1.8 2 2.2 2.4
            2.6 2.8 3 3.2 3.4 3.6 3.8 4 4.5 5 5.5 6 7 8 9 10
            '''.replace("\n", " ").split()]
        # These are the allowed US pipe sizes
        US_pipe_sizes = '''
            1/8 1/4 3/8 1/2 3/4 1 1-1/4 1-1/2 2 2-1/2 3 3-1/2 4 5 6 8 10 12 14
            16 18 20 24'''.replace("\n", " ").split()
        # Inside diameters are in mils
        ID_steel_sch_40 = {
            "1/8": 269,
            "1/4": 364,
            "3/8": 493,
            "1/2": 622,
            "3/4": 824,
            "1": 1049,
            "1-1/4": 1380,
            "1-1/2": 1610,
            "2": 2067,
            "2-1/2": 2469,
            "3": 3068,
            "3-1/2": 3548,
            "4": 4026,
            "5": 5047,
            "6": 6065,
            "8": 7981,
            "10": 10020,
            "12": 11940,
            "14": 13120,
            "16": 15000,
            "18": 16880,
            "20": 18820,
            "24": 22620,
        }
if 1:   # Utility
    def InterpretFraction(s):
        '''Interprets the string s as a fraction.  The following are
        equivalent forms:  '5/4', '1 1/4', '1-1/4', or '1+1/4'.  The
        fractional part in a proper fraction can be improper:  thus,
        '1 5/4' is returned as Fraction(9, 4).
        '''
        if "/" not in s:
            if "." in s or "e" in s.lower():
                m = "'{}' must contain '/' or be an integer"
                raise ValueError(m.format(s))
            return Fraction(s)
        t = s.strip()
        # First, try to convert the string to a Fraction object
        try:
            return Fraction(t)
        except ValueError:
            pass
        # Assume it's of the form 'i[ +-]n/d' where i, n, d are
        # integers.
        msg = "'%s' is not of the correct form" % s
        neg = True if t[0] == "-" else False
        fields = t.replace("+", " ").replace("-", " ").strip().split()
        if len(fields) != 2:
            raise ValueError(msg)
        try:
            ip = abs(int(fields[0]))
            fp = abs(Fraction(fields[1]))
            return -(ip + fp) if neg else ip + fp
        except ValueError:
            raise ValueError(msg)
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        name = sys.argv[0]
        degC = d["-t"]
        punit = d["-p"]
        l = d["-l"]
        print(dedent(f'''
        Usage:  {name} [options] size
        Prints a table of pressure loss due to friction for a pipe full of
        fluid (defaults to water) flowing at the indicated velocity.  The pipe
        size is the conventional inch-sized US pipe size such as 3/4, 1,
        1-1/4, etc.  If size does not designate a US inch-sized pipe, then the
        size is interpreted in inches unless a unit is given.
        
        You can include commonly-used units with numbers; for example, specify
        the pipe length as 100 feet by -l '100 ft'.
        
        The output columns are for the following roughnesses in um:
            PVC (plastic, brass, copper, glass, etc.)       5
            Steel                                          45
            Galvanized steel                              150
            Corroded steel                               1000
        Examples:
            {name} 1
                prints data for US 1 inch pipe (1.049 inches ID)
            {name} 1 inch
                prints data for a pipe with 1 inch ID
        Options:
          -d d  Specify the fluid's density (default units are kg/m3).  Must
                be used with -v option.
          -f    Show a larger range of fluid velocities (the default is the most
                common design range).
          -i    size is the pipe inside diameter in inches (i.e., don't interpret
                in terms of standard US pipe sizes).
          -l l  Specify the length of the pipe to calculate the pressure 
                drop.  [Default = {l}]
          -m    size is the pipe inside diameter in mm
          -n n  Number of significant figures
          -p p  Specify the pressure unit to use for output.  The default
                is {punit}.
          -t C  Water temperature in degrees C. [Default = {degC}]
          -v v  Specify the fluid's viscosity (default units are Pa*s).  Must
                  be used with -d option.
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = None      # Fluid density in kg/m3
        d["-F"] = False     # Show double velocity range
        d["-f"] = False     # Show full velocity range
        d["-i"] = False     # Interpret arg[0] as ID in inches
        d["-l"] = "100 m"   # Length of pipe
        d["-m"] = False     # Metric size
        d["-n"] = 2         # Number of significant figures
        d["-p"] = "kPa"     # Pressure units
        d["-s"] = False     # Limit velocities
        # Note:  the following temperature for water was chosen as it is the
        # measured temperature of the water from my home's faucets.
        d["-t"] = flt(13)   # Water temperature in degrees C
        d["-v"] = None      # Fluid dynamic viscosity in Pa*m
        d["special"] = False    # Flags special density & viscosity
        if len(sys.argv) < 2:
            Usage(d)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:Ffil:mn:p:t:v:")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in "Ffims":
                d[o] = not d[o]
            if o in ("-d",):
                try:
                    err = "'{}' isn't a valid density"
                    d["-d"] = GetQuantity(a, err, dim=u.dim("kg/m3"))
                    d["special"] = True
                except Exception as e:
                    Error(str(e))
            elif o in ("-l",):
                d["-l"] = a
            elif o in ("-p",):
                d["-p"] = a
            elif o in ("-n",):
                try:
                    d["-n"] = int(a)
                except Exception:
                    Error(f"'{a}' is not a valid integer")
                if not (1 <= d["-n"] <= 15):
                    Error("-n option must be between 1 and 15")
            elif o in ("-t",):
                try:
                    d["-t"] = flt(a)
                except Exception:
                    Error(f"'{a}' is not a valid temperature in deg C")
                if not (0 <= d["-t"] <= 100):
                    Error("Temperature must be between 0 and 100 deg C")
            if o in ("-v",):
                try:
                    err = "'{}' isn't a valid dynamic viscosity"
                    d["-v"] = GetQuantity(a, err, dim=u.dim("Pa*s"))
                    d["special"] = True
                except Exception as e:
                    Error(str(e))
        if ((d["-d"] is not None and d["-v"] is None) or
            (d["-d"] is None and d["-v"] is not None)):
            Error("Both -d and -v must be used together")
        if d["-d"] is None:
            d["-d"] = flt(WaterDensity(d["-t"]))
        if d["-v"] is None:
            d["-v"] = flt(WaterDynamicViscosity(d["-t"]))
        SetFluidVelocities(d)
        if len(args) < 1:
            Usage(d)
        return ' '.join(args)
if 1:   # Core functionality
    def GetDiameter(dia, d):
        '''Return the pipe inside diameter in m.  
        '''
        if dia in US_pipe_sizes:
            return flt(ID_steel_sch_40[dia]/1000*0.0254)
        else:
            # The default unit is inches; see if we can convert to a flt.
            try:
                d = flt(dia)
                return d*u("inches")
            except ValueError:
                return flt(GetQuantity(dia, dim="m"))
    def SetFluidVelocities(d):
        '''The normal range of fluid velocities for practical problems is
        about 0.5 to 3 m/s.  Using the -f option extends this to 0.1 to 10
        m/s.  The -F option extends the high end, but is beyond the usual
        conditions encountered in practical plumbing problems.
        '''
        global velocities
        if d["-f"]:     # Full range of velocities
            return
        elif d["-F"]:
            pred = lambda x: 10 < x <= 100
            velocities += list(filter(pred, [round(100*i, 1) for i in velocities]))
        else:
            pred = lambda x: 0.1 <= x <= 3
            velocities = list(filter(pred, velocities))
    def PrintTable(diameter_m, d):
        A = flt(math.pi*diameter_m**2/4)
        g = flt(9.80665)        # Standard acceleration of gravity in m/s2
        rho, mu, l = d["-d"], d["-v"], d["-l"]
        L = GetQuantity(l)
        pressure_unit = d["-p"]
        print(dedent(f'''
                 Volumetric     Mass         Pressure drop, {pressure_unit}/{l}
         Vel       flow         flow               --------- Steel ----------
         m/s     L/s    gpm     kg/s      PVC      Clean     Galv.   Corroded
        ------  -----  ------   -----    -----     -----     -----   --------
        '''))
        for v in velocities:
            D, Q = flt(diameter_m), flt(A*v)
            Re = flt(rho*v*diameter_m/mu)       # Reynolds number
            if use_sig:
                v_mps = sig(v)
                Q_Lps = sig(A*v/u("L/s"))
                Q_gpm = sig(A*v/u("gpm"))
                m_kgps = sig(A*v*rho)
            else:
                v_mps = str(v)
                Q_Lps = str(A*v/u("L/s"))
                Q_gpm = str(A*v/u("gpm"))
                m_kgps = str(A*v*rho)
            n = 7
            print(f"{v_mps:^6s} {Q_Lps:^{n}s} {Q_gpm:^{n}s} {m_kgps:^{n}s}", end="")
            f_pvc = FrictionFactor(D, Re, 5*u("um"))          # PVC 
            f_steel = FrictionFactor(D, Re, 45*u("um"))
            f_galv = FrictionFactor(D, Re, 150*u("um"))       # Galvanized steel
            f_corroded = FrictionFactor(D, Re, 1000*u("um"))  # Corroded steel
            # Calculate pressure loss in Pa per 100 m of length
            digits = 2      # Two significant figures reflect the uncertainties
            dp = flt(0.5*(L/D)*rho*v**2)
            if use_sig:
                dp_pvc = sig(f_pvc*dp/u(pressure_unit), digits)
                dp_steel = sig(f_steel*dp/u(pressure_unit), digits)
                dp_galv = sig(f_galv*dp/u(pressure_unit), digits)
                dp_corroded = sig(f_corroded*dp/u(pressure_unit), digits)
            else:
                dp_pvc = str(f_pvc*dp/u(pressure_unit))
                dp_steel = str(f_steel*dp/u(pressure_unit))
                dp_galv = str(f_galv*dp/u(pressure_unit))
                dp_corroded = str(f_corroded*dp/u(pressure_unit))
            n = 7
            print(f"  {dp_pvc:^{n}s}   {dp_steel:^{n}s}   {dp_galv:^{n}s}   "
                  f"{dp_corroded:^{n}s}")
        print(dedent('''
        Conversions:
          m/s = 3.28 ft/s       kg/s = 2.20 lbm/s       kPa = 0.145 psi
          1 m water = 9.81 kPa = 1.42 psi   1 ft water = 0.434 psi = 2.99 kPa'''))
if __name__ == "__main__":
    d = {}      # Options dictionary
    dia = ParseCommandLine(d)
    if use_sig:
        sig.rtz = sig.rlz = sig.rdp = True
        sig.low = 1e-3
    else:
        x = flt(0)
        x.n = d["-n"]
        x.rtz = x.rtdp = True
    diameter_m = flt(GetDiameter(dia, d))
    title = "Friction pressure drops for"
    if dia in US_pipe_sizes:
        print("{} {} inch US pipe ({:.3f} inches ID)".format(
            title, dia, ID_steel_sch_40[dia]/1000))
    else:
        print("{} {} ID pipe".format(title, dia))
    name = "Fluid"
    if not d["special"]:
        if use_sig:
            print("Water at {} deg C = {} deg F".format(sig(d["-t"]),
                sig(d["-t"]*1.8 + 32)))
        else:
            print(f"Water at {d['-t']} deg C = {d['-t']*1.8 + 32} deg F")
        name = " "
    if use_sig:
        print("{} density = {} kg/m3, dynamic viscosity = {} mPa*s\n".format(
            name, sig(d["-d"], 6), sig(1000*d["-v"], 4)))
    else:
        print(f"{name} density = {d['-d']} kg/m3, dynamic viscosity = {1000*d['-v']} mPa*s\n")
    PrintTable(diameter_m, d)
