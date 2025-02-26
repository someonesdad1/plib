"""

ToDo
    - -r option changes the reference resistance R in Ω (600 Ω default)
    - Change existing -r to -s option (step of table); allow n to be a float > 0
    - Change command line to 'low_dB high_dB [step]' for generating table

Prints out tables of dB stuff

"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Prints out tables of dB stuff
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import os
    import sys
    from math import sqrt, log10 as log
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
    from columnize import Columnize
    from f import flt, sqrt, log10
    from color import t
if 1:  # Global variables
    W = int(os.environ["COLUMNS"]) - 1
    x = flt(0)
    x.N = 3
    x.rtz = True
    # Color coding
    t.dBV = t("brnl")
    t.dBm600 = t("magl")
    t.dBm50 = t("grnl")
    t.dBm75 = t("yell")
    t.always = True


def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)


def Usage(d, status=1):
    name = sys.argv[0]
    print(
        dedent(f"""
    Usage:  {name} [options]
      Print dB information.  The default is to print a dBm(600 Ω) to voltage table.  The range
      printed is typical for HP AC voltmeters, -80 to 60 dBm.
    Options:
        -5      Print dBm(50 Ω) to dBm(600 Ω) table
        -d      Print distortion in dBc table converted to %
        -h      Print a manpage
        -n n    Use n digits in calculations
        -p      Show voltage drop in % vs drop in dB
        -r n    Print dB table in steps of n [{d["-r"]}]
        -t      Print a conversion table amongst common dB measures
        -v      Print dBV to dBm(600 Ω) table
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-5"] = False  # Print dBm(50 Ω) to dBm(600 Ω) table
    d["-d"] = False  # Print distortion data only
    d["-n"] = 3  # Number of digits
    d["-p"] = False  # % drop vs dB
    d["-r"] = 0  # dB table step
    d["-t"] = False  # Print conversions amongst common dB measures
    d["-v"] = False  # Print dBV to dBm(600 Ω) table
    try:
        opts, args = getopt.getopt(sys.argv[1:], "5dhn:pr:t")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("5dpt"):
            d[o] = not d[o]
        elif o == "-n":
            d[o] = n = int(a)
            if not (1 <= n <= 15):
                Error(f"Number of digits must be between 1 and 15")
            flt(0).N = n
        elif o == "-r":
            d[o] = n = int(a)
            if n < 1:
                Error(f"{o} option's value must be integer > 0")
        elif o in ("-h", "--help"):
            Usage(d, status=0)
    return args


def Distortion():
    print(f"{'Distortion in dBc (dB below carrier) converted to %':^{W}s}")
    print(f"{'percent = 100*10**(dBc/20)':^{W}s}")
    out = ["dBc   %"]
    for dBc in range(101):
        pct = flt(100 * 10 ** (-dBc / 20))
        out.append(f"{-dBc:4d}  {pct}")
    for i in Columnize(out):
        print(i)


def dBV_dBm600():
    w1, w2 = 8, 8
    print(f"{'dBV to dBm(600 Ω)':^{W}s}")
    out = [f"{t.dBV}{'dBV':^{w1}s}{t.n}  {t.dBm600}{'dBm':^{w2}s}{t.n}"]
    for dBV in range(60, 0, -d["-r"]):
        dBm = flt(20 * log(10 ** (dBV / 20) / sqrt(600 / 1000)))
        out.append(f"{t.dBV}{str(dBV):^{w1}s}{t.n}  {t.dBm600}{dBm!s:^{w2}s}{t.n}")
    for dBV in range(101):
        dBm = flt(20 * log(10 ** (-dBV / 20) / sqrt(600 / 1000)))
        out.append(f"{t.dBV}{str(-dBV):^{w1}s}{t.n}  {t.dBm600}{dBm!s:^{w2}s}{t.n}")
    for i in Columnize(out):
        print(i)


