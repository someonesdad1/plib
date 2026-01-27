'''

1.  Stored data on the atomic mass of elements
2.  Calculate the molecular mass of a chemical formula

    GetAtomicMassData(digits=4)
        Returns a namedtuple of NT2 type with components
            - Z   = <int> Atomic number
            - sym = <str> Element symbol
            - am =  <flt> Relative atomic mass
        I suggest you ask for no more than 5 digits, as the returned value is a sum of
        the product of the isotopic composition and the atomic mass of the isotope.
        Note this does not represent e.g. the mean atomic mass measured from samples
        from the Earth's crust.  Don't be surprised if the atomic mass numbers differ
        a bit from what you see in your periodic table, as the measured atomic mass of
        an element will always depend on its isotopic composition.  

        For practical work to 4 or 5 figures, you can assume the returned floating
        point numbers as having the units g/mol.

    PrintRawData(*z, spc=False):
        This function is used to show the raw NIST atomic mass data.  If you don't give
        any atomic number integers as arguments, all elements will be shown.  If spc is
        True, you'll get a blank line between elements.  To see e.g. the first n
        elements' data, use PrintRawData(range(n + 1)).  To see the different types of
        data for each element, try PrintRawData(1, 2, 4, 6, 43, 96, spc=1).

        The returned data is a list of namedtuple of NT1 type with the components
            - Z    = <int> Atomic number
            - sym  = <str> Symbol
            - mn   = <int> Mass number
            - ram  = <unc> Relative atomic mass
            - ic   = <unc> Isotopic composition
            - sam  = <list> Standard atomic mass (may be a float)
            - note = <str> Notes

    The atomic mass data are from
    https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses
    as of Jan 2026 and represent the relative atomic mass of the elements (only the more
    common isotopes, not the full list).  

    Here, relative means the mass is divided by 12, the atomic mass of carbon 12 in the
    atomic and nuclear ground state.

    The measured mass of the carbon 12 atom is 11.9999999958(36) g/mol; note this is 12
    g/mol rounded to 10 figures).  This is stored in the global variable
    g.C12_atomic_mass.  If you want the measured value of the atomic mass of an element,
    multiply its relative atomic mass by g.C12_atomic_mass/12 and you'll have it in the
    units g/mol.  This will be an uncertainties module ufloat instance for an
    isotope, but it will be a floating point number for data from GetAtomicMassData(),
    which you should use for routine computations.

    Consult
    https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-column-descriptions
    for more detailed explanation of the raw data.

'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Atomic mass data oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2026 Don Peterson oo>
        <oo lic ∞ 
            MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo cat ∞ science oo>
        <oo test ∞ --test oo>
        <oo todo ∞ 

            - Provide a GetData to get the atomic mass data
                - GetAtomicMass(an=None, n=5, unc=False)
                - Returns a namedtuple of NT2 type
            - <done> Get the NIST data parsed
            - <done> Return information in a named tuple
            - <done> Use appropriate floating point representation

        oo>
    '''
    if 1:   # Standard imports
        from collections import namedtuple, defaultdict
        import contextlib
        import getopt
        import io
        import re
        import sys
    if 1:   # Custom imports
        import termtables as tt
        import roundoff
        from lwtest import run, Assert
        from f import flt
        from wrap import dedent
        from color import t
        from columnize import Columnize
        from uncertainties import ufloat, ufloat_fromstr
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
        if 1:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()     # Holder for global variables
        ii = isinstance
        g.C12_atomic_mass = ufloat_fromstr("11.9999999958(36)") # g/mol
        # Named tuple for raw data
          # Z    = <int> Atomic number
          # sym  = <str> Symbol
          # mn   = <int> Mass number
          # ram  = <unc> Relative atomic mass
          # ic   = <unc> Isotopic composition
          # sam  = <list> Standard atomic mass (may be a float)
          # note = <str> Notes
        NT1 = namedtuple("AM1", "Z sym mn ram ic sam note")
        # Named tuple for atomic mass data
        NT2 = namedtuple("AM2", "Z sym am")
