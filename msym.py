'''
 
Provide for simple command line mathematical equations
 
Call the Interpret(s) function with a string s to have it converted to a
Unicode string with special characters, exponents, and subscripts
substituted.  
 
Special characters are indicated by the '%' character followed by a
string.  For example, the lowercase Greek letters are the first three
characters of their names.  The capital Greek letters are the same
except the first letter is capitalized.  Example:  '%alp' represents a
lowercase alpha.
 
Exponents are indicated with '^{s}' where s is a string of allowed
characters (see the Interpret function for what's allowed).
Analogously, use '_{s}' for subscripts.  Note the curly brackets are
required.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2016 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <math> Make simple math equations from the command line using
    # Unicode.
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import re
if 1:   # Custom imports
    from columnize import Columnize
def _GetSymbols():
    '''Attach attributes to the Interpret function:
 
    symbols:  A dictionary containing the symbols and their Unicode equivalent.
    rsub:  regexp for finding subscript expressions.
    rsup:  regexp for finding superscript expressions.
    '''
    _symbols = '''
    # Lowercase Greek letters
    alp α, bet β, gam ɣ, del δ, eps ϵ, eps1 ɛ, zet ζ, eta η, the θ, iot
    ɩ, kap κ, lam λ, mu μ, nu ν, xi ξ, omi ο, pi π, rho ρ, sig σ, tau τ,
    ups ʊ, phi φ, phi1 chr(0x03d5), chi χ, psi ψ, ome ω,
 
    # Uppercase Greek letters
    Alp Α, Bet Β, Gam Γ, Del Δ, Eps Ε, Zet Ζ, Eta Η, The Θ, Iot Ι, Kap
    Κ, Lam Λ, Mu Μ, Nu Ν, Xi Ξ, Omi Ο, Pi Π, Rho Ρ, Sig Σ, Tau Τ, Ups Υ,
    Phi Φ, Chi Χ, Psi Ψ, Ome Ω,
 
    # Other characters
    deg °, sqrt √, inf ∞, dot ·, pm ±, mp ∓, ge ≥, le ≤, ne ≠, identical ≡,
    def ≝, and ∧, or ∨, intersection ∩, union ∪, therefore ∴, 
    times ×, divide ÷, prop ∝, suchthat ∍, insmall ∊, in ∈, notin ∉, 
    null ∅, exists ∃, forall ∀, arc ∡, angle ∠, parallel ∥, 
    real ℝ, complex ℂ, integer ℤ, whole ℕ, rational ℚ, im ℐ, re ℛ,
    notsubset ⊄, subset ⊂, 
    partial ∂, integral ∫, nabla ∇
    '''
    S, symbols, s = Interpret, {}, []
    for line in _symbols.split("\n"):
        l = line.strip()
        if not l or l[0] == "#":
            continue
        s.append(l)
    s = ' '.join(s)
    s.replace("\n", " ")
    for i in s.split(","):
        if not i:
            continue
        name, sym = i.strip().split()
        if sym.startswith("chr(0x"):
            sym = eval(sym)
        symbols["%" + name] = sym
    S.symbols = symbols
    # These are the characters allowed by Unicode
    superscripts  = r"+-0123456789in\(\)"
    superscripts1 =  "⁺⁻⁰¹²³⁴⁵⁶⁷⁸⁹ⁱⁿ⁽⁾"
    subscripts  = r"+-0123456789jtspnmlkhxoeavuri\(\)"
    subscripts1 =  "₊₋₀₁₂₃₄₅₆₇₈₉ⱼₜₛₚₙₘₗₖₕₓₒₑₐᵥᵤᵣᵢ₍₎"
    S.supersub = {}
    for i, char in enumerate(superscripts.replace("\\", "")):
        S.supersub[char] = superscripts1[i]
    S.subsub = {}
    for i, char in enumerate(subscripts.replace("\\", "")):
        S.subsub[char] = subscripts1[i]
    # Compile superscript/subscript regular expressions
    S.rsub = re.compile(r"(_{[" + subscripts + "]+})")
    S.rsup = re.compile(r"(\^{[" + superscripts + "]+})")
    # Compile special character subscripts
    s = ["(" + i + ")" for i in symbols]
    S.special_chars = re.compile('|'.join(s))
def Interpret(s):
    '''Change the string s into an expression by substituting for the
    special characters and superscripts/subscripts.
 
    Example:  if s is '%%%alp^{-32} %bet^{3i} %gam_{2} %del_{3i}', the
    returned string is '%α⁻³² β³ⁱ ɣ₂ δ₃ᵢ'.
    '''
    S = Interpret
    if not hasattr(Interpret, "symbols"):
        _GetSymbols()
    pct_sym = chr(0x1f4a9)
    # Get rid of any actual '%' characters
    s = s.replace("%%", pct_sym)
    # Replace special characters
    mo = S.special_chars.search(s)
    while mo:
        t = s[mo.start():mo.end()]
        s = s.replace(t, S.symbols[t])
        mo = S.special_chars.search(s)
    # Superscripts
    mo = S.rsup.search(s)
    while mo:
        g = mo.groups()[0]
        e = []
        for i in g[2:-1]:
            e.append(S.supersub[i])
        e = ''.join(e)
        s = s[:mo.start()] + e + s[mo.end():]
        mo = S.rsup.search(s)
    # Subscripts
    mo = S.rsub.search(s)
    while mo:
        g = mo.groups()[0]
        e = []
        for i in g[2:-1]:
            e.append(S.subsub[i])
        e = ''.join(e)
        s = s[:mo.start()] + e + s[mo.end():]
        mo = S.rsub.search(s)
    s = s.replace(pct_sym, "%")
    return s
def DumpSupportedCharacters():
    s = []
    for name, sym in sorted(Interpret.symbols.items()):
        s.append(name[1:] + " " + sym)
    for i in Columnize(s, indent=" "*2):
        print(i)
if __name__ == "__main__":
    t = "%%%alp^{-32} %bet^{3i} %gam_{2} %del_{3i}"
    s = Interpret(t)
    print('''Example:
    t = {}
    Interpret(t) = {}'''.format(t, s))
    assert(s == "%α⁻³² β³ⁱ ɣ₂ δ₃ᵢ")
    print("Supported characters:")
    DumpSupportedCharacters()
