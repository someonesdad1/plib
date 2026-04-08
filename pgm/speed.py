'''
Calculate spindle RPM from material and diameter

Primary reference will be MH 19th ed pg 1697 to 1731.  Most of such tables
seem to standardize on a feed of 12 mils/rev and a depth of cut of 1/8
inch.

-1 can be an option to use half of the MH recommendations.  This can be a
good starting point when being conservative or unsure of the material.

-2 can be used for carbide, which doubles the sfpm value.

The materials I'm most interested in are

    Aluminum
    Brass, tough alloys like naval brass
    Brass, free machining, leaded
    Bronze, bearing alloy
    Bronze, cast
    Copper
    Iron, cast (through scale or under scale)
    Titanium
    Monel
    Steel
        Free machining, sulfurized
        Free machining, leaded
        Plain carbon
        Alloy, sulfurized
        Alloy, leaded
        Alloy
        Cast
        Stainless, ferritic
        Stainless, austenitic
        Stainless, martensitic
        Tool (water hardening, annealed)
        
Turning:  1706-1713
Milling:  1716-1722
Drilling: 1725-1731 (includes reaming)

'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Calculate spindle RPM from material and diameter
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
    if 1:  # Custom imports
        from wrap import dedent
        import trm
        t = trm.TrmDP()
        from f import flt, pi
        try:
            import termtables as tt
        except ImportError:
            pass
        if 1:
            import debug
            debug.SetDebugger()
        # from columnize import Columnize
    if 1:  # Global variables
        class G:
            pass
        g = G()  # Storage for global variables as attributes
        g.dbg = False
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        ii = isinstance
        g.W = int(os.environ.get("COLUMNS", "80")) - 1
        g.L = int(os.environ.get("LINES", "50"))
if 1:  # Cutting data
    if 1:  # Cutting data from https://physics.byu.edu
        '''
        Taken from https://physics.byu.edu/courses/experimental/docs/physics240/toolspeeds.pdf
        For HSS tools
    
        Speeds in sfpm          Drilling           Lathe       Mill
            Aluminum              250             350-700     250-500
            Brass & bronze        200             250-500     150-450
            Copper                70              100-250     100-200
            Cast iron, soft       120             100-250     80-120
            Cast iron, hard       80              50-150      50-100
            Mild steel            110             100-250     70-120
            Cast steel            50              70-150      80-100
            Alloy steels          60              50-150      30-60
            Tool steel            60              50-150      40-70
            Stainless steel       30              60-180      30-60
            Titanium              30              90-200      40-60
            Steel, high Mn        15              40-100      20-40
    
                                       Lathe               Mill
        Depth of cut, mils          HSS     Carbide     HSS     Carbide
            Aluminum                50      70          50      50
            Mild steel              30      50          30      30
            Alloy steels            25      45          25      25
            Stainless steel         30      50          30      30
            Brass                   50      70          50      50
    
        Feeds for turning in mils per revolution
                                    Roughing        Finish
            Aluminum                15-25           5-10
            Brass & bronze          15-25           3-10
            Copper                  10-20           4-8
            Cast iron, soft         15-25           5-10
            Cast iron, hard         10-20           3-10
            Mild steel              10-20           3-10
            Cast steel              10-20           3-10
            Alloy steels            10-20           3-10
            Tool steel              10-20           3-10
            Stainless steel         10-20           3-10
            Titanium                10-20           3-10
            Steel, high Mn          10-20           3-10
        
        Feeds for milling in mils per revolution
                                    Face mill       Side mill   End mill
            Aluminum                5-20            4-10        5-10
            Brass & bronze          4-20            4-10        5-10
            Copper                  4-10            4-7         4-8
            Cast iron, soft         4-16            4-9         4-8
            Cast iron, hard         4-10            2-6         2-6
            Mild steel              4-10            2-7         2-10
            Alloy steels            4-10            2-7         2-6
            Tool steel              4-8             2-6         2-6
            Stainless steel         4-8             2-6         2-6
            Titanium                4-8             2-6         2-6
            Steel, high Mn          4-8             2-6         2-6
    
        Feeds for drilling in mils per revolution
            Diam, inches        mils/rev
            < 0.12              1 - 2
            0.12 - 0.25         2 - 4
            0.25 - 0.5          4 - 7
            0.5 -  1            7 - 15
            > 1                 15 - 25
    
        Manual drilling RPM vs diameter chart (source unknown)
                        Mild        Al &
            Dia, in     Steel       Brass
            0           1530        1600
            1/16        1330        1580
            1/8         1150        1510
            3/16        990         1400
            1/4         830         1240
            3/8         580         875
            7/16        475         700
            1/2         380         530
            5/8         240         295
            3/4         140         200
            7/8         100         200
            1           100         150
        '''
    if 1:  # Cutting data from Morse
        '''
        "Machinist's Practical Guide", copyright 1929, 1963-1970, 1973-1974
        A small handbook I probably got in the 1970's
    
        page 13:  Milling cutters, speeds in sfpm
            Aluminum            600+
            Copper              300+
            Brass               300
            Bronze              200
            Malleable iron      100
            Cast iron           100
            Cast steel          70
            Steel 100 Brinell   150
                  200 Brinell   70
                  300 Brinell   40
                  400 Brinell   20
                  500 Brinell   10
            Stainless steel
                Free machining  70
                Other           40
            Titanium, kpsi
                < 100           35-55
                100-135         25-35
                >= 135          15-25
            High tensile steels, kpsi
                180-220         25-40
                220-260         10-25
                260-300         6-10
            High temperature alloys
                Ferritic low    40-60
                Austenitic      20-30
                Nickel-based    5-20
                Cobalt-based    5-10
    
        Feed per tooth in mils/minute
            Face milling                7
            Straddle milling            5
            Slot milling (side mills)   3
            Slab milling, light         4
            Slab milling, heavy         8
            Sawing                      0.5 to 1
            Thread milling              0.5 to 1
        '''
    if 1:  # Cutting data from Cleveland
        '''
        From Grandpa's lathe, it's a small PVC circular "slide rule"
        Copyright 1947
    
        Smaller drills
            Drilling sfpm for HSS           60
            Drilling sfpm for carbon steel  30
        
        For larger drills on other side, sfpm
            60, 80, 90, 100 for "Cle-forge"
            30, 50          for carbon steel
        '''
    if 1:  # Cutting data from MH 27th ed
        '''
        Ref. table 1 on pg 1027
        For HSS, feed is 12 mils/rev and a 125 mil depth of cut; see page 1036
        for an adjustment table.  NOTE THESE NUMBERS ARE FOR A TOOL LIFE OF 15
        MINUTES.  I would probably divide the recommended surface speeds by 2
        to get more realistic home shop numbers.
        '''
    if 1:  # Cutting data from MH 19th ed
        '''
        Opinion:  This is probably the most reliable information to use.  The
        27th ed. clearly expands on the same material & words, but is more
        tedious to digest, probably because most of the focus is on throughput
        with HSS simply not being used anymore in high volume production.
    
        Ref. pg 1706-1713 for turning
            Are for 12 mil/rev and 1/8" depth of cut
    
        pg 1703 states reaming speeds should be about 2/3 those of drilling
        with a feed of 1.5 to 4 mils per flute per rev.
        '''
    if 1:  # Cutting data from Tubal Cain
        '''
        This is probably the most practical information, particularly
        because it is aimed at the HSM, not production people.  First use
        these numbers, then contrast them to MH 19th ed numbers.
        
        Inspection of the table shows the numbers are proportional to
        diameter, so the assumption is a constant surface speed.  
        
        We have sfpm = pi*D*R/12 where D is diameter in inches and R is
        RPM.  Thus, R = 12*sfpm/(pi*D).  Use the 1 inch diameter row;
        multiply the table RPM by 0.2618 (pi/12) to get the sfpm:
        
                            SFPM            Ratio
            i  Group   Rough   Finish       F/R
            0    A      20       25         1.25
            1    B      40       50         1.25
            2    C      65       75         1.15
            3    D      120      140        1.17
            4    E      600      785        1.31
            
        For mental computation, use R = 4*sfpm/D.
        '''
        tubal = {
            # Group, sfpm, f/r ratio
            "A": (20, 1.25),
            "B": (40, 1.25),
            "C": (65, 1.25),
            "D": (120, 1.17),
            "E": (600, 1.31),
        }
        tubal_matl = {
            "Aluminum": "E",
            "Bakelite": "C",
            "Brass": "D",
            "Brass, red": "C",
            "Bronze": "C",
            "Copper": "C",
            "Iron, cast": "C",
            "Iron, cast (hard)": "A",
            "Iron, malleable": "B",
            "Monel": "B",
            "Steel (cast)": "B",
            "Steel (freecutting)": "D",
            "Steel": "C",
            "Stainless steel": "B",
            "Drill rod": "B",
            "Plastics": "D",
        }
if 1:  # Utility
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(
            dedent(f'''
        Usage:  {sys.argv[0]} [options] diameter [material]
          For the given diameter, show the needed spindle speed for
          turning, milling, and drilling.  With no arguments, print out a
          table.
        Options:
            -d n    Number of digits [{d["-d"]}]
            -h      Print a manpage
            -p      Generate a plot
        ''')
        )
        exit(status)
    def ParseCommandLine(opts):
        opts["-m"] = False     # Diameters are in mm
        opts["-d"] = 3         # Number of significant digits
        opts["-p"] = False     # Plot
        try:
            Opts, args = getopt.getopt(sys.argv[1:], "d:hmp")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in Opts:
            if o[1] in list("mp"):
                opts[o] = not opts[o]
            elif o == "-d":
                try:
                    opts[o] = int(a)
                    if not (1 <= opts[o] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o == "-h":
                Usage(status=0)
        if opts["-p"]:
            PlotGraph()
        x = flt(0)
        x.N = opts["-d"]
        return args
if 1:  # Core functionality
    def TableOld():
        # Diameters in mils
        dia = list(flt(int(i)/1000) for i in '''
            20 40 60 80 100 125 150 200 250 313 375 438 500 625 750 813 875 938 1000
            1125 1250 1375 1500 1750 2000 2500 3000 3500 4000 5000 6000
        '''.split())
        ltr = "A B C D E".split()
        print("Turning speed for various materials (ref. Tubal Cain)\n")
        w0, w1, a = 10, 10, ">"
        gap = " "*2
        c = {
            "A": t("seal"),
            "B": t("purl"),
            "C": t("cynl"),
            "D": t("grnl"),
            "E": t("yell"),
        }
        print(f"{'Diameter':^{w0}s}")
        print(f"{'inches':^{w0}s}", end=gap)
        for l in ltr:
            print(f"{c[l]}{l:{a}{w1}s}{t.n}", end="")
        print()
        for D in dia:
            print(f"{D!s:^{w0}s}", end=gap)
            for l in ltr:
                sfpm, ratio = tubal[l]
                rpm = flt(12*sfpm/(pi*D))
                print(f"{c[l]}{rpm!s:{a}{w1}s}{t.n}", end="")
            print()
        # Print material key
        for l in ltr:
            matls = []
            for i in tubal_matl:
                if tubal_matl[i] == l:
                    matls.append(i)
            t.print(f"{c[l]}{l}:  {'; '.join(matls)}")
    def Table(diameters):
        '''Print the table for the indicated diameters.  Dimensions are in inches unless
        the -m option was used.  diameters is a list of strings.
        '''
        # Construct the diameters in inches
        dia = []
        for d in diameters:
            di = flt(d)
            if opts["-m"]:
                di /= 25.4
            dia.append(di)
        # Column colors
        cols = {
            "E": t.sky,
            "D": t.yel,
            "C": t.mag,
            "B": t.wht,
            "A": t.wht,
        }
        E, D, C, N = cols["E"], cols["D"], cols["C"], t.n
        data = [
            ["",       "",   "",             "",             f"{C}Bakelite{N}",  "",          ""],
            ["",       "",   "",             "",             f"{C}Red brass{N}", "Monel",     "Hard"],
            ["",       "",   "",             f"{D}Brass",    f"{C}Copper{N}",    "Drill rod", "cast"],
            ["Inches", "mm", f"{E}Aluminum", f"{D}Plastics", f"{C}Steel{N}",     "SST",       "iron"],
            ["------", "--", f"{E}--------", f"{D}--------", f"{C}---------{N}", "---------", "----"],
            #                 E               D               C                  B            A
        ]
        for d in dia:
            o = []
            o.append(f"{d}")    # Diameter in inches
            if d >= 0.15:
                o.append(f"{d*25.4:.0f}")   # Diameter in mm
            else:
                o.append(f"{d*25.4:.1f}")   # Diameter in mm
            for i in "E D C B A".split():
                spd = flt(12*tubal[i][0]/(pi*d))
                with spd:
                    spd.N = 2
                    rpm = cols[i] + str(spd)
                o.append(rpm)
            data.append(o)
        s = t.ornl
        data.append(["", f"{s}SFPM", "600", "120", "65",     "40", "20"]),
        data.append(["", f"{s}m/s", "3", "0.61", "0.33",     "0.2", "0.1"]),
        t.print(f"{t.grnl}Rough turning speeds (finish speeds about 20% higher)")
        tt.print(data, style=" "*15, alignment="rrrrrrr")
    def PlotGraph():
        from pylab import pi, loglog, array, show, grid, xlabel, ylabel
        from pylab import legend, title, savefig
        dia = array((0.02, 0.1, 0.2, 0.5, 1, 2, 5, 6))
        lbl = {
            600: ("Aluminum", "--"),
            120: ("Brass, plastics", "-."),
            65: ("Bakelite, red brass, Cu, steel", "-"),
            40: ("Monel, drill rod, SST", ":"),
            20: ("Hard cast iron", "--"),
        }
        for sfpm in (600, 120, 65, 40, 20):
            rpm = 12*sfpm/(pi*dia)
            l, s = lbl[sfpm]
            loglog(dia, rpm, "k" + s, label=l)
        grid()
        xlabel("Diameter, inches")
        ylabel("Speed, RPM")
        legend(loc="upper right")
        title("Spindle speed versus diameter")
        #show()
        savefig("cutting_speed.png", dpi=600)
        exit()
if __name__ == "__main__":
    opts = {}  # Options dictionary
    args = ParseCommandLine(opts)
    if args:
        # Print for given diameter
        Table(args)
    else:
        dia = list(str(flt(int(i)/1000)) for i in '''
            20 40 60 80 100 125 150 200 250 313 375 438 500 625 750 813 875 938 1000
            1125 1250 1375 1500 1750 2000 2500 3000 3500 4000 5000 6000
            '''.split())
        Table(dia)
