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
        import string
        import sys
        import webbrowser
        from pprint import pprint as pp
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from lwtest import Assert
        if 0:
            import debug
            debug.SetDebugger()
        t.dbg = t("brnl")
    if 1:   # Global variables
        ii = isinstance
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
        g.sym2num = {}      # {('h', 1), ('he', 2), ...
                            #  ('H', 1), ('He', 2)}
        g.num2sym = {}      # {(1, 'h'), (2, 'he')}
        g.num2Sym = {}      # {(1, 'H'), (2, 'He')}
        g.num2name = {}     # {(1, 'hydrogen'), (2, 'helium')}
        g.num2Name = {}     # {(1, 'Hydrogen'), (2, 'Helium')}
        g.name2num = {}     # [('hydrogen', 1), ('helium', 2)]
        g.Name2num = {}     # [('Hydrogen', 1), ('Helium', 2)]
        g.names = []        # ['hydrogen', 'helium', ...
                            #  'Hydrogen', 'Helium']
        g.symbols = []      # ['h', 'he', 'li', 'be', ...
                            #  'H', 'He', 'Li', 'Be']
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
            -d      Dump data structures
            -i      Launch page on isotopes
            -o      Open wikipedia page on matched elements
            -t      Run self-tests
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False     # Dump data structures
        d["-i"] = False     # Open isotopes page
        d["-o"] = False     # Open web page instead of printing to stdout
        d["-t"] = False     # Run self-tests
        try:
            opts, args = getopt.getopt(sys.argv[1:], "dhiot") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("dhiot"):
                d[o] = not d[o]
        GetData()
        if d["-t"]:
            TestGetElements()
        if not args:
            Usage()
        return args
if 1:   # Core functionality
    def Uppercase(word):
        assert(word)
        return word[0].upper() + word[1:]
    def GetData():
        'Construct global dicts'
        for line in elements.strip().split("\n"):
            Name, Sym, num = [i.strip() for i in line.split()]
            num = int(num)
            sym = Sym.lower()
            name = Name.lower()
            # Dicts
            g.sym2num[sym] = num
            g.sym2num[Sym] = num
            g.num2sym[num] = sym
            g.num2Sym[num] = Sym
            g.num2Name[num] = Name
            g.num2name[num] = name
            g.Name2num[Name] = num
            g.name2num[name] = num
            #  Lists
            g.symbols.append(Sym)
            g.symbols.append(sym)
            g.names.append(Name)
            g.names.append(name)
        #  Set of capitalized element names
        g.all = set(i for i in g.names if i[0] in string.ascii_uppercase)
        if d["-d"]:     # Dump data structures
            def L(di):
                return list(di.items())[:2]
            print(f"{t.dbg}g.names    [list]: {g.names[:4]}")
            print(f"g.symbols  [list]: {g.symbols[:4]}")
            print()
            #
            print(f"g.sym2num  [dict]: {L(g.sym2num)}")
            #
            print(f"g.num2sym  [dict]: {L(g.num2sym)}")
            print(f"g.num2Sym  [dict]: {L(g.num2Sym)}")
            print(f"g.num2name [dict]: {L(g.num2name)}")
            print(f"g.num2Name [dict]: {L(g.num2Name)}")
            #
            print("All formal element names, capitalized:")
            t.print(f"  g.all       [set]: {list(g.all)[:2]}")
            print()
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
    def GetElements(el, test=False):
        '''Return the name(s) of the indicated element as a list.
        Search strategy:
            - See if it's an integer, meaning an atomic number
            - See if it's an element symbol (1st character must be upper case)
            - See if it's a full element name
            - Search with it as a regex
        If test is True, always return a list, even if empty.
        '''
        if not el.strip():
            return []
        try:    # Atomic number?
            atomic_number = int(el)
            name = g.num2Name[atomic_number]
            assert(name in g.all)
            return [name]
        except (ValueError, KeyError):
            if test:
                return []
        # Element symbol?
        if el[0] in string.ascii_uppercase:
            try:
                if el in g.symbols:
                    atomic_number = g.sym2num[el]
                    name = g.num2Name[atomic_number]
                    assert(name in g.all)
                    return [name]
            except KeyError:
                if test:
                    return []
        # Matches a full element name?
        if el in g.names:
            index = g.names.index(el)
            name = Uppercase(g.names[index])
            assert(name in g.all)
            return [name]
        # Use regular expression
        r = re.compile(el)
        names = []
        for name in g.names:
            mo = r.search(name)
            if mo and Uppercase(name) not in names:
                names.append(Uppercase(name))
        for name in names:
            assert(name in g.all)
        return names
    def TestGetElements():
        'Check that GetElements returns reasonable values'
        # Valid atomic number
        Assert(GetElements("1") == ["Hydrogen"])
        # Invalid atomic number
        Assert(GetElements("0", test=True) == [])
        # Valid symbol
        Assert(GetElements("H") == ["Hydrogen"])
        # Invalid symbol
        Assert(GetElements("Zz", test=True) == [])
        # Valid full element name
        Assert(GetElements("Hydrogen") == ["Hydrogen"])
        Assert(GetElements("hydrogen") == ["Hydrogen"])
        # Invalid full element name
        Assert(GetElements("Zydrogen") == [])
        # Valid regex
        Assert(GetElements("[YZ]") == ['Zinc', 'Yttrium', 'Zirconium', 'Ytterbium'])
        # Invalid regex
        Assert(GetElements("Zydrogen") == [])
        Assert(GetElements("") == [])
        #
        print("Tests passed")
        exit(0)

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    # Find all the element names referenced by the command line
    g.found_names = []
    for el in args:
        for name in GetElements(el):
            if name not in g.found_names:
                g.found_names.append(name)
    if d["-d"]:   # Dump for debugging
        print("Found the following elements:")
        pp(g.found_names)
        exit()
    # Open the web pages
    for name in g.found_names:
        if d["-o"] or d["-i"]:
            LaunchWebPage(name)
        else:
            w = 14
            num = g.name2num[name.lower()]
            sym = g.num2sym[num]
            print(f"{name:{w}s} {num:3d} {Uppercase(sym)}")
