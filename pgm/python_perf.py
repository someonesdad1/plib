"""
Print execution time of some math operations
    You can pass the value of N, which is the number of times to
    repeat the timeit() measurement, on the command line; it defaults to 1e5.
    I've found that 1e5 seems to be a good choice to give reasonably
    repeatable results and not take too long to execute.

        Time to execute in 2011 was about 16 s.  With my computer built
        in 2016, it took 5 s in 2021.

    If mpmath is present, the script will print out times for some mpmath
    functions.  This was written for mpmath version 0.12, so some functions
    in later versions aren't present.  Before you sneer at the mpmath
    performance (it's slow compared to the floating point stuff done by
    hardware), realize that it's a pure-python implementation and gives
    arbitrary precision.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2010 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Print execution time of some math operations
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import platform
    import timeit
    import time
    import math
    import cmath
if 1:  # Custom imports
    from wrap import dedent

    try:
        import mpmath as mp

        has_mpmath = True
    except ImportError:
        has_mpmath = False
if 1:  # Global variables
    N = int(1e5)  # How many repeats
    Nmp = N // 100  # mpmath stuff takes substantially longer
    assert Nmp >= 10, "N must be >= 1000 (it's %d)" % N
    if len(sys.argv) > 1:
        N = int(float(sys.argv[1]))
    thousands_separator = ","
    m = "from math import "
    c = "from cmath import "
    mp = "from mpmath import mpf, mpc, "
    #
    expressions = {
        "arithmetic": (
            ("Arithmetic", "", "", N),
            ("  Integer addition", "3 + 4", "", N),
            ("  Integer subtraction", "3 - 4", "", N),
            ("  Integer multiplication", "3*4", "", N),
            ("  Integer division", "3//4", "", N),
            ("  Long addition", "30000000000000000 + 40000000000000000", "", N),
            ("  Long subtraction", "30000000000000000 - 40000000000000000", "", N),
            ("  Long multiplication", "30000000000000000*40000000000000000", "", N),
            ("  Long division", "30000000000000000//40000000000000000", "", N),
            ("  Float addition", "3. + 4.", "", N),
            ("  Float subtraction", "3. - 4.", "", N),
            ("  Float multiplication", "3.*4.", "", N),
            ("  Float division", "3./4.", "", N),
            ("  Complex addition", "(1. + 2.j) + (3. + 4.j)", "", N),
            ("  Complex subtraction", "(1. + 2.j) - (3. + 4.j)", "", N),
            ("  Complex multiplication", "(1. + 2.j)*(3. + 4.j)", "", N),
            ("  Complex division", "(1. + 2.j)/(3. + 4.j)", "", N),
        ),
        "real_functions": (
            ("Elementary real functions", "", "", N),
            ("  sin", "sin(1.)", m + "sin", N),
            ("  cos", "cos(1.)", m + "cos", N),
            ("  tan", "tan(1.)", m + "tan", N),
            ("  asin", "asin(1.)", m + "asin", N),
            ("  acos", "acos(1.)", m + "acos", N),
            ("  atan", "atan(1.)", m + "atan", N),
            ("  atan2", "atan2(1., 2.)", m + "atan2", N),
            ("  hypot", "hypot(1., 2.)", m + "hypot", N),
            ("  sinh", "sinh(1.)", m + "sinh", N),
            ("  cosh", "cosh(1.)", m + "cosh", N),
            ("  tanh", "tanh(1.)", m + "tanh", N),
            ("  asinh", "asinh(1.)", m + "asinh", N),
            ("  acosh", "acosh(1.)", m + "acosh", N),
            ("  atanh", "atan(1.)", m + "atan", N),
            ("  fabs", "fabs(-1.2)", m + "fabs", N),
            ("  factorial(10)", "factorial(10)", m + "factorial", N),
            ("  factorial(100)", "factorial(100)", m + "factorial", N // 10),
            ("  floor", "floor(-1.2)", m + "floor", N),
            ("  fmod", "fmod(10.1, 0.2)", m + "fmod", N),
            ("  frexp", "frexp(10.1)", m + "frexp", N),
            ("  ldexp", "ldexp(10.1, 2)", m + "ldexp", N),
            ("  modf", "modf(10.1)", m + "modf", N),
            ("  trunc", "trunc(10.1)", m + "trunc", N),
            ("  exp", "exp(10.1)", m + "exp", N),
            ("  log", "log(10.1)", m + "log", N),
            ("  log1p", "log1p(10.1)", m + "log1p", N),
            ("  log10", "log10(10.1)", m + "log10", N),
            ("  pow", "pow(10.1, 2)", m + "pow", N),
            ("  sqrt", "sqrt(10.1)", m + "sqrt", N),
            ("  degrees", "degrees(10.1)", m + "degrees", N),
            ("  radians", "radians(10.1)", m + "radians", N),
        ),
        "complex_functions": (
            ("Elementary complex functions", "", "", N),
            ("  sin", "sin(1.j)", c + "sin", N),
            ("  cos", "cos(1.j)", c + "cos", N),
            ("  tan", "tan(1.j)", c + "tan", N),
            ("  asin", "asin(1.j)", c + "asin", N),
            ("  acos", "acos(1.j)", c + "acos", N),
            ("  atan", "atan(0.5j)", c + "atan", N),
            ("  atan", "atan(0.5)", c + "atan", N),
            ("  sinh", "sinh(1.j)", c + "sinh", N),
            ("  cosh", "cosh(1.j)", c + "cosh", N),
            ("  tanh", "tanh(1.j)", c + "tanh", N),
            ("  asinh", "asinh(1.j)", c + "asinh", N),
            ("  acosh", "acosh(1.j)", c + "acosh", N),
            ("  atanh", "atan(0.5j)", c + "atan", N),
            ("  exp", "exp(1.j)", c + "exp", N),
            ("  log", "log(1.j)", c + "log", N),
            ("  log10", "log10(1.j)", c + "log10", N),
            ("  sqrt", "sqrt(1.j)", c + "sqrt", N),
            ("  phase", "phase(1.j)", c + "phase", N),
            ("  polar", "polar(1.j)", c + "polar", N),
            ("  rect", "rect(1., 2.)", c + "rect", N),
        ),
        "mpmath_functions": (
            ("mpmath functions (N//%d)" % (N // Nmp), "", "", N),
            ("  sqrt", "sqrt(mpf(1.))", mp + "sqrt", Nmp),
            ("  sqrt", "sqrt(mpc(1.j))", mp + "sqrt", Nmp),
            ("  hypot", "hypot(mpf(1.), mpf(2.))", mp + "hypot", Nmp),
            ("  exp", "exp(mpf(1.))", mp + "exp", Nmp),
            ("  exp", "exp(mpc(1.j))", mp + "exp", Nmp),
            ("  ln", "ln(mpf(11.))", mp + "ln", Nmp),
            ("  ln", "ln(mpc(11.j))", mp + "ln", Nmp),
            ("  log10", "log10(mpf(11.))", mp + "log10", Nmp),
            ("  log10", "log10(mpc(11.j))", mp + "log10", Nmp),
            ("", "", "", Nmp),
            ("  sin", "sin(mpf(1.))", mp + "sin", Nmp),
            ("  sin", "sin(mpc(1.j))", mp + "sin", Nmp),
            ("  cos", "cos(mpf(1.))", mp + "cos", Nmp),
            ("  cos", "cos(mpc(1.j))", mp + "cos", Nmp),
            ("  tan", "tan(mpf(1.))", mp + "tan", Nmp),
            ("  tan", "tan(mpc(1.j))", mp + "tan", Nmp),
            ("  asin", "asin(mpf(1.))", mp + "asin", Nmp),
            ("  asin", "asin(mpc(1.j))", mp + "asin", Nmp),
            ("  acos", "acos(mpf(1.))", mp + "acos", Nmp),
            ("  acos", "acos(mpc(1.j))", mp + "acos", Nmp),
            ("  atan", "atan(mpf(1.))", mp + "atan", Nmp),
            ("  atan", "atan(mpc(1.j))", mp + "atan", Nmp),
            ("  sinh", "sinh(mpf(1.))", mp + "sinh", Nmp),
            ("  sinh", "sinh(mpc(1.j))", mp + "sinh", Nmp),
            ("  cosh", "cosh(mpf(1.))", mp + "cosh", Nmp),
            ("  cosh", "cosh(mpc(1.j))", mp + "cosh", Nmp),
            ("  tanh", "tanh(mpf(1.))", mp + "tanh", Nmp),
            ("  tanh", "tanh(mpc(1.j))", mp + "tanh", Nmp),
            ("  asinh", "asinh(mpf(1.))", mp + "asinh", Nmp),
            ("  asinh", "asinh(mpc(1.j))", mp + "asinh", Nmp),
            ("  acosh", "acosh(mpf(1.))", mp + "acosh", Nmp),
            ("  acosh", "acosh(mpc(1.j))", mp + "acosh", Nmp),
            ("  atanh", "atanh(mpf(1.))", mp + "atanh", Nmp),
            ("  atanh", "atanh(mpc(1.j))", mp + "atanh", Nmp),
            ("  sinc", "sinc(mpf(1.))", mp + "sinc", Nmp),
            ("  sincpi", "sincpi(mpf(1.))", mp + "sincpi", Nmp),
            ("  degrees", "degrees(mpf(1.))", mp + "degrees", Nmp),
            ("  radians", "radians(mpf(1.))", mp + "radians", Nmp),
            ("", "", "", Nmp),
            ("  factorial", "factorial(10)", mp + "factorial", Nmp),
            ("  factorial", "factorial(100)", mp + "factorial", Nmp),
            ("  factorial", "factorial(1000)", mp + "factorial", Nmp),
            ("  factorial", "factorial(100000)", mp + "factorial", Nmp),
            ("  gamma", "gamma(mpf(100))", mp + "gamma", Nmp),
            ("  loggamma", "loggamma(mpf(100))", mp + "loggamma", Nmp),
            ("  beta", "beta(10, 11)", mp + "beta", Nmp),
            ("  harmonic", "harmonic(mpf(10))", mp + "harmonic", Nmp),
            ("  harmonic", "harmonic(mpf(100))", mp + "harmonic", Nmp),
            ("  harmonic", "harmonic(mpc(10j))", mp + "harmonic", Nmp),
            ("  harmonic", "harmonic(mpc(100j))", mp + "harmonic", Nmp),
            ("  incomplete gamma", "gammainc(10, 1, 2)", mp + "gammainc", Nmp),
            ("  incomplete gamma", "gammainc(100, 1, 2)", mp + "gammainc", Nmp),
            ("  exponential integral", "ei(mpf(10))", mp + "ei", Nmp),
            ("  exponential integral", "ei(mpf(100))", mp + "ei", Nmp),
            ("  logarithmic integral", "li(mpf(10))", mp + "li", Nmp),
            ("  logarithmic integral", "li(mpf(100))", mp + "li", Nmp),
            ("  error function", "erf(mpf(10))", mp + "erf", Nmp),
            ("  inverse error function", "erfinv(mpf(0.1))", mp + "erfinv", Nmp),
            ("", "", "", Nmp),
            ("  Bessel function 1", "besselj(10, mpf(2))", mp + "besselj", Nmp),
            ("  Bessel function 2", "bessely(10, mpf(2))", mp + "bessely", Nmp),
            ("  Legendre", "legendre(10, mpf(2))", mp + "legendre", Nmp),
            ("  zeta", "zeta(10)", mp + "zeta", Nmp),
            ("  zeta", "zeta(mpc(10j))", mp + "zeta", Nmp),
        ),
    }


def TwoFig(x):
    """Round x to two significant figures and return it as a string.
    Insert commas if needed.
    """
    s, t = list(str(int(float("%.1e" % x)))), ""
    s.reverse()
    for i, c in enumerate(s):
        if i and i % 3 == 0:
            t += thousands_separator
        t += c
    s = list(t)
    s.reverse()
    return "".join(s)


def P(s, val, size=35):
    fmt = "%%-%ds %%s" % size
    try:
        v = eval(val)
    except Exception:
        return
    print(fmt % (s, v))


def Numbers():
    print("\nNumber information")
    P("  Max int", "sys.maxint")
    P("  Largest negative int", "-sys.maxint - 1")
    print("  Floating point info:")
    P("    Number of digits", "sys.float_info.dig")
    P("    Mantissa digits", "sys.float_info.mant_dig")
    P("    Exponent radix", "sys.float_info.radix")
    P("    Maximum floating point number", "sys.float_info.max")
    P("    Minimum floating point number", "sys.float_info.min")
    P("    Maximum exponent for radix", "sys.float_info.max_exp")
    P("    Maximum exponent for 10", "sys.float_info.max_10_exp")
    P("    Minimum exponent for radix", "sys.float_info.min_exp")
    P("    Minimum exponent for 10", "sys.float_info.min_10_exp")
    P("    (First number > 1) - 1", "sys.float_info.epsilon")
    P("    Addition rounds", "sys.float_info.rounds")


def System():
    print()
    print("System information")
    print("  ", sys.version)
    P("  flags", "sys.flags")
    P("  Platform", "platform.platform()")
    P("  ", "sys.platform")
    P("  Python implementation", "platform.python_implementation()")
    P("  API version", "sys.api_version")
    P("  Java version", "platform.java_ver()")
    P("  Win32 version", "platform.win32_ver()")
    P("  Mac version", "platform.mac_ver()")
    P("  Linux version", "platform.linux_distribution()")
    P("  libc version", "platform.libc_ver()")
    P("  log2(maximum container size)", '"%.2f" % (math.log(sys.maxsize)/math.log(2))')


def RunGroup(group):
    fmt = "%-25s %-42s %9s"
    print()
    for op, expr, setup, n in group:
        if not expr:
            print(op)
            continue
        T = timeit.Timer(expr, setup)
        t = T.timeit(n)
        print(fmt % (op, expr, TwoFig(t / n * 1e9)))


if __name__ == "__main__":
    t = time.time()
    print(
        """          Python performance measures %s
          -----------------------------------------------------
                            log10(N) = %g
                                                                         Time
  Operation               Expression                                     in ns
  ---------------------   -----------------------------------------      ----- """
        % (time.asctime(), math.log10(N))
    )
    RunGroup(expressions["arithmetic"])
    RunGroup(expressions["real_functions"])
    RunGroup(expressions["complex_functions"])
    if has_mpmath:
        RunGroup(expressions["mpmath_functions"])
    Numbers()
    System()
    print("\nTotal time to execute = %.2f s" % (time.time() - t))

# ---------------------------------------------------------------------------
# Results Feb 2011 python 2.6.5     16.2 s
"""
For new PC Jimmy built for me Feb 2011:

          Python performance measures Thu Nov 15 10:44:26 2012
          -----------------------------------------------------
                            log10(N) = 5
                                                                         Time
  Operation               Expression                                     in ns
  ---------------------   -----------------------------------------      -----

