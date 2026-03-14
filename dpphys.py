'''

Routines associated with physical things
        
'''
if 1:  # Header
    if 1:   # Standard imports
        import math
    if 1:   # Custom imports
        import dptypes
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Import symbols
        pass
    if 1:   # Global variables
        g = dptypes.Constant()
        g.dbg = False
if 1:   # Classes
    pass
if 1:   # Functions
    def Height(current_height_inches, age_years, sex):
        '''Returns the predicted adult height in inches of a child.  Unattributed, but
        found in the C code files of Glenn Rhoads' old website
        http://remus.rutgers.edu/~rhoads/Code/code.html, which was defunct in 2010.
        '''
        if not (0 < current_height_inches < 72):
            raise ValueError("current_height_inches must be between 0 and 72")
        if not (0 < age_years < 20):
            raise ValueError("age_years must be between 0 and 20")
        if sex.lower() not in "mf":
            raise ValueError("sex must be 'm' or 'f'")
        a, h = age_years, current_height_inches
        if sex.lower() == "m":
            return h/(((0.00011*a - 0.0032)*a + 0.0604)*a + 0.3796)
        else:
            return h/(((0.00028*a - 0.0071)*a + 0.0926)*a + 0.3524)
    def HeatIndex(air_temp_deg_F, relative_humidity_percent):
        '''From http://www.weather.gov/forecasts/graphical/sectors/idaho.php#tabs.  See also
        http://www.crh.noaa.gov/pub/heat.php.
        
        Heat Index combines the effects of heat and humidity. When heat and humidity combine to reduce
        the amount of evaporation of sweat from the body, outdoor exercise becomes dangerous even for
        those in good shape.
        
        Example:  for 90 deg F and 50% RH, the heat index is 94.6.
        
        The equation used is a multiple regression fit to a complicated set of equations that must be
        solved iteratively.  The uncertainty with a prediction is given at 1.3 deg F.  See
        http://www.srh.noaa.gov/ffc/html/studies/ta_htindx.PDF for details.
        
        If heat index is:
        
            80-90 degF:  Caution:  fatigue possible with prolonged exposure or activity.
            90-105:      Extreme caution:  sunstroke, muscle cramps and/or heat exhaustion possible
                        with prolonged exposure and/or physical activity.
            105-129:     Danger:  sunstroke, muscle cramps and/or heat exhaustion likely.  Heatstroke
                        possible with prolonged exposure and/or physical activity.
            >= 130       Extreme danger:  Heat stroke or sunstroke likely.
        '''
        RH, Tf = relative_humidity_percent, air_temp_deg_F
        HI = (-42.379 + 2.04901523*Tf + 10.14333127*RH - 0.22475541*Tf*RH - 6.83783e-3*Tf*Tf
            - 5.481717e-2*RH*RH + 1.22874e-3*Tf*Tf*RH + 8.5282e-4*Tf*RH*RH - 1.99e-6*Tf*Tf*RH*RH)
        return HI
    def IdealGas(P=0, v=0, T=0, MW=28.9):
        '''Given two of the three variables P, v, and T, calculates the third for the indicated gas.
        The variable that is unknown should have a value of zero.
            P = pressure in Pa
            v = specific volume in m^3/kg
            T = absolute temperature in K
            MW = molecular weight = molar mass in g/mol (defaults to air) Note you can also supply a
                string; if the lower-case version of this string is in the dictionary of
                gas_molar_mass below, the molar mass for that gas will be used.
        The tuple (P, v, T) will be returned.
        
        WARNING:  Note that v is the specific volume, not the volume!
        
        The equation used is P*v = R*T where R is the gas constant for this particular gas.  It is the
        universal gas constant divided by the molecular weight of the gas.
        
        The ideal gas law is an approximation, but a good one for high temperatures and low pressures.
        Here, high and low are relative to the critical temperature and pressure of the gas; these can
        be found in numerous handbooks, such as the CRC Handbook of Chemistry and Physics, the
        Smithsonian Critical Tables, etc.
        
        Some molar masses and critical values for common gases are (Tc is critical temperature, Pc is
        critical pressure (multiply by 1e5 to get Pa), MW is molecular weight):
        
                    Tc, K    Pc, bar    MW, g/mol
            air        133.3     37.69     28.9
            ammonia    405.6    113.14     17.03
            argon      151.0     48.00     39.95
            co2        304.2     73.82     44.0099
            helium       5.2      2.25      4.003
            hydrogen    33.3     12.97      2.01594
            methane    190.6     46.04     16.04298
            nitrogen   126.1     33.94     28.0134
            oxygen     154.6     50.43     31.9988
            propane    369.8     42.49     26.03814
            water      647.3    221.2      18.01534
            xenon      289.8     58.00    131.30
        '''
        gas_molar_mass = {
            "air": 28.9,
            "ammonia": 17.03,
            "argon": 39.95,
            "co2": 44.0099,
            "helium": 4.003,
            "hydrogen": 2.01594,
            "methane": 16.04298,
            "nitrogen": 28.0134,
            "oxygen": 31.9988,
            "propane": 26.03814,
            "water": 18.01534,
            "xenon": 131.30,
        }
        if isinstance(MW, str):
            MW = gas_molar_mass[MW.lower()]
        else:
            assert P >= 0 and v >= 0 and T >= 0 and MW >= 0
        molar_gas_constant = 8.3145  # J/(mol*K)
        R = molar_gas_constant/(float(MW)/1000)  # 1000 converts g to kg
        if sum([i == 0 for i in (P, v, T)]) != 1:
            raise ValueError("One and only one of P, v, T must be zero")
        if not P:
            return R*T/v
        elif not v:
            return R*T/P
        else:
            return P*v/R
    def SpeedOfSound(T):
        '''Returns speed of sound in air in m/s as a function of temperature T in K.  Assumes sea level
        air pressure.
        '''
        assert T > 0
        return 331.4*math.sqrt(T/273.15)
    def WindChillInDegF(wind_speed_in_mph, air_temp_deg_F):
        '''Wind Chill for exposed human skin, expressed as a function of wind speed in miles per hour
        and temperature in degrees Fahrenheit.  http://en.wikipedia.org/wiki/Wind_chill.
        '''
        if wind_speed_in_mph <= 3:
            raise ValueError("Wind speed must be > 3 mph")
        if air_temp_deg_F > 50:
            raise ValueError("Air temperature must be < 50 deg F")
        return (
            35.74
            + 0.6215*air_temp_deg_F
            - 35.75*wind_speed_in_mph**0.16
            + 0.4275*air_temp_deg_F*wind_speed_in_mph**0.16
        )
    def TempConvert(T, in_unit, to_unit):
        '''Convert the temperature in T in the unit specified in in_unit to the unit
        specified by to_unit.
        '''
        allowed, k, r, a, b = "cfkr", 273.15, 459.67, 1.8, 32
        def check(unit, orig):
            if len(unit) != 1 and unit not in allowed:
                raise ValueError(f"{orig!r} is a bad temperature unit")
        inu, tou = [i.lower() for i in (in_unit, to_unit)]
        check(inu, in_unit)
        check(tou, to_unit)
        if inu == tou:
            return T
        d = {
            "cf": lambda T: a*T + b,
            "ck": lambda T: T + k,
            "cr": lambda T: a*(T + k),
            "fc": lambda T: (T - b)/a,
            "fk": lambda T: (T - b)/a + k,
            "fr": lambda T: T + r,
            "kc": lambda T: T - k,
            "kf": lambda T: a*(T - k) + b,
            "kr": lambda T: a*T,
            "rc": lambda T: (T - r - b)/a,
            "rf": lambda T: T - r,
            "rk": lambda T: T/a,
        }
        Tout = d[inu + tou](T)
        e = ValueError("Converted temperature is too low")
        if ((tou in "kr" and Tout < 0) or (tou == "c" and Tout < -k) 
            or (tou == "f" and Tout < -r)):
            raise e
        return Tout

