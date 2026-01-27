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
        from collections import namedtuple, defaultdict, deque
        import contextlib
        import getopt
        import io
        import re
        import sys
    if 1:   # Custom imports
        import termtables as tt
        import roundoff
        from cmddecode import CommandDecode
        from lwtest import run, Assert
        from f import flt
        from wrap import dedent
        from color import t
        from columnize import Columnize
        from uncertainties import ufloat, ufloat_fromstr
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()     # Holder for global variables
        ii = isinstance
        g.C12_atomic_mass = ufloat_fromstr("11.9999999958(36)") # g/mol
        g.max_digits = 6
        g.digits = 3    # Default number of digits
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
        # Colors
        t.hdr = t.purl
        t.err = t.ornl
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
    def GetRawData(file="/plib/atomic_mass.data", Z_begin=0, Z_end=0):
        '''Return a list of namedtuples containing the NIST data on atomic mass for the
        common isotopes of the elements.  Z_begin and Z_end control which elements are
        put into the returned list.
        
        The data are
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
        if not isinstance(Z_begin, int) and isinstance(Z_end, int):
            raise TypeError(f"Z_begin and Z_end must be integers > 0")
        if not (Z_begin <= Z_end):
            raise ValueError(f"Z_begin must be <= Z_end")
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
        # Trim the list if needed
        if Z_begin or Z_end:
            def include(x):
                return (Z_begin <= x <= Z_end)
            o = []
            for item in data:
                if include(item.Z):
                    o.append(item)
            data = o
        return data
    def PrintRawData(*z, spc=False, Z_begin=0, Z_end=0):
        '''z is a list of Z values to print.  if spc is True, insert blank lines between
        the elements.  Z_begin and Z_end control which elements are printed.
        '''
        data = GetRawData(Z_begin=Z_begin, Z_end=Z_end)
        # Print data with termtables
        hdr = f"{t.hdr}Z Sym RelAtMass IsoComp StdAtMass{t.n}".split()
        o, lastZ = [hdr], None
        for i in data:
            row = []
            if lastZ is None:
                row.append(str(i.Z))
                lastZ = i.Z
            else:
                if i.Z != lastZ:
                    row.append(str(i.Z))
                    lastZ = i.Z
                else:
                    row.append("")
            row.append(_Symbol(i.sym, i.mn))
            row.append(f"{i.ram:.1uS}")
            if ii(i.ic, (int, str)):
                row.append(str(i.ic))   # It's 1 or ''
            else:
                row.append(f"{i.ic:.1uS}")  # It's a ufloat
            if ii(i.sam, (list, str)):
                row.append(str(i.sam))  # It's a list of a single number
            else:
                row.append(f"{i.sam:.1uS}") # It's a ufloat
            if not z or i.Z in z:
                o.append(row)
        o.append(hdr)
        if spc:
            # This first was used to fix a bug in termtables, but here it will be used
            # to insert line breaks between the elements to make the table easier to
            # read.
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                tt.print(o, padding=(0, 0), style=" "*15, alignment="ccrrr")
            lines = f.getvalue().split("\n")
            # Process the lines:  split and get the first token; if it's an integer
            # after the first integer, insert a newline.
            o, dq, first = [], deque(lines), True
            while dq:
                line = dq.popleft()
                f = line.split()
                if f and f[0].endswith("Z"):
                    # It's the header or trailer
                    print(line)
                    continue
                else:
                    if not f:
                        break
                    try:
                        Z = int(f[0])
                        if not first:
                            print()
                        first = False
                        print(line)
                    except ValueError:
                        print(line)
        else:
            tt.print(o, padding=(0, 0), style=" "*15, alignment="ccrrr")
        if z:
            return
        # Print explanation
        print()
        print(dedent(f'''
        These data came from
        https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses.
        Click on "All Elements" and "Linearized ASCII Output"; the "All isotopes" box
        wasn't checked, giving the more common isotopes only.
        
        The symbols are
          {t.hdr}Z{t.n}     Atomic number
        
          The element's symbol includes the mass number of the isotope.
        
          {t.hdr}RelAtMass{t.n} is the atomic mass with its associated uncertainty.  Here, relative
          means the mass is relative to the ¹²C atom (in the nuclear and atomic ground
          state), which has a mass of 11.9999999958(36) g/mol.
        
          {t.hdr}IsoComp{t.n} is the isotope composition most commonly found in the laboratory and
          may not represent the composition of the Earth's crust.
        
          {t.hdr}StdAtMass{t.n} is the standard atomic mass, given as an interval in square brackets
          or as a single number.  A single number in brackets is used for the most
          stable isotope of a radioactive element.
        
          A number in parentheses is a standard uncertainty of the measured value in the
          normal short-form syntax:  '0.0759(4)' means '0.0759 ± 0.0004'.
        
        '''))
    def GetAtomicMassData(digits=g.digits, Z_begin=0, Z_end=0):
        '''Return a list of named tuples of data for each element.  The tuples are NT2 =
        namedtuple("AM2", "Z sym am").  The am element (the atomic mass) will be a flt
        rounded to the stated number of digits.  For elements with atomic number higher
        than 94 (plutonium), the am element will be an integer that is rounded off from
        the mean of the isotopic masses.
        '''
        msg = f"digits must be an int between 1 and {g.max_digits}"
        if not isinstance(digits, int):
            raise TypeError(msg)
        if not (1 <= digits <= g.max_digits):
            raise ValueError(msg)
        data = GetRawData(Z_begin=Z_begin, Z_end=Z_end)
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
                #am.rtz = False
            else:
                am.n = 1
                #am.rtz = am.rtdp = True
            o.append(NT2(Z, el.sym, am))
        return o
    def GetAtomicMassDict(digits=g.digits, Z_begin=0, Z_end=0):
        '''Returns a dictionary keyed by the element's symbol with the element's
        relative atomic mass as the value.
        '''
        di = {}
        for item in GetAtomicMassData(digits=digits, Z_begin=0, Z_end=0):
            di[item.sym] = item.am
        return di

    if 0: #∞∞ 
        if 1:
            #PrintRawData()
            PrintRawData(1, 2, 4, 6, 43, 96, spc=1, Z_begin=2, Z_end=45)
            #PrintRawData(*range(95, 120), spc=1)
        else:
            for i in GetAtomicMassData(digits=3, Z_begin=10, Z_end=30):
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
if 1:  # Molecular mass
    if 1:  # Old functionality
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
    class MolecularMass:
        '''Calculate the molecular mass of a chemical formula.  Example:
        the mass of Ca(C₂H₃O₂)₂ = Ca(C2H3O2)2 is 
            mm = MolecularMass(6)
            print(mm.mass("Ca(C₂H₃O₂)₂"))
        prints out '158.161'.  As a convenience, the Unicode subscript and superscript
        characters are translated to the normal ASCII digit characters.
        '''
        def __init__(self, digits=g.digits):
            '''The keyword digits is an integer to round the atomic mass calculations
            to and can be from 1 to 6.
            '''
            self.di = GetAtomicMassDict(digits=digits)
            self.digits = digits
            # Make a helper to translate subscripts
            self.tr = ''.maketrans("₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹", "01234567890123456789")
        def mass(self, formula):
            "Returns the formula's molecular mass in g/mol or raises an exception"
            # The algorithm for this calculation came from
            # https://gist.github.com/Rhomboid/5994999
            if not isinstance(formula, str):
                raise TypeError("formula must be a string")
            try:
                formula = ''.join(formula.strip())  # Remove all whitespace
                mm = self._calculate_mass(formula)
                mm.n = self.digits
                return mm
            except Exception:
                raise ValueError(f"{formula!r} is an incorrect formula")
        def _calculate_mass(self, formula):
            tokens = re.findall(r"[A-Z][a-z]*|\d+|\(|\)", formula.translate(self.tr))
            if not tokens:
                raise ValueError("Empty formula")
            return self._parse(tokens, [], self.di)
        def _find_closing_paren(self, tokens):
            count = 0
            for index, tok in enumerate(tokens):
                if tok == ")":
                    count -= 1
                    if not count:
                        return index
                elif tok == "(":
                    count += 1
            raise ValueError("unmatched parentheses")
        def _parse(self, tokens, stack, dict):
            if not tokens:
                return sum(stack)
            tok = tokens[0]
            if tok == "(":
                end = self._find_closing_paren(tokens)
                stack.append(self._parse(tokens[1:end], [], dict))
                return self._parse(tokens[end + 1 :], stack, dict)
            elif tok.isdigit():
                stack[-1] *= int(tok)
            else:
                stack.append(dict[tok])
            return self._parse(tokens[1:], stack, dict)

if __name__ == "__main__":
    # Dictionary to relate atomic number to element symbol
    elem2z = {
        "H": 1, "He": 2, "Li": 3, "Be": 4, "B": 5, "C": 6, "N": 7, "O": 8, "F": 9, "Ne":
        10, "Na": 11, "Mg": 12, "Al": 13, "Si": 14, "P": 15, "S": 16, "Cl": 17, "Ar":
        18, "K": 19, "Ca": 20, "Sc": 21, "Ti": 22, "V": 23, "Cr": 24, "Mn": 25, "Fe":
        26, "Co": 27, "Ni": 28, "Cu": 29, "Zn": 30, "Ga": 31, "Ge": 32, "As": 33, "Se":
        34, "Br": 35, "Kr": 36, "Rb": 37, "Sr": 38, "Y": 39, "Zr": 40, "Nb": 41, "Mo":
        42, "Tc": 43, "Ru": 44, "Rh": 45, "Pd": 46, "Ag": 47, "Cd": 48, "In": 49, "Sn":
        50, "Sb": 51, "Te": 52, "I": 53, "Xe": 54, "Cs": 55, "Ba": 56, "La": 57, "Ce":
        58, "Pr": 59, "Nd": 60, "Pm": 61, "Sm": 62, "Eu": 63, "Gd": 64, "Tb": 65, "Dy":
        66, "Ho": 67, "Er": 68, "Tm": 69, "Yb": 70, "Lu": 71, "Hf": 72, "Ta": 73, "W":
        74, "Re": 75, "Os": 76, "Ir": 77, "Pt": 78, "Au": 79, "Hg": 80, "Tl": 81, "Pb":
        82, "Bi": 83, "Po": 84, "At": 85, "Rn": 86, "Fr": 87, "Ra": 88, "Ac": 89, "Th":
        90, "Pa": 91, "U": 92, "Np": 93, "Pu": 94, "Am": 95, "Cm": 96, "Bk": 97, "Cf":
        98, "Es": 99, "Fm": 100, "Md": 101, "No": 102, "Lr": 103, "Rf": 104, "Db": 105,
        "Sg": 106, "Bh": 107, "Hs": 108, "Mt": 109, "Ds": 110, "Rg": 111, "Cn": 112,
        "Nh": 113, "Fl": 114, "Mc": 115, "Lv": 116, "Ts": 117, "Og": 118,
    }
    # Insert the lowercase forms of the elements too
    keys, values = [i.lower() for i in elem2z], list(elem2z.values())
    elem2z.update(zip(keys, values))
    # Make a cmddecode object to identify user's elements
    cmddec = CommandDecode(keys, ignore_case=True)
    def Test_MolecularMass():
        digits = g.max_digits
        di = GetAtomicMassDict(digits=digits)
        mm = MolecularMass(digits=digits)
        # Check the mass of each element
        elements = '''
            Ac Ag Al Am Ar As At Au B Ba Be Bh Bi Bk Br C Ca Cd Ce Cf Cl Cm Co Cr Cs Cu
            Db Dy Er Es Eu F Fe Fm Fr Ga Gd Ge H He Hf Hg Ho Hs I In Ir K Kr La Li Lr Lu
            Md Mg Mn Mo Mt N Na Nb Nd Ne Ni No Np O Os P Pa Pb Pd Pm Po Pr Pt Pu Ra Rb
            Re Rf Rh Rn Ru S Sb Sc Se Sg Si Sm Sn Sr Ta Tb Tc Te Th Ti Tl Tm U V W Xe Y
            Yb Zn Zr'''
        sum = 0
        for i in elements.split():
            m = mm.mass(i)
            expected = di[i]
            Assert(m == expected)
            sum += m
        # Calculate elements as if it was a formula.  This should be equal to the sum we
        # just calculated.
        m = mm.mass(elements)
        Assert(m == sum)
        # Do a few molecular formulas
        m = CalculateMass("H2O")
        Assert(m == 18.0148)
        m = CalculateMass("Ca(C2H3O2)2")
        Assert(m == 158.1654)
        Assert(isinstance(m, flt))
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] cmd [arguments]
          cmd
           f    Print the molecular mass of the formula(s) as arguments (case is
                important, unlike for the 'r' and 't' commands)
           r    Print the raw atomic mass table from NIST showing isotope data.
                Arguments can be atomic number or symbol.
           t    Print an atomic mass table
        Examples:
          'f -d 6 H2O' prints 18.0151 g/mol ('H₂O' and 'H²O' also work)
          'f Ca(C₂H₃O₂)₂' prints 158.2 g/mol
          'r Pd' prints the six common isotopes of Pd
          'r 1 6' prints the raw data for hydrogen and carbon ('r h c' also works)
          't hg fe' prints a columnar table with Hg and Fe highlighted in color, 
              showing you how far apart in atomic number they are
        Options:
            -b n    Begin the output Z at this number
            -d n    Number of digits in result [{d["-d"]}] (1 to {g.max_digits})
            -e n    End the output Z at this number
            -s      Insert lines between elements (r command only)
            -u      Limit output to elements at and below U (Z = 92); this is equivalent
                    to using '-e 92'.
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-b"] = 0         # Begin output Z at this number
        d["-d"] = g.digits  # Number of digits in result
        d["-e"] = 0         # End output Z at this number
        d["-s"] = False     # Insert lines between elements
        d["-t"] = False     # Print table
        d["-u"] = False     # Limit elements to Z <= 92
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "b:d:e:su", ["help", "test"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("su"):
                d[o] = not d[o]
            elif o in ("-b", "-e"):
                try:
                    d[o] = abs(int(a))
                except ValueError:
                    msg = f"{o} option's argument must be an integer"
                    Error(msg)
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= g.max_digits):
                        raise ValueError()
                except ValueError:
                    msg = f"{o} option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--test",):
                exit(run(globals(), halt=True)[0])
        if d["-u"]:
            if d["-e"]:
                d["-e"] = min(d["-e"], 92)
            else:
                d["-e"] = 92
        x = flt(0)
        x.N = d["-d"]
        x.rtz = x.rtdp = True
        if d["-t"]:
            PrintTable()
        return args
    def GetCommandArgs(args):
        'Return the arguments as a list of atomic numbers'
        z = []
        for arg in args:
            items = cmddec(arg)
            if len(items) == 1:
                z.append(elem2z[arg])  # It's a symbol
            elif len(items) > 1:
                t.print(f"{t.err}{arg!r} doesn't identify a unique element")
                exit(1)
            else:   # It must be an integer
                try:
                    z.append(int(arg))
                except Exception:
                    t.print("{t.err}{arg!r}:  non-integer argument in {args!r}")
                    exit(1)
        return z
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    cmd = args.pop(0)
    if cmd == "f":
        mm = MolecularMass(digits=d["-d"])
        for arg in args:
            print(f"{arg} = {mm.mass(arg)} g/mol")
    elif cmd == "r":
        if args:
            z = GetCommandArgs(args)
            PrintRawData(*z, spc=d["-s"], Z_begin=d["-b"], Z_end=d["-e"])
        else:
            PrintRawData(spc=d["-s"], Z_begin=d["-b"], Z_end=d["-e"])
    elif cmd == "t":
        z = GetCommandArgs(args)
        # Print in columnar form
        o, items = [], GetAtomicMassData(digits=d["-d"], Z_begin=d["-b"], Z_end=d["-e"])
        # Get width of each of the 3 elements
        wz, wsym, wam = 0, 0, 0
        for item in items:
            wz = max(wz, len(str(item.Z)))
            wsym = max(wz, len(str(item.sym)))
            wam = max(wz, len(str(item.am)))
        for nt in items:
            s = f"{nt.Z:{wz}d} {nt.sym:{wsym}s} {nt.am!s:{wam}s}"
            if nt.Z in z:   # Decorate it in color if user specified it
                s = t.hdr + s + t.n
            o.append(s)
        for i in Columnize(o, sep=" "*4):
            print(i)
    else:
        print(f"{cmd!r} is an unrecognized command")
