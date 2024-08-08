'''
Print out the cost of electrical power.
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Print out cost of electrical power
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Imports
        import sys
        from math import *
        import getopt
        from pprint import pprint as pp
    if 1:   # Custom imports
        from wrap import dedent
        from f import flt
        from fpformat import FPFormat
        from columnize import Columnize
        from u import u, ParseUnit, dim
        from color import t
        import matrix
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        ii = isinstance
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Manpage():
    print(dedent(f'''
    This script prints out the cost of electrical power for a constant load.  The assumptions are
        
        - Your cost for electrical power is a constant
        - The power dissipation of the load is constant
        - The power factor is 1

    The output is a table that gives the cost as a function of how many hours per day you run the
    load.

    Example
    -------

        I have two 22 inch square box fans that run at 70 W on high, as measured by a Kill-a-Watt
        meter.  I use these fans to pull cool outside air into and through the house during the
        summer to cool the walls, floor, and ceiling of the house.  These fans typically run from
        about 10 pm to 9 am each day.  

        I use this script to print out a cost table with the command line arguments of '2*70'.
        The table printed is 

            Cost of electrical power:  input is '2*70'
              Cost basis is 11.6 ¢ per kW*hr
              Input power is = 140 W = 0.19 hp
              Output is rounded to 2 figures (-d option)
            
            hr/day   Daily     Weekly   Monthly    Yearly 
            ------  --------  --------  --------  --------  
              1       1.6¢      11¢       49¢       $5.9  
              2       3.2¢      23¢       98¢       $12   
            <snip>
              11      18¢       $1.2      $5.4      $65   
            <snip>
              23      37¢       $2.6      $11       $140  
              24      39¢       $2.7      $12       $140  

        The command line argument '2*70' shows that you can use python syntax to compute the
        desired power.  The math module's symbols are in scope.  Since I run the fans from 10 pm
        to 9 am, the total time is 11 hours per day.  My power cost is 18¢ per day or $5.4 per
        month.  

        Contrast this to my air conditioning unit, whose minimum circuit current specification on
        the label is nearly 25 A at 240 V RMS, which is 6 kW of power.  On hot days where I live
        (at and above 105 °F), the air conditioner can run continuously and be unable to cool the
        house to 90 °F or lower.  I've measured the plywood of the roof under such conditions at
        160 °F and the attic at 130 °F, even with the attic fan running full time.  Running the
        air conditioner for 6 hours at 6 kW and an assumed power factor of 0.9 costs $3.7 per day.
        A month of such temperatures and power use would cause a significant increase in my
        electric bill.

        Those cheap box fans are used to avoid using the air conditioner.  At night, I use the
        fans to draw cool air in at one end of the house and exhaust it at the other end of the
        house.  The goal is to get turbulent cool airflow and use it to cool off the ceiling,
        walls, and floors during the night.  In the morning, the house is nearly the same as the
        outside temperature and I can avoid running the air conditioner at all.  A friend in
        Phoenix AZ uses this method along with an airflow meter to measure the flow velocity.  He
        also opens cupboard doors, closet doors, etc. to disrupt laminar air flow and cool these
        volumes off also.

    Power factor:  It is assumed the power factor is unity unless you use the -p option.  If you
    are not familiar with the concept of power factor and real versus apparent power, see
    https://en.wikipedia.org/wiki/Power_factor.  The cost numbers in the table are scaled by the
    power factor.  Typical consumers aren't dinged for non-unity power factors, but industrial
    users are unless they install power factor correction circuitry.  

    '''))
    exit(0)
def Usage(status=0):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] p1 [p2 ...]
      Prints out various period costs of electrical power for the rate of {100*flt(d["-r"])}¢/(kW*hr) for a given
      power p1, p2, ... in watts.  Cost is current as of {d["date"]} for southwest Idaho USA.

      You can append an optional power unit to p1 with a space (put the expression in quotes to
      escape it from shell parsing).  The powers can be expressions (the math module's symbols are
      in scope).
    Example:
        {sys.argv[0]} '300*cos(49*pi/180) hp'
      prints out a table for a power of an apparent power of 300 hp at a power factor angle of 49
      degrees (power factor is 0.65).
    Options:
      -d n      Set the number of significant figures in the output [{d["-d"]}]
      -l        Print typical lighting power table
      -h        Print a manpage
      -i        Print the consumption of various instruments
      -r C      Change the cost per kW*hr to C dollars
      -t        Show some costs for typical appliances
    '''))
    exit(status)
