"""
ToDo
    - Find the values for all pri 0 materials

Specific heat of some materials
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Specific heat of some materials
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import getopt
        import os
        import re
        from pathlib import Path as P
        import sys
    if 1:  # Custom imports
        from wrap import dedent
        from color import t
        from f import flt

        if 1:
            import debug

            debug.SetDebugger()
    if 1:  # Global variables

        class G:
            pass

        g = G()  # Storage for global variables as attributes
        g.dbg = False
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        ii = isinstance
        g.W = int(os.environ.get("COLUMNS", "80")) - 1
        g.L = int(os.environ.get("LINES", "50"))
        # Colors
        t.sol = t("wht")
        t.liq = t("trq")
        t.gas = t("denl")
        t.title = t("magl", attr="ul")
        t.trlr = t("ornl")
if 1:  # Data
    # References
    #   https://en.wikipedia.org/wiki/Table_of_specific_heat_capacities
    #   https://www.engineeringtoolbox.com/specific-heat-capacity-d_391.html
    #   https://en.wikipedia.org/wiki/List_of_thermal_conductivities
    # Nominally at room temperature (25 °C).  A//B*C means A/(B*C).
    #   Name, phase, Cp in J//g*K, thermal conductivity in W//m*K, priority
    #   Phase is s, l, g, m (mixed)
    data = """
        Acetone;                l;      2.18;       -        ; 0
        Acrylic plastic;        s;      1.5;        0.18     ; 0
        Air;                    g;      1.012;      0.0262   ; 0
        Alumina;                s;      0.72;       -        ; 0
        Aluminum;               s;      0.897;      237      ; 0
        Animal tissue;          s;      3.5;        -        ; 1
        Argon;                  g;      0.52;       0.0187   ; 1
        Arsenic;                s;      0.328;      -        ; 1
        Asphalt;                s;      0.92;       -        ; 0
        Beryllium;              s;      1.02;       -        ; 1
        Bismuth;                s;      0.123;      7.97     ; 1
        Brass;                  s;      0.38;       85       ; 0
        Brick;                  s;      0.84;       -        ; 0
        Cadmium;                s;      0.231;      -        ; 1
        Carbon dioxide;         g;      0.839;      0.0162   ; 0
        Chalk;                  s;      0.75;       -        ; 1
        Charcoal;               s;      0.84;       -        ; 1
        Chromium;               s;      0.449;      -        ; 1
        Concrete w/ aggregate;  s;      0.9;        1.3      ; 1
        Concrete;               s;      0.88;       -        ; 0
        Copper;                 s;      0.385;      401      ; 0
        Cork;                   s;      2;          -        ; 1
        Diamond;                s;      0.509;      1000     ; 1
        Epoxy cast resins;      s;      1.0;        -        ; 0
        Ethanol;                l;      2.44;       0.1      ; 1
        Fire brick;             s;      0.88;       -        ; 1
        Gasoline;               l;      2.22;       -        ; 0
        Glass;                  s;      0.84;       0.74     ; 0
        Gold;                   s;      0.129;      313      ; 1
        Granite;                s;      0.790;      -        ; 1
        Graphite;               s;      0.710;      60       ; 0
        Gypsum;                 s;      1.09;       -        ; 0
        Helium;                 g;      5.19;       0.1558   ; 1
        Human body;             s;      3;          -        ; 0
        Hydrogen sulfide;       g;      1.015;      -        ; 1
        Hydrogen;               g;      14.30;      0.1754   ; 1
        Ice  at -10 °C;         s;      2.05;       2.2      ; 0
        Iron, cast;             s;      0.50;       62.5     ; 0
        Iron;                   s;      0.449;      74.4     ; 0
        Lead;                   s;      0.129;      -        ; 0
        Leather;                s;      1.5;        -        ; 1
        Lithium;                s;      3.58;       -        ; 1
        Magnesium;              s;      1.02;       -        ; 1
        Marble;                 s;      0.88;       2.5      ; 1
        Mercury;                l;      0.14;       -        ; 1
        Methanol;               l;      2.14;       0.1      ; 1
        Molten salt;            l;      1.56;       -        ; 1
        Mud, wet;               s;      2.5;        -        ; 0
        Neon;                   g;      1.03;       -        ; 1
        Nitrogen;               g;      1.04;       0.0251   ; 0
        Nylon 66;               s;      1.7;        0.29     ; 0
        Oxygen;                 g;      0.918;      0.0262   ; 0
        PET;                    s;      1.2;        -        ; 1
        PVC;                    s;      1.0;        -        ; 0
        Paper;                  s;      1.34;       0.14     ; 0
        Paper, cardboard;       s;      -;          0.25     ; 0
        Paraffin wax;           s;      2.5;        -        ; 0
        Polycarbonate;          s;      1.2;        -        ; 0
        Polyethylene;           s;      2.30;       -        ; 0
        Polypopylene;           s;      1.9;        -        ; 0
        Polystyrene;            s;      1.4;        -        ; 0
        Polystyrene, expanded;  s;      -;          0.04     ; 0
        Polyurethane foam;      s;      -;          0.03     ; 0
        Quartz;                 s;      0.7;        -        ; 0
        Salt, NaCl;             s;      0.88;       -        ; 1
        Sand;                   s;      0.84;       -        ; 0
        Sandstone;              s;      0.7;        -        ; 1
        Silica (fused);         s;      0.70;       -        ; 0
        Silicon;                s;      0.7;        -        ; 1
        Silicon carbide;        s;      0.67;       -        ; 1
        Silver;                 s;      0.233;      406      ; 0
        Slate;                  s;      0.76;       -        ; 1
        Snow, fresh;            s;      2.1;        0.15     ; 0
        Snow, compact;          s;      -;          0.35     ; 0
        Snow, beginning to thaw;s;      -;          0.64     ; 0
        Sodium;                 s;      1.23;       -        ; 1
        Soil, dry;              s;      0.8;        -        ; 0
        Soil, wet;              s;      1.5;        -        ; 0
        Steam at 100 °C;        g;      2.03;       -        ; 0
        Steel;                  s;      0.466;      45.4     ; 0
        Steel, stainless;       s;      -;          9.3      ; 0
        Tantalum;               s;      0.14;       -        ; 1
        Teflon;                 s;      1.2;        0.25     ; 0
        Tin;                    s;      0.227;      -        ; 1
        Titanium;               s;      0.523;      -        ; 1
        Tungsten;               s;      0.134;      -        ; 1
        Uranium;                s;      0.116;      -        ; 1
        Vinyl plastic;          s;      -;          0.13     ; 0
        Water;                  l;      4.18;       0.592    ; 0
        Wood (1.2 to 2.9);      s;      2;          0.3      ; 0
        Zinc;                   s;      0.387;      -        ; 1
    """
    spht = []
    for line in data.split("\n"):
        if not line.strip():
            continue
        f = [i.strip() for i in line.strip().split(";")]
        matl, ph, cp, tc, pri = f
        assert ph in "slg"
        cp = 0 if cp == "-" else flt(cp)
        tc = 0 if tc == "-" else flt(tc)
        spht.append((matl, ph, cp, tc, pri))
    spht = tuple(sorted(spht))
    # Get widths
    w0 = max(len(i[0]) for i in spht)
    w1 = 6
    w2 = max(len(str(i[2])) for i in spht)
    w3 = max(len(str(i[3])) for i in spht)
if 1:  # Utility

    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Manpage():
        print(
            dedent(f"""

        The specific heat is the amount of energy per unit mass of material
        that must be added to a material to raise its temperature 1 K.  The
        heat capacity will most generally be a function of temperature and
        your calculations will be incorrect if a phase change is involved.

        The specific heat values given are isobaric, meaning that the
        system's pressure is constant.  For a gas, adding heat will cause
        it to expand.  For gases, the ration of the isobaric heat capacity
        to the isochoric (at constant volume) is around 1.3 to 1.7.

        The heat conductivity is a measure of how well heat flows in a
        material.

        All values given are approximate and represent average values or
        the most common allotropic form.  These are for making back of the
        envelope calculations; proper references should be consulted for
        serious work.

        Water's heat of fusion is 334 J/g and heat of vaporization is 2265
        J/g.

        References
            - Koshkin and Shirkevich, "Handbook of Elementary Physics", MIR
              Publishers, 3rd ed., 1977

        """)
        )
        exit(0)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] [regex]
          Show a table of specific heats and thermal conductivity (search
          for regex if given).  Only the most commonly-used materials are
          shown in the table unless -a is used.  
        Options:
            -a      Show all materials
            -d n    Number of digits [{d["-d"]}]
            -H      Print a manpage
            -h      Print usage help
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False  # Show all materials
        d["-d"] = 2  # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:Hh")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 4):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 4"
                    Error(msg)
            elif o == "-H":
                Manpage()
            elif o == "-h":
                Usage(status=0)
        x = flt(0)
        x.N = d["-d"]
        x.rtz = x.rtdp = True
        return args


if 1:  # Core functionality

    def PrintItem(*args, all=False):
        matl, ph, cp, tc, pri = args
        pri = int(pri)
        f = lambda x: str(x) if x else "-"
        p = {
            "s": "solid",
            "l": "liquid",
            "g": "gas",
        }
        c = ""
        if ph == "s":
            c = t.sol
        elif ph == "l":
            c = t.liq
        elif ph == "g":
            c = t.gas
        if pri == 0 or all:
            t.print(
                f"{c}{matl:{w0}s}{spc}{f(p[ph]):^{w1}s}{spc}{f(cp):^{w2}s}{spc}{f(tc):^{w3}s}"
            )

    def Hdr():
        t.print(
            f"{t.title}{'Material':{w0}s}{spc}{'Phase':^{w1}s}{spc}{'Cp':^{w2}s}{spc}{'k':^{w3}s}"
        )

    def Trlr():
        t.print(f"{t.trlr}Cp = specific heat at constant pressure in J/(g*K)")
        t.print(f"{t.trlr}k = thermal conductivity in W/(m*K)")
        t.print(f"{t.trlr}Values given to {d['-d']} figures.  T ~ 20 °C, P ~ 101 kPa.")


if __name__ == "__main__":
    d = {}  # Options dictionary
    spc = " " * 4
    args = ParseCommandLine(d)
    if not args:
        Hdr()
        for i in spht:
            PrintItem(*i)
        Trlr()
    else:
        R = [re.compile(i, re.I) for i in args]
        results = []
        for i in spht:
            matl = i[0]
            for r in R:
                mo = r.search(matl)
                if mo:
                    results.append(i)
                    break
        if results:
            Hdr()
            for i in results:
                PrintItem(*i, all=True)
            Trlr()
