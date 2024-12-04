if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Calculates the BMI given height and mass
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Imports
        import sys
        import getopt
        from pdb import set_trace as xx
    if 1:   # Custom imports
        from columnize import Columnize
        from wrap import dedent
        from f import flt
        from frange import frange
        from color import t
    if 1:   # Global variables
        lb2kg = 0.453592
        in2m = 0.0254
        # Glenda measured my height at 69.5 inches with socks on
        personal_height_inches = 69.4
        # Colors
        t.low = t.denl
        t.normal = t.grn
        t.high = t.ornl
        t.obese = t.redl
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage():
        name = sys.argv[0]
        print(dedent(f'''
        Usage:  {name} [options] mass_lbs height_inches
          Calculates and returns the body mass index for the given mass and height.  BMI is (mass
          in kg)/(height in m)^2.  General categories are:

        '''))
        Key()
        print(dedent(f'''
        
        Options:
          -k      Show metric mass and height table
          -m      Mass is in kg and height in m.
          -p      Print the US percentiles table
          -t      Print out table of BMI (you can include a height in inches
                  on the command line if you wish)
        '''))
        exit()
    def ParseCommandLine(d):
        d["-k"] = False     # Show mass and height table
        d["-m"] = False     # Mass in kg and height in m
        d["-p"] = False     # Show US percentiles table
        d["-t"] = False     # Show BMI table
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "kmpt")
        except getopt.GetoptError as str:
            msg, option = str
            print(msg)
            sys.exit(1)
        for o, a in optlist:
            if o == "-k":
                ShowMetricTable()
            elif o == "-m":
                d[o] = True
            elif o == "-p":
                US_Data()
            elif o == "-t":
                Table(args)
        if len(args) not in (1, 2):
            Usage()
        return args
    def Key(indent=" "*6):
        i = " "*4
        t.print(f"{i}{GetColor(18)}< 18.5     Underweight")
        t.print(f"{i}{GetColor(20)}18.5-25    Normal")
        t.print(f"{i}{GetColor(27)}25-30      Overweight")
        t.print(f"{i}{GetColor(31)}>30        Obese")