def ParseCommandLine(d):
    # From https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a
    d["date"] = "May 2024"  # Month/year of above webpage revision
    d["-d"] = 2         # Number of significant digits
    d["-i"] = False     # Instrument consumption
    d["-l"] = False     # Print out lighting power too
    d["-p"] = 1         # Power factor
    # This value is for the state of Idaho
    d["-r"] = "0.1155"  # Cost of kW*hr of electrical energy in $
    d["-t"] = False     # Table of typical costs
    flt(0).N = d["-d"]
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:hilp:r:t")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in "ilt":
            d[o] = not d[o]
        elif o in ("-d",):
            try:
                d["-d"] = int(a)
                if not (1 <= d["-d"] <= 15):
                    raise ValueError()
            except ValueError:
                Error("-d argument must be an integer between 1 and 15")
        elif o == "-h":
            Manpage()
        if o in ("-p",):
            try:
                d[o] = float(a)
                if not 0 < d[o] <= 1:
                    raise Exception()
            except Exception:
                Error("-p option's argument must be a number on (0, 1]")
        if o in ("-r",):
            try:
                d[o] = float(a)
                if d[o] <= 0:
                    raise Exception()
            except Exception:
                Error("-r option's argument must be a number > 0")
    x = flt(0)
    x.N = d["-d"]
    x.rtz = False
    x.rtdp = True
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
        Usage()
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
    print(dedent('''
    Lighting electrical power consumption, W
      From https://en.wikipedia.org/wiki/Lumen_%28unit%29
      Accessed 25 Jan 2017

             Incandescent
    Lumens   Non-halogen  Halogen   CFL         LED 
       90        15          6      2-3          3  
      200        25                 3-5          3  
      450        40          29     9-11        5-8  
      800        60                 13-15       9-12  
     1100        75          53     18-20      13-16  
     1600       100          72     24-28      18-22  
     2400       150                 30-52       30  
     3100       200                 49-75       32  
     4000       300                 75-100      40.5  

    Luminous efficiency
        https://en.wikipedia.org/wiki/Luminous_efficacy#Examples_2
        # = 120 V, @ = 230 V, [I have rounded to 2 figures]

                                    lm/W        %
    Combustion, gas mantle           1-2        0.15-0.3
    100 W tungsten incand. #         18         2.6
    100 W tungsten halogen @         17         2.4
    LED screw base lamp #            100        15
    LED, theoretical max             260-300    38-44
    Carbon arc                       2-7        0.3-1
    Xenon arc                        30-90      4.4-14
    Mercury-xenon arc                50-55      7.3-8
    HP Hg vapor arc                  58-78      8.5-11
    9-32 W CFL                       46-75      8-11
    T8 fl. tube, elec. ballast       80-100     12-15
    HP Na                            85-150     12-22
    LP Na                            100-200    15-29
    Truncated 5800 K black body      251        37
    Ideal, green 555 nm              683        100

    '''))
