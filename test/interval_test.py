import sys
from lwtest import run, raises, assert_equal
from decimal import Decimal
from interval import have_uncertainties, Interval, Rng, inf, Eps, U
from interval import have_datetime, datetime, have_mpmath, oo, Range
from interval import Partition, Indeterminate
import sys

from pdb import set_trace as xx
if 0:
    import debug
    debug.SetDebugger()

def TestRange():
    # One parameter
    a, stop = [], 5
    for i in Range(inf):
        if i >= stop:
            break
        a.append(i)
    assert(a == list(range(stop)))
    # Two parameters
    a = []
    for i in Range(0, inf):
        if i >= stop:
            break
        a.append(i)
    assert(a == list(range(stop)))
    # Three parameters
    a = []
    for i in Range(0, inf, 1):
        if i >= stop:
            break
        a.append(i)
    assert(a == list(range(stop)))
    # Test using -inf
    a, start, stop, inc = [], 0, 10, -1
    result = [-i for i in range(stop)]
    for i in Range(0, -inf, -1):
        if i <= -stop:
            break
        a.append(i)
    assert(a == result)
 
def TestBasicIntervals():
    # Show you can have an empty Interval
    i = Interval()
    # Construct a reasonably complex Interval object and verify the
    # 'in' operator works as expected.
    eps = 1e-14
    i = Interval(
        1, 2, 2.3,      # "Points"
        (3, 4),         # Convenience:  2-sequences map to closed ranges
    )
    i.add(Rng(5, 7.2, ropen=True))      # Add half-open interval
    i.add(Rng(88, inf, lopen=True))     # Add half-open semi-infinite interval
    for j in (1, 2, 2.3, 3, 3 + eps, 4, 4 - eps, 5, 5 + eps, 7.2 - eps,
              88*(1 + eps), 1e308):
        assert(j in i)
    for j in (0, 1 - eps, 1 + eps, 7.2, 88):
        assert(j not in i)
    # Show deletion works
    i.remove(Rng(3, 4))
    assert(3 not in i)
    # Show Rng's open keyword is equivalent to using lopen and ropen
    a, b = 0, 5
    r1 = Rng(a, b, open=True)
    r2 = Rng(a, b, lopen=True, ropen=True)
    assert(r1 == r2)
    # Show an Interval created with numerous copies of the same Rng object
    # is equivalent to one of the Rng objects.
    a, b = 0, 1
    items = [Rng(a, b)]*10
    i = Interval(*items)
    assert(len(i.ranges) == 1)
    r = i.ranges[0]
    assert(a == r.a and b == r.b)
 
def TestInInterval():
    eps = 1e-15
    i = Interval(1, 2, Rng(5, 7.2, ropen=True), Rng(88, inf))
    i.add(Rng(12, 14, lopen=True, ropen=True, integer=True))
    i.add(-42)
    for j in (-42, 1, 2, 5, 5 + eps, 7.2 - eps, 13, 88, 1e308,
              inf - eps, inf - 1e308, inf):
        assert(j in i)
    eps = 1e-14
    for j in (-inf, -43, -42 - eps, -42 + eps, -41, 7.2, 12, 14,
              13 + eps, 88 - eps):
        assert(j not in i)
    # Real line except 0
    i = Interval(Rng(-inf, 0, ropen=True), Rng(0, inf, lopen=True))
    assert(-eps in i)
    assert(eps in i)
    assert(0 not in i)
    assert(0.0 not in i)
 
def TestIntervalExpand():
    # This also tests Rng.expand()
    if not have_uncertainties:
        return
    s, eps, a, b, k = 0.01, 1e-14, 1, 2, 2
    u1, u2 = U.ufloat(a, s), U.ufloat(b, s)
    R = Rng(u1, u2)
    I = Interval(R.copy())
    for r in (R, I):
        assert(a in r)
        assert(a + eps in r)
        assert(a - eps not in r)
        assert(b in r)
        assert(b - eps in r)
        assert(b + eps not in r)
    # Check Rng's expand()
    R.expand(k)
    assert(a - k*s in R)
    assert(b + k*s in R)
    # Check Interval's expand()
    I.expand(k)
    assert(a - k*s in I)
    assert(b + k*s in I)
    r = I.ranges[0]
    assert(isinstance(r.a, float))
    assert(isinstance(r.b, float))
 
