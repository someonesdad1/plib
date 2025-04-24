'''
Print PVC and steel US pipe dimensions
'''

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
if 1:  # Custom imports
    from wrap import dedent
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
