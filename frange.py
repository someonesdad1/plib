'''
Generators that are floating point analogs of range()
    frange(start, stop, step)
        Best to initialize with string representations of floating point
        numbers.  You can control the output type and the implementation
        type, allowing use with a variety of number types.  Example:
            for i in frange("0", "1", "0.1"):
                sys.stdout.write(str(i) + " ")
        results in
            0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
        If start contains a '/' character, impl and return_type
        parameters are set to Rational.
 
    ifrange(start, stop, step)
        Generator that works similarly to frange, but is a simpler
        implementation.  Must be used with 12 or less significant figures.
        Requires roundoff.RoundOff; if not present, the module still works
        but this function won't be available.
 
    lrange(start_decade, stop_decade)
        Useful for producing sequences that can be used for log-log plotting.
        Can also return numpy arrays.  Examples:
            for i in lrange(0, 2):
                sys.stdout.write(str(i) + " ")
        results in
            1 2 3 4 5 6 7 8 9 10 20 30 40 50 60 70 80 90
        and
            for i in lrange(0, 3, mantissas=[1, 2, 5]):
                sys.stdout.write(str(i) + " ")
        results in
            1 2 5 10 20 50 100 200 500
 
    A convenience function Sequence(string) is supplied that will return
    a list from the specifications in the string.  Example:
        Sequence('1:1.5:0.1   5:1:-1  1/4:3/4:1/8')
    returns
        [1, 1.1, 1.2, 1.3, 1.4, 1.5,
        5, 4, 3, 2, 1,
        1/4, 3/8, 1/2, 5/8, 3/4]
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2010, 2015 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <programming> Generators that are floating point analogs of
    # range().  Also provides a utility function that can produce
    # arithmetic sequences of integers, floating point numbers, and
    # fractions.
    #∞what∞#
    #∞test∞# --test #∞test∞#
    pass
if 1:   # Imports
    import re
    import sys
    import itertools
    from decimal import Decimal
    from numbers import Integral
    from fractions import Fraction
    from pdb import set_trace as xx
if 1:   # Custom imports
    try:
        from roundoff import RoundOff
        has_RoundOff = True
    except ImportError:
        has_RoundOff = False
    try:
        numpy_available = True
        import numpy
    except ImportError:
        numpy_available = False
if 1:   # Global variables
    __all__ = "frange ifrange lrange Rational Sequence".split()
    # Regular expression to split strings on whitespace
    split_ws = re.compile(r"\s+")
class Rational(Fraction):
    '''The Rational class is a fractions.Fraction object except that
    it has a conventional proper fraction string representation.
    '''
    def __str__(self):
        n, d = abs(self.numerator), abs(self.denominator)
        s = ["-"] if self.numerator*self.denominator < 0 else [""]
        if d == 1:
            s.append(str(n))
        else:
            ip, remainder = divmod(n, d)
            if ip:
                s.extend([str(ip), "-"])
            s.extend([str(remainder), "/", str(d)])
        return ''.join(s)
def frange(start, stop=None, step=None, return_type=float, impl=Decimal,
           strict=True, include_end=False):
    '''A floating point generator analog of range.  start, stop, and step
    are either python floats, integers, or strings representing floating
    point numbers (or any other object that impl can convert to an object
    that behaves with numerical semantics).  The iterates returned will be
    of type return_type, which should be a function that converts the impl
    type to the desired type.  impl defines the numerical type to use for
    the implementation.  strict is used to define whether we should try to
    convert an impl object to a string before converting it to a
    return_type.  If strict is True, this is not allowed.  If strict is
    False, the conversion will be tried.  Setting strict to False may allow
    some number types to work with other number types, however, the burden
    is on the user to determine if frange still behaves as expected.
 
    If include_end is True, then the step is added to the stop number.
    This allows you to get e.g. an inclusive list of integers.  However,
    for floating point values, you may get a number one step beyond the
    stopping point.  Examples:
 
        frange("1", "3", "0.9") returns 1.0, 1.9, 2.8
 
    but
 
        frange("1", "3", "0.9" include_end=True) returns
        1.0 1.9 2.8 3.7
 
    Python's Decimal class is used for the default implementation, but you
    can choose it to be e.g. floats if you wish (however, you'll then have
    the typical naive implementation seen all over the web).  Consult
    http://www.python.org/dev/peps/pep-0327/ and the decimal module's
    documentation to learn more about why a float implementation is naive.
 
    To help ensure you get the output you want, use strings for start, stop
    and step.  This is the "proper" way to initialize Decimals with
    non-integer values.  start, stop, and step can be python floating point
    numbers if you wish, but you may not get the sequence you expect.  For
    an example, compare the output of frange(9.6001, 9.601, 0.0001) and
    frange("9.6001", "9.601", "0.0001").  Most users will probably expect
    the output from the second form, which excludes the stop value like
    range does.
 
    Examples of use (also look at the unit tests):
        a = list(frange("0.125", "1", ".125"))
    results in a being
        [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
 
    Alternatively, you can use rational numbers in frange (need python 2.6
    or later) because they have the proper numerical semantics.  A
    convenience class called Rational is provided in this module because it
    allows fractions to be printed in their customary proper form.
         R = Rational
         b = list(frange("1/8", "1", "1/8", impl=R, return_type=R))
    results in b being
         [1/8, 1/4, 3/8, 1/2, 5/8, 3/4, 7/8]
    and we also have a == b is True.
 
    The happy accident of a == b being True is only because these decimal
    fractions can be represented exactly in binary floating point.  This is
    not true in general:
        c = list(frange("0.1", "1", "0.1"))
        d = list(frange("1/10", "1", "1/10", impl=R, return_type=R))
    results in c == d being False.
 
    Print out c to see why c and d are not equal (this is practically the
    canonical example of the problems with binary floating point for us
    humans that love decimal arithmetic).
 
    A convenience is that if '/' is in the string for start, all the
    numbers are interpreted as Rational objects.
    '''
    def ceil(x):
        i = int(abs(x))
        if x > i:
            i += 1
        return (-1 if x < 0 else 1)*i
    if isinstance(start, str) and "/" in start:
        impl = return_type = Rational
    init = lambda x: (impl(repr(x)) if isinstance(x, float) else impl(x))
    start = init(start)
    if stop is not None:
        stop = init(stop)
    else:
        start, stop = impl(0), start
    step = impl(1) if step is None else init(step)
    if include_end:
        stop += step
    if not step and start < stop:
        while True:
            try:
                yield return_type(start)
            except TypeError:
                if strict:
                    raise
                yield return_type(str(start))
    else:
        for i in range(ceil((stop - start)/step)):
            try:
                yield return_type(start)
            except TypeError:
                if strict:
                    raise
                yield return_type(str(start))
            start += step
def lrange(start_decade, end_decade, dx=1, x=1, mantissas=None,
           use_numpy=False):
    '''Provides a logarithmic analog to the frange function.  Returns a
    list of values with logarithmic spacing (if use_numpy is True, will
    return a numpy array).
 
    Example:  lrange(0, 2, mantissas=[1, 2, 5]) returns
    [1, 2, 5, 10, 20, 50].
    '''
    msg = "%s must be an integer"
    if not isinstance(start_decade, Integral):
        raise ValueError(msg % "start_decade")
    if not isinstance(end_decade, Integral):
        raise ValueError(msg % "end_decade")
    msg = "%s must lie in [1, 10)"
    if not (1 <= dx < 10):
        raise ValueError(msg % "dx")
    if not (1 <= x < 10):
        raise ValueError(msg % "x")
    if mantissas is None:
        mantissas = []
        while x < 10:
            mantissas.append(x)
            x += dx
    values = []
    for exp in range(start_decade, end_decade):
        values += [i*10**exp for i in mantissas]
    if use_numpy and numpy_available:
        return numpy.array(values)
    return values
def Sequence(s):
    '''Return a sequence of numbers based on the specifications in s.
    Specifications are separated by whitespace characters and are of the
    forms
        a
        a:b
        a:b:c
    where a is the starting number and b is the ending number.  The
    increment is 1 unless c is given.  Unlike python's range function,
    the endpoint is included in the sequence.
 
    Example:  Sequence('1:1.5:0.1   5:1:-1  1/4:3/4:1/8') returns
        [1, 1.1, 1.2, 1.3, 1.4, 1.5,
         5, 4, 3, 2, 1,
         1/4, 3/8, 1/2, 5/8, 3/4]
    '''
    out = []
    for spec in split_ws.split(s):
        spec = spec.strip()
        if not spec:
            continue
        c = "1"
        f = spec.split(":")
        if len(f) == 1:
            a = f[0]
            b = a
        elif len(f) == 2:
            a, b = f
        elif len(f) == 3:
            a, b, c = f
        else:
            msg = "'{}' is a bad sequence specification"
            raise ValueError(msg.format(spec))
        out += list(frange(a, b, c, include_end=True))
    def MakeIntIfPossible(x):
        i = int(x)
        if i == x:
            return i
        return x
    return [MakeIntIfPossible(i) for i in out]
def ifrange(start, stop, step=1):
    '''Provides an iterator similar to frange but with a simpler
    implementation.  Use with integers, floats, and Rationals.  You
    should rely on no more than 12 significant figures in the returned
    numbers.
    '''
    if not has_RoundOff:
        raise RuntimeError("roundoff module not available")
    for i in itertools.count(start, step):
        x = RoundOff(i)
        if x >= stop:
            return
        yield x
if __name__ == "__main__": 
    if 1:   # Imports
        from decimal import Decimal
        from fractions import Fraction
        from pdb import set_trace as xx
        import getopt
        import os
        import pathlib
        import sys
    if 1:   # Custom modules
        from wrap import dedent
        from lwtest import run, raises, assert_equal, Assert
        import color as C
    if 1:   # Global variables
        d = {}      # Options dictionary
        P = pathlib.Path
        yel, norm = C.fg(C.yellow, s=1), C.normal(s=1)
    if 1:   # Module's base code
        def Error(msg, status=1):
            print(msg, file=sys.stderr)
            exit(status)
        def Usage(d, status=1):
            name = sys.argv[0]
            print(dedent(f'''
            Usage:  {name} [options] etc.
              Explanations...
             
            Options:
              --test      Run internal self tests
            '''))
            exit(status)
        def ParseCommandLine(d):
            d["--test"] = False         # Run self tests
            try:
                opts, args = getopt.getopt(sys.argv[1:], "h", 
                    "test".split())
            except getopt.GetoptError as e:
                print(str(e))
                exit(1)
            for o, a in opts:
                if o in ("-h", "--help"):
                    Usage(d, status=0)
                elif o == "--test":
                    d["--test"] = True
            #if not args:
            #    Usage(d)
            return args
    if 1:   # Test code 
        if 1:   # Global variables
            n, N = 10, 100000  # "Large" numbers
            s = ("9.6001 9.6002 9.6003 9.6004 9.6005 "
                "9.6006 9.6007 9.6008 9.6009")
            eps = 1./10**sys.float_info.dig
        def Test_Normal_one_parameter():
            got = list(frange(str(n)))
            expected = [float(i) for i in range(n)]
            assert(got == expected)
        def Test_Normal_one_parameter_Decimals():
            got = list(frange(str(n), return_type=Decimal))
            expected = [Decimal(i) for i in range(n)]
            assert(got == expected)
        def Test_Normal_two_parameters():
            got = list(frange(str(n//2), str(n)))
            expected = [float(i) for i in range(n//2, n)]
            assert(got == expected)
        def Test_Normal_two_parameters_Decimals():
            got = list(frange(str(n//2), str(n), return_type=Decimal))
            expected = [Decimal(i) for i in range(n//2, n)]
            assert(got == expected)
        def Test_Normal_three_parameters():
            got = list(frange("9.6001", "9.601", "0.0001"))
            expected = [float(i) for i in s.split()]
            assert(got == expected)
        def Test_Normal_three_parameters_Decimals():
            got = list(frange("9.6001", "9.601", "0.0001", return_type=Decimal))
            expected = [Decimal(i) for i in s.split()]
            assert(got == expected)
        def Test_Counting_down():
            got = list(frange(str(n), "0", "-1"))
            expected = [float(i) for i in range(n, 0, -1)]
            assert(got == expected)
        def Test_Numbers_outside_float_range():
            s = "e-28000"
            got = list(frange("1"+s, "4"+s, "1"+s, return_type=Decimal))
            expected = [Decimal('1E-28000'), Decimal('2E-28000'), 
                        Decimal('3E-28000')]
            assert(got == expected)
            s = "e28000"
            got = list(frange("1"+s, "4"+s, "1"+s, return_type=Decimal))
            expected = [Decimal('1E28000'), Decimal('2E28000'), 
                        Decimal('3E28000')]
            assert(got == expected)
        def Test_Sequence_of_complex_numbers():
            got = list(complex(0, i) for i in frange(str(n)))
            expected = [complex(0, i) for i in range(n)]
            assert(got == expected)
        def Test_mpmath():
            try:
                from mpmath import mpf, mpc, mp, arange
            except ImportError:
                print(f"{yel}{__file__}:  Warning:  mpmath not tested{norm}",
                    file=sys.stderr)
            else:
                # Plain floating point
                got = list(frange(str(n), return_type=lambda x: mpf(str(x))))
                expected = [mpf(i) for i in range(n)]
                assert(got == expected)
                # Use mpf for implementation and return type
                got = list(frange(str(n), return_type=mpf, impl=mpf))
                expected = [mpf(i) for i in range(n)]
                assert(got == expected)
                # mpmath's complex numbers 
                got = list(frange(str(n), return_type=lambda x: mpc(0, str(x))))
                expected = [mpc(0, i) for i in range(n)]
                assert(got == expected)
                # One would expect mpmath to work as well as Decimal in the
                # following call:
                #   frange("9.6001", "9.601", "0.0001", return_type=mpf, impl=mpf)
                # I found that it doesn't work for the default 15 decimals
                # places (it generates 10 numbers instead of 9, just like using
                # impl=float).  However, changing to >= 16 decimal places lets
                # the code work the same as Decimal.  Note:  I'm using an older
                # version (0.12) of mpmath (0.16 is the current version as this
                # is written), so this might work with a newer version.
                mp.dps = 16
                got = list(frange("9.6001", "9.601", "0.0001", return_type=mpf, 
                                impl=mpf))
                expected = [mpf(i) for i in s.split()]
                assert(got == expected)
        def Test_numpy():
            try:
                import numpy
            except ImportError:
                print(f"{yel}{__file__}:  Warning:  numpy not tested{norm}",
                    file=sys.stderr)
            else:
                # Things work OK for the following case
                got = numpy.array(list(frange(str(n))))
                expected = numpy.arange(0, n, float(1))
                assert(list(got) == list(expected))
                # However, the following test case won't work with the default
                # frange implementation using Decimal numbers; the Decimal
                # implementation will return 9 numbers, but both numpy and
                # frange(impl=float) will return 10 numbers.  This is the
                # "hazard" of computing with floats and their roundoff
                # problems.  But we get things to "work" (i.e., frange
                # duplicates the output of numpy's arange) by using impl=float.
                start, stop, step = 9.6001, 9.601, 0.0001
                got = frange(start, stop, step, impl=float)
                expected = numpy.arange(start, stop, step)
                assert(list(got) == list(expected))
        def Test_fractions():
            # The following test case shows that frange can be used with a
            # rational number class to return a sequence of rational numbers by
            # using rational arithmetic.  This won't work with versions of
            # python earlier than 2.6.
            try:
                from fractions import Fraction as Rat
            except ImportError:
                print("\nfractions not tested\n", file=sys.stderr)
            else:
                got = list(frange("1/3", "5", "1/3", return_type=Rat, impl=Rat))
                # Note that because we're using floats, we have to avoid using
                # 5 to ensure that we get the same number of elements as in
                # got.  Again, this kind of thing is problematic with the
                # quantization errors of binary floating point arithmetic.
                start, stop, inc = 1/float(3), 5 - eps, 1/float(3)
                expected = list(frange(start, stop, inc, return_type=float, 
                                    impl=float))
                assert(len(got) == len(expected))
                # There are small differences between the numbers; we use 
                # eps to detect failures. 
                for i, j in zip(got, expected):
                    assert(abs(i - j) <= eps)
        def Test_include_end():
            # Test with integers
            res = list(frange("1", "3", return_type=int))
            assert(res == [1, 2])
            res = list(frange("1", "3", return_type=int, include_end=True))
            assert(res == [1, 2, 3])
            # Test with floats
            res = list(frange("1", "3", "0.9"))
            assert(res == [1.0, 1.9, 2.8])
            res = list(frange("1", "3", "0.9", include_end=True))
            assert(res == [1.0, 1.9, 2.8, 3.7])
        def Test_doctest_examples():
            # Basic frange tests
            got = list(frange("0", "1", "0.1"))
            expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
            assert(got == expected)
            #
            got = list(frange("0.125", "1", ".125"))
            expected = [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
            assert(got == expected)
            #
            R = Rational
            got = list(frange("1/8", "1", "1/8", impl=R, return_type=R))
            expected = [Fraction(i) for i in "1/8 1/4 3/8 1/2 5/8 3/4 7/8".split()]
            assert(got == expected)
            # Note integers can be coerced to fractions
            got = list(frange(0, 1, "1/8", impl=R, return_type=R))
            expected = [Fraction(i) for i in 
                "0 1/8 1/4 3/8 1/2 5/8 3/4 7/8".split()]
            assert(got == expected)
            # lrange tests
            got = lrange(0, 1)
            expected = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            assert(got == expected)
            #
            got = list(lrange(0, 2))
            expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 
                70, 80, 90]
            assert(got == expected)
            #
            got = list(lrange(0, 3, mantissas=[1, 2, 5]))
            expected = [1, 2, 5, 10, 20, 50, 100, 200, 500]
            assert(got == expected)
            #
            got = lrange(0, 2, dx=2)
            expected = [1, 3, 5, 7, 9, 10, 30, 50, 70, 90]
            assert(got == expected)
        def Test_Rational():
            R = Rational
            got = [i for i in frange("1", "4", ".6", impl=R, return_type=R)]
            expected = [R(1, 1), R(8, 5), R(11, 5), R(14, 5), R(17, 5)]
            assert(got == expected)
        def Test_ifrange():
            # Basic tests
            got = list(ifrange(0, 1, 0.1))
            expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
            assert(got == expected)
            #
            got = list(ifrange(0.125, 1, 0.125))
            expected = [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
            assert(got == expected)
            #
            R = Rational
            got = list(ifrange(R(1, 8), 1, R(1, 8)))
            expected = [Fraction(i) for i in "1/8 1/4 3/8 1/2 5/8 3/4 7/8".split()]
            assert(got == expected)
            # Note integers can be coerced to fractions
            got = list(ifrange(0, 1, R(1, 8)))
            expected = [Fraction(i) for i in 
                "0 1/8 1/4 3/8 1/2 5/8 3/4 7/8".split()]
            assert(got == expected)
    if 1:   # Example code 
        def Sixteenths():
            print(dedent(f'''
            Example of frange:  printing sixteenths:
            for i in frange("1/16", 2, 1/16):
                print(f"  {{i!s:10s}} {{i!r}}")
            
            '''))
            for i in frange("1/16", 2, 1/16):
                print(f"  {i!s:10s} {i!r}")
    args = ParseCommandLine(d)
    if d["--test"]:
        exit(run(globals(), regexp=r"Test_", halt=1)[0])
    else:
        Sixteenths()
