'''Dimensions of sockets in shop
'''

# Copyright (C) 2020 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Academic Free License version 3.0.
# See http://opensource.org/licenses/AFL-3.0.
#
 
if 1:   # Imports & globals
    import getopt
    import os
    import sys
    from columnize import Columnize
 
    # Debugging stuff
    from pdb import set_trace as xx
    if 0:
        import debug
        debug.SetDebugger()  # Start debugger on unhandled exception

if sys.stdout.isatty():
    w = "[0;37;40m"       # White
    h = "[1;33;40m"       # Highlight color
else:
    w = h = ""

def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)

def Regular():
    print('''
D = diameter, L = length, in inches
                {h}3/8 square drive sockets{w}
Snap-On  Standard         Deep     | Mac Std    Sunex Univ dp | Craftsman dp
          D     L       D     L    | mm    D         D        |   D 
1/4     0.664 0.913                | 6   0.683                |
5/16    0.664 0.903                | 7   0.686                |
3/8     0.664 0.908                | 8   0.680                |
7/16    0.658 0.902   0.663 2.120  | 9   0.682                | 0.651
1/2     0.714 0.934   0.709 2.125  | 10  0.656*    0.629      | 0.651
9/16    0.772 1.004   0.770 2.379  | 11  0.684     0.670      | 0.649
5/8     0.837 1.038   0.836 2.377  | 12  0.680     0.741      | 0.674
11/16   0.927 1.097   0.927 2.637  | 13  0.713     0.741      | 0.693
3/4     0.990 1.111   0.986 2.627  | 14  0.776     0.820      | 0.750
13/16   1.077 1.149   1.045 2.744  | 15  0.809     0.865      | 0.790
7/8     1.151 1.150   1.147 2.750  | 16  0.876     0.903      | 0.839
15/16  @1.237 1.318                | 17  0.932     0.900      | 0.895
1      @1.307 1.373                | 18  0.987     0.981      | L = 2.5
                                   | 19  1.014     1.060      |
                                   |  L = 1.1                 |
              {h}1/4 square drive sockets{w}
Snap-On  Standard        Deep      | Craftsman Std   | Snap-On deep
          D    L       D     L     | mm    D    L    |   D    L
5/32   *0.452 0.867                | 4   0.473 0.834 |
3/16    0.478 0.882  *0.448 1.988  | 5   0.473 0.840 | 0.476 2.005
                                   | 5.5             | 0.477 2.009
7/32    0.479 0.878   0.447 1.987  | 6   0.475 0.837 | 0.479 2.007
1/4     0.478 0.877   0.434 1.980  | 7   0.449 0.876 | 0.477 2.006
9/32    0.478 0.877   0.478 2.001  | 8   0.477 0.840 | 0.478 1.994
5/16    0.478 0.877   0.429 1.985  | 9   0.558 0.824 | 0.501 2.003
11/32   0.494 0.879   0.495 2.008  | 10  0.539 0.869 | 0.549 2.001
3/8     0.540 0.879   0.547 1.992  | 11  0.620 0.844 | 0.604 2.002
7/16    0.603 0.878   0.620 2.003  | 12  0.656 0.837 | 0.650 2.002
1/2     0.676 0.872   0.683 1.988  | 13  0.683 0.883 | 0.693 2.003
9/16    0.740 0.860   0.740 1.985  | 14              | 0.740 2.001
5/8     0.824 0.979                |                 |

* = Craftsman
@ = Challenger
'''[1:-1].format(**globals()))

def Big():
    print('''
                {h}3/4 square drive sockets{w}
       D      L                    D      L             
19   1.424  1.969           36   1.969  2.397
22   1.413  1.985           38   2.010  2.328
24   1.389  1.965           41   2.210  2.478
26   1.432  1.969           42   2.228  2.413
27   1.455  2.065           45   2.418  2.538 
28   1.530  2.051           46   2.402  2.577 
30   1.609  2.071           48   2.505  2.792
32   1.711  2.242           50   2.644  2.711
34   1.838  2.278

Inch:    1-1/4, 1-3/8, 1-1/2
                {h}1/2 square drive sockets{w}
             Challenger           Snap-On           Bolt
              D      L            D      L          Size
9/16        0.877   1.43         --      --         3/8
5/8         0.863   1.52         --      --
11/16       0.933   1.50         --      --         7/16
3/4         1.050   1.50         --      --         1/2
13/16        --      --          --      --
7/8         1.176   1.57        1.177   1.51        9/16
15/16       1.235   1.61        1.269   1.50        5/8
1           1.302   1.56        1.333   1.52
1 1/16      1.427   1.65        1.422   1.63
1 1/8       1.494   1.75        1.488   1.75        3/4
1 3/16       --      --         1.599   1.76
1 1/4       1.618   1.74        1.675   1.88
1 5/16       --      --         1.734   1.86        7/8
1 3/8        --      --         1.897   2.06
1 7/16       --      --         1.922   2.25
1 1/2        --      --         1.988   2.24        1

Neiko metric deep impact socket diameters, L = 3.06
10      0.944       18      1.098
11      0.944       19      1.096
12      0.944       20      1.175
13      0.944       21      1.175
14      0.944       22      1.255
15      0.944       23      1.335
16      0.944       24      1.336
17      1.023       

'''[1:-1].format(**globals()))