def Header():
    print(
        dedent(f"""
    dBm definitions (R in Ω, V in volts)
        dBm(R Ω) = 20*log(V/sqrt(R/1000))
        V = sqrt(R/1000)*10**(dBm/20)
        R = V**2*10**(-dBm/10 + 3)
     
    Converting between different dBm voltage measures:
        dBm(R Ω) = dBm(S Ω) + C where C = 10*log(S/R)
            dBm(50 Ω) = dBm(600 Ω) + 10.8
            dBm(75 Ω) = dBm(600 Ω) + 9.0
            dBm(50 Ω) = dBm(75 Ω) + 1.8
        0 dBm(600 Ω) is 0.7746 V = sqrt(600/1000)
        0 dBm(50 Ω) is 0.2236 V = sqrt(50/1000)
        0 dBm(75 Ω) is 0.2739 V = sqrt(75/1000)
    """)
    )


def ConversionTable():
    w = 12  # Column width
    hdr = (
        f"{'Value':>{w}s}",
        f"{'dBm(50 Ω)':>{w}s}",
        f"{'dBm(75 Ω)':>{w}s}",
        f"{'dBm(600 Ω)':>{w}s}",
        f"{'dBV':>{w}s}",
        f"{'dBmV':>{w}s}",
        f"{'dBuV':>{w}s}",
    )
    print("dB values in voltage for various references\n")
    h = t.magl  # Header color
    t.print(f"{h}{' '.join(hdr)}")
    for db in range(60, -120 - 1, -d["-r"]):
        res = []
        res.append(sqrt(50 / 1000) * 10 ** (db / 20))  # dBm(50)
        res.append(sqrt(75 / 1000) * 10 ** (db / 20))  # dBm(75)
        res.append(sqrt(600 / 1000) * 10 ** (db / 20))  # dBm(600)
        res.append(10 ** (db / 20))  # dBV
        res.append(1e-3 * 10 ** (db / 20))  # dBmV
        res.append(1e-6 * 10 ** (db / 20))  # dBμV
        res = [f"{flt(i).engsi + 'V'!s:>{w}s}" for i in res]
        res.insert(0, f"{'%3d' % db!s:>{w}s}")
        if db % 10 == 0:
            t.print(f"{t('grnl')}{' '.join(res)}")
        else:
            print(" ".join(res))
    t.print(f"{h}{' '.join(hdr)}")


