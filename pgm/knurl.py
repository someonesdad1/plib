'''
Print out tables for the diameters that fit an integer number of knurl
pitches around the circumference.
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
    # Knurling utility
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import os
    from math import pi
if 1:   # Custom imports
    from wrap import dedent
    from columnize import Columnize
if 1:   # Global variables
    # Note:  the height is the depth of the knurling teeth.  This is used to
    # estimate the diameter growth of a fully-formed knurl (which will be
    # double this height).  I measured this from the knurls using a 10X
    # loupe and a rule graduated in 0.01 inches.  It's probably best to
    # determine this empirically for each knurl by measuring the actual
    # increase, as the rule-measured numbers come out a little large in my
    # experience.
    knurls = [
        # All dimensions in inches:
        #   Name, diameter, number of teeth, height
        # The knurls are printed out in reverse order so that the first one
        # in the list is last.
        ("Enco holder", 0.75, 40, 0.025),
        ("2 mm pitch", 1.027, 41, 0.02),
        ("1 mm pitch", 1.027, 82, 0.015),
        ("0.5 mm pitch", 1.027, 164, 0.01),
        ("Straight 1 wheel", 0.706, 100, 0.015),
        ("Reed SS20", 0.75, 48, 0.03),
        ("Reed BM20", 0.622, 33, 0.03),
        ("Unknown straight wheel pair", 0.74, 24, 0.1),
    ]
def PrintKnurlTable(knurl_data, Dmax=2):
    '''Print a table of ideal knurling diameters up to Dmax to fit an
    integral number of pitches around the circumference.
 
    NOTE:  all dimensions are in inches.
    '''
    name, dia, number_of_teeth, height = knurl_data
    n = 2   # Number of teeth around work circumference
    D = 0   # Calculated diameter for integer no. of teeth around circumference
    pitch = dia*pi/number_of_teeth
    diameters = []
    while True:
        D = n*pitch/pi
        s = f"{D:5.3f} [{n}]"
        if D < 0.1:
            n += 1
            continue    
        if D >= Dmax:
            break
        diameters.append(s)
        n += 1
    print(f"Knurl:  {name}    [diameter = {dia} inches, {number_of_teeth} teeth]")
    for i in Columnize(diameters, indent=" "*2, sep=" "*3):
        print(i)
    s = f"Maximum diameter increase = {2*height:.2f} inches"
    print(f"{s:^{W}s}")
    print()
if __name__ == "__main__":
    try:
        W = screen_width = int(os.environ["COLUMNS"])
    except Exception:
        W = 80
    print(f"{'Workpiece diameter in inches for perfect knurling':^{W}s}")
    print(dedent('''
    The maximum diameter increase is the estimate in inches of how much larger
    a fully-formed knurl will be over the starting diameter.  [X] is the
    integer number of knurl pitches around the circumference.
    ''')
    for i in reversed(range(len(knurls))):
        PrintKnurlTable(knurls[i])
