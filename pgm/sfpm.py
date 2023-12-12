'''
Calculate RPM for a desired surface speed and cutter diameter
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Calculate RPM for a desired surface speed and cutter diameter
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    from math import *
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from u import u, ParseUnit
    from f import flt
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] dia [surface_speed]
      Calculate the needed tool RPM to achieve a given surface speed for a
      given diameter.  surface_speed defaults to 100 sfpm.  The diameter dia is
      in inches be default, but you can append other units with no space
      character.
    Example:
        {sys.argv[0]} 3.1mm 600sfpm
      prints the RPM needed to achieve a 600 surface feet per minute linear
      speed for a 3.1 mm diameter bit.
    Options:
      -d n  Number of significant figures in output  [{d["-d"]}]
    
    Recommended surface speeds in sfpm:
                                   HSS        Carbide
                                 -------      -------
        Plain carbon steel, 1020   110          400
        Free machining steel       150          600
        Alloy steels              35-100      175-400
        Stainless steel             75          225
        Cast iron                   80          275
        Aluminum                   600         1200
        Brass, free cutting        350          600
        Copper alloys, harder     80-120      300-500
        Copper, OFHC               100          200
        Monel                       70          200
        Rubber, hard               150          300
        Zinc die castings        200-300     800-1200
    '''))
    exit(status)
def ParseCommandLine():
    d["-d"] = 3         # Number of significant digits
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-d",):
            try:
                d["-d"] = int(a)
                if not (1 <= d["-d"] <= 15):
                    raise ValueError()
            except ValueError:
                msg = "-d argument must be an integer between 1 and 15"
                Error(msg)
    flt(0).n = d["-d"]
    flt(0).rtz = flt(0).rtdp = True
    if len(args) not in (1, 2):
        Usage(d)
    return args
def GetDiameter(arg):
    dia_entered, unit_dia = ParseUnit(args[0])
    if not unit_dia:
        unit_dia = "inch"
    try:
        d["dia_m"] = flt(eval(dia_entered))*u(unit_dia)
        d["dia_mm"] = d["dia_m"]*1000
    except Exception:
        Error(f"'{arg}' is an invalid diameter")
    d["dia_entered"], d["unit_dia"] = dia_entered, unit_dia
def GetSurfaceSpeed(arg):
    if arg is None:
        d["surface_speed"] = flt(100)
        d["surface_speed_unit"] = "sfpm"
        d["surface_speed_m_per_s"] = flt(100*u("ft/min"))
    else:
        surface_speed, surface_speed_unit = ParseUnit(arg)
        if not surface_speed_unit:
            surface_speed_unit = "ft/min"
        try:
            surface_speed_m_per_s = (flt(eval(surface_speed)) *
                                     u(surface_speed_unit))
        except Exception:
            Error(f"'{args[1]}' is an invalid surface speed")
        d["surface_speed"] = surface_speed
        d["surface_speed_unit"] = surface_speed_unit
        d["surface_speed_m_per_s"] = surface_speed_m_per_s
def PrintReport():
    frequency_Hz = d["surface_speed_m_per_s"]/(pi*d["dia_m"])
    d["rpm"] = frequency_Hz/u("1/min")
    print(dedent(f'''
    Diameter      = {d["dia_entered"]} {d["unit_dia"]} = {d["dia_mm"]} mm
    Surface speed = {d["surface_speed"]} {d["surface_speed_unit"]} = {d["surface_speed_m_per_s"]} m/s
    RPM needed    = {d["rpm"]}
    '''))
if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine()
    GetDiameter(args[0])
    arg = args[1] if len(args) == 2 else None
    GetSurfaceSpeed(arg)
    PrintReport()