if 1:  # NIST data
    def _Parse(s):
        'Given the string s from the NIST data, convert it to an appropriate type'
        a, b = s.split("=")
        if "(" in b:
            value = ufloat_fromstr(b.replace("#", ""))
        elif "[" in b:
            value = [flt(i) for i in eval(b)]
        elif "." in b:
            value = flt(b)
        else:
            try:
                value = int(b.strip())
            except Exception:
                value = b.strip()
        return a, value
    def _Symbol(symbol, massnum):
        'Return e.g. ⁹⁶Mo when symbol is "Mo" and massnum is 96'
        e, o = "⁰¹²³⁴⁵⁶⁷⁸⁹", []
        for i in str(massnum):
            o.append(e[int(i)])
        return ''.join(o) + symbol
    def GetRawData(file="/plib/atomic_mass.data"):
        '''Return a list of namedtuples containing the NIST data on atomic mass for the
        common isotopes of the elements.  The data are
          Z    = <int> Atomic number
          sym  = <str> Symbol
          mn   = <int> Mass number
          ram  = <unc> Relative atomic mass
          ic   = <unc> Isotopic composition
          sam  = <list> Standard atomic mass
          note = <str> Notes:
           g  Geological materials are known in which the element has an isotopic
              composition outside the limits for normal material. The difference
              between the atomic weight of the element in such materials and that
              given in the table may exceed the stated uncertainty.
           m  Modified isotopic compositions may be found in commercially available
              material because the material has been subjected to an undisclosed or
              inadvertent isotopic fractionation. Substantial deviations in atomic
              weight of the element from that given in the table can occur.
           r  Range in isotopic composition of normal terrestrial material prevents
              a more precise standard atomic weight being given; the tabulated
              atomic-weight value and uncertainty should be applicable to normal
              materials.
         
        The data are from https://www.nist.gov/pml/atomic-weights-and-isotopic-\
        compositions-relative-atomic-masses.  Click on "All Elements", then "Linearized
        ASCII Output" to get these data (do not click on "All isotopes".  The file
        /plib/atomic_mass.data will contain this information, updated irregularly
        (last download was 26 Jan 2026).
    
        The relative atomic mass is relative to the ground state of carbon 12, which is
        11.9999999958(36) g/mol (from http://physics.nist.gov/constants with 2018 CODATA
        adjustment).
        '''
        if 1:   # Parse the atomic_mass.data file
            lines = [i.strip() for i in open("atomic_mass.data").read().split("\n")]
            # Position on the first data line
            while lines:
                if lines[0].startswith("Atomic Number ="):
                    break
                else:
                    lines.pop(0)
            # Get the records for each isotope
            n, data = 7, []
            while lines:
                record = lines[0:n]
                del lines[0:n]
                #print(record)
                o = []
                for i, item in enumerate(record):
                    a, b = _Parse(item)
                    o.append(b)
                    #print(f"{a} {b!r}")
                data.append(NT1(*o))
                # Position on next record's first line
                while lines:
                    if lines[0].startswith("Atomic Number ="):
                        break
                    else:
                        lines.pop(0)
        return data
    def PrintRawData(*z, spc=False):
        '''z is a list of Z values to print.  if spc is True, insert blank lines between
        the elements.
        '''
        data = GetRawData()
        # Print data with termtables
        hdr = f"{t.skyl}Z Sym RelAtMass IsoComp StdAtMass{t.n}".split()
        nbs = "•"
        el = [nbs]*len(hdr)  # Empty line (a nbs that will be replaced)
        o, last = [hdr], None
        for i in data:
            a, lf = [], False
            if str(i.Z) != last:
                if last:
                    lf = True
                a.append(str(i.Z))
                last = str(i.Z)
            else:
                a.append(" "*3)
            a.append(_Symbol(i.sym, i.mn))
            a.append(f"{i.ram:.1uS}")
            if ii(i.ic, (int, str)):
                a.append(str(i.ic))
            else:
                a.append(f"{i.ic:.1uS}")
            if ii(i.sam, (list, str)):
                a.append(str(i.sam))
            else:
                a.append(f"{i.sam:.1uS}")
            if not z or i.Z in z:
                if lf and spc:
                    o.append(el)
                o.append(a)
        o.append(hdr)
        if 1:
            # termtables has a bug in that it won't print a column consisting of spaces.
            # Here, we'll capture printing to stdout and change the nonbreaking space to
            # a space character.
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                tt.print(o, padding=(0, 0), style=" "*15, alignment="ccrrr")
            s = f.getvalue().replace(nbs, " ")
            print(s, end="")
        if z:
            return
        # Print explanation
        print()
        print(dedent('''
        These data came from
        https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses.
        Click on "All Elements" and "Linearized ASCII Output"; the "All isotopes" box
        wasn't checked, giving the more common isotopes only.
        
        The symbols are
          Z     Atomic number
        
          The element's symbol includes the mass number of the isotope.
        
          RelAtMass is the atomic mass with its associated uncertainty.  Here, relative
          means the mass is relative to the ¹²C atom (in the nuclear and atomic ground
          state), which has a mass of 11.9999999958(36) g/mol.
        
          IsoComp is the isotope composition most commonly found in the laboratory and
          may not represent the composition of the Earth's crust.
        
          StdAtMass is the standard atomic mass, given as an interval in square brackets
          or as a single number.  A single number in brackets is used for the most
          stable isotope of a radioactive element.
        
          A number in parentheses is a standard uncertainty of the measured value in the
          normal short-form syntax:  '0.0759(4)' means '0.0759 ± 0.0004'.
        
        '''))
    def GetAtomicMassData(digits=4):
        '''Return a list of named tuples of data for each element.  The tuples are NT2 =
        namedtuple("AM2", "Z sym am").  The am element (the atomic mass) will be a flt
        rounded to the stated number of digits.  For elements with atomic number higher
        than 94 (plutonium), the am element will be an integer that is rounded off from
        the mean of the isotopic masses.
        '''
        data = GetRawData()
        def GetAtomicMass(Z, items):
            '''Return the atomic mass as a flt for this element with atomic number Z.
            items is a list of the named tuples for each isotope.
            
            Named tuple elements for items:
              Z    = <int>  Atomic number
              sym  = <str>  Symbol
              mn   = <int>  Mass number
              ram  = <unc>  Relative atomic mass
              ic   = <unc>  Isotopic composition
              sam  = <list> Standard atomic mass (may be a float)
            '''
            am = 0      # Atomic mass
            if Z <= 94:
                # Elements up to plutonium:  For each element, the ic component can be a
                # ufloat, 1, or an empty string:
                #   ufloat:  Add up the item.ic*item.ram terms
                #   '':      Set item.ic to zero unless item.sam is a list (it's a radioactive element)
                #   1:       Use item.sam
                for item in items:
                    if ii(item.ic, int):    # If ic is 1, then this is the only isotope
                        assert item.ic == 1
                        am = flt(item.sam.n)
                        break
                    elif ii(item.ic, str):  # It's the empty string
                        assert not item.ic
                        if ii(item.sam, list):
                            # It's a radioactive element like Tc
                            am = flt(item.sam[0])
                            break
                        else:
                            # There's no atomic mass contribution from this isotope
                            continue
                    else:
                        term = flt(item.ram.n*item.ic.n)
                        am += term
            else:
                # Elements past plutonium:  For each element, the ic component is a
                # ufloat and is summed to get the mean, which is rounded to an
                # integer.
                count = 0
                for item in items:
                    count += 1
                    am += item.ram.n
                am = int(round(am/count, 0))
            return am
        # Organize data by atomic number
        byZ = defaultdict(list)
        for i in data:
            byZ[i.Z].append(i)
        # For each element, get its atomic mass by summing the mass of the isotopes by
        # their fractional abundance to get a weighted average.
        o = []
        for Z in byZ:
            items = byZ[Z]
            am = GetAtomicMass(Z, items)
            el = items[0]
            # Round the atomic mass am off to the indicated number of digits
            am = flt(roundoff.RoundOff(am, digits))
            if am:
                am.n = digits
                am.rtz = False
            else:
                am.n = 1
                am.rtz = am.rtdp = True
            o.append(NT2(Z, el.sym, am))
        return o

    if 1:
        if 0:
            #PrintRawData()
            PrintRawData(1, 2, 4, 6, 43, 96, spc=1)
            #PrintRawData(*range(95, 120), spc=1)
        else:
            for i in GetAtomicMassData(digits=3):
                print(f"{i.Z:3d}      {i.sym:2s}      {i.am!s}")
        exit()

