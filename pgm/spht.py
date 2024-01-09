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
    # Mostly from https://en.wikipedia.org/wiki/Table_of_specific_heat_capacities
    # Nominally at room temperature (25 °C).  A//B*C means A/(B*C).
    spht = (
        # Name, phase, Cp in J//g*K, thermal conductivity in W//m*K
        ("Acrylic plastic", solid, flt(0.0), flt(0.18)),
        ("Air, typical room", gas, flt(1.012), flt(0.0262)),
        ("Aluminum", solid, flt(1.012), flt(237)),
        ("Animal tissue", mixed, flt(3.5)),
        ("Argon", gas, flt(0.52)),
        ("Arsenic", solid, flt(0.328)),
        ("Beryllium", solid, flt(1.82)),
        ("Bismuth", solid, flt(0.123)),
        ("Cadmium", solid, flt(0.231)),
        ("Carbon dioxide", gas, flt(0.839)),
        ("Chromium", solid, flt(0.449)),
        ("Copper", solid, flt(0.385)),
        ("Diamond", solid, flt(0.509)),
        ("Ethanol", liquid, flt(2.44)),
        ("Gasoline", liquid, flt(2.22)),
        ("Glass", solid, flt(0.84)),
        ("Gold", solid, flt(0.129)),
        ("Granite", solid, flt(0.790)),
        ("Graphite", solid, flt(0.710)),
        ("Helium", gas, flt(5.1932)),
        ("Hydrogen", gas, flt(14.30)),
        ("Hydrogen sulfide", gas, flt(1.015)),
        ("Iron", solid, flt(0.449)),
        ("Lead", solid, flt(0.129)),
        ("Lithium", solid, flt(3.58)),
        ("Magnesium", solid, flt(1.02)),
        ("Mercury", liquid, flt(0.14)),
        ("Methanol", liquid, flt(2.14)),
        ("Molten salt", liquid, flt(1.56)),
        ("Nitrogen", gas, flt(1.04)),
        ("Neon", gas, flt(1.03)),
        ("Oxygen", gas, flt(0.918)),
        ("Paraffin wax", solid, flt(2.5)),
        ("Polyethylene", solid, flt(2.30)),
        ("Silica (fused)", solid, flt(0.70)),
        ("Silver", solid, flt(0.233)),
        ("Sodium", solid, flt(1.23)),
        ("Steel", solid, flt(0.466)),
        ("Tin", solid, flt(0.227)),
        ("Titanium", solid, flt(0.523)),
        ("Tungsten", solid, flt(0.134)),
        ("Uranium", solid, flt(0.116)),
        ("Steam at 100 °C", gas, flt(2.03)),
        ("Water", liquid, flt(4.18)),
        ("Ice  at -10 °C", solid, flt(2.05)),
        ("Zinc", solid, flt(0.387)),

        ("Asphalt", solid, flt(0.92)),
        ("Brick", solid, flt(0.84)),
        ("Concrete", solid, flt(0.88)),
        ("Gypsum", solid, flt(1.09)),
        ("Marble", solid, flt(0.88)),
        ("Sand", solid, flt(0.84)),
        ("Soil", solid, flt(0.80)),
        ("Wood (1.2 to 2.9)", solid, flt(1.7)),

        ("Human body", mixed, flt(3)),
    )
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
