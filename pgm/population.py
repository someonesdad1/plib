"""
Print out CDC population projections for 2025
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2020 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Print out CDC population projections for 2025
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import os
    import sys
    from pprint import pprint as pp
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
    from f import flt
    from columnize import Columnize

    if 0:
        import debug

        debug.SetDebugger()
if 1:  # Global variables

    class g:
        pass

    g.width = int(os.environ.get("COLUMNS", 80)) - 1
    ii = isinstance
    # Downloaded Sun 18 Jul 2021 11:37:14 AM
    # Go to https://wonder.cdc.gov/controller/datarequest?stage=search&action=current
    # and enter "population projection".  This will show a "National
    # Population Projections 2014-2060" database.  Click on the DataRequest
    # link, then choose 2025 for the year; press the Send button.
    #
    # CDC projection for US population in 2025
    # Age,  population (age 0 means < 1 year old)
    # The number for 100 is all people 100 and older
    us_pop_2025 = dedent("""
        0      4186576
        1      4197220
        2      4205907
        3      4210440
        4      4210075
        5      4204428
        6      4193907
        7      4180042
        8      4164245
        9      4146602
        10     4128442
        11     4109654
        12     4089560
        13     4098930
        14     4128441
        15     4131344
        16     4142165
        17     4287520
        18     4331448
        19     4326904
        20     4346931
        21     4389574
        22     4392852
        23     4408702
        24     4539354
        25     4628888
        26     4583669
        27     4602895
        28     4625272
        29     4661876
        30     4749435
        31     4825917
        32     4874647
        33     4970042
        34     5029834
        35     4997740
        36     4792058
        37     4664181
        38     4568193
        39     4563702
        40     4575594
        41     4419964
        42     4463654
        43     4447184
        44     4384387
        45     4450111
        46     4172187
        47     4076565
        48     4022069
        49     3892190
        50     3991435
        51     3855959
        52     3896116
        53     4053760
        54     4265522
        55     4300840
        56     4066170
        57     3964599
        58     3954133
        59     4008084
        60     4225261
        61     4283946
        62     4260421
        63     4233305
        64     4262292
        65     4270214
        66     4104003
        67     4051170
        68     3975371
        69     3801304
        70     3731353
        71     3543067
        72     3368881
        73     3196938
        74     3051136
        75     2926656
        76     2790385
        77     2705841
        78     2750507
        79     1980674
        80     1894298
        81     1786857
        82     1759610
        83     1469854
        84     1279906
        85     1146127
        86     1014374
        87     906904
        88     774675
        89     678967
        90     592109
        91     478724
        92     411762
        93     345627
        94     285336
        95     234032
        96     177955
        97     138358
        98     103182
        99     74014
        100    119381
        Total  347334912
    """)


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(d, status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options]
      Prints a table of the projected population in millions by age for the 
      year 2025.  Source was CDC.
    Options:
      -c    Show cumulative data
      -d n  Print to n significant figures [{d["-d"]}]
      -H    Print a histogram
      -h    Print a manpage
      -p    Print percentages of the total US population
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-c"] = False  # Print cumulative data
    d["-H"] = False  # Print histogram
    d["-p"] = False  # Print percentages
    d["-d"] = 3  # Number of significant digits
    try:
        opts, args = getopt.getopt(sys.argv[1:], "cd:Hhp")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("cHp"):
            d[o] = not d[o]
        elif o in ("-d",):
            try:
                d["-d"] = int(a)
                if not (1 <= d["-d"] <= 15):
                    raise ValueError()
            except ValueError:
                msg = "-d option's argument must be an integer between 1 and 15"
                Error(msg)
        elif o in ("-h", "--help"):
            Usage(d, status=0)
    flt(0).n = d["-d"]
    return args


def Rnd(n):
    """Return the integer n rounded to the current number of significant
    figures.
    """
    assert ii(n, int)
    x = flt(n)
    with x:
        x.rtz = True
        s = str(flt(n))
        if s[-1] == ".":
            s = s[:-1]
        return int(s)


def GetData():
    population, population_total = [], None
    for line in us_pop_2025.split("\n"):
        line = line.strip()
        if not line:
            continue
        age, num = [i.strip() for i in line.split()]
        if age == "Total":
            population_total = int(num)
        else:
            population.append([age, int(num)])
    assert population_total == sum([j for i, j in population])
    # Get cumulative population data
    cumulative = [i[:] for i in population]
    for i in range(1, len(cumulative)):
        cumulative[i][1] += cumulative[i - 1][1]
    return population, cumulative, population_total


def PctTable():
    N = population_total
    o = []
    for age, n in population:
        f = flt(100 * n / N)
        o.append((age, f))
    # Get width of widest fraction
    w = max([len(str(f)) for age, f in o])
    t = [f"Age  {'%':^{w}s}"]
    for age, f in o:
        t.append(f"{age:^4s} {f!s:>{w}s}")
    print(
        dedent(f"""
    Percent of total US population by age in years (CDC projection for 2025)
      Printed to {d["-d"]} significant figures
      Total population = {N:,}
    """)
    )
    for line in Columnize(t):
        print(line)


def PopTable():
    N = population_total
    o = ["Age   Number"]
    for age, n in population:
        o.append(f"{age:^4s} {Rnd(n):>9,d}")
    print(
        dedent(f"""
    Total US population by age in years (CDC projection for 2025)
        Printed to {d["-d"]} significant figures
        Total population = {N:,}
    """)
    )
    for line in Columnize(o):
        print(line)


def CumulPctTable():
    N = population_total
    o = []
    for age, n in cumulative:
        f = flt(100 * n / N)
        o.append((age, f))
    # Get width of widest fraction
    w = max([len(str(f)) for age, f in o])
    t = [f"Age  {'%':^{w}s}"]
    for age, f in o:
        t.append(f"{age:^4s} {f!s:>{w}s}")
    print(
        dedent(f"""
    Cumulative % of total US population by age in years (CDC projection for 2025)
      Printed to {d["-d"]} significant figures
      Total population = {N:,}
    """)
    )
    for line in Columnize(t):
        print(line)


def CumulPopTable():
    N = population_total
    o = ["Age   Number"]
    for age, n in cumulative:
        o.append(f"{age:^4s} {Rnd(n):>11,d}")
    print(
        dedent(f"""
    Cumulative total US population by age in years (CDC projection for 2025)
      Printed to {d["-d"]} significant figures
      Total population = {N:,}
    """)
    )
    for line in Columnize(o):
        print(line)


def GetDict():
    """Return a dictionary of age: population where age is a string and
    population is an integer.
    """
    pd = {}
    for age, value in population:
        pd[age] = value
    return pd


def PrintAge(age):
    try:
        int(age)
    except ValueError:
        Error(f"'{age}' is not an integer age")
    if int(age) not in range(101):
        Error(f"'{age}' must be between 0 and 99 inclusive")
    N = population_total
    pd = GetDict()
    print(
        dedent(f"""
    CDC US population projection for 2025
      Printed to {d["-d"]} significant figures
      Total population = {Rnd(N):,}
    """)
    )
    print(f"Age {age}")
    n = Rnd(pd[age])
    p = flt(100 * pd[age] / N)
    print(f"  Number of people this age {n:,} ({p}%)")
    # People younger and older than this age
    a = int(age)
    if a <= 99:
        y = Rnd(sum([i[1] for i in population[:a]]))
        o = Rnd(sum([i[1] for i in population[a + 1 :]]))
    else:
        y = Rnd(sum([i[1] for i in population[:100]]))
        o = 0
    yp, yo = flt(100 * y / N), flt(100 * o / N)
    print(f"  Number of people younger than this age {y:,} ({yp}%)")
    print(f"  Number of people older than this age   {o:,} ({yo}%)")


def Histogram():
    N = population_total
    print(
        dedent(f"""
    CDC US population projection for 2025
      Total population = {N:,}
    """)
    )
    pct = [flt(100 * i[1] / N) for i in population]
    pmin, pmax, w = min(pct), max(pct), g.width - 4
    for i in range(101):
        print(f"{i:^3d}", end=" ")
        p = pct[i] / pmax
        print(f"{'*' * (int(p * w))}")


if __name__ == "__main__":
    d = {}  # Options dictionary
    ages = ParseCommandLine(d)
    population, cumulative, population_total = GetData()
    if ages:
        for age in ages:
            PrintAge(age)
    else:
        if d["-c"]:
            CumulPctTable() if d["-p"] else CumulPopTable()
        elif d["-H"]:
            Histogram()
        else:
            PctTable() if d["-p"] else PopTable()
