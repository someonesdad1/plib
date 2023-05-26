'''
Print out a table showing the math/cmath functions and their return types.
Done for python 3.9.10.
'''
from wrap import dedent
from astr import alen
from color import t
if 1:
    import debug
    debug.SetDebugger()
if 0:   # Header
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
        import math
        import cmath
        import os
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, t
        from columnize import Columnize
        if 1:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        # name args ; returns [; note]
        # seq = sequence of integers or floats
        # fseq = float sequence
        # iseq = int sequence

        mathfuncs = '''
            acos        float; float
            acosh       float; float
            asin        float; float
            asinh       float; float
            atan        float; float
            atan2       float, float; float
            atanh       float; float
            ceil        float; int
            comb        int, int; int
            copysign    float, float; float
            cos         float; float
            cosh        float; float
            degrees     float; float
            dist        fseq, fseq; float
            erf         float; float
            erfc        float; float
            exp         float; float
            expm1       float; float
            fabs        float; float
            factorial   int; int
            floor       float; int
            fmod        float, float; float
            frexp       float; float, int
            fsum        seq; float 
            gamma       float; float
            gcd         iseq; int
            hypot       seq; float    
            isclose     float, float; bool
            isfinite    float; bool 
            isinf       float; bool
            isnan       float; bool
            isqrt       int; int 
            lcm         iseq; int
            ldexp       float, int; float
            lgamma      float; float
            log         float, =float; float
            log10       float; float
            log1p       float; float
            log2        float; float
            modf        float; float, float 
            nextafter   float, float; float
            perm        int, =int; int 
            pow         float, float; float
            prod        seq, =float; float; (int if all of iter are ints)
            radians     float; float
            remainder   float, float; float
            sin         float; float 
            sinh        float; float 
            sqrt        float; float 
            tan         float; float 
            tanh        float; float 
            trunc       float; int 
            ulp         float; float 

        '''
        # cmath's functions can take arguments of int, float, or complex
        cmathfuncs = '''
            acos        z; complex
            acosh       z; complex
            asin        z; complex
            asinh       z; complex
            atan        z; complex
            atanh       z; complex
            cos         z; complex
            cosh        z; complex
            exp         z; complex
            isclose     z, z; bool 
            isfinite    z; bool
            isinf       z; bool
            isnan       z; bool
            log         z; complex
            log10       z; complex
            phase       z; float
            polar       z; float, float
            rect        float, float; complex
            sin         z; complex
            sinh        z; complex
            sqrt        z; complex
            tan         z; complex
            tanh        z; complex
        '''
        # Colors
        C = {
            "bool": t("magl"),
            "int": t("lwnl"),

            "float": t("yell"),
            "complex": t("cynl"),
            "z": t("purl"),
        }
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = 3         # Number of significant digits
        #if len(sys.argv) < 2:
        #    Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
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
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        return args
if 1:   # Core functionality
    def GetMathFuncs(show=False):
        funcs = []
        for i in dir(math):
            if i.startswith("__"):
                continue
            f = eval(f"math.{i}")
            t = type(f)
            if "float" in str(t):
                continue
            funcs.append(i)
        if show:
            print("Math functions:")
            for i in Columnize(funcs, indent=" "*2):
                print(i)
        return funcs
    def GetCMathFuncs(show=False):
        funcs = []
        print()
        for i in dir(cmath):
            if i.startswith("__"):
                continue
            f = eval(f"cmath.{i}")
            t = type(f)
            if "float" in str(t):
                continue
            funcs.append(i)
        if show:
            print("Cmath functions:")
            for i in Columnize(funcs, indent=" "*2):
                print(i)
        return funcs
    def CheckMathFuncs():
        for line in mathfuncs.strip().split("\n"):
            line = line.strip()
            if not line or line[0] == "#":
                continue
            func = line[:12].strip()
            input, output = [i.strip() for i in line[12:].split(";")]
            #print(func, input, output)
            if input == "[float]" and output == "[float]":
                x = 0.5
                try:
                    y = eval(f"math.{func}(x)")
                except ValueError:
                    y = eval(f"math.{func}(3*x)")
                if not ii(y, float):
                    raise Exception(f"{func}:  bad type")

if 0 and __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if 0:
        if 1:
            mathfuncs = GetMathFuncs()
            cmathfuncs = GetCMathFuncs(show=1)
        else:
            CheckMathFuncs()
    else:
        for line in cmathfuncs.split("\n"):
            line = line.strip()
            if not line:
                continue
            name = line[:12].strip()
            a, b = line[12:].strip().split(";")
            a, b = [i.strip() for i in (a, b)]
            ca = C["z"] if "z" in a else C["float"]
            if b in "bool float complex".split():
                cb = C[b]
            else:
                assert("," in b)
                cb = C["float"]
            t.print(f"{name}({ca}{a}{t.n}) → {cb}{b}")