sockets = {
    # Dia  Size   Brand    Type  Drive
    (664, "1/4", "SO", "std", "3/8"),
    (664, "5/16", "SO", "std", "3/8"),
    (664, "3/8", "SO", "std", "3/8"),
    (658, "7/16", "SO", "std", "3/8"),
    (714, "1/2", "SO", "std", "3/8"),
    (772, "9/16", "SO", "std", "3/8"),
    (837, "5/8", "SO", "std", "3/8"),
    (927, "11/16", "SO", "std", "3/8"),
    (990, "3/4", "SO", "std", "3/8"),
    (1077, "13/16", "SO", "std", "3/8"),
    (1151, "7/8", "SO", "std", "3/8"),
    (1237, "15/16", "CH", "std", "3/8"),
    (1307, "1", "CH", "std", "3/8"),

    (663, "7/16", "SO", "deep", "3/8"),
    (709, "1/2", "SO", "deep", "3/8"),
    (770, "9/16", "SO", "deep", "3/8"),
    (836, "5/8", "SO", "deep", "3/8"),
    (927, "11/16", "SO", "deep", "3/8"),
    (986, "3/4", "SO", "deep", "3/8"),
    (1045, "13/16", "SO", "deep", "3/8"),
    (1147, "7/8", "SO", "deep", "3/8"),

    (683, "6", "Mac", "std", "3/8"),
    (686, "7", "Mac", "std", "3/8"),
    (680, "8", "Mac", "std", "3/8"),
    (682, "9", "Mac", "std", "3/8"),
    (656, "10", "CR", "std", "3/8"),
    (684, "11", "Mac", "std", "3/8"),
    (680, "12", "Mac", "std", "3/8"),
    (713, "13", "Mac", "std", "3/8"),
    (776, "14", "Mac", "std", "3/8"),
    (809, "15", "Mac", "std", "3/8"),
    (876, "16", "Mac", "std", "3/8"),
    (932, "17", "Mac", "std", "3/8"),
    (987, "18", "Mac", "std", "3/8"),
    (1014, "19", "Mac", "std", "3/8"),

    (629, "10", "SU", "univ deep", "3/8"),
    (670, "11", "SU", "univ deep", "3/8"),
    (741, "12", "SU", "univ deep", "3/8"),
    (741, "13", "SU", "univ deep", "3/8"),
    (820, "14", "SU", "univ deep", "3/8"),
    (865, "15", "SU", "univ deep", "3/8"),
    (903, "16", "SU", "univ deep", "3/8"),
    (900, "17", "SU", "univ deep", "3/8"),
    (981, "18", "SU", "univ deep", "3/8"),
    (1060, "19", "SU", "univ deep", "3/8"),

    (651, "9", "CR", "deep", "3/8"),
    (651, "10", "CR", "deep", "3/8"),
    (649, "11", "CR", "deep", "3/8"),
    (674, "12", "CR", "deep", "3/8"),
    (693, "13", "CR", "deep", "3/8"),
    (750, "14", "CR", "deep", "3/8"),
    (790, "15", "CR", "deep", "3/8"),
    (839, "16", "CR", "deep", "3/8"),
    (895, "17", "CR", "deep", "3/8"),

    (452, "5/32", "CR", "std", "1/4"),
    (478, "3/16", "SO", "deep", "1/4"),
    (479, "7/32", "SO", "deep", "1/4"),
    (478, "1/4", "SO", "deep", "1/4"),
    (478, "9/32", "SO", "deep", "1/4"),
    (478, "5/16", "SO", "deep", "1/4"),
    (494, "11/32", "SO", "deep", "1/4"),
    (540, "3/8", "SO", "deep", "1/4"),
    (603, "7/16", "SO", "deep", "1/4"),
    (676, "1/2", "SO", "deep", "1/4"),
    (740, "9/16", "SO", "deep", "1/4"),
    (824, "5/8", "SO", "deep", "1/4"),

    (448, "3/16", "SO", "deep", "1/4"),
    (447, "7/32", "SO", "deep", "1/4"),
    (434, "1/4", "SO", "deep", "1/4"),
    (478, "9/32", "SO", "deep", "1/4"),
    (429, "5/16", "SO", "deep", "1/4"),
    (495, "11/32", "SO", "deep", "1/4"),
    (547, "3/8", "SO", "deep", "1/4"),
    (620, "7/16", "SO", "deep", "1/4"),
    (683, "1/2", "SO", "deep", "1/4"),
    (740, "9/16", "SO", "deep", "1/4"),

    (473, "4", "CR", "std", "1/4"),
    (473, "5", "CR", "std", "1/4"),
    (474, "6", "CR", "std", "1/4"),
    (449, "7", "CR", "std", "1/4"),
    (477, "8", "CR", "std", "1/4"),
    (558, "9", "CR", "std", "1/4"),
    (539, "10", "CR", "std", "1/4"),
    (620, "11", "CR", "std", "1/4"),
    (656, "12", "CR", "std", "1/4"),
    (683, "13", "CR", "std", "1/4"),

    (476, "5", "SO", "deep", "1/4"),
    (477, "5.5", "SO", "deep", "1/4"),
    (479, "6", "SO", "deep", "1/4"),
    (477, "7", "SO", "deep", "1/4"),
    (478, "8", "SO", "deep", "1/4"),
    (501, "9", "SO", "deep", "1/4"),
    (549, "10", "SO", "deep", "1/4"),
    (604, "11", "SO", "deep", "1/4"),
    (650, "12", "SO", "deep", "1/4"),
    (693, "13", "SO", "deep", "1/4"),
    (740, "14", "SO", "deep", "1/4"),

    (877, "9/16", "CH", "std", "1/2"),
    (863, "5/8", "CH", "std", "1/2"),
    (933, "11/16", "CH", "std", "1/2"),
    (1050, "3/4", "CH", "std", "1/2"),
    (1176, "7/8", "CH", "std", "1/2"),
    (1235, "15/16", "CH", "std", "1/2"),
    (1302, "1", "CH", "std", "1/2"),
    (1427, "1-1/16", "CH", "std", "1/2"),
    (1494, "1-1/8", "CH", "std", "1/2"),
    (1618, "1-1/4", "CH", "std", "1/2"),

    (1177, "7/8", "SO", "std", "1/2"),
    (1269, "15/16", "SO", "std", "1/2"),
    (1333, "1", "SO", "std", "1/2"),
    (1422, "1-1/16", "SO", "std", "1/2"),
    (1488, "1-1/8", "SO", "std", "1/2"),
    (1599, "1-3/16", "SO", "std", "1/2"),
    (1675, "1-1/4", "SO", "std", "1/2"),
    (1734, "1-5/16", "SO", "std", "1/2"),
    (1897, "1-3/8", "SO", "std", "1/2"),
    (1922, "1-5/16", "SO", "std", "1/2"),
    (1988, "1-1/2", "SO", "std", "1/2"),

    (944, "10", "NE", "deep", "1/2"),
    (944, "11", "NE", "deep", "1/2"),
    (944, "12", "NE", "deep", "1/2"),
    (944, "13", "NE", "deep", "1/2"),
    (944, "14", "NE", "deep", "1/2"),
    (944, "15", "NE", "deep", "1/2"),
    (944, "16", "NE", "deep", "1/2"),
    (1023, "17", "NE", "deep", "1/2"),
    (1098, "18", "NE", "deep", "1/2"),
    (1096, "19", "NE", "deep", "1/2"),
    (1175, "20", "NE", "deep", "1/2"),
    (1175, "21", "NE", "deep", "1/2"),
    (1255, "22", "NE", "deep", "1/2"),
    (1335, "23", "NE", "deep", "1/2"),
    (1336, "24", "NE", "deep", "1/2"),

    (1424, "19", "HF", "std", "3/4"),
    (1413, "22", "HF", "std", "3/4"),
    (1389, "24", "HF", "std", "3/4"),
    (1432, "26", "HF", "std", "3/4"),
    (1455, "27", "HF", "std", "3/4"),
    (1530, "28", "HF", "std", "3/4"),
    (1609, "30", "HF", "std", "3/4"),
    (1711, "32", "HF", "std", "3/4"),
    (1838, "34", "HF", "std", "3/4"),
    (1969, "36", "HF", "std", "3/4"),
    (2010, "38", "HF", "std", "3/4"),
    (2210, "41", "HF", "std", "3/4"),
    (2228, "42", "HF", "std", "3/4"),
    (2418, "45", "HF", "std", "3/4"),
    (2402, "46", "HF", "std", "3/4"),
    (2505, "48", "HF", "std", "3/4"),
    (2644, "50", "HF", "std", "3/4"),
}

