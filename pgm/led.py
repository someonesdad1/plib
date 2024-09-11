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
    # Design LED & resistor
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
    from color import C
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
    class g:
        pass
    g.n = C.norm
    g.a = C.yel
    g.p = C.lmag
    g.o = C.lgrn
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] color voltage
          Print the resistance to put in series with an LED to allow it to
          run at the given voltage at various currents.  Colors can be grn,
          red, yel, wht, blu.
        Options:
          -a      Show all values, even if above resistor's rated power
          -c      Don't print colors
          -d n    Set number of significant figures
          -3      Use 3 mm LED data (5 mm is default)
          -h      Print more detailed help and LED data used
          -p      Print tables for common resistor power ratings
          -w p    Resistor rated power in W [{d["-w"]}]
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Show all the current choices
        d["-c"] = False     # Turn off color printing
        d["-3"] = False     # Use 3 mm LED data
        d["-d"] = 3         # Number of significant digits
        d["-p"] = False     # Print for range of powers
        d["-w"] = 0.25      # Default resistor power in W
        try:
            opts, args = getopt.getopt(sys.argv[1:], "3acd:hpw:")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("3acp"):
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
        if d["-c"]:
            g.n = g.a = g.o = ""
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
        w = 70 
        print(f"{'LED Resistor Selection':^{w}s}")
        print(f"{'----------------------':^{w}s}")
        # Problem parameters
        w = 20 
        print(f"{'Operating voltage':{w}s} {voltage} V")
        print(f"{'LED color':{w}s} {GetColor(color)}")
        print(f"{'LED diameter':{w}s} {3 if d['-3'] else 5} mm")
        print(f"{g.p}{'Resistor power':{w}s} {ResistorPower(pwr)} W{g.n}")
        # Header
        w = 10
        print()
        print(" "*11, "---Voltage drops---")
        print(" "*13, end="")
        print(f"Diode     Resistor    -----{g.a}Actual{g.n}------     "
              f"-----{g.o}On-hand{g.n}-----")
        print(f"{'i, mA':^{w}s} {'Vd, V':^{w}s} {'Vr, V':^{w}s} ", end="")
        print(f"{'R, Ω':^{w}s} {'%power':^{w}s} ", end="")
        print(f"{'Ro, Ω':^{w}s} {'%power':^{w}s}")
        h = "-"*6
        for i in range(7):
            print(f"{h:^{w}s} ", end="")
        print()
        # Table
        for j in o:
            i, Vd, Vr, R, pct, Ro, pcto = j
            if pct > 100 and not d["-a"]:
                break
            print(f"{i!s:^{w}s} ", end="")
            print(f"{Vd!s:^{w}s} ", end="")
            print(f"{Vr!s:^{w}s} ", end="")
            print(f"{g.a}{R:^{w}s}{g.n} ", end="")
            print(f"{int(pct):6d}     ", end="")
            print(f"{g.o}{Ro:^{w}s}{g.n} ", end="")
            print(f"{int(pcto):6d}")
        if d["-p"]:
            print()
    def Solve(color, operating_voltage_V, resistor_power_rating_W):
        P = resistor_power_rating_W
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
        I.extend(range(1, 31, 1))
        # Make an array of [i, V, voltage - V, R, Ro, pct_pwr]
        o = []
        for curr in I:
            i = curr/1000                   # Current in A
            Vd = i2V(curr)                  # Voltage drop across diode
            Vr = operating_voltage_V - Vd   # Voltage drop across resistor
            if Vr > 0:
                R = Vr/i                    # Actual resistance needed
                Ro = FindClosest(R)         # Closest on-hand resistor
                power = i**2*R              # Actual resistor power
                pct = flt(100*power/P)      # Actual power percent
                if Ro is None:
                    o.append([curr, Vd, Vr, fp(R), pct, "-", "-"])
                else:
                    powero = i**2*Ro            # On-hand resistor power
                    pcto = flt(100*powero/P)    # On-hand power percent
                    o.append([curr, Vd, Vr, fp(R), pct, fp(Ro), pcto])
        PrintResults(color, operating_voltage_V, resistor_power_rating_W, o)