if 1:   # Core functionality
    def ShowMetricTable():
        print("Weight table:  lb to kg")
        m = []
        for lb in frange("90", "251", "2.5"):
            m.append(f"{lb:5.1f}  {lb*0.45359237:.1f}")
        for i in Columnize(m, col_width=15):
            print(i)
        print()
        print("Height table:  inches to m")
        m = []
        for inches in range(24, 97):
            m.append(f"{inches:3d}  {inches*0.0254:3.2f}")
        for i in Columnize(m, col_width=15):
            print(i)
        exit()

    def GetColor(bmi):
        'Return escape code for color'
        if not bmi:
            return t.n
        elif bmi < 18.5:
            return t.low
        elif 18.5 <= bmi <= 25:
            return t.normal
        elif 25 < bmi <= 30:
            return t.high
        else:
            return t.obese
    def US_Data():
        '''Table data from https://en.wikipedia.org/wiki/Body_mass_index#United_States.  Data are
        for years 2011-2014 and are for people 20 years and older.  Body mass index (BMI) in
        kg/m2.
        '''
        percentiles = (5, 10, 15, 25, 50, 75, 85, 90, 95)
        men = '''
            All   	20.7	22.2	23.0	24.6	27.7	31.6	34.0	36.1	39.8
            20–29	19.3	20.5	21.2	22.5	25.5	30.5	33.1	35.1	39.2
            30–39	21.1	22.4	23.3	24.8	27.5	31.9	35.1	36.5	39.3
            40–49	21.9	23.4	24.3	25.7	28.5	31.9	34.4	36.5	40.0
            50–59	21.6	22.7	23.6	25.4	28.3	32.0	34.0	35.2	40.3
            60–69	21.6	22.7	23.6	25.3	28.0	32.4	35.3	36.9	41.2
            70–79	21.5	23.2	23.9	25.4	27.8	30.9	33.1	34.9	38.9
            ≥ 80	20.0	21.5	22.5	24.1	26.3	29.0	31.1	32.3	33.8
        '''.strip()
        women = '''
            All   	19.6	21.0	22.0	23.6	27.7	33.2	36.5	39.3	43.3
            20–29	18.6	19.8	20.7	21.9	25.6	31.8	36.0	38.9	42.0
            30–39	19.8	21.1	22.0	23.3	27.6	33.1	36.6	40.0	44.7
            40–49	20.0	21.5	22.5	23.7	28.1	33.4	37.0	39.6	44.5
            50–59	19.9	21.5	22.2	24.5	28.6	34.4	38.3	40.7	45.2
            60–69	20.0	21.7	23.0	24.5	28.9	33.4	36.1	38.7	41.8
            70–79	20.5	22.1	22.9	24.6	28.3	33.4	36.5	39.1	42.9
            ≥ 80	19.3	20.4	21.3	23.3	26.1	29.7	30.9	32.8	35.2
        '''.strip()
        # Colors for columns
        c = {
            0: t.whtl,
            1: t.purl,
            2: t.denl,
            3: t.cyn,
            4: t.trql,
            5: t.grnl,
            6: t.trql,
            7: t.cyn,
            8: t.ornl,
            9: t.redl,
        }
        print("US adult BMI data from 2011-2014 for adults 20 years and older")
        w, indent = 7, 4
        for loc, name, category in ((35, "Men", men), (35, "Women", women)):
            t.print(f"{' '*loc}{t.yell}{name} Percentiles")
            print(" "*indent, end="")
            #                          0  1  2  3  4  5  6  7  8  9
            for i, item in enumerate("Age 5 10 15 25 50 75 85 90 95".split()):
                print(f"{c[i]}{item:^{w}s}{t.n}", end=" ")
            t.print()
            for line in category.split("\n"):
                print(" "*indent, end="")
                for i, item in enumerate(line.strip().split("\t")):
                    print(f"{c[i]}{item.strip():^{w}s}{t.n}", end=" ")
                t.print()
            print()
        exit(0)
    def Table(args):
        'Print out a BMI table'
        if args:
            h = float(args[0])*in2m
            if h > 2.2:
                print(f"'{args[0]}' inches is too tall", file=sys.stderr)
                exit(1)
        else:
            h = personal_height_inches*in2m
        bmi, dbmi = 15, 1
        print(f"For height = {flt(h/in2m)} inches = {flt(h)} m")
        print("BMI   pounds     kg")
        print("----  ------   -----")
        norm = GetColor(0)
        while bmi <= 40:
            print(f"{GetColor(bmi)}{flt(bmi)}", end="")
            m_kg = bmi*h**2
            m_lb = m_kg/lb2kg
            print(f" {m_lb:6.0f}   {m_kg:6.1f}{norm}")
            bmi += dbmi
        print("Color key:")
        Key(indent=" "*2)
        exit(0)

if __name__ == "__main__": 
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    height = personal_height_inches  # My height in inches
    if len(args) == 2:
        mass, height = [float(i) for i in args]
    else:
        mass = float(args[0])
    if not d["-m"]:
        mass *= lb2kg
        height *= in2m
    # Check mass and height for reasonableness
    mlo, mhi = 10, 200
    hlo, hhi = 0.6, 2.5
    if not (mlo <= mass <= mhi):
        Error(f"Mass must be between {mlo} and {mhi} kg")
    if not (hlo <= height <= hhi):
        Error(f"Height must be between {hlo} and {hhi} m")
    bmi = mass/height**2
    print(f"Mass   = {mass:.1f} kg = {mass/lb2kg:.0f} lb")
    print(f"Height = {height:.1f} m = {height/in2m:.1f} in")
    t.print(f"{GetColor(bmi)}BMI    = {bmi:.1f}")