def TestEps():
    o, e = 1, 0.01
    for E in (Eps(o, releps=e), Eps(o, eps=e)):
        assert(E.a == o - e and E.b == o + e)
        assert(o - 2*e not in E)
        assert(o - e in E)
        assert(o in E)
        assert(o + e in E)
        assert(o + 2*e not in E)
        assert(E in E)
        assert(E == E)
    # Equality comparison with number
    eps = 1e-15
    for e in (Eps(1, eps=1), Eps(1, releps=1)):
        assert(0 - eps != e)
        assert(0 - eps not in e)
        assert(2 + eps != e)
        assert(2 + eps not in e)
        for i in (0, 0.01, 0.5, 0.99, 1, 1.01, 1.5, 1.99, 2):
            assert(i in e)
            assert(i in e)
    # Using an uncertainties.ufloat
    if have_uncertainties:
        x = U.ufloat(1, 1)
        e = Eps(x, k=1)
        assert(e.a == 0 and e.b == 2)
        e = Eps(x, k=2)
        assert(e.a == -1 and e.b == 3)
    # Make an open epsilon ball
    e = Eps(2, eps=1, open=True)
    a, b, eps = 1, 3, 1e-15
    assert(a not in e)
    assert(a + eps in e)
    assert(b - eps in e)
    assert(b not in e)
 
def TestRngInit():
    raises(ValueError, Rng)
    raises(ValueError, Rng, 1)
    raises(ValueError, Rng, 1, 2, 3)
    raises(ValueError, Rng, (1,))
    raises(ValueError, Rng, (1, 2, 3))
    # Can use equal values if neither end is open
    Rng(1, 1)
    Rng(1, 1.0)
    Rng(1.0, 1.0)
    Rng("a", "a")
    raises(ValueError, Rng, 1, 1, lopen=True)
    raises(ValueError, Rng, 1, 1, ropen=True)
    raises(ValueError, Rng, 1, 1, lopen=True, ropen=True)
    # Can't use float with integer keyword
    raises(ValueError, Rng, (1.1, 2), integer=True)
    # Can't use complex numbers
    raises(TypeError, Rng, (1.1+3j, 2-7j))
    if have_mpmath:  # mp.mpc is mpmath's complex number type
        c1, c2 = mp.mpc(3, -4), mp.mpc(-88, -88)
        raises(TypeError, Rng, (c1, c2))
    # Integer initialization
    r = Rng(1, 2)
    assert(r.a == 1 and r.b == 2 and not r.int)
    r = Rng(1, 2, integer=True)
    assert(r.a == 1 and r.b == 2 and r.int)
    # Floats
    r = Rng(1.1, 2.2)
    assert(r.a == 1.1 and r.b == 2.2 and not r.int)
    # Decimal
    r = Rng(Decimal("1.1"), Decimal("2.2"))
    # mpmath mpf objects
    if have_mpmath:
        r = Rng(mp.mpf("1.1"), mp.mpf("2.2"))
    if have_datetime:
        # timedelta objects
        t1 = datetime.timedelta(hours=5)
        t2 = datetime.timedelta(hours=6)
        r = Rng(t1, t2)
        r = Rng(t2, t1)
        r = Rng(t1, t2, lopen=True)
        r = Rng(t1, t2, ropen=True)
        r = Rng(t1, t2, lopen=True, ropen=True)
        # Date objects
        d1, d2 = datetime.date(2013, 8, 1), datetime.date(2013, 10, 16)
        r = Rng(d1, d2)
    # Can use strings because they support the proper ordering semantics.
    r = Rng("a", "b")
    r = Rng("a", "b", lopen=True)
    r = Rng("a", "b", ropen=True)
    r = Rng("a", "b", lopen=True, ropen=True)
 