if 1:   # Old set of data
        g.atomic_mass = {
            # From https://gist.github.com/Rhomboid/5994999
            # Downloaded Tue 12 Aug 2014 02:23:51 PM
            # Chemical name:  atomic mass in g/mol
            "Ac": flt(227.0),
            "Ag": flt(107.87),
            "Al": flt(26.982),
            "Am": flt(243.0),
            "Ar": flt(39.948),
            "As": flt(74.922),
            "At": flt(210.0),
            "Au": flt(196.08),
            "B": flt(10.811),
            "Ba": flt(137.33),
            "Be": flt(9.0122),
            "Bh": flt(264.0),
            "Bi": flt(208.98),
            "Bk": flt(247.0),
            "Br": flt(79.904),
            "C": flt(12.011),
            "Ca": flt(40.078),
            "Cd": flt(112.41),
            "Ce": flt(140.12),
            "Cf": flt(251.0),
            "Cl": flt(35.453),
            "Cm": flt(247.0),
            "Co": flt(58.933),
            "Cr": flt(51.996),
            "Cs": flt(132.91),
            "Cu": flt(63.546),
            "Db": flt(262.0),
            "Dy": flt(162.50),
            "Er": flt(167.26),
            "Es": flt(252.0),
            "Eu": flt(151.96),
            "F": flt(18.998),
            "Fe": flt(55.845),
            "Fm": flt(257.0),
            "Fr": flt(223.0),
            "Ga": flt(69.723),
            "Gd": flt(157.25),
            "Ge": flt(72.61),
            "H": flt(1.0079),
            "He": flt(4.0026),
            "Hf": flt(178.49),
            "Hg": flt(200.59),
            "Ho": flt(164.93),
            "Hs": flt(269.0),
            "I": flt(126.90),
            "In": flt(114.82),
            "Ir": flt(192.22),
            "K": flt(39.098),
            "Kr": flt(83.80),
            "La": flt(138.91),
            "Li": flt(6.941),
            "Lr": flt(262.0),
            "Lu": flt(174.97),
            "Md": flt(258.0),
            "Mg": flt(24.305),
            "Mn": flt(54.938),
            "Mo": flt(95.94),
            "Mt": flt(268.0),
            "N": flt(14.007),
            "Na": flt(22.990),
            "Nb": flt(92.906),
            "Nd": flt(144.24),
            "Ne": flt(20.180),
            "Ni": flt(58.693),
            "No": flt(259.0),
            "Np": flt(237.0),
            "O": flt(15.999),
            "Os": flt(190.23),
            "P": flt(30.974),
            "Pa": flt(231.04),
            "Pb": flt(207.2),
            "Pd": flt(106.42),
            "Pm": flt(145.0),
            "Po": flt(209.0),
            "Pr": flt(140.91),
            "Pt": flt(196.08),
            "Pu": flt(244.0),
            "Ra": flt(226.0),
            "Rb": flt(85.468),
            "Re": flt(186.21),
            "Rf": flt(261.0),
            "Rh": flt(102.91),
            "Rn": flt(222.0),
            "Ru": flt(101.07),
            "S": flt(32.065),
            "Sb": flt(121.76),
            "Sc": flt(44.956),
            "Se": flt(78.96),
            "Sg": flt(266.0),
            "Si": flt(28.086),
            "Sm": flt(150.36),
            "Sn": flt(118.71),
            "Sr": flt(87.62),
            "Ta": flt(180.95),
            "Tb": flt(158.93),
            "Tc": flt(97.61),
            "Te": flt(127.60),
            "Th": flt(232.04),
            "Ti": flt(47.867),
            "Tl": flt(204.38),
            "Tm": flt(168.93),
            "U": flt(238.03),
            "V": flt(50.942),
            "W": flt(183.84),
            "Xe": flt(131.29),
            "Y": flt(88.906),
            "Yb": flt(173.04),
            "Zn": flt(65.39),
            "Zr": flt(91.224),
        }