Arithmetic
  Integer addition        3 + 4                                             25
  Integer subtraction     3 - 4                                             25
  Integer multiplication  3*4                                               25
  Integer division        3//4                                              26
  Long addition           30000000000000000 + 40000000000000000             25
  Long subtraction        30000000000000000 - 40000000000000000             25
  Long multiplication     30000000000000000*40000000000000000               25
  Long division           30000000000000000//40000000000000000              25
  Float addition          3. + 4.                                           25
  Float subtraction       3. - 4.                                           25
  Float multiplication    3.*4.                                             25
  Float division          3./4.                                             69
  Complex addition        (1. + 2.j) + (3. + 4.j)                           73
  Complex subtraction     (1. + 2.j) - (3. + 4.j)                           74
  Complex multiplication  (1. + 2.j)*(3. + 4.j)                             73
  Complex division        (1. + 2.j)/(3. + 4.j)                            170

Elementary real functions
  sin                     sin(1.)                                          160
  cos                     cos(1.)                                          150
  tan                     tan(1.)                                          170
  asin                    asin(1.)                                         140
  acos                    acos(1.)                                         170
  atan                    atan(1.)                                         170
  atan2                   atan2(1., 2.)                                    320
  hypot                   hypot(1., 2.)                                    520
  sinh                    sinh(1.)                                         300
  cosh                    cosh(1.)                                         300
  tanh                    tanh(1.)                                         300
  asinh                   asinh(1.)                                        230
  acosh                   acosh(1.)                                        160
  atanh                   atan(1.)                                         170
  fabs                    fabs(-1.2)                                       160
  factorial(10)           factorial(10)                                    380
  factorial(100)          factorial(100)                                15,000
  floor                   floor(-1.2)                                      170
  fmod                    fmod(10.1, 0.2)                                  250
  frexp                   frexp(10.1)                                      330
  ldexp                   ldexp(10.1, 2)                                   290
  modf                    modf(10.1)                                       270
  trunc                   trunc(10.1)                                      290
  exp                     exp(10.1)                                        150
  log                     log(10.1)                                        230
  log1p                   log1p(10.1)                                      170
  log10                   log10(10.1)                                      180
  pow                     pow(10.1, 2)                                     300
  sqrt                    sqrt(10.1)                                       130
  degrees                 degrees(10.1)                                     70
  radians                 radians(10.1)                                     69