def Details():
    print(dedent('''
    Units:  mA for current, V for volts, Ω for resistance.  All non-DC values are RMS.

    The script's objective is to give you a range of operating currents for the LED that let you
    pick a single 1/4 W resistor from the on-hand values.  This is specific to my inventory of
    resistors, so you'll want to populate the resistors.py script with your own values.

    This task is analytically problematic because of the nonlinear nature of the diode's current
    versus voltage characteristics (see https://en.wikipedia.org/wiki/Diode_modelling for
    details).  However, a piecewise linear model is practical and is how this script works (by
    linear interpolation in the tables given below).

    The columns printed out in the script's report are:

      i         RMS current through the resistor and diode
      Vd        RMS voltage drop across the diode, interpolated from the measured data below
      Vr        RMS voltage drop across the resistor.  This is for the actual calculated
                resistance value R, not the on-hand resistance Ro.
      R         Calculated resistance needed
      Ro        Closest on-hand resistance to R
      %power    % of resistor's rated power run at the indicated current

    Comments
    --------
      The script's output contains estimated values; they do not reflect the stochastic
      variability of the diodes' characteristics nor any measurement uncertainties.  For a
      critical application, you'll want to measure such things yourself.  In addition, the
      script's output is dependent on the measured values of my supply of LEDs purchased in 2017
      (see below).

      I rarely run these diodes over 10 mA.  Many panel annunciator tasks work for indoor use at 1
      to 5 mA.

      A common use case is to choose a resistor for one of these LEDs to run at AC line voltage.
      Since my line voltage is 120 V RMS and I also design for output from one of my Variacs which
      can be up to 140 V, I conservatively pick a resistor to run at 150 V RMS.  With 1/4 W
      resistors, this usually means running at 1 mA or less.  To run at 1 mA, the needed resistor
      is typically 147 kΩ, independent of the LED color because most of the voltage is dropped
      across the resistor.

      A handy tool for the bench is to put five of the LEDs in series, one each of yellow, green,
      red, blue, and white.  If you look at the table data below, you'll see these strings of LEDs
      will run at 11 to 14 V.  You can hook up the strings to a DC power supply and adjust the
      voltage to see what the LEDs look like at the same current.  

    Measured LED properties
    -----------------------

      The output of this script is dependent on the measured values of 3 and 5 mm LEDs purchased
      from banggood in 2017:

      3 mm LEDs received 21 Jul 2017, 750 pieces of yellow, green, red, blue, and white, 20 mA,
      $7.45 delivered, https://www.banggood.com/750-Pcs-3mm-LED-Diode-Yellow-Red-Blue-Green-\\
      White-Assortment-Light-DIY-Kit-p-1122409.html?rmmds=search

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
  
      5 mm LEDs received 21 Jul 2017, 1000 pieces of yellow, green, red, blue, and white, 20 mA,
      $12.88 delivered, https://www.banggood.com/1000Pcs-5-Colors-5mm-F5-Ultra-Bright-Round-LED-\\
      Diode-Kit-p-1059729.html?rmmds=search

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

      Green is surprisingly bright at 1 mA; yellow is disappointing.  Output in candela at 20 mA
      for 5 mm LEDs:
          Red     2.5-3         600-635 nm
          Yellow  15-20         588-590 nm
          Blue    6-8           460-465 nm
          Green   15-18         567-570
          White   6-8           8 kK color temperature
      I have run these 5 mm LEDs up to 100 mA where they are too bright to look at directly.
      Yellow should probably only be run to 80 mA.

      A spot check of some LEDs in my junkbox gave with a 12 V power supply and a 1 kohm resistor:
                Measured                Script's prediction
        Color   i, mA   Vd              i, mA   Vd
        grn     9.4     2.675           9       2.65
        grn ‡   10.1    1.994           9       2.65
        wht     9.1     2.997           9       2.93
        yel     10.0    2.067           10      2.05
        red ‡   10.4    1.698           10      1.98
        blu     9.1     3.015           9       2.92
        wht     9.2     2.919           9       2.93

        ‡ Probably older LEDs, as they didn't have the bright output of the banggood LEDs

      Conclusion:  The script will probably estimate things to within 5% to 10%, which should be
      good enough for casual work.

      Voltage for an RGB LED, sample of one 24 Jun 2023
           mA    Red      Green      Blue
          0.5   1.75       2.30      2.50
           1    1.78       2.37      2.54
          2.5   1.84       2.50      2.60
           5    1.88       2.68      2.68
          7.5   1.93       2.80      2.74
          10    1.96       2.91      2.81
          20    2.06       3.22      3.00
          25    2.09       3.33      3.08
          30    2.12       3.42      3.14
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
