import sys
from lwtest import run, raises, assert_equal
from decimal import Decimal
from io import StringIO

from pdb import set_trace as xx
if 1:
    import debug
    debug.SetDebugger()

try:
    import numpy
    have_numpy = True
except ImportError:
    have_numpy = False
try:
    import mpmath
    have_mpmath = True
except ImportError:
    have_mpmath = False

nl = "\n"

def TestRaises():
    f = lambda x: 1/x
    # Function call & object instantiation semantics
    raises(ZeroDivisionError, f, 0)
    try:
        raises(RuntimeError, f, 1)
    except AssertionError:
        pass
    else:
        raise Exception("Bug!")
    class A:
        def __init__(self):
            raise RuntimeError
    raises(RuntimeError, A)
    # Context manager semantics
    with raises(ZeroDivisionError):
        f(0)
    with raises(ZeroDivisionError) as x:
        assert(x is None)
        f(0)
    try:
        with raises(ZeroDivisionError):
            f(1)
    except AssertionError:
        pass
    else:
        raise Exception("Bug!")

def TestAssertEqual():
    '''Demonstrate that the assert_equal function can detect equal and 
    non-equal objects for the following types:
        Numbers
            integers
            floats
            Decimals
            complex
        Sequences of numbers
        Arbitrary objects that can be compared
    '''
    E = AssertionError
    # Numbers
    x = 0.0
    assert_equal(int(x), int(x))
    raises(E, assert_equal, int(x), int(x) + 1)
    assert_equal(x, x)
    raises(E, assert_equal, x, x + 1.0)
    x, y = "0.0", "1.0"
    assert_equal(Decimal(x), Decimal(x))
    raises(E, assert_equal, Decimal(x), Decimal(y))
    x, y = 1+1j, 1+2j
    assert_equal(x, x)
    raises(E, assert_equal, x, x + 1.0)
    if have_mpmath:
        x = mpmath.mpf("1.0")
        assert_equal(x, x)
        raises(E, assert_equal, x, x + 1.0)
    # Sequences of numbers
    x = [1.0, 2.0]
    y = [int(i) for i in x]
    assert_equal(y, y)
    raises(E, assert_equal, y, [i + 1 for i in y])
    assert_equal(x, x)
    raises(E, assert_equal, x, [i + 1 for i in x])
    x = [Decimal("1.0"), Decimal("2.0")]
    assert_equal(x, x)
    raises(E, assert_equal, x, [i + 1 for i in x])
    x = [1+1j, 1+2j]
    assert_equal(x, x)
    raises(E, assert_equal, x, [i + 1 for i in x])
    if have_mpmath:
        x = [mpmath.mpf("1.0"), mpmath.mpf("1.0")]
        assert_equal(x, x)
        raises(E, assert_equal, x, [i + 1 for i in x])
    if have_numpy:
        x = numpy.array([1.0, 1.0])
        assert_equal(x, x)
        raises(E, assert_equal, x, x + 1)
    #-----------------
    # abstol
    x, eps = 1, 1e-15
    assert_equal(x, x + eps, abstol=2*eps)
    raises(E, assert_equal, x, x + eps, abstol=eps)
    # Check things work if one argument is zero
    x, eps = 0, 1e-15
    assert_equal(0, eps, abstol=2*eps)
    assert_equal(eps, 0, abstol=2*eps)
    #-----------------
    # reltol
    x, tol, eps = 1, 0.01, 1e-15
    assert_equal(x, x*(1 + tol - eps), reltol=tol)
    raises(E, assert_equal, x, x*(1 + tol), reltol=tol)
    # reltol & abstol both defined, use_min=True
    assert_equal(x, x*(1 + tol - eps), reltol=tol, abstol=0) # Passes
    raises(E, assert_equal, x, x*(1 + tol - eps), reltol=tol,
                  abstol=0, use_min=True)  # Catches failure
    # Check things work if one argument is zero
    assert_equal(0, 1, reltol=1)
    assert_equal(1, 0, reltol=1)
    # ----- Other objects -----
    # Strings
    x = "a string"
    assert_equal(x, x)
    raises(E, assert_equal, x, x[:-1])
    # Classes and instances
    class A: pass
    class B: pass
    a, b = A(), B()
    assert_equal(a, a)
    assert_equal(A, A)
    raises(E, assert_equal, a, b)
    raises(E, assert_equal, A, B)
    # Functions
    assert_equal(TestRaises, TestRaises)
    raises(E, assert_equal, TestRaises, assert_equal)

def TestRun():
    def TestA(): raise ValueError()
    def TestB(): raise ValueError()
    def testA(): raise ValueError()
    st, d = StringIO(), {"TestA":TestA, "TestB":TestB, "testA":testA}
    # Test halt keyword
    failed, messages = run(d, stream=None, halt=True)
    assert(messages.split(nl)[0] == "TestA failed:  ValueError()")
    # Test that run has two failures
    failed, messages = run(d, stream=None)
    m1, m2 = "TestA failed:", "TestB failed:"
    assert(m1 in messages and m2 in messages)
    # Show regexp change results in only one function being run
    failed, messages = run(d, stream=None, regexp="^TestA$")
    assert(m1 in messages and m2 not in messages)
    # Change to a case sensitive search
    st = StringIO()
    failed, messages = run(d, stream=st, regexp="^testA$", reopts=0)
    s = st.getvalue().strip().split(nl)
    assert(s[0] == "testA failed:  ValueError()")
    assert(m1 not in messages and m2 not in messages)

if __name__ == "__main__":
    exit(run(globals())[0])