def Title(s):
    # The following is needed to get the underlining to print all the way across
    sp = " " * ((W - len(s)) // 2)
    s = sp + s + sp[:-1] + chr(0xA0)
    t.print(f"{t(attr='ul')}{s:^{W}s}")


def dBmToVoltage(R=600, nl=False):
    "Print a dBm(R Ω) to voltage table"
    # Colors
    C = {600: t.magl, 50: t.yell, 75: t.trql}
    c = C.get(R, "t.whtl")
    w1, w2 = 12, 8
    Title(f"dBm({R} Ω) to voltage")
    out = [f"{c}{f'dBm({R} Ω)':^{w1}s}{t.n}  {'Voltage, V':^{w2}s}"]
    u = sqrt(R / 1000)
    for dBm in range(50, 0, -d["-r"]):
        V = flt(u * 10 ** (dBm / 20))
        out.append(f"{c}{str(dBm):^{w1}s}{t.n}  {V.engsi + 'V':^{w2}s}")
    for dBm in range(0, -61, -d["-r"]):
        V = flt(u * 10 ** (dBm / 20))
        out.append(f"{c}{str(dBm):^{w1}s}{t.n}  {V.engsi + 'V':^{w2}s}")
    for i in Columnize(out):
        print(i)
    if nl:
        print()


def dBVToVoltage():
    w1, w2 = 12, 8
    Title("dBV to voltage")
    out = [f"{t.dBV}{'dBV':^{w1}s}{t.n}  {'Voltage, V':^{w2}s}"]
    for dBV in range(50, 0, -d["-r"]):
        V = flt(10 ** (dBV / 20))
        out.append(f"{t.dBV}{str(dBV):^{w1}s}{t.n}  {V.engsi + 'V':^{w2}s}")
    for dBV in range(0, -61, -d["-r"]):
        V = flt(10 ** (dBV / 20))
        out.append(f"{t.dBV}{str(dBV):^{w1}s}{t.n}  {V.engsi + 'V':^{w2}s}")
    for i in Columnize(out):
        print(i)


def dB50_to_dB600():
    w1, w2 = 12, 12
    t.print(f"{t(attr='ul')}{'dBm(50 Ω) to dBm(600 Ω)':^{W}s}")
    print()
    out = [f"{t.dBm50}{'dBm(50 Ω)':^{w1}s}{t.n}  {t.dBm600}{'dBm(600 Ω)':^{w2}s}{t.n}"]
    c = flt(10 * log10(600 / 50))
    for dBm50 in range(60, 0, -d["-r"]):
        dBm600 = dBm50 + c
        out.append(f"{t.dBm50}{dBm50!s:^{w1}s}{t.n}  {t.dBm600}{dBm600!s:^{w2}s}{t.n}")
    for dBm50 in range(0, 81, d["-r"]):
        dBm600 = -dBm50 + c
        out.append(f"{t.dBm50}{-dBm50!s:^{w1}s}{t.n}  {t.dBm600}{dBm600!s:^{w2}s}{t.n}")
    for i in Columnize(out):
        print(i)


def PercentDrop():
    print(f"dB drop versus percentage drop")


"""
Change to command on command line

Commands
    eq
        Print equations
    db%
        dB drop to percentage table
    %db
        % drop to dB drop 
            Equations:
                dB = 20*log10(V/V0)
                10**(dB/20) = V/V0
                or V = V0*10**(dB/20)
                % = 100*(V - V0)/V0 = 100(V/V0 - 1) = 100*(10**(dB/20) - 1)
    dbc
        Distortion in dBc converted to % table
    %
        Distortion in % converted to dBc table
    conv fromΩ toΩ [step]
        Table converting between two dB(R Ω) values
    dbv R [step]
        dBV to dB(R Ω) table
    R dbv [step]
        dB(R Ω) to dBV table
    v
        Print voltages from 1 kV to 1 μV in steps of 1-2-5 and their equivalents in common dB
        measures (dBm(50 Ω), dBm(75 Ω), dBm(600 Ω), dBV)

Options
    - -s n  Step size for dB table [1]
    - -r R  Resistance reference in Ω 
    - -H    Print a manpage

dBm definitions (R in Ω, V in volts)
    dBm(R Ω) = 20*log(V/sqrt(R/1000))
    V = sqrt(R/1000)*10**(dBm/20) = C*10**(dBm/20)
        C = 0.7746 V for 600 Ω
        C = 0.2739 V for 75 Ω
        C = 0.2236 V for 50 Ω
    R = V**2*10**(-dBm/10 + 3)

Converting between different dBm voltage measures:
    dBm(R Ω) = dBm(S Ω) + C where C = 10*log(S/R)
        dBm(50 Ω) = dBm(600 Ω) + 10.8
        dBm(75 Ω) = dBm(600 Ω) + 9.0
        dBm(50 Ω) = dBm(75 Ω) + 1.8
    0 dBm(600 Ω) is 0.7746 V = sqrt(600/1000)
    0 dBm(50 Ω) is 0.2236 V = sqrt(50/1000)
    0 dBm(75 Ω) is 0.2739 V = sqrt(75/1000)

"""
if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    Header()
    print()
    if not d["-r"]:
        d["-r"] = 2
    if d["-d"]:
        Distortion()
    elif d["-5"]:
        dB50_to_dB600()
    elif d["-p"]:
        PercentDrop()
    elif d["-t"]:
        ConversionTable()
    elif d["-v"]:
        dBV_dBm600()
    else:
        dBmToVoltage(50, nl=True)
        dBmToVoltage(600, nl=True)
        dBVToVoltage()
