'''
TODO:
    * Test sum attribute
    * Consider getting rid of Complex and importing flt/cpx
        * This could mean Matrices container is obsolete and can be
          removed.
    * Move ParseComplex to f.py?
        * Should it also support the iy+x and yi+x forms?
Matrix module (python 3 only)
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2019 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <math> Matrix module.  This module is a derivative work of the 3.0.0
    # version of pymatrix, gotten on 15 Jul 2019 from
    # https://github.com/dmulholl/pymatrix.git.
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Standard imports
    from cmath import sqrt as csqrt
    from collections import OrderedDict
    from collections.abc import Iterable
    from decimal import Decimal, localcontext
    from fractions import Fraction
    from functools import reduce, partial
    from itertools import zip_longest, starmap
    from os import environ
    from pdb import set_trace as xx
    import locale
    import math
    import operator
    import random
    import re
    import sys
    import textwrap
if 1:   # Custom imports
    # You can decide here whether you want this module to support
    # mpmath, the python uncertainties library, or sympy.
    # Alternately, you can define the environment variables
    # MATRIX_MPMATH, MATRIX_UNCERTAINTIES, or MATRIX_SYMPY to have these
    # libraries imported if you don't hard-code the import.
    get_mpmath = "MATRIX_MPMATH" in environ
    get_uncertainties = "MATRIX_UNCERTAINTIES" in environ
    get_sympy = "MATRIX_SYMPY" in environ
    have_mpmath = False
    have_unc = False
    have_sympy = False
    if 1 or get_mpmath:
        try:
            import mpmath
            have_mpmath = True
        except ImportError:
            pass
    if 1 or get_uncertainties:
        try:
            from uncertainties import ufloat, UFloat, ufloat_fromstr
            have_unc = True
        except ImportError:
            pass
    if 0 or get_sympy:
        try:
            import sympy
            have_sympy = True
        except ImportError:
            pass
    from pdb import set_trace as xx
    if 0:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    __version__ = "10Jun2021"
    __all__ = '''
        Complex cross dot Flatten have_mpmath have_sympy have_unc
        Matrices Matrix matrix MatrixContext random_matrix RoundOff
        vector'''.split()
    ii = isinstance
class ParseComplex(object):
    '''Parses complex numbers in the ways humans like to write them.
    Instantiate the object, then call it with the string to parse; the
    real and imaginary parts are returned as a tuple.  You can pass in a
    number type to the constructor (you can also use fractions.Fraction)
    and the returned tuple will be composed of that type of number.
    '''
    _cre = r'''
        %s                          # Match at beginning
        ([+-])%s                    # Optional leading sign
        %s                          # Placeholder for imaginary unit
        (\.\d+|\d+\.?|\d+\.\d+)     # Required digits and opt. decimal point
        (e[+-]?\d+)?                # Optional exponent
        %s                          # Match at end
    '''
    # Pure imaginary, xi or ix
    _I1 = _cre % ("^", "?", "", "[ij]$")
    _I2 = _cre % ("^", "?", "[ij]", "$")
    # Reals
    _R = _cre % ("^", "?", "", "$")
    # Complex number:  x+iy
    _C1 = (_cre % ("^", "?", "", "")) + (_cre % ("", "", "", "[ij]$"))
    # Complex number:  x+yi
    _C2 = (_cre % ("^", "?", "", "")) + (_cre % ("", "", "[ij]", "$"))
    # Complex number:  iy+x
    _C3 = (_cre % ("^", "?", "[ij]", "")) + (_cre % ("", "?", "", "$"))
    # Complex number:  yi+x
    _C4 = (_cre % ("^", "?", "", "[ij]")) + (_cre % ("", "?", "", "$"))
    # Regular expressions (Flags:  I ignore case, X allow verbose)
    _imag1 = re.compile(_I1, re.X | re.I)
    _imag2 = re.compile(_I2, re.X | re.I)
    _real = re.compile(_R, re.X | re.I)
    _complex1 = re.compile(_C1, re.X | re.I)
    _complex2 = re.compile(_C2, re.X | re.I)
    _complex3 = re.compile(_C3, re.X | re.I)
    _complex4 = re.compile(_C4, re.X | re.I)
    def __init__(self, number_type=float):
        self.number_type = number_type
    def __call__(self, s):
        '''Return a tuple of two real numbers representing the real
        and imaginary parts of the complex number represented by
        s.  The allowed forms are (x and y are real numbers):
            Real:               x
            Pure imaginary      iy, yi
            Complex             x+iy, x+yi
        Space characters are allowed in the s (they are removed before
        processing).
        '''
        nt = self.number_type
        # Remove any whitespace, use lowercase, and change 'j' to 'i'
        s = re.sub(r"\s+", "", s).lower().replace("j", "i")
        # Imaginary unit is a special case
        if s in ("i", "+i"):
            return nt(0), nt(1)
        elif s in ("-i",):
            return nt(0), nt(-1)
        # "-i+3", "i+3" are special cases
        if s.startswith("i") or s.startswith("-i") or s.startswith("+i"):
            li = s.find("i")
            if s[li + 1] == "+" or s[li + 1] == "-":
                rp = nt(s[li + 1:])
                ip = -nt(1) if s[0] == "-" else nt(1)
                return rp, ip
        # "n+i", "n-i" are special cases
        if s.endswith("+i") or s.endswith("-i"):
            if s.endswith("+i"):
                return nt(s[:-2]), 1
            else:
                return nt(s[:-2]), -1
        # Parse with regexps
        mo = ParseComplex._imag1.match(s)
        if mo:
            return nt(0), self._one(mo.groups())
        mo = ParseComplex._imag2.match(s)
        if mo:
            return nt(0), self._one(mo.groups())
        mo = ParseComplex._real.match(s)
        if mo:
            return self._one(mo.groups()), nt(0)
        mo = ParseComplex._complex1.match(s)
        if mo:
            return self._two(mo.groups())
        mo = ParseComplex._complex2.match(s)
        if mo:
            return self._two(mo.groups())
        mo = ParseComplex._complex3.match(s)
        if mo:
            return self._two(mo.groups(), flip=True)
        mo = ParseComplex._complex4.match(s)
        if mo:
            return self._two(mo.groups(), flip=True)
        raise ValueError("'%s' is not a proper complex number" % s)
    def _one(self, groups):
        s = ""
        for i in range(3):
            if groups[i]:
                s += groups[i]
        return self.number_type(s)
    def _two(self, groups, flip=False):
        nt = self.number_type
        s1 = self._one(groups)
        s2 = ""
        for i in range(3, 6):
            if groups[i]:
                s2 += groups[i]
        if flip:
            return nt(s2), nt(s1)
        else:
            return nt(s1), nt(s2)
class Matrix:
    '''Matrix object supporting basic linear algebra operations.  Rows
        and columns are numbered starting from 0.  The preferred methods
        for accessing matrix elements are m[i, j] or m(i, j) where i is the
        row and j is the column.  A matrix with one row or column is a row
        or column vector and the indexing scheme lets you get at a vector's
        elements with one index.
 
        A number of methods use the following keyword arguments:
 
            c is used to indicate the operation is with respect to columns
            rather than rows.
    
            ip is used to indicate the operation should be done in_place.
            Most methods will return a new matrix object, but sometimes you
            want the operation done on the current instance, in which case
            set ip to True.
    '''
    # The _str class variable is used to switch the role of __str__()
    # and __repr__() when True.  This is useful in the debugger and
    # interactive python to see the elements of a matrix more easily.
    # Each Matrix instance can change this class variable through its s
    # attribute.
    _str = False
 
    # The Matrix.PC object is used to parse complex numbers.
    PC = ParseComplex()
 
    # If Matrix.use_Complex is True, complex numbers are instantiated in
    # getnum using the Complex class (see below), allowing customized
    # input and formatting of complex number forms.  If
    # Matrix.use_Complex is False, python's complex numbers are used.
    use_Complex = False
 
    # The SigFig class variable is used to define how many significant
    # figures to use when comparing matrix elements for equality.  If
    # not None, it will override any sigfig attributes of instances.
    SigFig = None
 
    def __init__(self, rows, cols, fill=0):
        if not ii(rows, int) or not ii(cols, int):
            raise TypeError("rows and cols must be integers")
        self._r = rows
        self._c = cols
        self._grid = [[fill for i in range(cols)] for j in range(rows)]
        self._numtype = None
        self._frozen = False
        self._sigfig = None
    def __add__(self, other): 
        '''Returns self + other; other can be a compatible matrix or
        scalar.
        '''
        if ii(other, Matrix):   # Matrix addition
            if self.r != other.r or self.c != other.c:
                raise TypeError('Cannot add matrices of different sizes')
            m = Matrix(self.r, self.c)
            with Flatten(self):
                M1 = self._grid
            with Flatten(other):
                M2 = other._grid
            m._grid = list(starmap(operator.add, zip(M1, M2)))
            m._nested()
            m._copy_attr(self)
            return m
        else:   # Scalar addition
            try:
                return self.map(lambda x: x + other)
            except Exception:
                raise TypeError("Cannot add {} to a matrix".format(type(other)))
    def __call__(self, i, j=None): 
        'Notationally equivalent to m[i] or m[i, j]'
        return self[i] if j is None else self[i, j]
    def __contains__(self, item): 
        'Returns True if item is in matrix'
        with Flatten(self): 
            return item in self._grid
    def __eq__(self, other): 
        'Return True if self and other are equal element-wise'
        return self.equals(other)
    def __floordiv__(self, other): 
        '''Allows self//other where other is a scalar.  Not defined if 
        other is a matrix.
        '''
        if ii(other, Matrix):
            raise TypeError("// not defined for two matrices")
        else:
            try:
                return self.map(lambda x: x//other)
            except Exception:
                raise TypeError(f"Cannot divide matrix by {type(other)}")
    def __getitem__(self, key):
        '''Enables self[i, j] indexing and assignment.  You can also use
        slices to get rows, columns, and submatrices:
            m[i:]       Returns row i as vector
            m[:j]       Returns column j as vector
            m[i:j]      Returns rows i through j inclusive as submatrix
            m[:i:j]     Returns columns i through j inclusive as submatrix
        Negative indexes are supported like in python sequences.
 
        self(i, j) works the same as self[i, j].
 
        If key is an integer and self is a vector, then self[key]
        returns the indicated component.  Otherwise, self[i] returns row
        i as a row vector.
        '''
        if ii(key, (tuple, list)):
            row, col = key
            return self._grid[row][col]
        elif ii(key, slice):
            i, j, k = key.start, key.stop, key.step
            # Check that only allowed slice forms are present
            if not ((i is not None and j is None and k is None) or
                    (i is None and j is not None and k is None) or
                    (i is not None and j is not None and k is None) or
                    (i is None and j is not None and k is not None)):
                raise ValueError("Slice '{}' is invalid".format(key))
            if j is None and k is None:     # [i:]
                # Return row i
                nr = self.r 
                i = i + nr if i < 0 else i
                if not (0 <= i < nr):
                    raise ValueError("index must be between 0 and "
                                     "{}".format(nr - 1))
                return self.row(i)
            elif i is None and k is None:   # [:j]
                # Return column j
                nc = self.c
                j = j + nc if j < 0 else j
                if not (0 <= j < nc):
                    raise ValueError("index must be between 0 and "
                                     "{}".format(nc - 1))
                return self.col(j)
            elif k is None:                 # [i:j]
                # Return rows i to j
                nr = self.r
                i = i + nr if i < 0 else i
                j = j + nr if j < 0 else j
                if not (0 <= i < nr):
                    raise ValueError("First index must be between 0 and "
                                     "{}".format(nr - 1))
                if not (i <= j < nr):
                    raise ValueError("Second index must be between 0 and "
                                     "{}".format(nr - 1))
                if i >= j:
                    raise ValueError("First index must be < second")
                m = matrix(self._grid[i:j+1])
                m._copy_attr(self)
                return m
            elif i is None:                 # [:j:k]
                # Return columns j to k
                nc = self.c 
                j = j + nc if j < 0 else j
                k = k + nc if k < 0 else k
                if not (0 <= j < nc):
                    raise ValueError("index must be between 0 and "
                                     "{}".format(nc))
                if not (0 <= k < nc):
                    raise ValueError("index must be between 0 and "
                                     "{}".format(nc))
                if j >= k:
                    raise ValueError("First index must be < second")
                m = matrix(self.t._grid[j:k+1]).t
                m._copy_attr(self)
                return m
            else:
                raise ValueError("Slice '{}' is invalid".format(key))
        elif ii(key, int):
            if self.is_vector:
                with Flatten(self): 
                    return self._grid[key]   # Return vector component
            else:
                # Return matrix row as a row vector
                m = matrix([self._grid[key]])
                m._copy_attr(self)
                return m
        else:
            raise TypeError("key is an invalid type")
    def __hash__(self):
        '''A matrix is inherently a mutable container, but we also want
        it to be stored in other containers, so we'll define the hash
        value to be the id of the instance.
        '''
        return hash(id(self))
    def __iter__(self): 
        'Iteration: for row, col, element in self'
        for row in range(self.r):
            for col in range(self.c):
                yield row, col, self[row, col]
    def __mul__(self, other): 
        '''Multiply by another matrix or a scalar.  If the result is a 
        1 by 1 matrix, the number is returned instead of the matrix.
        '''
        if ii(other, Matrix):
            if self.c != other.r:
                raise TypeError('Incompatible sizes for multiplication')
            m = Matrix(self.r, other.c)
            for row, col, x in m:
                for r, c in zip(self.row(row), other.col(col)):
                    m[row, col] += r[2]*c[2]
            return m[0, 0] if m.size == (1, 1) else m
        else:
            return self.map(lambda x: x*other)
    def __neg__(self): 
        'Return a new matrix with all elements negated'
        return self.map(lambda x: -x)
    def __pos__(self): 
        'Returns a copy of +self'
        return self.map(lambda x: +x)
    def __pow__(self, other): 
        '''Returns self**other.  other can be any integer; if 0, the
        identity matrix is returned.  If other is negative, the inverse
        matrix is raised to the abs(other) power.
        '''
        if not ii(other, int):
            raise TypeError("Only integer powers are supported")
        if not self.is_square:
            raise TypeError("The matrix must be square to raise to a power")
        if not other:
            return self.identity(self.r)
        else:
            m = self.copy if other > 0 else self.i
            n = m.copy
            for i in range(abs(other) - 1):
                m = m*n
            m._copy_attr(self)
            return m
    def __radd__(self, other): 
        'Allows for scalar + matrix'
        return self + other
    def __repr__(self):
        return self._string() if self.s else self._repr()
    def __rmul__(self, other): 
        'Allows for scalar*matrix'
        return self*other
    def __rsub__(self, other): 
        'Allows for scalar - matrix'
        return -self + other
    def __rtruediv__(self, other): 
        'Return other/matrix = other*matrix.i'
        return other*self.i
    def __setitem__(self, key, value):
        '''Set the indicated matrix element to value.  You can address
        row i and column j by indexing as [i, j] or (i, j).
 
        If key is an integer, you can replace the indicated row with a
        list or vector as long as the number of elements in value is
        equal to the number of columns.  
  
        If key is an integer and self is a vector, the indicated element
        will be changed.
        '''
        self._check_frozen()
        if ii(key, (tuple, list)):  # Set a single element
            nr, nc = self.r, self.c
            row, col = key
            row = row + nr if row < 0 else row
            col = col + nc if col < 0 else col
            if not (0 <= row < nr):
                raise ValueError("row must be 0 to {}".format(nr - 1))
            if not (0 <= col < nc):
                raise ValueError("col must be 0 to {}".format(nc - 1))
            self._grid[row][col] = value
        elif ii(key, int):
            # This is either to insert a new row or change the element
            # of a vector.
            if self.is_vector:
                key = key + self.len if key < 0 else key
                if 0 <= key < self.len:
                    with Flatten(self): 
                        self._grid[key] = value
                else:
                    raise ValueError("Vector index of {} is bad".format(key))
            else:
                msg = "value must be a {{}} with {} elements".format(self.c)
                if ii(value, Matrix):
                    if not value.is_vector and value.len != self.c :
                        raise TypeError(msg.format("vector"))
                    v = value.l
                else:
                    try:
                        v = list(value)
                        if len(v) != self.c:
                            raise Exception()
                    except Exception:
                        raise TypeError(msg.format("list"))
                self._grid[key] = v
        else:
            raise TypeError("Need tuple or int for key for assignment")
    def __str__(self):
        return self._repr() if self.s else self._string()
    def __sub__(self, other): 
        '''Subtract a matrix or scalar from the current matrix and return
        the result.
        '''
        if ii(other, Matrix):
            # Matrix subtraction
            if self.r != other.r or self.c != other.c:
                raise TypeError("Cannot subtract matrices of different sizes")
            m = Matrix(self.r, self.c)
            return -other + self
        else:
            # Assume it's a number to subtract from each element
            try:
                return self.map(lambda x: x - other)
            except Exception:
                raise TypeError("Cannot subtract {} from a "
                                "matrix".format(type(other)))
    def __truediv__(self, other): 
        '''Allows self/other where other is a scalar or a matrix.  If 
        self and other are square matrices of the same size, returns
        self*other.i.
        '''
        if ii(other, Matrix):
            # Must have self and other square and of the same size
            if not self.is_square or not other.is_square:
                raise TypeError("Self and other must be square matrices")
            if self.r != other.r:
                raise TypeError("Self and other must be the same size")
            return self*other.i
        else:
            try:
                return self.map(lambda x: x/other)
            except Exception:
                raise TypeError("Cannot divide matrix by {}".format(type(other)))
    def add(self, n, m, constant=1, c=False): 
        '''In-place row or column operation.  Adds constant times row m
        to row n or constant times column m to column n.
        '''
        self._check_frozen()
        if c:
            n = n + self.c if n < 0 else n
            m = m + self.c if m < 0 else m
            for i in range(self.r):
                self[i, n] += constant*self[i, m]
        else:
            n = n + self.r if n < 0 else n
            m = m + self.r if m < 0 else m
            self._grid[n] = [i + j for i, j in 
                zip([i*constant for i in self._grid[m]], self._grid[n])]
    def cholesky(self, ip=False):
        '''Cholesky decomposition into a lower triangular matrix.  If ip
        is True, perform the decomposition in-place; otherwise, return
        the lower triangular matrix.  self must be Hermitian and
        positive-definite (i.e., z.t*M*z must be > 0 for every nonzero
        column vector z where z ϵ ℂ^n).  All of a matrix's eigenvalues
        are positive if and only if the matrix is positive-definite.
        '''
        # From http://rosettacode.org/wiki/Cholesky_decomposition
        L = [[0]*self.r for _ in range(self.r)]
        try:
            for i, (Ai, Li) in enumerate(zip(self.nl, L)):
                for j, Lj in enumerate(L[:i+1]):
                    s = sum(Li[k]*Lj[k] for k in range(j))
                    # Note we must use math.sqrt because x**0.5 can
                    # return a complex result.
                    try:
                        Li[j] = (math.sqrt(Ai[i] - s) if (i == j) else
                                 (1/Lj[j]*(Ai[j] - s)))
                    except TypeError as e:
                        Li[j] = (csqrt(Ai[i] - s) if (i == j) else
                                 (1/Lj[j]*(Ai[j] - s)))
        except (ValueError, ZeroDivisionError):
            raise TypeError("Matrix not positive-definite or Hermitian")
        m = matrix(L)
        if not ip:
            m._copy_attr(self)
            return m
        self._grid = m._grid
    def chop(self, tol=100*sys.float_info.epsilon): 
        '''Remove small floating point matrix elements and replace them
        with zero.  If a real or imaginary component of a matrix element
        has an absolute value less than or equal to tol, replace that
        component with zero.  Other things like integers or Fraction
        instances will be left alone, regardless of their magnitude.
 
        Note this method works in-place on the current matrix.
        '''
        f = lambda x: 0 if abs(x) <= tol else x
        def ch(x):
            if ii(x, complex):
                return complex(f(x.real), f(x.imag))
            elif ii(x, Complex):
                return Complex(f(x.real), f(x.imag))
            elif have_mpmath and ii(x, mpmath.mpc):
                return mpmath.mpc(f(x.real), f(x.imag))
            elif ii(x, float):
                return f(x)
            elif have_mpmath and ii(x, mpmath.mpf):
                return f(x)
            elif have_unc and ii(x, UFloat):
                raise TypeError("Can't chop an uncertain number")
            elif ii(x, Decimal):
                return f(x)
            else:
                return x
        with Flatten(self):
            self._grid = [ch(i) for i in self._grid]
    def cofactor(self, row, col): 
        '''Return the cofactor, which is the determinant of the matrix with
        the indicated row and column removed, scaled by (-1)**(row + col).
        '''
        row = row + self.r if row < 0 else row
        col = col + self.c if col < 0 else col
        # Note the minor is the determinant
        return pow(-1, row + col)*self.minor(row, col)
    def col(self, *n): 
        'Returns the indicated columns as a new matrix'
        for i in n:
            if i < 0:
                k = self.c + i
                if not (0 <= k < self.c):
                    raise ValueError("n must be between -1 and {}".format(
                        -self.c))
            else:
                if not (0 <= i < self.c):
                    raise ValueError("n must be between 0 and {}".format(
                        self.c - 1))
        return self.t.row(*n).t
    def decorate(self, decorations):
        '''Return a matrix of strings that contain the results of
        applying the elements of decorations to the elements of the self
        matrix.  
 
        decorations is a sequence of 2-tuples (a, b).  a can be a type,
        number, or string and when a matrix element matches a (using ==),
        b is substituted for it.  If b is callable as a function,
        b(element) is substituted.
        
        Example:  suppose we have m which is a sparse 4x4 matrix:
            0.0 0.0 1.0 0.0
            0.0 0.0 0.0 2.0
            0.0 0.0 0.0 0.0
            0.0 0.0 0.0 0.0
        This is hard to read because of all the 0 symbols.  We can
        change the 0.0 elements to '.' and convert the floats to
        integers to make things easier to read.  To do this, set
        d = [(0, "."), (float, lambda x: int(x))] and call
        print(m.decorate(d)) to get
            . . 1 .
            . . . 2
            . . . .
            . . . .
        which shows the nonzero elements more clearly.
        '''
        m = self.copy
        m._flatten()
        L = m._grid
        for i, item in enumerate(L):
            for key, value in decorations:
                if item == key:
                    L[i] = value    # Substitution
                    break
                # See if it's of this type
                try:
                    if ii(item, key):
                        if callable(value):
                            L[i] = value(item)  # Call a function
                        else:
                            L[i] = value        # Substitution
                    break
                except TypeError:
                    # key probably isn't a type
                    pass
        m._grid = L
        m._nested()
        return m
    def delete(self, n, c=False):
        '''Delete the indicated row or column from the current matrix and
        return the row or column as a vector.
 
        Example:  for the matrix 
            1 2
            3 4
        calling delete(0) results in the matrix becoming the row vector 
            3 4
        and returns the row vector 
            1 2
        Calling delete(0, c=True) returns the column vector
            1
            3
        and the matrix becomes the column vector
            2
            4
        '''
        self._check_frozen()
        if c:
            n = n + self.c if n < 0 else n
            if self.is_col_vector:
                raise TypeError("Can't remove a column from a column vector")
            if not (0 <= n < self.c):
                raise ValueError("n must be between 0 and {}".format(self.c - 1))
            # Used delete_row() on the transpose
            m = self.t
            cv = m._grid.pop(n)     # cv is a list
            m._r -= 1
            self._grid = m.t._grid  # Put the reduced matrix back
            cv = vector(*cv).t      # Convert it to a column vector
            self._c -= 1
            cv._copy_attr(self)
            return cv
        else:
            n = n + self.r if n < 0 else n
            if self.is_row_vector:
                raise TypeError("Can't remove a row from a row vector")
            if not (0 <= n < self.r):
                raise ValueError("n must be between 0 and {}".format(self.r - 1))
            r = self._grid.pop(n)
            self._r -= 1
            v = vector(*r)
            v._copy_attr(self)
            return v
    def equals(self, other, tol=None): 
        '''Returns True if self and other are identically-sized matrices
        and their corresponding elements agree to within tol.  The test
        is abs(i - j) <= tol where i and j are matrix elements, so it
        also works on complex matrices.  If tol is omitted, perform an
        equality check (==) on corresponding elements instead.
 
        If the sigfig attribute of self or other is not None, then it is
        used to compare the corresponding matrix elements to the
        indicated significant number of figures by rounding off; the
        smaller of the two sigfig values is used.  If Matrix.sigfig is
        not None, then it is used irrespective of the instance.sigfig
        values.
        '''
        if not ii(other, Matrix):
            raise TypeError("other must be a Matrix instance")
        if self.r != other.r or self.c != other.c:
            return False
        s, o = self.l, other.l
        if tol is not None:
            t = [abs(i - j) <= tol for i, j in zip(s, o)]
            return all(t)
        # Get the value of sigfig to use
        sigfig = self._get_sigfig(other)
        if sigfig is not None:
            f = lambda x: RoundOff(x, digits=sigfig)
            return all([f(i) == f(j) for i, j in zip(s, o)])
        else:
            # Simple equality test
            return all([i == j for i, j in zip(s, o)])
    def find(self, *items, tol=None, reltol=None): 
        '''Returns a list of (row, col) tuples indicating where the items
        are found in the matrix.  If tol is not None, an item's index is
        returned if abs(item - element) <= tol.  The same is true for
        reltol, except the comparison is 
            abs((item - element)/element) <= reltol
        if element is nonzero or 
            abs((item - element)/item) <= reltol
        if element is zero.
 
        All items will be checked and all locations of elements that match
        any of the items will be returned.
 
        Note:  the function RoundOff is used to fix annoying problems with
        floating point numbers.  For example, if an element is 1.01 and you
        use a tolerance of 0.01, the difference from 1 may be calculated as 
        0.010000000000000009.  The RoundOff function rounds this to 12
        figures by default, so most comparisons should work as expected (12
        digits was chosen because it is beyond the significance of most
        physical measurements).
        '''
        found = []
        if tol == None and reltol == None:
            for row, col, x in self:
                for item in items:
                    if x == item:
                        found.append([row, col])
        elif tol is not None:
            for row, col, x in self:
                for item in items:
                    t = RoundOff(abs(x - item))
                    if t <= tol:
                        found.append([row, col])
        else:
            for row, col, x in self:
                for item in items:
                    t = RoundOff(abs(x - item))
                    t = (RoundOff(abs(t/x)) if x else 
                         RoundOff(abs(t/item)) if item else 0)
                    if t <= reltol:
                        found.append([row, col])
        return found
    def float(self, ip=False):
        '''Return a new matrix with each element x converted to a float
        if the imaginary part of the element is zero.  If ip is True, do
        this in-place for the current matrix.
  
        Note:  this method differs from setting self.numtype=float
        because the conversion only happens if the element's imaginary
        part is zero.
        '''
        def Float(x):
            if ii(x, complex) and not x.imag:
                return x.real
            return x
        if ip:
            self._check_frozen()
        m = self if ip else self.copy
        m.map(Float, ip=True)
        return None if ip else m
    def insert(self, n, c=False, Vector=None, fill=0):
        '''Inserts a new row or column before the indicated row or
        column n, counting from top to bottom for rows and left to right
        for columns.  Set n to self.r to insert after the bottom row or
        self.c to insert after the rightmost column.  The new elements
        are filled with the value of fill.
 
        If Vector is not None, then the vector's values are inserted into
        the row or column.  The vector can be either a row or column vector
        as long as it has the correct number of elements for the target row
        or column.
 
        Examples:  for the matrix 
            1 2
            3 4
        calling insert(0) adds a new row of zeros before row 0 to give
            0 0
            1 2
            3 4
        Calling insert(2) results in 
            1 2
            3 4
            0 0
        Calling insert(2, c=True) results in 
            1 2 0
            3 4 0
        '''
        self._check_frozen()
        if c:
            concat = True if n == self.c else False
            n = n + self.c if n < 0 else n
            if not (0 <= n < self.c) and not concat:
                raise ValueError("n must be between 0 "
                                 "and {}".format(self.c - 1))
            if Vector is not None:
                if Vector.len != self.r:
                    raise TypeError("Vector must have {} elements".format(
                                    self.r))
                v = Vector if Vector.is_col_vector else Vector.t
            else:
                v = vector(self.r, c=True, fill=fill)
            # Operate on the transpose so we can use insert for rows
            m = self.t
            if concat:
                m.insert(self.c, c=False, Vector=v)
            else:
                m.insert(n, c=False, Vector=v)
            self._grid = m.t._grid
            self._c += 1
        else:
            concat = True if n == self.r else False
            n = n + self.r if n < 0 else n
            if not (0 <= n < self.r) and not concat:
                raise ValueError("n must be between 0 "
                                 "and {}".format(self.r - 1))
            if Vector is not None:
                if Vector.len != self.c:
                    raise TypeError("Vector must have {} elements".format(
                                    self.c))
                v = Vector if Vector.is_row_vector else Vector.t
            else:
                v = vector(self.c, fill=fill)
            if concat:
                self._grid.append(v._grid[0])
            else:
                self._grid.insert(n, v._grid[0])
            self._r += 1
    def int(self, ip=False):
        '''Return a new matrix with each element x converted to an integer
        if int(x) == x.  If ip is True, do this for the current matrix.
 
        Note:  this method differs from setting self.numtype=int because
        the conversion only happens if the matrix value and its integer
        value are equal.
        '''
        def Int(x):
            try:
               return int(x) if int(x) == x else x
            except TypeError:
                return x
        if ip:
            self._check_frozen()
        m = self if ip else self.copy
        m.map(lambda x:  Int(x) if Int(x) == x else x, ip=True)
        return None if ip else m
    def is_diagonal(self, tol=None): 
        '''Return True if the matrix is a diagonal matrix.  If tol is
        not None, then each off-diagonal element x must satisfy 
        abs(x) <= tol to return True.  If tol is None, then each
        off-diagonal element x must satisfy x == 0 to return True.
        '''
        f = (lambda x:  x != 0) if tol is None else (lambda x:  abs(x) > tol)
        m = self.lower(incl_diag=False)
        nonzero = any([f(i) for i in m.l])
        if nonzero:
            return False
        m = self.upper(incl_diag=False)
        nonzero = any([f(i) for i in m.l])
        return not nonzero
    def join(self, m, c=False):
        '''Join a matrix m to self.  If c is False, m and self must have
        the same number of rows and m is joined on the right side of
        self.  If c is True, m and self must have the same number of
        columns and m is joined on the bottom side of self.
        '''
        if not ii(m, Matrix):
            raise TypeError("m must be a Matrix instance")
        self._check_frozen()
        if c:
            if self.c != m.c:
                raise TypeError("m must have {} columns".format(self.c))
            M, m = self.t, m.t
            for i in range(self.c):
                M._grid[i].extend(m._grid[i])
            self._grid = M.t._grid
            self._r += m._r
        else:
            if self.r != m.r:
                raise TypeError("m must have {} rows".format(self.r))
            for i in range(self.r):
                self._grid[i].extend(m._grid[i])
            self._c += m._c
    def lower(self, ip=False, incl_diag=True, fill=0):
        '''Return the lower triangular matrix and include the diagonal
        if incl_diag is True.  The upper off-diagonal elements will be
        set to fill.  If ip is True, perform this operation on the current
        matrix and return None.
        '''
        if not self.is_square:
            raise TypeError("Matrix must be square")
        if ip:
            self._check_frozen()
        m = self if ip else self.copy
        for i in range(self.r):
            for j in range(self.c):
                if incl_diag:
                    if j > i:
                        m[i, j] = fill
                else:
                    if j >= i:
                        m[i, j] = fill
        return None if ip else m
    def map(self, func, n=None, c=False, ip=False):
        '''Returns a new matrix by applying the univariate function func to
        each element.  If in-place is True, do this for the current
        instance and return None.
 
        n and c restrict the operation, if present.  n can either be a
        number or a sequence of numbers.  If it's a number, it means to
        apply the map to row n.  If n is a sequence, it is applied to
        each of the indicated rows or columns.  If c is False, it means
        apply to a row; if it is True, apply to column n.  
        '''
        if ip:
            self._check_frozen()
        m = self.copy
        if n is None:
            # Whole matrix
            with Flatten(m): 
                m._grid = [func(i) for i in m._grid]
            if ip:
                self._grid = m._grid
            return None if ip else m
        elif ii(n, int):
            # Single row or column
            if not (0 <= n < self.c if c else self.r):
                raise ValueError("n must be between 0 and {}".format(
                        self.c if c else self.r))
            # Modify row or column n
            m = m.t if c else m
            m._grid[n] = [func(i) for i in m._grid[n]]
            m = m.t if c else m
            if ip:
                self._grid = m._grid
                return
            return m
        elif not ii(n, str) and ii(n, Iterable):
            # Multiple rows or columns
            for i in n:
                m.map(func, i, c=c, ip=ip)
            if ip:
                self._grid = m._grid
                return
            return m
        else:
            raise TypeError("n must be an integer or sequence")
    def minor(self, row, col):
        '''Returns the minor, which is the determinant of the matrix with
        the indicated row and column deleted.
        '''
        if not self.is_square:
            raise TypeError("Can only return a minor for a square matrix")
        m = self.copy
        m.delete(row)
        m.delete(col, c=True)
        return m.det
    def replace(self, n, vector, c=False):
        'Replace row or column n with the given vector'
        self._check_frozen()
        t = self.c if c else self.r
        n = n + t if n < 0 else n
        if not vector.is_vector:
            raise TypeError("vector must be a vector")
        if vector.len != t:
            raise TypeError("vector must have {} elements".format(t))
        if not (0 <= n < t):
            raise ValueError("n must be between 0 and {}".format(t - 1))
        if c:
            self.t._grid[n] = vector.l
        else:
            self._grid[n] = vector.l
    def resize(self, r, c, fill=0):
        '''Resize this matrix in-place to have r rows and c columns.  New
        elements will have the value fill.  If size is reduced, some
        elements may be lost.
        '''
        self._check_frozen()
        if not ii(r, int) and not ii(c, int):
            raise TypeError("r and c must be integers")
        if r < 1 or c < 1:
            raise ValueError("r and c must be > 0")
        # Flatten self._grid
        L = list(Matrix._Flatten(self._grid))
        # Get new length
        n, N = r*c, len(L)
        if N > n:
            L = L[:n]
        elif N < n:
            L.extend([fill]*(n - N))
        # Change type if needed
        if self.numtype is not None:
            L = [self.numtype(i) for i in L]
        # Convert self._grid to nested list
        self._grid = [list(i) for i in zip_longest(*([iter(L)]*c))]
        self._r, self._c = r, c
    def rotate(self, n=1, c=False, ip=False):
        '''Rotate n rows down (or n columns right if c is True).  If n
        is negative, then rows are rotated up and columns are rotated
        left.
         
        Examples:  If m is
            1 2 3
            4 5 6
            7 8 9
        then m.rotate() returns
            4 5 6
            1 2 3
            7 8 9
        and m.rotate(c=True) returns
            3 1 2
            6 4 5
            9 7 8
        '''
        if not n:
            return self if ip else self.copy
        n = -n  # Needed to get the correct direction
        N = self.c if c else self.r
        n = N + n if n < 0 else n
        n %= N
        assert(n >= 0)
        if not n:
            return self if ip else self.copy
        L = self.t.nl if c else self.nl
        for i in range(n):
            r = L.pop(0)
            L.append(r)
        # Reassemble
        if c:
            m = matrix(L)
            m._copy_attr(self)
            if ip:
                self._grid = m.t.nl
            else:
                return m.t
        else:
            if ip:
                self._grid = L
            else:
                m = self.copy
                m._grid = L
                return m
    def round(self, ip=False):
        '''If instance.sigfig or Matrix.SigFig are set, round the matrix
        elements to the indicated number of significant figures.  Note
        that Matrix.SigFig overrides instance.sigfig.  Otherwise, do
        nothing.  If ip is True, do in-place.
        '''
        sigfig = None
        if self.sigfig:
            sigfig = self.sigfig
            if Matrix.SigFig:
                sigfig = min(self.sigfig, Matrix.SigFig)
        if Matrix.SigFig:
            sigfig = Matrix.SigFig
        if sigfig:
            assert(sigfig > 0)
            f = partial(RoundOff, digits=sigfig)
            if ip:
                self.map(f, ip=True)
            else:
                return self.map(f)
        else:
            if not ip:
                return self.copy
    def row(self, *n):
        'Returns the indicated row(s) as a new matrix'
        # Validate n's components
        for i in n:
            if i < 0:
                k = self.r + i
                if not (0 <= k < self.r):
                    raise ValueError("n must be between -1 and {}".format(
                        -self.r))
            else:
                if not (0 <= i < self.r):
                    raise ValueError("n must be between 0 and {}".format(
                        self.r - 1))
        s = []
        for i in n:
            i = self.r + i if i < 0 else i
            s.append(self._grid[i])
        if len(n) == 1:
            m = vector(s[0])
        else:
            m = matrix(s)
        m._copy_attr(self)
        return m
    def scale(self, n, b, c=False): 
        'Multiply row or column n by the constant b'
        self._check_frozen()
        if c:
            n = n + self.c if n < 0 else n
            m = self.t
            m._grid[n] = [b*i for i in m._grid[n]]
            self._grid = m.t._grid
        else:
            n = n + self.r if n < 0 else n
            self._grid[n] = [b*i for i in self._grid[n]]
    def solve(self, b=None, numtype=None, aug=False): 
        '''Given a vector b, solve the equation m*x = b and return x as a
        vector of the same shape (row or column) as b.  If numtype is not
        None, then self and b are coerced to the indicated type before
        computation.  The returned vector will have the same attributes as
        self.
 
        For convenience, self can be an augmented matrix by setting aug
        to True.  Then self must be an n x (n+1) matrix where the last
        column is the b vector.
        '''
        if aug:
            if self.c != self.r + 1:
                raise TypeError("Improper augmented matrix")
            M = self.copy
            B = M.delete(self.c - 1, c=True)
            if numtype is not None:
                M.numtype = numtype
                B.numtype = numtype
            x = M.i*B
        else:
            if not b.is_vector:
                raise TypeError("b must be a vector")
            if numtype is not None:
                M, B = self.copy, b.copy
                M.numtype, B.numtype = numtype, numtype
                x = (M.i*B.t).t if B.is_row_vector else M.i*B
            else:
                x = (self.i*b.t).t if b.is_row_vector else self.i*b
        x._copy_attr(self)
        return x
    def swap(self, n, m, c=False): 
        'In-place swap of the two indicated rows or columns'
        self._check_frozen()
        if n == m:
            return
        if c:
            n = n + self.c if n < 0 else n
            m = m + self.c if m < 0 else m
            M = self.t
            M._grid[n], M._grid[m] = M._grid[m], M._grid[n]
            self._grid = M.t._grid 
        else:
            n = n + self.r if n < 0 else n
            m = m + self.r if m < 0 else m
            self._grid[n], self._grid[m] = self._grid[m], self._grid[n]
    def split(self, n, c=False):
        '''Returns two matrices; the first one will include the rows or
        columns from 0 to n; the second will be the remainder.  A ValueError
        exception will be raised if n indicates the last row or column, as
        None would have to be returned for the second matrix.  The original
        matrix is unchanged.
        '''
        R, C = self._r, self._c
        if not ii(n, int): 
            raise TypeError("n must be an integer")
        def row_split(M, n):
            if n < 0 or n >= M.r - 1:
                if M.is_row_vector:
                    raise TypeError("Can't split a row vector on rows")
                raise ValueError("n must be >= 0 and < {}".format(M.r - 1))
            m1, m2 = matrix(M._grid[:n + 1]), matrix(M._grid[n + 1:])
            m1._copy_attr(self)
            m2._copy_attr(self)
            return m1, m2
        if c:
            if n < 0 or n >= C - 1:
                if self.is_col_vector:
                    raise TypeError("Can't split a column vector on columns")
                raise ValueError("n must be >= 0 and < {}".format(c - 1))
            # Do column split by using row method on transpose
            m1, m2 = row_split(self.t, n)
            m1._copy_attr(self)
            m2._copy_attr(self)
            return m1.t, m2.t
        else:
            return row_split(self, n)
    def upper(self, ip=False, incl_diag=True, fill=0):
        '''Return the upper triangular matrix and include the diagonal
        if incl_diag is True.  The lower off-diagonal elements will be
        fill.  If ip is True, perform this operation on the current
        matrix and return None.
        '''
        if not self.is_square:
            raise TypeError("Matrix must be square")
        if ip:
            self._check_frozen()
        m = self if ip else self.copy
        for i in range(self.r):
            for j in range(self.c):
                if incl_diag:
                    if j < i:
                        m[i, j] = fill
                else:
                    if j <= i:
                        m[i, j] = fill
        return None if ip else m
    # ---------------------- Private methods ----------------------------
    def _check_frozen(self):
        if self.frozen:
            raise TypeError("Cannot modify a frozen matrix or vector")
    def _copy_attr(self, m):
        'Copy the attributes of the matrix m to self'
        if not ii(m, Matrix):
            raise TypeError("m must be a Matrix instance")
        self.numtype = m._numtype
        self.frozen = m._frozen
        self.sigfig = m._sigfig
    def _flatten(self):
        'Convert self._grid to a flat list'
        self._grid = Matrix._Flatten(self._grid)
    def _nested(self):
        'Convert self._grid to a nested list'
        if not ii(self._grid[0], list):
            self._grid = [list(i) for i in 
                         zip_longest(*([iter(self._grid)]*self.c))]
    def _get_sigfig(self, other=None):
        '''Return the sigfig value to use for a comparison.  If
        Matrix.SigFig is not None, return it.  Otherwise, return the
        smaller of self.sigfig and other.sigfig.
        '''
        if Matrix.SigFig is not None:
            if not ii(Matrix.SigFig, int):
                raise TypeError("Matrix.sigfig must be an integer")
            if Matrix.SigFig < 1:
                raise ValueError("Matrix.sigfig must be > 0")
            return Matrix.SigFig
        if other is None:
            return self._sigfig
        else:
            if self._sigfig is None:
                return other._sigfig
            else:
                if other._sigfig is None:
                    return self._sigfig
                else:
                    return min(self._sigfig, other._sigfig)
    def _get_type_dict(self):
        '''Return a dictionary whose keys are the string form of the 
        type() of an object.  The values are (symbol, description) where
        symbol is the string representing the type and description is 
        a short explanation.
        '''
        return OrderedDict((
            ('©', 'Complex'),
            ('ℂ', 'complex'),
            ('D', 'Decimal'),
            ('ℝ', 'Float'),
            ('ℚ', 'Fraction'),
            ('F', 'Function'),
            ('ℤ', 'Integer'),
            ('λ', 'lambda function'),
            (']', 'List'),
            ('𝕄', 'Matrix'),
            ('f', 'Method'),
            ('Λ', 'mpmath ivmpf'),
            ('∇', 'mpmath mpc'),
            ('Δ', 'mpmath mpf'),
            ('"', 'String'),
            ('𝕊', 'sympy object'),
            (')', 'Tuple'),
            ('±', 'Uncertainties variable'),
            ('?', 'Unknown'),
            ('𝕍', 'Vector')
            ))
    def _string(self):
        '''Return the string form of the matrix.  If self.digits is not
        zero, then floats, Decimals, complex, and Complex numbers will
        be rounded off to the indicated number of digits.  The returned
        string is formatted to print to the console compactly.
 
        Example:  with self.digits set to 2,
            str(matrix("2.817 3/4 Decimal('1.2345') 38.277-4.50911j"))
        will return 
            '2.8       3/4       1.2 (38-4.5j)'
 
        Warning:  Decimal() numbers with more digits than the platform's
        float will not be formatted correctly; it is recommended you not 
        use more than 12 digits.
        '''
        def Rnd(x):
            digits = (Matrix.SigFig if Matrix.SigFig is not None else
                      self._sigfig if self._sigfig is not None else None)
            if digits:
                if ii(x, (float, Decimal)):
                    return str(RoundOff(float(x), digits))
                elif ii(x, Complex):
                    # This is a bit of a hack to get self's sigdig
                    # setting to the Complex instance (but it works).
                    x.sigdig = digits
                    return str(x)
                elif ii(x, complex):
                    if Matrix.use_Complex:
                        return str(Complex(RoundOff(x, digits)))
                    return str(RoundOff(x, digits))
                else:
                    return str(x)
            else:
                if ii(x, complex) and Matrix.use_Complex:
                    return str(Complex(x))
                return str(x)
        with Flatten(self): 
            maxlen = max(len(Rnd(i)) for i in self._grid)
        string = '\n'.join(
            ' '.join(Rnd(e).rjust(maxlen) for e in row) for row in self._grid
        )
        return textwrap.dedent(string)
    def _repr(self):
        if self._frozen:
            s = "<*{} {}x{} 0x{:x}*>"
        else:
            s = "<{} {}x{} 0x{:x}>"
        return s.format(self.__class__.__name__, self.r, self.c, id(self))
    # ---------------------- Static methods -----------------------------
    @staticmethod
    def condition_string(s):
        '''If s is a multiline string, remove all lines of the form
        ^\w*#.*$.  This allows a data string to contain python-style 
        comments, which is handy for documentation.
 
        This allows a matrix to be defined such as:  
            matrix("""
                # Data from 13 Jan experiment with PM voltage = 677 V and
                # using photon counter 6.
                # Bias, mV    Gate init.       Counts
                    162         274             2450
                    120         180             3254
                    223         375             3802
                    131         205             2838
            """)
        '''
        s = s.strip()
        if "\n" in s:
            n = []
            for line in s.split("\n"):
                if line and line.strip()[0] != "#":
                    n.append(line)
            return '\n'.join(n)
        else:
            return s
    @staticmethod
    def from_list(p, **kw):
        '''Instantiate a matrix from a list or tuple p.  These are the
        valid forms:
 
        Size not given
            A:  Nested list:  A single argument is a list [L1, L2, ...,
            Ln] where each of the L's is a sequence of length m.  This
            will result in a matrix of n rows and m columns.
 
            B:  Flat list with no size, which will return a row vector.
 
        Size given
            C:  Flat list with size ([1, 2, 3, 4], size=(2, 2))
 
        Examples:  M = Matrix.from_list
 
        M([[1, 2, 3]]) and M([1, 2, 3]) return the row vector
            1 2 3
        M([[1], [2], [3]]) returns the column vector
            1
            2
            3
        M([[1, 2, 3], [4, 5, 6]]) returns the matrix
            1 2 3
            4 5 6
        M([1, 2, 3, 4], size=(2, 2)) returns the matrix
            1 2
            3 4
        '''
        size = kw.get("size", None)
        numtype = kw.get("numtype", None)
        if size is None:    # Form A or B
            assert(ii(p, (list, tuple)))
            if ii(p[0], (list, tuple)): # Form A (nested list)
                r, c = len(p), len(p[0])
                if not all([len(i) == c for i in p]):
                    raise TypeError(f"Not all rows have {c} elements")
                m = Matrix(r, c)
                m._grid = p
                if numtype is not None:
                    m.numtype = numtype
                return m
            else:   # Form B:  flat sequence; return a row vector
                m = Matrix(1, len(p))
                m._grid = [p]
                return m
        else:
            # Form C
            e = TypeError("size keyword must be a tuple of two integers")
            try:
                r, c = size
            except ValueError:
                raise e
            if not (ii(r, int) and ii(c, int)):
                raise e
            m = Matrix(r, c)
            with Flatten(m):
                m._grid = p
            if len(m.l) != r*c:
                raise TypeError("List needs {} elements".format(r*c))
            if numtype is not None:
                m.numtype = numtype
            return m
        raise TypeError("Improper arguments")
    @staticmethod
    def from_string(s, rowsep=None, colsep=None, expr=None, numtype=None):
        '''Instantiate a matrix from a string.  
  
        Examples:
            matrix("1 2\\n3 4") returns the 2x2 matrix
                1 2
                3 4
            as does matrix("1 2;3 4", ";").
        '''
        s = Matrix.condition_string(s)
        rows = s.strip().split(rowsep) if rowsep else s.strip().splitlines()
        m = Matrix(len(rows), len(rows[0].split(colsep)))
        for i, row in enumerate(rows):
            for j, x in enumerate(row.split(colsep)):
                m[i, j] = Matrix.getnum(x, expr=expr, numtype=numtype)
        return m
    @staticmethod
    def getnum(x, **kw):  
        '''Returns the number x; if it is a string, the method tries to
        identify it and return it in the most appropriate form.  If numtype
        is not None, then it will be coerced to the indicated type.
        expr is used to pass globals() and locals() dictionaries so that
        x can be eval'd when it is a string.
        '''
        numtype = kw.get("numtype", None)
        expr = kw.get("expr", None)
        if expr is not None and ii(x, str):
            # Assume x is an expression to be evaluated with globals
            # dictionary expr[0] and locals dictionary expr[1].
            if not ii(expr, (list, tuple)) and len(expr) != 2:
                raise ValueError(f"expr must be sequence of 2 dicts or None")
            return eval(x, expr[0], expr[1])
        if numtype is not None:
            return Matrix.NumberConvert(x, numtype)
        if not ii(x, str):
            # Assume it's already some form of number
            return x
        # It's a string, so see if we can identify it
        if (("complex" in x or "Complex" in x or "Fraction" in x or
              "Decimal" in x) and ")" in x):
            return eval(x)
        elif "i" in x.lower() or "j" in x.lower():
            re, im = Matrix.PC(x)
            if Matrix.use_Complex:
                return Complex(re, im)
            else:
                return complex(re, im)
        elif have_mpmath and ("mpf" in x or "mpc" in x):
            return eval(x)
        elif have_unc and ("(" in x or "+/-" in x or "+-" in x or "±" in x):
            if "+-" in x:
                # "+-" is not part of the uncertainties library, but I use
                # it enough to warrant putting it in getnum().
                return ufloat_fromstr(x.replace("+-", "+/-"))
            else:
                return ufloat_fromstr(x)
        elif "/" in x:
            return Fraction(x)
        elif "." in x or "e" in x:
            return float(x)
        else:
            return int(x)
    @staticmethod
    def hilbert(n): 
        '''Return an n x n Hilbert matrix.  For element [i, j], the value
        is 1/(i + j + 1).  Note that the matrix is explicitly set to use
        the Fraction numerical type.
        '''
        m = Matrix(n, n)
        m._numtype = Fraction
        for i in range(n):
            for j in range(n):
                m[i, j] = Fraction(1, i + j + 1)
        return m
    @staticmethod
    def identity(n): 
        'Return an n x n identity matrix'
        m = Matrix(n, n)
        for i in range(n):
            m[i, i] = 1
        return m
    @staticmethod
    def NumberConvert(x, T):
        '''Convert the number x to the type T.  Note some conversions
        will lose information; these are marked with #** in case you'd
        like to change them.
        '''
        def extract(s):
            'Return the portion of s between single quotes'
            s = s[s.find("'") + 1:]
            return s[:s.find("'")]
        if have_unc and T == ufloat:
            if ii(x, complex):
                return ufloat(x.real, 0)    #**
            elif ii(x, (Fraction, Decimal)):
                return ufloat(float(x), 0)  #**
            elif ii(x, UFloat):
                return x
            return ufloat(x, 0)
        elif T is complex:
            if have_unc and ii(x, UFloat):
                return complex(x.nominal_value, 0)  #**
            return complex(x, 0)    #**
        elif ii(x, float):
            if T is Decimal or T is Fraction:
                return T(str(x))
            return T(x)
        elif ii(x, complex):
            if T is Decimal or T is Fraction:
                return T(str(x.real))   #**
            return T(x.real)    #**
        elif ii(x, Fraction):
            if T is Decimal:
                return Decimal(x.numerator)/Decimal(x.denominator)
            elif have_mpmath and T is mpmath.mpf:
                return mpmath.mpf(x.numerator)/mpmath.mpf(x.denominator)
        elif ii(x, Decimal):
            if have_mpmath and T is mpmath.mpf:
                n, d = x.as_integer_ratio()
                return mpmath.mpf(n)/mpmath.mpf(d)
        elif have_mpmath and ii(x, mpmath.mpf):
            if T is Fraction:
                return Fraction(extract(str(x)))
            elif T is Decimal:
                return Decimal(extract(str(x)))
        elif have_unc and ii(x, UFloat):
            if T is complex:
                return complex(x.nominal_value, 0)  #**
            if T is Fraction or T is Decimal:
                return T(str(x.nominal_value))  #**
            return T(x.nominal_value)   #**
        try:
            return T(x)
        except Exception:
            raise TypeError("Conversion not supported")
    @staticmethod
    def from_sympy(m):
        '''m must be a sympy.Matrix object.  This function returns
        a matrix.Matrix object.
        '''
        d = vars(m)
        M = Matrix(d["rows"], d["cols"])
        with Flatten(M):
            M._grid = d["_mat"]
        return M
    @staticmethod
    def to_sympy(m):
        '''m must be a matrix.Matrix instance.  Returns a SymPy matrix
        from m.
        '''
        return sympy.Matrix(m.nl)
    @staticmethod
    def from_mpmath(m):
        '''m must be a mpmath.matrix object.  This function returns
        a matrix.Matrix object from it.
        '''
        return matrix(m.tolist())
    @staticmethod
    def to_mpmath(m):
        '''m must be a matrix.Matrix instance.  Returns an mpmath matrix
        from m.
        '''
        return mpmath.matrix(m.nl)
    @staticmethod
    def _Flatten(L):
        'Flatten every sequence in L and return a list'
        # Adapted from code by Kevin L. Sitze on 2010-11-25.  From
        # http://code.activestate.com/recipes/577470-fast-flatten-with-depth-control-and-oversight-over/?in=lang-python
        lt = (list, tuple)
        is_seq = lt if callable(lt) else lambda x: ii(x, lt)
        r, s = [], []
        s.append((0, L))
        while s:
            i, L = s.pop()
            while i < len(L):
                while is_seq(L[i]):
                    if not L[i]:
                        break
                    else:
                        s.append((i + 1, L))
                        L = L[i]
                        i = 0
                else:
                    r.append(L[i])
                i += 1
        return r
    # ---------------------- Class methods -----------------------------
    @classmethod
    def set_default_state(cls):
        '''This method sets the Matrix class variables to a default
        state.
        '''
        Matrix._str = False
        Matrix.PC = ParseComplex()
        Matrix.use_Complex = False
        Matrix.SigFig = None
    @classmethod
    def get_state(cls):
        'Save the class variables in a dictionary and return it.'
        d = {}
        d["_str"] = Matrix._str
        d["PC"] = Matrix.PC
        d["use_Complex"] = Matrix.use_Complex
        d["SigFig"] = Matrix.SigFig
        return d
    @classmethod
    def set_state(cls, state_dict):
        for key, value in state_dict.items():
            exec("Matrix.{} = value".format(key))
    # ------------------------ Properties -------------------------------
    @property
    def adjoint(self): 
        'Returns the Hermitian conjugate matrix'
        def C(x):
            return x.conjugate() if ii(x, complex) else x
        return self.t.map(C)
    @property
    def adjugate(self): 
        'Returns the adjugate matrix (transpose of cofactors)'
        return self.cofactors.t
    @property
    def c(self): 
        'Returns the number of columns in the matrix'
        return self._c
    @c.setter
    def c(self, value): 
        'Sets the number of columns in the matrix'
        self._check_frozen()
        self.resize(self.r, value)
    @property
    def cofactors(self): 
        '''Returns the matrix of cofactors.  The cofactor [i, j] of a
        square matrix is the determinant of the matrix with row i and
        column j deleted, multiplied by (-1)**(i + j).
 
        The transpose of the cofactors matrix (i.e., adjugate) divided by
        the determinant is the inverse of the original matrix.
        '''
        m = Matrix(self.r, self.c)
        for row, col, element in self:
            m[row, col] = self.cofactor(row, col)
        m._copy_attr(self)
        return m
    @property
    def cols(self): 
        'Returns a column iterator for each column in the matrix'
        for col in range(self.c):
            yield self.col(col)
    @property
    def conj(self): 
        'Returns a new matrix with elements that are complex conjugates'
        m = self.copy
        for row, col, element in self:
            if ii(m[row, col], complex):
                m[row, col] = m[row, col].conjugate()
        m._copy_attr(self)
        return m
    @property
    def copy(self): 
        'Returns a copy of the matrix'
        m = Matrix(self.r, self.c)
        m._grid = self._grid.copy()
        # Need to explicitly make copies of the rows too
        for i in range(m.r):
            m._grid[i] = self._grid[i].copy()
        m._copy_attr(self)
        return m
    @property
    def det(self): 
        'Returns the determinant of the matrix'
        if not self.is_square:
            raise TypeError("Non-square matrix does not have determinant")
        ref, _, multiplier = get_row_echelon_form(self)
        ref_det = reduce(operator.mul, ref.diag.l)
        sigfig = Matrix.SigFig if Matrix.SigFig is not None else self.sigfig 
        det = ref_det/multiplier
        det = det if ref_det else 0
        return RoundOff(det, digits=sigfig) if sigfig else det
    @property
    def diag(self): 
        'Return the diagonal of the matrix as a row vector'
        if not self.is_square:
            raise TypeError("Matrix must be square to return diagonal")
        d = []
        for i in range(self.r):
            d.append(self[i, i])
        return vector(d)
    @diag.setter
    def diag(self, seq):
        'Set the diagonal elements to those of seq, a list or vector'
        self._check_frozen()
        if not self.is_square:
            raise TypeError("Matrix must be square to set diagonal")
        if (not ii(seq, (list, tuple)) and 
            (ii(seq, Matrix) and not seq.is_vector)):
            raise TypeError("seq must be list, tuple, or vector")
        e = TypeError("seq must be of length {}".format(self.r))
        if ii(seq, Matrix):
            if seq.len != self.r:
                raise e
        else:
            if len(seq) != self.r:
                raise e
        for i in range(self.r):
            self._grid[i][i] = seq[i]
    @property
    def elements(self): 
        '''Returns an iterator over the matrix's elements.'''
        for row in range(self.r):
            for col in range(self.c):
                yield self[row, col]
    @property
    def frozen(self): 
        '''The frozen attribute lets you make a matrix read-only by
        setting the attribute to True.
        '''
        return self._frozen
    @frozen.setter
    def frozen(self, frozen): 
        self._frozen = bool(frozen)
    @property
    def grid(self): 
        '''Get a reference to the matrix instance's internal nested list
        storage for the elements.
 
        ********************** WARNING **********************
 
        This is a potentially risky attribute to use because you will
        have references to the data in the matrix instance.  If you
        change the list, you'll change the data in the matrix.
        Conversely, if a matrix operation changes the matrix, then 
        the list you have may no longer have references to the grid's
        elements.  This could lead to hard-to-find bugs.
        '''
        return self._grid
    @grid.setter
    def grid(self, grd): 
        '''Replace the self._grid nested list.  The new nested list grd
        must match the old one in size.
        '''
        self._check_frozen()
        if len(grd) != self.r:
            raise TypeError("grd must have {} rows".format(self.r))
        try:
            cols_ok = all([len(i) == self.c for i in grd])
        except Exception:
            raise TypeError("grd is not a nested list")
        if not cols_ok:
            raise TypeError("grd must have {} columns".format(self.c))
        self._grid = grd
    @property
    def i(self): 
        'Returns the inverse matrix'
        if not self.is_square:
            raise TypeError('Non-square matrix cannot have an inverse')
        identity = Matrix.identity(self.r)
        rref, inverse = get_reduced_row_echelon_form(self, identity)
        if rref != identity:
            raise TypeError('Matrix is non-invertible')
        inverse._copy_attr(self)
        return inverse
    @property
    def is_col_vector(self): 
        '''Returns True if matrix is a column vector'''
        return self.c == 1
    @property
    def is_correl(self): 
        '''Return True if matrix could be a correlation matrix.  The
        diagonal elements must be 1, the matrix must be symmetric, and
        the off-diagonal elements must be in [-1, 1].
        '''
        if not self.is_symmetric:
            return False
        if not all([i == 1 for i in self.diag.l]):
            return False
        lst = self.lower(incl_diag=False).l
        if not all([-1 <= i <= 1 for i in lst]):
            return False
        return True
    @property
    def is_hermitian(self): 
        '''Return True if matrix is Hermitian (i.e., it's the same as its 
        conjugate transpose).  A Hermitian matrix has real eigenvalues
        and can be diagonalized by a unitary matrix.  A Hermitian matrix
        is also called self-adjoint.  A unitary matrix is Hermitian and
        its adjoint (conjugate transpose) is its inverse.
        '''
        sigfig = self._get_sigfig()
        def f(x):
            if sigfig is not None:
                return RoundOff(x, digits=sigfig)
            else:
                return x
        def C(x, y):
            'Return True if x and y are complex conjugates'
            try:
                if not ii(x, complex) and not ii(y, complex):
                    return f(x) == f(y)
                a = complex(x)
                b = complex(y)
                return ((f(a.real) == f(b.real)) and 
                        (f(a.imag) == -f(b.imag)))
            except Exception:
                return False
        if not self.is_square:
            return False
        try:
            # Compare elements pairwise with the transpose.  Note we use
            # the lower triangular matrices, which means we make less
            # than half the comparisons if we used the full matrix.
            s = self.lower(incl_diag=False).l
            t = self.t.lower(incl_diag=False).l
            if not all([C(i, j) for i, j in zip(s, t)]):    
                return False
            # The diagonal elements must also be non-complex
            return all([not ii(i, complex) for i in self.diag.l])
        except Exception:
            return False
    @property
    def is_int(self): 
        'Return True if all matrix elements are integers.'
        return all([ii(i, int) for i in self.l])
    @property
    def is_invertible(self): 
        '''Returns True if this matrix has an inverse.
        '''
        try:
            inverse = self.i
            return True
        except TypeError:
            return False
    @property
    def is_pos_def(self): 
        '''Return True if the matrix is positive-definite.  self must be
        Hermitian and z.t*self*z must be > 0 for every nonzero column
        vector z where z ϵ ℂ^n.  All of a matrix's eigenvalues are 
        positive if and only if the matrix is positive-definite.
        '''
        # Do some relatively quick checks first
        if not self.is_square or not self.is_hermitian:
            return False
        # We have to check that self isn't a zero matrix, as the
        # cholesky() algorithm won't raise an exception in this case.
        if self == Matrix(self.r, self.r):
            return False
        try:
            self.cholesky()
            return True
        except TypeError:
            return False
    @property
    def is_orthogonal(self): 
        '''Return True if this matrix is orthogonal (rows and columns
        are orthogonal unit vectors).  The transpose of an orthogonal
        matrix is equal to its inverse.  The determinant of an orthogonal
        matrix is either +1 or -1.
        '''
        if not self.is_square:
            return False
        return self.t == self.i
    @property
    def is_complex(self): 
        'Return True if the matrix has complex elements'
        return any([ii(i, complex) for i in self.l])
    @property
    def is_normal(self): 
        '''Return True if the matrix is a normal matrix.  A normal
        matrix can be diagonalized by a unitary matrix.
        '''
        if not self.is_square:
            return False
        a = self.adjoint
        return self*a == a*self 
    @property
    def is_real(self): 
        'Return True if the matrix has no complex elements'
        return not any([ii(i, complex) for i in self.l])
    @property
    def is_row_vector(self): 
        'Returns True if matrix is a row vector'
        return self.r ==1
    @property
    def is_skew(self): 
        '''Returns True if matrix m is skew-symmetric (m.t == -m).
        If m and n are skew-symmetric, then so is m + n and a scalar
        times m.  m.trace is zero.  The non-zero eigenvalues of a
        skew-symmetric matrix are pure imaginary.
        '''
        return self.t == -self
    @property
    def is_square(self): 
        'Return True if matrix is a square matrix'
        return self.r == self.c
    @property
    def is_symmetric(self): 
        '''Return True if matrix is symmetric (i.e., it's equal to its
        transpose).  A real symmetric matrix can be diagonalized by an
        orthogonal matrix.
        '''
        if not self.is_square:
            return False
        try:
            # Compare elements pairwise with the transpose.  Note we use
            # the lower triangular matrices, which means we make less
            # than half the comparisons if we used the full matrix.
            s = self.lower(incl_diag=False).l
            t = self.t.lower(incl_diag=False).l
            sigfig = self._get_sigfig()
            if sigfig is not None:
                f = lambda x: RoundOff(x, digits=sigfig)
                return all([f(i) == f(j) for i, j in zip(s, t)])
            else:
                return all([i == j for i, j in zip(s, t)])
                
        except Exception:
            return False
    @property
    def is_unitary(self): 
        '''Returns True if the matrix is unitary.  
        '''
        if not self.is_square:
            return False
        return self.adjoint == self.i
    @property
    def is_vector(self): 
        '''Returns True if matrix is a row or column vector'''
        return self.is_row_vector or self.is_col_vector 
    @property
    def len(self): 
        'Returns the number of elements in the matrix'
        return self.r*self.c
    @property
    def l(self): 
        '''Return a flattened list of the matrix's elements'''
        return Matrix._Flatten(self.copy._grid)
    @property
    def mag(self): 
        'Returns the Euclidean length of the vector.'
        if not self.is_vector:
            raise TypeError("mag can be used on vectors only")
        try:
            return math.sqrt(sum(e**2 for _, _, e in self))
        except TypeError as e:
            return abs(csqrt(sum(e**2 for _, _, e in self)))
    @property
    def nl(self): 
        '''Return a copy of the nested list of the matrix's elements'''
        return self._grid.copy()
    @property
    def norm(self): 
        '''Returns the Frobenius norm for the matrix.  A matrix norm is 
        useful to bound the absolute value of the largest eigenvalue;
        it's between the reciprocal of the norm of the inverse matrix
        and the norm of the matrix.
        '''
        try:
            return math.sqrt(sum(i*i for i in self.l))
        except TypeError as e:
            return csqrt(sum(i*i for i in self.l))
    @property
    def numtype(self): 
        '''Returns the numerical type of the elements or None if it is not
        set.  Even though numtype might be set to a specific numerical
        type, it doesn't mean all the elements of the matrix have this type
        because subsequent operations can change the elements' type.   If
        you want to have the elements be all one type, set numtype to the
        desired type and all the elements will be coerced to that type.
        '''
        return self._numtype
    @numtype.setter
    def numtype(self, numerical_type): 
        '''Sets the numerical type of the matrix.  Set to None to have no 
        specific type for the elements.
        '''
        self._check_frozen()
        if numerical_type is not None:
            with Flatten(self): 
                self._grid = [Matrix.NumberConvert(i, numerical_type) 
                              for i in self._grid]
        self._numtype = numerical_type
    @property
    def r(self): 
        'Returns the number of rows in the matrix'
        return self._r
    @r.setter
    def r(self, value): 
        'Sets the number of rows in the matrix'
        self._check_frozen()
        self.resize(value, self.c)
    @property
    def rank(self): 
        '''Returns the rank of the matrix (the number of linearly 
        independent rows).
        '''
        rank = 0
        for row in self.ref.rows:
            for element in row:
                if element != 0:
                    rank += 1
                    break
        return rank
    @property
    def ref(self): 
        'Returns the row echelon form of the matrix'
        m = get_row_echelon_form(self)[0]
        m._copy_attr(self)
        return m
    @property
    def rows(self): 
        'Returns a row iterator for each row in the matrix'
        for row in range(self.r):
            yield self.row(row)
    @property
    def rref(self): 
        'Returns the reduced row echelon form of the matrix'
        m = get_reduced_row_echelon_form(self)[0]
        m._copy_attr(self)
        return m
    @property
    def sigfig(self): 
        '''The sigfig attribute is used to control comparisons of matrix
        elements as numbers.  If it is not None, then two matrix
        elements are declared equal if they are the same number after
        rounding to the indicated number of significant figures.
 
        If Matrix.SigFig is not None, it takes precedence over instance
        sigfig values when comparisons are made.
        '''
        return self._sigfig
    @sigfig.setter
    def sigfig(self, value): 
        self._check_frozen()
        if value is not None and not ii(value, int):
            raise TypeError("value must be an integer")
        if value is not None and value < 1:
            raise ValueError("value must be > 0")
        self._sigfig = value
    @property
    def size(self): 
        'Returns (number of rows, number of columns)'
        return self.r, self.c
    @size.setter
    def size(self, value): 
        'Set the size of the matrix; value must be a 2-sequence of ints'
        self._check_frozen()
        e = TypeError("value must be a 2-sequence of ints")
        if not ii(value, (list, tuple)):
            raise e
        if not ii(value[0], int) and not ii(value[1], int):
            raise e
        self.resize(*value)
    @property
    def s(self): 
        '''The s attribute is used to control what the __str__() and
        __repr__() methods return.  If s is set to False (the default),
        then __str__() returns the string form that makes the matrix
        look as you'd write it on paper and __repr__() returns a string
        such as '<Matrix 2x2 0xffcf0b50>'.
 
        When using the debugger and you type the command 'p m' where m
        is a Matrix instance, you see the __repr__ form of the matrix.
        A similar thing happens when you type '>>> m' at the interactive
        python prompt.  In such cases, you'd probably rather see the
        __str__() form; to do this, set the s attribute to True and
        the __str__ and __repr__ behaviors are swapped.  This can be
        done in the debugger with the command '!m.s = True'.
        '''
        return Matrix._str
    @s.setter
    def s(self, value): 
        Matrix._str = bool(value)
    @property
    def sum(self): 
        '''Returns the sum of all the elements.
        '''
        with Flatten(self):
            return sum(self._grid)
    @property
    def t(self): 
        'Returns the transpose as a new matrix'
        m = self.copy
        m._grid = [list(i) for i in zip(*m._grid)]
        m._r, m._c = self.c, self.r
        m._copy_attr(self)
        return m
    @property
    def trace(self): 
        'Returns the sum of the diagonal elements'
        return sum(self.diag.l)
    @property
    def type(self): 
        '''Returns a matrix containing strings representing the types of
        the elements of self.
        '''
        def T(x):
            '''Return abbreviated string form of type of x
            '''
            d = {
                "str": '"',
                "int": "ℤ",
                "float": "ℝ",
                "method": "f",
                "decimal.Decimal": "D",
                "fractions.Fraction": "ℚ",
                "complex": "ℂ",
                "matrix.Complex": "ℂ",
                "uncertainties.core.Variable": "±",
                "list": "]",
                "tuple": ")",
                "mpmath.ctx_mp_python.mpf": "Δ",
                "mpmath.ctx_mp_python.mpc": "∇",
                "mpmath.ctx_iv.ivmpf": "Λ",
            }
            if " <lambda> " in str(x):
                return "λ"
            if str(x).startswith("<function "):
                return "F"
            if str(type(x)).startswith("<class 'sympy"):
                return "𝕊"
            try:
                if x.is_vector:
                    return "𝕍"
            except AttributeError:
                pass
            if ii(x, Matrix):
                return "𝕄"
            s = str(type(x))
            loc = s.find("'")
            s = s[loc + 1:]
            loc = s.find("'")
            s = s[:loc]
            if s in d:
                return d[s]
            return "?"
        return self.map(T)
    @property
    def types(self): 
        '''Return a string showing the symbols used to codify matrix
        element types.  Use this string to help you understand the
        symbols shown when you use the .type attribute on a matrix.
        '''
        d, l = self._get_type_dict(), ["Type decorations:"]
        for k, v in d.items():
            l.append("    {}    {}".format(k, v))
        return '\n'.join(l)
    @property
    def uvec(self): 
        'Returns a unit vector in the same direction.'
        if not self.is_vector:
            raise TypeError("uvec can be used on vectors only")
        m = self/self.mag
        m._copy_attr(self)
        return m
