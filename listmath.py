'''
This scripts lets you look up or show all of the math functions in math
and cmath modules.
'''
#∞test∞# ignore #∞test∞#
import sys
from columnize import Columnize
from collections import namedtuple, defaultdict
from pprint import pprint as pp
from pdb import set_trace as xx
if len(sys.argv) > 1:
    import debug
    debug.SetDebugger()
if 1:
    rawdata = {
        # Num_args, function signature
        # * = list of args
        # i = one iterable
        "3.7.4 math": '''
            1 math.ceil(x)
            2 math.copysign(x, y)
            1 math.fabs(x)
            1 math.factorial(x)
            1 math.floor(x)
            2 math.fmod(x, y)
            1 math.frexp(x)
            i math.fsum(iterable)
            2 math.gcd(a, b)
            4 math.isclose(a, b, *, rel_tol=1e-09, abs_tol=0.0)
            1 math.isfinite(x)
            1 math.isinf(x)
            1 math.isnan(x)
            2 math.ldexp(x, i)
            1 math.modf(x)
            2 math.remainder(x, y)
            1 math.trunc(x)
            1 math.exp(x)
            1 math.expm1(x)
            2 math.log(x[, base])
            1 math.log1p(x)
            1 math.log2(x)
            1 math.log10(x)
            2 math.pow(x, y)
            1 math.sqrt(x)
            1 math.acos(x)
            1 math.asin(x)
            1 math.atan(x)
            2 math.atan2(y, x)
            1 math.cos(x)
            2 math.hypot(x, y)
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
            ''',
        "3.7.4 cmath": '''
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
            ''',
        "3.9.4 math": '''
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
            1 math.expm1(x)
            2 math.log(x[, base])
            1 math.log1p(x)
            1 math.log2(x)
            1 math.log10(x)
            2 math.pow(x, y)
            1 math.sqrt(x)
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
            ''',
        "3.9.4 cmath": '''
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
            ''',
    }

    def GetData():
        'Return list of named tuples'
        entry = namedtuple("Entry", "ver lib n name args")
        o = []
        for k in rawdata:
            for i in rawdata[k].split("\n"):
                i = i.strip()
                if not i:
                    continue
                version, whichlib = k.split()
                version = version.replace(".", "")
                n, s = i.split(sep=" ", maxsplit=1)
                m, func = s.split(sep=".", maxsplit=1)
                assert(whichlib == m)
                if n == "0":
                    fname = func
                    arg = None
                else:
                    fname, arg = func.split(sep="(", maxsplit=1)
                    arg = "(" + arg
                t = entry(version, m[0], n, fname, arg)
                o.append(t)
        return o

    def PrintCols(lst, indent=" "*2):
        for line in Columnize(lst, indent=indent):
            print(line)

    def Version(item):
        v = '.'.join(list(f"{item.ver}"))
        return f"Version {v}"

    def Report(math, cmath):
        ver = Version(math[0])
        m = [i.name for i in math]
        if 0:
            print(f"{ver} math:")
            PrintCols(m)
        c = [i.name for i in cmath]
        if 0:
            print(f"{ver} cmath:")
            PrintCols(c)
        m, c = set(m), set(c)
        print(f"{ver} names common to math & cmath:")
        com = m & c
        PrintCols(sorted(list(com)))
        print(f"{ver} names only in math:")
        only = m - c
        PrintCols(sorted(list(only)))
        print(f"{ver} names only in cmath:")
        only = c - m
        PrintCols(sorted(list(only)))

if __name__ == "__main__": 
    print(f'''Python math/cmath differences (compiled 13 Apr 2021)
    3.9.4 data collected from web pages at:
        https://docs.python.org/3/py-modindex.html
    (Produced by /pylib/{__file__})
    ''')
    sep = "-"*70
    # Split into two lists by version
    data = GetData()
    d394 = [i for i in data if i.ver == "394"]
    d374 = [i for i in data if i.ver == "374"]
    # Get math & cmath lists
    math394 = [i for i in d394 if i.lib == "m"]
    cmath394 = [i for i in d394 if i.lib == "c"]
    math374 = [i for i in d374 if i.lib == "m"]
    cmath374 = [i for i in d374 if i.lib == "c"]

    # Report commonalities
    Report(math394, cmath394)
    if 0:
        print(sep)
        Report(math374, cmath374)

    # Show diffs between 374 and 394
    v394 = Version(math394[0])
    v374 = Version(math374[0])
    m374 = set([i.name for i in math374 + cmath374])
    m394 = set([i.name for i in math394 + cmath394])
    print(sep)
    n = ' '.join(sorted(list(m394 - m374)))
    print(f"New to {v394}: ", n)
    print(f"Removed from {v374}: ", ' '.join(list(m374 - m394)))
    print(sep)

    # Print all names
    def uniq(x):
        return list(sorted(list(set(x)))) 
    all_names = uniq([i.name for i in d394])
    print(f"All math/cmath names for {v394} (count = {len(all_names)}):")
    PrintCols(all_names)
    print(sep)
    # Now print univariate, bivariate, etc.
    print(f"Names organized by calling type:")
    types = set(i.n for i in d394)
    all = []  # Check we got them all
    # Constants
    s = uniq(i.name for i in d394 if i.n == "0")
    print(f"\nConstants:  {' '.join(s)}")
    all.extend(s)
    # Univariate
    print(f"\nUnivariate:")
    s = uniq(i.name for i in d394 if i.n == "1")
    univariate = uniq(i for i in d394 if i.n == "1")
    PrintCols(s)
    all.extend(s)
    # Bivariate
    print(f"\nBivariate:")
    s = uniq(i.name for i in d394 if i.n == "2")
    bivariate = uniq(i for i in d394 if i.n == "2")
    PrintCols(s)
    all.extend(s)
    # Iterator
    print(f"\nIterator:")
    s = uniq(i.name for i in d394 if i.n == "i")
    iterator = uniq(i for i in d394 if i.n == "i")
    PrintCols(s)
    all.extend(s)
    # List of args
    print(f"\nList of arguments:")
    s = uniq(i.name for i in d394 if i.n == "*")
    list_of_args = uniq(i for i in d394 if i.n == "*")
    PrintCols(s)
    all.extend(s)
    # Other
    print(f"\nOthers:")
    s = uniq(i.name for i in d394 if i.n == "4")
    other = uniq(i for i in d394 if i.n == "4")
    PrintCols(s)
    all.extend(s)
    # Verify we printed all of them
    a = set(all)
    o = set(i.name for i in d394)
    assert(a == o)
    def P(title, container):
        print(f"\n{title}")
        for i in sorted(container, key=kf):
            lib = "cmath" if i.lib == "c" else "math"
            s = f"    {lib}.{i.name}{i.args}"
            print(s)
    # Now print argument syntax for non-univariate functions
    print(sep)
    print("Argument syntax for functions")
    def kf(x):
        return x.name
    P("Univariate", univariate)
    P("Bivariate", bivariate)
    P("Iterator", iterator)
    P("List of arguments", list_of_args)
    P("Other", other)
    if 0:
        # Show a data element
        print(math394[0])