def TestRngAddition():
    r1, r2 = Rng(1, 2), Rng(2, 3)
    for r in (r1 + r2, r1 | r2):
        assert(r.a == 1 and r.b == 3)
    r1, r2 = Rng(1, 2), Rng(1, 3)
    for r in (r1 + r2, r1 | r2):
        assert(r.a == 1 and r.b == 3)
    # Half-open on the left
    r1, r2 = Rng(1, 2, lopen=True), Rng(1, 3)
    for r in (r1 + r2, r1 | r2):
        assert(r.a == 1 and r.b == 3 and not r.lopen and not r.ropen)
    # Both half-open on the left
    r1, r2 = Rng(1, 2, lopen=True), Rng(1, 3, lopen=True)
    for r in (r1 + r2, r1 | r2):
        assert(r.a == 1 and r.b == 3 and r.lopen and not r.ropen)
    # Half-open on the right
    r1, r2 = Rng(1, 2, ropen=True), Rng(1, 3)
    for r in (r1 + r2, r1 | r2):
        assert(r.a == 1 and r.b == 3 and not r.lopen and not r.ropen)
    # Both half-open on the right
    r1, r2 = Rng(1, 2, ropen=True), Rng(1, 3, ropen=True)
    for r in (r1 + r2, r1 | r2):
        assert(r.a == 1 and r.b == 3 and not r.lopen and r.ropen)
    # No overlap
    r1, r2 = Rng(1, 2), Rng(3, 4)
    i = Interval(r1, r2)
    assert(r1 + r2 == i)
    # Integer intervals
    r1, r2 = Rng(1, 5, integer=True), Rng(2, 6, integer=True)
    assert(r1 + r2 == Rng(1, 6, integer=True))
    assert(r1 | r2 == Rng(1, 6, integer=True))
    # Rng union with Interval works
    r, i = Rng(1, 3), Interval((2, 4), (5, 6))
    assert(r + i == Interval((1, 4), (5, 6)))
    assert(i + r == Interval((1, 4), (5, 6)))
    assert(r | i == Interval((1, 4), (5, 6)))
    assert(i | r == Interval((1, 4), (5, 6)))
 
def TestRngMultiplication():
    # Closed
    r1, r2 = Rng(1, 2), Rng(2, 3)
    for r in (r1*r2, r1 & r2):
        assert(r == Rng(2, 2))
    r1, r2 = Rng(1, 2), Rng(1, 3)
    for r in (r1*r2, r1 & r2):
        assert(r.a == 1 and r.b == 2)
    # Half-open on the left
    r1, r2 = Rng(1, 2, lopen=True), Rng(1, 3)
    for r in (r1*r2, r1 & r2):
        assert(r.a == 1 and r.b == 2 and r.lopen and not r.ropen)
    # Half-open on the right
    r1, r2 = Rng(1, 2, ropen=True), Rng(1, 3)
    for r in (r1*r2, r1 & r2):
        assert(r.a == 1 and r.b == 2 and r.ropen and not r.lopen)
    # Both open
    r1, r2 = Rng(1, 2, lopen=True, ropen=True), Rng(1, 3)
    for r in (r1*r2, r1 & r2):
        assert(r.a == 1 and r.b == 2 and r.lopen and r.lopen)
    # No overlap
    r1, r2 = Rng(1, 2), Rng(3, 4)
    for r in (r1*r2, r1 & r2):
        assert(r is None)
    # Integer intervals
    r1, r2 = Rng(1, 5, integer=True), Rng(2, 6, integer=True)
    for r in (r1*r2, r1 & r2):
        assert(r == Rng(2, 5, integer=True))
    # Can intersect with an Interval object
    r, i = Rng(1, 3), Interval((2, 4), (5, 6))
    assert(r*i == Interval((2, 3)))
    assert(i*r == Interval((2, 3)))
    assert(r & i == Interval((2, 3)))
    assert(i & r == Interval((2, 3)))
 
