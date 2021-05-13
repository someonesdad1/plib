if 1:  # Imports
    from matrix import matrix, Matrix, Complex, MatrixContext, cross
    from matrix import Matrices, vector, dot, Flatten, have_unc, have_mpmath
    from matrix import have_sympy, random_matrix, RoundOff, ParseComplex
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

if __name__ == "__main__":
    SetupGlobalTestData()
    exit(run(globals(), halt=True)[0])
