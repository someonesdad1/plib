'''

----------------------------------------------------------------------
Update Sun 20 Dec 2020 06:05:23 PM

It appears sympy covers most of the things I envisioned for an interval
library.  See https://docs.sympy.org/latest/modules/sets.html.

Something I don't like about sympy is that it's big and takes time to
import.  For example, for python 3.7.10, I get 3.8 s to import it when
it isn't cached and 1.5 s when it is.  It only takes about 0.2 s to
import this module.

----------------------------------------------------------------------
Udate Thu 07 Nov 2019 08:32:30 AM

Let
    ℝ = set of real numbers
    ℤ = set of integers = {..., -1, 0, 1, 2, ...}
    ℕ = set of natural numbers = {1, 2, ...}
    ℕ𝟘 = set of natural numbers with zero = {0, 1, 2, ...}
    ℚ = set of rational numbers
    ℕ ⊂ ℕ𝟘 ⊂ ℤ ⊂ ℚ ⊂ ℝ
    ⅀ = arbitrary set of scalars

I think it would make sense to continue work on this module, as the PyPi
libraries I've downloaded on intervals (Page's and a successor) are for
python 2 and interval3 wouldn't pass its self tests.

I think an Interval object ought to be derived from a set, letting it
contain arbitrary heterogeneous objects.  The core need is to be able to
test 'x in Interval' where x is an arbitrary object.  The implementation
would use the underlying set, but include a special container for Rng
objects; this container needs to stay in sorted order for binary
searches when 'in' is used.  The Rng objects define a discrete or
continuous range of scalars.  If you include arbitrary Rng scalars with
e.g. floating point Rng, then the scalars must be orderable with respect
to floats.

Rng objects would need to represent a range of a scalar; the only
property of a scalar needed is that scalars a and b must have the 
relation a < b decidable (i.e., the scalars are orderable).

Start with a document that shows the key use cases and provides examples
of how it typically would be used.  The overriding goal is that it
simulate a set of continuous and discrete intervals and points for
defining a group of scalars.  The primary difference from a regular
python set is that if it contains one or more continuous intervals, it
cannot be iterated over; but of course this is reasonable, as it's an
infinite set.  A property Interval.is_iterable will keep track of this,
which will be False if any continuous Rng object is present or any Rng
object has a boundary point of Infinity.  (In reality, python reals can
be iterated over as they are a finite set.)

It would be interesting to see how well certain mathematical sets could
be modeled.  For example, see if the real line with the integers removed
could be modeled.  This is easy to visualize and describe (ℝ - ℤ).  This
is an interesting use case and it may be possible to do by providing
built-in abstractions of such things.  In fact, they could be encoded
with Unicode characters in the familiar of ℝ ℤ ℕ ℚ, as they are allowed
python symbols.

These mathematical sets are easy to describe in code.  For example, ℝ
could be a class whose constructor is ℝ(float, int, Decimal, Fraction,
mpf).  Then x in ℝ would be gotten with

    def __init__(self, *types):
        self.types = types
    def ℝ.__contains__(self, x)
        return any([isinstance(x, i) for i in self.types])

Another way to describe ℝ is Rng(-inf, inf), at least for floats.  To
describe ℝ - ℤ, you'd want to use Rng(-inf, inf) and NRng(-inf, inf,
integer=True) where NRng is an object which means something must not be
in that set.  Or the arithmetic operator must be able to handle an
expression like 'Rng(-inf, inf) - Rng(-inf, inf, integer=True)'.

ℚ is the set of rationals and would be defined by x in Rng(-inf, inf)
and isinstance(x, Fraction).  Note fractions are ordered with respect to
floats and integers, so they work well together.  To support this, the
Rng object could use a keyword 'type'.

Note the general Rng object wouldn't need a type.  Then the only
requirement on Rng(a, b) is that type(a) == type(b) and a and b are
orderable.
        
Use case examples:
    
    - You want a set that contains 

----------------------------------------------------------------------

Note:  I stopped work on this module because someone pointed out that PyPi
had an interval library (see /pylib/other_libs/interval-1.0.0.tar by Jacob
Page).  Unfortunately, this library only runs under python 2.7; when I
convert the docstring test print() statements to python 3 form, the tests
fail.

Page's library is under the LGPL, so it might be worth deriving a new 
library that works under both python 2.7 and 3.6.  I'd want to make sure
that his stuff works with any objects that are orderable (his examples make
me think it does).

Should his core class be derived from a set?  This would allow boolean
operations with regular heterogeneous sets.  This would allow use cases
such as a set that x = set(("cat", "dog", IntervalSet(1, 5))).  Then a
test such as "3.5 in x" would return True.  This models the generality of
sets that one would encounter in practice.  However, it might not be too
efficient, as the "in" operator would be an O(n) operation.  Note his basic
architecture uses a list as the basic container.  More objectionable is
that mathematical sets are not orderable, whereas an IntervalSet is.

----------------------------------------------------------------------

Module to provide discrete and continuous intervals and containers of
these intervals.  This module will probably work with python 2.1 or
later (it has been tested with python 2.7.6 and 3.4.0).
 
Most usage will involve numerical points and intervals, so I will often
use the term 'numbers', but the objects defining things only need to be
orderable, so I will call them scalars to connote this ordering.
 
    Example:  you could mix astronomical Julian day objects that were
    represented internally by an mpmath floating point number with
    python's integers and floats as long as you defined the proper
    comparison semantics for the Julian day object with integers and
    floats.
 
Typical use case:  a problem requires input numbers that are restricted
to the integers between 1 and 10 or any floating point numbers between
11 and 15.5.  You'd construct an Interval object that described that
requirement by
 
    interval = Interval(Rng(1, 10, integer=True), (11, 15.5))
 
Given a number x, you would test whether x is in the interval by
whether 'x in interval' or 'x == interval' are True.  Since Rng and
Interval objects model sets of mathematical objects, both objects
support unions and intersections.
 
The module's public symbols are:
 
Interval (class)
    Container of Rng objects and scalars.  The most common use case is
    with numerical objects such as integers, floats, and Decimal numbers,
    but other scalars can be used such as strings or date objects (see
    unit tests for examples).
Rng (class)
    Class that simulates a single discrete or continuous range (i.e.,
    interval) where either end can be open or closed.  Requires
    initialization with two scalars defining the endpoints of the
    range.  The scalars can be different types as long as they can be
    ordered with respect to each other (example:  integers and floats).
    The integer keyword for the constructor allows creating discrete
    ranges.
Eps (class, derived from Rng)
    Convenience class that simulates a continuous numerical range
    specified by a center point and half-width (an "epsilon ball").
    The half-width can be given by either a relative or absolute number
    or it can be derived from a standardized uncertainty with a stated
    coverage factor.
Partition (class, derived from Interval)
    This is a convenience container that holds a partition of a portion
    or all of the real line.  The Partition's Rng objects, when unioned
    together, will result in the original interval.  Call a partition
    object p as a function p(x) and it will return the index of the Rng
    object that contains the scalar x or None if x is not in the
    partition.
Infinity (class)
    Class that emulates the behavior of infinity by comparing larger
    than any other object except itself.  Also supports the four basic
    arithmetic operations and should compare properly with nearly any
    orderable object type.  The is_infinite() method lets you test
    whether an object is infinite.
inf (instance of Infinity class)
    Convenience instance.  Allows construction of semi-infinite
    intervals.  Example:  Interval((0, inf)) constructs an interval
    that models real numbers >= zero.
Range (function)
    Convenience function that replaces python's built-in range().
    Range(inf) works as you'd expect.
 
See interval.odt or interval.pdf for documentation.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <programming> Emulates mathematical intervals.  Warning:  this is
    # uncompleted code and shouldn't be used for production work.
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Imports
    import bisect
    import datetime
    import sys
    from decimal import Decimal
    from pdb import set_trace as xx
if 1:  # Custom imports
    try:
        import mpmath as mp
        have_mpmath = True
    except ImportError:
        have_mpmath = False
    try:
        import uncertainties as U
        have_uncertainties = True
    except ImportError:
        have_uncertainties = False
if 1:  # Global variables
    __all__ = [
        "Eps",
        "inf",
        "Indeterminate",
        "Infinity",
        "Interval",
        "Partition",
        "Range",
        "Rng",
    ]
    # Controls whether binary search is used in the membership algorithms.
    use_binary_search = True
class Indeterminate(ValueError):
    pass
class Infinity(object):
    ''' Provide an object that compares to things like infinity does.
    It can also be used with datetime and string objects and can have
    objects arithmetically added and subtracted from it.  Note you
    can do simple arithmetic operations too.
 
    The basic properties of infinity are
        x + inf = inf if x != -inf
        x*inf = +inf if x > 0
        x*inf = -inf if x < 0
        x/inf = 0 if x != inf and x != -inf
 
    If you want a more full-featured infinity object, see Konsta
    Vesterinen's https://pypi.python.org/pypi/infinity/1.4.
 
    As I was writing more and more tests for Infinity objects, the
    class' methods started to look more like Vesterinen's above.  I
    remember thinking when I first saw his implementation "Jeez, I
    don't need all those methods for what I'm going to do".  Each
    method gets added when you see a test case fail that, of course,
    should obviously work, so you find yourself just adding one more
    method.
    '''
    def __init__(self, negative=False):
        self.neg = bool(negative)
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.neg == other.neg
        return False
    def __lt__(self, other):
        return self.neg
    def __gt__(self, other):
        return not self.neg
    def __ge__(self, other):
        return self > other or self == other
    def __le__(self, other):
        return self < other or self == other
    def __abs__(self):
        return self.__class__(negative=False)
    def __neg__(self):
        return self.__class__(negative=not self.neg)
    def __sub__(self, other):
        inf = self.__class__(negative=False)
        if ((self.neg and other == -inf) or
                (not self.neg and other == inf)):
            raise Indeterminate
        return self
    def __rsub__(self, other):
        return -self + other
    def __add__(self, other):
        inf = self.__class__(negative=False)
        if ((self.neg and other == inf) or
                (not self.neg and other == -inf)):
            raise Indeterminate
        return self
    def __radd__(self, other):
        return self + other
    def __mul__(self, other):
        if not other:
            raise Indeterminate
        if (self < 0 and other > 0) or (self > 0 and other < 0):
            return -abs(self)
        return abs(self)
    def __rmul__(self, other):
        return self*other
    def __pos__(self):
        return self
    def __div__(self, other):
        if self.is_infinite(other):
            raise Indeterminate
        return self
    def __rdiv__(self, other):
        if self.is_infinite(other):
            raise Indeterminate
        return 0 if other else self
    __truediv__ = __floordiv__ = __div__
    __rtruediv__ = __rfloordiv__ = __rdiv__
    def __float__(self):
        # Note:  this may not work on some platforms
        return float("-inf") if self.neg else float("inf")
    def __hash__(self):
        # Note hash(float("inf")) returns 314159; I've chosen to use
        # 314159265, the largest such integer less than 2**31.
        c = 314159265
        return -c if self.neg else c
    def timetuple(self):
        '''Matches methods in datetime.date and datetime.datetime
        classes to allow them to be compared to dates.
        '''
        return tuple()
    def __repr__(self):
        return "-∞" if self.neg else "∞"
    def is_infinite(self, x):
        return x in (self, -self)
if 1:  # Convenience instance of infinity
    oo = inf = Infinity() # Convenience instance
class Rng(object):
    ''' Holds two orderable objects that define a range (I'll also call
    it an interval).  If the constructor's integer keyword is True,
    then the range is discrete and it contains integers; otherwise, it
    is continuous.
 
    The primary uses of Rng objects are:
 
        * Allow testing to see if an object is in the range.
        * Combine two Rng objects into one via addition and
          multiplication, operations analogous to the union and
          intersection of sets, respectively.  Note that the union of
          two disjoint Rng objects can return an Interval object.
          The intersection of two Rng objects can return a Rng object
          with the left endpoint equal to the right (i.e., a scalar).
        * Define an ordering for Rng objects so a container (class
          Interval, below) of them can be sorted, facilitating binary
          searches for membership.  The container allows complicated
          discrete and continuous ranges to be modeled.
 
    The objects used in the constructor do not need to be numbers; the
    only requirement is that they must be orderable amongst themselves.
    Thus, for example, a range can be defined by a pair of strings:
    Rng("a", "z") defines a range that contains the lower case ASCII
    letters (but not all of them; for example, 'zymurgy' won't be
    within this range).  I anticipate that the major use case for Rng
    objects will be with integer and floating point numbers.
 
    Despite the implementation of two "arithmetic" operations (addition
    and multiplication) and the nomenclature, note that Rng objects are
    not intended to model interval arithmetic (see Knuth volume 2 or
    http://en.wikipedia.org/wiki/Interval_arithmetic for more details).
    '''
    def __init__(self, *p, **kw):
        '''Valid arguments for constructor:
            1.  Two objects a, b.
            2.  A 2-sequence of objects.
 
        These objects must have ordering semantics and must be
        orderable with respect to python's integers, floats, and
        float("inf").  If the integer keyword is True, they must be
        python integers.
 
        Note it's legal to construct a Rng object with Rng(a, a).
 
        Keywords are:
            integer     The sequence is made of integers.
            lopen       The left end of the range is open if True.
            ropen       The right end of the range is open if True.
            open        Set both ends to open.
        '''
        self.int = kw.get("integer", False)
        self.lopen = bool(kw.get("lopen", False))
        self.ropen = bool(kw.get("ropen", False))
        if bool(kw.get("open", False)):
            self.lopen = self.ropen = True
        # Validate input data
        if len(p) == 1:     # Must be a 2-sequence of numbers
            e = ValueError("Need a 2-sequence of orderable objects")
            try:
                n = len(p[0])
                if n != 2:
                    raise e
                a, b = p[0]
            except TypeError:
                raise e
        elif len(p) == 2:
            a, b = p[0], p[1]
        else:
            m = "Init with two orderable objects or 2-sequence of such objects"
            raise ValueError(m)
        if self.int:
            msg = "'integer' keyword means objects must be integers or inf"
            if not isinstance(a, int) and abs(a) != inf:
                raise ValueError(msg)
            if not isinstance(b, int) and abs(b) != inf:
                raise ValueError(msg)
            # Check for open intervals that cause this discrete Rng to
            # not contain any points.
            left = a + 1 if self.lopen else a
            right = b - 1 if self.ropen else b
            if left > right:
                raise ValueError("Empty discrete interval")
        if a == b and (self.lopen or self.ropen):
            raise ValueError("Empty interval because a == b and is open")
        if a < b:
            self.a, self.b = a, b
        else:
            self.a, self.b = b, a
            self.lopen, self.ropen = self.ropen, self.lopen
        # If either a or b are infinite, then the associated interval
        # must be closed for proper comparison semantics.
        self.lopen = False if a in (-inf, inf) else self.lopen
        self.ropen = False if b in (-inf, inf) else self.ropen
    def copy(self):  # Makes a copy
        return Rng(self.a, self.b, lopen=self.lopen, ropen=self.ropen,
                   integer=self.int)
    def __lt__(self, other):  # Implements 'self < other'
        if isinstance(other, self.__class__):
            if self.a == other.a:
                if not self.lopen and other.lopen:
                    return True
                return False
            else:
                return self.a < other.a
        else:
            return self.a < other
    def __gt__(self, other):  # Implements 'self > other'
        return not(self < other or self == other)
    def __le__(self, other):  # Implements 'self <= other'
        return not (self > other)
    def __ge__(self, other):  # Implements 'self >= other'
        return not (self < other)
    def __eq__(self, other):  # Implements 'self == other'
        '''other can be of two types:  an orderable object and a Rng
        object.  If it's an orderable object, equality is the same
        thing as being in the interval.  For a Rng object, equality
        means all the attributes of the two Rng objects are the same.
        '''
        if isinstance(other, Interval):
            raise ValueError("other can't be an interval")
        if not isinstance(other, self.__class__):
            return other in self
        return (
            self.a == other.a and
            self.b == other.b and
            self.lopen == other.lopen and
            self.ropen == other.ropen and
            self.int == other.int
        )
    def expand(self, k=1):
        '''If either of the endpoints is an uncertainties ufloat
        object, expand it to mean - k*stddev on the left or
        mean + k*stddev on the right and replace the ufloat with a
        float.
        '''
        if not have_uncertainties:
            return
        if isinstance(self.a, U.UFloat):
            self.a = float(self.a.nominal_value - k*self.a.std_dev)
        if isinstance(self.b, U.UFloat):
            self.b = float(self.b.nominal_value + k*self.b.std_dev)
    def overlap(self, other, relaxed=False):
        '''Return True if self and other intersect.  If relaxed is
        True, then True will be returned in the special case of self
        and other being
            [a, b) and [b, c]
        or
            [a, b] and (b, c]
        In these two cases, the intersection is null, but we'd want to
        say the intervals overlapped so that we could coalesce them
        into 1.
        '''
        if not isinstance(other, Rng):
            raise ValueError("other must be a Rng object")
        if self == other:
            return True
        # Order them so that o1 is less than o2.
        o1, o2 = (self, other) if self < other else (other, self)
        if relaxed:
            half = ((o1.ropen and not o2.lopen) or
                    (not o1.ropen and o2.lopen))
            if half:
                return o1.b == o2.a
        else:
            if o1.b < o2.a:
                return False
            elif o1.b == o2.a:
                return True if not o1.ropen and not o2.lopen else False
            return True
    def __add__(self, other):  # Union of Rng with other
        '''Addition is analogous to set union and can return either
        another Rng object if the two Rng objects or will return an
        Interval object if they don't.  None will never be returned
        because empty Rng objects are not allowed.
        '''
        if isinstance(other, Interval):
            return other + self
        if not self.overlap(other):
            return Interval(self, other)
        o1, o2 = (self, other) if self < other else (other, self)   # o1 < o2
        integer = self.int and other.int
        if o1.b > o2.b:
            b = o1.b
            ropen = o1.ropen
        else:
            b = o2.b
            ropen = o2.ropen
        return self.__class__((o1.a, b), lopen=o1.lopen, ropen=ropen,
                              integer=integer)
    def __radd__(self, other):
        return self + other
    def __or__(self, other):
        return self + other
    def __ror__(self, other):
        return self + other
    def __mul__(self, other):
        '''Multiplication is analogous to set intersection and returns
        a new Rng object that is effectively the intersection of self
        and other if the two Rng objects overlap.  Note if only the
        endpoints overlap, a scalar can be returned, which is a Rng
        object with equal endpoints.  If there's no overlap, None is
        returned.
        '''
        if isinstance(other, Interval):
            return other*self
        if not self.overlap(other):
            return None
        # Make sure o1 is less than o2
        o1, o2 = (self, other) if self < other else (other, self)
        integer = self.int and other.int
        a, lopen = o2.a, o2.lopen
        o = o1 if o1.b < o2.b else o2
        b, ropen = o.b, o.ropen
        return Rng(a, a) if a == b else \
            self.__class__((a, b), lopen=lopen, ropen=ropen, integer=integer)
    def __rmul__(self, other):
        return self*other
    def __and__(self, other):
        return self*other
    def __rand__(self, other):
        return self*other
    def __contains__(self, value):
        '''Note a Rng object can contain another Rng object; i.e., the
        test 'rng1 in rng2' is legitimate.
        '''
        if isinstance(value, Interval):
            return Interval(self) + value
        elif isinstance(value, self.__class__):
            if self == value:
                return True     # A range always contains itself
            if self.int + value.int not in (0, 2):
                return False    # Both or neither must be discrete
            # If you sketch the four different endpoint conditions for
            # the two ranges when the endpoints are equal, you'll see
            # that <= or >= must be used only if both intervals are
            # closed; otherwise, the < or > comparisons must be used.
            c = not self.lopen and not value.lopen
            left = value.a >= self.a if c else value.a > self.a
            c = not self.ropen and not value.ropen
            right = value.b <= self.b if c else value.b < self.b
            return True if left and right else False
        else:
            if self.int and not isinstance(value, int):
                # A non-integer can't be in a discrete range (it can,
                # of course, be numerically in the range, but we
                # disallow this case to get the desired discrete
                # semantics).
                return False
            elif self.lopen:  # Left end open
                if value <= self.a:
                    return False
                else:  # value is > left end of range
                    if self.ropen:
                        # Don't need to check for inf because interval
                        # would have been set to closed.
                        return False if value >= self.b else True
                    else:
                        if value == inf:
                            return value == self.b
                        return False if value > self.b else True
            else:  # Left end closed
                # Note infinite ends will be closed
                if value == -inf:
                    return self.a == -inf
                if value < self.a:
                    return False
                else:
                    if self.ropen:
                        return False if value >= self.b else True
                    else:
                        if value == inf and self.b == inf:
                            return True
                        return False if value > self.b else True
    def __repr__(self):
        infinity = "oo"     # Unicode infinity symbol is \u221e
        l, r = "(" if self.lopen else "[",  ")" if self.ropen else "]"
        a, b = self.a, self.b
        a = "-" + infinity if a == -inf else self.a
        b = infinity if b == inf else self.b
        i = " integer" if self.int else ""
        return "Rng<{l}{a}, {b}{r}{i}>".format(**locals())
class Eps(Rng):
    ''' This is a convenience subclass of Rng to be used to construct
    ranges about a floating point value using half-widths.  Three
    construction methods are provided:  a relative half-width, an
    absolute half-width, or using a standard uncertainty multiplied by
    a k-factor (for the latter, you need to have the python
    uncertainties library installed; see
    http://pypi.python.org/pypi/uncertainties).  A keyword to the
    constructor allows the range (i.e., interval) to be open or closed
    [default is closed].
 
    The class variable releps is used for the default relative
    precision.  This is set to a value that will probably be convenient
    for for most floating point calculations that haven't involved lots
    of iteration.
 
    Some uses are:
 
        * Provide an interval comparison for dealing with e.g. roundoff
          error in floating point calculations.
        * Provide interval comparisons for physical measurements where
          the uncertainty intervals can be estimated.
 
    For the latter use case, the constructor can be initialized with a
    ufloat() object from the python Uncertainties library.  The
    half-width of the interval is then k times the standard uncertainty
    (this is sometimes called an "expanded uncertainty" and k is
    usually called the coverage factor).
    '''
    Releps = 5e-15
    def __init__(self, x, releps=Releps, eps=None, k=1, open=False):
        '''Must be initialized with one or two floating point numbers
        (see note below).  x is the numerical value and you must supply
        one of releps or eps.  releps is the relative half-width of the
        interval and eps is the direct half-width.  If you supply
        releps, the interval is [x*(1 - releps), x*(1 + releps)] and if
        you supply eps, the interval is [x - eps, x + eps].
 
        If you supply eps, it takes precedence over releps.
 
        k is used in the case where x is an Uncertainties ufloat.  In
        this case, the interval will be [n - k*s, n + k*s] where n is
        the nominal value of the ufloat and s is its standard
        deviation.
 
        Note:  the most common use case is with floating point numbers,
        but this class can be used with any orderable objects that have
        floating point semantics for addition, subtraction, and
        multiplication, as those are the arithmetic operations used in
        the constructor.
        '''
        self.super = super(self.__class__, self)
        if have_uncertainties and isinstance(x, U.UFloat):
            m, u = x.nominal_value, x.std_dev
            a, b = m - k*u, m + k*u
        else:
            if eps is not None:
                if isinstance(x, Decimal):
                    e = Decimal(str(eps))
                    a, b = x - e, x + e
                else:
                    a, b = x - eps, x + eps
            else:
                if isinstance(x, Decimal):
                    e = Decimal(str(releps))
                    a, b = x*(1 - e), x*(1 + e)
                else:
                    a, b = x*(1 - releps), x*(1 + releps)
            if abs(a) is inf or abs(b) is inf:
                raise ValueError("Can't use infinity")
        self.super.__init__(a, b, lopen=open, ropen=open)
    def __repr__(self):
        return self.super.__repr__().replace("Rng", "Eps")
class Interval(object):
    ''' Models a composite collection of scalars and discrete/continuous
    ranges of scalars.  The basic Interval object is a container of
    scalars and Rng objects.  The scalars will often be numbers of some
    type, but the only requirement is that they be orderable.  Note the
    container can be heterogeneous, as can the Rng objects -- for
    example, a Rng could have endpoints defined by an integer and
    floating point number:  Rng(2, 5.7).
 
    The Rng objects are collected in the self.ranges container and the
    individual objects (i.e., non-Rng objects) are put into
    self.points.  You can modify containers if you wish, but you must
    maintain the self.ranges list in sorted order to have proper
    operation of the Interval container.
 
    The self.ranges container is a python list by default, but you can
    change the container type if you wish by the constructor's
    container keyword.  See the Speed section in the documentation.
    '''
    def __init__(self, *items, **kw):
        '''An Interval container can be initialized with a sequence of
        any of the following types of objects:
            1.  Number
            2.  Rng object
            3.  2-sequence of numbers (turned into a Rng object)
            4.  Another Interval object
        I use the term numbers, but these 'numbers' can be any scalar
        (orderable object).  The container keyword defaults to a python
        list, but you can change it to any object with list semantics.
        '''
        self.container_type = kw.get("container", list)
        self.ranges = self.container_type()
        self.points = set()
        self.add(*items)
    def remove(self, *items):
        '''Remove the items in the items sequence; they can either by
        Rng objects or individual point objects.  It's not an error if
        the object to be removed isn't in the container.
        '''
        # O(n + m) where n is number of items in self.ranges and m is
        # the size if the items sequence.
        for item in items:
            if isinstance(item, Rng):
                try:
                    i = self.ranges.index(item)
                    del self.ranges[i]
                except ValueError:
                    pass
            elif isinstance(item, Interval):
                for i in item.ranges:
                    self.remove(i)
                for i in item.points:
                    self.points.discard(i)
            elif isinstance(item, str):
                self.points.discard(item)
            else:
                # It could be a 2-sequence
                try:
                    if len(item) == 2:
                        self.remove(Rng(*item))
                except TypeError:
                    # It's a scalar
                    self.points.discard(item)
    def _insert_rng(self, rng):
        '''rng is a Rng object; insert it into the container.
        '''
        # O(1) for empty self.ranges; O(log(n)) for non-empty container.
        if not isinstance(rng, Rng):
            raise ValueError("rng must be a Rng object")
        if not self.ranges:
            self.ranges.append(rng)
        else:
            # Insert rng using bisection to maintain self.ranges in
            # sorted order.
            insertion_index = bisect.bisect_right(self.ranges, rng)
            if insertion_index != len(self.ranges):
                self.ranges.insert(insertion_index, rng)
            else:
                self.ranges.append(rng)
    def add(self, *items):  # Add items to Interval
        '''Add items to the Interval.
        '''
        # The algorithm is O(m + n) for inserting m objects into a
        # container of n Rng objects.
        inserted_item = False
        for item in items:
            if isinstance(item, Interval):
                for rng in item.ranges:
                    self._insert_rng(rng)
                    inserted_item = True
                self.points.update(item.points)
            elif isinstance(item, Rng):
                self._insert_rng(item)
                inserted_item = True
            else:
                # It's either a sequence of 2 numbers or a scalar
                if isinstance(item, str):
                    # Strings handled specially so we don't accidentally
                    # do len() on a string.
                    self.points.add(item)
                else:
                    # It's a 2-sequence if len() works on it; otherwise
                    # it's a scalar.
                    try:
                        if len(item) != 2:
                            msg = "'{0}' must be 2-sequence".format(item)
                            raise ValueError(msg)
                    except TypeError:
                        self.points.add(item)
                    else:
                        try:
                            self._insert_rng(Rng(item))
                        except TypeError as e:
                            if "unorderable" in str(e):
                                msg = "Incompatible scalars"
                                raise ValueError(msg)
                            else:
                                raise
                        inserted_item = True
        if inserted_item and len(self.ranges) > 1:
            self._coalesce()
    def _coalesce(self, relaxed=False):  # Interval:  coalesce self.ranges
        # Coalesce the Rng objects in self.ranges using pairwise unions
        # if they overlap.  If relaxed is false, the definition of
        # overlapping is that their intersection is not null.  If
        # relaxed is True, they will overlap if the two intervals i1
        # and i2 where i1 < i2 "just miss" intersecting because i1's
        # right-hand endpoint is open and equal to i2's left-hand
        # endpoint, which is closed (or vice versa).  In other words,
        # if relaxed is True, then a situation with half-open intervals
        # like [a, b) and [b, c] or [a, b] and (b, c] will result in
        # the coalesced interval [a, c].  This is not done by default
        # because it may not be the desired behavior.
    
        # This is an O(n) algorithm.  Note if any of the Rng objects
        # have equal endpoints (i.e., they're a scalar), they're put
        # into the points container.
        t = self.container_type()
        for rng in self.ranges:
            if rng.a == rng.b:
                assert(not(rng.lopen or rng.ropen))
                self.points.add(rng.a)
            else:
                if t and t[-1].overlap(rng, relaxed=relaxed):
                    t[-1].ropen = False
                    t[-1] += rng
                else:
                    t.append(rng)
        self.ranges = t
    def collapse(self):
        '''Causes the contained Rng objects to be coalesced and relaxes
        the requirement that they must have at least one point of
        overlap to be coalesced.  Thus, two intervals like [a, b) and
        [b, c] will be collapsed into [a, c].
        '''
        self._coalesce(relaxed=True)
    def expand(self, k=1):
        '''Search through each Rng object in the Interval and expand
        any that contain uncertainties ufloat objects using the
        indicated coverage factor k.
        '''
        if not have_uncertainties:
            return
        for rng in self.ranges:
            rng.expand(k)
        self.ranges.sort()
        self._coalesce()
    def __repr__(self):
        t = ", ".join([str(i) for i in sorted(self.points)])
        p = "Points = {{{0}}}".format(t) if t else ""
        t = ', '.join([str(i) for i in self.ranges])
        s = ", " if p else ""
        r = "{0}Ranges = {1}".format(s, t) if t else ""
        return "Interval({0}{1})".format(p, r)
    def __eq__(self, other):
        if not isinstance(other, Interval):
            raise ValueError("other must be an Interval object")
        return (self.points == other.points) and (self.ranges == other.ranges)
    def __contains__(self, item):
        '''item can be an orderable object or a Rng object.
        '''
        if isinstance(item, Interval):
            raise ValueError("item can't be an Interval")
        if not isinstance(item, Rng) and item in self.points:
            return True
        if use_binary_search:   # (self.ranges is kept in sorted order)
            return self._find_index(item) is not None  # O(log(n))
        else:
            for rng in self.ranges:  # Linear O(n) search
                if item in rng:
                    return True
                # If we're past the last possible Rng object that item
                # could be in, stop the iteration.
                if isinstance(item, Rng):
                    if item.b < rng.a:
                        return False
                else:
                    if item < rng.a:
                        return False
            return False
    def _find_index(self, x):
        '''Return the rightmost index i of the Rng container
        (self.ranges) where self.ranges[i] <= x or None if it's not
        found.
        '''
        # Algorithm from python documentation on bisect module,
        # "Searching Sorted Lists".
        a, n = self.ranges, len(self.ranges)
        i = bisect.bisect_right(a, x)
        return i - 1 if (i and x in a[i - 1]) else None
    def copy(self):
        '''Returns a copy of an Interval object.
        '''
        i = Interval()
        i.points = self.points.copy()
        i.ranges = self.ranges[:]
        return i
    def __add__(self, other):
        '''Models the mathematical union.  other can be a None, Rng,
        Interval, or 2-sequence of scalars.
        '''
        cp = self.copy()
        if other is None:
            pass
        elif isinstance(other, Interval):
            cp.add(*other.ranges)
            cp.points |= other.points
        elif isinstance(other, Rng):
            cp.add(other)
        else:
            self.add(Rng(*other))   # 2-sequence
        return cp
    def __radd__(self, other):
        return self + other
    def __or__(self, other):
        return self + other
    def __ror__(self, other):
        return self + other
    def _intersect(self, rng):
        '''rng must be a Rng object.  If rng is in self, then
        incorporate rng into self by pairwise intersection.
        '''
        # O(n) algorithm
        if not isinstance(rng, Rng):
            raise ValueError("rng must be a Rng object")
        results = self.container_type()
        for r in self.ranges:
            i = r*rng
            if i is not None:
                results.append(i)
        # Note we do not need to sort results, as it should already be
        # sorted because self.ranges was and the intersection only
        # picked the Rng or a subset of each Rng.  Note results can be
        # empty.
        self.ranges = results
    def __mul__(self, other):
        '''Models the mathematical intersection.  other can be None, a
        Rng, Interval, or 2-sequence of scalars.
        '''
        cp = self.copy()
        if other is None:
            return None
        elif isinstance(other, Interval):
            for rng in other.ranges:
                cp._intersect(rng)
            cp.points &= other.points
        elif isinstance(other, Rng):
            cp._intersect(other)
        else:
            cp._intersect(Rng(*other))      # 2-sequence
        cp._coalesce()
        return cp
    def __rmul__(self, other):
        return self*other
    def __and__(self, other):
        return self*other
    def __rand__(self, other):
        return self*other
class Partition(Interval):
    ''' Models a partition of a portion of the real line or all of it
    (see note below).  The partition is a set of Rng objects that are
    half-open on one end and result in the whole portion of the real
    line when their union is taken.  The primary interface is to call
    the Partition object as a function with a number.  The index of the
    partition this number is in is returned or None if the number is
    not in the partition.
 
    Note:  I've used the common use case of partitioning the real line,
    but since the Partition object is a subclass of Interval and
    Partition's methods do not require any methods of the scalars in
    its Rng objects other than ordering operators, the Partition class
    can be used to partition any discrete or continuous orderable set
    of scalars.
 
    Though a Partition object is an Interval, I've decided that their
    use is specialized and I've not allowed them to have the addition
    and multiplication features of Intervals.  The reason is that, in
    general, they would no longer be Partition objects, which would be
    evidenced that taking the union of their Rng objects would no
    longer give the original interval.  In other words, this union of
    the Rng objects to give the original interval is a class invariant.
    '''
    def __init__(self, *items, **kw):
        '''The items must be scalars, inf, or -inf -- or the
        first item can be a sequence of such items.
        '''
        self.super = super(self.__class__, self)
        self.super.__init__()
        self.lopen = kw.get("lopen", False)  # Open on right by default
        e = ValueError("Need at least two scalars to create a partition")
        if not items:
            raise e
        elif len(items) == 1:
            our_items = items[0]
            if len(our_items) < 2:
                raise e
        else:
            our_items = items
        # Put the unique items into a sorted list
        self.items = list(set(our_items))
        self.items.sort()
        # Pair each item with the next one in the list and construct a
        # Rng object from them.
        for i in zip(self.items, self.items[1:]):
            rng = Rng(i, lopen=True) if self.lopen else Rng(i, ropen=True)
            self.add(rng)
        # To ensure that a union of all the Rng objects contained
        # returns the original closed interval, change the appropriate
        # endpoint in the first or last Rng object.
        if self.lopen:
            self.ranges[0].lopen = False
        else:
            self.ranges[-1].ropen = False
    def collapse(self):
        '''This is a convenience operation that changes all the Rng
        objects in the container to closed intervals and then takes
        their union and returns it as an Interval object that should be
        equal to the original interval (i.e., it's a class invariant).
        The original Partition object is unchanged.
 
        It's different than Interval.collapse() in that all of the
        Rng objects are set to closed.
        '''
        # O(n)
        r = self.container_type()
        for i in self.ranges:
            i.lopen = i.ropen = False
            r.append(i)
        return Interval(*r)
    def __repr__(self):
        return self.super.__repr__().replace("Interval", "Partition")
    def __call__(self, x):
        '''Return and integer representing the index position of the
        partition x is in or None if it cannot be found.
        '''
        if use_binary_search:  # Can do because container is kept sorted
            return self._find_index(x)
        else:
            # O(n) linear algorithm
            for i, rng in enumerate(self.ranges):
                if x in rng:
                    return i
                # If rng's left-hand point is greater than x, then all
                # further Rng objects' will be too, so we're done.
                if rng.a > x:
                    break
            return None
    def __getitem__(self, i):
        '''Allows you to get the Rng object corresponding to a given
        integer index returned from p(x) where p is a Partition object
        and x is a scalar.
        '''
        return self.ranges[i]
    def __add__(self, other):
        raise SyntaxError("Operation not allowed")
    def __radd__(self, other):
        raise SyntaxError("Operation not allowed")
    def __mul__(self, other):
        raise SyntaxError("Operation not allowed")
    def __rmul__(self, other):
        raise SyntaxError("Operation not allowed")
def Range(*p):
    ''' Convenience generator that can replace python's built-in range()
    function.  The built-in unfortunately doesn't work with Infinity
    objects, but Range() does -- allowing you to create "infinite"
    arithmetical progressions.  Of course, the loop that uses such
    things must have an explicit ending point or your script will
    not terminate.
    '''
    if len(p) == 1:
        start, stop, inc = 0, p[0], 1
    elif len(p) == 2:
        start, stop, inc = p[0], p[1], 1
    elif len(p) == 3:
        start, stop, inc = p[0], p[1], p[2]
    else:
        raise ValueError("Need 1 to 3 arguments")
    i = start
    if inf.is_infinite(stop) and stop == -inf:
        while i > stop:
            yield i
            i += inc
    else:
        while i < stop:
            yield i
            i += inc
if 0:
    # Show ordering amongst different scalars
    from mpmath import mpf
    from fractions import Fraction
    from uncertainties import ufloat
    from itertools import combinations
    m = mpf("1.2")
    d = Decimal("1.3")
    f = Fraction(14, 10)
    u = ufloat(1.5, 1)
    for x, y in combinations((m, d, f, u), 2):
        try:
            print(f"{type(x)} < {type(y)} = {x < y}")
        except Exception:
            print(f"{type(x)} < {type(y)} not supported")
if __name__ == "__main__": 
    import sys
    from lwtest import run, raises, assert_equal, Assert
    def TestRange():
        # One parameter
        a, stop = [], 5
        for i in Range(inf):
            if i >= stop:
                break
            a.append(i)
        Assert(a == list(range(stop)))
        # Two parameters
        a = []
        for i in Range(0, inf):
            if i >= stop:
                break
            a.append(i)
        Assert(a == list(range(stop)))
        # Three parameters
        a = []
        for i in Range(0, inf, 1):
            if i >= stop:
                break
            a.append(i)
        Assert(a == list(range(stop)))
        # Test using -inf
        a, start, stop, inc = [], 0, 10, -1
        result = [-i for i in range(stop)]
        for i in Range(0, -inf, -1):
            if i <= -stop:
                break
            a.append(i)
        Assert(a == result)
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
            Assert(j in i)
        for j in (0, 1 - eps, 1 + eps, 7.2, 88):
            Assert(j not in i)
        # Show deletion works
        i.remove(Rng(3, 4))
        Assert(3 not in i)
        # Show Rng's open keyword is equivalent to using lopen and ropen
        a, b = 0, 5
        r1 = Rng(a, b, open=True)
        r2 = Rng(a, b, lopen=True, ropen=True)
        Assert(r1 == r2)
        # Show an Interval created with numerous copies of the same Rng object
        # is equivalent to one of the Rng objects.
        a, b = 0, 1
        items = [Rng(a, b)]*10
        i = Interval(*items)
        Assert(len(i.ranges) == 1)
        r = i.ranges[0]
        Assert(a == r.a and b == r.b)
    def TestInInterval():
        eps = 1e-15
        i = Interval(1, 2, Rng(5, 7.2, ropen=True), Rng(88, inf))
        i.add(Rng(12, 14, lopen=True, ropen=True, integer=True))
        i.add(-42)
        for j in (-42, 1, 2, 5, 5 + eps, 7.2 - eps, 13, 88, 1e308,
                inf - eps, inf - 1e308, inf):
            Assert(j in i)
        eps = 1e-14
        for j in (-inf, -43, -42 - eps, -42 + eps, -41, 7.2, 12, 14,
                13 + eps, 88 - eps):
            Assert(j not in i)
        # Real line except 0
        i = Interval(Rng(-inf, 0, ropen=True), Rng(0, inf, lopen=True))
        Assert(-eps in i)
        Assert(eps in i)
        Assert(0 not in i)
        Assert(0.0 not in i)
    def TestIntervalExpand():
        # This also tests Rng.expand()
        if not have_uncertainties:
            return
        s, eps, a, b, k = 0.01, 1e-14, 1, 2, 2
        u1, u2 = U.ufloat(a, s), U.ufloat(b, s)
        R = Rng(u1, u2)
        I = Interval(R.copy())
        for r in (R, I):
            Assert(a in r)
            Assert(a + eps in r)
            Assert(a - eps not in r)
            Assert(b in r)
            Assert(b - eps in r)
            Assert(b + eps not in r)
        # Check Rng's expand()
        R.expand(k)
        Assert(a - k*s in R)
        Assert(b + k*s in R)
        # Check Interval's expand()
        I.expand(k)
        Assert(a - k*s in I)
        Assert(b + k*s in I)
        r = I.ranges[0]
        Assert(isinstance(r.a, float))
        Assert(isinstance(r.b, float))
    def TestEps():
        o, e = 1, 0.01
        for E in (Eps(o, releps=e), Eps(o, eps=e)):
            Assert(E.a == o - e and E.b == o + e)
            Assert(o - 2*e not in E)
            Assert(o - e in E)
            Assert(o in E)
            Assert(o + e in E)
            Assert(o + 2*e not in E)
            Assert(E in E)
            Assert(E == E)
        # Equality comparison with number
        eps = 1e-15
        for e in (Eps(1, eps=1), Eps(1, releps=1)):
            Assert(0 - eps != e)
            Assert(0 - eps not in e)
            Assert(2 + eps != e)
            Assert(2 + eps not in e)
            for i in (0, 0.01, 0.5, 0.99, 1, 1.01, 1.5, 1.99, 2):
                Assert(i in e)
                Assert(i in e)
        # Using an uncertainties.ufloat
        if have_uncertainties:
            x = U.ufloat(1, 1)
            e = Eps(x, k=1)
            Assert(e.a == 0 and e.b == 2)
            e = Eps(x, k=2)
            Assert(e.a == -1 and e.b == 3)
        # Make an open epsilon ball
        e = Eps(2, eps=1, open=True)
        a, b, eps = 1, 3, 1e-15
        Assert(a not in e)
        Assert(a + eps in e)
        Assert(b - eps in e)
        Assert(b not in e)
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
        Assert(r.a == 1 and r.b == 2 and not r.int)
        r = Rng(1, 2, integer=True)
        Assert(r.a == 1 and r.b == 2 and r.int)
        # Floats
        r = Rng(1.1, 2.2)
        Assert(r.a == 1.1 and r.b == 2.2 and not r.int)
        # Decimal
        r = Rng(Decimal("1.1"), Decimal("2.2"))
        # mpmath mpf objects
        if have_mpmath:
            r = Rng(mp.mpf("1.1"), mp.mpf("2.2"))
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
            Assert(r.a == 1 and r.b == 3)
        r1, r2 = Rng(1, 2), Rng(1, 3)
        for r in (r1 + r2, r1 | r2):
            Assert(r.a == 1 and r.b == 3)
        # Half-open on the left
        r1, r2 = Rng(1, 2, lopen=True), Rng(1, 3)
        for r in (r1 + r2, r1 | r2):
            Assert(r.a == 1 and r.b == 3 and not r.lopen and not r.ropen)
        # Both half-open on the left
        r1, r2 = Rng(1, 2, lopen=True), Rng(1, 3, lopen=True)
        for r in (r1 + r2, r1 | r2):
            Assert(r.a == 1 and r.b == 3 and r.lopen and not r.ropen)
        # Half-open on the right
        r1, r2 = Rng(1, 2, ropen=True), Rng(1, 3)
        for r in (r1 + r2, r1 | r2):
            Assert(r.a == 1 and r.b == 3 and not r.lopen and not r.ropen)
        # Both half-open on the right
        r1, r2 = Rng(1, 2, ropen=True), Rng(1, 3, ropen=True)
        for r in (r1 + r2, r1 | r2):
            Assert(r.a == 1 and r.b == 3 and not r.lopen and r.ropen)
        # No overlap
        r1, r2 = Rng(1, 2), Rng(3, 4)
        i = Interval(r1, r2)
        Assert(r1 + r2 == i)
        # Integer intervals
        r1, r2 = Rng(1, 5, integer=True), Rng(2, 6, integer=True)
        Assert(r1 + r2 == Rng(1, 6, integer=True))
        Assert(r1 | r2 == Rng(1, 6, integer=True))
        # Rng union with Interval works
        r, i = Rng(1, 3), Interval((2, 4), (5, 6))
        Assert(r + i == Interval((1, 4), (5, 6)))
        Assert(i + r == Interval((1, 4), (5, 6)))
        Assert(r | i == Interval((1, 4), (5, 6)))
        Assert(i | r == Interval((1, 4), (5, 6)))
    def TestRngMultiplication():
        # Closed
        r1, r2 = Rng(1, 2), Rng(2, 3)
        for r in (r1*r2, r1 & r2):
            Assert(r == Rng(2, 2))
        r1, r2 = Rng(1, 2), Rng(1, 3)
        for r in (r1*r2, r1 & r2):
            Assert(r.a == 1 and r.b == 2)
        # Half-open on the left
        r1, r2 = Rng(1, 2, lopen=True), Rng(1, 3)
        for r in (r1*r2, r1 & r2):
            Assert(r.a == 1 and r.b == 2 and r.lopen and not r.ropen)
        # Half-open on the right
        r1, r2 = Rng(1, 2, ropen=True), Rng(1, 3)
        for r in (r1*r2, r1 & r2):
            Assert(r.a == 1 and r.b == 2 and r.ropen and not r.lopen)
        # Both open
        r1, r2 = Rng(1, 2, lopen=True, ropen=True), Rng(1, 3)
        for r in (r1*r2, r1 & r2):
            Assert(r.a == 1 and r.b == 2 and r.lopen and r.lopen)
        # No overlap
        r1, r2 = Rng(1, 2), Rng(3, 4)
        for r in (r1*r2, r1 & r2):
            Assert(r is None)
        # Integer intervals
        r1, r2 = Rng(1, 5, integer=True), Rng(2, 6, integer=True)
        for r in (r1*r2, r1 & r2):
            Assert(r == Rng(2, 5, integer=True))
        # Can intersect with an Interval object
        r, i = Rng(1, 3), Interval((2, 4), (5, 6))
        Assert(r*i == Interval((2, 3)))
        Assert(i*r == Interval((2, 3)))
        Assert(r & i == Interval((2, 3)))
        Assert(i & r == Interval((2, 3)))
    def TestRngOrdering():
        r1, r2 = Rng(1, 3), Rng(2, 3)
        Assert(r1 < r2)
        Assert(r1 <= r2)
        Assert(r2 > r1)
        Assert(r2 >= r1)
        Assert(not r1 > r2)
        Assert(not r1 >= r2)
        Assert(r1 != r2)
        r1, r2 = Rng(1, 3), Rng(1, 3)
        Assert(r1 == r2)
        Assert(not r1 > r2)
        Assert(r1 >= r2)
        Assert(not r2 < r1)
        Assert(r2 >= r1)
    def TestIntervalAdd():
        # Check Interval.add()
        # Single point
        i = Interval()
        i.add(0)
        Assert(i == Interval(0))
        # Multiple points
        i = Interval()
        i.add(0, 1)
        Assert(i == Interval(0, 1))
        # Single range via sequence
        i = Interval()
        i.add((1, 2))
        Assert(i == Interval(Rng(1, 2)))
        # Single range via Rng
        i = Interval()
        i.add(Rng(1, 2))
        Assert(i == Interval(Rng(1, 2)))
        # Single range via Interval
        i = Interval()
        i.add(Interval((1, 2)))
        Assert(i == Interval(Rng(1, 2)))
        # Multiple ranges via sequence
        i = Interval()
        i.add((1, 2), (3, 4))
        Assert(i == Interval(Rng(1, 2), Rng(3, 4)))
        # Multiple ranges via Rng
        i = Interval()
        i.add(Rng(1, 2), Rng(3, 4))
        Assert(i == Interval(Rng(1, 2), Rng(3, 4)))
        # Multiple ranges via Interval
        i = Interval()
        i.add(Interval((1, 2), (3, 4)))
        Assert(i == Interval(Rng(1, 2), Rng(3, 4)))
        # Adding ranges and points from another Interval
        i = Interval(0, 1, (10, 11), (13, 14))
        j = Interval(2, 3, (15, 16), (17, 18))
        i.add(j)
        Assert(i == Interval(0, 1, 2, 3,
                            Rng(10, 11),
                            Rng(13, 14),
                            Rng(15, 16),
                            Rng(17, 18)
                            ))
        # Same, but Rng objects should coalesce into one
        i = Interval(0, 1, (10, 11), (12, 13))
        j = Interval(2, 3, (11, 12), (13, 14))
        i.add(j)
        Assert(i == Interval(0, 1, 2, 3, Rng(10, 14)))
    def TestIntervalRemove():
        empty = Interval()
        # Check Interval.remove()
        # Single point
        i = Interval(0)
        i.remove(0)
        Assert(i == empty)
        # Multiple points, no Rng objects
        i = Interval(0, 1, 2)
        i.remove(1, 2)
        Assert(i == Interval(0))
        # Multiple points with Rng object
        i = Interval(0, 1, 2, (4, 5))
        i.remove(1, 2)
        Assert(i == Interval(0, (4, 5)))
        # Single range via sequence
        i = Interval((1, 2))
        i.remove((1, 2))
        Assert(i == empty)
        # Single range via Rng
        i = Interval((1, 2))
        i.remove(Rng(1, 2))
        Assert(i == empty)
        # Single range via Interval
        i = Interval((1, 2))
        i.remove(Interval((1, 2)))
        Assert(i == empty)
        # Multiple ranges via sequence
        i = Interval(0, (1, 2), (3, 4), (5, 6))
        i.remove((1, 2), (3, 4))
        Assert(i == Interval(0, Rng(5, 6)))
        # Multiple ranges via Rng
        i = Interval(0, (1, 2), (3, 4), (5, 6))
        i.remove(Rng(1, 2), Rng(3, 4))
        Assert(i == Interval(0, Rng(5, 6)))
        # Multiple ranges via Interval
        i = Interval(0, (1, 2), (3, 4), (5, 6))
        i.remove(Interval((1, 2), (3, 4)))
        Assert(i == Interval(0, Rng(5, 6)))
    def TestIntervalAddition():
        # Empty intervals
        Assert(Interval() + Interval() == Interval())
        Assert(Interval() | Interval() == Interval())
        # Intervals with points only
        Assert(Interval(1) + Interval(2) == Interval(1, 2))
        Assert(Interval(1) | Interval(2) == Interval(1, 2))
        # Intervals with only Rng objects
        i1, i2 = Interval((1, 2)), Interval((3, 4))
        Assert(i1 + i2 == Interval((1, 2), (3, 4)))
        Assert(i1 | i2 == Interval((1, 2), (3, 4)))
        i1, i2 = Interval((1, 2)), Interval((1, 2))
        Assert(i1 + i2 == Interval((1, 2)))
        Assert(i1 | i2 == Interval((1, 2)))
        i1, i2 = Interval((1, 2)), Interval((2, 4))
        Assert(i1 + i2 == Interval((1, 4)))
        Assert(i1 | i2 == Interval((1, 4)))
        # Intervals with points and Rng objects
        i1, i2 = Interval(5, (1, 2)), Interval(6, (3, 4))
        Assert(i1 + i2 == Interval((1, 2), (3, 4), 5, 6))
        Assert(i1 | i2 == Interval((1, 2), (3, 4), 5, 6))
        # Empty intervals return an empty Interval
        i1, i2 = Interval(), Interval()
        Assert(i1 + i2 == Interval())
        Assert(i1 | i2 == Interval())
        # Contiguous open range won't coalesce but will collapse
        i1, i2 = Interval(Rng(1, 2, ropen=True)), Interval((2, 4))
        i, r = i1 + i2, Interval((1, 4))
        Assert(i != r)
        i.collapse()
        Assert(i == r)
    def TestIntervalMultiplication():
        # Empty intervals
        Assert(Interval()*Interval() == Interval())
        Assert(Interval()*Interval(1) == Interval())
        Assert(Interval() & Interval() == Interval())
        Assert(Interval() & Interval(1) == Interval())
        # Intervals with points only
        Assert(Interval(1)*Interval(2) == Interval())
        Assert(Interval(1, 2)*Interval(1) == Interval(1))
        Assert(Interval(1) & Interval(2) == Interval())
        Assert(Interval(1, 2) & Interval(1) == Interval(1))
        # Intervals with only Rng objects
        i1, i2 = Interval((1, 2)), Interval((1.5, 2))
        Assert(i1*i2 == Interval((1.5, 2)))
        Assert(i1 & i2 == Interval((1.5, 2)))
        i1, i2 = Interval((1, 2)), Interval((1, 2))
        Assert(i1*i2 == Interval((1, 2)))
        Assert(i1 & i2 == Interval((1, 2)))
        i1, i2 = Interval((1, 2)), Interval((2, 4))
        Assert(i1*i2 == Interval(2))
        Assert(i1 & i2 == Interval(2))
        # Intervals with points and Rng objects
        i1, i2 = Interval(5, (1, 2)), Interval(5, 6, (2, 4))
        Assert(i1*i2 == Interval(2, 5))
        Assert(i1 & i2 == Interval(2, 5))
    def TestIn():
        # Floats
        a, eps = 2.5, 1e-15
        for r in (Rng(0, a), Rng(a, 0)):
            Assert(0 in r)
            Assert(0 + eps in r)
            Assert(1 in r)
            Assert(a in r)
            Assert(a - eps in r)
        r = Rng(0, 2, lopen=True, ropen=True)
        Assert(0 not in r)
        Assert(0 + eps in r)
        Assert(2 not in r)
        Assert(2 - eps in r)
        # Integers
        a = 5
        r = Rng(0, a, integer=True)
        for i in range(a + 1):
            Assert(i in r)
            Assert(i + eps not in r)
            Assert(i - eps not in r)
        r = Rng(0, 2, integer=True, lopen=True, ropen=True)
        Assert(0 not in r)
        Assert(1 in r)
        Assert(2 not in r)
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
            Assert(1 in r)
            Assert(1.0 in r)
            Assert(Decimal(1) in r)
            Assert(Decimal("1.0") in r)
            Assert(2 in r)
            Assert(2.5 in r)
            Assert(3 in r)
            Assert(Decimal(3) in r)
            Assert(3.0 in r)
            Assert(Decimal("3.0") in r)
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
            Assert(1 not in r)
            Assert(1.0 not in r)
            Assert(Decimal(1) not in r)
            Assert(Decimal("1.0") not in r)
            Assert(2 in r)
            Assert(2.5 in r)
            Assert(3 in r)
            Assert(Decimal(3) in r)
            Assert(3.0 in r)
            Assert(Decimal("3.0") in r)
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
            Assert(1 in r)
            Assert(1.0 in r)
            Assert(Decimal(1) in r)
            Assert(Decimal("1.0") in r)
            Assert(2 in r)
            Assert(2.5 in r)
            Assert(3 not in r)
            Assert(Decimal(3) not in r)
            Assert(3.0 not in r)
            Assert(Decimal("3.0") not in r)
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
            Assert(1 not in r)
            Assert(1.0 not in r)
            Assert(Decimal(1) not in r)
            Assert(Decimal("1.0") not in r)
            Assert(2 in r)
            Assert(2.5 in r)
            Assert(3 not in r)
            Assert(Decimal(3) not in r)
            Assert(3.0 not in r)
            Assert(Decimal("3.0") not in r)
    def TestInInfiniteIntervals():
        r = Rng(0, inf, lopen=True, ropen=True)
        Assert(0 not in r)
        Assert(inf in r)
        Assert(1.2345678e308 in r)
        Assert(Decimal("1e50000") in r)
        Assert(-inf not in r)
        r = Rng(-inf, 0, lopen=True, ropen=True)
        Assert(-inf in r)
        Assert(-1.2345678e308 in r)
        Assert(Decimal("-1e50000") in r)
        Assert(inf not in r)
        r = Rng(-inf, inf, lopen=True, ropen=True)
        Assert(-inf in r)
        Assert(-1.2345678e308 in r)
        Assert(Decimal("-1e50000") in r)
        Assert(0 in r)
        Assert(1.2345678e308 in r)
        Assert(Decimal("1e50000") in r)
        Assert(inf in r)
    def TestInWithMpmath():
        if have_mpmath:
            r = Rng(0, inf, lopen=True, ropen=True)
            Assert(mp.mpf("0") not in r)
            Assert(mp.mpf("1e-50000") in r)
            Assert(mp.mpf("1e50000") in r)
            # A rather large number, but still finite:
            Assert(10**mp.mpf("1e100") in r)
    def TestInWithASCII():
        r = Rng("a", "z")
        for i in range(128):
            if ord("a") <= i <= ord("z"):
                Assert(chr(i) in r)
            else:
                Assert(chr(i) not in r)
        r = Rng("a", "z", lopen=True)
        Assert("a" not in r)
        Assert("b" in r)
        r = Rng("a", "z", ropen=True)
        Assert("y" in r)
        Assert("z" not in r)
    def TestInWithUnicode():
        low, high = 1000, 2000
        a, b = 1200, 1700
        r = Rng(chr(a), chr(b))
        for i in range(low, high + 1):
            if a <= i <= b:
                Assert(chr(i) in r)
            else:
                Assert(chr(i) not in r)
    def TestInWithWordStrings():
        r = Rng("goodbye", "hello")
        Assert("greet" in r)
        Assert("gimlet" not in r)
        Assert("h" in r)
        Assert("hellacious" in r)
        Assert("help" not in r)
    def TestInWithDateObjects():
        d1, d2 = datetime.date(2013, 8, 1), datetime.date(2013, 10, 16)
        r, yr = Rng(d1, d2), 2013
        Assert(datetime.date(yr, 7, 31) not in r)
        Assert(datetime.date(yr, 8, 1) in r)
        Assert(datetime.date(yr, 8, 2) in r)
        Assert(datetime.date(yr, 10, 15) in r)
        Assert(datetime.date(yr, 10, 16) in r)
        Assert(datetime.date(yr, 10, 17) not in r)
        yr = 2012
        Assert(datetime.date(yr, 7, 31) not in r)
        Assert(datetime.date(yr, 8, 1) not in r)
        Assert(datetime.date(yr, 8, 2) not in r)
        Assert(datetime.date(yr, 10, 15) not in r)
        Assert(datetime.date(yr, 10, 16) not in r)
        Assert(datetime.date(yr, 10, 17) not in r)
    def TestInfinity():
        # Basic ordering
        M = sys.float_info.max  # Largest float
        for x in (-1e308, -10, -1.0, 0, 1.0, 10, 1e308, M):
            Assert(x < inf)
            Assert(x <= inf)
            Assert(x > -inf)
            Assert(x >= -inf)
            Assert(x != inf)
            Assert(x != -inf)
        # Check with mpmath numbers
        if have_mpmath:
            for i in ("-1e308", "-10", "-1.0", "0", "1.0", "10", "1e308"):
                x = mp.mpf(i)
                Assert(x < inf)
                Assert(x <= inf)
                Assert(x > -inf)
                Assert(x >= -inf)
                Assert(x != inf)
                Assert(x != -inf)
        # Check with Decimal numbers
        for i in ("-1e308", "-10", "-1.0", "0", "1.0", "10", "1e308"):
            x = Decimal(i)
            Assert(x < inf)
            Assert(x <= inf)
            Assert(x > -inf)
            Assert(x >= -inf)
            Assert(x != inf)
            Assert(x != -inf)
        # Order with respect to self
        Assert(inf == inf)
        Assert(+inf == inf)
        Assert(-inf == -inf)
        Assert(-inf < inf)
        Assert(-inf <= inf)
        Assert(inf > -inf)
        Assert(inf >= -inf)
        # Addition
        Assert(1 + inf + 1 == inf)
        Assert(inf + inf == inf)
        Assert(1 + -inf + 1 == -inf)
        # Subtraction
        Assert(1 - inf - 1 == -inf)
        Assert(-inf - inf == -inf)
        Assert(-inf - 1 == -inf)
        Assert(1 - inf == -inf)
        # Multiplication
        Assert(inf*1 == inf)
        Assert(inf*1.0 == inf)
        Assert(inf*inf == inf)
        Assert(-inf*-inf == inf)
        Assert(-inf*(-inf) == inf)
        Assert(-inf*inf == -inf)
        # Division
        for i in (1, 1.0, 0):
            Assert(inf/i == inf)
            Assert(inf//i == inf)
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
        Assert(abs(inf) == inf)
        Assert(abs(-inf) == inf)
        # Can put into dictionary
        d = {inf: None, -inf: None}
        # Can convert to a float infinity
        Assert(float(inf) == float("inf"))
        Assert(float(-inf) == float("-inf"))
        # String representation
        Assert(str(inf) == "∞")
        Assert(str(-inf) == "-∞")
        # Can compare to dates and strings
        dt = datetime.datetime(2014, 1, 1)
        for d in (dt, "a"):
            Assert(d != inf)
            Assert(d < inf)
            Assert(d <= inf)
            Assert(d > -inf)
            Assert(d >= -inf)
            Assert(d != -inf)
        # Test utility function
        Assert(inf.is_infinite(inf))
        Assert(inf.is_infinite(-inf))
        Assert(not inf.is_infinite(1))
        Assert(not inf.is_infinite(-1))
    def TestPartition():
        s = [inf, 0, -oo, 1, oo, -inf]
        # Show both constructor calls work.  Results in the interval
        # [-oo, 0, 1, oo].
        p = Partition(*s)
        p = Partition(s)
        # Results in Partition(Ranges = Rng<[-oo, 0)>, Rng<[0, 1)>, Rng<[1, oo]>)
        Assert(p(-1) == 0)
        Assert(p[p(-1)] == Rng((-inf, 0), ropen=True))
        Assert(p(0) == 1)
        Assert(p(1) == 2)
        # Partition with left end open
        p = Partition(s, lopen=True)
        Assert(p(-1) == 0)
        Assert(p[p(-1)] == Rng((-inf, 0), lopen=True))
        # Show class invariant hasn't changed.
        a, b = 0, 10
        for p in (Partition(range(a, b + 1), lopen=False),
                Partition(range(a, b + 1), lopen=True)):
            i = p.collapse()
            # Check that this Interval object is equal to the original range
            Assert(len(i.ranges) == 1 and Rng(a, b) == i.ranges[0])
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
    exit(run(globals(), halt=0)[0])