def TestRngOrdering():
    r1, r2 = Rng(1, 3), Rng(2, 3)
    assert(r1 < r2)
    assert(r1 <= r2)
    assert(r2 > r1)
    assert(r2 >= r1)
    assert(not r1 > r2)
    assert(not r1 >= r2)
    assert(r1 != r2)
    r1, r2 = Rng(1, 3), Rng(1, 3)
    assert(r1 == r2)
    assert(not r1 > r2)
    assert(r1 >= r2)
    assert(not r2 < r1)
    assert(r2 >= r1)
 
def TestIntervalAdd():
    # Check Interval.add()
    # Single point
    i = Interval()
    i.add(0)
    assert(i == Interval(0))
    # Multiple points
    i = Interval()
    i.add(0, 1)
    assert(i == Interval(0, 1))
    # Single range via sequence
    i = Interval()
    i.add((1, 2))
    assert(i == Interval(Rng(1, 2)))
    # Single range via Rng
    i = Interval()
    i.add(Rng(1, 2))
    assert(i == Interval(Rng(1, 2)))
    # Single range via Interval
    i = Interval()
    i.add(Interval((1, 2)))
    assert(i == Interval(Rng(1, 2)))
    # Multiple ranges via sequence
    i = Interval()
    i.add((1, 2), (3, 4))
    assert(i == Interval(Rng(1, 2), Rng(3, 4)))
    # Multiple ranges via Rng
    i = Interval()
    i.add(Rng(1, 2), Rng(3, 4))
    assert(i == Interval(Rng(1, 2), Rng(3, 4)))
    # Multiple ranges via Interval
    i = Interval()
    i.add(Interval((1, 2), (3, 4)))
    assert(i == Interval(Rng(1, 2), Rng(3, 4)))
    # Adding ranges and points from another Interval
    i = Interval(0, 1, (10, 11), (13, 14))
    j = Interval(2, 3, (15, 16), (17, 18))
    i.add(j)
    assert(i == Interval(0, 1, 2, 3,
                         Rng(10, 11),
                         Rng(13, 14),
                         Rng(15, 16),
                         Rng(17, 18)
                         ))
    # Same, but Rng objects should coalesce into one
    i = Interval(0, 1, (10, 11), (12, 13))
    j = Interval(2, 3, (11, 12), (13, 14))
    i.add(j)
    assert(i == Interval(0, 1, 2, 3, Rng(10, 14)))
def TestIntervalRemove():
    empty = Interval()
    # Check Interval.remove()
    # Single point
    i = Interval(0)
    i.remove(0)
    assert(i == empty)
    # Multiple points, no Rng objects
    i = Interval(0, 1, 2)
    i.remove(1, 2)
    assert(i == Interval(0))
    # Multiple points with Rng object
    i = Interval(0, 1, 2, (4, 5))
    i.remove(1, 2)
    assert(i == Interval(0, (4, 5)))
    # Single range via sequence
    i = Interval((1, 2))
    i.remove((1, 2))
    assert(i == empty)
    # Single range via Rng
    i = Interval((1, 2))
    i.remove(Rng(1, 2))
    assert(i == empty)
    # Single range via Interval
    i = Interval((1, 2))
    i.remove(Interval((1, 2)))
    assert(i == empty)
    # Multiple ranges via sequence
    i = Interval(0, (1, 2), (3, 4), (5, 6))
    i.remove((1, 2), (3, 4))
    assert(i == Interval(0, Rng(5, 6)))
    # Multiple ranges via Rng
    i = Interval(0, (1, 2), (3, 4), (5, 6))
    i.remove(Rng(1, 2), Rng(3, 4))
    assert(i == Interval(0, Rng(5, 6)))
    # Multiple ranges via Interval
    i = Interval(0, (1, 2), (3, 4), (5, 6))
    i.remove(Interval((1, 2), (3, 4)))
    assert(i == Interval(0, Rng(5, 6)))

