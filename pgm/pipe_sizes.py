'''
Print PVC and steel US pipe dimensions
'''

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # PVC and steel US standard pipe dimensions
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from fractions import Fraction
    if 1:  # Custom imports
        from wrap import dedent
        import termtables as tt
if 0:   # Original implementation
    print(
        dedent(f'''
              Schedule 40 PVC pipe                    Schedule 80 PVC pipe
        Nominal                                 Nominal
         Size      OD      Wall      ID          Size      OD      Wall      ID
        -------   -----    -----    -----       -------   -----    -----    -----
         1/2      0.840    0.109    0.622        1/2      0.840    0.147    0.546
         3/4      1.050    0.113    0.824        3/4      1.050    0.154    0.742
         1        1.315    0.133    1.049        1        1.315    0.179    0.957
         1-1/4    1.660    0.140    1.380        1-1/4    1.660    0.191    1.278
         1-1/2    1.900    0.145    1.610        1-1/2    1.900    0.200    1.500
         2        2.375    0.154    2.067        2        2.375    0.218    1.939
        
        Schedule 40 steel pipe
        ----------------------
            Taper = 3/4" per foot = 1 in 16 = 3.56° included angle
            PD measured at start of external thread
        
        Nominal
        Pipe     Pipe     Pipe                   Thread    Pitch     Weight   Tap
        Size      OD       ID      Wall   tpi    Pitch    diameter  lb/inch  Drill
        -----    ------   ------  -----   ---    ------   --------  -------  -----
        1/8      0.405    0.269   0.070   27     0.0370    0.364     0.020   0.339
        1/4      0.540    0.364   0.090   18     0.0556    0.477     0.035   7/16
        3/8      0.675    0.493   0.090   18     0.0556    0.612     0.047   37/64
        1/2      0.840    0.622   0.109   14     0.0714    0.758     0.071   23/32
        3/4      1.050    0.824   0.113   14     0.0714    0.968     0.094   59/64
        1        1.315    1.049   0.133   11.5   0.0870    1.214     0.140   1-5/32
        1 1/4    1.660    1.380   0.140   11.5   0.0870    1.557     0.189   1-1/2
        1 1/2    1.900    1.610   0.145   11.5   0.0870    1.796     0.226   1-47/64
        2        2.375    2.067   0.154   11.5   0.0870    2.269     0.304   2-7/32
        2 1/2    2.875    2.469   0.203   8      0.1250    2.720     0.482   2-5/8
        3        3.500    3.068   0.216   8      0.1250    3.341     0.631   3-1/4
        3 1/2    3.000    3.548   0.226   8      0.1250    3.838     0.758   3-3/4
        4        4.500    4.026   0.237   8      0.1250    4.334     0.898   4-1/4
        5        5.563    5.047   0.258   8      0.1250    5.391     1.22
        6        6.625    6.065   0.280   8      0.1250    6.446     1.58
        ''')
    )
if 1:   # Using dimensions
    o8, oq, oh, tq, t8 = "⅛ ¼ ½ ¾ ⅜".split()
    sch40 = {
        # Key is fractional size
        # Value fields in mils are
        #   OD
        #   Wall
        #   tpi
        #   PD
        #   Tap drill
        #   Sch80 PVC wall thickness
        Fraction(1, 8): (405,    70, 27,    364, 339),
        Fraction(1, 4): (540,    90, 18,    477, 438),
        Fraction(3, 8): (675,    90, 18,    612, 37000/64),
        Fraction(1, 2): (840 ,  109, 14,    758, 23/32,        147),
        Fraction(3, 4): (1050,  113, 14,    968, 59/64,        154),
        Fraction(1, 1): (1315,  133, 11.5, 1214, 1+5/32,       179),
        Fraction(5, 4): (1660,  140, 11.5, 1557, 1+1/2,        191),
        Fraction(3, 2): (1900,  145, 11.5, 1796, 1+47/64,      200),
        Fraction(2, 1): (2375,  154, 11.5, 2269, 2+7/32,       218),
        Fraction(5, 2): (2875,  203, 8,    2720, 2+5/8),
        Fraction(3, 1): (3500,  216, 8,    3341, 3+1/4),
        Fraction(7, 2): (3000,  226, 8,    3838, 3+3/4),
        Fraction(4, 1): (4500,  237, 8,    4334, 4+1/4),
        Fraction(5, 1): (5563,  258, 8,    5391, 1.22),
        Fraction(6, 1): (6625,  280, 8,    6446, 1.58),
    }
    def FF(fraction):
        'Return a formatted fraction string'
        i, r = divmod(fraction.numerator, fraction.denominator)
        if fraction.denominator == 8:
            if r == 1:
                return o8
            elif r == 3:
                return t8
            else:
                raise ValueError
        elif fraction.denominator == 4:
            if r == 1:
                if i == 0:
                    return oq
                else:
                    return f"1{oq}"
            elif i == 0 and r == 3:
                return tq
            elif r == 3:
                return tq
            else:
                raise ValueError
        elif fraction.denominator == 2:
            if r == 1:
                if i == 1:
                    return f"1{oh}"
                elif i == 2:
                    return f"2{oh}"
                elif i == 3:
                    return f"3{oh}"
                else:
                    return oh
            else:
                raise ValueError
        else:
            return str(int(fraction))
    # Build table data
    for i in sch40:
        print(i, FF(i))
