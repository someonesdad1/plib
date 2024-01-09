'''
Specific heat of some materials
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Specific heat of some materials
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        from f import flt
        #from columnize import Columnize
    if 1:   # Global variables
        class G:
            pass
        g = G()  # Storage for global variables as attributes
        g.dbg = False
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        ii = isinstance
        g.W = int(os.environ.get("COLUMNS", "80")) - 1
        g.L = int(os.environ.get("LINES", "50"))
if 1:   # Data
    # References
    #   https://en.wikipedia.org/wiki/Table_of_specific_heat_capacities
    #   https://www.engineeringtoolbox.com/specific-heat-capacity-d_391.html
    #   https://en.wikipedia.org/wiki/List_of_thermal_conductivities
    # Nominally at room temperature (25 °C).  A//B*C means A/(B*C).
    #   Name, phase, Cp in J//g*K, thermal conductivity in W//m*K
    #   Phase is s, l, g, m (mixed)
    data = '''
        Acrylic plastic;        s;      1.5;        0.18
        Air, typical room;      g;      1.012;      0.0262
        Alumina;                s;      0.72;       -
        Aluminum;               s;      0.897;      237
        Animal tissue;          s;      3.5;        -
        Argon;                  g;      0.52;       -
        Arsenic;                s;      0.328;      -
        Asphalt;                s;      0.92;       -
        Beryllium;              s;      1.02;       -
        Bismuth;                s;      0.123;      7.97
        Brass;                  s;      0.38;       -
        Brick;                  s;      0.84;       -
        Cadmium;                s;      0.231;      -
        Carbon dioxide;         g;      0.839;      -
        Chalk;                  s;      0.75;       -
        Charcoal;               s;      0.84;       -
        Chromium;               s;      0.449;      -
        Concrete w/ aggregrate; s;      0.9;        -
        Concrete;               s;      0.88;       -
        Copper;                 s;      0.385;      401
        Cork;                   s;      2;          -
        Diamond;                s;      0.509;      1000
        Epoxy cast resins;      s;      1.0;        -
        Ethanol;                l;      2.44;       0.1
        Fire brick;             s;      0.88;       -
        Gasoline;               l;      2.22;       -
        Glass;                  s;      0.84;       -
        Gold;                   s;      0.129;      -
        Granite;                s;      0.790;      -
        Graphite;               s;      0.710;      -
        Gypsum;                 s;      1.09;       -
        Helium;                 g;      5.19;       -
        Human body;             s;      3;          -
        Hydrogen sulfide;       g;      1.015;      -
        Hydrogen;               g;      14.30;      -
        Ice  at -10 °C;         s;      2.05;       -
        Iron;                   s;      0.449;      -
        Lead;                   s;      0.129;      -
        Leather;                s;      1.5;        -
        Lithium;                s;      3.58;       -
        Magnesium;              s;      1.02;       -
        Marble;                 s;      0.88;       2.5
        Mercury;                l;      0.14;       -
        Methanol;               l;      2.14;       0.1
        Molten salt;            l;      1.56;       -
        Mud, wet                s;      2.5;        -
        Neon;                   g;      1.03;       -
        Nitrogen;               g;      1.04;       -
        Nylon 66;               s;      1.7;        -
        Oxygen;                 g;      0.918;      -
        PET                     s;      1.2;        -
        PVC                     s;      1.0;        -
        Paper;                  s;      1.34;       -
        Paraffin wax;           s;      2.5;        -
        Polycarbonate           s;      1.2;        -
        Polyethylene;           s;      2.30;       -
        Polypopylene            s;      1.9;        -
        Polystyrene             s;      1.4;        -
        Polystyrene, expanded;  s;      -;          0.04
        Polyurethane foam;      s;      -;          0.03
        Quartz                  s;      0.7;        -
        Salt, NaCl              s;      0.88;       -
        Sand;                   s;      0.84;       -
        Sandstone               s;      0.7;        -
        Silica (fused);         s;      0.70;       -
        Silicon                 s;      0.7;        -
        Silicon carbide         s;      0.67;       -
        Silver;                 s;      0.233;      406
        Slate                   s;      0.76;       -
        Snow                    s;      2.1;        0.15
        Sodium;                 s;      1.23;       -
        Soil, dry               s;      0.8;        -
        Soil, wet               s;      1.5;        -
        Soil;                   s;      0.80;       -
        Steam at 100 °C;        g;      2.03;       -
        Steel;                  s;      0.466;      -
        Tantalum                s;      0.14;       -
        Teflon                  s;      1.2;        0.25
        Tin;                    s;      0.227;      -
        Titanium;               s;      0.523;      -
        Tungsten;               s;      0.134;      -
        Uranium;                s;      0.116;      -
        Water;                  l;      4.18;       0.592
        Wood (1.2 to 2.9);      s;      1.7;        -
        Zinc;                   s;      0.387;      -
    '''
    spht = []
    for line in data.split("\n"):
        if not line.strip():
            continue
        f = [i.strip() for i in line.strip().split(";")]
        matl, ph, cp, tc = f
        assert(ph in "slg")
        cp = None if cp == "-" else flt(cp)
        tc = None if tc == "-" else flt(tc)
        spht.append((matl, ph, cp, tc))
    spht = tuple(spht)
    from pprint import pprint as pp
    pp(spht)
    exit()

if 1:   # Utility
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
            
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [units]
          Show a table of specific heats.  Units default to 
          J/(g*K).
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Describe this option
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o == "-h":
                Usage(status=0)
        return args
if 1:   # Core functionality
    pass

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