class MatrixContext:
    '''Context manager to save the class variable state of Matrix and
    Complex and restore them on exit.
 
    Example of use:  Suppose you're in the middle of a calculation with
    the class variable settings you want, but you're interrupted with
    another calculation that needs to use different values for the class
    variables.  You can do this new calculation by
 
        with MatrixContext():
            <do calculations>
 
    Whatever settings you make to Matrix and Complex class variables
    within the with block are forgotten after the block is finished.
 
    Note __enter__ returns None, so that 'with MatrixContext() as c' is
    acceptable syntax, but the c variable is None.  This was deliberate
    to avoid having a reference to the isolated class variables' values
    before the with block was entered.
    '''
    def __enter__(self):
        self.Matrix = Matrix.get_state()
        self.Complex = Complex.get_state()
    def __exit__(self, type, value, traceback):
        Matrix.set_state(self.Matrix)
        Complex.set_state(self.Complex)
class Flatten:
    '''Context manager to convert the Matrix object's internal storage
    for elements to a flattened list to facilitate processing, then back
    to a nested list after processing is finished.
 
    An example of use where self is a Matrix instance and f is a
    univariate function to apply to each element in the matrix.  This is
    used internally in the Matrix class implementation.
    
        with Flatten(self):
            self._grid = [f(i) for i in self._grid]
    '''
    def __init__(self, m):  
        'm is a Matrix instance'
        self.m = m
    def __enter__(self):
        self.m._flatten()
    def __exit__(self, type, value, traceback):
        self.m._nested()