if 1:  # Core functionality
    def PrintTable():
        out, w = [], 70
        for i in g.atomic_mass:
            out.append(f"{i:2s} {g.atomic_mass[i]!s:>6s}")
        t.print(f"{t('purl')}{'Atomic masses in g/mol':^{w}s}")
        for i in Columnize(out, col_width=15):
            print(i)
        # Now print sorted by mass
        m = []
        for i in g.atomic_mass:
            m.append((g.atomic_mass[i], i))
        out = []
        for mass, name in sorted(m):
            out.append(f"{mass!s:>6s} {name:2s}")
        print()
        t.print(f"{t('grn')}{'Sorted by mass in g/mol:':^{w}s}")
        for i in Columnize(out, col_width=15):
            print(i)
        exit(0)
    def Find_closing_paren(tokens):
        count = 0
        for index, tok in enumerate(tokens):
            if tok == ")":
                count -= 1
                if count == 0:
                    return index
            elif tok == "(":
                count += 1
        raise ValueError("unmatched parentheses")
    def Parse(tokens, stack, dict):
        if len(tokens) == 0:
            return sum(stack)
        tok = tokens[0]
        if tok == "(":
            end = Find_closing_paren(tokens)
            stack.append(Parse(tokens[1:end], [], dict))
            return Parse(tokens[end + 1 :], stack, dict)
        elif tok.isdigit():
            stack[-1] *= int(tok)
        else:
            stack.append(dict[tok])
        return Parse(tokens[1:], stack, dict)
    def CalculateMass(formula):
        tokens = re.findall(r"[A-Z][a-z]*|\d+|\(|\)", formula)
        if not tokens:
            raise Exception("Empty")
        return Parse(tokens, [], g.atomic_mass)
    def GetMass(formula):
        try:
            print(f"{formula}: {CalculateMass(formula)} g/mol")
        except Exception:
            print(f"{formula!r} is an incorrect formula")

