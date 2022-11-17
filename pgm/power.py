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
    from color import C
if 1:   # Global variables
    ii = isinstance
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    flt(0).n = 3
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] p1 [p2 ...]
      Prints out various period costs of electrical power for the rate of
      {100*flt(d["-r"])}¢/(kW*hr) for a given power p1, p2, ... in watts.  

      You can append an optional power unit to p1 with a space (put the
      expression in quotes to escape it from shell parsing).  The powers
      can be expressions (the math module's symbols are in scope).
    Example:
        {sys.argv[0]} '300*cos(49*pi/180) hp'
      prints out a table for a power of an apparent power of 300 hp at a power
      factor angle of 49 degrees (power factor is 0.65).
    Options:
      -d n      Set the number of significant figures in the output [{d["-d"]}]
      -l        Print typical lighting power table
      -r C      Change the cost per kW*hr to C dollars
      -i        Print the consumption of various instruments
      -t        Show some costs for typical appliances
    '''))
    exit(status)
def ParseCommandLine(d):
    x = flt(0)
    d["-r"] = "0.104"   # Cost of kW*hr of electrical energy in $
    d["-d"] = 2         # Number of significant digits
    d["-l"] = False     # Print out lighting power too
    d["-i"] = False     # Instrument consumption
    d["-t"] = False     # Table of typical costs
    x.n = d["-d"]
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:hilr:t")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in "ilt":
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
    x.N = d["-d"]
    if d["-i"]:
        Instruments()
        exit(0)
    elif d["-l"]:
        Lighting()
        exit(0)
    elif d["-t"]:
        TypicalAppliances()
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
def Instruments():
    fp= FPFormat()  # Use to line up cost decimal points
    fp.digits(2)
    inst = {
        # Item:  power in W
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
    c = flt(2.77778e-07)*d["-r"]/100  # Power cost in $/J
    cent_day = 24*3600*100*c    # Cost of 1 W for 24 hr in cents
    c.rtz = c.rtdp = True
    # Number check:  1 W for 24 hr is 24*3600 J or 86400 J.  At 2.78e-7 $/J,
    # this is a cost of $0.0240.  Thus, a 20 W instrument should cost 48
    # cents per day or $175/year.
    for i, pow in inst.items():
        day = flt(pow*cent_day)
        yr = flt(365.25*day/100)
        p = fp.dp(pow, width=6, dpoint=3)
        D = fp.dp(day, width=6, dpoint=3)
        y = fp.dp(yr, width=6, dpoint=3)
        print(f"{i:32s} {p:8s}    {D:6s}     {y:6s}")
    print("Cost of power is 6.5¢ per kW*hr = 1.806e-8 $/J")
def TypicalAppliances():
    # Most of this data from https://generatorist.com/power-consumption-of-household-appliances
    items = [
        ("100 W light bulb", 100),
        ("75 W light bulb", 75),
        ("60 W light bulb", 60),
        ("20 W LED or CFL light bulb", 20),
        ("10 W LED light bulb", 10),
        ("1.2 kW electric heater", 1200),
        ("1 W LED light", 1),
        ("Heat pump", 4700),
        ("Electric water heater", 4000),
        ("Tankless electric water heater", 6600),
        ("1/2 hp well pump", 1000),
        ("Central air conditioning", 3800),
        ("1/3 hp furnace fan", 700),
        ("Microwave", 1000),
        ("Electric stove, 8 inch element", 2100),
        ("Electric oven", 2150),
        ("Electric clothes dryer", 5400),
        ("Hair dryer", 1250),
        ("Freezer", 500),
        ("Dishwasher", 1500),
        ("Modern refrigerator", 400),
        ("Smart refrigerator", 500),
        ("Washing machine", 1150),
        ("Vacuum cleaner", 1150),
        ("Desktop computer", 100),
        ("Laser print (running)", 600),
        ("Pedestal fan", 50),
    ]
    items = sorted([(i[1], i[0]) for i in items])
    w = max([len(i[1]) for i in items])
    print(f"{'Item':^{w}s}  Watts    ¢ per 8 hr")
    print(f"{'-'*w:^{w}s}  -----    ----------")
    c = 100*flt(2.77778e-07)*d["-r"]  # Power cost in cents/J
    cents_day = 8*3600*c    # Cost of 1 W for 8 hr in cents
    for item in items:
        power_W, name = item
        cost = cents_day*power_W
        print(f"{name:{w}s}  {int(power_W):4d}     {cost!s:^11s}")
def PowerCostByState():
    '''Return a dict keyed by state with value of average cost in cents per
    kW*hr.
    '''
    # Residential power costs from https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a	
    # Downloaded 22 Oct 2021	
    # Average cost in cents per kW*hr	
    data = '''
        10.24 	Washington 
        10.41 	Idaho 
        10.86 	Nevada 
        10.91 	Louisiana 
        11.00 	Utah 
        11.23 	Oklahoma 
        11.26 	Tennessee 
        11.42 	Arkansas 
        11.49 	Oregon 
        11.56 	North Carolina 
        11.56 	Montana 
        11.60 	Kentucky 
        11.63 	Nebraska 
        11.65 	Mississippi 
        11.72 	Wyoming 
        11.75 	Texas 
        11.88 	Delaware 
        11.89 	Florida 
        12.11 	West Virginia 
        12.23 	North Dakota 
        12.64 	Arizona 
        12.71 	Virginia 
        12.85 	South Dakota 
        12.90 	South Carolina 
        12.91 	District of Columbia 
        12.98 	Maryland 
        13.07 	Kansas 
        13.12 	Ohio 
        13.21 	Missouri 
        13.23 	Illinois 
        13.35 	Alabama 
        13.43 	Indiana 
        13.44 	Colorado 
        13.55 	Georgia 
        13.73 	Pennsylvania 
        13.98 	Minnesota 
        14.39 	Iowa 
        14.49 	New Mexico 
        14.56 	Wisconsin 
        16.38 	Maine 
        16.99 	New Jersey 
        17.79 	Michigan 
        18.99 	Vermont 
        19.05 	New Hampshire 
        19.60 	New York 
        20.50 	Rhode Island 
        22.04 	Connecticut 
        22.45 	California 
        22.85 	Massachusetts 
        23.42 	Alaska 
        33.24 	Hawaii 
    '''
    pc = {}
    for line in data.split("\n"):
        line = line.strip()
        if not line:
            continue
        cost, state = line.split("\t")
        print(flt(cost), state)
        pc[state] = flt(cost)
    return pc
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
    N = C.norm
    print("{} costs (at {:.1f} ¢ per kW*hr):".format(s,
          dollar_per_kW_hr*100))
    print(Money(power_W*dollar_per_joule*hour, "hour"))
    print(C.lgrn, Money(power_W*dollar_per_joule*eight_hour_day, "8 hour day"), N, sep="")
    print(Money(power_W*dollar_per_joule*day, "day"))
    print(C.lyel, Money(power_W*dollar_per_joule*week, "week"), N, sep="")
    print(Money(power_W*dollar_per_joule*month, "month"))
    print(C.lred, Money(power_W*dollar_per_joule*year, "year"), N, sep="")
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
if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    for arg in args:
        Power(arg)