def Usage(d, status=1):
    name = sys.argv[0]
    s = f'''
Usage:  {name} [options] [dia1 [dia2 ...]]
  Show on-hand sockets that are close to the indicated diameter(s) in
  inches.  If no diameters are given, print a list of all sockets.

Options:
    -h      Print a manpage
    -m      Use mm for diameters
    -t      Tolerance in percent (default is {d['-t']}%)
    -T      Show table of sockets by diameter
'''[1:-1]
    print(s)
    exit(status)

def ParseCommandLine(d):
    d["-m"] = False     # Use mm
    d["-t"] = 5         # Tolerance in %
    d["-T"] = False     # Table
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hmt:T")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("mT"):
            d[o] = not d[o]
        elif o == "-t":
            try:
                d[o] = tol = float(a)
                if tol <= 0:
                    Error("-t option must be > 0")
            except Exception:
                Error(f"'{a}' not a valid tolerance")
        elif o == "-h":
            Usage(d, status=0)
    return args

def Table():
    print("Diameter in ", end="")
    if d["-m"]:
        print("mm")
    else:
        print("inches")
    for D, sz, mfg, type, drive in sorted(sockets):
        if d["-m"]:
            dia_mm = 25.4*D/1000
            print(f"    {dia_mm:5.2f}     {sz:8s} {mfg:^6s} {type:10s} {drive:4s}")
        else:
            print(f"    {D/1000:5.3f}     {sz:8s} {mfg:^6s} {type:10s} {drive:4s}")
    Mfg()
    ShortTable()

