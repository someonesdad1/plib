'''
Print out sizes of common US nails
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2017 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Print out sizes of common US nails
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Custom imports
    from wrap import dedent
    from f import flt
    from u import u
if 1:   # Global variables
    steel_wire_gauge = {
        # Gauge number, diameter in inches
        # https://sizes.com/tools/nails_wire_gauge.htm
        "2": 0.2625,"2.5": 0.253,"3": 0.2437,"3.5": 0.234,"4": 0.2253,
        "4.5": 0.216,"5": 0.207,"5.5": 0.2,"6": 0.192,"6.5": 0.184,
        "7": 0.177,"7.5": 0.17,"8": 0.162,"8.5": 0.155,"9": 0.1483,
        "9.5": 0.142,"10": 0.135,"10.25": 0.131,"10.5": 0.128,
        "11": 0.1205,"11.5": 0.113,"12": 0.1055,"12.5": 0.099,
        "13": 0.0915,"13.5": 0.086,"14": 0.08,"14.5": 0.076,"15": 0.072,
    }
    nail_data = dedent('''
        # Data from https://sizes.com/tools/nails_common_wire.htm
        # Fields:
        #   0   Size [pennyweight]
        #   1   Length [inches]
        #   2   Diameter, steel wire gauge
        #   3   Number in a pound
        2d      1        15        876
        3d      1.25     14        568
        4d      1.5      12.5      316
        5d      1.75     12.5      271
        6d      2        11.5      181
        7d      2.25     11.5      161
        8d      2.5      10.25     106
        9d      2.75     10.5      96 
        10d     3        9         69 
        12d     3.25     9         64 
        16d     3.5      8         49 
        20d     4        6         31 
        30d     4.5      5         24 
        40d     5        4         18 
        50d     5.5      3         14 
        60d     6        2         11 
    ''')
def GetNailData():
    '''Return list of tuples (pennyweight, length, swg, mass) in SI
    units.
    '''
    nails = []
    for i in nail_data.split("\n"):
        i = i.strip()
        if not i or i[0] == "#":
            continue
        pennyweight, L, swg, lb = i.split()
        L = flt(L)*u("inches")
        D = flt(steel_wire_gauge[swg]*u("in"))
        m = 1/flt(lb)*u("lb")
        numperlb = int(lb)
        nails.append((pennyweight, L, D, m, numperlb))
    return nails
if __name__ == "__main__":
    x = flt(0)
    x.n = 3
    x.rtz = True
    print(f"{'US Common steel nail sizes':^60s}\n")
    print(dedent('''
                    Length          Diameter         Mass    Number
    Pennyweight   inch      mm     inch     mm         g     per lb
    -----------   ----     ----   -----    ----     ------   ------
    '''))
    for pennyweight, L, D, m, numperlb in GetNailData():
        print(f"   {pennyweight:^4s}", end=" "*5)
        # Length
        print(f"{L/u('in')!s:^8s}", end=" ")
        print(f"{L/u('mm')!s:^8s}", end="")
        # Diameter
        print(f"{D/u('in'):^8.3f}", end=" ")
        print(f"{D/u('mm'):^6.2f}", end=" "*4)
        # Mass
        print(f"{m/u('g')!s:^8s}", end=" ")
        # Number per lb
        print(f"{numperlb:^8d}")
