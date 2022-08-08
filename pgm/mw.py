# From https://gist.github.com/Rhomboid/5994999
# Downloaded Tue 12 Aug 2014 02:23:51 PM
# Minor modifications by DP.

import re
import sys
from lwtest import run, assert_equal
from pdb import set_trace as xx

atomic_mass = {
    "Ac": 227.0,
    "Ag": 107.87,
    "Al": 26.982,
    "Am": 243.0,
    "Ar": 39.948,
    "As": 74.922,
    "At": 210.0,
    "Au": 196.08,
    "B": 10.811,
    "Ba": 137.33,
    "Be": 9.0122,
    "Bh": 264.0,
    "Bi": 208.98,
    "Bk": 247.0,
    "Br": 79.904,
    "C": 12.011,
    "Ca": 40.078,
    "Cd": 112.41,
    "Ce": 140.12,
    "Cf": 251.0,
    "Cl": 35.453,
    "Cm": 247.0,
    "Co": 58.933,
    "Cr": 51.996,
    "Cs": 132.91,
    "Cu": 63.546,
    "Db": 262.0,
    "Dy": 162.50,
    "Er": 167.26,
    "Es": 252.0,
    "Eu": 151.96,
    "F": 18.998,
    "Fe": 55.845,
    "Fm": 257.0,
    "Fr": 223.0,
    "Ga": 69.723,
    "Gd": 157.25,
    "Ge": 72.61,
    "H": 1.0079,
    "He": 4.0026,
    "Hf": 178.49,
    "Hg": 200.59,
    "Ho": 164.93,
    "Hs": 269.0,
    "I": 126.90,
    "In": 114.82,
    "Ir": 192.22,
    "K": 39.098,
    "Kr": 83.80,
    "La": 138.91,
    "Li": 6.941,
    "Lr": 262.0,
    "Lu": 174.97,
    "Md": 258.0,
    "Mg": 24.305,
    "Mn": 54.938,
    "Mo": 95.94,
    "Mt": 268.0,
    "N": 14.007,
    "Na": 22.990,
    "Nb": 92.906,
    "Nd": 144.24,
    "Ne": 20.180,
    "Ni": 58.693,
    "No": 259.0,
    "Np": 237.0,
    "O": 15.999,
    "Os": 190.23,
    "P": 30.974,
    "Pa": 231.04,
    "Pb": 207.2,
    "Pd": 106.42,
    "Pm": 145.0,
    "Po": 209.0,
    "Pr": 140.91,
    "Pt": 196.08,
    "Pu": 244.0,
    "Ra": 226.0,
    "Rb": 85.468,
    "Re": 186.21,
    "Rf": 261.0,
    "Rh": 102.91,
    "Rn": 222.0,
    "Ru": 101.07,
    "S": 32.065,
    "Sb": 121.76,
    "Sc": 44.956,
    "Se": 78.96,
    "Sg": 266.0,
    "Si": 28.086,
    "Sm": 150.36,
    "Sn": 118.71,
    "Sr": 87.62,
    "Ta": 180.95,
    "Tb": 158.93,
    "Tc": 97.61,
    "Te": 127.60,
    "Th": 232.04,
    "Ti": 47.867,
    "Tl": 204.38,
    "Tm": 168.93,
    "U": 238.03,
    "V": 50.942,
    "W": 183.84,
    "Xe": 131.29,
    "Y": 88.906,
    "Yb": 173.04,
    "Zn": 65.39,
    "Zr": 91.224
}

def find_closing_paren(tokens):
    count = 0
    for index, tok in enumerate(tokens):
        if tok == ')':
            count -= 1
            if count == 0:
                return index
        elif tok == '(':
            count += 1
    raise ValueError('unmatched parentheses')

def parse(tokens, stack=None):
    if stack is None:
        stack = []
    if len(tokens) == 0:
        return sum(stack)
    tok = tokens[0]
    if tok == '(':
        end = find_closing_paren(tokens)
        stack.append(parse(tokens[1:end], []))
        return parse(tokens[end + 1:], stack)
    elif tok.isdigit():
        stack[-1] *= int(tok)
    else:
        stack.append(atomic_mass[tok])
    return parse(tokens[1:], stack)

def MolarMass(formula):
    '''A token is:
        * A chemical name composed of a capital letter followed by
          zero or more lower case letters.
        * A sequence of digits.
        * A '(' or a ')'.
    '''
    tokens = re.findall(r'[A-Z][a-z]*|\d+|\(|\)', formula)
    return parse(tokens)

def Test():
    data = (
        ("Ca(C2H3O2)2", 158.165),
        ("(NH4)2SO4", 132.138),
        ("(NH4)(NO3)", 80.043),
        ("(((H2O)4)3)8", 1729.421),
    )
    for formula, result in data:
        mw = MolarMass(formula)
        assert_equal(mw, result, abstol=0.01)

if __name__ == "__main__":
    # Use -t to run tests
    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        fail, msg = run(globals(), quiet=True)
        if fail:
            print("Tests failed")
            exit(1)
        print("Tests passed")
        exit(0)
    msg = "Molar mass of {0} = {1:.2f} g/mol"
    if len(sys.argv) == 1:
        print('''
Prints the molecular mass of a chemical formula.  You must enter a
formula using the standard chemical name symbols (e.g., Cl, Fe, etc.).
Example:  water is H2O with a molecular weight of 18.01.
'''[1:])
        while True:
            formula = input("Input a formula: ").strip()
            if not formula or formula.lower() == "q":
                break
            try:
                mw = MolarMass(formula)
                print(msg.format(formula, mw))
            except Exception as e:
                print("Error:  %s" % e)
    else:
        # Use the formula(s) from the command line
        for formula in sys.argv[1:]:
            try:
                mw = MolarMass(formula)
                print(msg.format(formula, mw))
            except Exception as e:
                print("Error:  %s" % e)