def TestIntervalAddition():
    # Empty intervals
    assert(Interval() + Interval() == Interval())
    assert(Interval() | Interval() == Interval())
    # Intervals with points only
    assert(Interval(1) + Interval(2) == Interval(1, 2))
    assert(Interval(1) | Interval(2) == Interval(1, 2))
    # Intervals with only Rng objects
    i1, i2 = Interval((1, 2)), Interval((3, 4))
    assert(i1 + i2 == Interval((1, 2), (3, 4)))
    assert(i1 | i2 == Interval((1, 2), (3, 4)))
    i1, i2 = Interval((1, 2)), Interval((1, 2))
    assert(i1 + i2 == Interval((1, 2)))
    assert(i1 | i2 == Interval((1, 2)))
    i1, i2 = Interval((1, 2)), Interval((2, 4))
    assert(i1 + i2 == Interval((1, 4)))
    assert(i1 | i2 == Interval((1, 4)))
    # Intervals with points and Rng objects
    i1, i2 = Interval(5, (1, 2)), Interval(6, (3, 4))
    assert(i1 + i2 == Interval((1, 2), (3, 4), 5, 6))
    assert(i1 | i2 == Interval((1, 2), (3, 4), 5, 6))
    # Empty intervals return an empty Interval
    i1, i2 = Interval(), Interval()
    assert(i1 + i2 == Interval())
    assert(i1 | i2 == Interval())
    # Contiguous open range won't coalesce but will collapse
    i1, i2 = Interval(Rng(1, 2, ropen=True)), Interval((2, 4))
    i, r = i1 + i2, Interval((1, 4))
    assert(i != r)
    i.collapse()
    assert(i == r)
 
def TestIntervalMultiplication():
    # Empty intervals
    assert(Interval()*Interval() == Interval())
    assert(Interval()*Interval(1) == Interval())
    assert(Interval() & Interval() == Interval())
    assert(Interval() & Interval(1) == Interval())
    # Intervals with points only
    assert(Interval(1)*Interval(2) == Interval())
    assert(Interval(1, 2)*Interval(1) == Interval(1))
    assert(Interval(1) & Interval(2) == Interval())
    assert(Interval(1, 2) & Interval(1) == Interval(1))
    # Intervals with only Rng objects
    i1, i2 = Interval((1, 2)), Interval((1.5, 2))
    assert(i1*i2 == Interval((1.5, 2)))
    assert(i1 & i2 == Interval((1.5, 2)))
    i1, i2 = Interval((1, 2)), Interval((1, 2))
    assert(i1*i2 == Interval((1, 2)))
    assert(i1 & i2 == Interval((1, 2)))
    i1, i2 = Interval((1, 2)), Interval((2, 4))
    assert(i1*i2 == Interval(2))
    assert(i1 & i2 == Interval(2))
    # Intervals with points and Rng objects
    i1, i2 = Interval(5, (1, 2)), Interval(5, 6, (2, 4))
    assert(i1*i2 == Interval(2, 5))
    assert(i1 & i2 == Interval(2, 5))
 
def TestIn():
    # Floats
    a, eps = 2.5, 1e-15
    for r in (Rng(0, a), Rng(a, 0)):
        assert(0 in r)
        assert(0 + eps in r)
        assert(1 in r)
        assert(a in r)
        assert(a - eps in r)
    r = Rng(0, 2, lopen=True, ropen=True)
    assert(0 not in r)
    assert(0 + eps in r)
    assert(2 not in r)
    assert(2 - eps in r)
    # Integers
    a = 5
    r = Rng(0, a, integer=True)
    for i in range(a + 1):
        assert(i in r)
        assert(i + eps not in r)
        assert(i - eps not in r)
    r = Rng(0, 2, integer=True, lopen=True, ropen=True)
    assert(0 not in r)
    assert(1 in r)
    assert(2 not in r)
 
def TestInClosedInterval():
    l, r = False, False
    R = (
        Rng(1, 3, lopen=l, ropen=r),
        Rng(1.0, 3, lopen=l, ropen=r),
        Rng(1, 3.0, lopen=l, ropen=r),
        Rng(1.0, 3.0, lopen=l, ropen=r),
        Rng(Decimal(1), 3, lopen=l, ropen=r),
        Rng(1, Decimal(3), lopen=l, ropen=r),
        Rng(Decimal(1), Decimal(3), lopen=l, ropen=r),
    )
    for r in R:
        assert(1 in r)
        assert(1.0 in r)
        assert(Decimal(1) in r)
        assert(Decimal("1.0") in r)
        assert(2 in r)
        assert(2.5 in r)
        assert(3 in r)
        assert(Decimal(3) in r)
        assert(3.0 in r)
        assert(Decimal("3.0") in r)
 