if __name__ == "__main__":  
    if 1:   # Standard imports
        pass
    if 1:   # Custom imports
        import dpmath
        import lwtest
    if 1:   # Import symbols
        run = lwtest.run
        raises = lwtest.raises
        Assert = lwtest.Assert
    def Test_Height():
        Assert(dpmath.AlmostEqual(Height(48, 12, "m"), 57.576, 1e-3))
        Assert(dpmath.AlmostEqual(Height(48, 12, "f"), 51.89, 1e-3))
    def Test_HeatIndex():
        Assert(dpmath.AlmostEqual(HeatIndex(40, 96), 101, 7e-2))
        Assert(dpmath.AlmostEqual(HeatIndex(100, 90), 132, 4e-1))
    def Test_TempConvert():
        k, r = 273.15, 459.67
        Assert(dpmath.AlmostEqual(TempConvert(0, "c", "f"), 32))
        Assert(dpmath.AlmostEqual(TempConvert(0, "c", "k"), k))
        Assert(dpmath.AlmostEqual(TempConvert(0, "c", "r"), 32 + r))
        Assert(dpmath.AlmostEqual(TempConvert(0, "c", "c"), 0))
        Assert(dpmath.AlmostEqual(TempConvert(212, "f", "c"), 100))
        Assert(dpmath.AlmostEqual(TempConvert(212, "f", "f"), 212))
        Assert(dpmath.AlmostEqual(TempConvert(212, "f", "k"), k + 100))
        Assert(dpmath.AlmostEqual(TempConvert(212, "f", "r"), r + 212))
    def Test_IdealGas():
        P, v, T = 0.101325e6, 0, 300
        v = IdealGas(P, v, T)
        Assert(dpmath.AlmostEqual(v, 0.85181, 1e-5))
        P = 0
        P = IdealGas(P, v, T)
        Assert(dpmath.AlmostEqual(P, 0.101325e6))
        T = 0
        T = IdealGas(P, v, T)
        Assert(dpmath.AlmostEqual(T, 300))
    def Test_SpeedOfSound():
        Assert(dpmath.AlmostEqual(SpeedOfSound(273.15), 331.4, 1e-5))
    def Test_WindChillInDegF():
        Assert(dpmath.AlmostEqual(WindChillInDegF(20, 0), -21.9952, 1e-5))
    exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])

def GetGist():
    gist = {}
    gist["gist"] = "Routines associated with physical things"
    gist["copy"] = "Copyright © 2026 Don Peterson"
    gist["lic"] = "MIT License (see /plib/_lic.mit)"
    gist["test"] = "notest"
    gist["cat"] = ""
    gist["todo"] = '''
    '''
    return gist
