'''
Design a voltage reference from diodes and a resistor in series.  This script prints out the
measured voltage & current relationships of various diodes.
'''
 
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright © 2025 Don Peterson #∞copyright∞#
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
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from math import log as ln, exp
        from frange import frange
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from scipy.interpolate import interp1d
        from dpprint import PP
        from transpose import Transpose
        from columnize import Columnize
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        g.w = 10
        g.ind = " "*4
        ii = isinstance
        pp = PP()
if 1:   # Utility
    def GetColors():
        t.i = t.sky
        t.V = t.trql
        t.P = t.yel
        t.title = t.purl
        t.subtitle = t.whtl
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] op value1 [value2...]
          Print the voltage/current relationships for various diodes, gotten from measured values
          for a single diode and linear interpolation.  Functionality defined by the op argument:
            v       Print the voltage/current table for the selected diode
            i       Print the current/voltage table for the selected diode
          Additional values are i or v values evaluated at that value only.  Predicted values are
          approximate due to variations between diodes.
        Options:
            -a      Print a report for each diode type
            -d str  Select diode type (see list below, si1 == 1N4148 is default)
            -h      Print a manpage
            -n n    Number of digits in output [{d["-n"]}]
        '''))
        # Print diode types list
        print("Diode types:")
        dt = sorted(diodes.keys())
        for i in Columnize(dt, columns=5, col_width=15, indent=" "*4):
            print(i)
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Print report for all diodes
        d["-d"] = "si1"     # Selected diode
        d["-n"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:hn:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-d":     # Select diode
                # The -d option is a regex
                r = re.compile(a, re.I)
                matches = []
                for i in diodes:
                    mo = r.search(i)
                    if mo:
                        matches.append(i)
                if not matches: 
                    Error(f"{a!r} didn't match any diode name")
                elif len(matches) == 1:
                    d[o] = matches[0]
                else:
                    s = "\n"
                    Error(f"{a!r} had multiple matches: {s}{s.join(matches)}")
            elif o == "-n":     # Number of digits
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    Error(f"-n option's argument must be an integer between 1 and 15")
            elif o == "-t":     # Table 
                d[o] = int(a)
                if d[o] < 2:
                    Error(f"-t option's argument must be an integer >= 2")
            elif o == "-h":
                Usage()
        x = flt(0)
        x.N = d["-n"]
        x.rtz = True
        x.rtdp = True
        GetColors()
        return args
if 1:   # Doc
    def Manpage():
        print(dedent(f'''

        This script shows the measured current versus voltage relationships of on-hand diodes.
        Internally, the script uses your measured voltage/current relationships of the diodes you
        have on-hand.  Of course, it comes to you with the diodes that I have on-hand, but you'll
        want to measure you own diodes.  To do this, get a constant voltage DC power supply, put a
        suitable resistor across the diode, use DMMs to measure the diode's voltage and current,
        and generate a set of data for that diode.  I recommend measuring the current over a wide
        range.

        Since the diodes' behaviors will be stochastic, even for an set of diodes from a single
        manufacturing lot, the script's output is only an approximation, so you'll want to build,
        test, and tune a particular exemplar.  Remember the diodes' behaviors will also be
        temperature dependent:  a silicon diode has a temperature coefficient of about -2 mV/K.

        Example:  2 V reference

            I wanted a 2 V reference voltage in a circuit to provide an offset.  The voltage I'd
            put across this diode resistor stack would be 13.5 V (a float battery charger for
            lead-acid batteries).  A silicon PN junction diode has a voltage drop of about 0.6 V
            to 0.7 V at 1 mA.  Thus, three of these diodes should give 1.8 V to 2 V at 1 mA.  Fine
            tuning can be done by changing the series resistance.  (2 V)/3 is about 0.67 V, so run
            the script with the argument 'v'.  You'll see 0.65 V for a 1N4148 diode (the default)
            at 2.5 mA.  Thus, the design is three of these 1N4148 diodes across 13.5 V with a
            suitable resistor, giving 1.95 V across the 3 diodes.  We can now use the script with
            the 'i' argument to see better current resolution:  to get 2 V, we'd need a bit over
            4.5 mA of current.  Run the script with 'i 0.0045' and the voltage will be 668 mV.

            The diode voltage is 3(0.668) = 2.004 V and the resistor needs to drop 13.5 - 2 or 
            11.5 V.  With 4.5 mA of current, this is 11.5/4.5 kΩ or 2.5 kΩ.  I'd use my
            on-hand resistors of 1 kΩ and 1.5 kΩ; the power is 50 mW, so a 1/4 W resistor is fine.

            However, I also need an LED on the front panel of this battery charger to show that
            the power is on.  Run the script with the argument '-a' and you'll see the voltages
            for all the diodes.  A 2 V drop can be gotten with a 6.2 mA current through a 3mm
            yellow LED.  I chose this color because it wouldn't clash with the other 8 LEDs on the
            charger's panel.  I'll have 5 V for the microprocessor, so it needs a series resistor
            of 3/6.2 kΩ or 480 Ω.

        '''))
        exit(0)
if 1:   # Classes
    class Diode:
        def __init__(self, name, i_max_A, PIV, V_V, i_A, note=None):
            '''
            name        E.g. 1N4148
            i_max_A     Maximum current rating in A
            PIV         Peak inverse voltage rating
            V_V         V-i curve voltage data in V
            i_A         V-i curve current data in A
            '''
            self.name = name
            self.i_max_A = i_max_A
            self.PIV = PIV
            self.V_V = tuple(sorted(V_V))
            self.i_A = tuple(sorted(i_A))
            self.note = note
            # Invariants
            Assert(len(V_V) == len(i_A))
            # Generate the interpolation functions using scipy
            self.vi = interp1d(self.i_A, self.V_V)
            self.iv = interp1d(self.V_V, self.i_A)
        def __str__(self):
            if self.note:
                return self.name + f" ({self.note})"
            return self.name
        def __repr__(self):
            return f"Diode({self.name!r})"
        def i(self, V):
            'Return diode current in A for voltage V in V or None if out of range'
            try:
                return flt(self.iv(V))
            except ValueError:
                return None
        def V(self, i):
            'Return diode voltage in V for current i in A or None if out of range'
            try:
                return flt(self.vi(i))
            except ValueError:
                return None
        if 1:   # Properties
            @property
            def imax(self):
                return max(self.i_A)
            @property
            def imin(self):
                return min(self.i_A)
            @property
            def vmax(self):
                return max(self.V_V)
            @property
            def vmin(self):
                return min(self.V_V)
    diodes = {}
    def ConstructDiodeData():
        if 1:   # 1N4148
            # Raw data in mV and mA
            V_V = [flt(i)/1000 for i in (260, 320, 360, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900)]
            i_A = [flt(i) /1000 for i in (0.001, 0.002, 0.005, 0.01, 0.03, 0.1, 0.3, 0.8, 2.5, 8, 18, 40, 100, 200)]
            # Store the data in the diode container
            name = "si1"    # This was a 1N4148 diode
            D = diodes[name] = Diode(name, flt(0.3), flt(100), V_V, i_A, "1N4148 silicon diode")
        if 1:   # Unknown small signal Si diode
            # Columns:  current in mA, voltage in mV
            # Measured 19 Feb 2025, Aneng 870 for current, Aneng 8009 for voltage, HP E3615A DC power
            # supply, EDFM 1 W resistance box.  This resistor came from the junk box and looks exactly
            # like a 1N4148; however, it's 1 mA current is about 120 mV higher than the 1N4148 that I
            # measured a number of years ago.
            data = dedent('''
                0.001   421
                0.005   510
                0.01    544
                0.02    574.7
                0.05    612
                0.1     640
                0.2     666
                0.5     699
                1       721
                2       741
                5       768
                10      788
                20      807
                50      833
                100.64  852''')
            m = []
            for line in data.split("\n"):
                row = [flt(i) for i in line.split()]
                m.append(row)
            mt = Transpose(m)
            i_A = [flt(i/1000) for i in mt[0]]
            V_V = [flt(i)/1000 for i in mt[1]]
            name = "si2"
            i_max, PIV = "?", "?"
            D = Diode(name, i_max, PIV, V_V, i_A, "Small signal Si diode in junkbox")
            diodes[name] = D
        if 1:   # 3 mm LEDs
            # 3 mm LEDs measured voltage drops as function of current
            #   mA      yel      grn      red      blu      wht
            data = dedent('''
                0.5     1.85     1.87     1.81     2.62     2.60
                 1      1.90     1.91     1.84     2.67     2.64
                 2      1.94     1.94     1.87     2.74     2.70
                 5      1.99     1.98     1.93     2.86     2.80
                10      2.03     2.02     1.97     3.00     2.90
                15      2.06     2.04     2.01     3.10     2.98
                20      2.07     2.06     2.03     3.16     3.05
                25      2.09     2.07     2.05     3.21     3.11
                30      2.10     2.08     2.07     3.25     3.17''')
            # Generate a nested list
            m = []
            for line in data.split("\n"):
                row = [flt(i) for i in line.split()]
                m.append(row)
            mt = Transpose(m)
            i_A = [flt(i/1000) for i in mt[0]]      # Current
            V_V_yel = [flt(i) for i in mt[1]]       # yel voltage
            V_V_grn = [flt(i) for i in mt[2]]       # grn voltage
            V_V_red = [flt(i) for i in mt[3]]       # red voltage
            V_V_blu = [flt(i) for i in mt[4]]       # blu voltage
            V_V_wht = [flt(i) for i in mt[5]]       # wht voltage
            i_max, PIV = 0.05, 20
            name = "yel3"; diodes[name] = Diode(name, i_max, PIV, V_V_yel, i_A)
            name = "grn3"; diodes[name] = Diode(name, i_max, PIV, V_V_grn, i_A)
            name = "red3"; diodes[name] = Diode(name, i_max, PIV, V_V_red, i_A)
            name = "blu3"; diodes[name] = Diode(name, i_max, PIV, V_V_blu, i_A)
            name = "wht3"; diodes[name] = Diode(name, i_max, PIV, V_V_wht, i_A)
        if 1:   # 5 mm LEDs
            # 5 mm LEDs measured voltage drops as function of current
            #   mA      yel      grn      red      blu      wht
            data = dedent('''
                0.5     1.85     2.28     1.76     2.61     2.61
                 1      1.88     2.33     1.79     2.65     2.65
                 2      1.92     2.40     1.83     2.71     2.70
                 5      1.98     2.54     1.90     2.82     2.82
                10      2.05     2.68     1.98     2.95     2.96
                15      2.09     2.78     2.03     3.05     3.07
                20      2.12     2.86     2.07     3.13     3.14
                25      2.15     2.92     2.10     3.19     3.21
                30      2.16     2.98     2.13     3.25     3.26''')
            # Generate a nested list
            m = []
            for line in data.split("\n"):
                row = [flt(i) for i in line.split()]
                m.append(row)
            mt = Transpose(m)
            i_A = [flt(i/1000) for i in mt[0]]      # Current
            V_V_yel = [flt(i) for i in mt[1]]       # yel voltage
            V_V_grn = [flt(i) for i in mt[2]]       # grn voltage
            V_V_red = [flt(i) for i in mt[3]]       # red voltage
            V_V_blu = [flt(i) for i in mt[4]]       # blu voltage
            V_V_wht = [flt(i) for i in mt[5]]       # wht voltage
            i_max, PIV = 0.05, 20
            name = "yel5"; diodes[name] = Diode(name, i_max, PIV, V_V_yel, i_A)
            name = "grn5"; diodes[name] = Diode(name, i_max, PIV, V_V_grn, i_A)
            name = "red5"; diodes[name] = Diode(name, i_max, PIV, V_V_red, i_A)
            name = "blu5"; diodes[name] = Diode(name, i_max, PIV, V_V_blu, i_A)
            name = "wht5"; diodes[name] = Diode(name, i_max, PIV, V_V_wht, i_A)
        if 1:   # 1N5817G Schottky
            # Columns:  voltage in mV, current in mA
            data = dedent('''
                10.6    0.00253
                52.1    0.032
                102.8   0.2503
                137.4   0.9461
                172     3.2
                241.9   46.9
                265.4   106.2
                288.4   224
                300.4   328
                319.3   526
                337.7   786
                350.9   1003''')
            m = []
            for line in data.split("\n"):
                row = [flt(i) for i in line.split()]
                m.append(row)
            mt = Transpose(m)
            V_V = [flt(i)/1000 for i in mt[0]]
            i_A = [flt(i/1000) for i in mt[1]]
            name = "1N5817G"
            i_max, PIV = flt(1), flt(20)
            diodes[name] = Diode(name, i_max, PIV, V_V, i_A, "Schottky diode")
        if 1:   # 1N5818 Schottky
            # Columns:  voltage in mV, current in mA
            data = dedent('''
                15.34     0.00047
                63.16     0.00645
                101.38    0.02969
                156.36    0.2436
                203.3     1.2
                295.5     42.3
                322.3     104
                369       383
                397       680
                420       980''')
            m = []
            for line in data.split("\n"):
                row = [flt(i) for i in line.split()]
                m.append(row)
            mt = Transpose(m)
            V_V = [flt(i)/1000 for i in mt[0]]
            i_A = [flt(i/1000) for i in mt[1]]
            name = "1N5818"
            i_max, PIV = flt(1), flt(30)
            diodes[name] = Diode(name, i_max, PIV, V_V, i_A, "Schottky diode")
        if 1:   # 1N4004
            # Columns:  current in mA, voltage in mV
            data = dedent('''
                0.001       287.7
                0.002       327.9
                0.005       373.4
                0.01        405.1
                0.02        433.6
                0.05        467.3
                0.1         491.8
                0.2         516.8
                0.5         551.8
                1           580.0
                2           609.4
                5           648.8
                10          678.5
                20          707.1
                50          743.4
                100         768
                200         793
                500         820
                1000        840''')
            m = []
            for line in data.split("\n"):
                row = [flt(i) for i in line.split()]
                m.append(row)
            mt = Transpose(m)
            i_A = [flt(i/1000) for i in mt[0]]
            V_V = [flt(i)/1000 for i in mt[1]]
            name = "1N4004"
            i_max, PIV = flt(1), flt(400)
            diodes[name] = Diode(name, i_max, PIV, V_V, i_A)
        if 1:   # 1N4007
            # Columns:  current in mA, voltage in mV
            data = dedent('''
                0.001       286.6
                0.002       327.3
                0.005       374.2
                0.01        406.5
                0.02        437.3
                0.05        474.8
                0.1         503.0
                0.2         532.5
                0.5         573.2
                1           605.0
                2           637.3
                5           680.3
                10          712.7
                20          744.5
                50          785.1
                100         811
                200         833
                500         848
                1000        861''')
            m = []
            for line in data.split("\n"):
                row = [flt(i) for i in line.split()]
                m.append(row)
            mt = Transpose(m)
            i_A = [flt(i/1000) for i in mt[0]]
            V_V = [flt(i)/1000 for i in mt[1]]
            name = "1N4007"
            i_max, PIV = flt(1), flt(1000)
            diodes[name] = Diode(name, i_max, PIV, V_V, i_A)
    ConstructDiodeData()
if 1:   # Core functionality
    def PrintVoltageHeader(diode):
        t.print(f"{t.title}Voltage/current relationship for {diode.name} diode")
        t.print(f"{t.subtitle}  Max current = {diode.i_max_A} A, PIV = {diode.PIV}")
        if diode.note:
            t.print(f"  {t.subtitle}{diode.note}")
        t.print(f"{g.ind}{t.V}{'Voltage':>{g.w}s}"
                f"{g.ind}{t.i}{'Current':>{g.w}s}"
                f"{g.ind}{t.P}{'Power':>{g.w}s}")
        t.print(f"{g.ind}{t.V}{'-'*7:>{g.w}s}"
                f"{g.ind}{t.i}{'-'*7:>{g.w}s}"
                f"{g.ind}{t.P}{'-'*7:>{g.w}s}")
    def PrintVoltage(V, diode):
        i = diode.i(V)
        if i is None:
            return
        p = V*i
        sv = f"{V.engsi}V"
        si = f"{i.engsi}A"
        sp = f"{p.engsi}W"
        t.print(f"{g.ind}{t.V}{sv:>{g.w}s}"
                f"{g.ind}{t.i}{si:>{g.w}s}"
                f"{g.ind}{t.P}{sp:>{g.w}s}")
    def VoltageTable(diode):
        'Print a voltage table for the indicated diode instance'
        # Get the voltages in mV to print
        V = [1, 2, 3, 4, 5, 6, 7, 8, 9,
             10, 20, 30, 40, 50, 60, 70, 80, 90,
             100, 150, 200, 250, 300, 350, 400, 450, 500,
             600, 650, 700, 750, 800, 850, 900, 950]
        V += range(1000, 5001, 50)
        PrintVoltageHeader(diode)
        for v in V:
            PrintVoltage(flt(v/1000), diode)
    def PrintCurrentHeader(diode):
        t.print(f"{t.title}Current/voltage relationship for {diode.name} diode")
        t.print(f"  {t.subtitle}Max current = {diode.i_max_A} A, PIV = {diode.PIV}")
        if diode.note:
            print(f"  {t.subtitle}{diode.note}")
        t.print(f"{g.ind}{t.i}{'Current':>{g.w}s}"
                f"{g.ind}{t.V}{'Voltage':>{g.w}s}"
                f"{g.ind}{t.P}{'Power':>{g.w}s}")
        t.print(f"{g.ind}{t.i}{'-'*7:>{g.w}s}"
                f"{g.ind}{t.V}{'-'*7:>{g.w}s}"
                f"{g.ind}{t.P}{'-'*7:>{g.w}s}")
    def PrintCurrent(i, diode):
        v = diode.V(i)
        if v is None:
            return
        p = v*i
        sv = f"{v.engsi}V"
        si = f"{i.engsi}A"
        sp = f"{p.engsi}W"
        t.print(f"{g.ind}{t.i}{si:>{g.w}s}"
                f"{g.ind}{t.V}{sv:>{g.w}s}"
                f"{g.ind}{t.P}{sp:>{g.w}s}")
    def CurrentTable(diode):
        'Print a current table for the selected diode'
        # Get the currents in mA to print
        DI = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5,
              1, 2, 3, 4, 5, 6, 7, 8, 9,
              10, 20, 30, 40, 50, 60, 70, 80, 90,
              100, 150, 200, 250, 300, 350, 400, 450, 500,
              600, 650, 700, 750, 800, 850, 900, 950, 1000]
        DI += range(1100, 10000, 100)
        DI += range(10000, 100000, 1000)
        PrintCurrentHeader(diode)
        for I in DI:
            PrintCurrent(flt(I)/1000, diode)

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["-a"] and not args:
        for diode in diodes:
            VoltageTable(diodes[diode])
    elif len(args) == 1:
        if args[0].lower() == "v":
            func = VoltageTable
        elif args[0].lower() == "i":
            func = CurrentTable
        if d["-a"]:
            for diode in diodes:
                func(diodes[diode])
        else:
            func(diodes[d["-d"]])
    else:   # Print at selected values
        diode = diodes[d["-d"]]
        if args[0].lower() == "v":
            PrintVoltageHeader(diode)
            for V in args[1:]:
                PrintVoltage(flt(V), diode)
        else:
            PrintCurrentHeader(diode)
            for i in args[1:]:
                PrintCurrent(flt(i), diode)