class Matrices():
    '''Convenience container for Matrix instances.  The primary method
    is apply(), which applies a function to each matrix.
 
    The container is a dictionary to allow user-defined information to
    be stored with each matrix.
 
    Use case:  A calculation done with matrices that contain floating
    point numbers.  When the calculation is finished, a report is
    printed and it is desired to print the results at 4 significant
    figures.  While performing the calculation, each matrix m appearing
    in the report can be stored in the container using the command 
        
        M.add(m, data)
 
    where M is the Matrices instance and m is a container of arbitrary
    data you'd like to save with the matrix.  To do the rounding at the
    end of the calculations, you'd call
 
        M.apply(lambda x: RoundOff(x, digits=4), ip=True)
 
    which would round each floating point number in each matrix to 4
    figures.
 
    You can iterate on the instance.  For example, to print out the
    matrices and their data, use
        for m, data in Matrices_instance:
            print("Matrix =")
            print(m)
            print("Data =)
            print(data)
 
    Warning:  If you apply a function to a matrix that makes a copy of
    the matrix and returns a new matrix, the id() of the new matrix will
    not match the original matrix and this new matrix will replace the
    original matrix in the container.  Thus, any references to you had
    to the original matrix will not be current.  One defense for this is
    to make the data a string that identifies the instance in some
    useful way, as this will get transferred to the new matrix.
    '''
    def __init__(self):
        self._d = OrderedDict()
    def add(self, matrix_instance, data=None):
        self._d[matrix_instance] = data
    def delete(self, matrix_instance):
        if matrix_instance in self._d:
            del self._d[matrix_instance]
    def apply(self, func, predicate=None, ip=False):
        '''Apply func to each matrix if the predicate function on matrix
        returns True or unconditionally if predicate is None.  func(m)
        should return a matrix given a matrix argument m.  The
        dictionary value for each matrix is kept with the matrix,
        whether it was operated on by func or not.
 
        If ip is True, func is expected to operate on each matrix
        element and no return value is needed.
        '''
        newdict = OrderedDict()
        if 0:
            for m, data in self._d.items():
                if predicate is not None and not predicate(m):
                    newdict[m] = data
                    continue
                m.map(func, ip=True) if ip else func(m)
                newdict[m] = data
        else:
            if ip:
                # Note this won't get an exception that the dictionary
                # changed during iteration because the Matrix instance's
                # hash won't change.
                for m in self._d:
                    if predicate is None:
                        m.map(func, ip=True)
                    elif predicate(m):
                        m.map(func, ip=True)
            else:
                newdict = OrderedDict()
                for m, data in self._d.items():
                    if predicate is None:
                        newdict[func(m)] = data
                    else:
                        if predicate(m):
                            newdict[func(m)] = data
                        else:
                            newdict[m] = data
                self._d = newdict
    def __iter__(self):
        for k, v in self._d.items():
            yield (k, v)
    @property
    def len(self):
        return len(self._d)