if 1:
    PrintTable()
    exit()

if __name__ == "__main__":
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(
            dedent(f'''
        Usage:  {sys.argv[0]} [options] formula1 [formula2...]
          Print the molecular mass of chemical formulas.  Examples:
            H: 1.008 g/mol
            H2O: 18 g/mol
            Ca(C2H3O2)2: 158.2 g/mol
        Options:
            -d n    Number of digits in result [{d["-d"]}]
            -t      Print atomic mass table
        ''')
        )
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 4  # Number of digits in result
        d["-t"] = False  # Print table
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:t", ["help", "test"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("t"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--test",):
                exit(run(globals(), halt=True)[0])
        x = flt(0)
        x.N = d["-d"]
        if d["-t"]:
            PrintTable()
        return args
    def Test_BigFormula():
        m = CalculateMass("H")
        Assert(m == g.atomic_mass["H"])
        m = CalculateMass("H2O")
        Assert(m == 18.0148)
        m = CalculateMass("Ca(C2H3O2)2")
        Assert(m == 158.1654)
        # Single formula of all elements.  This is a checksum of the
        # g.atomic_mass dictionary's elements.
        a = (
            "AcAgAlAmArAsAtAuBBaBeBhBiBkBrCCaCdCeCfClCmCoCrCsCuDbDyErEsEu"
            "FFeFmFrGaGdGeHHeHfHgHoHsIInIrKKrLaLiLrLuMdMgMnMoMtNNaNbNdNe"
            "NiNoNpOOsPPaPbPdPmPoPrPtPuRaRbReRfRhRnRuSSbScSeSgSiSmSnSrTa"
            "TbTcTeThTiTlTmUVWXeYYbZnZr"
        )
        b = (
            227.0, 107.87, 26.982, 243.0, 39.948, 74.922, 210.0, 196.08, 10.811, 137.33,
            9.0122, 264.0, 208.98, 247.0, 79.904, 12.011, 40.078, 112.41, 140.12, 251.0,
            35.453, 247.0, 58.933, 51.996, 132.91, 63.546, 262.0, 162.50, 167.26, 252.0,
            151.96, 18.998, 55.845, 257.0, 223.0, 69.723, 157.25, 72.61, 1.0079, 4.0026,
            178.49, 200.59, 164.93, 269.0, 126.90, 114.82, 192.22, 39.098, 83.80,
            138.91, 6.941, 262.0, 174.97, 258.0, 24.305, 54.938, 95.94, 268.0, 14.007,
            22.990, 92.906, 144.24, 20.180, 58.693, 259.0, 237.0, 15.999, 190.23,
            30.974, 231.04, 207.2, 106.42, 145.0, 209.0, 140.91, 196.08, 244.0, 226.0,
            85.468, 186.21, 261.0, 102.91, 222.0, 101.07, 32.065, 121.76, 44.956, 78.96,
            266.0, 28.086, 150.36, 118.71, 87.62, 180.95, 158.93, 97.61, 127.60, 232.04,
            47.867, 204.38, 168.93, 238.03, 50.942, 183.84, 131.29, 88.906, 173.04,
            65.39, 91.224,
        )
        Assert(CalculateMass(a) == sum(b))
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    for arg in args:
        GetMass(arg)
