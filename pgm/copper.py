'''
Print out copper pipe sizes.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2019 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Copper pipe sizes
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import os
    import sys
    from math import pi
    from collections import OrderedDict
    from pdb import set_trace as xx
if 1:   # Custom imports
    from u import u
    from wrap import dedent
if 1:   # Global variables
    copper_density_g_per_cc = 8.96*u("g/cc")
    copper_density_lb_per_cubic_inch = copper_density_g_per_cc/u("lb/in3")
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Data():
    '''Return a dictionary keyed by the tubing nominal size in inches.
    '''
    # Data from https://www.sizes.com/materials/pipeCopper.htm
    #   Type K:  heaviest wall, underground burial
    #   Type L:  most common size
    #   Type M:  thin wall, low pressure
    return OrderedDict((
        # Nom     OD     ID_K   ID_L   ID_M
        ("3/8",   [1/2,   0.402, 0.430, 0.450]),
        ("1/2",   [5/8,   0.528, 0.545, 0.569]),
        ("5/8",   [3/4,   0.652, 0.668, 0.690]),
        ("3/4",   [7/8,   0.745, 0.785, 0.811]),
        ("1",     [1+1/8, 0.995, 1.025, 1.055]),
        ("1-1/4", [1+3/8, 1.245, 1.265, 1.291]),
        ("1-1/2", [1+5/8, 1.481, 1.505, 1.527]),
        ("2",     [2+1/8, 1.959, 1.985, 2.009]),
    ))
if __name__ == "__main__":
    data = Data()
    print(dedent(f'''
                         Copper Tubing and Pipe
                         ----------------------
    
    Nominal size is 1/8 inch less than actual outside diameter.  Type K is
    heaviest wall, typically used for underground applications.  Tyle L is the
    most common.  Type M is the lightest wall for low cost and low pressure.
    "Hard" pipe is drawn and unannealed; "soft" pipe is annealed.  You can
    anneal copper by heating it red hot and quenching in water.  Do not use
    flare fittings on copper unless it has been annealed because it can split
    when you flare it.
     
    Dimensions in inches
                                Inside Diameter
    Nominal     OD      Type K      Type L      Type M
    -------   ------    ------      ------      ------
    '''))
    f = "{:^7s}   {:6.3f}    {:6.3f}      {:6.3f}      {:6.3f}"
    f = "{{:^7s}}   {}    {{:6.3f}}      {{:6.3f}}      {{:6.3f}}"
    for size, j in data.items():
        OD, ID_K, ID_L, ID_M = j
        print(f.format("{:6.3f}").format(size, *j))
    print()
    # Mass per unit length
    print("Mass per unit length in lb/ft")
    for size, j in data.items():
        OD, ID_K, ID_L, ID_M = j
        m = lambda ID: pi*12*(OD**2 - ID**2)/4
        print(f.format(" "*6).format(size, m(ID_K), m(ID_L), m(ID_M)))

