'''
Print US pipe dimensions
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
        import sys
    if 1:  # Custom imports
        from f import flt
        from color import t
        from wrap import dedent
        import termtables as tt
        if len(sys.argv) > 1:
            import debug       
            debug.SetDebugger()
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
    def PipeSizes(metric=False):
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
            Fraction(3, 8): (675,    90, 18,    612, 1000*(37/64)),
            Fraction(1, 2): (840 ,  109, 14,    758, 1000*(23/32),   147/1000),
            Fraction(3, 4): (1050,  113, 14,    968, 1000*(59/64),   154/1000),
            Fraction(1, 1): (1315,  133, 11.5, 1214, 1000*(1+5/32),  179/1000),
            Fraction(5, 4): (1660,  140, 11.5, 1557, 1000*(1+1/2),   191/1000),
            Fraction(3, 2): (1900,  145, 11.5, 1796, 1000*(1+47/64), 200/1000),
            Fraction(2, 1): (2375,  154, 11.5, 2269, 1000*(2+7/32),  218/1000),
            Fraction(5, 2): (2875,  203, 8,    2720, 1000*(2+5/8)),
            Fraction(3, 1): (3500,  216, 8,    3341, 1000*(3+1/4)),
            Fraction(7, 2): (3000,  226, 8,    3838, 1000*(3+3/4)),
            Fraction(4, 1): (4500,  237, 8,    4334, 1000*(4+1/4)),
            Fraction(5, 1): (5563,  258, 8,    5391, 1000*(1.22)),
            Fraction(6, 1): (6625,  280, 8,    6446, 1000*(1.58)),
        }
        def FF(fraction):
            'Return a formatted fraction string'
            i, r = divmod(fraction.numerator, fraction.denominator)
            if not r:
                return f"{i}"
            elif i:
                return f"{i}-{r}/{fraction.denominator}"
            else:
                return f"{r}/{fraction.denominator}"
        # Set up flt formatting
        x = flt(0)
        x.rtz = x.rdp = True
        # Table title
        t.title = t.purl if metric else t.ornl 
        t.body = t.sky if metric else t.whtl
        if metric:
            print(f"{' '*28}{t.title}", "US Pipe sizes in mm", t.body)
        else:
            print(f"{' '*25}{t.title}", "US Pipe sizes in inches", t.body)
        # Build table data
        p = " "*1
        header = [
            f"{p}Size{p}",
            f"{p}OD  {p}",
            f"{p}Wall{p}",
            f"{p}ID {p}",
            f"{p}tpi{p}" if not metric else f"{p}   {p}",
            f"{p}pitch{p}" ,
            f"{p}PD  {p}",
            f"{p}Tap drill{p}",
            f"{p}Wall80{p}",
            f"{p}ID80{p}"
        ]
        data = [[
            f"{p}{'-'*5}{p}",   # Size
            f"{p}{'-'*6}{p}",   # OD
            f"{p}{'-'*5}{p}",   # Wall
            f"{p}{'-'*5}{p}",   # ID
            f"{p}{'-'*4}{p}" if not metric else f"{p}   {p}",   # tpi
            f"{p}{'-'*6}{p}",   # pitch
            f"{p}{'-'*6}{p}",   # PD
            f"{p}{'-'*9}{p}",   # TD
            f"{p}{'-'*6}{p}",   # Wall80
            f"{p}{'-'*6}{p}"    # ID80
        ]]
        assert(len(header) == len(data[0]))
        for k in sch40:
            entry = sch40[k]
            #print(f"{i!s:5s} {FF(k)}")
            if len(entry) == 5:
                OD, wall, tpi, PD, TD = [flt(j) for j in entry]
                wall80 = 0
            else:
                OD, wall, tpi, PD, TD, wall80 = [flt(j) for j in entry]
            # Get columns
            size = FF(k)
            OD, wall, PD, TD = [flt(j)/1000 for j in (OD, wall, PD, TD)]
            ID = OD - 2*wall
            pitch = 1/tpi
            ID80 = OD - 2*wall80 if wall80 else 0
            if metric:
                n, m = 1, 25.4
                elem = [f"{p}{size}{p}", 
                        f"{p}{m*OD:>.{n}f}{p}", 
                        f"{p}{m*wall:>.{n}f}{p}", 
                        f"{p}{m*ID:>.{n}f}{p}", 
                        f"{p}{''}{p}", 
                        f"{p}{m*pitch:>.{n}f}{p}", 
                        f"{p}{m*PD:>.{n}f}{p}", 
                        f"{p}{m*TD:>.{n}f}{p}", 
                        f"{p}{m*wall80:>.{n}f}{p}" if wall80 else f"{p}{p}", 
                        f"{p}{m*ID80:>.{n}f}{p}" if wall80 else f"{p}{p}", 
                ]
            else:
                n = 3
                elem = [f"{p}{size}{p}", 
                        f"{p}{OD:>.{n}f}{p}", 
                        f"{p}{wall:>.{n}f}{p}", 
                        f"{p}{ID:>.{n}f}{p}", 
                        f"{p}{tpi}{p}", 
                        f"{p}{pitch:>.{n + 1}f}{p}", 
                        f"{p}{PD:>.{n}f}{p}", 
                        f"{p}{TD:>.{n}f}{p}", 
                        f"{p}{wall80:>.{n}f}{p}" if wall80 else f"{p}{p}",
                        f"{p}{ID80:>.{n}f}{p}" if wall80 else f"{p}{p}"
                ]
            assert(len(header) == len(elem))
            data.append(elem)
        tt.print(data, header=header, padding=(0, 0), style=None, alignment="r"*len(header))
    PipeSizes(metric=True)
    t.print()
    PipeSizes(metric=False)
