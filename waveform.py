'''

To Do
    - Get rid of sig, use flt 
    - Get running under python 3.11.5
    - Document the self._* attributes in the constructor
    - Review method names
    - Add a vertical ASCII plotting method that shows how things behave
    - Write a linear interpolation routine so scipy isn't mandatory
        - Is resizing really necessary?  Just create a new Waveform instance.

Module to create common waveforms as numpy arrays

    Examples are sine waves, square waves, triangle waves, pulses, etc.  These arrays are created
    by the Waveform object.

    See the pydoc display of this module's documentation along with the Waveform.pdf documentation
    file included in the distribution.  Running this module as a script will produce some plotted
    examples if you have scipy and matplotlib installed.  You'll also need the sig.py module from
    http://code.google.com/p/hobbyutil/.

    Once you've created a Waveform object, you can use it to get numpy arrays of the waveform by
    calling the Waveform object with the number of periods you want.  Example:

        # Create a sine wave with 11 points per period
        w = Waveform("sin", 11)
        y = w(2)   # Get an array containing two periods
        print(y)

        results in:

        [ 0.     0.541  0.91   0.99   0.756  0.282 -0.282 -0.756 -0.99
        -0.91  -0.541  0.     0.541  0.91   0.99   0.756  0.282 -0.282
        -0.756 -0.99  -0.91  -0.541]

    Note:  you may be surprised that the last point of the waveform doesn't return to zero (this is
    intentional so that multiple periods can be created by concatenating the raw data).  If you need
    this, use something like

        y = w(2 + (1 + eps)/w.size)

    where eps is a small number (1e-10 might be a good choice).  This avoids roundoff problems with
    floating point arithmetic compared to the naive expression w*(2 + 1/w.size).

    The Waveform object always internally stores one period of the waveform.  The object's attributes
    can be used to change the characteristics of the returned numpy array that represents the
    waveform.  Example:

        w = Waveform("sin", 21)
            Returns a Waveform object with 21 points per period that
            represents a sine wave of amplitude 1.
        w.ampl = 4.3
            Sets the amplitude to 4.3.
        w.nclip = 0
            Clip any negative values to zero.  Note there may still be
            some small negative values remaining due to the algorithm and
            how the zero attribute is set; see the discussion on clipping
            below.
        print(w)

    results in:

        Waveform(
        [0.00, 1.27, 2.42, 3.36, 4.00, 4.29, 4.19, 3.72, 2.92, 1.87, 0.641,
        0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
        )

    Note the difference in the outputs of print(w) and print(w()).

    Clipping
    --------

    Clipping is done with respect to the deviations of the waveform's points above and below the mean.
    Here's how it works.  Calculate the distance d for the waveform w as

        d = max(w) - mean(w)

    This is the distance the largest point in the waveform is above the mean.  Then clip any points
    above ymax = mean(w) + d*w.pclip to be ymax.  Treat the points below the mean analogously with
    w.nclip.

    This clipping can leave small positive or negative values where you would expect zero; this is
    caused by rounding errors.  This can be demonstrated by the following code:

        w = Waveform("sin", 20)
        w.nclip = 0
        w.zero = None
        x, y = w.xy(1)
        print(y)

    which produces

        [  0.000e+00   3.090e-01   5.878e-01   8.090e-01   9.511e-01
        1.000e+00   9.511e-01   8.090e-01   5.878e-01   3.090e-01
        1.225e-16  -1.388e-17  -1.388e-17  -1.388e-17  -1.388e-17
        -1.388e-17  -1.388e-17  -1.388e-17  -1.388e-17  -1.388e-17]

    If the zero attribute is set to (-1e-15, 1e-15), the following output is produced:

        [ 0.     0.309  0.588  0.809  0.951  1.     0.951  0.809  0.588
        0.309  0.    -0.    -0.    -0.    -0.    -0.    -0.    -0.
        -0.    -0.   ]
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2012, 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Module to get various waveforms as numpy arrays.
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        #from collections import deque
        #from pathlib import Path as P
        #import getopt
        import os
        #import re
        import sys
        import numpy as np
        from numpy.random import normal as _normal
        from collections.abc import Iterable
        from collections import defaultdict
    if 1:   # Custom imports
        #from f import flt
        from wrap import dedent
        #from color import t
        #from lwtest import Assert
        from sig import sig as _sig
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
        # scipy's interpolation routine is used when resizing a waveform.  This is optional here
        # because I may write a built-in routine that does simply linear interpolation.
        g.have_scipy = False
        try:
            from scipy.interpolate import interp1d
            g.have_scipy = True
        except ImportError:
            pass
class Waveform(object):
    _names = set((
        # The 'unknown' name is used to indicate a Waveform object that was initialized with a
        # sequence or was constructed as a composite of two other Waveform objects.  Since no copy
        # of the original data is kept, the _make() method doesn't reconstruct the Waveform's data
        # like for the other waveform types.
        "cosine",
        "dc",
        "halfsine",
        "haversine",
        "noise",
        "pulse",
        "ramp",
        "semicircle",
        "sine",
        "square",
        "triangle",
        "unknown",
    ))
    def __init__(self, *args):
        '''Create a Waveform object by the following constructors:
            Waveform(name, size)
                Makes one of the supported waveforms indicated by name with size points per
                period.  It's straightforward to add support for new types of waveforms (modify
                the _make method).  name is a string defined in the _names attribute of the
                Waveform object.  You only need to include as many characters as necessary in name
                to make it unique.
            Waveform(iterable)
                The iterable must be convertible to a numpy array.
            Waveform(numpy_array)
                The numpy array will be flattened.
            Waveform(waveform_object)
                Creates a copy of an existing Waveform object.
        '''
        self.reset()
        if len(args) == 1:
            # Initializing with another Waveform object, array or iterable
            if isinstance(args[0], Waveform):
                self.reset(args[0])
            elif isinstance(args[0], np.ndarray):
                self._data = np.array(args[0].flat).astype(float)
                self._size = len(self._data)
                self._name = "unknown"
            elif isinstance(args[0], Iterable):
                self._data = np.array(np.array(args[0]).flat).astype(float)
                self._size = len(self._data)
                self._name = "unknown"
            else:
                msg = "Need sequence, numpy array, or Waveform object"
                raise ValueError(msg)
        elif len(args) == 2:
            # Name and number of points given
            self._name, msg = self._GetName(args[0]), ""
            if isinstance(self._name, tuple):
                candidates = str(self._name).replace("[", "").replace("]", "")
                msg = ("'%s' is an ambiguous waveform name; it could be:\n"
                       "  %s" % (args[0], candidates))
            if not self._name:
                msg = "'%s' is unrecognized waveform name" % args[0]
            self._size = int(args[1])
            if self._size < 2:
                msg = "Size must be > 1"
            if msg:
                raise ValueError(msg)
            self._make()
        else:
            raise ValueError("Constructor requires 1 or 2 arguments")
    def reset(self, other=None):
        '''Reset attributes to default values.  If other is given, it's another Waveform object,
        so use its attributes to set self's.
        '''
        if other:
            assert isinstance(other, Waveform)
            self._data = other._data
            self._size = other._size
            self._name = other._name
        # Reset the attributes to default values
        self._ampl = 1 if not other else other._ampl
        self._dc = 0 if not other else other._dc
        self._duty = 0.5 if not other else other._duty
        self._gates = None if not other else other._gates
        self._kind = "linear" if not other else other._kind
        self._lge = True if not other else other._lge
        self._nclip = 1 if not other else other._nclip
        self._ndig = 3 if not other else other._ndig
        self._pclip = 1 if not other else other._pclip
        self._rle = True if not other else other._rle
        if other:
            self._zero = other._zero
        else:
            if 1:  # Two typical behaviors -- pick which one you like
                # This works with typical python floats
                eps = 1e-15
                self._zero = (-eps, eps)
            else:
                # Don't do any rounding
                self._zero = None
        self._x = None
    def _make(self):
        # Construct the waveform from the given information.
        n, X, pi = self._size, lambda n: np.arange(n)/n, np.pi
        self._x = X(n)
        nleft = int(n*self._duty)
        nright = n - nleft
        if self._name == "sine":
            left = np.sin(np.pi*X(nleft))
            right = -np.sin(np.pi*X(nright))
            self._data = np.concatenate((left, right))
        elif self._name == "cosine":
            nmiddle = int(n*(1 - self._duty))
            nleft = (n - nmiddle)//2
            nright = n - nmiddle - nleft
            left = np.cos(pi/2*X(nleft))
            xmiddle = pi/2*(1 + 2*X(nmiddle))
            middle = np.cos(xmiddle)
            xright = pi*(3/2 + X(nright)/2)
            right = np.cos(xright)
            self._data = np.concatenate((left, middle, right))
        elif self._name == "square":
            nleft = int(self._duty*self._size)
            left = np.ones(nleft)
            right = -np.ones(nright)
            self._data = np.concatenate((left, right))
        elif self._name == "pulse":
            nleft = int(self._duty*self._size)
            left = np.ones(nleft) if nleft else np.array([])
            nright = max(0, self._size - nleft)
            right = np.zeros(nright)
            self._data = np.concatenate((left, right))
        elif self._name == "triangle":
            def GetSides(nleft, nright):
                if nleft < nright:
                    # Left side up must go from 0 to just less than 1.
                    # The right side must go from 1 to just greater than
                    # 0.
                    xleft = np.arange(nleft)/nleft
                    xright = 1 - np.arange(nright)/nright
                else:
                    # Left side up must go from 0 to 1.  The right side
                    # must go from just less than 1 to just greater than
                    # 0.
                    xleft = np.arange(nleft)/(nleft - 1)
                    xright = 1 - np.arange(1, nright + 1)/(nright + 1)
                return np.concatenate((xleft, xright))
            # Left-hand side
            if 0:
                nleft = self._size//4
                nright = n//2 - nleft
            else:
                nL = int(self._size*self._duty)
                nleft = nL//2
                nright = nL - nleft
            left = GetSides(nleft, nright)
            # Right-hand side
            n = self._size - nleft - nright
            nleft = n//2
            nright = n - nleft
            right = GetSides(nleft, nright)
            self._data = np.concatenate((left, -right))
        elif self._name == "ramp":
            self._data = np.arange(n)/(n - 1)
        elif self._name == "noise":
            self._data = _normal(0, 1, self._size)
        elif self._name == "semicircle":
            mp = self._size//2
            self._data = np.sqrt(1/4 - (self._x - 1/2)**2)
            # Normalize amplitude to unity
            self._data /= self._data.max()
        elif self._name == "halfsine":
            self._data = np.sin(np.pi*self._x)
        elif self._name == "haversine":
            self._data = (1 - np.cos(2*np.pi*self._x))/2
        elif self._name == "unknown":
            pass
        elif self._name == "dc":
            self._data = np.zeros(n)
        else:
            raise RuntimeError("Bug:  unknown waveform name")
        assert len(self._data) == self._size
        self._data = self._adjust_zero(self._data)
    def xfm(self, f, *args):
        '''Apply a function f to the data in the array to transform the
        data.  f is a function that can operate on a numpy array; if
        args is not empty, then these arguments are appended to the
        function call.  Note this turns the waveform type into
        "unknown".
        '''
        if args:
            self._data = f(*([self._data] + list(args)))
        else:
            self._data = f(self._data)
        self._name = "unknown"
    def _adjust_zero(self, y):
        '''Set any array elements in y that are near zero to zero as
        specified by the pair of numbers in self._zero.  Note that the
        elements that were negative and near zero will wind up being
        -0.
        '''
        if not self._zero:
            return y
        neg, pos = self._zero
        s = np.bitwise_and(y > neg, y < 0)  # Negative numbers
        y = (~s)*y
        s = np.bitwise_and(y > 0, y < pos)  # Positive numbers
        y = (~s)*y
        return y
    def __str__(self):
        '''Convert the Waveform object to a string representation.
        This string will include all of the numpy data in the
        waveform.  You can change the number of significant digits in
        the output data by changing the ndig attribute.
        '''
        x, y = self.xy()
        return "Waveform(\n" + _sig(y, self._ndig) + "\n)"
    def __repr__(self):
        '''Same as __str__ but includes the attribute values.
        '''
        x, y = self.xy()
        s = "Waveform(\nAttributes:\n"
        attributes = self.__dict__.keys()
        attributes.sort()
        fmt = "  %%-%ds= %%s\n" % max([len(i) for i in attributes])
        for i in attributes:
            v = self.__dict__[i]
            if isinstance(v, (float, Iterable)):
                t = v if isinstance(v, str) else _sig(v, self._ndig)
            else:
                t = str(v)
            s += fmt % (i[1:], t)
        s += ")"
        return s
    def xy(self, num_periods=1):
        '''Returns a tuple (x, y) where x and y are numpy vectors.  x
        represents the abscissa values and y represents num_periods
        periods of the waveform.  Apply all the attributes first to
        the waveform.  x and y have the same number of data points.
        A common use of this method is to generate data for plotting.
        '''
        try:
            n = float(num_periods)
        except TypeError:
            msg = "Argument must be an object that can be converted to a float"
            raise TypeError(msg)
        if n <= 0:
            raise ValueError("Number of periods must be > 0")
        g = self._data.copy()
        g = self._gate(g)
        g = self._clip(g)
        g = g*self._ampl + self._dc
        res = [g]*(int(num_periods))    # Whole number of periods
        n = np.fmod(num_periods, 1)*self._size  # Fractional period
        res.append(g[:n])
        y = np.concatenate(res)
        y = self._adjust_zero(y)
        x = num_periods*np.arange(len(y))/len(y)
        return (x, y)
    def awg(self):
        '''Generate a sequence of numbers suitable for a particular
        arbitrary waveform generator.  You must implement this method
        yourself.
        '''
        raise NotImplementedError("Waveform.awg() needs to be implemented")
    def __call__(self, num_periods=1):
        '''When a Waveform object w is called with a number, the data
        array with num_periods is generated and returned.  Thus, for
        example, to get 4.5 periods of the waveform, call w(4.5).
        '''
        return self.xy(num_periods)[1]
    def _clip(self, y):
        '''Clip the waveform between the maximum and minimum values.
        First, divide the waveform into top and bottom portions around
        the mean.  Then for the upper portion, the distance d is
            d = max(waveform data) - mean
        Then the waveform's upper values are clipped to be no more
        than a distance d*self._pclip above the mean.  An analogous
        operation is done for the lower portion.
        '''
        if self._pclip == 1 and self._nclip == 1:
            return y
        mean = np.average(y)
        dmax, dmin = y.max() - mean, mean - y.min()
        if self._pclip < 1:
            M = self._pclip*dmax
            # The following array will be a Boolean numpy array that
            # is True where the values are greater than the clipping
            # value.
            g = y > mean + M
            y = g*(mean + M) + (~g)*y
        if self._nclip < 1:
            M = self._nclip*dmin
            # The following array will be a Boolean numpy array that
            # is True where the values are less than the clipping
            # value.
            g = y < mean - M
            y = g*(mean - M) + (~g)*y
        return y
    def _gate(self, y):
        '''Given the array y, which is a copy of self._data, apply the
        gating rules and return the modified array.
        '''
        if not self._gates:
            return y
        n = len(y)
        assert n == self._size
        g = list(self._gates[:])
        for g0, g1 in g:
            n0, n1 = int(n*g0), int(n*g1)
            s = np.array(range(n))
            if self._lge:
                if self._rle:
                    t = np.bitwise_and(s >= n0, s <= n1)
                else:
                    t = np.bitwise_and(s >= n0, s < n1)
            else:
                if self._rle:
                    t = np.bitwise_and(s > n0, s <= n1)
                else:
                    t = np.bitwise_and(s > n0, s < n1)
            y *= ~t
        return y
    def __neg__(self):
        '''Unary negation:  multiplies the internal numpy array of the
        data by -1.  The waveform type is "unknown" after this
        operation.
        '''
        self._data = -self._data
        self._name = "unknown"
        return self
    def __mul__(self, const):
        '''Scale the waveform object by the given constant.  If the
        const is another Waveform object, it is resampled to the same
        size as self._data and used to modulate self (i.e., const's
        data are multiplied point-wise by self's data).
        '''
        if isinstance(const, Waveform):
            const._resample(self._size)
            assert len(const._data) == len(self._data)
            self._data *= const._data
        else:
            self._data *= float(const)
            self._data = self._adjust_zero(self._data)
        self._name = "unknown"
        return self
    def __rmul__(self, const):
        return self.__mul__(const)
    def __add__(self, other):
        '''Adding two Waveform objects results in another Waveform
        object that is a concatenation of the two arrays; note we use
        the attributes to define the new arrays (i.e., we don't use
        the raw data).  The attributes of the resulting object are set
        to their defaults and the resulting waveform type is "unknown".
        '''
        if isinstance(other, Iterable):
            other = Waveform(other)
        if isinstance(other, Waveform):
            x, me = self.xy()
            x, them = other.xy()
            self._data = np.concatenate((me, them))
            self.reset()
            self._size = len(self._data)
            self._x = np.arange(self._size)/self._size
        else:
            # If other is a number, then add it to each value of the
            # array.
            try:
                x = float(other)
            except TypeError:
                msg = "Added value must be convertible to a float"
                raise TypeError(msg)
            self._data += x
        self._name = "unknown"
        self._data = self._adjust_zero(self._data)
        return self
    def __radd__(self, other):
        return other.__add__(self)
    def __sub__(self, other):
        '''Similar to addition except the other array is negated.
        '''
        if isinstance(other, Iterable):
            other = Waveform(other)
        if isinstance(other, Waveform):
            x, me = self.xy()
            x, them = other.xy()
            self._data = np.concatenate((me, -them))
            self.reset()
            self._size = len(self._data)
            self._x = np.arange(self._size)/self._size
        else:
            # If other is a number, then subtract it from each value
            # of the array.
            try:
                x = float(other)
            except TypeError:
                msg = "Added value must be convertible to a float"
                raise TypeError(msg)
            self._data -= x
        self._name = "unknown"
        self._data = self._adjust_zero(self._data)
        return self
    def __rsub__(self, other):
        return other.__sub__(self)
    def _resample(self, n):
        '''Use scipy's interp1d function to interpolate the waveform
        to a new size.  The waveform type is turned into "unknown".
        '''
        if not g.have_scipy:
            raise RuntimeError("Need scipy to resample")
        assert self._name == "unknown"
        if self._x is None:
            self._x = np.arange(self._size)/self._size
        f = interp1d(self._x, self._data, kind=self._kind)
        self._x = np.linspace(0, self._x.max(), n)
        self._data = f(self._x)
        self._data = self._adjust_zero(self._data)
    def periodize(self, num_periods):
        '''Replace self._data with a concatenation of num_periods (can be a float) of self._data.
        The waveform type is turned into "unknown".
        '''
        if num_periods <= 0:
            raise ValueError("num_periods must be > 0")
        g = self._data
        # Get integer number of periods
        res = [g]*(int(num_periods))
        # Get fractional number of period
        n = np.fmod(num_periods, 1)*self._size
        res.append(g[:n])
        self._data = np.concatenate(res)
        n = self._size = len(self._data)
        self._x = num_periods*np.arange(n)/n
        self._name = "unknown"
        self._data = self._adjust_zero(self._data)
    def normalize(self):
        '''Scale the amplitude of the data points so that the largest
        value in absolute value is unity.  The waveform type is turned
        into "unknown".
        '''
        factor = max(self._data.max(), np.abs(self._data.min()))
        self._data /= factor
        self._data = self._adjust_zero(self._data)
        self._name = "unknown"
    def _GetName(self, name):
        '''name is a string.  Find if name uniquely identifies a
        string in Waveform._names; if so, return it.  If it isn't
        unique, return a tuple of the matches.  Otherwise return None.
        '''
        assert isinstance(name, str)
        d, n = defaultdict(list), len(name)
        for i in Waveform._names:
            if i == "unknown":
                continue
            d[i[:len(name)]] += [i]
        if name in d:
            if len(d[name]) == 1:
                return d[name][0]
            else:
                return tuple(d[name])
        return None
    # Attributes
    def _get_ampl(self):
        return self._ampl
    def _set_ampl(self, ampl):
        self._ampl = float(ampl)
        if self._ampl <= 0:
            raise ValueError("ampl must be > 0")
    doc = dedent('''
        Setting the amplitude scales all of the points of the waveform
        by this value. [1]
    ''')
    ampl = property(_get_ampl, _set_ampl, None, doc)
    def _get_data(self):
        return self._data.copy()
    doc = dedent('''
        Returns the raw data representing one period of the waveform.
        This is a read-only attribute.
    ''')
    data = property(_get_data, None, None, doc)
    def _get_pclip(self):
        return self._pclip
    def _set_pclip(self, pclip):
        self._pclip = float(pclip)
        if not (0 <= self._pclip <= 1):
            raise ValueError("pclip must be in [0, 1]")
    doc = dedent('''
        Clips the upper portion of the waveform at a specified fraction
        of the "positive" amplitude.  See the discussion on clipping in
        the documentation PDF.  [1]
    ''')
    pclip = property(_get_pclip, _set_pclip, None, doc)
    def _get_nclip(self):
        return self._nclip
    def _set_nclip(self, nclip):
        self._nclip = float(nclip)
        if not (0 <= self._nclip <= 1):
            raise ValueError("nclip must be in [0, 1]")
    doc = dedent('''
        Clips the lower portion of the waveform at a specified fraction
        of the "negative" amplitude.  See the discussion on clipping in
        the documentation PDF.  [1]
    ''')
    nclip = property(_get_nclip, _set_nclip, None, doc)
    def _get_dc(self):
        return self._dc
    def _set_dc(self, dc):
        self._dc = float(dc)
    doc = dedent('''
        Adds a constant to each point of the waveform.  (The name comes
        from an electrical signal having a DC offset.) [0]
    ''')
    dc = property(_get_dc, _set_dc, None, doc)
    def _get_duty(self):
        return self._duty
    def _set_duty(self, duty):
        if not (0 <= float(duty) <= 1):
            raise ValueError("duty must be in [0, 1]")
        self._duty = float(duty)
        if self._name != "unknown":
            self._make()
    doc = dedent('''
        Duty cycle for square waves and pulses; this is the fraction of
        the period that the square wave is positive or the pulse is
        nonzero. [0.5]
    ''')
    duty = property(_get_duty, _set_duty, None, doc)
    def _get_kind(self):
        return self._kind
    def _set_kind(self, kind):
        if not isinstance(kind, (str, int, float)):
            raise ValueError("kind must be a string or number")
        self._kind = kind
    doc = dedent('''
        Sets the type of interpolation to use (see the documentation
        for scipy.interpolate.interp1d for allowed values).  This
        attribute is only needed for resampling.  ["linear"]
    ''')
    kind = property(_get_kind, _set_kind, None, doc)
    def _get_gates(self):
        return self._gates
    def _set_gates(self, gates):
        '''gates must be an iterable of pairs of numbers.
        '''
        ve = ValueError("gates must be an iterable of pairs of numbers")
        if not gates:
            self._gates = None
            return
        elif not isinstance(gates, Iterable):
            raise ve
        # Check each pair of numbers
        try:
            for a, b in gates:
                if not (0 <= a <= 1):
                    msg = "%s is invalid gate number" % a
                    raise RuntimeError()
                if not (0 <= b <= 1):
                    msg = "%s is invalid gate number" % b
                    raise RuntimeError()
                if a > b:
                    msg = "First gate number must be <= second number"
                    raise RuntimeError()
        except ValueError:
            raise ve
        except RuntimeError:
            raise ValueError(msg)
        self._gates = gates
    doc = dedent('''
        Is an iterable of pairs of numbers (a, b) where both a and b
        must be in [0, 1] and a <= b.  The waveform's points between
        x = a and x = b are set to zero.  The comparisons are made
        depending on the settings of the lge and rle attributes.
        [None]
    ''')
    gates = property(_get_gates, _set_gates, None, doc)
    def _get_rle(self):
        return self._rle
    def _set_rle(self, rle):
        '''rle is a Boolean.  If it is True, then the gating
        comparison for the right-hand portion is <=; otherwise, it is
        <.
        '''
        self._rle = True if rle else False
        return self._rle
    doc = dedent('''
        A Boolean used in gating.  If True, the comparison used
        for the left-hand index is <=; otherwise, the comparison
        is <.  [True]
    ''')
    rle = property(_get_rle, _set_rle, None, doc)
    def _get_lge(self):
        return self._lge
    def _set_lge(self, lge):
        '''lge is a Boolean.  If it is True, then the gating
        comparison for the left-hand portion is >=; otherwise, it is
        >.
        '''
        self._lge = True if lge else False
        return self._lge
    doc = dedent('''
        A Boolean used in gating.  If True, the comparison
        used for the left-hand index is >=; otherwise, the
        comparison is >.  [True]
    ''')
    lge = property(_get_lge, _set_lge, None, doc)
    def _get_ndig(self):
        return self._ndig
    def _set_ndig(self, ndig):
        if int(ndig) < 1:
            raise ValueError("ndig must be integer > 0")
        self._ndig = int(ndig)
    doc = dedent('''
        The number of significant figures to use when
        converting the data array to a string via str()
        or repr().  [3]
    ''')
    ndig = property(_get_ndig, _set_ndig, None, doc)
    def _get_size(self):
        assert self._size == len(self._data)
        return self._size
    def _set_size(self, size):
        n = int(size)
        if n < 2:
            raise ValueError("size must be > 2")
        if n != self._size and self._name == "unknown":
            self._resample(n)
            self._size = n
        else:
            self._size = n
            self._make()
    doc = dedent('''
        The number of points in the waveform.  If you set
        this to a new value, the waveform is regenerated
        if it is not of the type "unknown"; for the latter
        case, it is done by using scipy's interp1d method
        (thus, you need to have scipy installed).
    ''')
    size = property(_get_size, _set_size, None, doc)
    def _get_x(self):
        return self._x.copy()
    doc = dedent('''
        Returns a numpy array that represents the abscissas
        of the stored waveform (remember, the stored waveform
        represents one period).  Each value will be in the
        half-open interval [0, 1).
    ''')
    x = property(_get_x, None, None, doc)
    def _get_y(self):
        return self._data.copy()
    doc = dedent('''
        Returns a numpy array that represents the ordinates
        of the stored waveform (remember, the stored waveform
        represents one period).
    ''')
    y = property(_get_y, None, None, doc)
    def _get_zero(self):
        return self._zero
    def _set_zero(self, zero):
        '''zero must either be None or a tuple of numbers.  If a
        tuple, the first number must be negative or zero and the
        second number must be 0 or positive.
        '''
        if not zero:
            self._zero = None
        else:
            try:
                n, p = [float(i) for i in zero]
            except Exception:
                msg = "zero argument must be a tuple of numbers"
                raise ValueError(msg)
            if n and n > 0:
                msg = ("First element of zero tuple must be 0 or a "
                       "negative number")
                raise ValueError(msg)
            if p and p < 0:
                msg = ("Second element of zero tuple must be 0 or a "
                       "positive number")
                raise ValueError(msg)
            self._zero = (n, p)
        self._data = self._adjust_zero(self._data)
    doc = dedent('''
        Is a tuple (-a, b) such that negative numbers between
        -a and 0 are set to zero; positive numbers between 0 and
        b are set to zero.  This controls roundoff error problems.
        Can also be None if you do not want these changes to be
        made. [(-1e-15, 1e-15)]
    ''')
    zero = property(_get_zero, _set_zero, None, doc)

    def _get_max(self):
       pass 

    del doc
if 1:   # Plot some examples (needs matplotlib)
    def PlotExamples():
        if len(sys.argv) > 1 and sys.argv[1] == "test":
            RunSelftests()
        # Make bitmaps of the various waveforms that can be created, along
        # with some manipulations.
        names = ("dc", "sine", "cosine", "square", "triangle", "pulse",
                "ramp", "halfsine", "semicircle", "noise")
        n, dpi, pt, nl = 100, 75, ".-", "\n"
        filename = "pictures/waveform_%s.png"
        for name in names:
            w = Waveform(name, n)
            x, y = w.xy()
            clf()
            plot(x, y, pt)
            title("Waveform(%s, %d)" % (name, n))
            grid()
            savefig(filename % name, dpi=dpi)
            print(name, end=" ")
        # Demonstrate some features
        #---------------------------------------------------------------
        # Addition with a constant
        w, c, name = Waveform("sin", n), 1, "const_addition"
        x, y = (w + c).xy()
        clf()
        plot(x, y, pt)
        title("Waveform(%s, %d) + %s" % ("sin", n, c))
        grid()
        savefig(filename % name, dpi=dpi)
        print(name, end=" ")
        #---------------------------------------------------------------
        # Addition of two waveforms
        w, name = Waveform("sin", n), "add_2_waveforms"
        w1 = Waveform("triangle", n)
        x, y = (w + w1).xy()
        clf()
        plot(x, y, pt)
        title("Sine plus triangle")
        grid()
        savefig(filename % name, dpi=dpi)
        print(name, end=" ")
        #---------------------------------------------------------------
        # Subtraction of two waveforms
        w, name = Waveform("sin", n), "subtract_2_waveforms"
        w1 = Waveform("triangle", n)
        x, y = (w - w1).xy()
        clf()
        plot(x, y, pt)
        title("Sine minus triangle")
        grid()
        savefig(filename % name, dpi=dpi)
        print(name, end=" ")
        #---------------------------------------------------------------
        # Modulation by multiplication
        w, name = Waveform("sin", n), "modulation"
        w = Waveform(w(10))
        w1 = Waveform("sin", n)
        w1.xfm(abs)
        x, y = (w*w1).xy()
        clf()
        plot(x, y)
        title("Sine modulated by abs(sine)")
        grid()
        savefig(filename % name, dpi=dpi)
        print(name, end=" ")
        #---------------------------------------------------------------
        # Clipping
        w, name = Waveform("sin", n), "clipping"
        w.pclip = 0.9
        w.nclip = 0.5
        x, y = w.xy()
        clf()
        plot(x, y, pt)
        title("Clipped sine:  pclip = %s, nclip = %s" % (w.pclip, w.nclip))
        grid()
        ylim(-1, 1)
        savefig(filename % name, dpi=dpi)
        print(name, end=" ")
        #---------------------------------------------------------------
        # Gated
        w, name = Waveform("sin", n), "gated"
        w.gates = [(0.2, 0.35)]  # Zero between 0.2 and 0.35
        x, y = w.xy()
        clf()
        plot(x, y, pt)
        title("Gated sine:  gates = %s" % _sig(w.gates))
        grid()
        ylim(-1, 1)
        savefig(filename % name, dpi=dpi)
        print(name, end=" ")
        #---------------------------------------------------------------
        # Composite waveform:  SCR
        w, name = Waveform("halfsine", n), "scr"
        w.gates = [(0, 0.25)]
        x, y = (w - w).xy(2)
        clf()
        plot(x, y, pt)
        title("Simulated SCR Waveform")
        grid()
        savefig(filename % name, dpi=dpi)
        print(name, end=" ")
        #---------------------------------------------------------------
        # Composite waveform:  trapezoid
        name = "trapezoid"
        w1 = Waveform("ramp", 100)
        w2 = Waveform("dc", 2*100) + 1
        w3 = -Waveform("ramp", 3*100) + 1
        w4 = Waveform("dc", 100)
        w = w1 + w2 + w3 + w4
        x, y = (w - w).xy()
        clf()
        plot(x, y)
        title("Trapezoidal Waveform")
        grid()
        a = 1.05
        ylim(-a, a)
        savefig(filename % name, dpi=dpi)
        print(name, end=" ")
        #---------------------------------------------------------------
        # Composite waveform:  trapezoid
        name = "staircase"
        n, steps = 20, 8
        w = Waveform("dc", n)
        for i in range(1, steps + 1):
            u = Waveform("dc", n)
            u.dc = i
            w += u
        w.normalize()
        x, y = w.xy()
        clf()
        plot(x, y)
        title("Staircase Waveform")
        grid()
        a = 0.05
        ylim(-a, 1 + a)
        savefig(filename % name, dpi=dpi)
        print(name, end=" ")
        #---------------------------------------------------------------
        # Composite waveform:  pulse train
        name = "pulse_train"
        n, num_pulses, duty = 100, 5, 0.1
        w = Waveform("pulse", n)
        w.duty = duty
        w1 = Waveform(w)
        for i in range(num_pulses - 1):
            w += w1
        x, y = w.xy()
        clf()
        plot(x, y)
        title("%d Pulses (duty cycle = %s" % (num_pulses, _sig(duty, 1)))
        grid()
        a = 0.05
        ylim(-a, 1 + a)
        savefig(filename % name, dpi=dpi)
        print(name, end=" ")
        #---------------------------------------------------------------
        # "MW" waveform (two sine humps)
        w, name = Waveform("sin", n), "mw"
        w.xfm(abs)
        x, y = (w - w).xy()
        clf()
        plot(x, y)
        title("\"MW\" Waveform (two sine humps)")
        grid()
        savefig(filename % name, dpi=dpi)
        print(name, end=" ")
if 1:   # Other routines
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def AsciiPlot(waveform):
        lines, columns = GetScreen()    
        w = Waveform(waveform)  # Get a copy
        # Make the size one less than the number of lines so it fits on the screen
        w.size = lines - 1
        # Get maximum and minimum y values and pick the biggest in absolute value
        y = w.y
        ybig = max(abs(max(y)), abs(min(y)))
        # See if we should print the y = 0 axis (i.e., it's "on screen")
        zero = False
        if not max(y) or not min(y) or max(y)*min(y) < 0:
            zero = True
        # Scale y by dividing each element by ybig
        y /= ybig
        # Scale y by columns//2
        y *= columns//2
        # Now print the points 
        for i in range(w.size):
            
        breakpoint() #xx

if __name__ == "__main__":  
    w = Waveform("sine", 100)
    AsciiPlot(w)