Elementary complex functions
  sin                     sin(1.j)                                         700
  cos                     cos(1.j)                                         700
  tan                     tan(1.j)                                         710
  asin                    asin(1.j)                                      1,100
  acos                    acos(1.j)                                      1,100
  atan                    atan(0.5j)                                       450
  atan                    atan(0.5)                                        420
  sinh                    sinh(1.j)                                        500
  cosh                    cosh(1.j)                                        500
  tanh                    tanh(1.j)                                        460
  asinh                   asinh(1.j)                                       680
  acosh                   acosh(1.j)                                     1,100
  atanh                   atan(0.5j)                                       450
  exp                     exp(1.j)                                         470
  log                     log(1.j)                                         570
  log10                   log10(1.j)                                       660
  sqrt                    sqrt(1.j)                                        600
  phase                   phase(1.j)                                       290
  polar                   polar(1.j)                                       700
  rect                    rect(1., 2.)                                     380

mpmath functions (N//100)
  sqrt                    sqrt(mpf(1.))                                 18,000
  sqrt                    sqrt(mpc(1.j))                                73,000
  hypot                   hypot(mpf(1.), mpf(2.))                       57,000
  exp                     exp(mpf(1.))                                  37,000
  exp                     exp(mpc(1.j))                                 70,000
  ln                      ln(mpf(11.))                                  33,000
  ln                      ln(mpc(11.j))                                 57,000
  log10                   log10(mpf(11.))                               70,000
  log10                   log10(mpc(11.j))                             100,000

  sin                     sin(mpf(1.))                                  48,000
  sin                     sin(mpc(1.j))                                 76,000
  cos                     cos(mpf(1.))                                  47,000
  cos                     cos(mpc(1.j))                                 77,000
  tan                     tan(mpf(1.))                                  70,000
  tan                     tan(mpc(1.j))                                 85,000
  asin                    asin(mpf(1.))                                 48,000
  asin                    asin(mpc(1.j))                               190,000
  acos                    acos(mpf(1.))                                 31,000
  acos                    acos(mpc(1.j))                               210,000
  atan                    atan(mpf(1.))                                 36,000
  atan                    atan(mpc(1.j))                                60,000
  sinh                    sinh(mpf(1.))                                 62,000
  sinh                    sinh(mpc(1.j))                                94,000
  cosh                    cosh(mpf(1.))                                 62,000
  cosh                    cosh(mpc(1.j))                                95,000
  tanh                    tanh(mpf(1.))                                 69,000
  tanh                    tanh(mpc(1.j))                                87,000
  asinh                   asinh(mpf(1.))                                63,000
  asinh                   asinh(mpc(1.j))                               68,000
  acosh                   acosh(mpf(1.))                                27,000
  acosh                   acosh(mpc(1.j))                              210,000
  atanh                   atanh(mpf(1.))                                18,000
  atanh                   atanh(mpc(1.j))                              140,000
  sinc                    sinc(mpf(1.))                                 74,000
  sincpi                  sincpi(mpf(1.))                               50,000
  degrees                 degrees(mpf(1.))                              37,000
  radians                 radians(mpf(1.))                              32,000

  factorial               factorial(10)                                 13,000
  factorial               factorial(100)                                16,000
  factorial               factorial(1000)                               21,000
  factorial               factorial(100000)                            230,000
  gamma                   gamma(mpf(100))                               18,000
  loggamma                loggamma(mpf(100))                            66,000
  beta                    beta(10, 11)                                  91,000
  harmonic                harmonic(mpf(10))                            100,000
  harmonic                harmonic(mpf(100))                            82,000
  harmonic                harmonic(mpc(10j))                         1,400,000
  harmonic                harmonic(mpc(100j))                          870,000
  incomplete gamma        gammainc(10, 1, 2)                           400,000
  incomplete gamma        gammainc(100, 1, 2)                          340,000
  exponential integral    ei(mpf(10))                                  380,000
  exponential integral    ei(mpf(100))                               1,200,000
  logarithmic integral    li(mpf(10))                                  340,000
  logarithmic integral    li(mpf(100))                                 370,000
  error function          erf(mpf(10))                                   7,900
  inverse error function  erfinv(mpf(0.1))                           1,000,000

  Bessel function 1       besselj(10, mpf(2))                           39,000
  Bessel function 2       bessely(10, mpf(2))                        1,400,000
  Legendre                legendre(10, mpf(2))                         110,000
  zeta                    zeta(10)                                     130,000
  zeta                    zeta(mpc(10j))                             2,700,000

Number information
  Max int                           2147483647
  Largest negative int              -2147483648
  Floating point info:
    Number of digits                15
    Mantissa digits                 53
    Exponent radix                  2
    Maximum floating point number   1.79769313486e+308
    Minimum floating point number   2.22507385851e-308
    Maximum exponent for radix      1024
    Maximum exponent for 10         308
    Minimum exponent for radix      -1021
    Minimum exponent for 10         -307
    (First number > 1) - 1          2.22044604925e-16
    Addition rounds                 1

System information
  2.6.5 (r265:79096, Mar 19 2010, 21:48:26) [MSC v.1500 32 bit (Intel)]
  flags                             sys.flags(debug=0, py3k_warning=0, division_warning=0, division_new=1, inspect=0, interactive=0, optimize=0, dont_write_bytecode=1, no_user_site=0, no_site=0, ignore_environment=0, tabcheck=0, verbose=0, unicode=0, bytes_warning=0)
  Platform                          Windows-XP-5.1.2600-SP3
                                    win32
  Python implementation             CPython
  API version                       1013
  Java version                      ('', '', ('', '', ''), ('', '', ''))
  Win32 version                     ('XP', '5.1.2600', 'SP3', 'Multiprocessor Free')
  Mac version                       ('', ('', '', ''), '')
  Linux version                     ('', '', '')
  libc version                      ('', '')
  log2(maximum container size)      31.00

Total time to execute = 16.17 s
"""
# Results Jul 2021 python 3.7.5     4.8 s
"""
This computer was built around 2016

          Python performance measures Tue Jul 20 21:21:35 2021
          -----------------------------------------------------
                            log10(N) = 5
                                                                         Time
  Operation               Expression                                     in ns
  ---------------------   -----------------------------------------      ----- 

Arithmetic
  Integer addition        3 + 4                                              5
  Integer subtraction     3 - 4                                              5
  Integer multiplication  3*4                                                5
  Integer division        3//4                                               6
  Long addition           30000000000000000 + 40000000000000000              5
  Long subtraction        30000000000000000 - 40000000000000000              6
  Long multiplication     30000000000000000*40000000000000000                6
  Long division           30000000000000000//40000000000000000               5
  Float addition          3. + 4.                                            6
  Float subtraction       3. - 4.                                            5
  Float multiplication    3.*4.                                              5
  Float division          3./4.                                              5
  Complex addition        (1. + 2.j) + (3. + 4.j)                            5
  Complex subtraction     (1. + 2.j) - (3. + 4.j)                            5
  Complex multiplication  (1. + 2.j)*(3. + 4.j)                              6
  Complex division        (1. + 2.j)/(3. + 4.j)                              5

Elementary real functions
  sin                     sin(1.)                                           63
  cos                     cos(1.)                                           59
  tan                     tan(1.)                                           82
  asin                    asin(1.)                                          42
  acos                    acos(1.)                                          40
  atan                    atan(1.)                                          64
  atan2                   atan2(1., 2.)                                    110
  hypot                   hypot(1., 2.)                                    160
  sinh                    sinh(1.)                                          84
  cosh                    cosh(1.)                                          74
  tanh                    tanh(1.)                                          97
  asinh                   asinh(1.)                                        160
  acosh                   acosh(1.)                                         36
  atanh                   atan(1.)                                          65
  fabs                    fabs(-1.2)                                        36
  factorial(10)           factorial(10)                                     43
  factorial(100)          factorial(100)                                 1,600
  floor                   floor(-1.2)                                       89
  fmod                    fmod(10.1, 0.2)                                   78
  frexp                   frexp(10.1)                                      100
  ldexp                   ldexp(10.1, 2)                                    72
  modf                    modf(10.1)                                        99
  trunc                   trunc(10.1)                                       66
  exp                     exp(10.1)                                         50
  log                     log(10.1)                                         93
  log1p                   log1p(10.1)                                       76
  log10                   log10(10.1)                                       64
  pow                     pow(10.1, 2)                                     120
  sqrt                    sqrt(10.1)                                        94
  degrees                 degrees(10.1)                                     45
  radians                 radians(10.1)                                     43

Elementary complex functions
  sin                     sin(1.j)                                         180
  cos                     cos(1.j)                                         180
  tan                     tan(1.j)                                         190
  asin                    asin(1.j)                                        610
  acos                    acos(1.j)                                        620
  atan                    atan(0.5j)                                       160
  atan                    atan(0.5)                                        150
  sinh                    sinh(1.j)                                        140
  cosh                    cosh(1.j)                                        150
  tanh                    tanh(1.j)                                        150
  asinh                   asinh(1.j)                                       220
  acosh                   acosh(1.j)                                       630
  atanh                   atan(0.5j)                                       160
  exp                     exp(1.j)                                         110
  log                     log(1.j)                                         100
  log10                   log10(1.j)                                       110
  sqrt                    sqrt(1.j)                                        170
  phase                   phase(1.j)                                        66
  polar                   polar(1.j)                                       130
  rect                    rect(1., 2.)                                     110

mpmath functions (N//100)
  sqrt                    sqrt(mpf(1.))                                  5,300
  sqrt                    sqrt(mpc(1.j))                                22,000
  hypot                   hypot(mpf(1.), mpf(2.))                       16,000
  exp                     exp(mpf(1.))                                  10,000
  exp                     exp(mpc(1.j))                                 15,000
  ln                      ln(mpf(11.))                                   9,100
  ln                      ln(mpc(11.j))                                 17,000
  log10                   log10(mpf(11.))                               19,000
  log10                   log10(mpc(11.j))                              31,000

  sin                     sin(mpf(1.))                                   9,900
  sin                     sin(mpc(1.j))                                 17,000
  cos                     cos(mpf(1.))                                   9,900
  cos                     cos(mpc(1.j))                                 17,000
  tan                     tan(mpf(1.))                                  13,000
  tan                     tan(mpc(1.j))                                 15,000
  asin                    asin(mpf(1.))                                 13,000
  asin                    asin(mpc(1.j))                                62,000
  acos                    acos(mpf(1.))                                  9,300
  acos                    acos(mpc(1.j))                                67,000
  atan                    atan(mpf(1.))                                  9,300
  atan                    atan(mpc(1.j))                                18,000
  sinh                    sinh(mpf(1.))                                 13,000
  sinh                    sinh(mpc(1.j))                                15,000
  cosh                    cosh(mpf(1.))                                 13,000
  cosh                    cosh(mpc(1.j))                                14,000
  tanh                    tanh(mpf(1.))                                 12,000
  tanh                    tanh(mpc(1.j))                                17,000
  asinh                   asinh(mpf(1.))                                18,000
  asinh                   asinh(mpc(1.j))                               20,000
  acosh                   acosh(mpf(1.))                                 7,800
  acosh                   acosh(mpc(1.j))                               68,000
  atanh                   atanh(mpf(1.))                                 5,300
  atanh                   atanh(mpc(1.j))                               45,000
  sinc                    sinc(mpf(1.))                                 18,000
  sincpi                  sincpi(mpf(1.))                               16,000
  degrees                 degrees(mpf(1.))                              11,000
  radians                 radians(mpf(1.))                               9,300

  factorial               factorial(10)                                  2,200
  factorial               factorial(100)                                 3,000
  factorial               factorial(1000)                               23,000
  factorial               factorial(100000)                             23,000
  gamma                   gamma(mpf(100))                                3,500
  loggamma                loggamma(mpf(100))                             7,600
  beta                    beta(10, 11)                                  25,000
  harmonic                harmonic(mpf(10))                             33,000
  harmonic                harmonic(mpf(100))                            25,000
  harmonic                harmonic(mpc(10j))                           480,000
  harmonic                harmonic(mpc(100j))                          300,000
  incomplete gamma        gammainc(10, 1, 2)                           270,000
  incomplete gamma        gammainc(100, 1, 2)                          360,000
  exponential integral    ei(mpf(10))                                   34,000
  exponential integral    ei(mpf(100))                                  19,000
  logarithmic integral    li(mpf(10))                                   37,000
  logarithmic integral    li(mpf(100))                                  40,000
  error function          erf(mpf(10))                                   3,500
  inverse error function  erfinv(mpf(0.1))                             370,000

  Bessel function 1       besselj(10, mpf(2))                           23,000
  Bessel function 2       bessely(10, mpf(2))                          680,000
  Legendre                legendre(10, mpf(2))                          45,000
  zeta                    zeta(10)                                       3,700
  zeta                    zeta(mpc(10j))                               430,000

Number information
  Floating point info:
    Number of digits                15
    Mantissa digits                 53
    Exponent radix                  2
    Maximum floating point number   1.7976931348623157e+308
    Minimum floating point number   2.2250738585072014e-308
    Maximum exponent for radix      1024
    Maximum exponent for 10         308
    Minimum exponent for radix      -1021
    Minimum exponent for 10         -307
    (First number > 1) - 1          2.220446049250313e-16
    Addition rounds                 1

System information
   3.7.10 (default, May  5 2021, 12:24:16) 
[GCC 10.2.0]
  flags                             sys.flags(debug=0, inspect=0, interactive=0, optimize=0, dont_write_bytecode=1, no_user_site=0, no_site=0, ignore_environment=0, verbose=0, bytes_warning=0, quiet=0, hash_randomization=1, isolated=0, dev_mode=False, utf8_mode=0)
  Platform                          CYGWIN_NT-10.0-17134-WOW64-3.2.0-340.i686-i686-32bit-WindowsPE
                                    cygwin
  Python implementation             CPython
  API version                       1013
  Java version                      ('', '', ('', '', ''), ('', '', ''))
  Win32 version                     ('', '', '', '')
  Mac version                       ('', ('', '', ''), '')
  Linux version                     ('', '', '')
  libc version                      ('', '')
  log2(maximum container size)      31.00

Total time to execute = 4.80 s
"""
# Results Aug 2022 python 3.9.10    4.1 s
"""
          Python performance measures Mon Aug  8 07:25:38 2022
          -----------------------------------------------------
                            log10(N) = 5
                                                                         Time
  Operation               Expression                                     in ns
  ---------------------   -----------------------------------------      ----- 

Arithmetic
  Integer addition        3 + 4                                              5
  Integer subtraction     3 - 4                                              5
  Integer multiplication  3*4                                                5
  Integer division        3//4                                               5
  Long addition           30000000000000000 + 40000000000000000              5
  Long subtraction        30000000000000000 - 40000000000000000              6
  Long multiplication     30000000000000000*40000000000000000                5
  Long division           30000000000000000//40000000000000000               5
  Float addition          3. + 4.                                            5
  Float subtraction       3. - 4.                                            5
  Float multiplication    3.*4.                                              5
  Float division          3./4.                                              5
  Complex addition        (1. + 2.j) + (3. + 4.j)                            5
  Complex subtraction     (1. + 2.j) - (3. + 4.j)                            5
  Complex multiplication  (1. + 2.j)*(3. + 4.j)                              5
  Complex division        (1. + 2.j)/(3. + 4.j)                              5

Elementary real functions
  sin                     sin(1.)                                           44
  cos                     cos(1.)                                           44
  tan                     tan(1.)                                           58
  asin                    asin(1.)                                          38
  acos                    acos(1.)                                          37
  atan                    atan(1.)                                          45
  atan2                   atan2(1., 2.)                                     58
  hypot                   hypot(1., 2.)                                     42
  sinh                    sinh(1.)                                          62
  cosh                    cosh(1.)                                          44
  tanh                    tanh(1.)                                          65
  asinh                   asinh(1.)                                        130
  acosh                   acosh(1.)                                         39
  atanh                   atan(1.)                                          44
  fabs                    fabs(-1.2)                                        35
  factorial(10)           factorial(10)                                     40
  factorial(100)          factorial(100)                                 1,600
  floor                   floor(-1.2)                                       28
  fmod                    fmod(10.1, 0.2)                                   47
  frexp                   frexp(10.1)                                      110
  ldexp                   ldexp(10.1, 2)                                    43
  modf                    modf(10.1)                                       120
  trunc                   trunc(10.1)                                       24
  exp                     exp(10.1)                                         36
  log                     log(10.1)                                         74
  log1p                   log1p(10.1)                                       50
  log10                   log10(10.1)                                       45
  pow                     pow(10.1, 2)                                      69
  sqrt                    sqrt(10.1)                                        96
  degrees                 degrees(10.1)                                     26
  radians                 radians(10.1)                                     27

Elementary complex functions
  sin                     sin(1.j)                                          91
  cos                     cos(1.j)                                          91
  tan                     tan(1.j)                                          96
  asin                    asin(1.j)                                        340
  acos                    acos(1.j)                                        350
  atan                    atan(0.5j)                                        91
  atan                    atan(0.5)                                         88
  sinh                    sinh(1.j)                                         82
  cosh                    cosh(1.j)                                         78
  tanh                    tanh(1.j)                                         85
  asinh                   asinh(1.j)                                        71
  acosh                   acosh(1.j)                                       350
  atanh                   atan(0.5j)                                        91
  exp                     exp(1.j)                                          64
  log                     log(1.j)                                          57
  log10                   log10(1.j)                                        59
  sqrt                    sqrt(1.j)                                         58
  phase                   phase(1.j)                                        40
  polar                   polar(1.j)                                       120
  rect                    rect(1., 2.)                                      58

mpmath functions (N//100)
  sqrt                    sqrt(mpf(1.))                                  4,500
  sqrt                    sqrt(mpc(1.j))                                19,000
  hypot                   hypot(mpf(1.), mpf(2.))                       13,000
  exp                     exp(mpf(1.))                                   9,200
  exp                     exp(mpc(1.j))                                 13,000
  ln                      ln(mpf(11.))                                   7,500
  ln                      ln(mpc(11.j))                                 14,000
  log10                   log10(mpf(11.))                               17,000
  log10                   log10(mpc(11.j))                              27,000

  sin                     sin(mpf(1.))                                   8,200
  sin                     sin(mpc(1.j))                                 15,000
  cos                     cos(mpf(1.))                                   8,000
  cos                     cos(mpc(1.j))                                 15,000
  tan                     tan(mpf(1.))                                  11,000
  tan                     tan(mpc(1.j))                                 14,000
  asin                    asin(mpf(1.))                                 12,000
  asin                    asin(mpc(1.j))                                55,000
  acos                    acos(mpf(1.))                                  7,300
  acos                    acos(mpc(1.j))                                62,000
  atan                    atan(mpf(1.))                                  8,200
  atan                    atan(mpc(1.j))                                15,000
  sinh                    sinh(mpf(1.))                                 12,000
  sinh                    sinh(mpc(1.j))                                11,000
  cosh                    cosh(mpf(1.))                                 12,000
  cosh                    cosh(mpc(1.j))                                12,000
  tanh                    tanh(mpf(1.))                                 11,000
  tanh                    tanh(mpc(1.j))                                14,000
  asinh                   asinh(mpf(1.))                                17,000
  asinh                   asinh(mpc(1.j))                               17,000
  acosh                   acosh(mpf(1.))                                 6,400
  acosh                   acosh(mpc(1.j))                               62,000
  atanh                   atanh(mpf(1.))                                 4,100
  atanh                   atanh(mpc(1.j))                               40,000
  sinc                    sinc(mpf(1.))                                 17,000
  sincpi                  sincpi(mpf(1.))                               14,000
  degrees                 degrees(mpf(1.))                               8,400
  radians                 radians(mpf(1.))                               8,100

  factorial               factorial(10)                                  1,800
  factorial               factorial(100)                                 2,300
  factorial               factorial(1000)                               23,000
  factorial               factorial(100000)                             22,000
  gamma                   gamma(mpf(100))                                2,800
  loggamma                loggamma(mpf(100))                             6,900
  beta                    beta(10, 11)                                  21,000
  harmonic                harmonic(mpf(10))                             31,000
  harmonic                harmonic(mpf(100))                            23,000
  harmonic                harmonic(mpc(10j))                           410,000
  harmonic                harmonic(mpc(100j))                          260,000
  incomplete gamma        gammainc(10, 1, 2)                           260,000
  incomplete gamma        gammainc(100, 1, 2)                          350,000
  exponential integral    ei(mpf(10))                                   33,000
  exponential integral    ei(mpf(100))                                  19,000
  logarithmic integral    li(mpf(10))                                   34,000
  logarithmic integral    li(mpf(100))                                  38,000
  error function          erf(mpf(10))                                   3,100
  inverse error function  erfinv(mpf(0.1))                             330,000

  Bessel function 1       besselj(10, mpf(2))                           20,000
  Bessel function 2       bessely(10, mpf(2))                          570,000
  Legendre                legendre(10, mpf(2))                          41,000
  zeta                    zeta(10)                                       3,200
  zeta                    zeta(mpc(10j))                               450,000

Number information
  Floating point info:
    Number of digits                15
    Mantissa digits                 53
    Exponent radix                  2
    Maximum floating point number   1.7976931348623157e+308
    Minimum floating point number   2.2250738585072014e-308
    Maximum exponent for radix      1024
    Maximum exponent for 10         308
    Minimum exponent for radix      -1021
    Minimum exponent for 10         -307
    (First number > 1) - 1          2.220446049250313e-16
    Addition rounds                 1

System information
   3.9.10 (main, Jan 20 2022, 21:37:52) 
[GCC 11.2.0]
  flags                             sys.flags(debug=0, inspect=0, interactive=0, optimize=0, dont_write_bytecode=0, no_user_site=0, no_site=0, ignore_environment=0, verbose=0, bytes_warning=0, quiet=0, hash_randomization=1, isolated=0, dev_mode=False, utf8_mode=0)
  Platform                          CYGWIN_NT-10.0-17134-3.3.5-341.x86_64-x86_64-64bit-WindowsPE
                                    cygwin
  Python implementation             CPython
  API version                       1013
  Java version                      ('', '', ('', '', ''), ('', '', ''))
  Win32 version                     ('', '', '', '')
  Mac version                       ('', ('', '', ''), '')
  libc version                      ('', '')
  log2(maximum container size)      63.00

Total time to execute = 4.13 s
"""
