'''
Design an ad hoc voltage reference from diodes
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
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
        pp = PP()
if 1:   # Utility
    def GetColors():
        t.err = t.redl
        t.i = t.orn
        t.V = t.grn
        t.diode = t.magl
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
          Functionality defined by the op argument:
            v       Print the predicted voltage(s) for the given current(s)
            i       Print the predicted current(s) for the given voltage(s)
            ref     Design a voltage reference using diodes
        Options:
            -d num  Select diode type
                        0   1N4148 [default]
            -h      Print a manpage
            -n n    Number of digits in output [{d["-n"]}]
            -t n    Print a voltage or current table with n points for the diode
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 0         # Which diode to model
        d["-n"] = 3         # Number of significant digits
        d["-t"] = None      # Print table with indicated number of points
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:hn:t:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-d":     # Select diode
                d[o] = int(a)
                if d[o] < 0:
                    Error(f"-d option's argument must be an integer >= 0")
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
        return args
if 1:   # Doc
    def Manpage():
        print(dedent(f'''

            This tool uses measured current versus voltage curves of on-hand diodes to design a
            voltage reference.  Your input is the operating voltage and the desired voltage.  The
            script will select a set of diodes and a resistor to approximate the desired output
            voltage.  The resistor and diodes are all in series and the voltage is applied to the
            whole string.

            The measured diode characteristics are given in mV and mA.  You are responsible for
            providing the measured or modeled data for these current/voltage characteristics.  I
            recommend 1-2-5 spacing from 1 μA up to the diode's current rating.  This information is
            encapsulated in the Diode objects, which have i(V) and V(i) methods, found by
            interpolation on your entered data.  The Diode object also has a PIV attribute, the
            maximum inverse voltage rating and i_max_mA, the maximum current rating in mA.

            Diodes:
                1N5817G Schottky 1 A 20 PIV
                1N5818 Schottky 1 A 30 PIV
                1N4148 300 mA 100 PIV
                1N3600 200 mA 100 PIV
                1N4004 1 A 400 PIV
                1N4007 1 A 1000 PIV
                3 mm LED:  yel, grn, red, blu, wht
                5 mm LED:  yel, grn, red, blu, wht

        '''))
        exit(0)
if 1:   # Classes
    class Diode:
        def __init__(self, name, i_max_A, PIV, V_V, i_A):
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
            self.V_V = tuple(V_V)
            self.i_A = tuple(i_A)
            Assert(len(V_V) == len(i_A))
            # Generate the interpolation functions using scipy
            self.vi = interp1d(self.i_A, self.V_V)
            self.iv = interp1d(self.V_V, self.i_A)
        def __str__(self):
            return self.name
        def __repr__(self):
            return self.name
        def i(self, V):
            'Return diode current in A for voltage V in V'
            return flt(self.iv(V))
        def V(self, i):
            'Return diode voltage in V for current i in A'
            return flt(self.vi(i))
    diodes = {}
    def D1N4148():
        # Raw data in mV and mA
        V_V = [flt(i)/1000 for i in (260, 320, 360, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900)]
        i_A = [flt(i) /1000 for i in (0.001, 0.002, 0.005, 0.01, 0.03, 0.1, 0.3, 0.8, 2.5, 8, 18, 40, 100, 200)]
        # Store the data in the diode container
        name = "1N4148silicon"
        D = diodes[name] = Diode(name, flt(300), flt(100), V_V, i_A)
        if 1:   # Debug printout
            w = 10
            GetColors()
            Dbg(D)
            Dbg("Demonstrate interp functions give original data")
            Dbg(f"{t.ornl}Current as a function of voltage")
            ind = " "*4
            Dbg(f"{t.trql}{ind}num{ind}{'V':{w}s}{ind}{'i_calc':{w}s}{ind}   {'i_actual':{w}s}")
            for j, V in enumerate(V_V):
                Dbg(f"{ind}{j:2d}{ind}{flt(V)!s:{w}s} calc = {D.i(V)!s:{w}s}  table = {i_A[j]!s:{w}s}")
            Dbg("")
            Dbg(f"{t.ornl}Voltage as a function of current")
            Dbg(f"{t.trql}{ind}num{ind}{'i':{w}s}{ind}{'V_calc':{w}s}{ind}   {'V_actual':{w}s}")
            for j, i in enumerate(i_A):
                Dbg(f"{ind}{j:2d}{ind}{flt(i)!s:{w}s} calc = {D.V(i)!s:{w}s}  table = {V_V[j]!s:{w}s}")
    def D3mmLED():
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
        name = "LED3mm:yel"; diodes[name] = Diode(name, i_max, PIV, V_V_yel, i_A)
        name = "LED3mm:grn"; diodes[name] = Diode(name, i_max, PIV, V_V_grn, i_A)
        name = "LED3mm:red"; diodes[name] = Diode(name, i_max, PIV, V_V_red, i_A)
        name = "LED3mm:blu"; diodes[name] = Diode(name, i_max, PIV, V_V_blu, i_A)
        name = "LED3mm:wht"; diodes[name] = Diode(name, i_max, PIV, V_V_wht, i_A)
    def D5mmLED():
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
        name = "LED5mm:yel"; diodes[name] = Diode(name, i_max, PIV, V_V_yel, i_A)
        name = "LED5mm:grn"; diodes[name] = Diode(name, i_max, PIV, V_V_grn, i_A)
        name = "LED5mm:red"; diodes[name] = Diode(name, i_max, PIV, V_V_red, i_A)
        name = "LED5mm:blu"; diodes[name] = Diode(name, i_max, PIV, V_V_blu, i_A)
        name = "LED5mm:wht"; diodes[name] = Diode(name, i_max, PIV, V_V_wht, i_A)
    def D1N5817G():
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
        name = "1N5817Gschottky"
        i_max, PIV = flt(1), flt(20)
        diodes[name] = Diode(name, i_max, PIV, V_V, i_A)
    def D1N5818():
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
        name = "1N5818schottky"
        i_max, PIV = flt(1), flt(30)
        diodes[name] = Diode(name, i_max, PIV, V_V, i_A)

    # Construct diode data
    D1N4148()
    D3mmLED()
    D5mmLED()
    D1N5817G()
    D1N5818()
    pp(diodes)
    exit()
if 1:   # Core functionality
    def Table(numpoints, arg):
        'Print a table for the selected diode'
        D = diodes[d["-d"]]
        if arg == "i":
            t.print(f"{t.diode}Current vs. voltage for {D.name}")
            istart, iend = D.i_A[0], D.i_A[-1]
            step = (ln(iend) - ln(istart))/numpoints
            w = 10
            for ln_i in frange(str(ln(istart)), str(ln(iend)), str(step), include_end=False):
                i = flt(exp(ln_i))
                V = flt(D.V(i))
                I = f"{i.engsi}A"
                V = f"{V.engsi}V"
                t.print(f"{t.i}{I:>{w}s} {t.V}{V:>{w}s}")
        else:
            t.print(f"{t.diode}Voltage vs. current for {D.name}")
            vstart, vend = float(D.V_V[0]), float(D.V_V[-1])
            step = (ln(vend) - ln(vstart))/numpoints
            w = 10
            for ln_V in frange(str(ln(vstart)), str(ln(vend)), str(step), include_end=False):
                V = flt(exp(ln_V))
                i = flt(D.i(V))
                I = f"{i.engsi}A"
                V = f"{V.engsi}V"
                t.print(f"{t.i}{I:>{w}s} {t.V}{V:>{w}s}")

if 1:
    d = {"-d": 0,}
    Table(30, "i")
    print()
    Table(30, "v")
    exit()

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["-t"] is not None:
        if not args or args[0] not in "v i".split():
            Error(f"First command line argument needs to be v or i")
        Table(d["-t"], args[0])
