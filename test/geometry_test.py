import sys
from geometry import TriangleCircumscribedCircle, TriangleInscribedCircle
from geometry import QuadrilateralArea, QuadrilateralAngles
from geometry import QuadrilateralPerimeter, QuadrilateralDiagonals
from geometry import Det, IsIterable, ArePoints
from lwtest import run, assert_equal, raises
from pdb import set_trace as xx
if 0:
    import debug
    debug.SetDebugger()

def TestDet():
    a = (1, 0, 0, 0, 1, 0, 0, 0, 1)
    assert_equal(Det(*a), 1)
    assert_equal(Det(*range(1, 10)), 0)

def TestTriangleCircumscribedCircle():
    '''Unit circle with center at origin.
    '''
    p  = ((-1, 0), (0, 1), (1, 0))
    r, c = TriangleCircumscribedCircle(*p)
    assert_equal(r, 1)
    assert_equal(c[0], 0)
    assert_equal(c[1], 0)
    p  = ((0, 1), (1, 0), (-1, 0))
    r, c = TriangleCircumscribedCircle(*p)
    assert_equal(r, 1)
    assert_equal(c[0], 0)
    assert_equal(c[1], 0)
    p = ((1, 0), (-1, 0), (0, 1))
    r, c = TriangleCircumscribedCircle(*p)
    assert_equal(r, 1)
    assert_equal(c[0], 0)
    assert_equal(c[1], 0)

def TestTriangleInscribedCircle():
    '''From a graphical construction; numbers in mm.  This was a 45
    degree isoceles right triangle with the right angle at the origin.
    The right-most point was p3 and the highest point was p2.  The
    measured incircle diameter was 28.6 mm with measured center at
    (28.5, 28.5).
    '''
    a = 98.3
    p1 = (0, 0)
    p2 = (0, a)
    p3 = (a, 0)
    r0 = 28.79140340936
    tol = 2e-12
    for p in ((p1, p2, p3), (p3, p1, p2), (p2, p3, p1)):
        r, c = TriangleInscribedCircle(*p)
        assert_equal(r, r0, reltol=tol)
        assert_equal(c[0], r0, reltol=tol)
        assert_equal(c[1], r0, reltol=tol)

def TestQuadrilateralArea():
    a = 2.345
    p1 = (0, 0)
    p2 = (0, a)
    p3 = (a, a)
    p4 = (a, 0)
    # Test each permutation
    for p in ((p1, p2, p3, p4), (p4, p1, p2, p3),
        (p3, p4, p1, p2), (p2, p3, p4, p1)):
        A = QuadrilateralArea(*p)
        #print(p, A, a*a)
        assert_equal(A, a*a)

if __name__ == "__main__":
    exit(run(globals(), halt=0, dbg=0)[0])
