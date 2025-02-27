"""

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
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2016 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Thread pitch adjustments using taper attachment
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import math
        import getopt
        import os
        import sys
        import util
        from pdb import set_trace as xx
    if 1:  # Custom imports
        from f import flt, cos, acos, pi, tan, radians
        from wrap import dedent
        from u import u
        from color import t
    if 1:  # Global variables
        ii = isinstance
        # Data for Clausing 5914 lathe
        threading_tpi = """
            4 4.5 5 5.5 5.75 6 6.5 6.75 7 8 9 10 11 11.5 12 13 13.5 14 16 18 20
            22 23 24 26 27 28 32 36 40 44 46 48 52 54 56 64 72 80 88 92 96 104
            108 112 128 144 160 176 184 192 208 216 224"""
        TPI = [flt(i) for i in threading_tpi.split()]
        # Angle with respect to the centerline achievable using the taper attachment.
        # The taper attachment is graduated in include angles up to 20° on either
        # side of the centerline.
        taper_attachment_angle_deg = 10
        # From https://en.wikipedia.org/wiki/ISO_metric_screw_thread#Preferred_sizes
        common_metric_pitches = """
            .2 .25 .3 .35 .4 .45 .5 .7 .8 1.0 1.25 1.5 1.75 2 2.5 3 3.5 4 4.5 5
            5.5 6
        """


def sTPI(tpi):
    "Return a customary string for tpi"
    assert ii(tpi, flt)
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


def Klotz():
    """M. Klotz has a file data.zip that has a metric.txt file in it.  This
    is useful to print a table of metric & inch threads.  Contents of file:

        Standard metric screws and their Imperial equivalents

        dm = diameter (mm)
        pm = pitch (mm)
        di = diameter (in)
        pi = pitch (tpi)
        tdm = tap drill size (mm)
        tdi = tap drill size (in)

        dm  x  pm   (  di  x  pi )    tdm  ( tdi )  easily confused with

        1.6 x 0.35  (0.063 x 72.6)   1.25  (0.049)  [0-80 = 0.060 x 80]
        1.8 x 0.35  (0.071 x 72.6)   1.45  (0.057)  [1-72 = 0.073 x 72]
        2.0 x 0.40  (0.079 x 63.5)   1.60  (0.063)  [2-64 = 0.085 x 64]
        2.2 x 0.45  (0.087 x 56.4)   1.75  (0.069)  [2-56 = 0.085 x 56]
        2.5 x 0.45  (0.098 x 56.4)   2.05  (0.081)  [3-56 = 0.099 x 56]
        3.0 x 0.50  (0.118 x 50.8)   2.50  (0.098)  [4-48 = 0.112 x 48]
        3.5 x 0.60  (0.138 x 42.3)   2.90  (0.114)  [6-40 = 0.138 x 40]
        4.0 x 0.70  (0.157 x 36.3)   3.30  (0.130)  [8-36 = 0.164 x 36]
        4.5 x 0.75  (0.177 x 33.9)   3.75  (0.148)
        5.0 x 0.80  (0.197 x 31.8)   4.20  (0.165)  [10-32 = 0.190 x 32]
        6.0 x 1.00  (0.236 x 25.4)   5.00  (0.197)  [1/4-28 = 0.25 x 28]
        7.0 x 1.00  (0.276 x 25.4)   6.00  (0.236)
        8.0 x 1.25  (0.315 x 20.3)   6.75  (0.266)
        8.0 x 1.00  (0.315 x 25.4)   7.00  (0.276)
        10.0 x 1.50  (0.394 x 16.9)   8.50  (0.335)
        10.0 x 1.25  (0.394 x 20.3)   8.75  (0.344)
        12.0 x 1.75  (0.472 x 14.5)  10.25  (0.404)
        12.0 x 1.25  (0.472 x 20.3)  10.75  (0.423)
        14.0 x 2.00  (0.551 x 12.7)  12.00  (0.472)
        14.0 x 1.50  (0.551 x 16.9)  12.50  (0.492)
        16.0 x 2.00  (0.630 x 12.7)  14.00  (0.551)
        16.0 x 1.50  (0.630 x 16.9)  14.50  (0.571)
        18.0 x 2.50  (0.709 x 10.2)  15.50  (0.610)
        18.0 x 1.50  (0.709 x 16.9)  16.50  (0.650)
        20.0 x 2.50  (0.787 x 10.2)  17.50  (0.689)
        20.0 x 1.50  (0.787 x 16.9)  18.50  (0.728)
        22.0 x 2.50  (0.866 x 10.2)  19.50  (0.768)
        22.0 x 1.50  (0.866 x 16.9)  20.50  (0.807)
        24.0 x 3.00  (0.945 x  8.5)  21.00  (0.827)
        24.0 x 2.00  (0.945 x 12.7)  22.00  (0.866)
        27.0 x 3.00  (1.063 x  8.5)  24.00  (0.945)
        27.0 x 2.00  (1.063 x 12.7)  25.00  (0.984)
    """
    data = """
        1.6 x 0.35,  0.063 x 72.6,   1.25,  0.049,  0-80 = 0.060 x 80
        1.8 x 0.35,  0.071 x 72.6,   1.45,  0.057,  1-72 = 0.073 x 72
        2.0 x 0.40,  0.079 x 63.5,   1.60,  0.063,  2-64 = 0.085 x 64
        2.2 x 0.45,  0.087 x 56.4,   1.75,  0.069,  2-56 = 0.085 x 56
        2.5 x 0.45,  0.098 x 56.4,   2.05,  0.081,  3-56 = 0.099 x 56
        3.0 x 0.50,  0.118 x 50.8,   2.50,  0.098,  4-48 = 0.112 x 48
        3.5 x 0.60,  0.138 x 42.3,   2.90,  0.114,  6-40 = 0.138 x 40
        4.0 x 0.70,  0.157 x 36.3,   3.30,  0.130,  8-36 = 0.164 x 36
        4.5 x 0.75,  0.177 x 33.9,   3.75,  0.148,
        5.0 x 0.80,  0.197 x 31.8,   4.20,  0.165,  10-32 = 0.190 x 32
        6.0 x 1.00,  0.236 x 25.4,   5.00,  0.197,  1/4-28 = 0.25 x 28
        7.0 x 1.00,  0.276 x 25.4,   6.00,  0.236,
        8.0 x 1.25,  0.315 x 20.3,   6.75,  0.266,
        8.0 x 1.00,  0.315 x 25.4,   7.00,  0.276,
        10.0 x 1.50, 0.394 x 16.9,   8.50,  0.335,
        10.0 x 1.25, 0.394 x 20.3,   8.75,  0.344,
        12.0 x 1.75, 0.472 x 14.5,  10.25,  0.404,
        12.0 x 1.25, 0.472 x 20.3,  10.75,  0.423,
        14.0 x 2.00, 0.551 x 12.7,  12.00,  0.472,
        14.0 x 1.50, 0.551 x 16.9,  12.50,  0.492,
        16.0 x 2.00, 0.630 x 12.7,  14.00,  0.551,
        16.0 x 1.50, 0.630 x 16.9,  14.50,  0.571,
        18.0 x 2.50, 0.709 x 10.2,  15.50,  0.610,
        18.0 x 1.50, 0.709 x 16.9,  16.50,  0.650,
        20.0 x 2.50, 0.787 x 10.2,  17.50,  0.689,
        20.0 x 1.50, 0.787 x 16.9,  18.50,  0.728,
        22.0 x 2.50, 0.866 x 10.2,  19.50,  0.768,
        22.0 x 1.50, 0.866 x 16.9,  20.50,  0.807,
        24.0 x 3.00, 0.945 x  8.5,  21.00,  0.827,
        24.0 x 2.00, 0.945 x 12.7,  22.00,  0.866,
        27.0 x 3.00, 1.063 x  8.5,  24.00,  0.945,
        27.0 x 2.00, 1.063 x 12.7,  25.00,  0.984,"""[1:]
    t.m = t("royl")
    t.i = t("yell")
    t.conf = t("ornl")
    t.print(f"\n{t('purl')}Metric thread to Inch thread comparison")
    print("Dia  Pitch                     Tap Drill         Confused")
    print(" mm    mm   Inch dia & tpi     mm   inch           with")
    for line in data.split("\n"):
        f = [i.strip() for i in line.split(",")]
        # Metric thread size f[0]
        dm, _, pitch = f[0].split()
        dm, pitch = flt(dm), flt(pitch)
        print(f"{t.m}{dm!s:^4s}  {pitch!s:^4s}{t.n}", end=" " * 3)
        # Inch dia, tpi
        di, _, tpi = [i.strip() for i in f[1].split()]
        s = di + "-" + tpi
        print(f"{t.i}{s:^12s}{t.n}", end=" " * 4)
        # Tap drill
        tdm, tdi = [i.strip() for i in (f[2], f[3])]
        print(f"{t.m}{tdm:>5s}{t.n}  {t.i}{tdi:^5s}{t.n}", end=" " * 4)
        # Confused with
        if len(f) > 4:
            print(f"{t.conf}{f[4]}{t.n}", end="")
        print()


if __name__ == "__main__":
    factor = cos(radians(taper_attachment_angle_deg))
    w = 8
    x = flt(0)
    x.rtz = x.rlz = True
    print(
        dedent(f"""
    Clausing thread pitches in mils and mm using taper attachment adjustment
      Max angle = 10°, leading to max pitch reduction of {factor}
                
                 Pitch, mils            Pitch, mm
    tpi         Min       Nom         Min       Nom
    ---         ----      ----        ----      ----
    """)
    )
    for tpi in TPI:
        if len(sys.argv) < 2 and tpi > 56:
            continue
        p = 1000 / tpi  # In mils
        pmin = factor * p
        P = p * 25.4 / 1000  # In mm
        Pmin = factor * p * 25.4 / 1000
        print(f"{sTPI(tpi):^4s}", end=" " * 6)
        print(f"{pmin!s:^{w}s}  {p!s:^{w}s}", end=" " * 4)
        print(f"{Pmin!s:^{w}s}  {P!s:^{w}s}")
    if len(sys.argv) == 1:
        print("Include an argument to see all lathe pitches\n")
    print(
        dedent(f"""
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
        """)
    )
    Klotz()
