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
    from sig import sig
    import color as C
if 1:   # Global variables
    lb2kg = 0.453592
    in2m = 0.0254
    # Glenda measured my height at 69.5 inches with socks on, but I'll
    # round it down.
    personal_height_inches = 69
def GetColor(bmi):
    'Return escape code for color'
    if not bmi:
        return C.normal(s=1)
    elif bmi < 18.5:
        return C.fg(C.lcyan, s=1)
    elif 18.5 <= bmi <= 25:
        return C.fg(C.lgreen, s=1)
    elif 25 < bmi <= 30:
        return C.fg(C.yellow, s=1)
    else:
        return C.fg(C.lred, s=1)
def Key(indent=" "*6):
    if not d["-c"]:
        return
    norm = GetColor(0)
    under = GetColor(18)
    normal = GetColor(20)
    over = GetColor(27)
    obese = GetColor(31)
    print(f'''
{indent}{under}< 18.5      Underweight{norm}
{indent}{normal}18.5-25     Normal weight{norm}
{indent}{over}25-30       Overweight{norm}
{indent}{obese}>30         Obese{norm}'''[1:])
def Usage(status=1):
    name = sys.argv[0]
    print(f'''Usage:  {name} [options] mass_lbs height_inches
  Calculates and returns the body mass index for the given mass and
  height.  BMI is (mass in kg)/(height in m)^2.  General categories 
  are:''')
    Key()
    print(f'''Options:
    -c      Don't colorize the data
    -m      Mass is in kg and height in m.
    -t      Print out table of BMI (you can include a height in inches
            on the command line if you wish)''')
    exit(status)
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
    print(f"For height = {sig(h/in2m)} inches = {sig(h)} m")
    print("BMI   pounds     kg")
    print("----  ------   -----")
    norm = GetColor(0)
    while bmi <= 40:
        print(f"{GetColor(bmi)}{sig(bmi)}", end="")
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
    bmi = mass/height**2
    print("Mass   = %.1f" % mass + " kg = %.1f" % (mass/lb2kg) + " lb")
    print("Height = %.1f" % height + " m = %.1f" % (height/in2m) + " in")
    print("BMI    = %.1f" % bmi)
