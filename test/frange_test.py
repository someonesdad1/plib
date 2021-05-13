# Unit tests for testing the frange function
import sys
from frange import frange, Rational, lrange, ifrange
from decimal import Decimal
from fractions import Fraction
from lwtest import run
from pdb import set_trace as xx 

n, N = 10, 100000  # "Large" numbers
s = ("9.6001 9.6002 9.6003 9.6004 9.6005 "
     "9.6006 9.6007 9.6008 9.6009")
eps = 1./10**sys.float_info.dig


def test_Normal_one_parameter():
    got = list(frange(str(n)))
    expected = [float(i) for i in range(n)]
    assert(got == expected)

def test_Normal_one_parameter_Decimals():
    got = list(frange(str(n), return_type=Decimal))
    expected = [Decimal(i) for i in range(n)]
    assert(got == expected)

def test_Normal_two_parameters():
    got = list(frange(str(n//2), str(n)))
    expected = [float(i) for i in range(n//2, n)]
    assert(got == expected)

def test_Normal_two_parameters_Decimals():
    got = list(frange(str(n//2), str(n), return_type=Decimal))
    expected = [Decimal(i) for i in range(n//2, n)]
    assert(got == expected)

def test_Normal_three_parameters():
    got = list(frange("9.6001", "9.601", "0.0001"))
    expected = [float(i) for i in s.split()]
    assert(got == expected)

def test_Normal_three_parameters_Decimals():
    got = list(frange("9.6001", "9.601", "0.0001", return_type=Decimal))
    expected = [Decimal(i) for i in s.split()]
    assert(got == expected)

def test_Counting_down():
    got = list(frange(str(n), "0", "-1"))
    expected = [float(i) for i in range(n, 0, -1)]
    assert(got == expected)

def test_Numbers_outside_float_range():
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

def test_Sequence_of_complex_numbers():
    got = list(complex(0, i) for i in frange(str(n)))
    expected = [complex(0, i) for i in range(n)]
    assert(got == expected)

def test_mpmath():
    try:
        from mpmath import mpf, mpc, mp, arange
    except ImportError:
        print("{}:  Warning:  mpmath not tested".format(__file__),
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

def test_numpy():
    try:
        import numpy
    except ImportError:
        print("{}:  Warning:  numpy not tested".format(__file__),
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

def test_fractions():
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

def test_include_end():
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

def test_doctest_examples():
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

def test_Rational():
    R = Rational
    got = [i for i in frange("1", "4", ".6", impl=R, return_type=R)]
    expected = [R(1, 1), R(8, 5), R(11, 5), R(14, 5), R(17, 5)]
    assert(got == expected)

def test_ifrange():
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

if __name__ == "__main__":
    exit(run(globals())[0])
