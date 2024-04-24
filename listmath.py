'''
Prints out math/cmath functions and their syntax
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
        # Prints out math/cmath functions and their syntax
        #∞what∞#
        #∞test∞# ignore #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import namedtuple
        import cmath
        import math
        import os
        import platform
        import sys
    if 1:   # Custom imports
        from color import t
        from dpprint import PP
        pp = PP()   # Screen width aware form of pprint.pprint
        from columnize import Columnize
if 1:
    def GetSymbols():
        data = '''
            # num_args signature
            1 math.ceil(x)
            2 math.comb(n, k)
            2 math.copysign(x, y)
            1 math.fabs(x)
            1 math.factorial(x)
            1 math.floor(x)
            2 math.fmod(x, y)
            1 math.frexp(x)
            i math.fsum(iterable)
            * math.gcd(*integers)
            4 math.isclose(a, b, *, rel_tol=1e-09, abs_tol=0.0)
            1 math.isfinite(x)
            1 math.isinf(x)
            1 math.isnan(x)
            1 math.isqrt(n)
            * math.lcm(*integers)
            2 math.ldexp(x, i)
            1 math.modf(x)
            2 math.nextafter(x, y)
            2 math.perm(n, k=None)
            i math.prod(iterable, *, start=1)
            2 math.remainder(x, y)
            1 math.trunc(x)
            1 math.ulp(x)
            1 math.exp(x)
            1 math.exp2(x)
            1 math.expm1(x)
            2 math.log(x[, base])
            1 math.log1p(x)
            1 math.log2(x)
            1 math.log10(x)
            2 math.pow(x, y)
            1 math.sqrt(x)
            1 math.cbrt(x)
            1 math.acos(x)
            1 math.asin(x)
            1 math.atan(x)
            2 math.atan2(y, x)
            1 math.cos(x)
            2 math.dist(p, q)
            * math.hypot(*coordinates)
            1 math.sin(x)
            1 math.tan(x)
            1 math.degrees(x)
            1 math.radians(x)
            1 math.acosh(x)
            1 math.asinh(x)
            1 math.atanh(x)
            1 math.cosh(x)
            1 math.sinh(x)
            1 math.tanh(x)
            1 math.erf(x)
            1 math.erfc(x)
            1 math.gamma(x)
            1 math.lgamma(x)
            0 math.pi
            0 math.e
            0 math.tau
            0 math.inf
            0 math.nan
 
            1 cmath.phase(x)
            1 cmath.polar(x)
            2 cmath.rect(r, phi)
            1 cmath.exp(x)
            2 cmath.log(x[, base])
            1 cmath.log10(x)
            1 cmath.sqrt(x)
            1 cmath.acos(x)
            1 cmath.asin(x)
            1 cmath.atan(x)
            1 cmath.cos(x)
            1 cmath.sin(x)
            1 cmath.tan(x)
            1 cmath.acosh(x)
            1 cmath.asinh(x)
            1 cmath.atanh(x)
            1 cmath.cosh(x)
            1 cmath.sinh(x)
            1 cmath.tanh(x)
            1 cmath.isfinite(x)
            1 cmath.isinf(x)
            1 cmath.isnan(x)
            4 cmath.isclose(a, b, *, rel_tol=1e-09, abs_tol=0.0)
            0 cmath.pi
            0 cmath.e
            0 cmath.tau
            0 cmath.inf
            0 cmath.infj
            0 cmath.nan
            0 cmath.nanj
        '''
        o = []
        for line in data.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            numargs, s = line.split(sep=" ", maxsplit=1)
            module, func = s.split(sep=".", maxsplit=1)
            if numargs == "0":
                fname = func
                arg = None
            else:
                fname, arg = func.split(sep="(", maxsplit=1)
                arg = "(" + arg
            clr = t.m if module[0] == "m" else t.c
            e = entry(module[0], numargs, fname, arg, clr)
            o.append(e)
        return o
    def uniq(x):
        return list(sorted(set(x)))
    def Prt1(title, s):
        'Print the columnized colorized names'
        t.print(title)
        sym = []
        for i in s:
            sym.append((i.name, i))
        out = []
        for name, entry in sorted(sym):
            out.append(f"{entry.color}{name}{t.n}")
        for i in Columnize(out, indent=ind, esc=True):
            print(i)
    def Prt2(title, s):
        'Print the names'
        t.print(title)
        sym = []
        for i in s:
            sym.append((i.name, i))
        out = []
        for name, entry in sorted(sym):
            lib = "cmath" if entry.lib == "c" else "math"
            lib = f"{entry.color}{lib}"
            s = f"{lib}.{name}{entry.args}{t.n}"
            out.append(s)
        for i in Columnize(out, indent=ind, esc=True):
            print(i)
    def MathReport():
        'Show the math/cmath symbols'
        if 1:   # Get & check data
            o = GetSymbols()
            # Make dicts for math & cmath modules' symbols
            m, c = {}, {}
            for i in o:
                if i.lib == "m":
                    m[i.name] = i
                else:
                    c[i.name] = i
            # Make sure all math/cmath symbols are defined
            for i in dir(math):
                if i.startswith("__"):
                    continue
                if i not in m:
                    print("Error:  math.{i!r} not in data")
            for i in dir(cmath):
                if i.startswith("__"):
                    continue
                if i not in c:
                    print("Error:  cmath.{i!r} not in data")
        # Report
        t.print(f"{t('ornl')}math/cmath functions for python {platform.python_version()}")
        print(f"{ind}Produced by {__file__}")
        t.print(f"{ind}Colors:  {t.m}math{t.n}  {t.c}cmath")
        if 1:   # All symbols
            t.print(f"{t('grnl')}All symbols")
            sym = []
            for i in o:
                sym.append((i.name, i))
            out = []
            for name, entry in sorted(sym):
                out.append(f"{entry.color}{name}{t.n}")
            for i in Columnize(out, indent=ind, esc=True):
                print(i)
        if 1:   # Names organized by calling type
            print("-"*W)
            t.print(f"{t.hdr}Names organized by calling type")
            if 1:   # Constants
                s = [i for i in o if i.n == "0"]
                Prt1(f"{t.type}Constants", s)
            if 1:   # Univariate
                univariate = [i for i in o if i.n == "1"]
                Prt1(f"{t.type}Univariate", univariate)
            if 1:   # Bivariate
                bivariate = [i for i in o if i.n == "2"]
                Prt1(f"{t.type}Bivariate", bivariate)
            if 1:   # Iterator
                iterator = [i for i in o if i.n == "i"]
                Prt1(f"{t.type}Iterator", iterator)
            if 1:   # List of arguments
                list_of_arguments = [i for i in o if i.n == "*"]
                Prt1(f"{t.type}List of arguments", list_of_arguments)
            if 1:   # Other
                other = [i for i in o if i.n == "4"]
                Prt1(f"{t.type}Other", other)
        if 1:   # Argument syntax for functions
            print("-"*W)
            t.print(f"{t.hdr}Argument syntax for functions")
            Prt2(f"{t.type}Univariate", univariate)
            Prt2(f"{t.type}Bivariate", bivariate)
            Prt2(f"{t.type}Iterator", iterator)
            Prt2(f"{t.type}List of arguments", list_of_arguments)
            Prt2(f"{t.type}Other", other)

if __name__ == "__main__":  
    entry = namedtuple("Entry", "lib n name args color")
    t.m = t("brnl")
    t.c = t("denl")
    t.type = t("grnl")
    t.hdr = t("whtl", "royd")
    ind = " "*2
    W = int(os.environ.get("COLUMNS", "80")) - 1
    MathReport()
