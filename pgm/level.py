'''
Print a table of the measured sensitivity of levels
    These measurements were made with a tilting fixture on a machined 19
    mm thick aluminum plate 550 mm long by 58 mm wide.  A 1/4-28 UNF
    screw was used to change the slope of the plate in the long
    direction and a dial with 250 divisions on the screw was used to
    estimate how much the screw was turned.  I estimate the angle
    sensitivity to be about 100e-6 radians, which matches the Starrett
    98 level's sensitivity.  

    A level's sensitivity was defined to be the tilt necessary to
    produce a 0.5 mm movement of the bubble's edge, which was measured
    with a machinist's rule.  
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2010, 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Measured sensitivities of some bubble levels
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from f import flt, pi, atan, degrees
    if 0:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    # Relative cost is to a torpedo level and were gotten from web street
    # prices in March of 2010.  Sensitivity is the angle of tilt in
    # millidegrees needed to move the bubble 1/2 mm.
    levels = (
        # Name, relative cost, measured sensitivity in millidegrees
        ("Johnson torpedo level", 1, flt(97)),
        ("Checkpoint laser level", 2, flt(74)),
        ("Line level, Stanley", 0.1, flt(69)),
        ("Starrett combination square", 6, flt(36)),
        ("Starrett 134 cross test level", 3, flt(20)),
        ("Starrett 133 plumber's level, 15 inch", 23, flt(9.7)),
        ("Starrett 98 level", 7, flt(4.6)),
        # The following two sensitivities are estimated
        ("Starrett 199 precision level, 15 inch", 40, flt(0.57)),
        ("Grizzly H2682 precision level, 15 inch", 5, flt(0.29)),
    )
def Header():
    print(dedent('''
    Commercial shop levels
    ----------------------
                                              Relative        Sensitivity [1],
                                              Cost [2]          millidegrees
                                              --------        ----------------
    '''))
def PrintItem(name, relcost, sensitivity_mdeg):
    indent = " "*0
    fmt = "{}{:44s} {:^4s} {:>16s}"
    #print(fmt.format(indent, name, relcost, sensitivity_mdeg), end="")
    print(f"{name:44s} {relcost!s:^4s} {sensitivity_mdeg!s:>15s}", end="")
    if "199" in name or "Grizzly" in name:
        print("    [3]", end="")
    print()
def Trailer():
    print(dedent('''
    Notes:
      [1] Measured tilt for 1/2 mm bubble movement
      [2] From web street prices in 2010
      [3] estimated
    '''))
    # Sensitivities in different units
    digits = 2
    print(dedent(f'''

    Sensitivities (to {digits} figures)
    ----------------------------
                                      mils per   mm per
      1 in X  millidegrees   urad       foot        m
      ------  ------------  ------    --------   ------
    '''))
    fmt = "  {:>6d}  {:^12s}  {:>6s}     {:^8s}   {:^6s}"
    x = flt(0)
    with x:
        x.n = 2
        for i in (500, 750, 1000, 2000, 5000, 10000, 20000):
            θ = flt(atan(1/i))
            angle_urad = 1e6*θ
            angle_mdeg = 1000*flt(degrees(θ))
            slope = 12*1000*flt(1/i)
            mm_per_m = 1/flt(i)
            print(f"  {i:>6d}  {angle_mdeg!s:^12s}   {angle_urad!s:>4s}"
                  f"     {slope!s:^8s}   {mm_per_m!s:^6s}")
if __name__ == "__main__":
    x = flt(0)
    x.n = 3
    x.rtz = True
    Header()
    for name, relcost, sensitivity_mdeg in levels:
        PrintItem(name, relcost, sensitivity_mdeg)
    Trailer()
