'''

Print out lead-acid battery voltage and % of charge as a function of
temperature

The basic formulas are (see DeriveEquations())
    T = electrolyte temperature
    V = battery voltage in V
    P = percent charge on [0, 100]

Equations in °C:
  V = (P/100 + 15.5151)/1.3065 + (T - 26.7)/231.7
  P = -0.5638757*T + 130.65*V - 1536.454
Equations in °F:
  V = (P/100 + 15.5151)/1.3065 + (T - 80)/417
  P = -0.31330935*T + 130.65*V - 1526.445

'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2019 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Print out lead-acid battery voltage as function of temperature
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Imports
        import getopt
        import os
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from f import flt
        from frange import frange
        from color import t
    if 1:   # Global variables
        class G:
            pass
        g = G()  # Storage for global variables as attributes
        g.dbg = False
        ii = isinstance
        g.W = int(os.environ.get("COLUMNS", "80")) - 1
        g.L = int(os.environ.get("LINES", "50"))
        # Colors for charge levels
        t.bad = t("ornl")   # < 50%
        t.good = t("trq")   # >= 50%
if 1:  # Utility
    def Manpage():
        print(dedent(f'''
        The formula used for these tables is one I found many years ago on
        the web and I can't attribute it, but it looks like someone found a
        table of battery voltages as a function of P (percent of charge)
        and T (electrolyte temperature) and did a linear regression, as the
        function is of the form V = b0 + b1*P + b2*T where the b's are the
        regression constants and V is the voltage.

        These tables are approximate and can depend on a number of factors.
        A core assumption is that the battery is open circuit and has
        not been charged or discharged for 4 hours (battery manufacturers
        may recommend 24 hours).  Figure 5 in [1] is useful to give you a
        feel for the variance.

        A basic problem with testing a battery in a modern car is that the
        car's electronics can be drawing power at various times, even when
        the ignition is off.  The easiest fix is to disconnect the positive
        battery terminal, but be sure you can do this without causing the
        car problems (our GM and Subaru cars withstand this OK, but a
        friend had a 2000's Audi that would get pretty screwed up if its
        battery was disconnected). 

        Equations in °C:
            V = (P/100 + 15.5151)/1.3065 + (T - 26.7)/231.7
            P = -0.5638757*T + 130.65*V - 1536.454
        Equations in °F:
            V = (P/100 + 15.5151)/1.3065 + (T - 80)/417
            P = -0.31330935*T + 130.65*V - 1526.445
        where
            P = percent of charge (0 to 100)
            V = battery voltage
            T = temperature of electrolyte

        References
        ----------
        [1] https://www.power-sonic.com/wp-content/uploads/2018/12/Technical-Manual.pdf
        [2] https://batteryuniversity.com/article/bu-903-how-to-measure-state-of-charge
        '''))
        exit(status)
    def Usage(d, status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [temperature]
          Print a table of percent of charge of a lead acid battery as a
          function of electrolyte temperature and voltage.  Allow 24 hours
          for the battery to reach equilibrium after charging and make sure
          there is no load on the battery.

          If temperature is included, print a table of voltages for that
          temperature.
        Example:  temp = 0
          The table gives the battery voltage for % charge from 0 to 109%.  I
          went out to one of our cars and used an IR thermometer to measure the
          battery temperature at -4 °C.  The battery voltage was 12.30 V, but
          it was rising by 10-20 mV/s, probably because the door locks were
          opened with the clicker.  The closest temperature is 0 °C, so the 
          voltage table indicates the % charge is 71%.  It has been 2 weeks
          since this battery was charged and it has been unused in that time.
          This measurement indicates to me that I need to charge the battery
          again.
        Options
          -f    Use °F
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-f"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "fh")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in "f":
                d[o] = not d[o]
            if o in ("-h", "--help"):
                Usage(d, status=0)
        return args
if 1:  # Core functionality
    def DeriveEquations():
        'Use sympy to invert the relations'
        from sympy import symbols, Eq, solve
        V, P, T = symbols("V P T")
        # °C
        print("Equations in °C:")
        print("  V = (P/100 + 15.5151)/1.3065 + (T - 26.7)/231.7")
        f = Eq(V, (P/100 + 15.5151)/1.3065 + (T - 26.7)/231.7)
        print(f"  P = {solve(f, P)[0]}")
        # °F
        print("Equations in °F:")
        print("  V = (P/100 + 15.5151)/1.3065 + (T - 80)/417")
        f = Eq(V, (P/100 + 15.5151)/1.3065 + (T - 80)/417)
        print(f"  P = {solve(f, P)[0]}")
        exit()
    def C(T_degF):
        return 5/9*(T_degF - 32)
    def V(pct_chg, T_degC):
        '''I cannot attribute this formula for lead-acid battery voltage as a
        function of % of charge and electrolyte temperature, as I found it many
        years ago and didn't write down the source.
        '''
        return (pct_chg/100 + 15.5151)/1.3065 + (T_degC - 26.7)/231.7
    def VoltageTable(degC=True):
        '''Print out a table of % of charge as a function of DC voltage.
        The voltages go down the left column from 11.6 to 12.8 in steps of
        50 mV.  The electrolyte temperature is in steps of 5 °C or 10 °F.
 
        Equations in °C:
            V = (P/100 + 15.5151)/1.3065 + (T - 26.7)/231.7
            P = -0.563875701337937*T + 130.65*V - 1536.45451877427
        Equations in °F:
            V = (P/100 + 15.5151)/1.3065 + (T - 80)/417
            P = -0.313309352517986*T + 130.65*V - 1526.44525179856
        '''
        if d["-f"]: # Use °F
            pass
        else:       # Use °C
            if 1:   # Print header
                print(f"Percent charge as a function of lead-acid battery voltage")
                print("  (Battery has not been charged or discharged for at least 24 hours)")
                print()
                print(f"{'Electrolyte Temperature, °C':^{g.W}s}")
                # Percent of charge will be a 2 digit integer and
                # temperature will be 3 digits (typically to allow from -20
                # to 70).  We'll have a space between columns, so each
                # column will be 4 characters.  The first column is voltage
                # and will be 5 characters.
                T_degC = list(range(-20, 71, 5))
                # Trim items off this list until the column width is <= g.W
                while len(T_degC)*4 + 7 > g.W:
                    T_degC.pop()
                print(f"Volts ", end="")
                for T in T_degC:
                    print(f"{T:>4d}", end="")
                print()
                print(f"----- ", end="")
                for T in T_degC:
                    print(f" ---", end="")
                print()
            # Print table
            for V in frange("11.7", "12.8", "0.05", include_end=True, return_type=flt):
                print(V, end=" ")
                for T in T_degC:
                    P = -0.563875701337937*T + 130.65*V - 1536.45451877427
                    if 0 <= P <=100:
                        if P < 50:
                            print(f"{t.bad}{int(round(P, 0)):>4d}{t.n}", end="")
                        else:
                            print(f"{t.good}{int(round(P, 0)):>4d}{t.n}", end="")
                    else:
                        #print(f"····", end="")
                        c = "․"
                        c = "˙"
                        c = "·"
                        #print(f"{c*3:>4s}", end="")
                        print(f"{'  · '}", end="")
                print()
    def ChargeTable(temperature):
        T = int(temperature)
        if T % 10 != 0:
            print("Temperature must be divisible by 10")
            exit(1)
        degC = not d["-f"]
        w = int(os.environ.get("COLUMNS", 80)) - 1 
        print(f"{t.bad}{'Lead-Acid Battery Voltage at % of Charge':^{w}s}{t.n}\n")
        deg = f"°{'C' if degC else 'F'}"
        n = 6
        s = f"Temperature in {deg}"
        print(f"{t.good}{s:^{w}s}{t.n}")
        print(" %  ", end=f"{t.good}")
        for i in range(10):
            print(f"{T + i:^{n}d} ", end="")
        print(t.n)
        print("--- ", end="")
        for i in range(10):
            print(f"{'-'*n:^{n}s} ", end="")
        print()
        for pct in range(0, 101, 10):
            print(f"{pct:3d}", end=" ")
            for T_offset in range(10):
                T0 = T + T_offset
                if not degC:
                    T0 = C(T0)  # Change F to C
                v = V(pct, T0)
                print(f"{v:{n}.3f}", end=" ")
            print()
        print()

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if not args:
        VoltageTable()
    else:
        ChargeTable(args[0])
