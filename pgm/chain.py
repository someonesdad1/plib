'''
Calculate the layout information needed to chain-drill a hole or disk
from some sheet material by chain-drilling.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2013 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Calculate how to chain drill a hole
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from get import GetNumber
    from f import flt, pi, degrees, sin
if 1:   # Global variables
    default_unit = "inches"
    ii = isinstance
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def ParseCommandLine(d):
    d["-d"] = 3         # Number of significant digits
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
    #sig.digits = d["-d"]
    #sig.rtz = True
    flt(0).n = d["-d"]
def GetUserData(d):
    desired = d["desired"]  # It will be a lowercase letter
    # Make it 'hole' or 'disk'
    desired = {"h": "hole", "d": "disk"}[desired[0]]
    key = f"{desired}_diameter" % desired
    # Diameter
    pm = f"What is the {desired} diameter you want? "
    value, unit = GetNumber(pm, low=0, low_open=True, allow_quit=True,
                            vars=globals(), use_unit=True)
    unit = unit if unit else default_unit
    d[key] = flt(value, unit=unit)
    # Drill diameter to use
    pm = "What drill diameter will be used? "
    value, unit = GetNumber(pm, low=0, low_open=True, allow_quit=True,
                            vars=globals(), use_unit=True)
    unit = unit if unit else default_unit
    d["chain_drill"] = flt(value, unit=unit)
    # Distance between drilled hole edges
    pm = "What is the distance between the hole edges? "
    value, unit = GetNumber(pm, low=0, low_open=True, allow_quit=True,
                            vars=globals(), use_unit=True)
    unit = unit if unit else default_unit
    d["dist_betw_holes"] = flt(value, unit=unit)
    # Allowance
    pm = "What is the allowance between the final diameter and chain holes? "
    value, unit = GetNumber(pm, low=0, low_open=True, allow_quit=True,
                            vars=globals(), use_unit=True)
    unit = unit if unit else default_unit
    d["allowance"] = flt(value, unit=unit)
def GetInfo(d):
    digits = d["-d"]
    unit = default_unit
    print(dedent(f'''
    This script calculates the parameters for chain drilling a hole or a
    disk from sheet material.  Default units are {unit}; you can optionally
    type in any common unit name and it should be recognized.  Type q to exit
    at any time.  Use the -d option on the command line to change the number of
    significant figures in the report (default = {digits}).
    '''))
    opt = {"d": "disk", "h": "hole"}
    d["desired"] = "hole"
    while True:
        print(dedent('''
        Do you want to chain-drill a hole (h) or a disk (d)? ''', end=""))
        s = input("[%s] " % d["desired"][0])
        s = s.lower().strip()
        if s in opt:
            d["desired"] = opt[s]
            break
        elif s == "q":
            exit(0)
        elif not s:
            # Use default value
            break
        else:
            print("Unrecognized response\n")
    GetUserData(d)
    print()
def PrintResultsOrig(d):
    corr = 2*d["allowance"] + d["chain_drill"]
    desired = d["desired"]  # Will be 'hole' or 'disk'
    key = "%s_diameter" % desired
    D = d[key] - corr if d["desired"] == "hole" else d[key] + corr
    dbh = d["dist_betw_holes"]
    n = int((pi*D - dbh)/(d["chain_drill"] + dbh))
    if n <= 1:
        Error("Problem has no reasonable solution")
    dia = d[key]
    circ = D
    angle_radians = 2*pi/n
    theta_deg = angle_radians*180/pi
    chord = D*sin(angle_radians/2)
    chain = d["chain_drill"]
    matl_betw = chord - d["chain_drill"]
    allow = d["allowance"]
    chord = chord
    betw_hole = d["dist_betw_holes"]
    # Check for reasonableness
    if n < 1:
        print("No acceptable solution.  Try again.")
        exit(1)
    # Set up report variables in inches and mm
    dia_in = sig(dia/u("inches"))
    dia_mm = sig(dia/u("mm"))
    chain_in = sig(chain/u("inches"))
    chain_mm = sig(chain/u("mm"))
    allow_in = sig(allow/u("inches"))
    allow_mm = sig(allow/u("mm"))
    betw_hole_in = sig(betw_hole/u("inches"))
    betw_hole_mm = sig(betw_hole/u("mm"))
    matl_betw_in = sig(matl_betw/u("inches"))
    matl_betw_mm = sig(matl_betw/u("mm"))
    circ_in = sig(circ/u("inches"))
    circ_mm = sig(circ/u("mm"))
    chord_in = sig(chord/u("inches"))
    chord_mm = sig(chord/u("mm"))
    theta = sig(theta_deg)
    # Print report
    print(dedent(f'''
    Chain-drilled {desired} input data:
        Desired {desired} diameter               = {dia_in} inches ({dia_mm} mm)
        Drill diameter                      = {chain_in} inches ({chain_mm} mm)
        Distance between drilled hole edges = {betw_hole_in} inches ({betw_hole_mm} mm)
        Allowance                           = {allow_in} inches ({allow_mm} mm)
      Results:
        Number of holes to drill            = {n}
        Angle between holes                 = {theta} deg
        Minimum material between holes      = {matl_betw_in} inches ({matl_betw_mm} mm)
      Information to lay out chain holes:
        Circle for chain hole centers       = {circ_in} inches ({circ_mm} mm)
        Divider setting for hole layout     = {chord_in} inches ({chord_mm} mm)
    '''))
def PrintResults(d):
    corr = 2*d["allowance"] + d["chain_drill"]
    desired = d["desired"]  # Will be 'hole' or 'disk'
    key = f"{desired}_diameter"
    D = d[key] - corr if d["desired"] == "hole" else d[key] + corr
    dbh = d["dist_betw_holes"]
    n = int((pi*D - dbh)/(d["chain_drill"] + dbh))
    if n <= 1:
        Error("Problem has no reasonable solution")
    dia = d[key]
    circ = D
    angle_radians = 2*pi/n
    theta_deg = degrees(angle_radians)
    chord = D*sin(angle_radians/2)
    chain = d["chain_drill"]
    matl_betw = chord - d["chain_drill"]
    allow = d["allowance"]
    chord = chord
    betw_hole = d["dist_betw_holes"]
    # Check for reasonableness
    if n < 1:
        print("No acceptable solution.  Try again.")
        exit(1)
    # Set up report variables in inches and mm
    dia_in = str(dia.to("inches"))
    dia_mm = str(dia.to("mm"))
    chain_in = str(chain.to("inches"))
    chain_mm = str(chain.to("mm"))
    allow_in = str(allow.to("inches"))
    allow_mm = str(allow.to("mm"))
    betw_hole_in = str(betw_hole.to("inches"))
    betw_hole_mm = str(betw_hole.to("mm"))
    matl_betw_in = str(matl_betw.to("inches"))
    matl_betw_mm = str(matl_betw.to("mm"))
    circ_in = str(circ.to("inches"))
    circ_mm = str(circ.to("mm"))
    chord_in = str(chord.to("inches"))
    chord_mm = str(chord.to("mm"))
    theta = str(theta_deg)
    # Print report
    print(dedent(f'''
    Chain-drilled {desired} input data:
        Desired {desired} diameter               = {dia_in} ({dia_mm})
        Drill diameter                      = {chain_in} ({chain_mm})
        Distance between drilled hole edges = {betw_hole_in} ({betw_hole_mm})
        Allowance                           = {allow_in} ({allow_mm})
      Results:
        Number of holes to drill            = {n}
        Angle between holes                 = {theta} deg
        Minimum material between holes      = {matl_betw_in} ({matl_betw_mm})
      Information to lay out chain holes:
        Circle for chain hole centers       = {circ_in} ({circ_mm})
        Divider setting for hole layout     = {chord_in} ({chord_mm})
    '''))
if __name__ == "__main__":
    d = {}
    ParseCommandLine(d)
    if 0:
        GetInfo(d)
    else:
        # Debugging:  5 inch diameter, 1/4 inch diameter drill, 0.1 inches
        # between hole edges, and 0.05 from final diameter.
        if 0:
            factor = u("inches")
            d["hole_diameter"] = factor*5
            d["dist_betw_holes"] = factor*0.1
            d["desired"] = "hole"
            d["chain_drill"] = factor*0.25
            d["allowance"] = factor*0.05
        else:
            d["hole_diameter"] = flt(5, units="inches")
            d["dist_betw_holes"] = flt(0.1, units="inches")
            d["desired"] = "hole"
            d["chain_drill"] = flt(0.25, units="inches")
            d["allowance"] = flt(0.05, units="inches")
    PrintResults(d)