class Complex(complex):
    '''A convenience class class based on python's complex number class,
    but adds:
        * More instantiations from strings
        * Choice of imaginary unit
 
    The Matrix.SigFig class variable will be used to round the
    __str__form to the indicated number of significant figures.
    '''
    imaginary_unit = "i"
    # The following class variables are used to change how all Complex
    # objects display.
    _Tuple = False          # Use (real,imag) form.
    _Polar = False          # Use mag∠phase form
    _Degrees = False        # Use degrees in polar form
    _Wide = False           # Use x + yi form rather than x+yi
    def __new__(cls, real, imag=None):
        '''Initialize a new Complex instance.  real can be a string or
        number.  If present, imag can be a string or number
        '''
        re, im = 0, 0
        if ii(real, (int, float, Fraction, Decimal)):
            re = float(real)
        elif ii(real, (complex, Complex)):
            re, im = real.real, real.imag
        elif ii(real, str):
            if imag is not None:
                raise TypeError("imag not allowed if real is string")
            re, im = Matrix.PC(real)
        else:
            raise TypeError("real must be a string or number")
        if imag is not None:
            if ii(imag, (int, float, Fraction, Decimal)):
                im = float(imag)
            else:
                raise TypeError("imag must be a number")
        instance = super(Complex, cls).__new__(cls, re, im)
        return instance
    def __str__(self):
        '''This method lets you display complex numbers as you prefer.
        If you wish to use python's complex number default, just return
        'super(Complex, self.cls).__str__(self)'.
 
        My preference is that a complex number should be displayed as
        real or pure imaginary when that's the case -- and I prefer to
        use 'i' as the imaginary unit.
 
        The Matrix.SigFig setting is used to round floating point
        numbers if it is not None.  I also like to see the real and
        imaginary components displayed as integers if they are equal to
        integers after rounding.  1i should be displayed as i.
 
        Note:  a matrix can have its sigdig attribute set but
        Matrix.SigDig can be None.  In such a case, the calling code can
        set the Complex instance's sigdig attribute to the number of
        digits desired.  It's a hack, but it works.
        '''
        if Matrix.SigFig is not None:
            real = RoundOff(self.real, Matrix.SigFig)
            imag = RoundOff(self.imag, Matrix.SigFig)
        elif hasattr(self, "sigdig"):
            real = RoundOff(self.real, self.sigdig)
            imag = RoundOff(self.imag, self.sigdig)
        else:
            real = self.real
            imag = self.imag
        if self.t:
            s = "({}, {})" if self.wide else "({},{})"
            return s.format(real, imag)
        elif self.polar:
            theta = math.atan2(self.imag, self.real)
            mag = math.hypot(self.real, self.imag)
            if self.deg:   
                theta *= 180/math.pi
            t = "°" if self.deg else ""
            if Matrix.SigFig is not None:
                theta = RoundOff(theta, Matrix.SigFig)
                mag = RoundOff(mag, Matrix.SigFig)
            sep = " ∠ " if self.wide else "∠"
            return "{}{}{}{}".format(mag, sep, theta, t)
        else:
            if real == int(real):
                real = int(real)
            if imag == int(imag):
                imag = int(imag)
            if real and not imag:
                return str(real)
            elif not real and not imag:
                return "0"
            elif not real and imag:
                if imag == 1:
                    return Complex.imaginary_unit
                elif imag == -1:
                    return "-" + Complex.imaginary_unit
                return str(imag) + Complex.imaginary_unit
            else:
                # Both real and imag not zero
                if self.wide:
                    sgn = " - " if imag < 0 else " + "
                    return sgn.join([str(real), str(abs(imag)) +
                        Complex.imaginary_unit])
                else:
                    sgn = "" if imag < 0 else "+"
                    if imag in (1, -1):
                        sgn = "-" if imag == -1 else sgn
                        return sgn.join([str(real), Complex.imaginary_unit])
                    else:
                        return sgn.join([str(real), str(imag) +
                            Complex.imaginary_unit])
    def __repr__(self):
        'Display to full precision'
        real = self.real
        imag = self.imag
        sgn = "" if imag < 0 else "+"
        return sgn.join([str(real), str(imag) + Complex.imaginary_unit])
    @classmethod
    def set_default_state(cls):
        Complex.imaginary_unit = "i"
        Complex._Tuple = False
        Complex._Polar = False
        Complex._Degrees = False
        Complex._Wide = False
    @property
    def t(self):
        'Return True if the current display method is a tuple'
        return Complex._Tuple
    @t.setter
    def t(self, value):
        'Set the current display method to tuple:  str(z) --> (re, im)'
        Complex._Tuple = bool(value)
        Complex._Polar = False
    @property
    def polar(self):
        'Return True if the current display method is polar'
        return Complex._Polar
    @polar.setter
    def polar(self, value):
        'Set the current display method to polar:  str(z) --> mag∠angle'
        Complex._Polar = bool(value)
        Complex._Tuple = False
    @property
    def deg(self):
        'Return True if the polar angle is displayed in degrees'
        return Complex._Degrees
    @deg.setter
    def deg(self, value):
        'If True, the polar angle is displayed in degrees'
        Complex._Degrees = bool(value)
    @property
    def wide(self):
        '''Return True if a space character separates the connecting sign 
        in the Cartesian representation.
        '''
        return Complex._Wide
    @wide.setter
    def wide(self, value):
        'Set the Cartesian representation to wide'
        Complex._Wide = bool(value)
    @classmethod
    def get_state(cls):
        'Save the class variables in a dictionary'
        d = {}
        d["imaginary_unit"] = Complex.imaginary_unit
        d["_Tuple"] = Complex._Tuple
        d["_Polar"] = Complex._Polar
        d["_Degrees"] = Complex._Degrees
        d["_Wide"] = Complex._Wide
        return d
    @classmethod
    def set_state(cls, state_dict):
        '''Restore the class variables from a dictionary (used by the 
        MatrixContext context manager to save/restore Complex and Matrix
        class state).
        '''
        for key, value in state_dict.items():
            exec("Complex.{} = value".format(key))
