'''
TODO:
    * Test sum attribute

Matrix module (python 3 only)
'''
if True: # Imports & globals
    # This module is a derivative work of the 3.0.0 version of pymatrix,
    # gotten on 15 Jul 2019 from
    # https://github.com/dmulholl/pymatrix.git.

    # Copyright (C) 2019 Don Peterson
    # Contact:  gmail.com@someonesdad1
    
    #
    # Licensed under the Open Software License version 3.0.
    # See http://opensource.org/licenses/OSL-3.0.
    #

    from collections import OrderedDict
    from collections.abc import Iterable
    from decimal import Decimal, localcontext
    from fractions import Fraction
    from functools import reduce, partial
    from itertools import chain, zip_longest, starmap
    from pdb import set_trace as xx
    import math
    from cmath import sqrt as csqrt
    import operator
    from os import environ
    import random
    import re
    import sys
    import textwrap

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
    __version__ = "11Aug2019"
    __all__ = [
        "Complex", 
        "cross", 
        "dot", 
        "Flatten", 
        "have_mpmath",
        "have_sympy",
        "have_unc",
        "Matrices", 
        "Matrix", 
        "matrix", 
        "MatrixContext", 
        "random_matrix", 
        "RoundOff",
        "vector",
        ]

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
    and columns are numbered starting from 0.  The preferred methods for
    accessing matrix elements are m[i, j] or m(i, j) where i is the row
    and j is the column.  A matrix with one row or column is a row or
    column vector and the indexing scheme lets you get at a vector's
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
        if not isinstance(rows, int) or not isinstance(cols, int):
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
        if isinstance(other, Matrix):   # Matrix addition
            if self.r != other.r or self.c != other.c:
                raise TypeError('Cannot add matrices of different sizes')
            m = Matrix(self.r, self.c)
            with Flatten(self): M1 = self._grid
            with Flatten(other): M2 = other._grid
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
        if isinstance(other, Matrix):
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
        if isinstance(key, (tuple, list)):
            row, col = key
            return self._grid[row][col]
        elif isinstance(key, slice):
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
        elif isinstance(key, int):
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
        if isinstance(other, Matrix):
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
        if not isinstance(other, int):
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
        if isinstance(key, (tuple, list)):  # Set a single element
            nr, nc = self.r, self.c
            row, col = key
            row = row + nr if row < 0 else row
            col = col + nc if col < 0 else col
            if not (0 <= row < nr):
                raise ValueError("row must be 0 to {}".format(nr - 1))
            if not (0 <= col < nc):
                raise ValueError("col must be 0 to {}".format(nc - 1))
            self._grid[row][col] = value
        elif isinstance(key, int):
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
                if isinstance(value, Matrix):
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
        if isinstance(other, Matrix):
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
        if isinstance(other, Matrix):
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
            if isinstance(x, complex):
                return complex(f(x.real), f(x.imag))
            elif isinstance(x, Complex):
                return Complex(f(x.real), f(x.imag))
            elif have_mpmath and isinstance(x, mpmath.mpc):
                return mpmath.mpc(f(x.real), f(x.imag))
            elif isinstance(x, float):
                return f(x)
            elif have_mpmath and isinstance(x, mpmath.mpf):
                return f(x)
            elif have_unc and isinstance(x, UFloat):
                raise TypeError("Can't chop an uncertain number")
            elif isinstance(x, Decimal):
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
                    if isinstance(item, key):
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
            cv = m._grid.pop(n)    # cv is a list
            m._r -= 1
            cv = vector([cv]).t  # Convert it to a column vector
            self._grid = m.t._grid
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
            v = vector([r])
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
        if not isinstance(other, Matrix):
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
            if isinstance(x, complex) and not x.imag:
                return x.real
            return x
        if ip:
            self._check_frozen()
        m = self if ip else self.copy
        m.map(Float, ip=True)
        return None if ip else m
    def insert(self, n, c=False, vector=None, fill=0):
        '''Inserts a new row or column before the indicated row or
        column n, counting from top to bottom for rows and left to right
        for columns.  Set n to self.r to insert after the bottom row or
        self.c to insert after the rightmost column.  The new elements
        are filled with the value of fill.
 
        If vector is not None, then the vector's values are inserted into
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
            if vector is not None:
                if vector.len != self.r:
                    raise TypeError("vector must have {} elements".format(
                                    self.r))
                v = vector if vector.is_col_vector else vector.t
            else:
                v = vector(self.r, c=True, fill=fill)
            # Operate on the transpose so we can use insert for rows
            m = self.t
            if concat:
                m.insert(self.c, c=False, vector=v)
            else:
                m.insert(n, c=False, vector=v)
            self._grid = m.t._grid
            self._c += 1
        else:
            concat = True if n == self.r else False
            n = n + self.r if n < 0 else n
            if not (0 <= n < self.r) and not concat:
                raise ValueError("n must be between 0 "
                                 "and {}".format(self.r - 1))
            if vector is not None:
                if vector.len != self.c:
                    raise TypeError("vector must have {} elements".format(
                                    self.c))
                v = vector if vector.is_row_vector else vector.t
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
        if not isinstance(m, Matrix):
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
        elif isinstance(n, int):
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
        elif not isinstance(n, str) and isinstance(n, Iterable):
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
        if not isinstance(r, int) and not isinstance(c, int):
            raise TypeError("r and c must be integers")
        if r < 1 or c < 1:
            raise ValueError("r and c must be > 0")
        # Flatten self._grid
        L = list(chain.from_iterable(self._grid))
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
        if not isinstance(n, int): 
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
        if not isinstance(m, Matrix):
            raise TypeError("m must be a Matrix instance")
        self.numtype = m._numtype
        self.frozen = m._frozen
        self.sigfig = m._sigfig
    def _flatten(self):
        'Convert self._grid to a flat list'
        if isinstance(self._grid[0], list):
            # Note this only flattens the first level of nesting:
            # [[1, 2], [3, 4, [5, 6]]] --> [1, 2, 3, 4, [5, 6]]
            self._grid = list(chain.from_iterable(self._grid))
    def _nested(self):
        'Convert self._grid to a nested list'
        if not isinstance(self._grid[0], list):
            self._grid = [list(i) for i in 
                         zip_longest(*([iter(self._grid)]*self.c))]
    def _get_sigfig(self, other=None):
        '''Return the sigfig value to use for a comparison.  If
        Matrix.SigFig is not None, return it.  Otherwise, return the
        smaller of self.sigfig and other.sigfig.
        '''
        if Matrix.SigFig is not None:
            if not isinstance(Matrix.SigFig, int):
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
                if isinstance(x, (float, Decimal)):
                    return str(RoundOff(float(x), digits))
                elif isinstance(x, Complex):
                    # This is a bit of a hack to get self's sigdig
                    # setting to the Complex instance (but it works).
                    x.sigdig = digits
                    return str(x)
                elif isinstance(x, complex):
                    if Matrix.use_Complex:
                        return str(Complex(RoundOff(x, digits)))
                    return str(RoundOff(x, digits))
                else:
                    return str(x)
            else:
                if isinstance(x, complex) and Matrix.use_Complex:
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
    def from_list(*p, **kw):
        '''Instantiate a matrix from a list.  These are the valid forms:
 
        Nested list:  A single argument is a list [L1, L2, ..., Ln]
        where each of the L's is a sequence of length m.  This will
        result in a matrix of n rows and m columns.
 
        Flat list with size, such as
            matrix([1, 2, 3, 4], size=(2, 2))
            matrix(1, 2, 3, 4, size=(2, 2))
 
        Flat list with no size, which will return a row vector.
 
        Examples:
            matrix([[1, 2, 3]]) and matrix(1, 2, 3) return the row vector
                1 2 3
            matrix([[1], [2], [3]]) returns the column vector
                1
                2
                3
            matrix([[1, 2, 3], [4, 5, 6]]) returns the matrix
                1 2 3
                4 5 6
            matrix([1, 2, 3, 4], size=(2, 2)) returns the matrix
                1 2
                3 4
            as does matrix(1, 2, 3, 4, size=(2, 2)).
        '''
        # Four valid forms for p:
        #   A:  p = ([[1, 2], [3, 4]],)     Nested list
        #   B:  p = ([1, 2, 3, 4],), size   Flat list with size
        #   C:  p = (1, 2, 3, 4), size      Flat list with size
        #   D:  p = (1, 2, 3, 4)            Flat list with no size (vector)
        size = kw.get("size", None)
        numtype = kw.get("numtype", None)
        if size is None:
            # Form A or D
            if len(p) == 1 and isinstance(p[0], Iterable):
                # Form A (nested list)
                r, c = len(p[0]), len(p[0][0])
                if not all([len(i) == c for i in p[0]]):
                    raise TypeError("Not all rows have {} elements".format(c))
                m = Matrix(r, c)
                m._grid = p[0]
                if numtype is not None:
                    m.numtype = numtype
                return m
            else:
                # Form D:  return a row vector
                assert(len(p) > 1)  # Otherwise would have identity matrix
                return vector(*p)
        else:
            # Form B or C
            e = TypeError("size keyword must be a tuple of two integers")
            try:
                r, c = size
            except ValueError:
                raise e
            if not (isinstance(r, int) and isinstance(c, int)):
                raise e
            # flat == True for form B, False for form C
            flat = len(p) == 1 and isinstance(p[0], Iterable)
            m = Matrix(r, c)
            with Flatten(m):
                m._grid = p[0] if flat else p
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
    def getnum(x, numtype=None, expr=None):  
        '''Returns the number x; if it is a string, the method tries to
        identify it and return it in the most appropriate form.  If numtype
        is not None, then it will be coerced to the indicated type.
        '''
        if expr is not None and isinstance(x, str):
            # Assume x is an expression to be evaluated with globals
            # dictionary expr[0] and locals dictionary expr[1].
            return eval(x, expr[0], expr[1])
        if numtype is not None:
            return Matrix.NumberConvert(x, numtype)
        if not isinstance(x, str):
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
            if isinstance(x, complex):
                return ufloat(x.real, 0)    #**
            elif isinstance(x, (Fraction, Decimal)):
                return ufloat(float(x), 0)  #**
            elif isinstance(x, UFloat):
                return x
            return ufloat(x, 0)
        elif T is complex:
            if have_unc and isinstance(x, UFloat):
                return complex(x.nominal_value, 0)  #**
            return complex(x, 0)    #**
        elif isinstance(x, float):
            if T is Decimal or T is Fraction:
                return T(str(x))
            return T(x)
        elif isinstance(x, complex):
            if T is Decimal or T is Fraction:
                return T(str(x.real))   #**
            return T(x.real)    #**
        elif isinstance(x, Fraction):
            if T is Decimal:
                return Decimal(x.numerator)/Decimal(x.denominator)
            elif have_mpmath and T is mpmath.mpf:
                return mpmath.mpf(x.numerator)/mpmath.mpf(x.denominator)
        elif isinstance(x, Decimal):
            if have_mpmath and T is mpmath.mpf:
                n, d = x.as_integer_ratio()
                return mpmath.mpf(n)/mpmath.mpf(d)
        elif have_mpmath and isinstance(x, mpmath.mpf):
            if T is Fraction:
                return Fraction(extract(str(x)))
            elif T is Decimal:
                return Decimal(extract(str(x)))
        elif have_unc and isinstance(x, UFloat):
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
            return x.conjugate() if isinstance(x, complex) else x
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
            if isinstance(m[row, col], complex):
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
        return matrix([d])
    @diag.setter
    def diag(self, seq):
        'Set the diagonal elements to those of seq, a list or vector'
        self._check_frozen()
        if not self.is_square:
            raise TypeError("Matrix must be square to set diagonal")
        if (not isinstance(seq, (list, tuple)) and 
            (isinstance(seq, Matrix) and not seq.is_vector)):
            raise TypeError("seq must be list, tuple, or vector")
        e = TypeError("seq must be of length {}".format(self.r))
        if isinstance(seq, Matrix):
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
                if not isinstance(x, complex) and not isinstance(y, complex):
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
            return all([not isinstance(i, complex) for i in self.diag.l])
        except Exception:
            return False
    @property
    def is_int(self): 
        'Return True if all matrix elements are integers.'
        return all([isinstance(i, int) for i in self.l])
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
        return any([isinstance(i, complex) for i in self.l])
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
        return not any([isinstance(i, complex) for i in self.l])
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
        # Note this only flattens the first level of nesting:
        # [[1, 2], [3, 4, [5, 6]]] --> [1, 2, 3, 4, [5, 6]]
        return list(chain.from_iterable(self.copy._grid))
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
        if value is not None and not isinstance(value, int):
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
        if not isinstance(value, (list, tuple)):
            raise e
        if not isinstance(value[0], int) and not isinstance(value[1], int):
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
            if isinstance(x, Matrix):
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
    to the original matrix will not be current.  One defence for this is
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
        if isinstance(real, (int, float, Fraction, Decimal)):
            re = float(real)
        elif isinstance(real, (complex, Complex)):
            re, im = real.real, real.imag
        elif isinstance(real, str):
            if imag is not None:
                raise TypeError("imag not allowed if real is string")
            re, im = Matrix.PC(real)
        else:
            raise TypeError("real must be a string or number")
        if imag is not None:
            if isinstance(imag, (int, float, Fraction, Decimal)):
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

if True: # Utility functions
    def matrix(*p, **kw):
        '''Convenience function for instantiating Matrix objects.  Examples:
        Integer
          matrix(4):  Return an identity matrix of size 4
          matrix(4, fill=x):  Return size 4 square matrix filled with x
        String
          matrix("1 2\\n3 4")
          matrix("1 2; 3 4", ";")
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
        if len(p) == 1 and isinstance(p[0], int):
            if "size" in kw:
                raise TypeError("size keyword not allowed here")
            m = Matrix.identity(p[0])
            if "fill" in kw:
                with Flatten(m):
                    m._grid = [kw["fill"]]*len(m._grid)
            return m
        elif isinstance(p[0], str):
            return Matrix.from_string(*p, **kw)
        elif len(p) > 1 or isinstance(p[0], list):
            return Matrix.from_list(*p, **kw)
        elif hasattr(p[0], "read"):
            return matrix(p[0].read())
        else:
            raise NotImplementedError
    def vector(*p, **kw):

        '''Convenience function for instantiating row and column
        vectors.  Returns a row vector by default; use keyword "c" to
        get a column vector.
    
        vector(2) --> [0 0]
        vector(2, fill=7) --> [7 7]
        vector(2, fill="7") --> ["7" "7"]
        vector(*[1, 2, 3]) --> [1 2 3]
        vector([1, 2, 3]) --> [1 2 3]
        vector("1 2 3") --> [1 2 3]
        '''
        c = kw.get("c", False)
        if "c" in kw:
            del kw["c"]
        fill = kw.get("fill", 0)
        if c:
            # Make a column vector
            if isinstance(p[0], int):
                return Matrix(p[0], 1, fill=fill)
            elif isinstance(p[0], str):
                m = Matrix.from_string(*p, **kw)
                if m.c != 1:
                    raise ValueError("String is not valid column vector")
                return m
            elif isinstance(p[0], (tuple, list)):
                m = Matrix.from_list(*p[0], **kw)
                xx()
                if m.c != 1:
                    if m.r == 1:
                        # It was entered as a row vector
                        m = m.t
                    else:
                        raise ValueError("List is not valid column vector\n"
                            "Must be of form [[a], [b], ..., [c]].")
                return m
            else:
                raise NotImplementedError
        else:
            # Make a row vector
            if isinstance(p, (tuple, list)) and len(p) > 1:
                m = Matrix(1, len(p))  # Row vector
                with Flatten(m):
                    m._grid = list(p)
                return m
            elif isinstance(p[0], int):
                return Matrix(1, p[0], fill=fill)
            elif isinstance(p[0], str):
                m = Matrix.from_string(*p, **kw)
                if m.r != 1:
                    raise ValueError("String is not valid row vector")
                return m
            elif isinstance(p[0], (tuple, list)):
                m = Matrix.from_list(*p[0], **kw)
                if m.r != 1:
                    raise ValueError("List is not valid row vector.\n"
                        "Must be of form [[a, b, ..., c]].")
                return m
            else:
                raise NotImplementedError
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
        if isinstance(number, (int, Fraction)):
            return number
        if have_unc and isinstance(number, UFloat):
            return number
        if isinstance(number, complex):
            re = RoundOff(number.real, digits=digits)
            im = RoundOff(number.imag, digits=digits)
            return complex(re, im)
        can_convert = False
        if convert and not isinstance(number, Decimal):
            try:
                float(number)
                can_convert = True
            except ValueError:
                pass
        if isinstance(number, float) or (convert and can_convert):
            # Convert to a decimal, then back to a float
            x = Decimal(number)
            with localcontext() as ctx:
                ctx.prec = digits
                x = +x
                return float(x)
        elif isinstance(number, complex):
            return complex(
                RoundOff(number.real, digits=digits, convert=True),
                RoundOff(number.imag, digits=digits, convert=True)
                )
        elif isinstance(number, Decimal):
            with localcontext() as ctx:
                ctx.prec = digits
                number = +number
                return number
        elif have_mpmath and isinstance(number, mpmath.mpf):
            x = Decimal(mpmath.nstr(number, mpmath.mp.dps))
            with localcontext() as ctx:
                ctx.prec = digits
                x = +x
                s = str(x)
                return mpmath.mpf(s)
        elif have_mpmath and isinstance(number, mpmath.mpc):
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
    m = matrix("1 mpmath.mpc(2)\n3-5j 4.3(1)")
