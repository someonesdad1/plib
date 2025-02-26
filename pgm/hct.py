"""
Plot the electrical characteristics of the high current transformer.

    - Temperature rise as a function of secondary current
    - Primary/secondary current & voltage for secondary current ≤ 200 A

    - Electrical measurements made 20 Aug 2024
        - All AC measurements are RMS
        - Tubing short used to facilitate use with clamp-on ammeter
        - TO92 transformer used for 20 V and 40 V applied to HCT primary windings
            - Driven by 10 A Variac
        - HCT Primary
            - Voltage measured by Aneng 8009
            - Current measured by Zotek ZT111 (same as Aneng 8009)
        - HCT Secondary
            - Voltage measured by Aneng 870
            - Current measured by Kaiweets HT206D clamp-on ammeter, either 60 or 600 A range
        - Protocol was to limit maximum current to 200 A except for a quick determination of the
          maximum current gotten with the Variac at 100%.  Line voltage is typically 118 V.
            - Qualitative check was made by feeling the temperature of the tubing short

"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Program description string
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from collections import deque, namedtuple
        from pathlib import Path as P
        from pprint import pprint as pp
        import getopt
        import os
        import re
        import sys
    if 1:  # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from columnize import Columnize
        from u import u

        if 0:
            import debug

            debug.SetDebugger()
    if 1:  # Global variables

        class G:
            pass

        g = G()
        g.dbg = False
        ii = isinstance
if 1:  # Data
    winding_data = {
        # Left to right, the data fields are
        #   Primary current in mA
        #   Primary voltage in V
        #   Secondary current in A
        #   Secondary voltage in mV
        5: """69.8    1.869    10.1    4.35
              139.7   3.734    20.2    8.68
              357.5   9.589    52      22.48
              697.2   18.78    100.9   44.4
              1038    28.14    150.1   66.72
              1424    38.7     206.5   92.09""",
        4: """92.4    1.352    10      4.492
              183.1   2.687    19.9    8.984
              480.3   7.066    52.1    23.63
              942     13.88    101.5   46.66
              1385    20.55    150     69.58
              1861    27.66    200.8   94.51""",
        3: """160.4   1.059    11.5    5.444
              309.8   2.049    22.4    10.566
              698.2   4.638    50.3    23.99
              1423    9.478    102.2   49.22
              2093    13.98    150.4   73.23
              2835    18.99    203.5   99.56""",
        2: """251.1   0.5658   10.7    4.9
              481     1.086    20.5    9.452
              1205    2.727    51.5    23.78
              2370    5.374    100.8   47.06
              3549    8.091    150.6   71.8
              4781    10.88    202.4   96.9""",
        1: """ 552.1  0.3854   11.96   6.035
               1037   0.7292   22.73   11.48
               2330   1.642    50.9    25.96
               4618   3.259    100.5   51.83
               6918   4.886    150.6   78.23
               9430   6.659    204     107.4""",
    }
    # Convert to numerical arrays
    data = {}
    for w in winding_data:
        o = []
        for line in winding_data[w].split("\n"):
            s = [flt(i) for i in line.split()]
            o.append([flt(i) for i in line.split()])
        data[w] = o
if 1:  # Utility

    def GetColors():
        t.err = t("redl")
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        # Colors for voltages needed
        t.over = t.redl
        t.warn = t.ornl
        t.high = t.magl
        t.medium = t.purl
        t.low = t.trql

    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )

    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Manpage():
        print(
            dedent(f"""

        This script is for the transformer made by Electronic Corporation of America.  The
        markings on the transformer are

            HD4573--Rev 7
            115 V
            Part no. E.C.A. 10003

        This transformer has a mass of 13.1 kg and a size of 146x135x180 mm.  I assume it was made
        in the 1940's or 1950's at the latest, possibly earlier.  The insulation between the
        secondary winding is paper.  The secondary is made from copper sheet 2 mm thick and 45 mm
        wide; the cross sectional area is 90 mm², which is 6% larger than 3/0 AWG wire (10.4 mm in
        diameter).  It is labeled for 115 V input and has 5 primary winding taps labeled 1 through
        5.  The no-load output voltages for each primary terminal are (with 120 V on the primary
        winding)

         Terminal   Voltage     Ratio, %
            1         5.65        4.71
            2         2.91        2.43
            3         1.70        1.42
            4         1.13        0.94
            5         0.85        0.71
        
        The transformer is intended to provide high currents at low voltages.  I've measured its
        output current with a shorted secondary up to 609 A, as this is the largest value
        measureable by my Kaiweets HT206D clamp-on ammeter.

        Maximum allowed current is determined by the temperature rise of the transformer because
        of the Joule heating in the windings.  At 200 A, the measured temperature rise
        above ambient was 38 °C after 2.7 hours.  At 225 A, the temperature rise was 58 °C after
        1.3 hours at that current.  This current level would result in a transformer temperature
        of over 80 °C, which is too much in my opinion.  For continuous operation, I've decided
        that 200 A is the maximum current to be used.  The transformer is capable of withstanding
        larger currents for short periods of time (quantification will have to wait until I
        construct a suitable current transformer for the secondary).

        Operational parameters were measured for each terminal at nominal currents of 10, 20, 50,
        100, 150, and 200 A.  A short of 129 μΩ made from aluminum tubing was used as the load.
        The parameters measured were current and voltage for the primary and secondary.  The
        standard deviation of the voltage, current, and power ratios of the primary and secondary
        were between 0.2% and 1.1% of the mean ratio for each terminal.

        These measured data were plotted and were linear.  This resulted in linear regressions
        (all R² values > 0.999) that predict the primary voltage needed to get a desired current
        across this 129 μΩ short.  These regressions are used for the predictions of this script.
        They are intended to be estimates to get you into the ballpark for a particular load.

        Examples
        --------

        1.  What primary voltage to I need for 95 A?  With 95 as the script's argument, the output
            is
                For current = 95 A, use the following primary voltages:
                  Terminal 1    3.13 V
                  Terminal 2    5.15 V
                  Terminal 3    8.94 V
                  Terminal 4    13.3 V
                  Terminal 5    17.7 V

        2.  I have a 200 A Westinghouse shunt that belonged to my father-in-law.  I've measured
            its resistance as 501.0 μΩ using a 19.00 A DC current and an HP 6 digit voltmeter.  If
            I want to test the voltage drop of this shunt at 200 A (it's specified to have a 100
            mV voltage drop at 200 A), the script's output for the arguments '200 501e-6'  says I
            should use terminal 5 and apply 37.3 V to the primary.

            I connected the shunt to the transformer with two pieces of 0 AWG battery cable about
            350 mm long.  I set the Variac's output to 37.4 V and put an Aneng 8009 on the shunt's
            output to measure the shunt's voltage drop.  When turned on, the clamp-on ammeter read
            121.6 A and the voltage drop was 60.66 mV, 60% of what was wanted.  I adjusted the
            current to read 201.0 A, but the Aneng 8009 would not measure the voltage for some
            reason (even after switching to the normal voltage range).  I switched to the Aneng
            870 and it read 99.62 mV.  This 200 A current flowed for about 30 s to 40 s over two
            experiments and there was noticeable heating of the shunt's element -- my finger touch
            estimates a 5 to 10 °C rise.  The script's output predicts 20 W being dissipated in
            the shunt, accounting for the mild heating.

            Assuming the shunt is exactly 100 mV for 200 A, the measured current as judged by the
            shunt is 200(0.9961) or 199.2 A.  Using the DC calibrated 501 μΩ, the estimated
            current is i = V/R = 99.62e-3/501e-6 or 198.8 A.  The shunt's value is within about 1%
            of the Kaiweets clamp-on ammeter's measurement, good enough for this check.  

            The script's prediction was wrong, as it assumes a 129 μΩ load.  If we correct the
            predicted voltage by (501/129)37.3, we get 144 V.  The measured Variac output at 201 A
            was 60.7 V, so things don't scale like I'd expect.

        """)
        )

    def Usage(status=0):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] current_A [resistance_Ω]
          Display the needed primary voltage for a desired shorted secondary current for the high
          current transformer.  If the resistance is given, then the terminal number and primary
          voltage that should be used is printed.
        Options:
            -d n    Number of digits in numbers
            -h      Print a manpage
            -r      Display the raw measured data
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-d"] = 2  # Number of significant digits
        d["-r"] = False  # Display raw data
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:hr", "--debug")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("r"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o == "-h":
                Usage()
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an unhandled exception
                import debug

                debug.SetDebugger()
        GetColors()
        return args


if 1:  # Core functionality

    def PrintRawData():
        "Print the raw data"
        x = flt(0)
        x.N = d["-d"]
        x.rtz = True
        x.rtdp = True
        column_labels = ("i, A", "V, V", "i, A", "V, mV")
        w0, wc = 10, 10
        t.print(f"{t.yell}High current transformer raw data 21 Aug 2024")
        print("  Measurements made with aluminum tubing short of 129 μΩ")
        print("    Primary,   current = Zotek ZT111 (== Aneng 8009)")
        print("    Primary,   voltage = Aneng 8009")
        print("    Secondary, current = Kaiweets HT2006D clamp-on ammeter")
        print("    Secondary, voltage = Aneng 870")
        print()
        t.print(
            f"  {t.ornl}{' ' * (w0 + wc // 2)}Primary{' ' * (w0 // 2 + wc // 2 + 2)}Secondary"
        )
        for w in sorted(data):
            print(f"{t.sky}{f'Winding {w}':{w0}s}{t.ornl}", end="")
            for label in column_labels:
                print(f"{label:^{wc}s}", end="")
            t.print()
            for line in data[w]:
                print(f"{' ' * w0}", end="")
                for count, item in enumerate(line):
                    if not count:
                        item /= 1000
                    print(f"{item!s:^{wc}s}", end="")
                print()

    def GetColor(primary_voltage):
        "Return color escape code string for given voltage"
        if primary_voltage < 0:
            raise ValueError("primary_voltage must be zero or positive")
        if primary_voltage > 115:
            return t.over
        else:
            return t.N

    def GetVoltage(current, terminal):
        "Calculate needed voltage given current in A and terminal"
        if not ii(terminal, int):
            raise TypeError("terminal must be an int")
        if terminal not in (1, 2, 3, 4, 5):
            raise ValueError("terminal must 1, 2, 3, 4, or 5")
        if current < 0:
            raise ValueError("current must be ≥ 0")
        model = {
            1: (0.0335, -0.0549),
            2: (0.0549, -0.0689),
            3: (0.0950, -0.0874),
            4: (0.1405, -0.0885),
            5: (0.1861, 0.0541),
        }
        m, b = model[terminal]
        return flt(m * current + b)

    def CalculateVoltage(current):
        print(f"For current = {current} A, use the following primary voltages:")
        for terminal in (1, 2, 3, 4, 5):
            v = GetVoltage(current, terminal)
            if v <= 0:
                print(f"  Terminal {terminal}    ~ 0 V")
            else:
                t.print(f"  Terminal {terminal}    {GetColor(v)}{v} V")

    def CalculateVoltageFromResistance(current, resistance):
        print(f"For current = {current} A and resistance {resistance} Ω:")
        v = []
        for terminal in (1, 2, 3, 4, 5):
            v.append((terminal, GetVoltage(current, terminal)))
        # Find the lowest voltage needed for the desired resistance
        for terminal, voltage in reversed(v):
            i = voltage / resistance
            if i >= current:
                print(
                    f"  Use terminal {t.ornl}{terminal}{t.n} with {t.trql}{voltage}{t.n} V on the primary"
                )
                p = current**2 * resistance
                t.print(f"  Resistor power is {t.denl}{p} W")
                return
        t.print(f"  {t.err}Cannot reach desired current {current} with {resistance} Ω")


if 1:  # Classes
    # If you know any one of the primary or secondary current or voltage, you can predict the
    # other three values by knowing the ratios and regressions.
    OperationPoint = namedtuple("OperationPoint", "i_p i_s V_p V_s P_p P_s")

    class Winding:
        "Capture experimental data about a winding"

        def __init__(self, terminal):
            if not ii(terminal, int):
                raise TypeError("terminal must be an int")
            if terminal not in (1, 2, 3, 4, 5):
                raise ValueError("terminal must 1, 2, 3, 4, or 5")
            self.terminal = terminal
            # Summary of experimental current, voltage, and power ratios
            data = {  # Map terminal number to ratios
                1: (  # Tuple is ratio mean, ratio stdev
                    (21.8e-3, 0.11),  # Current:  (sec in A)/(pri in A)
                    (0.01588, 1.74e-4),  # Voltage:  (sec in V)/(pri in V)
                    (0.346, 0.0035),  # Power:  (sec in W)/(pri in W)
                ),
                2: (  # Tuple is ratio mean, ratio stdev
                    (42.5e-3, 0.14),  # Current:  (sec in A)/(pri in A)
                    (0.00877, 9.8e-5),  # Voltage:  (sec in V)/(pri in V)
                    (0.373, 0.0031),  # Power:  (sec in W)/(pri in W)
                ),
                3: (  # Tuple is ratio mean, ratio stdev
                    (71.9e-3, 0.22),  # Current:  (sec in A)/(pri in A)
                    (0.00519, 4.2e-5),  # Voltage:  (sec in V)/(pri in V)
                    (0.373, 0.0029),  # Power:  (sec in W)/(pri in W)
                ),
                4: (  # Tuple is ratio mean, ratio stdev
                    (108.2e-3, 0.35),  # Current:  (sec in A)/(pri in A)
                    (0.00336, 3.4e-5),  # Voltage:  (sec in V)/(pri in V)
                    (0.364, 0.0033),  # Power:  (sec in W)/(pri in W)
                ),
                5: (  # Tuple is ratio mean, ratio stdev
                    (144.8e-3, 0.33),  # Current:  (sec in A)/(pri in A)
                    (0.00235, 2.3e-5),  # Voltage:  (sec in V)/(pri in V)
                    (0.341, 0.0035),  # Power:  (sec in W)/(pri in W)
                ),
            }
            # Set up our ratios as secondary/primary
            self.i_ratio, self.i_ratio_s = data[terminal][0]
            self.V_ratio, self.V_ratio_s = data[terminal][1]
            self.P_ratio, self.P_ratio_s = data[terminal][2]

        def PriCurrent(self, current_A):
            "Return OperationPoint for primary current in A"
            i_pri = flt(current_A)
            i_sec = flt(i_pri * self.i_ratio)
            V_pri = flt(GetVoltage(i_sec, self.terminal))
            V_sec = flt(V_pri * self.V_ratio)
            P_pri = flt(V_pri * i_pri)
            P_sec = flt(V_sec * current_A)
            op = OperationPoint(i_pri, current_A, V_pri, V_sec, P_pri, P_sec)
            return op

        def SecCurrent(self, current_A):
            "Return OperationPoint for secondary current in A"
            i_sec = flt(current_A)
            V_pri = flt(GetVoltage(current_A, self.terminal))
            V_sec = flt(V_pri * self.V_ratio)
            i_pri = flt((i_sec / self.i_ratio) / 1000)
            P_pri = flt(V_pri * i_pri)
            P_sec = flt(V_sec * current_A)
            op = OperationPoint(i_pri, current_A, V_pri, V_sec, P_pri, P_sec)
            return op

        def PriVoltage(self, voltage_V):
            "Return OperationPoint for primary voltage in V"

        def SecVoltage(self, voltage_V):
            "Return OperationPoint for secondary voltage in V"

    x = Winding(5)
    # Data for 100.9 A for secondary gave:
    #       0.0442 V on secondary
    #       0.6972 A on primary
    #       18.78 V on primary
    if 1:  # Given secondary current
        print("Given secondary current")
        op = x.SecCurrent(100.9)
        print(f"    Primary   current = {op.i_p} A")
        print(f"    Primary   voltage = {op.V_p} V")
        print(f"    Primary   power   = {op.P_p} W")
        print(f"    Secondary current = {op.i_s} A")
        print(f"    Secondary voltage = {op.V_s * 1000} mV")
        print(f"    Secondary power   = {op.P_s} W")
    if 1:  # Given primary current
        print("Given primary current")
        op = x.PriCurrent(0.6972)
        print(f"    Primary   current = {op.i_p} A")
        print(f"    Primary   voltage = {op.V_p} V")
        print(f"    Primary   power   = {op.P_p} W")
        print(f"    Secondary current = {op.i_s} A")
        print(f"    Secondary voltage = {op.V_s * 1000} mV")
        print(f"    Secondary power   = {op.P_s} W")
    exit()


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if d["-r"]:
        PrintRawData()
    if len(args) == 1:
        current = flt(args[0])
        CalculateVoltage(current)
    elif len(args) == 2:
        current = flt(args[0])
        resistance = flt(args[1])
        CalculateVoltageFromResistance(current, resistance)
    else:
        Usage()