if 1: # Utility functions
    def matrix(*p, **kw):
        '''Convenience function for instantiating Matrix objects.  Examples:
        Integer
          matrix(4):  Return an identity matrix of size 4
          matrix(4, fill=x):  Return size 4 square matrix filled with x
        String
          matrix("1 2\\n3 4")
        List
          Nested list:  A single argument is a list [L1, L2, ..., Ln]
            where each of the L's is a sequence of length m.  This will
            result in a matrix of n rows and m columns.
          Flat list:
            matrix([1, 2, 3, 4], size=(2, 2))
            matrix(1, 2, 3, 4, size=(2, 2))
          Flat list with no size
            matrix(1, 2, 3, 4) returns a row vector
        Stream
          Reads the stream; use the string form in the stream.
        '''
        size = kw.get("size", None)
        fill = kw.get("fill", 0)
        if size is not None:
            r, c = size
            m = Matrix(r, c)
            n = r*c
            e = ValueError(f"list is not of size {r}x{c}")
            if len(p) == 1:
                # p[0] is a sequence
                q = list(p[0])
                if len(q) != n:
                    raise e
                with Flatten(m):
                    m._grid = q
            else:
                # p is a sequence
                if len(p) != n:
                    raise e
                with Flatten(m):
                    m._grid = list(p)
        else:
            if len(p) == 1:
                q = p[0]
                if ii(q, int):
                    if "fill" in kw:
                        m = Matrix(q, q, fill=fill)
                    else:
                        m = Matrix.identity(q)
                elif ii(q, (list, tuple)):
                    # Either a flat or nested list
                    q = list(q)
                    if len(Matrix._Flatten(q)) > len(p):
                        # Nested list
                        m = Matrix.from_list(q, **kw)
                        r, c = len(q), len(q[0])
                        assert m.r == r and m.c == c, "Bad row/column lengths" 
                    else:
                        m = Matrix.from_list(q, **kw)
                        assert(m.r == 1 and m.c == len(p))
                elif ii(q, str):
                    m = Matrix.from_string(q, **kw)
                elif hasattr(q, "read"):
                    # It's a stream
                    s = q.read()
                    if ii(s, bytes):
                        s = s.decode()
                    if not s:
                        raise ValueError("Empty stream")
                    m = matrix(s, **kw)
            else:
                # Either p is a sequence or p is a list of two or three
                # strings.
                if ii(p[0], str):
                    s = p[0]
                    sep = p[1]
                    linesep = p[2] if len(p) > 2 else "\n"
                    q = s.split(linesep)
                    r = [i.split(sep) for i in q]
                    for i, item in enumerate(r):
                        r[i] = [Matrix.getnum(j, **kw) for j in item]
                    m = matrix(r, **kw)
                else:
                    m = Matrix.from_list(list(p), **kw)
                    assert(m.r == 1 and m.c == len(p))
        assert(ii(m._grid, list))
        return m
    def vector(*p, **kw):
        '''Convenience function for instantiating row and column
        vectors.  Returns a row vector by default; set keyword "c" to
        True to get a column vector.
    
        The following forms return the row vector [1 2 3]
            A:  vector(1, 2, 3)
            B:  vector(*[1, 2, 3])
            C:  vector([1, 2, 3])
            D:  vector("1 2 3")
 
        The following forms return the column vector [1 2 3].t
            A:  vector(1, 2, 3, c=True)
            B:  vector(*[1, 2, 3], c=True)
            C:  vector([1, 2, 3], c=True)
            D:  vector("1 2 3", c=True)
 
        vector(1) and vector(1, c=True) both return the 1x1 matrix [1].
 
        vector(2, fill=0) returns [0 0]
        '''
        LT = (list, tuple)
        c = kw.get("c", False)
        fill = kw.get("fill", None)
        # Get q, the sequence of vector components
        q = Matrix._Flatten(p)
        if fill is not None:
            if len(q) != 1:
                raise ValueError("Only 1 argument (an integer) allowed")
            m = Matrix(1, q[0], fill=fill)
        else:
            if len(q) == 1:
                if ii(q[0], str):               
                    # Form D with string
                    q = [Matrix.getnum(i, **kw) for i in q[0].split()]
                elif hasattr(q[0], "read"):
                    # Form D with stream
                    s = q[0].read()
                    if ii(s, bytes):
                        s = s.decode()
                    if not s:
                        raise ValueError("Empty stream")
                    q = [Matrix.getnum(i, **kw) for i in s.split()]
            m = Matrix.from_list(q)
            assert(m.r == 1)
            assert(m._grid == [q])
        return m.t if c else m
    def random_matrix(r, c=None, integer=None, normal=None, 
                      uniform=None, seed=None, cmplx=False):
        '''Returns an r x c  matrix filled with random numbers.  If c is
        not given, the matrix is r x r.  If no keywords are given, the
        elements are random floats in [0, 1).
 
        Other keywords:
            integer=(a, b)  Random integers in [a, b].
            uniform=(a, b)  Random floats in [a, b).
            normal=(mu, s)  Normally distributed with mean mu and
                            standard deviation s.
            seed            Seed for the random number generator.
            cmplx           Generate complex numbers.
        '''
        random.seed(seed) if seed is not None else random.seed()
        if c is None:
            c = r
        n = r*c
        m = Matrix(r, c)
        if integer is not None:
            try:
                a, b = integer
            except Exception:
                raise ValueError("integer keyword must be a tuple of "
                                 "integers")
            if cmplx:
                real = [random.randint(a, b) for i in range(n)]
                imag = [random.randint(a, b) for i in range(n)]
                m._grid = [Complex(i, j) for i, j in zip(real, imag)]
            else:
                m._grid = [random.randint(a, b) for i in range(n)]
        elif normal is not None:
            try:
                mu, s = normal
            except Exception:
                raise ValueError("integer keyword must be a tuple of "
                                 "numbers")
            if cmplx:
                real = [random.gauss(mu, s) for i in range(n)]
                imag = [random.gauss(mu, s) for i in range(n)]
                m._grid = [Complex(i, j) for i, j in zip(real, imag)]
            else:
                m._grid = [random.gauss(mu, s) for i in range(n)]
        elif uniform is not None:
            try:
                a, b = uniform
            except Exception:
                raise ValueError("uniform keyword must be a tuple of "
                                 "numbers")
            if cmplx:
                real = [random.uniform(a, b) for i in range(n)]
                imag = [random.uniform(a, b) for i in range(n)]
                m._grid = [Complex(i, j) for i, j in zip(real, imag)]
            else:
                m._grid = [random.uniform(a, b) for i in range(n)]
        else:
            if cmplx:
                real = [random.random() for i in range(n)]
                imag = [random.random() for i in range(n)]
                m._grid = [Complex(i, j) for i, j in zip(real, imag)]
            else:
                m._grid = [random.random() for i in range(n)]
        m._nested()
        return m
    def dot(u, v):
        '''Returns <u, v>, the scalar product of vectors u and v.  Note
        that the vectors can be of any equal size and it is not
        necessary that one be a row vector and the other a column
        vector.
        '''
        if not u.is_vector or not v.is_vector:
            raise TypeError("u and v must be vectors")
        if u.len != v.len:
            raise TypeError("u and v must be the same size")
        if u.is_row_vector:
            return u*v if v.is_col_vector else u*v.t
        else:
            return v*u if v.is_row_vector else v.t*u
    def cross(u, v):
        'Returns u x v - the vector product of 3D vectors u and v'
        if not (u.is_vector and u.len == 3):
            raise TypeError("u must be a 3-vector")
        if not (v.is_vector and v.len == 3):
            raise TypeError("v must be a 3-vector")
        w = Matrix(3, 1)
        w[0, 0] = u[1, 0]*v[2, 0] - u[2, 0]*v[1, 0]
        w[1, 0] = u[2, 0]*v[0, 0] - u[0, 0]*v[2, 0]
        w[2, 0] = u[0, 0]*v[1, 0] - u[1, 0]*v[0, 0]
        return w
    def get_row_echelon_form(matrix, mirror=None):
        '''Determine the row echelon form of the matrix using the forward
        phase of the Gauss-Jordan elimination algorithm. If a mirror matrix
        is supplied, we apply the same sequence of row operations to it.
        Neither matrix is altered in-place; instead copies are returned.
        '''
        matrix = matrix.copy
        mirror = mirror.copy if mirror else None
        det_multiplier = 1
        # Start with the top row and work downwards.
        for top_row in range(matrix.r):
            # Find the leftmost column that is not all zeros.
            # Note: this step is sensitive to small rounding errors around zero.
            found = False
            for col in range(matrix.c):
                for row in range(top_row, matrix.r):
                    if matrix[row, col] != 0:
                        found = True
                        break
                if found:
                    break
            if not found:
                break
            # Get a non-zero entry at the top of this column.
            if matrix[top_row, col] == 0:
                matrix.swap(top_row, row)
                det_multiplier *= -1
                if mirror:
                    mirror.swap(top_row, row)
            # Make this entry '1'.
            if matrix[top_row, col] != 1:
                multiplier = 1/matrix[top_row, col]
                matrix.scale(top_row, multiplier)
                matrix[top_row, col] = 1 # assign directly in case of rounding errors
                det_multiplier *= multiplier
                if mirror:
                    mirror.scale(top_row, multiplier)
            # Make all entries below the leading '1' zero.
            for row in range(top_row + 1, matrix.r):
                if matrix[row, col] != 0:
                    multiplier = -matrix[row, col]
                    matrix.add(row, top_row, multiplier)
                    if mirror:
                        mirror.add(row, top_row, multiplier)
        return matrix, mirror, det_multiplier
    def get_reduced_row_echelon_form(matrix, mirror=None):
        '''Determine the reduced row echelon form of the matrix using the
        Gauss-Jordan elimination algorithm. If a mirror matrix is supplied,
        the same sequence of row operations will be applied to it. Note
        that neither matrix is altered in-place; instead copies are
        returned.
        '''
        # Forward phase: determine the row echelon form.
        matrix, mirror, ignore = get_row_echelon_form(matrix, mirror)
        # The backward phase of the algorithm. For each row, starting at the
        # bottom and working up, find the column containing the leading 1 and
        # make all the entries above it zero.
        for last_row in range(matrix.r - 1, 0, -1):
            for col in range(matrix.c):
                if matrix[last_row, col] == 1:
                    for row in range(last_row):
                        if matrix[row, col] != 0:
                            multiplier = -matrix[row, col]
                            matrix.add(row, last_row, multiplier)
                            if mirror:
                                mirror.add(row, last_row, multiplier)
                    break
        return matrix, mirror
    def RoundOff(number, digits=12, convert=False):
        '''Round the significand of number to the indicated number of digits
        and return the rounded number (integers and Fractions are returned
        untransformed).  number can be an int, float, Decimal, Fraction or
        complex number.
     
        If you have the mpmath library, mpf and mpc types can be rounded.
        If you have the uncertainties library, UFloats can be passed in, but
        they will be returned unchanged.
        
        Rounding can get rid of trailing 0's and 9's:
                745.6998719999999               --> 745.699872
                4046.8726100000003              --> 4046.87261
                0.0254*12 = 0.30479999999999996 --> 0.3048
        so that printing the floating point representation is easier to read.
     
        If convert is True, then use float() to convert number to a floating
        point form.
     
        The digits keyword can be any integer greater than zero.  Arbitrary
        precisions with Decimal and mpmath mpf and mpc numbers are supported.
     
        The digits keyword defaults to 12 digits.  This is deliberate
        because few practical problems need more digits if they're based on
        physical measurements (mathematical calculations are the exception
        where numerical accuracy may need to be assessed).  12 was chosen
        because it gives proper rounding in a number of practical test cases
        where 13 doesn't.  For example,
            x = math.pi/6
            math.sin(x) = 0.49999999999999994
            RoundOff(math.sin(x)) = 0.5
        '''
        if ii(number, (int, Fraction)):
            return number
        if have_unc and ii(number, UFloat):
            return number
        if ii(number, complex):
            re = RoundOff(number.real, digits=digits)
            im = RoundOff(number.imag, digits=digits)
            return complex(re, im)
        can_convert = False
        if convert and not ii(number, Decimal):
            try:
                float(number)
                can_convert = True
            except ValueError:
                pass
        if ii(number, float) or (convert and can_convert):
            # Convert to a decimal, then back to a float
            x = Decimal(number)
            with localcontext() as ctx:
                ctx.prec = digits
                x = +x
                return float(x)
        elif ii(number, complex):
            return complex(
                RoundOff(number.real, digits=digits, convert=True),
                RoundOff(number.imag, digits=digits, convert=True)
                )
        elif ii(number, Decimal):
            with localcontext() as ctx:
                ctx.prec = digits
                number = +number
                return number
        elif have_mpmath and ii(number, mpmath.mpf):
            x = Decimal(mpmath.nstr(number, mpmath.mp.dps))
            with localcontext() as ctx:
                ctx.prec = digits
                x = +x
                s = str(x)
                return mpmath.mpf(s)
        elif have_mpmath and ii(number, mpmath.mpc):
            re = Decimal(mpmath.nstr(number.real, mpmath.mp.dps))
            im = Decimal(mpmath.nstr(number.imag, mpmath.mp.dps))
            old_dps = mpmath.mp.dps
            with localcontext() as ctx:
                ctx.prec = digits
                re = +re
                im = +im
                sre, sim = str(re), str(im)
                with mpmath.workdps(digits):
                    z = mpmath.mpc(sre, sim)
                    return z
        else:
            raise TypeError("Unrecognized floating point type")
