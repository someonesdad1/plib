'''

Slight adjustments of the pitch of a thread

    From page 23, F. Colvin and F. Stanley, "Screw Thread Kinks", Hill
    Publishing, 1908 [sic]:

        In a nearby shop a tap was wanted on some work for export to France,
        and it was to be 1/2 inch in diameter and 1-1/2 m/m thread.

        The best lathe for the work was a 12-inch Hendey-Norton, and the
        nearest that would come to it was 17-1/2 threads per inch, or .057
        instead of .058 inch pitch, as the 1-1/2 m/m thread should be.  The
        difference was made up by setting over the tail center about 3/8 inch
        and then setting the taper attachment to the same taper.  The travel
        lost by the tool in following the taper brought the error to less than
        .00001 inch, which was near enough for the job.

    The taper attachment on the Clausing lathe can be set from 0 to 10° with
    respect to the centerline.  The increase in the tool path is the secant of
    10° or a maximum of 1.5%.  

    Thus, the pitch of a thread can be adjusted from 0 to -1.5% using this
    technique.  Note the end of the taper attachment closest to the headstock
    on the Clausing lathe has a scale which reads in the included taper angle,
    so it has to be divided by 2 to get the angle wrt the centerline.

    This script prints out the pitch adjustments that can be made with this
    technique, both in mils and mm pitch.
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2016 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Thread pitch adjustments using taper attachment.
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import math
        import getopt
        import os
        import sys
        import util
        from pdb import set_trace as xx
    if 1:   # Custom imports
        from f import flt, cos, acos, pi, tan, radians
        from wrap import dedent
        from u import u
        from color import t
    if 1:   # Global variables
        ii = isinstance
        # Data for Clausing 5914 lathe
        threading_tpi = '''
            4 4.5 5 5.5 5.75 6 6.5 6.75 7 8 9 10 11 11.5 12 13 13.5 14 16 18 20
            22 23 24 26 27 28 32 36 40 44 46 48 52 54 56 64 72 80 88 92 96 104
            108 112 128 144 160 176 184 192 208 216 224'''
        TPI = [flt(i) for i in threading_tpi.split()]
        # Angle with respect to the centerline achievable using the taper attachment.
        # The taper attachement is graduated in include angles up to 20° on either
        # side of the centerline.
        taper_attachment_angle_deg = 10
        # From https://en.wikipedia.org/wiki/ISO_metric_screw_thread#Preferred_sizes
        common_metric_pitches = '''
            .2 .25 .3 .35 .4 .45 .5 .7 .8 1.0 1.25 1.5 1.75 2 2.5 3 3.5 4 4.5 5
            5.5 6
        '''
def sTPI(tpi):
    'Return a customary string for tpi'
    assert(ii(tpi, flt))
    ip = int(tpi)
    fp = tpi - ip
    if not fp:
        return str(ip)
    if fp == 0.25:
        return str(ip) + "¼"
    elif fp == 0.5:
        return str(ip) + "½"
    elif fp == 0.75:
        return str(ip) + "¾"
    else:
        return str(tpi)
if __name__ == "__main__": 
    factor = cos(radians(taper_attachment_angle_deg))
    w = 8
    x = flt(0)
    x.rtz = x.rlz = True
    print(dedent(f'''
    Clausing thread pitches in mils and mm using taper attachment adjustment
      Max angle = 10°, leading to max pitch reduction of {factor}
                
                 Pitch, mils            Pitch, mm
    tpi         Min       Nom         Min       Nom
    ---         ----      ----        ----      ----
    '''))
    for tpi in TPI:
        if len(sys.argv) < 2 and tpi > 56:
            continue
        p = 1000/tpi                # In mils
        pmin = factor*p
        P = p*25.4/1000             # In mm
        Pmin = factor*p*25.4/1000
        print(f"{sTPI(tpi):^4s}", end=" "*6)
        print(f"{pmin!s:^{w}s}  {p!s:^{w}s}", end=" "*4)
        print(f"{Pmin!s:^{w}s}  {P!s:^{w}s}")
    if len(sys.argv) == 1:
        print("Include an argument to see all lathe pitches\n")
    print(dedent(f'''
        Common metric pitches attainable with taper settings and their errors

                                    Pitch
        Pitch,      Use    Angle    error
          mm        tpi      °        %
        ------      ---    -----    -----
          .2        128              -1.0
          .25       104              -2.4
          .3         88              -3.7
          .35        72     7.2        
          .4         64               -.8
          .45        56     7.2        
          .5         52              -2.4
          .7         36     7.2       
          .8         32               -.8
          1.0        26              -2.3
          1.25       20     10
          1.5        16     10        4.2
          1.75       14     10        2.1
          2          13              -2.3
          2.5        10     10         .1
          3           8     10        4.2 
          3.5         7     10        2.1
          4          6½              -2.3
          4.5        5½     10        1.1
          5          5      10         .1
          5.5        4½     10        1.1
          6          4      10        4.2
        '''))