def TestInHalfOpenIntervalOnLeft():
    l, r = True, False
    R = (
        Rng(1, 3, lopen=l, ropen=r),
        Rng(1.0, 3, lopen=l, ropen=r),
        Rng(1, 3.0, lopen=l, ropen=r),
        Rng(1.0, 3.0, lopen=l, ropen=r),
        Rng(Decimal(1), 3, lopen=l, ropen=r),
        Rng(1, Decimal(3), lopen=l, ropen=r),
        Rng(Decimal(1), Decimal(3), lopen=l, ropen=r),
    )
    for r in R:
        assert(1 not in r)
        assert(1.0 not in r)
        assert(Decimal(1) not in r)
        assert(Decimal("1.0") not in r)
        assert(2 in r)
        assert(2.5 in r)
        assert(3 in r)
        assert(Decimal(3) in r)
        assert(3.0 in r)
        assert(Decimal("3.0") in r)
 
def TestInHalfOpenIntervalOnRight():
    l, r = False, True
    R = (
        Rng(1, 3, lopen=l, ropen=r),
        Rng(1.0, 3, lopen=l, ropen=r),
        Rng(1, 3.0, lopen=l, ropen=r),
        Rng(1.0, 3.0, lopen=l, ropen=r),
        Rng(Decimal(1), 3, lopen=l, ropen=r),
        Rng(1, Decimal(3), lopen=l, ropen=r),
        Rng(Decimal(1), Decimal(3), lopen=l, ropen=r),
    )
    for r in R:
        assert(1 in r)
        assert(1.0 in r)
        assert(Decimal(1) in r)
        assert(Decimal("1.0") in r)
        assert(2 in r)
        assert(2.5 in r)
        assert(3 not in r)
        assert(Decimal(3) not in r)
        assert(3.0 not in r)
        assert(Decimal("3.0") not in r)
 
def TestInOpenInterval():
    l, r = True, True
    R = (
        Rng(1, 3, lopen=l, ropen=r),
        Rng(1.0, 3, lopen=l, ropen=r),
        Rng(1, 3.0, lopen=l, ropen=r),
        Rng(1.0, 3.0, lopen=l, ropen=r),
        Rng(Decimal(1), 3, lopen=l, ropen=r),
        Rng(1, Decimal(3), lopen=l, ropen=r),
        Rng(Decimal(1), Decimal(3), lopen=l, ropen=r),
    )
    for r in R:
        assert(1 not in r)
        assert(1.0 not in r)
        assert(Decimal(1) not in r)
        assert(Decimal("1.0") not in r)
        assert(2 in r)
        assert(2.5 in r)
        assert(3 not in r)
        assert(Decimal(3) not in r)
        assert(3.0 not in r)
        assert(Decimal("3.0") not in r)
 
def TestInInfiniteIntervals():
    r = Rng(0, inf, lopen=True, ropen=True)
    assert(0 not in r)
    assert(inf in r)
    assert(1.2345678e308 in r)
    assert(Decimal("1e50000") in r)
    assert(-inf not in r)
    r = Rng(-inf, 0, lopen=True, ropen=True)
    assert(-inf in r)
    assert(-1.2345678e308 in r)
    assert(Decimal("-1e50000") in r)
    assert(inf not in r)
    r = Rng(-inf, inf, lopen=True, ropen=True)
    assert(-inf in r)
    assert(-1.2345678e308 in r)
    assert(Decimal("-1e50000") in r)
    assert(0 in r)
    assert(1.2345678e308 in r)
    assert(Decimal("1e50000") in r)
    assert(inf in r)
 
