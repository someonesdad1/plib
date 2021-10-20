'''
Print out battery data
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2020 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Print out battery data
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import os
    import sys
    import subprocess
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
def PrintData():
    print(f'''
    Battery capacity in mA*hr (3.6 coul)  (mass in g, dimensions in mm)
        Alk.
       Mass,g   Alkaline    C-Zn  NiMH        Lithium  Diameter   Length
       ------   --------    ----  ---------   -------  ---------  ---------
AA       20      2890       1100  1700-2900     3000   13.5-14.5  49.5-50.5
AAA      11.5    1250        540  800-1000             9.5-10.5   43.3-44.5
AAAA      6.5     625                                  7.7-8.3    41.5-42.5
C        66      8350       3800  4500-6000            24.9-26.2  48.5-50
D       140     20500       8000  900-11500            32.3-34.2  59.5-61.5
9 volt   46       600(@25mA) 400  175           1200   16.5x25.5x47.5 +- 1
CR123    3 volts                                1500   17    34.5
                 9V:  + is smooth round terminal
Energizer alkaline spec sheet data:  i in mA, mA*hr at 21 degC [ending voltage]
  AA   [0.8]:  25/2800       100/2500       250/1800       500/1300
  AAA  [0.8]:  25/1250       100/1000       200/750        400/400
  9V   [4.8]:  25/600        100/450        300/350        500/300
  C    [0.8]:  25/8300       100/7300       300/5000       500/3200
  D    [0.8]:  25/20000      100/15000      250/13000      500/10000
 
Silver Oxide   Volts mA*hr     Alkaline   Volts  mA*hr   Dia   Length
------------   ----- -----     --------   -----  -----   ----  ------
    SR41        1.55   42        LR41       1.5    32     7.9    3.6
    SR44        1.55  200        LR44[2.0g] 1.5   150    11.6    5.4
Hearing aid batteries (typically Zinc-Air (ZnO2) 1.4 V)         Tab color
---------------------
    5       35 mA*hr    5.8 mm dia  2.15 mm long    0.20 g      Red
    10      75 mA*hr    5.8 mm dia  3.6  mm long    0.28 g      Yellow
    312    170 mA*hr    7.9 mm dia  3.6  mm long    0.49 g      Brown
    13     300 mA*hr    7.9 mm dia  5.4  mm long    0.80 g      Orange
    675    605 mA*hr   11.6 mm dia  5.4  mm long    1.76 g      Blue
    5.8 mm = 0.228", 7.9 mm = 0.311", 11.6 mm = 0.457"
Temperature effect:  New Duracell alkaline 9 V:  measured 9.65 V at 24
deg C; at -11 deg C (48 hr soak) was 9.67 V (both open circuit).
 
              V/cell    Chg          Loss/%/yr
Chemistry   New   EOL  Meth  Cycles Life/yr  Temp/C Comments
---------   ----- ----  ---  ------ -------  ------ -----------------------
Alkaline    1.5   0.9   --   --     5%       -30/55 Good ED, sloped D
Lithium     1.5-1       --   --     5-10+    -55/75 Flat D, long life hi ED
C-Zn        1.5         --   --     1-5       -5/55 Cheap, low ED, sloped D
Ag2O        1.5         --   --     6%       -20/55 Flat D, good ED
HgO         1.4         --   --     4%       -10/55 Flat D
Ni-Cd *     1.2   0.9   CC   500+   0.25      20/70 Hi disch, quick chg, mod ED
Pb-acid *   2.0   1.75  CV/F 200    1        -20/65 Hi cap, mod ED
NiMH *      1.2   1.0                               Hi ED, hi self-D
* = secondary (rechargeable)   F = float   D = discharge   ED = energy density
                               EOL = end of life
Include a command line argument to see lithium coin cell data.  Use aa, aaa,
etc. to see common battery PDF datasheets.
    '''[1:].rstrip())
def PrintLithium():
    print(dedent(f'''
    Lithium (LiMn02 chemistry) Coin cells (3 V nom, 3.6 V open circuit)
      No.     Dia, mm   Thk, mm   Mass, g     mA*hr
    ------    -------   -------   -------     -----
    '''))
    s = '''
    CR1025 10x2.5 0.7 30 3
    CR1216 12.5x1.6 0.7 25 3
    CR1220 12.5x2 1.2 35 3
    CR1225 12.5x2.5 0.9 50 3
    CR1612 16x1.2 0.8 40 3
    CR1616 16x1.6 1.2 50 3
    CR1620 16x2 1.3 75 3
    CR1632 16x3.2 1.8 125 3
    CR2012 20x1.2 1.4 55 3
    CR2016 20x1.6 1.6 90 3
    CR2025 20x2.5 2.5 165 3
    CR2032 20x3.2 3.1 200 3
    CR2320 23x2 3 130 3
    CR2325 23x2.5 3 190 3
    CR2330 23x3 4 265 3
    CR2354 23x5.4 5.9 560 3
    CR2412 24x1.2 2 100 3
    CR2430 24.5x3 4.6 290 3
    CR2450 24.5x5 6.3 620 3
    CR2477 24.5x7.7 10.5 1000 3
    CR3032 30x3.2 7.1 500 3
    CR927 9.5x2.7 0.51 30 3
'''  # From http://www.batteriesandbutter.com/coin_batttery_chart.html
    f = "    {:7s}     {:^4s}      {:^4s}      {:^4s}       {:>4s}"
    for line in s.strip().split("\n"):
        name, sz, mass, mAhr, V = line.split()
        dia, h = sz.split("x")
        print(f.format(name, dia, h, mass, mAhr))
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] [cmd]
    
      Print out battery data for no cmd.  If cmd is aa, aaa, c, d, 9v, then open
      the Duracell PDF for that battery.  For any other cmd, print out the lithium
      coin cell battery data too.
    
    Options:
        -h      Print a manpage
    '''))
    exit(status)
def ParseCommandLine(d):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-h", "--help"):
            Usage(d, status=0)
    return args
def Open(cmd):
    pth = "C:/cygwin/elec/batteries/duracell"
    file = f"{pth}/Duracell_{cmd.upper()}_alkaline.pdf"
    st = "C:/cygwin/bin/cygstart.exe"
    subprocess.Popen([st, file])
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    cmd = args[0].lower() if args else None
    if not cmd:
        PrintData()
    else:
        if cmd in "aa aaa c d 9v".split():
            Open(cmd)
        else:
            PrintData()
            PrintLithium()
# vim:  wm=0
