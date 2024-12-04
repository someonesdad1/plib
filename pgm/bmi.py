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
        from wrap import dedent
        from f import flt
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
          -c      Don't colorize the data
          -m      Mass is in kg and height in m.
          -t      Print out table of BMI (you can include a height in inches
                  on the command line if you wish)
        '''))
        exit()
    def ParseCommandLine(d):
        d["-c"] = True
        d["-m"] = False
        d["-t"] = False
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "cmt")
        except getopt.GetoptError as str:
            msg, option = str
            print(msg)
            sys.exit(1)
        for opt in optlist:
            if opt[0] == "-c":
                d["-c"] = not d["-c"]
            elif opt[0] == "-m":
                d["-m"] = True
            if opt[0] == "-t":
                Table(args)
        if len(args) not in (1, 2):
            Usage()
        return args
    def Key(indent=" "*6):
        if not d["-c"]:
            return
        i = " "*4
        t.print(f"{i}{GetColor(18)}< 18.5     Underweight")
        t.print(f"{i}{GetColor(20)}18.5-25    Normal")
        t.print(f"{i}{GetColor(27)}25-30      Overweight")
        t.print(f"{i}{GetColor(31)}>30        Obese")
if 1:   # Core functionality
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
        if d["-c"]:
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
