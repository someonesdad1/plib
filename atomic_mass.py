'''
Calculate the molecular weight of a chemical formula
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        # None
        #∞license∞#
        #∞what∞#
        # Calculate the molecular weight of a chemical formula.  Taken from
        # https://gist.github.com/Rhomboid/5994999.
        #∞what∞#
        #∞test∞# --test #∞test∞#
    # Standard imports
        import getopt
        import os
        import re
        from pathlib import Path as P
        import sys
        from pdb import set_trace as xx
    # Custom imports
        from lwtest import run, raises, assert_equal, Assert
        from f import flt
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from columnize import Columnize
    # Global variables
        ii = isinstance
        atomic_mass = {
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
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] formula1 [formula2...]
          Print the molecular mass of chemical formulas.  Examples:
            H: 1.008 g/mol
            H2O: 18 g/mol
            Ca(C2H3O2)2: 158.2 g/mol
        Options:
            -d n    Number of digits in result [{d['-d']}]
            -t      Print atomic mass table
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 4         # Number of digits in result
        d["-t"] = False     # Print table
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:t", 
                    ["help", "test"])
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
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
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
    def Test():
        m = CalculateMass("H")
        Assert(m == atomic_mass["H"])
        m = CalculateMass("H2O")
        Assert(m == 18.0148)
        m = CalculateMass("Ca(C2H3O2)2")
        Assert(m == 158.1654)
        # Single formula of all elements.  This is a checksum of the
        # atomic_mass dictonary's elements.
        a = ("AcAgAlAmArAsAtAuBBaBeBhBiBkBrCCaCdCeCfClCmCoCrCsCuDbDyErEsEu"
            "FFeFmFrGaGdGeHHeHfHgHoHsIInIrKKrLaLiLrLuMdMgMnMoMtNNaNbNdNe"
            "NiNoNpOOsPPaPbPdPmPoPrPtPuRaRbReRfRhRnRuSSbScSeSgSiSmSnSrTa"
            "TbTcTeThTiTlTmUVWXeYYbZnZr")
        b = (227.0, 107.87, 26.982, 243.0, 39.948, 74.922, 210.0, 196.08,
            10.811, 137.33, 9.0122, 264.0, 208.98, 247.0, 79.904, 12.011,
            40.078, 112.41, 140.12, 251.0, 35.453, 247.0, 58.933, 51.996,
            132.91, 63.546, 262.0, 162.50, 167.26, 252.0, 151.96, 18.998,
            55.845, 257.0, 223.0, 69.723, 157.25, 72.61, 1.0079, 4.0026,
            178.49, 200.59, 164.93, 269.0, 126.90, 114.82, 192.22, 39.098,
            83.80, 138.91, 6.941, 262.0, 174.97, 258.0, 24.305, 54.938, 95.94,
            268.0, 14.007, 22.990, 92.906, 144.24, 20.180, 58.693, 259.0,
            237.0, 15.999, 190.23, 30.974, 231.04, 207.2, 106.42, 145.0,
            209.0, 140.91, 196.08, 244.0, 226.0, 85.468, 186.21, 261.0,
            102.91, 222.0, 101.07, 32.065, 121.76, 44.956, 78.96, 266.0,
            28.086, 150.36, 118.71, 87.62, 180.95, 158.93, 97.61, 127.60,
            232.04, 47.867, 204.38, 168.93, 238.03, 50.942, 183.84, 131.29,
            88.906, 173.04, 65.39, 91.224)
        Assert(CalculateMass(a) == sum(b))
if 1:   # Core functionality
    def PrintTable():
        out, w = [], 70
        for i in atomic_mass:
            out.append(f"{i:2s} {atomic_mass[i]!s:>6s}")
        t.print(f"{t('purl')}{'Atomic masses in g/mol':^{w}s}")
        for i in Columnize(out, col_width=15):
            print(i)
        # Now print sorted by mass
        m = []
        for i in atomic_mass:
            m.append((atomic_mass[i], i))
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
            if tok == ')':
                count -= 1
                if count == 0:
                    return index
            elif tok == '(':
                count += 1
        raise ValueError('unmatched parentheses')
    def Parse(tokens, stack, dict):
        if len(tokens) == 0:
            return sum(stack)
        tok = tokens[0]
        if tok == '(':
            end = Find_closing_paren(tokens)
            stack.append(Parse(tokens[1:end], [], dict))
            return Parse(tokens[end + 1:], stack, dict)
        elif tok.isdigit():
            stack[-1] *= int(tok)
        else:
            stack.append(dict[tok])
        return Parse(tokens[1:], stack, dict)
    def CalculateMass(formula):
        tokens = re.findall(r'[A-Z][a-z]*|\d+|\(|\)', formula)
        if not tokens:
            raise Exception("Empty")
        return Parse(tokens, [], atomic_mass)
    def GetMass(formula):
        try:
            print(f"{formula}: {CalculateMass(formula)} g/mol")
        except Exception as e:
            print(f"{formula!r} is an incorrect formula")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    for arg in args:
        GetMass(arg)