def TestInWithMpmath():
    if have_mpmath:
        r = Rng(0, inf, lopen=True, ropen=True)
        assert(mp.mpf("0") not in r)
        assert(mp.mpf("1e-50000") in r)
        assert(mp.mpf("1e50000") in r)
        # A rather large number, but still finite:
        assert(10**mp.mpf("1e100") in r)
 
def TestInWithASCII():
    r = Rng("a", "z")
    for i in range(128):
        if ord("a") <= i <= ord("z"):
            assert(chr(i) in r)
        else:
            assert(chr(i) not in r)
    r = Rng("a", "z", lopen=True)
    assert("a" not in r)
    assert("b" in r)
    r = Rng("a", "z", ropen=True)
    assert("y" in r)
    assert("z" not in r)
 
def TestInWithUnicode():
    low, high = 1000, 2000
    a, b = 1200, 1700
    r = Rng(chr(a), chr(b))
    for i in range(low, high + 1):
        if a <= i <= b:
            assert(chr(i) in r)
        else:
            assert(chr(i) not in r)
 
def TestInWithWordStrings():
    r = Rng("goodbye", "hello")
    assert("greet" in r)
    assert("gimlet" not in r)
    assert("h" in r)
    assert("hellacious" in r)
    assert("help" not in r)
 
def TestInWithDateObjects():
    if have_datetime:
        d1, d2 = datetime.date(2013, 8, 1), datetime.date(2013, 10, 16)
        r, yr = Rng(d1, d2), 2013
        assert(datetime.date(yr, 7, 31) not in r)
        assert(datetime.date(yr, 8, 1) in r)
        assert(datetime.date(yr, 8, 2) in r)
        assert(datetime.date(yr, 10, 15) in r)
        assert(datetime.date(yr, 10, 16) in r)
        assert(datetime.date(yr, 10, 17) not in r)
        yr = 2012
        assert(datetime.date(yr, 7, 31) not in r)
        assert(datetime.date(yr, 8, 1) not in r)
        assert(datetime.date(yr, 8, 2) not in r)
        assert(datetime.date(yr, 10, 15) not in r)
        assert(datetime.date(yr, 10, 16) not in r)
        assert(datetime.date(yr, 10, 17) not in r)
 
