'''
Provides generators that can produce sequences of floating point and
rational numbers and that are floating point/rational analogs of
range().

frange(start, stop, step)
    Best to initialize with string representations of floating point
    numbers.  You can control the output type and the implementation type,
    allowing use with a variety of number types.  Example:
        for i in frange("0", "1", "0.1"):
            sys.stdout.write(str(i) + " ")
    results in
        0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
    If start contains a '/' character, impl and return_type parameters are
    set to Rational.

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

A convenience function Sequence(string) is supplied that will return a list
from the specifications in the string.  Example:
    Sequence('1:1.5:0.1   5:1:-1  1/4:3/4:1/8')
returns
    [1, 1.1, 1.2, 1.3, 1.4, 1.5,
     5, 4, 3, 2, 1,
     1/4, 3/8, 1/2, 5/8, 3/4]
'''

# Copyright (C) 2010, 2015 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

import re
import sys
import itertools
from decimal import Decimal
from numbers import Integral
from fractions import Fraction
from pdb import set_trace as xx

try:
    from roundoff import RoundOff
    has_RoundOff = True
except ImportError:
    has_RoundOff = False

__all__ = [
    "frange",
    "ifrange",
    "lrange",
    "Sequence",
]

try:
    numpy_available = True
    import numpy
except ImportError:
    numpy_available = False

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
    print("Sixteenths:")
    for i in frange("1/16", 2, 1/16):
        print("  {0:10s} {1}".format(str(i), repr(i)))
