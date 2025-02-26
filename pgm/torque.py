"""
Prints out data on bolts & torques
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2018 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Torque data on bolts
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    from pprint import pprint as pp
    from pdb import set_trace as xx
if 1:  # Custom imports
    from u import u
    from roundoff import RoundOff
    from sig import sig
    from f import flt
    from wrap import dedent, wrap


def GetInchBoltData():
    def Convert(f):
        "Convert the strings in ft*lb to floats in N*m"
        for i, s in enumerate(f):
            if i > 1:
                f[i] = flt(s) * u("ft*lb")
        return f

    # From https://www.boltdepot.com/fastener-information/Bolts/US-Recommended-Torque.aspx
    # Fields
    #   Size
    #   Grade 2 coarse
    #   Grade 2 fine
    #   Grade 5 coarse
    #   Grade 5 fine
    #   Grade 8 coarse
    #   Grade 8 fine
    #   18/8 SST coarse
    #   18/8 SST fine
    #   Bronze coarse
    #   Bronze fine
    #   Brass coarse
    #   Brass fine
    data = """
    1/4 	4 	4.7 	6.3 	7.3 	9 	10 	6.3 	7.8 	5.7 	7.3 	5.1 	6.4
    5/16 	8 	9 	13 	14 	18 	20 	11 	11.8 	10.3 	10.9 	8.9 	9.7
    3/8 	15 	17 	23 	26 	33 	37 	20 	22 	18 	20 	16 	18
    7/16 	24 	27 	37 	41 	52 	58 	31 	33 	29 	31 	26 	27
    1/2 	37 	41 	57 	64 	80 	90 	43 	45 	40 	42 	35 	37
    9/16 	53 	59 	82 	91 	115 	129 	57 	63 	53 	58 	47 	51
    5/8 	73 	83 	112 	128 	159 	180 	93 	104 	86 	96 	76 	85
    3/4 	125 	138 	200 	223 	282 	315 	128 	124 	104 	102 	118 	115
    7/8 	129 	144 	322 	355 	454 	501 	194 	193 	178 	178 	159 	158
    1 	188 	210 	483 	541 	682 	764 	287 	289 	265 	240 	235 	212
    """
    inch = []
    for line in data.split("\n"):
        line = line.strip()
        if not line:
            continue
        f = [i.strip() for i in line.split("\t")]
        inch.append(f)
    # Print report
    print("Inch-size bolts")
    print("""                            Recommended torque in ft*lb
       Grade 2     Grade 5     Grade 8    18/8 SST     Bronze       Brass
Size  UNC   UNF   UNC   UNF   UNC   UNF   UNC   UNF   UNC   UNF   UNC   UNF""")
    for i in inch:
        print("{:6s}".format(i[0]), end="")
        s = i[1:]
        for j in i[1:]:
            print("{:5s}".format(j), end=" ")
        print()
    print()
    print(
        wrap("""
    My 3/4 Plomb breaker bar has an effective lever arm of about 20 inches.
    Using a 1-1/8 inch 1/2 inch drive socket on a 6" extension and a 3/4 to
    1/2 adapter, I can just loosen the 3/4 UNF bolts on our load transferring
    hitch.
    """)
    )


def GetMetricBoltData():
    """From https://www.engineeringtoolbox.com/metric-bolts-maximum-torque-d_2054.html"""

    def Convert(x):
        """Convert x to a float and convert it from N*m to ft*lbf.  If it's
        the empty string, just return an empty string.
        """
        try:
            t = float(x) / u("ft*lbf")
            if t < 10:
                return str(round(t, 1))
            else:
                return sig(t, 2)
        except Exception:
            return ""

    # Fields
    #   Size in mm
    #   Grade 8.8 maximum tightening torque in N*m
    #   Grade 9.8 maximum tightening torque in N*m
    #   Grade 10.9 maximum tightening torque in N*m
    #   Grade 12.9 maximum tightening torque in N*m
    data = """
        5 	7.0 	7.8 	10.0 	11.7
        6 	11.8 	13.3 	17.0 	19.9
        8 	28.8 	32.3 	41.3 	48.3
        10 	57.3 	64.1 	81.8 	95.7
        12 	99.8 	112 	143 	167
        16 	248 	277 	354 	413
        20 	500 		690 	809
        24 	865 		1195 	1395
        30 	1719 		2377 	2774
    """
    metric = []
    for line in data.split("\n"):
        line = line.strip()
        if not line:
            continue
        f = [i.strip() for i in line.split("\t")]
        dia = int(f[0])
        s = [Convert(i) for i in f[1:]]
        metric.append([dia] + s)
    # Print report
    print("\nMetric bolts")
    print("""
                  Recommended torque in ft*lb
                          Bolt Grade 
Dia, mm      8.8        9.8        10.9       12.9
-------      ----       ----       -----      -----""")
    for i in metric:
        print("{:2d}          ".format(i[0]), end=" ")
        for j in i[1:]:
            print("{:10s}".format(j), end=" ")
        print()


def Torques():
    """These measurements were made using a Utica torque wrench that I
    calibrated using a home-made tool and accurately measured volumes of
    water for known weights.  Calibration uncertainty was under 0.5%.
    """
    print()
    print(
        wrap("""
    Wrench Torque Measurements (using calibrated torque wrench on 3/8 bolt,
    so wrench/socket was 9/16 inches).  These measurements were made when I
    was 66 and are my personal limits for what I can apply with one hand at
    the bench.  Much of the limiting factor was how uncomfortable the tool
    was in my hand.  The most comfortable tools were the two 3/8 inch drive
    ratchets marked with *.  The Force column is the calculated force I
    applied to the tool -- and note they are pretty consistent for the 
    short versus long tools.""")
    )
    print("""
                                Torque,    ELA,     Force,
 No.         Wrench             ft-lbf    inches     lbf    Model
 ---   ---------------------    ------    ------    ------  -----
  1    Challenger open end        29        5         70    5418
  2    SO short box               29        4.9       72    XS1618A
  3    SO short combination       29        4.9       72    OEX180
  4    SO long combination        53        6.9       92    OEX18
  5    SO deep offset box         64        8.1       95    XO1618
  6    SO Saltus                  53        6.7       94    FH1618C
  7    SO standard ratchet    *   53        6.5       97    F710
  8    SO long flex ratchet   *   76       10.1       90    F711A

  SO = Snap-On, ELA = effective lever arm""")


if __name__ == "__main__":
    GetInchBoltData()
    GetMetricBoltData()
    Torques()