def TestInfinity():
    # Basic ordering
    M = sys.float_info.max  # Largest float
    for x in (-1e308, -10, -1.0, 0, 1.0, 10, 1e308, M):
        assert(x < inf)
        assert(x <= inf)
        assert(x > -inf)
        assert(x >= -inf)
        assert(x != inf)
        assert(x != -inf)
    # Check with mpmath numbers
    if have_mpmath:
        for i in ("-1e308", "-10", "-1.0", "0", "1.0", "10", "1e308"):
            x = mp.mpf(i)
            assert(x < inf)
            assert(x <= inf)
            assert(x > -inf)
            assert(x >= -inf)
            assert(x != inf)
            assert(x != -inf)
    # Check with Decimal numbers
    for i in ("-1e308", "-10", "-1.0", "0", "1.0", "10", "1e308"):
        x = Decimal(i)
        assert(x < inf)
        assert(x <= inf)
        assert(x > -inf)
        assert(x >= -inf)
        assert(x != inf)
        assert(x != -inf)
    # Order with respect to self
    assert(inf == inf)
    assert(+inf == inf)
    assert(-inf == -inf)
    assert(-inf < inf)
    assert(-inf <= inf)
    assert(inf > -inf)
    assert(inf >= -inf)
    # Addition
    assert(1 + inf + 1 == inf)
    assert(inf + inf == inf)
    assert(1 + -inf + 1 == -inf)
    # Subtraction
    assert(1 - inf - 1 == -inf)
    assert(-inf - inf == -inf)
    assert(-inf - 1 == -inf)
    assert(1 - inf == -inf)
    # Multiplication
    assert(inf*1 == inf)
    assert(inf*1.0 == inf)
    assert(inf*inf == inf)
    assert(-inf*-inf == inf)
    assert(-inf*(-inf) == inf)
    assert(-inf*inf == -inf)
    # Division
    for i in (1, 1.0, 0):
        assert(inf/i == inf)
        assert(inf//i == inf)
    # Indeterminate operations
    for f in (
            lambda: -inf + inf,
            lambda: inf - inf,
            lambda: inf*0,
            lambda: inf*0.0,
            lambda: -inf*0,
            lambda: -inf*0.0,
            lambda: inf/inf,
            lambda: -inf/inf,
            lambda: -inf/-inf):
        raises(Indeterminate, f)
    # Absolute value
    assert(abs(inf) == inf)
    assert(abs(-inf) == inf)
    # Can put into dictionary
    d = {inf: None, -inf: None}
    # Can convert to a float infinity
    assert(float(inf) == float("inf"))
    assert(float(-inf) == float("-inf"))
    # String representation
    assert(str(inf) == "∞")
    assert(str(-inf) == "-∞")
    # Can compare to dates and strings
    dt = datetime.datetime(2014, 1, 1) if have_datetime else "a"
    for d in (dt, "a"):
        assert(d != inf)
        assert(d < inf)
        assert(d <= inf)
        assert(d > -inf)
        assert(d >= -inf)
        assert(d != -inf)
    # Test utility function
    assert(inf.is_infinite(inf))
    assert(inf.is_infinite(-inf))
    assert(not inf.is_infinite(1))
    assert(not inf.is_infinite(-1))
 
def TestPartition():
    s = [inf, 0, -oo, 1, oo, -inf]
    # Show both constructor calls work.  Results in the interval
    # [-oo, 0, 1, oo].
    p = Partition(*s)
    p = Partition(s)
    # Results in Partition(Ranges = Rng<[-oo, 0)>, Rng<[0, 1)>, Rng<[1, oo]>)
    assert(p(-1) == 0)
    assert(p[p(-1)] == Rng((-inf, 0), ropen=True))
    assert(p(0) == 1)
    assert(p(1) == 2)
    # Partition with left end open
    p = Partition(s, lopen=True)
    assert(p(-1) == 0)
    assert(p[p(-1)] == Rng((-inf, 0), lopen=True))
    # Show class invariant hasn't changed.
    a, b = 0, 10
    for p in (Partition(range(a, b + 1), lopen=False),
              Partition(range(a, b + 1), lopen=True)):
        i = p.collapse()
        # Check that this Interval object is equal to the original range
        assert(len(i.ranges) == 1 and Rng(a, b) == i.ranges[0])
    # Union or intersection not allowed
    p1, p2 = Partition(0, 1, 2), Partition(1, 2, 3)
    f = lambda: p1 + p2
    g = lambda: p1*p2
    raises(SyntaxError, f)
    raises(SyntaxError, g)
 
def IntervalPerformance():
    '''Construct a large Interval object containing n Rng objects.
    Time and print out the performance to both search and insert new
    Rng objects.
 
    The first measurements were the total time and showed that things
    were dominated by random number generation and building lists.  The
    second set of measurements used the code below and only measured
    the time to do lookups in an Interval object.
                                          1e5 lookups
        log10(len(Interval.ranges))      Lookup time, s
                    3                           1.9
                    4                           2.5
                    5                           2.8
    Thus, lookups appear to be fast enough for typical applications.
    Construction of large Interval objects can be time consuming,
    perhaps justifying the need for the plist library (see the
    documentation).
    '''
    from time import time
    from random import uniform, randint
    size, a = int(10**5), 10**6
    d = []
    for i in range(size):
        b = -a + 2*i
        d.append((b, b + 1))
    I = Interval(*d)
    # Number of lookups
    n = 10**5
    # Generate a sequence of random numbers to search for
    d = [uniform(0, a) for i in range(n)]
    # Now do lookups
    start = time()
    for num in d:
        num in I
    print("Time in s = %.2f" % (time() - start))
    print("size of Interval = %d" % len(I.ranges))
    print("Number of lookups = %d" % n)
    exit()
 
if __name__ == "__main__":
    exit(run(globals(), halt=0)[0])
