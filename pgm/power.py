'''
Print out the cost of electrical power.
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
    # Program description string
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    from math import *
    import getopt
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from f import flt
    from fpformat import FPFormat
    from columnize import Columnize
    from u import u, ParseUnit
if 1:   # Global variables
    ii = isinstance
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] power_in_W [unit]
      Prints out various period costs of electrical power (for the rate of
      {100*flt(d["-r"])}¢/(kW*hr) for a given power in watts.  You can append an optional
      power unit such as W, hp, metric_hp, tonref, and tonrefrigeration.
      power_in_W can be an expression that will be evaluated (the math module's
      symbols are in scope).
    Example:
        {sys.argv[0]} 300*cos(49*pi/180) metric_hp
      prints out a table for a power of an apparent power of 300 metric
      horsepower at a power factor angle of 49 degrees (power factor is 0.65).
    Options:
      -d n      Set the number of significant figures in the output [{d["-d"]}]
      -l        Print typical lighting power table
      -r C      Change the cost per kW*hr to C dollars
      -t        Print the consumption of various instruments
    '''))
    exit(status)
def ParseCommandLine(d):
    x = flt(0)
    d["-r"] = "0.065"   # Cost of kW*hr of electrical energy in $
    d["-d"] = 2         # Number of significant digits
    d["-l"] = False     # Print out lighting power too
    d["-t"] = False     # Instrument consumption
    x.n = d["-d"]
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:hlr:t")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in "lt":
            d[o] = not d[o]
        if o in ("-r",):
            try:
                d["-r"] = float(a)
                if d["-r"] <= 0:
                    raise Exception()
            except Exception:
                msg = "-r option's argument must be a number > 0"
                Error(msg)
        elif o in ("-d",):
            try:
                d["-d"] = int(a)
                if not (1 <= d["-d"] <= 15):
                    raise ValueError()
            except ValueError:
                msg = "-d argument must be an integer between 1 and 15"
                Error(msg)
        elif o in ("-h", "--help"):
            Usage(d, status=0)
    x.n = d["-d"]
    if d["-t"]:
        Instruments()
        exit(0)
    if d["-l"]:
        Lighting()
        exit(0)
    if not args:
        Usage(d)
    return args
def F(x):
    'For flt x, if str has trailing decimal point, remove it'
    assert(ii(x, flt))
    s = str(x)
    if s[-1] == ".":
        s = s[:-1]
    return s
def Money(amount, time_period):
    '''Print in dollars if the amount is greater than 1; in cents if
    less than 1.
    '''
    i, t = " "*4, time_period
    a = amount if amount >= 1 else 100*amount
    return f"{i}${F(a)} per {t}" if amount >= 1 else f"{i}{F(a)}¢ per {t}"
def Lighting():
        # Table from https://en.wikipedia.org/wiki/Lumen_%28unit%29
        # Accessed 25 Jan 2017.
        print(dedent('''
                    Lighting electrical power consumption, W
                 120 V
        lumens   incand.     CFL         LED 
          200      25 W       3-5 W        3 W
          450      40 W      9-11 W      5-8 W
          800      60 W     13-15 W     9-12 W
         1100      75 W     18-20 W    13-16 W
         1600     100 W     24-28 W    18-22 W
         2400     150 W     30-52 W       30 W
         3100     200 W     49-75 W       32 W
         4000     300 W    75-100 W     40.5 W
        '''))
def Power(power_expr):
    # Times in seconds
    hour = flt(3600)
    eight_hour_day = flt(8*hour)
    day = hour*24
    week = 7*day
    month = flt(365.25/12*day)
    year = flt(365.25*day)
    # Get power and unit
    unit = "W"
    val, un = ParseUnit(power_expr, allow_expr=True)
    if un:
        unit = un
    power_W = flt(eval(val)*u(unit))
    dollar_per_kW_hr = flt(d["-r"])
    dollar_per_joule = dollar_per_kW_hr/3.6e6
    kW_per_hp = flt(745.7)
    hp = str(power_W/kW_per_hp)
    if un:
        s = "A power of {} ({} W, {} hp)".format(power_expr, str(power_W), hp)
    else:
        pwr = "{} W".format(power_expr)
        s = "A power of {} ({} hp)".format(pwr, hp)
    print("{} costs (at {:.1f} ¢ per kW*hr):".format(s,
          dollar_per_kW_hr*100))
    print(Money(power_W*dollar_per_joule*hour, "hour"))
    print(Money(power_W*dollar_per_joule*eight_hour_day, "8 hour day"))
    print(Money(power_W*dollar_per_joule*day, "day"))
    print(Money(power_W*dollar_per_joule*week, "week"))
    print(Money(power_W*dollar_per_joule*month, "month"))
    print(Money(power_W*dollar_per_joule*year, "year"))
    cpy = power_W*dollar_per_joule*year
    print("Yearly cost as a function of hours per day:")
    hr_per_day = 24
    results = []
    for i in range(1, hr_per_day + 1):
        s = Money(cpy*i/hr_per_day, "year")
        s = s.strip().replace(" per year", "")
        results.append("  {:2d}:  ".format(i) + s)
    for i in Columnize(results):
        print(i)
def Instruments():
    fp= FPFormat()  # Use to line up cost decimal points
    fp.digits(2)
    inst = {
        "HP 427A     Voltmeter": 0.5,
        "HP 3435A    Digital multimeter": 2,
        "HP 3466A    Digital multimeter": 2,
        "HP 3400A    RMS voltmeter": 7,
        "HP E3615A   Power supply": 7,
        "B&K 8500    DC Load": 9,
        "B&K 4052    Function generator": 13,
        "B&K 2556A   Oscilloscope": 20,
        "B&K 9130    Power supply": 20,
        "HP 3456A    Voltmeter": 21,
        "HP 6038A    Power supply": 34,
        "HP 6033A    Power supply": 38,
        "HP 54601B   Oscilloscope": 50,
    }
    print(dedent(f'''
    Cost to run various instruments (power supplies in quiescent state)

    Instrument                       Power, W     ¢/day     $/year
    ------------------------------   --------     -----     ------
    '''))
    c = flt(1.80556e-08)     # Power cost in $/J
    cent_day = 24*3600*100*c    # Cost of 1 W for 24 hr in cents
    c.rtz = c.rtdp = True
    # Number check:  1 W for 24 hr is 24*3600 J or 86400 J.  At 2.78e-7 $/J,
    # this is a cost of $0.0240.  Thus, a 20 W instrument should cost 48
    # cents per day or $175/year.
    for i, pow in inst.items():
        day = flt(pow*cent_day)
        yr = flt(365.25*day/100)
        p = fp.dp(pow, width=6, dpoint=3)
        d = fp.dp(day, width=6, dpoint=3)
        y = fp.dp(yr, width=6, dpoint=3)
        print(f"{i:32s} {p:8s}    {d:6s}     {y:6s}")
    print("Cost of power is 6.5¢ per kW*hr = 1.806e-8 $/J")
if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    for arg in args:
        Power(arg)
