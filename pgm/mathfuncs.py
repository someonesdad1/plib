"""
Print out a table showing the math/cmath functions and their return types.
"""

from wrap import dedent
from astr import alen
from color import t

b = t("magl")
i = t("lwnl")
f = t("yell")
c = t("cynl")
z = t("purl")
x = t("ornl")
r = t("redl")
e = "∊"

s = dedent(f"""
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
    """)


def F(s):
    "Put in color-coding"
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
        print(f"{' ' * 28}Return type(s)")
        t.print(f"{' ' * 22}{r}math{' ' * 16}cmath")
        t.print(f"{' ' * 22}{r}----{' ' * 16}-----")
        continue
    if not line.strip():
        # print()
        continue
    g = line.split(";")
    name = F(g[0])
    print(name, end=" " * (20 - alen(name)))
    mret = F(g[1])
    print(mret, end=" " * (20 - alen(mret)))
    if len(g) > 2:
        print(F(g[2]))
    else:
        print()
print()
s = dedent("""
    phase(z); float
    polar(z); float, float
    rect(float, float) ; complex
""")
for line in s.split("\n"):
    if not line:
        continue
    g = line.split(";")
    name = F(g[0])
    print(name, end=" " * (40 - alen(name)))
    cmret = F(g[1])
    print(F(cmret))
print()
t.print(
    f"""
Type color coding:  {b}bool    {i}int    {f}float    {c}complex{t.n}
    {x}x{t.n}, {x}y{t.n} {e} {{{i}int{t.n}, {f}float{t.n}}}
    {z}z{t.n} {e} {{{i}int{t.n}, {f}float{t.n}, {c}complex{t.n}}}
    iseq = sequence of {i}int{t.n}
    fseq = sequence of {i}int{t.n} or {f}float{t.n}
""".strip()
)