if __name__ == "__main__": 
    from lwtest import run, raises, assert_equal
    from fractions import Fraction
    from decimal import Decimal
    from math import log10, sin, cos, pi, exp, sqrt
    from textwrap import dedent
    from pdb import set_trace as xx 
    import sys
    import os
    import io
    name = sys.argv[0]
    ii = isinstance
    # Import libraries if matrix.py is using them
    if have_unc:
        from uncertainties import ufloat, ufloat_fromstr, UFloat
        from uncertainties.core import Variable as ufloat_t
    else:
        print(f"{name}:  uncertainties not tested")
    if have_mpmath:
        import mpmath
        mpf, mpc = mpmath.mpf, mpmath.mpc
    else:
        print(f"{name}:  mpmath not tested")
    if have_sympy:
        from sympy import Matrix as spmatrix
    else:
        print(f"{name}:  sympy not tested")
    if 1:  # Global variables
        Fl = Matrix._Flatten
    def Assert(x, s=None):  # Because the assert statement can't be overridden
        'Drop into debugger if script has an argument'
        if len(sys.argv) > 1 and not x:
            xx()
        else:
            if s:
                assert x, s
            else:
                assert x
    def Type(t):
        'Return a uniform name for a type t'
        try:
            return Type.d[str(t)]
        except KeyError:
            if have_unc and (str(t).startswith("<function ufloat") or 
                str(t).startswith("<class 'uncertainties.core.Variable")):
                return "ufloat"
            raise
    Type.d = {
        "<class 'int'>": "int",
        "<class 'float'>": "float",
        "<class 'complex'>": "complex",
        "<class 'Complex'>": "Complex",
        "<class 'fractions.Fraction'>": "Fraction",
        "<class 'decimal.Decimal'>": "Decimal",
    }
    if have_mpmath:
        Type.d["<class 'mpmath.ctx_mp_python.mpf'>"] = "mpf"
    class Testing:
        '''Context manager to ensure a consistent Matrix and Complex class
        state before and after entry.  This helps ensure tests are isolated,
        as changing a class variable in one test function can cause side
        effects in other tests.
        '''
        def set_state(self):
            SetupGlobalTestData()
            Matrix.set_default_state()
            Complex.set_default_state()
        def __enter__(self):
            self.set_state()
        def __exit__(self, type, value, traceback):
            self.set_state()
    if True:  # Test data
        def SetupGlobalTestData():
            global a, b, c, d, a_transpose, a_cofactors, a_inverse, a_negated
            global a_plus_b, a_minus_b, a_mul_b, a_mul_c, a_mul_2, d_pow_4
            global c_transpose, i2, i3, z3, i, j, k, u, v, w, x
            a = matrix("1 2 4\n1 3 6\n-1 0 1")
            b = matrix("2 1 3\n0 -1 1\n1 2 0")
            c = matrix("1\n2\n3")
            d = matrix("2 0 0\n0 2 0\n0 0 2")
            a_transpose = matrix("1 1 -1\n2 3 0\n4 6 1")
            a_cofactors = matrix("3 -7 3\n-2 5 -2\n0 -2 1")
            a_inverse = matrix("3 -2 0\n-7 5 -2\n3 -2 1")
            a_negated = matrix("-1 -2 -4\n-1 -3 -6\n1 0 -1")
            a_plus_b = matrix("3 3 7\n1 2 7\n0 2 1")
            a_minus_b = matrix("-1 1 1\n1 4 5\n-2 -2 1")
            a_mul_b = matrix("6 7 5\n8 10 6\n-1 1 -3")
            a_mul_c = matrix("17\n25\n2")
            a_mul_2 = matrix("2 4 8\n2 6 12\n-2 0 2")
            d_pow_4 = matrix("16 0 0\n0 16 0\n0 0 16")
            c_transpose = matrix("1 2 3")
            i2 = Matrix.identity(2)
            i3 = Matrix.identity(3)
            z3 = Matrix(3, 3)
            i = matrix('1 0 0').t
            j = matrix('0 1 0').t
            k = matrix('0 0 1').t
            u = matrix('1 2 3').t
            v = matrix('4 5 6').t
            w = matrix('-3 6 -3').t
            x = matrix('0 3 4').t
    if True:    # Helper functions for testing
        def assert_false(x):
            Assert(not x)
        def assertAlmostEqual(a, b):
            'Implements the default unittest method'
            Assert(abs(round(a, 7) - round(b, 7)) == 0)
    if True:    # Initialization tests
        def test_init():
            with Testing():
                expected = matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
                m = Matrix(3, 3)
                Assert(m == expected)
                # With fill
                expected = matrix([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
                m = Matrix(3, 3, 1)
                Assert(m == expected)
                # Identity
                expected = matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
                m = matrix(3)
                Assert(m == expected)
                # From list
                vals = [[1, 2, 4], [1, 3, 6], [-1, 0, 1]]
                m = matrix(vals)
                Assert(m.size == (3, 3))
                Assert(Fl(vals) == m.l)
                # From default format string
                expected = matrix([[1, 2, 4], [1, 3, 6], [-1, 0, 1]])
                s = '1 2 4\n1 3 6\n-1 0 1'
                m = matrix(s)
                Assert(m == expected)
                # From alternate format string
                expected = matrix([[1, 2, 4], [1, 3, 6], [-1, 0, 1]])
                s = '1, 2, 4; 1, 3, 6; -1, 0, 1'
                m = matrix(s, ',', ';')
                Assert(m == expected)
        def test_init_with_list():
            with Testing():
                # Matrix forms
                m = matrix("1 2\n3 4")
                Assert(matrix([[1, 2], [3, 4]]) == m)
                t = matrix([1, 2, 3, 4], size=(2, 2))
                Assert(t == m)
                t = matrix(1, 2, 3, 4, size=(2, 2))
                Assert(t == m)
                # Vector forms
                v = matrix("1 2 3")
                Assert(matrix([[1, 2, 3]]) == v)
                Assert(matrix(1, 2, 3) == v)
                Assert(matrix([[1], [2], [3]]) == v.t)
                # Using vector() utility
                # Row vectors
                Assert(vector([[1, 2, 3]]) == v)
                Assert(vector([1, 2, 3]) == v)
                Assert(vector(1, 2, 3) == v)
                # Column vectors
                Assert(vector([[1, 2, 3]], c=True) == v.t)
                Assert(vector([1, 2, 3], c=True) == v.t)
                Assert(vector(1, 2, 3, c=True) == v.t)
                # Single element list
                n = 2
                v = Matrix(1, 1, fill=n)
                Assert(matrix([[n]]) == v)
                Assert(matrix([n]) == v == v.t)
                Assert(vector(n) == v == v.t)
                Assert(vector(1, fill=n) == v == v.t)
        def test_init_with_stream():
            with Testing():
                # Matrix
                s = "1 2\n3 4"
                f = io.StringIO(s)
                m, n = matrix(f), matrix(s)
                Assert(m == n)
                with raises(ValueError):
                    matrix(f)   # f is an empty stream
                s = "1 2 3"
                f = io.StringIO(s)
                m, n = matrix(f), matrix(s)
                Assert(m == n)
                with raises(ValueError):
                    matrix(f)   # f is an empty stream
                # Vector
                f = io.StringIO(s)
                m, n = vector(f), vector(s)
                Assert(m == n)
                with raises(ValueError):
                    vector(f)   # f is an empty stream
    if True:    # Algebra tests
        def test_equality():
            with Testing():
                Assert(a == a)
                assert_false(a != a)
                # copy
                Assert(a == a.copy)
                assert_false(a != a.copy)
                # other 
                Assert(a != b)
                assert_false(a == b)
        def test_unary():
            with Testing():
                assert_equal(+a, a)
                assert_equal(-a, a_negated)
        def test_addition():
            with Testing():
                assert_equal(a + z3, a)
                assert_equal(a + b, a_plus_b)
                # Addition of a scalar
                m = matrix("1 1\n1 1")
                assert_equal(m + 1, 2*m)
                assert_equal(1 + m, 2*m)
                # Invalid dimensions
                raises(TypeError, a.__add__, c)
                # Vector addition
                v1 = matrix("1 2")
                v2 = matrix("3 4")
                Assert(v1 + v2 == matrix("4 6"))
                Assert(v1.t + v2.t == matrix("4 6").t)
                # Vectors must be the same shape
                raises(TypeError, v1.__add__, v2.t)
                raises(TypeError, v1.t.__add__, v2)
        def test_subtraction():
            with Testing():
                assert_equal(a - z3, a)
                assert_equal(a - a, z3)
                assert_equal(a - b, a_minus_b)
                # Subtract a scalar
                m = matrix("1 1\n1 1")
                assert_equal(m - 1, 0*m)
                assert_equal(1 - m, 0*m)
                # invalid dimensions
                raises(TypeError, a.__sub__, c)
        def test_multiplication():
            with Testing():
                assert_equal(a*i3, a)
                assert_equal(i3*a, a)
                assert_equal(a*b, a_mul_b)
                assert_equal(a*c, a_mul_c)
                # m*m.i == identity
                m = matrix("2 4\n6 8")
                Assert(m*m.i == i2)
                # invalid dimensions
                raises(TypeError, c.__mul__, a)
                # scalar mult
                assert_equal(a*2, a_mul_2)
                assert_equal(2*a, a_mul_2)
                # (row vector)*(column vector) give scalar
                m = matrix("1 2")
                n = matrix("3\n4")
                assert_equal(m*n, 11)
        def test_floordiv():
            with Testing():
                m = matrix("2 4\n6 9")
                q = m//2
                Assert(q == matrix("1 2\n3 4"))
                # Doesn't work with two matrices
                raises(TypeError, m.__floordiv__, m)
        def test_truediv():
            with Testing():
                m = matrix("2 4\n6 8")
                q = m/2
                Assert(q == matrix("1 2\n3 4"))
                Assert(all([isinstance(i, float) for _, _, i in q]))
                # Matrix division
                q = m/m
                Assert(q == Matrix.identity(2))
                Assert(all([isinstance(i, float) for _, _, i in q]))
                # scalar/matrix
                s = 4
                q = s/m
                Assert(q == s*m.i)
                # matrix/scalar
                q = m/s
                Assert(q == matrix("2/4 4/4\n6/4 8/4"))
        def test_pow():
            with Testing():
                assert_equal(d**4, d_pow_4)
                assert_equal(i2**4, i2)
                # Diagonal matrix is easy to raise to power
                m = matrix("2 0\n0 3")
                assert_equal(m**8, matrix([[2**8, 0], [0, 3**8]]))
                # Low integer powers
                m, e = matrix("1 2\n3 4"), 1e-12
                Assert(m**-3 == m.i**3)
                Assert(m**-2 == m.i**2)
                Assert(m**-1 == m.i**1)
                Assert((m**-3).equals(1/(m*m*m), tol=e))
                Assert((m**-2).equals(1/(m*m), tol=e))
                Assert((m**-1).equals(1/m, tol=e))
    if True:    # Matrix operation tests
        def test_transpose():
            with Testing():
                assert_equal(a.t, a_transpose)
                assert_equal(c.t, c_transpose)
        def test_determinant():
            with Testing():
                assert_equal(a.det, 1)
                assert_equal(b.det, 0)
                with raises(TypeError):
                    c.det
        def test_cofactors():
            with Testing():
                assert_equal(a.cofactors, a_cofactors)
        def test_inverse():
            with Testing():
                assert_equal(a.i, a_inverse)
                # Inverse from adjugate = (transpose of cofactors)/det
                assert_equal(a.i, a.adjugate/a.det)
        def test_inverse_non_invertible():
            with Testing():
                with raises(TypeError):
                    b.i
        def test_iter():
            with Testing():
                m = matrix("1 2\n3 4")
                s = list(m)
                Assert(s[0] == (0, 0, 1))
                Assert(s[1] == (0, 1, 2))
                Assert(s[2] == (1, 0, 3))
                Assert(s[3] == (1, 1, 4))
                # Also test list attribute
                Assert(m.l == [1, 2, 3, 4])
        def test_equals():
            with Testing():
                m = matrix("1 2\n3 4")
                n = m.copy
                n[0, 0] += 0.01
                Assert(not m.equals(n, tol=0.001))
                # Note in the following 0.01 will fail because of roundoff
                Assert(m.equals(n, tol=0.01001))  
        def test_sigfig():
            with Testing():
                m = matrix("1 2\n3 4")
                n = m.copy
                m.sigfig = 15
                Assert(m.equals(n))
                n.map(lambda x: 1.001*x, ip=True)
                m.sigfig = 3
                Assert(m.equals(n))
                m.sigfig = 4
                Assert(not m.equals(n))
                # Both instances have sigfig defined
                m.sigfig = 3
                n.sigfig = 4
                Assert(m.equals(n))
                m.sigfig = 4
                n.sigfig = 3
                Assert(m.equals(n))
                # Matrix.SigFig is set
                Matrix.SigFig = 3
                Assert(m.equals(n))
                Matrix.SigFig = 4
                Assert(not m.equals(n))
                m.sigfig = n.sigfig = None
                Assert(not m.equals(n))
                Matrix.SigFig = 3
                Assert(m.equals(n))
        def test_minor():
            with Testing():
                M = matrix("1 2\n3 4")
                for i, j, m in ((0, 0, 4), (0, 1, 3), (1, 0, 2), (1, 1, 1)):
                    Assert(M.minor(i, j) == m)
        def test_cofactor():
            with Testing():
                m, n = matrix("1 2\n3 4"), 2
                for i, j, c in ((0, 0, 4), (0, 1, -3), (1, 0, -2), (1, 1, 1)):
                    Assert(m.cofactor(i, j) == c)
                    # Test negative indexes
                    Assert(m.cofactor(i - n, j - n) == c)
        def test_map():
            with Testing():
                m = matrix("1 2\n3 4")
                sq = matrix("1 4\n9 16")
                # Whole matrix, return a new matrix
                n = m.map(lambda x: x**2)
                Assert(n == sq)
                # Whole matrix, in-place
                m.map(lambda x: x**2, ip=True)
                Assert(m == sq)
                # Modify a row
                m = matrix("1 2\n3 4")
                n = m.map(lambda x: x//2, 1)
                Assert(n == matrix("1 2\n1 2"))
                # In-place row modification
                n = m.copy
                n.map(lambda x: x//2, 1, ip=True)
                Assert(n == matrix("1 2\n1 2"))
                n = m.copy
                n.map(lambda x: x**2, [0, 1], c=False, ip=True)
                Assert(n == sq)
                # Modify a column
                n = m.map(lambda x: x//2, 1, c=True)
                Assert(n == matrix("1 1\n3 2"))
                # In-place column modification
                n = m.copy
                n.map(lambda x: x//2, 1, c=True, ip=True)
                Assert(n == matrix("1 1\n3 2"))
                n = m.copy
                n.map(lambda x: x**2, [0, 1], c=True, ip=True)
                Assert(n == sq)
        def test_single_index():
            with Testing():
                m = matrix("1 2\n3 4")
                rv = m[0]
                Assert(rv.is_vector)
                Assert(rv.is_row_vector)
                Assert(rv == vector("1 2"))
                rv = m[1]
                Assert(rv.is_vector)
                Assert(rv.is_row_vector)
                Assert(rv == vector("3 4"))
                rv = m[-1]
                Assert(rv.is_vector)
                Assert(rv.is_row_vector)
                Assert(rv == vector("3 4"))
                rv = m[-2]
                Assert(rv.is_vector)
                Assert(rv.is_row_vector)
                Assert(rv == vector("1 2"))
                with raises(IndexError):
                    m[-3]
        def test_row_and_column_operations():
            with Testing():
                m = matrix("1 2\n3 4")
                if True:  # Row operations
                    # swap
                    n = m.copy
                    n.swap(0, 1)
                    Assert(n == matrix("3 4\n1 2"))
                    n = m.copy
                    n.swap(-2, -1)
                    Assert(n == matrix("3 4\n1 2"))
                    # add
                    n = m.copy
                    n.add(0, 1, 2)
                    Assert(n == matrix("7 10\n3 4"))
                    n = m.copy
                    n.add(0, 1)
                    Assert(n == matrix("4 6\n3 4"))
                    n = m.copy
                    n.add(-2, -1, 2)
                    Assert(n == matrix("7 10\n3 4"))
                    n = m.copy
                    n.add(-2, -1)
                    Assert(n == matrix("4 6\n3 4"))
                    # scale
                    n = m.copy
                    n.scale(0, 2)
                    Assert(n == matrix("2 4\n3 4"))
                    n = m.copy
                    n.scale(-2, 2)
                    Assert(n == matrix("2 4\n3 4"))
                if True:  # Column operations
                    # swap
                    n = m.copy
                    n.swap(0, 1, c=True)
                    Assert(n == matrix("2 1\n4 3"))
                    n = m.copy
                    n.swap(-2, -1, c=True)
                    Assert(n == matrix("2 1\n4 3"))
                    # add
                    n = m.copy
                    n.add(0, 1, 2, c=True)
                    Assert(n == matrix("5 2\n11 4"))
                    n = m.copy
                    n.add(0, 1, c=True)
                    Assert(n == matrix("3 2\n7 4"))
                    n = m.copy
                    n.add(-2, -1, 2, c=True)
                    Assert(n == matrix("5 2\n11 4"))
                    n = m.copy
                    n.add(-2, -1, c=True)
                    Assert(n == matrix("3 2\n7 4"))
                    # scale
                    n = m.copy
                    n.scale(0, 2, c=True)
                    Assert(n == matrix("2 2\n6 4"))
                    n = m.copy
                    n.scale(-2, 2, c=True)
                    Assert(n == matrix("2 2\n6 4"))
        def test_insert():
            with Testing():
                if True:    # insert_row
                    m = matrix("1 2\n3 4")
                    v = vector("5 6")
                    # Insert before first row
                    n = m.copy
                    n.insert(0, Vector=v)
                    assert_equal(n, matrix("5 6\n1 2\n3 4"))
                    # Insert before second row
                    n = m.copy
                    n.insert(1, Vector=v)
                    assert_equal(n, matrix("1 2\n5 6\n3 4"))
                    # Insert after second row
                    n = m.copy
                    n.insert(n.r, Vector=v)
                    assert_equal(n, matrix("1 2\n3 4\n5 6"))
                    # Insert row of 1's
                    n = m.copy
                    n.insert(0, fill=1)
                    assert_equal(n, matrix("1 1\n1 2\n3 4"))
                if True:    # insert_col
                    m = matrix("1 2\n3 4")
                    v = vector("5\n6", c=True)
                    # Insert before first column
                    n = m.copy
                    n.insert(0, c=True, Vector=v)
                    assert_equal(n, matrix("5 1 2\n6 3 4"))
                    # Insert before second column
                    n = m.copy
                    n.insert(1, c=True, Vector=v)
                    assert_equal(n, matrix("1 5 2\n3 6 4"))
                    # Insert after second column
                    n = m.copy
                    n.insert(n.c, c=True, Vector=v)
                    assert_equal(n, matrix("1 2 5\n3 4 6"))
        def test_delete():
            '''     1 2 3
                    4 5 6
                    7 8 9
            '''
            with Testing():
                m = matrix("1 2 3\n4 5 6\n7 8 9")
                # delete rows
                for N in (0, 3):  # N = 3 tests negative indexes
                    n = m.copy
                    v = n.delete(0 - N)
                    assert_equal(n, matrix("4 5 6\n7 8 9"))
                    assert_equal(v, vector("1 2 3"))
                    n = m.copy
                    v = n.delete(0 - N, c=False)
                    assert_equal(n, matrix("4 5 6\n7 8 9"))
                    assert_equal(v, vector("1 2 3"))
                    n = m.copy
                    v = n.delete(1 - N)
                    assert_equal(n, matrix("1 2 3\n7 8 9"))
                    assert_equal(v, vector("4 5 6"))
                    n = m.copy
                    v = n.delete(2 - N)
                    assert_equal(n, matrix("1 2 3\n4 5 6"))
                    assert_equal(v, vector("7 8 9"))
                    # delete columns
                    n = m.copy
                    v = n.delete(0 - N, c=True)
                    assert_equal(n, matrix("2 3\n5 6\n8 9"))
                    assert_equal(v, vector("1\n4\n7", c=True))
                    n = m.copy
                    v = n.delete(1 - N, c=True)
                    assert_equal(n, matrix("1 3\n4 6\n7 9"))
                    assert_equal(v, vector("2\n5\n8", c=True))
                    n = m.copy
                    v = n.delete(2 - N, c=True)
                    assert_equal(n, matrix("1 2\n4 5\n7 8"))
                    assert_equal(v, vector("3\n6\n9", c=True))
        def test_replace():
            with Testing():
                for N in (0, 2): # N = 2 tests negative indexes
                    m = matrix("1 2\n3 4")
                    v = matrix("5 6")
                    m.replace(0 - N, v)
                    Assert(m == matrix("5 6\n3 4"))
                    m.replace(1 - N, v)
                    Assert(m == matrix("5 6\n5 6"))
        def test_join():
            with Testing():
                m = matrix("1 2\n3 4")
                p = matrix("1 2\n3 4")
                m.join(p)
                Assert(m[0:].l == [1, 2, 1, 2])
                Assert(m[1:].l == [3, 4, 3, 4])
                # Columns
                m = matrix("1 2\n3 4")
                m.join(p, c=True)
                Assert(m[0:].l == [1, 2])
                Assert(m[1:].l == [3, 4])
                Assert(m[2:].l == [1, 2])
                Assert(m[3:].l == [3, 4])
        def test_rotate():
            with Testing():
                # Rotate rows
                m = matrix("1 2 3\n4 5 6\n7 8 9")
                m1 = matrix("7 8 9\n1 2 3\n4 5 6")
                m2 = matrix("4 5 6\n7 8 9\n1 2 3")
                Assert(m.rotate(0) == m)
                Assert(m.rotate(1) == m1)
                Assert(m.rotate(2) == m2)
                Assert(m.rotate(-1) == m2)
                Assert(m.rotate(-2) == m1)
                Assert(m.rotate(-3) == m)
                Assert(m.rotate(3) == m)
                # Rotate columns
                m1 = matrix("3 1 2\n6 4 5\n9 7 8")
                m2 = matrix("2 3 1\n5 6 4\n8 9 7")
                Assert(m.rotate(0, c=True) == m)
                Assert(m.rotate(1, c=True) == m1)
                Assert(m.rotate(2, c=True) == m2)
                Assert(m.rotate(-1, c=True) == m2)
                Assert(m.rotate(-2, c=True) == m1)
                Assert(m.rotate(-3, c=True) == m)
                Assert(m.rotate(3, c=True) == m)
        def test_round():
            with Testing():
                m = matrix("1.234 2.345\n3.456 4.567")
                n = m.copy
                n.sigfig = 4
                Assert(n.round() == m)
                n.sigfig = 3
                Assert(n.round() == m)
                # The previous result might be surprising, but it's by
                # design.  The comparison always uses the smaller of the two
                # instances' sigfig attribute.  To change this, either
                # unset one or use Matrix.SigFig.
                n.sigfig = None
                # Note it's still True because n wasn't rounded in-place
                Assert(n.round() == m)
                # Round it in place
                n.sigfig = 3
                n.round(ip=True)
                n.sigfig = None
                Assert(n != m)
                # Now show it works with Matrix.SigFig
                Matrix.SigFig = 3
                Assert(n == m)
                # Show we can still get a complete comparison using equals()
                # with tol set to 0.
                Assert(not n.equals(m, tol=0))
                # They're not equal if one more digit is added
                Matrix.SigFig = 4
                Assert(n != m)
    if True:    # vector operation tests
        def test_dot():
            with Testing():
                assert_equal(dot(u, v), 32)
                assert_equal(dot(v, u), 32)
                raises(TypeError, dot, a, u)
                raises(TypeError, dot, u, a)
                raises(TypeError, dot, u, matrix("1 2"))
                # Test row vector dot row vector
                r = vector("1 2")
                c = vector("3 4")
                assert_equal(dot(r, c), 11)
                assert_equal(dot(c, r), 11)
                # Test row vector dot column vector
                r = vector("1 2")
                c = vector("3\n4", c=True)
                assert_equal(dot(r, c), 11)
                assert_equal(dot(c, r), 11)
                # Test column vector dot column vector
                r = vector("1\n2", c=True)
                c = vector("3\n4", c=True)
                assert_equal(dot(r, c), 11)
                assert_equal(dot(c, r), 11)
                # Unequal size
                r = vector("1\n2", c=True)
                c = vector("3\n4\n5", c=True)
                raises(TypeError, dot, r, c)
                raises(TypeError, dot, c, r)
        def test_cross():
            with Testing():
                assert_equal(cross(u, v), w)
                assert_equal(cross(v, u), -w)
                assert_equal(cross(i, j), k)
                assert_equal(cross(j, i), -k)
                raises(TypeError, cross, u, a)
                raises(TypeError, cross, a, u)
                raises(TypeError, cross, u, matrix("1 2"))
        def test_mag():
            with Testing():
                assert_equal(x.mag, 5)
                # mag won't work on a matrix
                with raises(TypeError):
                    a.mag
        def test_uvec():
            with Testing():
                e, expect = 1e-15, [0, 0.6, 0.8]
                v = x.uvec
                assert_equal(expect[0], v[0], reltol=e)
                assert_equal(expect[1], v[1], reltol=e)
                assert_equal(expect[2], v[2], reltol=e)
                # uvec won't work on a matrix
                with raises(TypeError):
                    a.uvec
        def test_vector():
            with Testing():
                n = 3
                if True:  # Row vectors
                    v = vector(n, fill=0)
                    Assert(v.is_row_vector)
                    Assert(v.l == [0]*n)
                    # From string
                    v = vector("1 2 3")
                    Assert(v.is_row_vector)
                    Assert(v.l == [1, 2, 3])
                    vector("1 2\n3")
                    Assert(v.is_row_vector)
                    Assert(v.l == [1, 2, 3])
                    # From list
                    v = vector([[1, 2, 3]])
                    Assert(v.is_row_vector)
                    Assert(v.l == [1, 2, 3])
                if True:  # Column vectors
                    v = vector(n, c=True, fill=0)
                    Assert(v.is_col_vector)
                    Assert(v.l == [0]*n)
                    # From string
                    v = vector("1\n2\n3", c=True)
                    Assert(v.is_col_vector)
                    Assert(v.l == [1, 2, 3])
                    # From list
                    v = vector([[1], [2], [3]], c=True)
                    Assert(v.is_col_vector)
                    Assert(v.l == [1, 2, 3])
        def test_row_and_col():
            with Testing():
                m = matrix("1 2\n3 4")
                r = m.row(0)
                assert_equal(r, matrix("1 2"))
                Assert(r.is_row_vector)
                r = m.row(-2)
                assert_equal(r, matrix("1 2"))
                Assert(r.is_row_vector)
                r = m.row(-1)
                assert_equal(r, matrix("3 4"))
                Assert(r.is_row_vector)
                c = m.col(0)
                assert_equal(c, matrix("1\n3"))
                Assert(c.is_col_vector)
                c = m.col(-2)
                assert_equal(c, matrix("1\n3"))
                Assert(c.is_col_vector)
                c = m.col(-1)
                assert_equal(c, matrix("2\n4"))
                Assert(c.is_col_vector)
                raises(ValueError, m.row, 2)
                raises(ValueError, m.col, 2)
                # Extract multiple rows/columns
                m = matrix("1 2 3\n4 5 6\n7 8 9")
                r = m.row(0, 2)
                Assert(r == matrix("1 2 3\n7 8 9"))
                r = m.row(-3, -1)
                Assert(r == matrix("1 2 3\n7 8 9"))
                c = m.col(0, 2)
                Assert(c == matrix("1 3\n4 6\n7 9"))
                c = m.col(-3, -1)
                Assert(c == matrix("1 3\n4 6\n7 9"))
                raises(ValueError, m.row, 0, 3)
                raises(ValueError, m.col, 0, 3)
                raises(ValueError, m.row, -4, 2)
                raises(ValueError, m.col, -4, 2)
                # is_diagonal
                m = matrix("1 2\n3 4")
                Assert(not m.is_diagonal())
                m = matrix("1 0\n0 4")
                Assert(m.is_diagonal())
                m = matrix("1 0.01\n0 4")
                Assert(m.is_diagonal(tol=0.01))
    if True:    # Test attributes
        def test_attributes():
            with Testing():
                F = Fraction
                m = matrix("1 2\n3 4")
                t = matrix("1 3\n2 4")
                i = matrix("-2 1\n3/2 -1/2")
                a = matrix("4 -2\n-3 1")
                c = matrix("4 -3\n-2 1")
                r = matrix("1 2\n0 1")
                s = matrix("1 2\n2 1")
                v = matrix("1 2")
                rr = matrix("1 0\n0 1")
                Assert(m.r == 2)
                Assert(m.c == 2)
                Assert(m.det == -2)
                Assert(m.t == t)
                Assert(m.i == i)
                Assert(m.copy == m)
                Assert(m.adjugate == a)
                Assert(m.cofactors == c)
                Assert(m.ref == r)
                Assert(m.rref == rr)
                Assert(m.rank == 2)
                for i, r in enumerate(m.rows):
                    if i == 0:
                        Assert(str(r) == "1 2")
                    if i == 1:
                        Assert(str(r) == "3 4")
                Assert(m.len == 4)
                Assert(m.is_square == True)
                Assert(m.is_invertible == True)
                Assert(m.is_symmetric == False)
                Assert(s.is_symmetric == True)
                Assert(list(m.elements) == m.l)
                Assert(m.nl == m.grid)
                Assert(v.is_vector)
                Assert(not m.is_vector)
                # str
                n, ss, tt = 11, "<Matrix 2x2", "1 2\n3 4"
                Assert(not m.s)
                Assert(str(m) == tt)
                Assert(repr(m)[:n] == ss)
                m.s = True
                Assert(m.s)
                Assert(str(m)[:n] == ss)
                Assert(repr(m) == tt)
                m.s = False
                Assert(not m.s)
                # rows & cols
                r = [i.l for i in m.rows]
                Assert(r == [[1, 2], [3, 4]])
                c = [i.l for i in m.cols]
                Assert(c == [[1, 3], [2, 4]])
                # numtype 
                if 1:
                    Assert(m.numtype == None)
                    m.numtype = int
                    Assert(m.numtype == int)
                    Assert(all([type(i) == int for i in m.l]))
                    m.numtype = float
                    Assert(m.numtype == float)
                    Assert(all([type(i) == float for i in m.l]))
                    m.numtype = complex
                    Assert(m.numtype == complex)
                    Assert(all([type(i) == complex for i in m.l]))
                    # Also test Complex, which is a subclass of complex
                    m.numtype = Complex
                    Assert(m.numtype == Complex)
                    Assert(all([type(i) == Complex for i in m.l]))
                # Hermitian
                h = matrix("2 2+1j 4\n2-1j 3 0+1j\n4 0-1j 1")
                Assert(h.is_hermitian)
                # is_int
                m = matrix("1 2\n3 4")
                Assert(m.is_int)
                m.numtype=float
                Assert(not m.is_int)
                m = matrix("1 2\n3 4.")
                Assert(not m.is_int)
        def test_boolean_attributes():
            '''These need to be tested with both simple == tests and the 
            sigfig tests, both from the instance and from Matrix.SigFig.
            '''
            # is_symmetric
            with Testing():
                m, e = Matrix(2, 2, fill=1), 1e-4
                Assert(m.is_symmetric)
                m[0, 1] = 1 + e
                Assert(not m.is_symmetric)
                m.sigfig= 1
                Assert(m.is_symmetric)
                Assert(m.equals(m.t, tol=e))
                Matrix.SigFig = -int(log10(e)) + 1
                Assert(not m.is_symmetric)
                Matrix.SigFig = -int(log10(e)) 
                Assert(m.is_symmetric)
            # is_hermitian
            with Testing():
                for cmplx_t in (complex, Complex):
                    Matrix.SigFig = None
                    m, e = matrix("1 1+1j\n1-1j 1"), 1e-3
                    Assert(m.is_hermitian)
                    m[1, 0] = cmplx_t(1, -(1 + e))
                    Assert(not m.is_hermitian)
                    Assert(m.equals(m.t.conj, tol=e))
                    Assert(not m.equals(m.t.conj, tol=e/10))
                    m.sigfig = -int(log10(e)) + 1
                    Assert(not m.is_hermitian)
                    m.sigfig = -int(log10(e)) 
                    Assert(m.is_hermitian)
                    m.sigfig = -int(log10(e)) + 1
                    Assert(not m.is_hermitian)
                    Matrix.SigFig = -int(log10(e)) + 1
                    Assert(not m.is_hermitian)
                    Matrix.SigFig = -int(log10(e))
                    Assert(m.is_hermitian)
                # From http://mathworld.wolfram.com/HermitianMatrix.html
                m = matrix("-1 1-2i 0\n1+2i 0 -i\n0 i 1")
                Assert(m.is_hermitian)
                m = matrix("1 1+i 2i\n1-i 5 -3\n-2i -3 0")
                Assert(m.is_hermitian)
            # is_orthogonal
            with Testing():
                a, e = pi/4, 1e-10
                m = matrix('''# Element of SO(3) (rotation about z axis)
                            cos(a) sin(a) 0
                            -sin(a) cos(a) 0
                            0      0      1''', expr=(globals(), locals()))
                # Note:  m*m.t has diagonal elements of 1.0000000000000002,
                # which cause the m.is_orthogonal test to fail.  Hence, we 
                # map a RoundOff call to fix this.
                try:
                    Assert(m.is_orthogonal)
                except AssertionError:
                    prod = m*m.t
                    prod.map(RoundOff, ip=True)
                    identity = matrix(3)
                    Assert(prod == identity)
                n = m.copy
                n[1, 0] *= 1 + e
                Assert(not n.is_orthogonal)
                n.sigfig = -int(log10(e)) + 1
                Assert(not n.is_orthogonal)
                n.sigfig = -int(log10(e)) 
                Assert(not n.is_orthogonal)
                n.sigfig = -int(log10(e)) - 1
                Assert(n.is_orthogonal)
                Assert(n.is_unitary)
                # Show Matrix.SigFig overrides instance.sigfig
                Matrix.SigFig = -int(log10(e)) + 1
                Assert(not n.is_orthogonal)
                Matrix.SigFig = -int(log10(e)) 
                Assert(not n.is_orthogonal)
                Matrix.SigFig = -int(log10(e)) - 1
                Assert(n.is_orthogonal)
                Assert(n.is_unitary)
            # is_unitary
            with Testing():
                s = 1/sqrt(2)
                Matrix.use_Complex = True
                m = matrix("s s 0\n-s*1j s*1j 0\n0 0 1j", expr=({}, locals()))
                m.sigfig = 15
                Assert(not m.is_unitary)
                m.sigfig = 12
                Assert(m.is_unitary)
                for n in range(2, 20):
                    m = Matrix.identity(n)
                    Assert(m.is_unitary)
            # is_normal
            with Testing():
                m = matrix("i 0\n0 3-5i")
                Assert(not m.is_hermitian)
                Assert(m.is_normal)
            # is_skew
            with Testing():
                m = matrix("0 2 -1\n-2 0 -4\n1 4 0")
                Assert(m.is_skew)
                m[0, 0] = 1
                Assert(not m.is_skew)
                m = matrix("0")
                Assert(m.is_skew)
                m[0, 0] = 1
                Assert(not m.is_skew)
    if True:    # Miscellaneous
        def test_getnum():
            with Testing():
                gn = Matrix.getnum
                for x in (1, 1.0, 1+1j, Fraction(1, 1), Decimal(1)):
                    Assert(gn(x) == x)
                # Test with strings
                if 1:
                    Matrix.use_Complex = False
                    for s, t in (("1", int), ("1.", float), ("1e0", float),
                                ("1+0j", complex), ("1/1", Fraction),
                                ("Decimal(1)", Decimal)):
                        x = gn(s)
                        Assert(x == 1 and type(x) == t)
                    Matrix.use_Complex = True
                    for s, t in (("1", int), ("1.", float), ("1e0", float),
                                ("1+0j", Complex), ("1/1", Fraction),
                                ("Decimal(1)", Decimal)):
                        x = gn(s)
                        Assert(x == 1 and type(x) == t)
                Matrix.use_Complex = False
                # Show we can coerce types with numtype where meaningful
                for x in (1, 1., Decimal(1), Fraction(1)):
                    for t in (int, float, Decimal, Fraction):
                        try:
                            Assert(type(gn(x, t)) == t)
                        except TypeError:
                            # Can't convert Fraction to Decimal
                            Assert(type(x) == Fraction and t == Decimal)
                # Convert values with uncertainty
                if have_unc:
                    for s in "1.00(3) 1+/-0.03 1+-0.03 1±0.03".split():
                        x = gn(s)
                        Assert(x.nominal_value == 1)
                        Assert(x.std_dev == 0.03)
                # Use expressions
                x, y = 2, 3
                from math import sin, cos, pi
                m = matrix("sin(x**0.5*pi), cos(y**0.5*pi) ; x**2, y**2",
                        rowsep=";", colsep=",", expr=(globals(), locals()))
                Assert(m[0, 0] == sin(x**0.5*pi))
                Assert(m[0, 1] == cos(y**0.5*pi))
                Assert(m[1, 0] == x**2)
                Assert(m[1, 1] == y**2)
        def test_numtype():
            with Testing():
                s = '''1     2.
                    1+1j 3/4'''
                m = matrix("1 2.\n1+1j 3/4")
                m.numtype = complex  # All complex
                Assert(m[0:].l == [1+0j, 2+0j])
                Assert(m[1:].l == [1+1j, 0.75+0j])
                # Note we also need to check type because 1 == 1+0j
                for i in range(2):
                    for j in range(2):
                        Assert(type(m[i, j]) == complex)
                # Test the supported conversions
                m.numtype = int; Assert(all([type(i) == int for i in m.l]))
                m.numtype = float; Assert(all([type(i) == float for i in m.l]))
                m.numtype = complex; Assert(all([type(i) == complex for i in m.l]))
                m.numtype = Fraction; Assert(all([type(i) == Fraction for i in m.l]))
                m.numtype = Decimal; Assert(all([type(i) == Decimal for i in m.l]))
                if have_unc:
                    m.numtype = ufloat; Assert(all([type(i) == ufloat_t for i in m.l]))
                if have_mpmath:
                    m.numtype = mpf; Assert(all([type(i) == mpf for i in m.l]))
        def test_contains():
            with Testing():
                for i in (-1, 0, 1, 2, 3, 4, 6):
                    Assert(i in a)
                for i in (-2, 5, 7):
                    Assert(i not in a)
        def test_conj():
            with Testing():
                s = '''1+1j  2.+2.j
                    3-3j 3/4'''
                m = matrix(s)
                M = m.conj
                Assert(M[0:] == matrix("1-1j 2-2j"))
                Assert(M[1:] == matrix("3+3j 3/4"))
        def test_solve():
            with Testing():
                m = matrix("2 0\n0 2")
                b = matrix("2 3")
                # Solves if b is a row vector and returns a row vector
                x = m.solve(b)
                Assert(x[0, 0] == 1)
                Assert(x[0, 1] == 1.5)
                # Solves if b is a column vector and returns a column vector
                x = m.solve(b.t)
                Assert(x[0, 0] == 1)
                Assert(x[1, 0] == 1.5)
                # Solve by coercing to Fraction
                x = m.solve(b, numtype=Fraction)
                Assert(x[0, 0] == 1 and type(x[0, 0]) == Fraction)
                Assert(x[0, 1] == Fraction(3, 2))
                # Solve using augmented matrix
                M = m.copy
                M.insert(M.c, c=True, Vector=b)
                x = M.solve(aug=True)
                Assert(x[0, 0] == 1)
                Assert(x[1, 0] == 1.5)
        def test_static():
            with Testing():
                m = Matrix.identity(2)
                assert_equal(m.l, [1, 0, 0, 1])
                # hilbert
                m = Matrix.hilbert(2)
                Assert(m == matrix("1 1/2\n1/2 1/3"))
        def test_getnum():
            with Testing():
                Mg = Matrix.getnum
                for t in (int, float, complex, Complex, Decimal, Fraction):
                    Assert(type(Mg(1, numtype=t)) == t)
                if 1:
                    Matrix.use_Complex = False
                    for s, t, x in (("1", int, 1),
                                ("1.", float, 1.0),
                                ("1+0j", complex, 1+0j),
                                ("1+0i", complex, 1+0j),
                                ("Decimal(1)", Decimal, Decimal(1)),
                                ("1/2", Fraction, Fraction(1, 2))):
                        Assert(type(Mg(s)) == t)
                        Assert(Mg(s) == x)
                    Matrix.use_Complex = True
                    for s, t, x in (("1", int, 1),
                                ("1.", float, 1.0),
                                ("1+0j", Complex, 1+0j),
                                ("1+0i", Complex, 1+0j),
                                ("Decimal(1)", Decimal, Decimal(1)),
                                ("1/2", Fraction, Fraction(1, 2))):
                        Assert(type(Mg(s)) == t)
                        Assert(Mg(s) == x)
            if have_unc:
                with Testing():
                    u = type(ufloat(1, 1))
                    for s, t, x in (("2+/-1", u, ufloat(2, 1)),
                                    ("2+-1", u, ufloat(2, 1)),
                                    ("2±1", u, ufloat(2, 1)),
                                    ("2.0(1)", u, ufloat(2, 0.1))):
                        Assert(type(Mg(s)) == t)
                        # Have to handle ufloat == specially
                        Assert(Mg(s).nominal_value == x.nominal_value)
                        Assert(Mg(s).std_dev == x.std_dev)
        def test_find():
            with Testing():
                m = matrix("1 2\n3 1")
                s = m.find(1)
                assert_equal(s, [[0, 0], [1, 1]])
                s = m.find(1, 2)
                assert_equal(s, [[0, 0], [0, 1], [1, 1]])
                s = m.find(1, 2, 3)
                assert_equal(s, [[0, 0], [0, 1], [1, 0], [1, 1]])
                s = m.find(5)
                assert_equal(s, [])
                # Use absolute tolerance
                m[0, 0] = 1.01
                m[1, 1] = 1.0001
                s = m.find(1, tol=0.0001)
                assert_equal(s, [[1, 1]])
                s = m.find(1, tol=0.001)
                assert_equal(s, [[1, 1]])
                s = m.find(1, tol=0.01)
                assert_equal(s, [[0, 0], [1, 1]])
                # Use relative tolerance
                m = matrix("0 1\n2 3.03")
                s = m.find(3, reltol=0.01)
                assert_equal(s, [[1, 1]])
                s = m.find(3, reltol=0.0099)
                assert_equal(s, [])
        def test_sigfig():
            with Testing():
                if have_unc:
                    m = matrix("1/10 2.3456789 1.2-3.456j Decimal(1.22456) 3.2+/-0.1")
                    m.sigfig = 3
                    assert_equal(str(m), "1/10        2.35 (1.2-3.46j)        1.22"
                                        " 3.20+/-0.10")
                else:
                    m = matrix("1/10 2.3456789 1.2-3.456j Decimal(1.22456)")
                    m.sigfig = 3
                    assert_equal(str(m), "1/10        2.35 (1.2-3.46j)        1.22")
        def test_int():
            with Testing():
                m = matrix("1.0 2\n3.0 4.0")
                # Return copy
                n = m.int()
                Assert(n == matrix("1 2\n3 4"))
                Assert(all([isinstance(i, int) for i in n.l]))
                # Do in-place
                r = m.int(ip=True)
                Assert(r is None)
                Assert(m == matrix("1 2\n3 4"))
                Assert(all([isinstance(i, int) for i in m.l]))
        def test_resize():
            with Testing():
                m = matrix("1 2\n3 4")
                m.resize(2, 3)
                Assert(m == matrix("1 2 3\n4 0 0"))
                m.resize(1, 3)
                Assert(m == matrix("1 2 3"))
                m.resize(1, 1)
                Assert(m == matrix("1"))
                # Check fill
                m = matrix("1 2\n3 4")
                m.resize(2, 3, fill=77)
                Assert(m == matrix("1 2 3\n4 77 77"))
                # Show type continuation
                m = matrix("1 2\n3 4")
                m.numtype = float
                Assert(m == matrix("1. 2.\n3. 4."))
                Assert(all(ii(i, float) for i in m.l))
                m.resize(2, 3)
                Assert(m == matrix("1. 2. 3.\n4. 0. 0."))
                Assert(all(ii(i, float) for i in m.l))
                # Exception on bad data
                raises(TypeError, m.resize, 1, 1.)
                raises(TypeError, m.resize, 1., 1)
                raises(ValueError, m.resize, 1, 0)
                raises(ValueError, m.resize, 0, 1)
                # Exception if frozen
                m = matrix("1 2\n3 4")
                m.frozen = True
                raises(TypeError, m.resize, 1, 1)
                with raises(TypeError):
                    m.size = 1, 1
                # Setting m.r
                m = matrix("1 2\n3 4")
                m.r = 1
                Assert(m == matrix("1 2"))
                m.r = 2
                Assert(m == matrix("1 2\n0 0"))
                with raises(ValueError):
                    m.r = 0
                # Setting m.c
                m = matrix("1 2\n3 4")
                m.c = 1
                Assert(m == matrix("1\n2"))
                m.c = 2
                Assert(m == matrix("1 2\n0 0"))
                with raises(ValueError):
                    m.c = 0
        def test_split():
            with Testing():
                m = matrix("1 2\n3 4")
                m1, m2 = m.split(0)
                Assert(m1 == matrix("1 2"))
                Assert(m2 == matrix("3 4"))
                m1, m2 = m.split(0, c=True)
                Assert(m1 == matrix("1\n3"))
                Assert(m2 == matrix("2\n4"))
                # Check that numtype is kept
                m = matrix("1 2\n3 4")
                m.numtype = float
                m1, m2 = m.split(0)
                Assert(m1 == matrix("1 2"))
                Assert(m2 == matrix("3 4"))
                Assert(all(ii(i, float) for i in m1.l))
                Assert(all(ii(i, float) for i in m2.l))
                m1, m2 = m.split(0, c=True)
                Assert(m1 == matrix("1\n3"))
                Assert(m2 == matrix("2\n4"))
                Assert(all(ii(i, float) for i in m1.l))
                Assert(all(ii(i, float) for i in m2.l))
                # Check exceptions
                raises(TypeError, m.split, 0.)
                raises(ValueError, m.split, -1)
                raises(ValueError, m.split, 1)
                raises(TypeError, m.split, 0., c=True)
                raises(ValueError, m.split, -1, c=True)
                raises(ValueError, m.split, 1, c=True)
                # Can't split a row vector on rows
                m = matrix("1 2")
                raises(TypeError, m.split, 0)
                # But can split on columns
                m1, m2 = m.split(0, c=True)
                Assert(m1 == matrix("1"))
                Assert(m2 == matrix("2"))
                # Can't split a column vector on columns
                m = matrix("1\n2")
                raises(TypeError, m.split, 0, columns=True)
                # But can split on rows
                m1, m2 = m.split(0)
                Assert(m1 == matrix("1"))
                Assert(m2 == matrix("2"))
        def test_slices():
            with Testing():
                m = matrix("1 2 3\n4 5 6\n7 8 9")
                n = m[0:]
                Assert(n == matrix("1 2 3"))
                n = m[-3:]
                Assert(n == matrix("1 2 3"))
                n = m[:0]
                Assert(n == matrix("1 4 7").t)
                n = m[:-3]
                Assert(n == matrix("1 4 7").t)
                n = m[0:1]
                Assert(n == matrix("1 2 3\n4 5 6"))
                n = m[-3:-2]
                Assert(n == matrix("1 2 3\n4 5 6"))
                n = m[:0:1]
                Assert(n == matrix("1 2\n4 5\n7 8"))
                n = m[:-3:-2]
                Assert(n == matrix("1 2\n4 5\n7 8"))
                # Gets whole matrix
                Assert(m[0:2] == m)
                Assert(m[:0:2] == m)
                Assert(m[-3:-1] == m)
                Assert(m[:-3:-1] == m)
                # Bad parameters
                s = "m[3:] m[:3] m[0:3] m[:0:3] m[1:0] m[:1:0] m[2:1] m[:2:1]"
                for i in s.split():
                    exec("with raises(ValueError): {}".format(i))
        def test_frozen():
            with Testing():
                m = matrix("1 2\n3 4")
                m.frozen = True
                s = '''
                    m[0, 0] = 0
                    m.add(0, 1, 2)
                    m.delete(0)
                    m.delete(0, c=True)
                    m.insert(0)
                    m.insert(0, c=True)
                    m.int(ip=True)
                    m.map(int, ip=True)
                    m.scale(0, 1)
                    m.scale(0, 1, c=True)
                    m.resize(0, 1)
                    m.swap(0, 1)'''
                for i in s.strip().split("\n"):
                    exec("with raises(TypeError): {}".format(i.strip()))
        def test_call():
            with Testing():
                m = matrix("1 2\n3 4")
                Assert(m(0, 0) == m[0, 0])
                Assert(m(0, 1) == m[0, 1])
                Assert(m(1, 0) == m[1, 0])
                Assert(m(1, 1) == m[1, 1])
                # Check it works on vectors too
                m = matrix("1 2")
                Assert(m(0) == m[0])
                Assert(m(1) == m[1])
                m = m.t
                Assert(m(0) == m[0])
                Assert(m(1) == m[1])
        def test_diag():
            with Testing():
                m = matrix("1 2\n3 4")
                d = m.diag
                Assert(d.is_row_vector)
                Assert(d[0] == 1)
                Assert(d[1] == 4)
                # Set the diagonal values
                for s in ([88, 99], matrix([[88, 99]]),
                        matrix([[88], [99]])):
                    m.diag = s
                    for i in range(m.r):
                        Assert(m[i, i] == s[i])
        def test_adjoint():
            with Testing():
                m = matrix("1 2+3j\n4-5j 6j")
                a = m.adjoint
                Assert(a[0, 0] == 1)
                Assert(a[0, 1] == 4+5j)
                Assert(a[1, 0] == 2-3j)
                Assert(a[1, 1] == -6j)
        def test_float():
            with Testing():
                m = matrix("1.0 2+3j\n4-5j 6j")
                n = m*m.adjoint
                Assert(n[0, 0] == 14)
                Assert(n[0, 1] == 22-7j)
                Assert(n[1, 0] == 22+7j)
                Assert(n[1, 1] == 77)
                n.float(ip=True)    
                Assert(n[0, 0] == 14 and ii(n[0, 0], float))
                Assert(n[1, 1] == 77 and ii(n[1, 1], float))
                Assert(ii(n[0, 1], complex))
                Assert(ii(n[1, 0], complex))
        def test_decorate():
            with Testing():
                m = Matrix(4, 4)
                m.numtype = float
                m.numtype = None    # Avoids an exception when strings inserted
                m[0, 2] = 1.0
                m[1, 3] = 2.0
                d = [(0, "."), (int, lambda x: x)]
                n = m.decorate(d)
                s = '''
                    .   . 1.0   .
                    .   .   . 2.0
                    .   .   .   .
                    .   .   .   .'''[1:]
                Assert(str(n) == dedent(s))
        def test_grid():
            with Testing():
                m = matrix("1 2\n3 4")
                m.grid = [[5, 6], [7, 8]]
                Assert(m == matrix("5 6\n7 8"))
        def test_Testing():
            '''Verify the Testing context manager sets the class variables'
            states to the defaults at entry and back to the defaults at exit.
            '''
            # Set things to nonsense, then show that the state is correct
            # after entering the context manager.
            Matrix.SigFig =          \
                Matrix._str =        \
                Matrix.use_Complex = \
                Complex.imaginary_unit =       \
                Complex._Tuple =     \
                Complex._Polar =     \
                Complex._Degrees =   \
                Complex._Wide = "nonsense"
            with Testing():
                Assert(Matrix._str == False and
                    Matrix.use_Complex == False and
                    Matrix.SigFig == None and
                    Complex.imaginary_unit == "i" and
                    Complex._Tuple == False and
                    Complex._Polar == False and
                    Complex._Degrees == False and
                    Complex._Wide == False)
            # Set things to nonsense inside the context manager and show that
            # the state is correct after leaving the context manager.
            with Testing():
                Matrix.SigFig =          \
                    Matrix._str =        \
                    Matrix.use_Complex = \
                    Complex.imaginary_unit =       \
                    Complex._Tuple =     \
                    Complex._Polar =     \
                    Complex._Degrees =   \
                    Complex._Wide = "nonsense"
            Assert(Matrix._str == False and
                Matrix.use_Complex == False and
                Matrix.SigFig == None and
                Complex.imaginary_unit == "i" and
                Complex._Tuple == False and
                Complex._Polar == False and
                Complex._Degrees == False and
                Complex._Wide == False)
        def test_Complex_formatting():
            with Testing():
                Matrix.SigFig = 3
                z = Complex(1, -1/3)
                # Normal display
                Assert(str(z) == "1-0.333i")
                z.wide = True
                Assert(str(z) == "1 - 0.333i")
                z.wide = False
                # Tuple display
                z.t = True
                z.wide = False
                Assert(str(z) == "(1.0,-0.333)")
                z.wide = True
                Assert(str(z) == "(1.0, -0.333)")
                z.wide = False
                # Polar display with radians
                z.polar = True
                Assert(str(z) == "1.05∠-0.322")
                z.wide = True
                Assert(str(z) == "1.05 ∠ -0.322")
                z.wide = False
                # Polar display with degrees
                z.deg = True
                Assert(str(z) == "1.05∠-18.4°")
                z.wide = True
                Assert(str(z) == "1.05 ∠ -18.4°")
                z.wide = False
            with Testing():
                # Special forms
                Matrix.SigFig = 3
                z = Complex(1, -1)
                Assert(str(z) == "1-i")
                z = Complex(1, 1)
                Assert(str(z) == "1+i")
                z = Complex(0, -1)
                Assert(str(z) == "-i")
                z = Complex(0, 1)
                Assert(str(z) == "i")
                z = Complex(1)
                Assert(str(z) == "1")
                z = Complex(2)
                Assert(str(z) == "2")
                z = Complex(-1)
                Assert(str(z) == "-1")
                z = Complex(-2)
                Assert(str(z) == "-2")
                z = Complex(0, 0)
                Assert(str(z) == "0")
                z = Complex(1/3)
                Assert(str(z) == "0.333")
                z = Complex(-1/3)
                Assert(str(z) == "-0.333")
        def test_lower_upper():
            with Testing():
                m = matrix("1 2\n3 4")
                n = m.copy
                # lower
                Assert(n.lower() == matrix("1 0\n3 4"))
                Assert(n.lower(incl_diag=False) == matrix("0 0\n3 0"))
                n.lower(ip=True)
                Assert(n == matrix("1 0\n3 4"))
                n.lower(ip=True, incl_diag=False)
                Assert(n == matrix("0 0\n3 0"))
                # upper
                n = m.copy
                Assert(n.upper() == matrix("1 2\n0 4"))
                Assert(n.upper(incl_diag=False) == matrix("0 2\n0 0"))
                n.upper(ip=True)
                Assert(n == matrix("1 2\n0 4"))
                n.upper(ip=True, incl_diag=False)
                Assert(n == matrix("0 2\n0 0"))
        def test_MatrixContext():
            with Testing():
                sf = 3
                Matrix.SigFig = sf
                Complex.imaginary_unit = sf
                with MatrixContext():
                    Matrix.SigFig = "a string setting"
                Assert(Matrix.SigFig == sf)
                Assert(Complex.imaginary_unit == sf)
        def test_mpmath_sympy():
            '''Show we can convert a simple matrix.Matrix to mpmath and
            sympy matrices and back.
            '''
            if have_mpmath:
                with Testing():
                    m = matrix("1 2\n3 4")
                    M = Matrix.to_mpmath(m)
                    Assert(M[0,0] == 1)
                    Assert(M[0,1] == 2)
                    Assert(M[1,0] == 3)
                    Assert(M[1,1] == 4)
                    for i in range(2):
                        for j in range(2):
                            Assert(M[i, j] == m[i, j])
                            Assert(type(M[i, j]) == mpf)
                    n = Matrix.from_mpmath(M)
                    Assert(m == n)
            if have_sympy:
                with Testing():
                    m = matrix("1 2\n3 4")
                    M = Matrix.to_sympy(m)
                    s = "<class 'sympy.core.numbers"
                    for i in range(2):
                        for j in range(2):
                            Assert(M[i, j] == m[i, j])
                            Assert(str(type(M[i, j])).startswith(s))
                    n = Matrix.from_sympy(M)
                    Assert(m == n)
        def test_Matrices():
            with Testing():
                '''Demonstrate in-place modification of a matrix in
                conjunction with a predicate function.  Here, we'll square
                the elements of a matrix if all of its elements are even
                numbers.
                '''
                def all_even_elements(m):
                    return all([i % 2 == 0 for i in m.l])
                cont = Matrices()
                m = matrix("1 2\n3 4")      # Not even elements
                n = 2*m                     # Even elements
                # Add them to the container
                cont.add(m, "m")
                cont.add(n, "n")
                Assert(cont.len == 2)
                # Use a predicate to square the elements of the matrix with
                # even elements
                sq = lambda x: x*x
                cont.apply(sq, predicate=all_even_elements, ip=True)
                for k, v in cont:
                    if v == "m":
                        # m is unchanged
                        Assert(k == matrix("1 2\n3 4"))
                    else:
                        # n's elements were squared
                        Assert(k == matrix("4 16\n36 64"))
                # Delete n
                cont.delete(n)
                Assert(cont.len == 1)
                # Check that m is the remaining matrix
                for k, v in cont:
                    Assert(k == matrix("1 2\n3 4"))
                cont.delete(m)
                # Empty container
                Assert(cont.len == 0)
            with Testing():
                '''Demonstrate that a function can convert all matrix elements
                to floats.
                '''
                def NewFloatMatrix(m):
                    n = m.copy
                    n.map(float, ip=True)
                    return n
                cont = Matrices()
                m = matrix("1 2\n3 4")
                n = 2*m
                # Add them to the container
                cont.add(m, "m")
                cont.add(n, "n")
                Assert(cont.len == 2)
                # Apply the function to each matrix
                cont.apply(NewFloatMatrix)
                # Check values and types
                p = matrix("1 2\n3 4")
                for k, v in cont:
                    if v == "m":
                        Assert(k == p)
                        Assert(all([ii(i, float) for i in k.l]))
                        # Note we no longer have the original m matrix
                        Assert(id(k) != id(m))
                    else:
                        Assert(k == 2*p)
                        Assert(all([ii(i, float) for i in k.l]))
                        # Note we no longer have the original n matrix
                        Assert(id(k) != id(n))
        def test_cholesky():
            'Also test the is_positive_definite attribute here'
            N = 20  # Matrix size range
            with Testing():
                # Test matrices from 
                # http://rosettacode.org/wiki/Cholesky_decomposition
                m = matrix("25 15 -5\n15 18 0\n-5 0 11")
                n = matrix("5 0 0\n3 3 0\n-1 1 3")
                Assert(m.cholesky() == n)
                # Do it with mpmath
                if have_mpmath:
                    mp_m = m.to_mpmath(m)
                    p = m.from_mpmath(mpmath.cholesky(mp_m))
                    Assert(p == n)
                # 4x4 matrix
                a = matrix('''
                18  22   54   42
                22  70   86   62
                54  86  174  134
                42  62  134  106''')
                b = matrix('''
                4.24264    0.00000    0.00000    0.00000
                5.18545    6.56591    0.00000    0.00000
                12.72792    3.04604    1.64974    0.00000
                9.89949    1.62455    1.84971    1.39262''')
                a.sigfig = 6  # Equal to within 6 figures
                Assert(a.cholesky() == b)
                # Not positive-definite matrix
                # https://en.wikipedia.org/wiki/Definiteness_of_a_matrix#Examples
                m = matrix("1 2\n2 1")
                with raises(TypeError):
                    m.cholesky()
                Assert(not m.is_pos_def)
                # From mpmath/matrices/linalg.py docstring for cholesky()
                for n in range(2, N):
                    m = -Matrix.identity(n) + Matrix.hilbert(n)
                    with raises(TypeError):
                        m.cholesky()
                    Assert(not m.is_pos_def)
                # Zero matrix is not positive definite (note
                # mpmath.cholesky() doesn't detect this)
                for n in range(2, N):
                    z = Matrix(n, n)
                    Assert(not z.is_pos_def)
                # Non-square matrix is not positive definite
                m = matrix("1 2 3\n4 5 6")
                Assert(not m.is_pos_def)
                # Non-symmetric matrix is not positive definite
                m = matrix("1 2 \n2.01 1")
                Assert(not m.is_pos_def)
            with Testing():
                # The Cholesky decomposition of a Pascal upper-triangular
                # matrix is the identity matrix.  Code from
                # http://rosettacode.org/wiki/Pascal_matrix_generation#Python.
                def C(n, k):
                    result = 1
                    for i in range(1, k+1):
                        result = result*(n - i + 1)//i
                    return result
                def Upper(n):
                    return [[C(j, i) for j in range(n)] for i in range(n)]
                for i in range(2, N):
                    u = matrix(Upper(i))
                    m = u.cholesky()
                    Assert(m == Matrix.identity(i))
                    Assert(m.map(int) == Matrix.identity(i))
        def test_is_correl():
            N = 20  # Matrix size range
            with Testing():
                for n in range(2, N):
                    Assert(Matrix.identity(n).is_correl)
                    m = random_matrix(n) - 0.5
                    m = m.lower(incl_diag=False)
                    m += m.t
                    m.diag = vector([[1]*n])
                    Assert(m.is_correl)
        def TestRoundOff():
            def TestBasic():
                # Integers and Fractions aren't changed
                for i in range(-3, 3):
                    assert_equal(i, RoundOff(i))
                # Basic functionality
                for x, val in (
                    (0.0, 0.0),
                    (-0.0, -0.0),
                    (1.0, 1.0),
                    (-1.0, -1.0),
                    (0.1 + 1e-16, 0.1),
                    (1/3, 0.333333333333),
                    (3.3, 3.3),
                    (-3.3, -3.3),
                    (745.6998719999999, 745.699872),
                    (-745.6998719999999, -745.699872),
                    (4046.8726100000003, 4046.87261),
                    (-4046.8726100000003, -4046.87261),
                    (0.0254*12, 0.3048),
                    (-0.0254*12, -0.3048),
                    (0.062369999999999995, 0.06237),
                    (1233.4867714896711, 1233.48677149),
                    (0.15898729492799998, 0.158987294928),
                    (0.00045000000000000004, 0.00045),
                    (7.865790719999997e-06, 7.86579072e-06),
                    (0.019049999999999997, 0.01905),
                    (249.08890999999994, 249.08891),
                ):
                    assert_equal(RoundOff(x), val)
                # Show some transcendentals aren't significantly changed
                tol = 3e-12
                for x in (pi, exp(1), sqrt(2)):
                    assert_equal(RoundOff(x), x, reltol=tol)
                    assert_equal(RoundOff(-x), -x, reltol=tol)
                # Show we can round to a few significant figures
                const = 1e8
                for x, val in (
                    (pi,         3.142),
                    (pi*const,   3.142*const),
                    (pi/const,   3.142/const),
                ):
                    assert_equal(RoundOff(x, digits=4), val)
                    assert_equal(RoundOff(-x, digits=4), -val)
                if have_mpmath:
                    digits = 12
                    with mpmath.workdps(digits):
                        x = mpmath.mpf(249.08890999999994)
                        s = mpmath.nstr(x, digits)
                        assert_equal(s, "249.08891")
            def TestComplex():
                z = complex(1/3, 745.6998719999999)
                digits = 12
                w = RoundOff(z, digits=digits)
                assert_equal(w, 0.333333333333+745.699872j)
                if have_mpmath:
                    with mpmath.workdps(digits):
                        z = mpmath.mpc(1/3, 745.6998719999999)
                        w = RoundOff(z)
                        assert_equal(str(w), "(0.333333333333 + 745.699872j)")
            def TestFraction():
                x = Fraction(835875, 10185)
                y = RoundOff(x)
                assert_equal(x, y)
                assert_equal(id(x), id(y))
            def TestDecimal():
                n = 12
                x = Decimal("1.00000000000000000000000000000000000000000000000001")
                assert_equal(RoundOff(x, digits=n), Decimal('1.00000000000'))
            def Test_ufloat():
                if have_unc:
                    x = ufloat(1, 1)
                    y = RoundOff(x)
                    Assert(x == y)
                    assert_equal(id(x), id(y))
            TestBasic()
            TestComplex()
            TestFraction()
            TestDecimal()
            Test_ufloat()
        def TestParseComplex():
            test_cases = {
                # Pure imaginaries
                1j : (
                    "i", "j", "1i", "i1", "1j", "j1", "1 j", "j 1",
                    "I", "J", "1I", "I1", "1J", "J1", "1 i", "i 1",
                ),
                -1j : (
                    "-i", "-j", " - \t\n\r\v\f j",
                    "-I", "-J", " - \t\n\r\v\f J",
                ),
                3j : (
                    "3i", "+3i", "3.i", "+3.i", "3.0i", "+3.0i", "3.0e0i", "+3.0e0i",
                    "i3", "+i3", "i3.", "+i3.", "i3.0", "+i3.0", "i3.0e0", "+i3.0e0",
                    "3.000i", "i3.000", "3.000E0i", "i3.000E0",
                    "3.000e-0i", "i3.000e-0", "3.000e+0i", "i3.000e+0",
        
                    "3I", "+3I", "3.I", "+3.I", "3.0I", "+3.0I", "3.0e0I", "+3.0e0I",
                    "I3", "+I3", "I3.", "+I3.", "I3.0", "+I3.0", "I3.0e0", "+I3.0e0",
                    "3.000I", "I3.000", "3.000E0I", "I3.000E0",
                    "3.000e-0I", "I3.000e-0", "3.000e+0I", "I3.000e+0",
        
                    "3j", "+3j", "3.j", "+3.j", "3.0j", "+3.0j", "3.0e0j", "+3.0e0j",
                    "j3", "+j3", "j3.", "+j3.", "j3.0", "+j3.0", "j3.0e0", "+j3.0e0",
                    "3.000j", "j3.000", "3.000E0j", "j3.000E0",
                    "3.000e-0j", "j3.000e-0", "3.000e+0j", "j3.000e+0",
        
                    "3J", "+3J", "3.J", "+3.J", "3.0J", "+3.0J", "3.0e0J", "+3.0e0J",
                    "J3", "+J3", "J3.", "+J3.", "J3.0", "+J3.0", "J3.0e0", "+J3.0e0",
                    "3.000J", "J3.000", "3.000E0J", "J3.000E0",
                    "3.000e-0J", "J3.000e-0", "3.000e+0J", "J3.000e+0",
                ),
                -8j : (
                    "-8i", "-8.i", "-8.0i", "-8.0e0i",
                    "-i8", "-i8.", "-i8.0", "-i8.0E0",
        
                    "-8I", "-8.I", "-8.0I", "-8.0e0I",
                    "-I8", "-I8.", "-I8.0", "-I8.0E0",
        
                    "-8j", "-8.j", "-8.0j", "-8.0e0j",
                    "-j8", "-j8.", "-j8.0", "-j8.0E0",
        
                    "-8J", "-8.J", "-8.0J", "-8.0e0J",
                    "-J8", "-J8.", "-J8.0", "-J8.0E0",
                ),
                # Reals
                0 : (
                    "0", "+0", "-0", "0.0", "+0.0", "-0.0"
                    "000", "+000", "-000", "000.000", "+000.000", "-000.000",
                    "0+0i", "0-0i", "0i+0", "0i-0", "+0i+0", "+0i-0", "i0+0",
                    "i0-0", "+i0+0", "+i0-0", "-i0+0", "-i0-0",
                ),
                1 : (
                    "1", "+1", "1.", "+1.", "1.0", "+1.0", "1.0e0", "+1.0e0",
                                                        "1.0E0", "+1.0E0",
                    "1+0i", "1-0i",
                    "0i+1", "+0i+1", "-0i+1", "i0+1", "+i0+1", "-i0+1",
                ),
                -1 : (
                    "-1", "-1+0i", "-1-0i", "0i-1", "+0i-1", "-0i-1",
                    "i0-1", "+i0-1", "-i0-1",
                ),
                -2 : (
                    "-2", "-2.", "-2.0", "-2.0e0",
                ),
                -2.3 : (
                    "-2.3", "-2.30", "-2.3000", "-2.3e0", "-2300e-3", "-0.0023e3",
                    "-.23E1",
                ),
                2.345e-7 : (
                    "2.345e-7", "2345e-10", "0.00000002345E+1", "0.0000002345",
                ),
                # Complex numbers
                1+1j: ("1+i", "1+1i", "i+1", "1i+1", "i1+1"),
                1-1j: ("1-i", "1-1i", "-i+1", "-1i+1", "-i1+1"),
                -1-1j: ("-1-i", "-1-1i", "-i-1", "-1i-1", "-i1-1"),
                1-2j : (
                    "1-2i", "1-2.i", "1.-2i", "1.-2.i",
                    "1-j2", "1-j2.", "1.-j2", "1.-j2.",
                    "1.00-2.00I", "1.00-I2.00", "1000e-3-200000e-5I",
                    "1.00-J2.00", "1000E-3-J200000E-5",
                    "-2i+1", "-i2 + \n1",
                    "-i2+1",
                ),
                -1+2j : (
                    "2i-1", "i2-1",
                    "+2i-1", "+i2-1",
                ),
                -12.3+4.56e-7j : (
                    "-12.3+4.56e-7j",
                    "-12.3 + 4.56e-7j",
                    "- 1 2 . 3 + 4 . 5 6 e - 7 j",
                    "-1.23e1+456e-9i",
                    "-0.123e2+0.000000456i",
                ),
            }
            c = ParseComplex()
            for number in test_cases:
                for numstr in test_cases[number]:
                    real, imag = c(numstr)
                    num = complex(real, imag)
                    assert_equal(num, number)
            # Test that we can get Decimal types back
            c = ParseComplex(Decimal)
            a, b = c("1+3i")
            Assert(isinstance(a, Decimal) and isinstance(b, Decimal))
            Assert(a == 1 and b == 3)
            a, b = c("-1.2-3.4i")
            Assert(isinstance(a, Decimal) and isinstance(b, Decimal))
            Assert(a == Decimal("-1.2") and b == Decimal("-3.4"))
            # Test that we can get rational number components back
            c = ParseComplex(Fraction)
            a, b = c("-1.2-3.4i")
            Assert(isinstance(a, Fraction) and isinstance(b, Fraction))
            Assert(a == Fraction(-6, 5) and b == Fraction(-17, 5))
            # Show that numbers with higher resolutions than floats can be used
            c = ParseComplex(Decimal)
            rp = "0.333333333333333333333333333333333"
            ip = "3.44444444444444444444444444444"
            r, i = c(rp + "\n-i" + ip)  # Note inclusion of a newline
            Assert(r == Decimal(rp))
            Assert(i == Decimal("-" + ip))
            # Test that mpmath mpf numbers can be used
            if have_mpmath:
                c = ParseComplex(mpf)
                a, b = c("1.1 - 3.2i")
                Assert(isinstance(a, mpf) and isinstance(b, mpf))
                Assert(a == mpf("1.1") and b == mpf("-3.2"))
    SetupGlobalTestData()
    exit(run(globals(), halt=True)[0])
