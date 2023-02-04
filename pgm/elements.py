'''
Launch wikipedia pages for elements
    e.g. https://en.wikipedia.org/wiki/Hydrogen
    e.g. https://en.wikipedia.org/wiki/Isotopes_of_hydrogen
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        import re
        import sys
        import webbrowser
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        if 1:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        elements = '''
            Hydrogen       H    1
            Helium         He   2
            Lithium        Li   3
            Beryllium      Be   4
            Boron          B    5
            Carbon         C    6
            Nitrogen       N    7
            Oxygen         O    8
            Fluorine       F    9
            Neon           Ne   10
            Sodium         Na   11
            Magnesium      Mg   12
            Aluminium      Al   13
            Silicon        Si   14
            Phosphorus     P    15
            Sulfur         S    16
            Chlorine       Cl   17
            Argon          Ar   18
            Potassium      K    19
            Calcium        Ca   20
            Scandium       Sc   21
            Titanium       Ti   22
            Vanadium       V    23
            Chromium       Cr   24
            Manganese      Mn   25
            Iron           Fe   26
            Cobalt         Co   27
            Nickel         Ni   28
            Copper         Cu   29
            Zinc           Zn   30
            Gallium        Ga   31
            Germanium      Ge   32
            Arsenic        As   33
            Selenium       Se   34
            Bromine        Br   35
            Krypton        Kr   36
            Rubidium       Rb   37
            Strontium      Sr   38
            Yttrium        Y    39
            Zirconium      Zr   40
            Niobium        Nb   41
            Molybdenum     Mo   42
            Technetium     Tc   43
            Ruthenium      Ru   44
            Rhodium        Rh   45
            Palladium      Pd   46
            Silver         Ag   47
            Cadmium        Cd   48
            Indium         In   49
            Tin            Sn   50
            Antimony       Sb   51
            Tellurium      Te   52
            Iodine         I    53
            Xenon          Xe   54
            Cesium         Cs   55
            Barium         Ba   56
            Lanthanum      La   57
            Cerium         Ce   58
            Praseodymium   Pr   59
            Neodymium      Nd   60
            Promethium     Pm   61
            Samarium       Sm   62
            Europium       Eu   63
            Gadolinium     Gd   64
            Terbium        Tb   65
            Dysprosium     Dy   66
            Holmium        Ho   67
            Erbium         Er   68
            Thulium        Tm   69
            Ytterbium      Yb   70
            Lutetium       Lu   71
            Hafnium        Hf   72
            Tantalum       Ta   73
            Tungsten       W    74
            Rhenium        Re   75
            Osmium         Os   76
            Iridium        Ir   77
            Platinum       Pt   78
            Gold           Au   79
            Mercury        Hg   80
            Thallium       Tl   81
            Lead           Pb   82
            Bismuth        Bi   83
            Polonium       Po   84
            Astatine       At   85
            Radon          Rn   86
            Francium       Fr   87
            Radium         Ra   88
            Actinium       Ac   89
            Thorium        Th   90
            Protactinium   Pa   91
            Uranium        U    92
            Neptunium      Np   93
            Plutonium      Pu   94
            Americium      Am   95
            Curium         Cm   96
            Berkelium      Bk   97
            Californium    Cf   98
            Einsteinium    Es   99
            Fermium        Fm   100
            Mendelevium    Md   101
            Nobelium       No   102
            Lawrencium     Lr   103
            Rutherfordium  Rf   104
            Dubnium        Db   105
            Seaborgium     Sg   106
            Bohrium        Bh   107
            Hassium        Hs   108
            Meitnerium     Mt   109
            Darmstadtium   Ds   110
            Roentgenium    Rg   111
            Copernicium    Cn   112
            Nihonium       Nh   113
            Flerovium      Fl   114
            Moscovium      Mc   115
            Livermorium    Lv   116
            Tennessine     Ts   117
            Oganesson      Og   118
            '''
        # Mappings for element names, symbols, atomic numbers
        class g:
            pass
        g.sym2num = {}
        g.num2sym = {}
        g.num2name = {}
        g.name2num = {}
        g.names = []
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] el1 [el2 ...]
          Print the matched elements.  The el strings can be the element's
          symbol, a regular expression for the name, or the atomic number.
        Options:
            -i      Launch page on isotopes
            -o      Open wikipedia page on matched elements
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-i"] = False     # Open isotopes page
        d["-o"] = False     # Open web page instead of printing to stdout
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "io", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("io"):
                d[o] = not d[o]
        return args
if 1:   # Core functionality
    def Uppercase(word):
        assert(word)
        return word[0].upper() + word[1:]
    def GetData():
        'Construct global dicts'
        for line in elements.strip().split("\n"):
            name, sym, num = [i.strip().lower() for i in line.split()]
            num = int(num)
            g.names.append(name)
            g.sym2num[sym] = num
            g.num2sym[num] = sym
            g.num2name[num] = name
            g.name2num[name] = num
    def LaunchWebPage(name):
        base = "https://en.wikipedia.org/wiki/"
        if d["-i"]:
            # Open the isotope page
            url = base + "Isotopes_of_" + name.lower()
            webbrowser.open(url)
        else:
            # Open the element page
            url = base + name
            webbrowser.open(url)
    def GetElement(el):
        'Return the name(s) of the indicated element as a list'
        # See if it's an atomic number
        el = el.lower()
        try:
            return [Uppercase(g.num2name[int(el)])]
        except Exception:
            pass
        # See if it's a symbol
        try:
            return [Uppercase(g.num2name[g.sym2name[sym]])]
        except Exception:
            pass
        # See if it's an exact match to a name
        try:
            index = g.names.index(el)
            return [Uppercase(g.names[index])]
        except Exception:
            pass
        # Search for the string in names
        names = []
        for name in g.names:
            if el in name:
                names.append(Uppercase(name))
        if names:
            return names
        # Use regular expression
        r = re.compile(el)
        for name in g.names:
            mo = r.search(el)
            if mo:
                names.append(Uppercase(name))
        return names

if 0:
    url = "https://someonesdad1.github.io/hobbyutil/project_list.html"
    webbrowser.open(url)
    exit()

if __name__ == "__main__":
    d = {}      # Options dictionary
    GetData()
    args = ParseCommandLine(d)
    names = []
    for el in args:
        for name in GetElement(el):
            if name not in names:
                names.append(name)
    # Open the web pages
    for name in names:
        if d["-o"] or d["-i"]:
            LaunchWebPage(name)
        else:
            w = 14
            num = g.name2num[name.lower()]
            sym = g.num2sym[num]
            print(f"{name:{w}s} {num:3d} {Uppercase(sym)}")
