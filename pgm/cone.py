'''
Sheet metal cones
    Adapted from a utility from Marv Klotz.  Defunct url is:
    http://www.myvirtualnetwork.com/mklotz/fckeditor/UserFiles/File/cone.zip
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
    # Calculate the sheet material to make a cone
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent, wrap
    from get import GetNumber as GN
    from f import flt, pi, sin, atan, degrees, radians
    from color import C
if __name__ == "__main__":
    dbg = False
    if dbg:
        #d, D, height, olap = [flt(i) for i in (50, 100, 200, 0.1)]
        # Example on pg 6 of LayingOutFrustumWithDividers.pdf
        d, D, height, olap = [flt(i) for i in (1, 3, 2, 0)]
        # Results in paper are small radius = 1.12 and large radius =
        # 3.35; subtended angle is 161° (called included angle below).
    else:
        print(wrap(dedent('''
        Calculate the details of laying out a cone on sheet metal.
        The dimensional units are arbitrary; all entries must use the
        same units.
        ''')))
        d = flt(GN("\nSmall diameter of cone? ", low=0, low_open=True))
        D = flt(GN("Large diameter of cone? ", low=0, low_open=True))
        if D < d:
            print("Large diameter must be >= small diameter")
            exit(1)
        height = flt(GN("Height of cone? ", low=0, low_open=True))
        olap = flt(GN("Overlap fraction for joining? ", low=0, high=1))
        digits = GN("Number of significant digits? ", default=4, 
                    numtype=int, low=1, high=15)
    d.n = digits
    mean_diameter = (D - d)/2
    r = mean_diameter/height
    cone_included_angle = atan(r)
    sin_incl_angle = sin(cone_included_angle)
    r1, r2 = (d/sin_incl_angle)/2, (D/sin_incl_angle)/2
    edge, c1 = r2 - r1, 0
    if r1:
        z1 = (pi*d + olap)/r1
        c1 = 2*r1*sin(z1/2)
    incl_angle_of_pattern = (pi*D + olap)/r2
    c2 = 2*r2*sin(incl_angle_of_pattern/2)
    print(dedent(f'''
    Flat pattern for sheet metal cone (C == circumference):
      Input data:
        {C.yel}Significant digits          {d.n}
        Small diameter              {d} (C = {pi*d})
        Large diameter              {D} (C = {pi*D})
        Height of cone              {height}
        Overlap allowance           {olap}{C.norm}
      Calculated data:
        Included angle of pattern   {degrees(incl_angle_of_pattern)}°
        Smaller radius of pattern   {r1}
            Chord                   {c1}
            Arc length              {incl_angle_of_pattern*r1}
        Larger radius of pattern    {r2}
            Chord                   {c2}
            Arc length              {incl_angle_of_pattern*r2}
        Length of edge              {edge}
        Cone included angle         {degrees(cone_included_angle)}°
    '''))
