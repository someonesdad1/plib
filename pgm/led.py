'''
Allows a design of LED and resistor given the power rating of the resistor
you want to use
'''
 
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
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
if 1:   # Standard imports
    import getopt
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx
    from pprint import pprint as pp
if 1:   # Custom imports
    from wrap import dedent
    from get import GetNumbers as GN
    from interpolate import LinearInterpFunction
    from frange import frange
    from f import flt
    from resistors import FindClosest
    from fpformat import FPFormat
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    # LED characteristics
    i_mA = GN("0.5 1 2 5 10 15 20 25 30")
    LED5 = {
        # V in V array, i in mA array
        "yel": GN("1.85 1.88 1.92 1.98 2.05 2.09 2.12 2.15 2.16"),
        "grn": GN("2.28 2.33 2.40 2.54 2.68 2.78 2.86 2.92 2.98"),
        "red": GN("1.76 1.79 1.83 1.90 1.98 2.03 2.07 2.10 2.13"),
        "blu": GN("2.61 2.65 2.71 2.82 2.95 3.05 3.13 3.19 3.25"),
        "wht": GN("2.61 2.65 2.70 2.82 2.96 3.07 3.14 3.21 3.26"),
    }
    LED3 = {
        # V in V array, i in mA array
        "yel": GN("1.85 1.90 1.94 1.99 2.03 2.06 2.07 2.09 2.10"),
        "grn": GN("1.87 1.91 1.94 1.98 2.02 2.04 2.06 2.07 2.08"),
        "red": GN("1.81 1.84 1.87 1.93 1.97 2.01 2.03 2.05 2.07"),
        "blu": GN("2.62 2.67 2.74 2.86 3.00 3.10 3.16 3.21 3.25"),
        "wht": GN("2.60 2.64 2.70 2.80 2.90 2.98 3.05 3.11 3.17"),
    }
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] color voltage
          The script will print out the resistance to put in series with an
          LED to allow it to run at the given voltage at various currents.
          Colors can be grn, red, yel, wht, blu.
        Options:
            -a      Show all values, even if above resistor's rated power
            -d n    Set number of significant figures
            -3      Use 3 mm LED data (5 mm is default)
            -h      Print more detailed help and LED data used
            -p      Print tables for common resistor power ratings
            -w p    Resistor rated power in W [{d["-w"]}]
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Show all the current choices
        d["-3"] = False     # Use 3 mm LED data
        d["-d"] = 3         # Number of significant digits
        d["-p"] = False     # Print for range of powers
        d["-w"] = 0.25      # Default resistor power in W
        try:
            opts, args = getopt.getopt(sys.argv[1:], "3ad:hpw:")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("3ap"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o in ("-w",):
                try:
                    d["-w"] = flt(a)
                    if d["-w"] <= 0:
                        raise ValueError()
                except ValueError:
                    Error("-w option's argument must be > 0")
            elif o in ("-h", "--help"):
                Details()
        if len(args) != 2:
            Usage()
        x = flt(0)
        x.n = d["-d"]
        x.rtz = x.rtdp = True
        return args
if 1:   # Core functionality
    def GetColor(color):
        'Return needed color string'
        c = color.lower()
        if c in ("r", "re", "red"):
            return "red"
        elif c in ("g", "gr", "gre", "gree", "green", "grn"):
            return "grn"
        elif c in ("b", "bl", "blu", "blue"):
            return "blu"
        elif c in ("y", "ye", "yel", "yell", "yello", "yellow"):
            return "yel"
        elif c in ("w", "wh", "wht", "whi", "whit", "white"):
            return "wht"
    def ResistorPower(pwr):
        'Return a fraction string if suitable'
        if pwr == 0.125:
            return "1/8"
        elif pwr == 0.25:
            return "1/4"
        elif pwr == 0.5:
            return "1/2"
        elif pwr == 1:
            return "1"
        elif pwr == 2:
            return "2"
        elif pwr == 5:
            return "5"
        else:
            return str(pwr)
    def PrintResults(color, operating_voltage_V, resistor_power_rating_W, o):
        w = 60 
        print(f"{'LED Resistor Selection':^{w}s}")
        print(f"{'----------------------':^{w}s}")
        print()
        # Problem parameters
        w = 20 
        print(f"{'Operating voltage':{w}s} {voltage} V")
        print(f"{'LED color':{w}s} {GetColor(color)}")
        print(f"{'LED diameter':{w}s} {3 if d['-3'] else 5} mm")
        print(f"{'Resistor power':{w}s} {ResistorPower(pwr)} W")
        # Header
        w = 10
        print(" "*53, "% Resistor")
        print(" "*13, end="")
        print("Diode     Resistor    Actual    On-hand     rated")
        print(f"{'i, mA':^{w}s} {'Vd, V':^{w}s} {'Vr, V':^{w}s} ", end="")
        print(f"{'R, Ω':^{w}s} {'Ro, Ω':^{w}s} {'power':^{w}s} ")
        h = "-"*6
        for i in range(6):
            print(f"{h:^{w}s} ", end="")
        print()
        # Table
        for j in o:
            i, Vd, Vr, R, Ro, pct = j
            if pct > 100 and not d["-a"]:
                break
            print(f"{i!s:^{w}s} ", end="")
            print(f"{Vd!s:^{w}s} ", end="")
            print(f"{Vr!s:^{w}s} ", end="")
            print(f"{R:^{w}s} ", end="")
            print(f"{Ro:^{w}s} ", end="")
            print(f"{int(pct):6d}")
        if d["-p"]:
            print()
    def Solve(color, operating_voltage_V, resistor_power_rating_W):
        # Formatting tool
        FP = FPFormat(num_digits=3)
        fp = FP.engsi
        FP.trailing_decimal_point(False)
        # Set up interpolation functions
        if d["-3"]:
            V = LED3[GetColor(color)]
        else:
            V = LED5[GetColor(color)]
        V2i = LinearInterpFunction(V, i_mA)
        i2V = LinearInterpFunction(i_mA, V)
        # Define currents to print out
        I = list(frange("0.5", "1", "0.1"))
        I.extend(range(1, 21, 1))
        # Make an array of [i, V, voltage - V, R, Ro, pct_pwr]
        o = []
        for i in I:
            Vd = i2V(i)                     # Voltage drop across diode
            Vr = operating_voltage_V - Vd   # Voltage drop across resistor
            if Vr > 0:
                R = Vr/(i/1000)
                Ro = FindClosest(R)
                power = (i/1000)**2*R
                pct = flt(100*power/pwr)
                if Ro is None:
                    o.append([i, Vd, Vr, fp(R), "-", pct])
                else:
                    o.append([i, Vd, Vr, fp(R), fp(Ro), pct])
        PrintResults(color, operating_voltage_V, resistor_power_rating_W, o)
def Details():
    print(dedent('''
    All units are SI and RMS.

    This script uses the measured properties of my on-hand LEDs to estimate
    the needed series resistance for a given operating voltage across the
    diode and resistor and current through them both.  The estimates are
    made using linear interpolation of the table data given below.

    The basic objective of the script is to give you a range of operating
    currents for the LED that let you pick a single 1/4 W resistor from the
    on-hand values.  This is specific to my inventory of resistors, so
    you'll want to populate the resistors.py script with your own values.

    The columns printed out in the script's report are:

      i, mA
          This is the RMS current through the resistor and diode.
      Vd
          Voltage drop across the diode, interpolated from the measured
          data below.
      Vr
          Voltage drop across the resistor.  This is for the actual
          calculated resistance value R, not the on-hand resistance Ro.
      R
          Calculated resistance needed.
      Ro
          Closest on-hand resistance to R.
      % Resistor rated power
          % of resistor's rated power if a resistor of value R was run at
          the indicated current.  Note results will be different for the
          on-hand resistance.  You can scale the percentage rated power
          using Ro/R.

    Comments
    --------

      These are estimated values and do not reflect the stochastic
      variability of the diodes' characteristics.  For a critical
      application, you'll want to measure things yourself.  The script's
      intent is to get you into the ballpark.

      A common use case of mine is to choose a resistor for one of these
      LEDs to run at AC line voltage.  Since my line voltage is almost
      always 119 to 120 V RMS and I also design for output from one of my
      Variacs which can be up to 140 V, I conservatively pick a resistor to
      run at 150 V RMS.  With 1/4 W resistors, this usually means running
      at 1 mA or less.

      When fiddling with LEDs, a current source with a 10-turn pot for
      controlling the current is very helpful for measuring and
      characterizing.  An excellent current source can be made with an
      LM285 voltage reference, an op amp like the LM324, a 10-turn pot,
      suitable shunt resistors, and a MOSFET transistor like the IRF3205.
      For the bench, use a 12 V wall wart for power.  See
      https://someonesdad1.github.io/hobbyutil/elec/CurrentSource.pdf for
      a battery-operated example.

    Measured LED properties
    -----------------------

    The output of this script is dependent on the measured values of 3 and
    5 mm LEDs purchased from banggood in 2017:

      3 mm LEDs received 21 Jul 2017, 750 pieces of yellow, green, red,
      blue, and white, 20 mA, $7.45,
      https://www.banggood.com/750-Pcs-3mm-LED-Diode-Yellow-Red-Blue-Green-White-Assortment-Light-DIY-Kit-p-1122409.html?rmmds=search
      Measured voltage drops as function of current:
          mA     Yellow   Green     Red      Blue    White
          0.5     1.85     1.87     1.81     2.62     2.60
           1      1.90     1.91     1.84     2.67     2.64
           2      1.94     1.94     1.87     2.74     2.70
           5      1.99     1.98     1.93     2.86     2.80
          10      2.03     2.02     1.97     3.00     2.90
          15      2.06     2.04     2.01     3.10     2.98
          20      2.07     2.06     2.03     3.16     3.05
          25      2.09     2.07     2.05     3.21     3.11
          30      2.10     2.08     2.07     3.25     3.17
  
      5 mm LEDs received 21 Jul 2017, 1000 pieces of yellow, green, red,
      blue, and white, 20 mA, $12.88,
      https://www.banggood.com/1000Pcs-5-Colors-5mm-F5-Ultra-Bright-Round-LED-Diode-Kit-p-1059729.html?rmmds=search
      Measured voltage drops as function of current:
          mA     Yellow   Green     Red      Blue    White
          0.5     1.85     2.28     1.76     2.61     2.61
           1      1.88     2.33     1.79     2.65     2.65
           2      1.92     2.40     1.83     2.71     2.70
           5      1.98     2.54     1.90     2.82     2.82
          10      2.05     2.68     1.98     2.95     2.96
          15      2.09     2.78     2.03     3.05     3.07
          20      2.12     2.86     2.07     3.13     3.14
          25      2.15     2.92     2.10     3.19     3.21
          30      2.16     2.98     2.13     3.25     3.26
      Green is surprisingly bright at 1 mA; yellow is disappointing.
      Output in candela given as:
          Red     2.5-3
          Yellow  15-20
          Blue    6-8
          Green   15-18
          White   6-8
      I have run these 5 mm LEDs up to 100 mA where they are too bright to
      look at directly.  Yellow should probably only be run to 80 mA.
    '''))
    exit(0)
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    color, voltage = args[0], flt(args[1])
    if d["-p"]:
        for pwr in (1/8, 1/4, 1/2, 1, 2, 5):
            Solve(color, voltage, pwr)
    else:
        pwr = d["-w"]
        Solve(color, voltage, pwr)
    print("\nScale % rated power by Ro/R")