def Instruments():
    fp= FPFormat()  # Use to line up cost decimal points
    inst = {
        # Item:  power in W
        #"HP 427A     Voltmeter": 0.06,
        #"HP 3435A    Digital multimeter": 2,
        #"HP 3466A    Digital multimeter": 2,
        #"HP 3400A    RMS voltmeter": 7,
        "HP E3615A   Power supply": 7,
        "B&K 8500    DC Load": 9,
        "B&K 4052    Function generator": 13,
        #"B&K 2556A   Oscilloscope": 20,
        "B&K 9130    Power supply": 20,
        #"HP 3456A    Voltmeter": 21,
        "HP 6038A    Power supply": 34,
        "HP 6033A    Power supply": 38,
        "HP 54601B   Oscilloscope": 50,
        "HP 428B     Clamp-on ammeter": 50,
    }
    print(dedent(f'''
    Cost to run various instruments (power supplies in quiescent state)

    Instrument                       Power, W     ¢/day     $/month
    ------------------------------   --------     -----     -------
    '''))
    kWhr_cost = flt(d["-r"])    # Cost of a kW*hr in $
    J_per_kWhr = 3600000        # A kW*hr is 3600000 J
    dpj = kWhr_cost/J_per_kWhr  # Cost of power in $/J
    # Check with GNU units:  0.1155 $/(kW*hr) is equal to 3.2083333e-08 $/J
    assert abs(dpj - 3.2083333e-08) < 1e-15
    cent_day = 24*3600*100*dpj  # Cost of 1 W for 24 hr in cents
    fp.digits(3)    # Show numbers to 3 digits
    dpj.N = 3    
    dpj.rtz = dpj.rtdp = False
    monthly_total = 0
    for i, pow in inst.items():
        day = pow*cent_day              # In cents per day
        mo = flt(365.25*day/(12*100))   # In dollars per month
        p = fp.dp(pow, width=6, dpoint=3)
        D = fp.dp(day, width=6, dpoint=3)
        m = fp.dp(mo, width=6, dpoint=3)
        print(f"{i:32s} {p:8s}    {D:6s}     {m:6s}")
        monthly_total += mo
    print(f"\nMonthly cost to run all of these is ${monthly_total}")
    print(f"Cost of power is ${d['-r']} per kW*hr = {dpj} $/J")
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
    print(f"{'Item':^{w}s}  Watts    $ per 8 hr")
    print(f"{'-'*w:^{w}s}  -----    ----------")
    c = 100*flt(2.77778e-07)*d["-r"]  # Power cost in cents/J
    cents_day = 8*3600*c    # Cost of 1 W for 8 hr in cents
    for item in items:
        power_W, name = item
        cost = cents_day*power_W
        dollars = cost/100
        print(f"{name:{w}s}  {int(power_W):4d}     {dollars!s:^11s}")
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
        12.91 	District of Columbiacurrent  
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
        # Make sure un is dimensionally equal to power
        if dim(un) != dim("W"):
            Error(f"{un!r} is not a unit of power")
        unit = un
    power_W = flt(eval(val)*u(unit))
    dollar_per_kW_hr = flt(d["-r"])
    dollar_per_joule = dollar_per_kW_hr/3.6e6
    kW_per_hp = flt(745.7)
    hp = str(power_W/kW_per_hp)
    if 1:   # Header
        print(f"Cost of electrical power:  input is {power_expr!r}")
        print(f"  Cost basis is {dollar_per_kW_hr*100:.1f} ¢ per kW*hr")
        print(f"  Input power is = {power_W} W = {hp} hp")
        print(f"  Output is rounded to {d['-d']} figures (-d option)")
        print()
    pf = d["-p"]    # Power factor
    const = pf*power_W*dollar_per_joule
    cpd, cpw, cpm, cpy = [const*i for i in (day, week, month, year)]
    # Print daily, weekly, monthly, yearly in columns
    if 1:   # Generate table
        o = []
        for hr_per_day in range(1, 25):
            s = []
            s.append(f"{hr_per_day:^6d}")
            s.append(Money(cpd*hr_per_day/24, "day").strip().replace(" per day", ""))
            s.append(Money(cpw*hr_per_day/24, "week").strip().replace(" per week", ""))
            s.append(Money(cpm*hr_per_day/24, "month").strip().replace(" per month", ""))
            s.append(Money(cpy*hr_per_day/24, "year").strip().replace(" per year", ""))
            o.append(s)
    if 1:   # Get maximum column widths
        m = matrix.matrix(o)    # m is a 24x5 matrix
        w = []
        w.append(6)
        w.append(max(len(i[2]) for i in m.col(1)))
        w.append(max(len(i[2]) for i in m.col(2)))
        w.append(max(len(i[2]) for i in m.col(3)))
        w.append(max(len(i[2]) for i in m.col(4)))
        for i in (1, 2, 3, 4):
            w[i] = max(w[i], 8)
    gap = " "*2     # Space between columns
    if 1:   # Header
        print(f"{'hr/day':^{w[0]}s}{gap}"
                f"{'Daily':^{w[1]}s}{gap}"
                f"{'Weekly':^{w[2]}s}{gap}"
                f"{'Monthly':^{w[3]}s}{gap}"
                f"{'Yearly':^{w[4]}s}")
        for i in w:
            print(f"{'-'*i:^{i}s}", end=gap)
        print()
    if 1:   # Table
        for item in o:
            print(f"{item[0]:^{w[0]}s}{gap}"
                    f"{item[1]:^{w[1]}s}{gap}"
                    f"{item[2]:^{w[2]}s}{gap}"
                    f"{item[3]:^{w[3]}s}{gap}"
                    f"{item[4]:^{w[4]}s}")

if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    for arg in args:
        Power(arg)
