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
        from columnize import Columnize
        from util import Len
        if len(sys.argv) > 1:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()  # Storage for global variables as attributes
        g.dbg = False
        ii = isinstance
        g.W = int(os.environ.get("COLUMNS", "80")) - 1
        g.L = int(os.environ.get("LINES", "50"))
        # Colors for charge levels
        t.bad = t("lip")   # < 50%
        t.good = t("grn")   # >= 50%
if 1:  # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(dedent(f'''

        The formula used for these tables is one I found many years ago on the web and I can't
        attribute it, but it looks like someone found a table of battery voltages as a function of
        P (percent of charge) and T (electrolyte temperature) and did a linear regression, as the
        function is of the form V = b0 + b1*P + b2*T where the b's are the regression constants
        and V is the voltage.

        These tables are approximate and can depend on a number of factors.  A core assumption is
        that the battery is open circuit and has not been charged or discharged for 4 hours
        (battery manufacturers may recommend 24 hours).  Figure 5 in [1] is useful to give you a
        feel for the variance.

        A basic problem with testing a battery in a modern car is that the car's electronics can
        be drawing power at various times, even when the ignition is off.  The easiest fix is to
        disconnect the positive battery terminal.  Before doing this, make sure you can do this
        without causing the car problems (our GM and Subaru cars withstand this OK, but a friend
        had a 2000's Audi that would get pretty screwed up if its battery was disconnected). 

        Equations in °C:
            V = (P/100 + 15.5151)/1.3065 + (T - 26.7)/231.7
            P = -0.5638757*T + 130.65*V - 1536.454
              = 130.65*V - (1536.454 + 0.5638757*T)
        Equations in °F:
            V = (P/100 + 15.5151)/1.3065 + (T - 80)/417
            P = -0.31330935*T + 130.65*V - 1526.445
              = 130.65*V - (1526.445 + 0.31330935*T)
        where
            P = percent of charge (0 to 100)
            V = battery voltage
            T = temperature of electrolyte

        The second forms of the equations for P show that they are linear at a constant
        temperature.

        Caution:  you'd be wise to verify these tables and formulas with the batteries you have.
        I have two identical RV batteries purchased within a year or so of each other and one
        seems to fit the function model well, but the other doesn't, particularly in winter garage
        temperatures around 8-10 °C.  

        Figure 12 in [1] show some circuits that might help prevent overdischarge of batteries.  

        A good battery charger is a CV/CC (constant voltage and constant current) DC power supply.
        [3] recommends 2.25 V/cell to 2.27 V/cell as a float charge.  I chose to use 2.25 V/cell
        for the battery charger I built because I manually first charge my batteries with my 35-40
        year old analog charger that still works well.  For a 12 V battery with 6 cells, this
        means a charging voltage of 6(2.25) V or 12 + 3/2 = 13.5 V.

        A multiple battery charger design
            
            I usually have 4 to 6 batteries from vehicles and RVs stored in our garage over the
            winter (the kids and grandkids sometimes need batteries stored over the winter, which
            explains why I have more than a few).  I'd have to measure their voltage and put the
            charger on them every week or two, a tedious manual process because I've been doing it
            for more than 30 years.

            To automate this task, I used a 24 V DC switching power supply that I had on hand that
            had both constant voltage and constant current features.  I set the maximum charging
            current to about 0.75 A, as these batteries would each be charged daily for a selected
            period.  I used a $10 μC (microcontroller) with a $10 PC board with 8 relays that
            connected each battery to the charging voltage sequentially.  Another $1 relay was
            used to connect the selected battery across a voltage divider to allow the μC to
            measure the battery's voltage or connect it to the charging voltage.  An old
            mechanical timer power cycled the μC every night around 9 pm so that charging took
            place from about 9 pm to 1 am, then the batteries would be rested for around 8 hours
            when their voltages were measure the next morning.  A 16 character 2 line LCD display
            showed the estimated battery capacity of each connected battery, gotten by measuring
            the resting battery voltage.  I don't even look at the display, as there's an RGB LED
            on the charger that's green if nothing needs attention or red if one or more batteries
            need attention.  I had an old under $1 buck converter I used to get the 5 V needed for
            the μP from the power supply voltage.  The total cost was around $25, as I used mostly
            scrap laying around the house for the remaining stuff.

            Another design would use a power supply, but would use DC buck converters like the
            $5 units from https://www.mpja.com:  models 31562 or 33370.  You'd buy one of these
            for each battery to be charged and set the voltage and current appropriately for each
            battery.  If my μC design proves too problematic with my set of batteries, I'll buy a
            number of these buck converter boards.  This design will have the advantage of being
            able to choose the charging voltage and current for each battery -- and they'll all be
            charged in parallel.

            With both designs, you'll want to include a diode to protect each buck converter or
            the power supply from the user connecting a battery backwards.  If you limit the
            current like I did to around 0.75 A, a 1N400X diode with a 1 A rating will work.
            Remember to take the diode's voltage drop into account when setting the battery's
            charging voltage or measure it at the battery's positive terminal.


        References
        ----------
        [1] https://www.power-sonic.com/wp-content/uploads/2018/12/Technical-Manual.pdf
        [2] https://batteryuniversity.com/article/bu-903-how-to-measure-state-of-charge
        [3] https://batteryuniversity.com/article/bu-403-charging-lead-acid
        '''))
        exit(0)
    def Usage(d, status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [temperature]
            Print a table of percent of charge of a lead acid battery as a function of electrolyte
            temperature and voltage.  Allow 24 hours for the battery to reach equilibrium after
            charging and make sure there is no load on the battery.

            If temperature is included, print a table of voltages for that temperature and ±5
            degrees above and below it.
        Example:  '{sys.argv[0]} -c -4'
            The table gives the battery voltage for % charge from 0 to 109%.  I went out to one of
            our cars and used an IR thermometer to measure the battery temperature at -4 °C.  The
            battery voltage was 12.30 V, but it was rising by 10-20 mV/s, probably because the
            door locks were opened with the clicker.  The table indicates the battery's charge is
            around 75%.  It has been 2 weeks since this battery was charged and it has been unused
            in that time.  This measurement indicates to me that I need to charge the battery
            again.
        Options
            -2    Give voltages to 2 places
            -c    Use °C [{d["-c"]}]
            -f    Print a table functions converting voltage to % charge at various temperatures
            -H    Print manpage
            -p    Print a table of voltages as a function of % charge at temperatures ±5 from
                  the given temperatures.  This helps visualize the slopes for both temperature 
                  and charge.
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-2"] = False
        d["-c"] = False
        d["-f"] = False
        d["-p"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "2cfHhp")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in "2cfp":
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(d, status=0)
            elif o in ("-H",):
                Manpage()
        x = flt(0)
        x.N = 4
        x.rtz = False
        return args
if 1:  # Core functionality
    def DeriveEquations():
        '''Use sympy to invert the relations.  Results are:

        Equations in °C:
            V = (P/100 + 15.5151)/1.3065 + (T - 26.7)/231.7
            P = -0.563875701337937*T + 130.65*V - 1536.45451877427
        Equations in °F:
            V = (P/100 + 15.5151)/1.3065 + (T - 80)/417
            P = -0.313309352517986*T + 130.65*V - 1526.44525179856
        '''
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
    def FtoC(T_degF):
        return 5/9*(T_degF - 32)
    def Voltage(pct_chg, T, degF=False):
        '''Calculate voltage given the % charge and temperature T in °C.  I can't attribute this
        formula for lead-acid battery voltage as a function of % of charge and electrolyte
        temperature, as I found it many years ago and didn't write down the source.
        '''
        if degF:
            T = (T - 32)*5/9
        return (pct_chg/100 + 15.5151)/1.3065 + (T - 26.7)/231.7
    def ChargeTable(temperature):
        'Print charge table when command line has a temperature'
        T = int(temperature)
        degC = d["-c"]
        w = 80  # Can use fixed-width
        low, high = T - 5, T + 5  # Which temperature columns to print
        print(f"{t.bad}{'Lead-Acid Battery Voltage at % of Charge':^{w}s}{t.n}\n")
        deg = f"°{'C' if degC else 'F'}"
        n = 6
        s = f"Temperature in {deg}"
        print(f"{t.good}{s:^{w}s}{t.n}")
        print(" %  ", end=f"{t.good}")
        R = range(low, high + 1)
        for i in R:
            print(f"{i:^{n}d} ", end="")
        print(t.n)
        print("--- ", end="")
        for i in R:
            print(f"{'-'*n:^{n}s} ", end="")
        print()
        for pct in range(0, 101, 10):
            print(f"{pct:3d}", end=" ")
            for T_offset in R:
                T0 = T + T_offset
                if not degC:
                    T0 = FtoC(T0)  # Change F to C
                v = Voltage(pct, T0)
                print(f"{v:{n}.2f}" if d["-2"] else f"{v:{n}.3f}", end=" ")
            print()
        print()
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
        if not d["-c"]: # Use °F
            if 1:   # Print header
                print(f"Percent charge as a function of lead-acid battery voltage")
                print("  (Battery has not been charged or discharged for at least 24 hours)")
                print()
                s = "  0  10  20  30  40  50  60  70  80  90 100 110 120 130 140 150 160"
                print(f"{' '*7}{'Electrolyte Temperature, °F':^{len(s)}s}")
                # Percent of charge will be a 2 digit integer and
                # temperature will be 3 digits (typically to allow from 0
                # to 160 °F).  We'll have a space between columns, so each
                # column will be 4 characters.  The first column is voltage
                # and will be 5 characters.
                T_degF = list(range(0, 161, 10))
                # Trim items off this list until the column width is <= g.W
                while len(T_degF)*4 + 7 > g.W:
                    T_degF.pop()
                print(f"Volts ", end="")
                for T in T_degF:
                    print(f"{T:>4d}", end="")
                print()
                print(f"----- ", end="")
                for T in T_degF:
                    print(f" ---", end="")
                print()
            # Print table
            for V in frange("11.7", "12.8", "0.05", include_end=True, return_type=flt):
                print(V, end=" ")
                for T in T_degF:
                    P = -0.313309352517986*T + 130.65*V - 1526.44525179856
                    if 0 <= P <=100:
                        if P < 50:
                            print(f"{t.bad}{int(round(P, 0)):>4d}{t.n}", end="")
                        else:
                            print(f"{t.good}{int(round(P, 0)):>4d}{t.n}", end="")
                    else:
                        print(f"{'  · '}", end="")
                print()
        else:       # Use °C
            if 1:   # Print header
                print(f"Percent charge as a function of lead-acid battery voltage")
                print("  (Battery has not been charged or discharged for at least 24 hours)")
                print()
                print(f"{'Electrolyte Temperature, °C':^{g.W}s}")
                # Percent of charge will be a 2 digit integer and
                # temperature will be 3 digits (typically to allow from -20
                # to 70 °C).  We'll have a space between columns, so each
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
                        print(f"{'  · '}", end="")
                print()
        print("Use -c for °C, -H for manpage")
    def PctVsVoltage(T, degF=False):
        'Return the equation for P(V) at the given temperature T'
        a, b = 130.65, -1526.44525179856
        def P_degF(V):
            return -0.313309352517986*T + a*V + b
        def P_degC(V):
            return -0.563875701337937*T + a*V + b
        return P_degF if degF else P_degC
    def PercentVersusVoltageTable(temperature):
        'Print percent of charge for every 1% with its corresponding voltage'
        T = temperature
        degC = d["-c"]
        t.v = t.lill
        t.p = t.ornl
        width = g.W
        deg = f"°{'C' if degC else 'F'}"
        o = []
        vlast = 11.851
        for pct in range(0, 101, 1):
            v = Voltage(pct, T, degF=not d['-c'])
            s = f"{t.p}{pct:3d}  {t.v}{v:6.3f}{t.n}"
            o.append(s)
        lines = list(Columnize(o, width=width))
        w = Len(lines[0])
        title1 = f"Lead-Acid Battery % of Charge vs. Voltage in V"
        print(f"{title1:^{w}s}")
        with T:
            T.rtz = True
            title2 = f"Temperature = {T} {deg}"
        print(f"{title2:^{w}s}\n")
        for i in lines:
            print(i)
        # Print the linear equation
        slope, b = flt(130.65), flt(1526.44525179856)
        b1 = flt(0.563875701337937*T) if d["-c"] else flt(0.313309352517986*T)
        intercept = b + b1
        print()
        with slope:
            slope.N = 6
            t.print(f"Linear equation:  {t.grnl}P = {slope}*V - {intercept}")
            p = slope*12.333 - intercept
            print(f"Example:  for 12.333 V, P = {slope}*12.333 - {intercept}")
            print(f"                          = {slope*12.333} - {intercept} = {p:.2f}")
    def PercentVersusVoltageFunctions():
        '''
        Equations in °C:
            P = -0.563875701337937*T + 130.65*V - 1536.45451877427
        Equations in °F:
            P = -0.313309352517986*T + 130.65*V - 1526.44525179856
        Constant names
                         a              slope           b
        '''
        slope = flt(130.65)
        ac, bc = flt(-0.563875701337937), flt(-1536.45451877427)
        af, bf = flt(-0.313309352517986), flt(-1526.44525179856)
        F = [flt(i) for i in "  0  10  20  30  40  50  60  70  80  90 100 110".split()]
        C = [flt(i) for i in "-15 -10  -5   0   5  10  15  20  25  30  35  40".split()]
        t.t, t.eq, t.f, t.c = t.ornl, t.magl, t.yell, t.grnl   # Colors
        # Print header
        t.print(f"{t.t}Equations for % charge as a function of voltage")
        print(f"    Voltage should be from 11.6 V to 12.8 V")
        t.print(f"        {t.eq}Equation is 130.65*V - b")
        print()
        w1, w2 = 6, 15
        w = (w1, w2, w1, w2)
        t.print(f"{t.f}{'°F':>{w[0]}s} " f"{'b for °F':^{w[1]}s} "
                f"{t.c}{'°C':>{w[2]}s} " f"{'b for °C':^{w[3]}s}")
        t.print(f"{t.f}{'-'*3:>{w[0]}s} " f"{'-'*8:^{w[1]}s} "
                f"{t.c}{'-'*3:>{w[2]}s} " f"{'-'*8:^{w[3]}s}")
        # Print table
        with slope:
            slope.N = 6
            slope.rtz = True
            for Tf, Tc in zip(F, C):
                ef = flt(f"{abs(af*Tf + bf)}")
                ec = flt(f"{abs(ac*Tc + bc)}")
                t.print(f"{t.f}{Tf!s:>{w[0]}s} " f"{ef:^{w[1]}.1f} "
                        f"{t.c}{Tc!s:>{w[2]}s} " f"{ec:^{w[3]}.1f}")
        # Print example
        print()
        print(dedent(f'''

        Example:  At 50 °F, the equation is 130.65*V - 1542.1.  12.57 V will give 100.1% charge
        and 12.19 V will give 50.5% charge.  Caution:  you'll want to verify these formulas before
        using them, as they may not apply to the batteries you're using.

        '''))

if 0:
    PercentVersusVoltageFunctions()
    exit()

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["-p"]:
        if args:
            T = flt(args[0])        # Assume °F
        else:
            T = flt(20) if d["-c"] else flt(70)
        ChargeTable(T)
    elif d["-f"]:
        PercentVersusVoltageFunctions()
    else:
        if not args:
            VoltageTable()
        else:
            for T in args:
                PercentVersusVoltageTable(T)