#------------------------------------------------------------------------------
b = t("magl")
i = t("lwnl")
f = t("yell")
c = t("cynl")
z = t("purl")
x = t("ornl")
r = t("redl")
e = "∊"
s = dedent(f'''
    python 3.9.10 math functions

    acos(x) ;  float ; complex
    acosh(x) ;  float ; complex
    asin(x) ;  float ; complex
    asinh(x) ;  float ; complex
    atan(x) ;  float ; complex
    atan2(y, x) ;  float
    atanh(x) ;  float ; complex
    ceil(x) ;  int
    comb(n, m) ;  int
    copysign(x, y) ;  float
    cos(x) ;  float
    cosh(x) ;  float
    degrees(x) ;  float
    dist(fseq, fseq) ;  float
    erf(x) ;  float
    erfc(x) ;  float
    exp(x) ;  float ; complex
    expm1(x) ;  float
    fabs(x) ;  float
    factorial(n) ;  int
    floor(x) ;  int
    fmod(x, y) ;  float
    frexp(x) ;  float, int
    fsum(fseq) ;  float 
    gamma(x) ;  float
    gcd(iseq) ;  int
    hypot(fseq) ;  float    
    isclose(x, y) ;  bool ; bool
    isfinite(x) ;  bool  ; bool
    isinf(x) ;  bool ; bool
    isnan(x) ;  bool ; bool
    isqrt(n) ;  int 
    lcm(iseq) ;  int
    ldexp(x, n) ;  float
    lgamma(x) ;  float
    log(x, =y) ;  float ; complex
    log10(x) ;  float ; complex
    log1p(x) ;  float
    log2(x) ;  float
    modf(x) ;  float, float 
    nextafter(x, y) ;  float
    perm(n, =m) ;  int 
    pow(x, y) ;  float
    prod(fseq, =x) ;  float
    radians(x) ;  float
    remainder(x, y) ;  float
    sin(x) ;  float  ; complex
    sinh(x) ;  float  ; complex
    sqrt(x) ;  float  ; complex
    tan(x) ;  float  ; complex
    tanh(x) ;  float  ; complex
    trunc(x) ;  int 
    ulp(x) ;  float 

    ''')

def F(s):
    s = s.replace("(x)", f"({x}x{t.n})")
    s = s.replace("(x,", f"({x}x{t.n},")
    s = s.replace("=x)", f"={x}x{t.n})")
    s = s.replace("y)", f"{x}y{t.n})")
    s = s.replace("(n,", f"({i}n{t.n},")
    s = s.replace("n)", f"{i}n{t.n})")
    s = s.replace(" m)", f" {i}m{t.n})")
    s = s.replace("=m)", f"={i}m{t.n})")
    s = s.replace("iseq", f"{i}iseq{t.n}")
    s = s.replace("fseq", f"{x}fseq{t.n}")
    s = s.replace("float", f"{x}float{t.n}")
    s = s.replace("complex", f"{c}complex{t.n}")
    s = s.replace("int", f"{i}int{t.n}")
    s = s.replace("bool", f"{b}bool{t.n}")
    s = s.replace("(z)", f"({z}z{t.n})")
    return s

# Print the elements in columns
for line in s.split("\n"):
    if "python" in line:
        print(line)
        print(f"{' '*28}Return type(s)")
        t.print(f"{' '*22}{r}math{' '*16}cmath")
        t.print(f"{' '*22}{r}----{' '*16}-----")
        continue
    if not line.strip():
        #print()
        continue
    g = line.split(";")
    name = F(g[0])
    print(name, end=" "*(20 - alen(name)))
    mret = F(g[1])
    print(mret, end=" "*(20 - alen(mret)))
    if len(g) > 2:
        print(F(g[2]))
    else:
        print()
print()
s = dedent('''
    phase(z); float
    polar(z); float, float
    rect(float, float) ; complex
''')
for line in s.split("\n"):
    if not line:
        continue
    g = line.split(";")
    name = F(g[0])
    print(name, end=" "*(40 - alen(name)))
    cmret = F(g[1])
    print(F(cmret))
print()
t.print(f'''
Type color coding:  {b}bool    {i}int    {f}float    {c}complex{t.n}
    {x}x{t.n}, {x}y{t.n} {e} {{{i}int{t.n}, {f}float{t.n}}}
    {z}z{t.n} {e} {{{i}int{t.n}, {f}float{t.n}, {c}complex{t.n}}}
    iseq = sequence of {i}int{t.n}
    fseq = sequence of {i}int{t.n} or {f}float{t.n}
'''.strip())