def ShortTable():
    diameters = '''
        429 434 447 448 449 452 473 474 476 477 478 479 494 495 501 539
        540 547 549 558 603 604 620 629 649 650 651 656 658 663 664 670
        674 676 680 682 683 684 686 693 709 713 714 740 741 750 770 772
        776 790 809 820 824 836 837 839 863 865 876 877 895 900 903 927
        932 933 944 981 986 987 990 1014 1023 1045 1050 1060 1077 1096
        1098 1147 1151 1175 1176 1177 1235 1237 1255 1269 1302 1307 1333
        1335 1336 1389 1413 1422 1424 1427 1432 1455 1488 1494 1530 1599
        1609 1618 1675 1711 1734 1838 1897 1922 1969 1988 2010 2210 2228
        2402 2418 2505 2644'''
    mils = [int(i) for i in diameters.split()]
    print("Available diameters in mils")
    for line in Columnize([f"{i:4d}" for i in mils], indent=" "*4,
                          col_width=6):
        print(line)
    print("Available diameters in mm")
    for line in Columnize([f"{i/1000*25.4:.1f}" for i in mils], 
                          indent=" "*4, col_width=6):
        print(line)

def Mfg():
    print('''
Manufacturers:
    CH      Challenger
    CR      Craftsman
    HF      Harbor Freight
    Mac     Mac Tools
    NE      Neiko
    SO      Snap-On
    SU      Sunex
'''.strip())

def Search(args):
    print(f"Tolerance = {d['-t']}%")
    for size in args:
        # Get diameter in mils
        D_mils = int(1000*float(size)*25.4 if d["-m"] else 1000*float(size))
        Find(D_mils, size)

def Find(D_mils, size):
    low = (1 - d["-t"]/100)*D_mils
    high = (1 + d["-t"]/100)*D_mils
    found = []
    for i in sockets:
        dia_mils = i[0]
        if low <= dia_mils <= high:
            found.append(i)
    if found:

        if d["-m"]:
            print(size, "mm")
        else:
            print(size, "inches")
        for D, sz, mfg, type, drive in sorted(found):
            print(f"    {D/1000:5.3f} {sz:8s} {mfg:2s} {type:4s} {drive:4s}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["-T"]:
        Table()
    elif args:
        Search(args)
    else:
        Big()
        Regular()
