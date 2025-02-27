"""
TODO:
    * Quadrilateral must verify the shape is convex.
      https://en.wikipedia.org/wiki/Quadrilateral#Concave_quadrilaterals
      gives the definition that a concave quadrilateral has one interior
      angle > 180 deg and one of the two diagonals lies outside the
      quadrilateral.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2010 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # <math> A collection of plane geometry formulas
    ##∞what∞#
    ##∞test∞# run #∞test∞#
    pass
if 1:  # Imports
    import collections
    from math import pi, atan, hypot, sqrt, asin
    from pdb import set_trace as xx
if 1:  # Custom imports
    from util import IsIterable, IsConvexPolygon
    from roundoff import RoundOff


def ArePoints(*points, n=2):
    """Return True if each of the parameters are n-tuples of numbers or
    objects that can be converted to numbers using float().
    """
    for p in points:
        if not IsIterable(p) or len(p) != n:
            return False
        try:
            [float(i) for i in p]
        except Exception:
            return False
    return True


def Det(*a):
    """Determinant of a 3 dimensional matrix (a[0] is element (1, 1),
    a[1] is element (1, 2), etc.).
    """
    assert len(a) == 9
    return (
        a[0] * (a[4] * a[8] - a[7] * a[5])
        - a[1] * (a[3] * a[8] - a[6] * a[5])
        + a[2] * (a[3] * a[7] - a[4] * a[6])
    )


def TriangleCircumscribedCircle(p1, p2, p3):
    """Return the (radius, center) of the circumscribed circle for the
    triangle of the 3 given points.  The Cartesian coordinates of the
    vertices of the triangle are in the points p1, p2, p3; each are
    2-vectors.
    """
    # Formulas and notation from
    # https://en.wikipedia.org/wiki/Circumscribed_circle
    if not ArePoints(p1, p2, p3, n=2):
        raise ValueError("Not all arguments are points")
    Ax, Ay = p1
    Bx, By = p2
    Cx, Cy = p3
    A = hypot(Ax, Ay)
    B = hypot(Bx, By)
    C = hypot(Cx, Cy)
    A2, B2, C2 = A * A, B * B, C * C
    Sx = Det(A2, Ay, 1, B2, By, 1, C2, Cy, 1) / 2
    Sy = Det(Ax, A2, 1, Bx, B2, 1, Cx, C2, 1) / 2
    a = Det(Ax, Ay, 1, Bx, By, 1, Cx, Cy, 1)
    b = Det(Ax, Ay, A2, Bx, By, B2, Cx, Cy, C2)
    if not a:
        raise ValueError("Points are collinear")
    center = (RoundOff(Sx / a), RoundOff(Sy / a))
    radius = RoundOff(sqrt(b / a + (hypot(Sx, Sy) / a) ** 2))
    return radius, center


def TriangleInscribedCircle(p1, p2, p3):
    """Return the (radius, center) of the inscribed circle for the
    triangle of the 3 given points.  The Cartesian coordinates of the
    vertices of the triangle are in the points p1, p2, p3; each are
    2-vectors.
    """
    if not ArePoints(p1, p2, p3, n=2):
        raise ValueError("Not all arguments are points")
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    # Length of the three sides
    a = hypot(x2 - x3, y2 - y3)
    b = hypot(x1 - x3, y1 - y3)
    c = hypot(x1 - x2, y1 - y2)
    s = a + b + c
    assert s and s > 0
    # Radius from http://mathworld.wolfram.com/Inradius.html
    radius = RoundOff(sqrt(((b + c - a) * (c + a - b) * (a + b - c)) / s) / 2)
    # Incircle center from http://mathworld.wolfram.com/Incenter.html.
    cx = RoundOff((a * x1 + b * x2 + c * x3) / s)
    cy = RoundOff((a * y1 + b * y2 + c * y3) / s)
    return radius, (cx, cy)


# For some quadrilateral formulas, see
# http://www.geometryatlas.com/categories/Quadrilaterals-General
def Quadrilateral(p1, p2, p3, p4):
    """For a convex quadrilateral, return a dictionary containing the
    following keys:
        area, perimeter
        d1, d2          Length of diagonals
        a, b, c, d      Length of sides
        A, B, C, D      Internal angles in radians
        theta           Angle between diagonals in radians

    Important:  the quadrilateral must be a convex quadrilateral for
    these equations to hold.

    The Cartesian coordinates of the vertices of the quadrilateral
    are in the points p1, p2, p3, p4; each are 2-vectors.  p1 must be
    adjacent to p2 which is adjacent to p3 which is adjacent to p4
    (i.e., name the points sequentially around a circle).
    """
    raise Exception("Not tested yet")
    if not ArePoints(p1, p2, p3, p4, n=2):
        raise ValueError("Not all arguments are points")
    if not IsConvexPolygon(p1, p2, p3, p4):
        raise ValueError("Quadrilateral is not convex")
    results = {}
    x = [p1[0], p2[0], p3[0], p4[0]]
    y = [p1[1], p2[1], p3[1], p4[1]]
    results["a"] = hypot(x[0] - x[1], y[0] - y[1])
    results["b"] = hypot(x[1] - x[2], y[1] - y[2])
    results["c"] = hypot(x[2] - x[3], y[2] - y[3])
    results["d"] = hypot(x[3] - x[1], y[3] - y[1])
    # Diagonals
    results["d1"] = hypot(x[0] - x[2], y[0] - y[2])
    results["d2"] = hypot(x[1] - x[3], y[1] - y[3])
    # Calculate the smaller central angle of the diagonals.  Do this by
    # calculating the dot product of the two diagonals.
    r1x, r1y = x[0] - x[2], y[0] - y[2]
    r2x, r2y = x[1] - x[3], y[1] - y[3]
    r1, r2 = hypot(r1x, r1y), hypot(r2x, r2y)
    sintheta = (r1x * r2x + r1y * r2y) / (r1 * r2)
    theta = asin(sintheta)
    d["theta"] = min(theta, pi - theta)
    # Area is one-half the cross product of the diagonal vectors
    d["area"] = abs(r1x * r2y - r2x * r1y) / 2
    # Area check:  http://www.geometryatlas.com/entries/165 (click on M)

    A = abs(
        (
            (
                (y[0] * x[1])
                + (y[0] * x[3] * (-1))
                + (y[1] * x[0] * (-1))
                + (y[1] * x[2])
                + (y[2] * x[1] * (-1))
                + (y[2] * x[3])
                + (y[3] * x[0])
                + (y[3] * x[2] * (-1))
            )
            * 1
            / 2
        )
    )
    assert abs(d["area"] / A - 1) < 1e-14

    return results


def QuadrilateralArea(p1, p2, p3, p4):
    """The Cartesian coordinates of the vertices of the quadrilateral
    are the points p1, p2, p3, p4; each are 2-vectors.
    """
    # From http://www.geometryatlas.com/entries/165 (click on the
    # circled M button).
    if not ArePoints(p1, p2, p3, p4, n=2):
        raise ValueError("Not all arguments are points")
    x0, x1, x2, x3 = p1[0], p2[0], p3[0], p4[0]
    y0, y1, y2, y3 = p1[1], p2[1], p3[1], p4[1]
    return abs(y0 * (x1 - x3) + y1 * (x2 - x0) + y2 * (x3 - x1) + y3 * (x0 - x2)) / 2


def QuadrilateralPerimeter(p1, p2, p3, p4):
    """The Cartesian coordinates of the vertices of the quadrilateral
    are in the points p1, p2, p3, p4; each are 2-vectors.
    """
    if not ArePoints(p1, p2, p3, p4, n=2):
        raise ValueError("Not all arguments are points")
    x = [p1[0], p2[0], p3[0], p4[0]]
    y = [p1[1], p2[1], p3[1], p4[1]]
    return (
        ((x[0] + (x[1] * (-1))) ** (2) + (y[0] + (y[1] * (-1))) ** (2)) ** (1 / 2)
        + (((x[0] * (-1)) + x[3]) ** (2) + ((y[0] * (-1)) + y[3]) ** (2)) ** (1 / 2)
        + ((x[1] + (x[2] * (-1))) ** (2) + (y[1] + (y[2] * (-1))) ** (2)) ** (1 / 2)
        + ((x[2] + (x[3] * (-1))) ** (2) + (y[2] + (y[3] * (-1))) ** (2)) ** (1 / 2)
    )


def QuadrilateralAngles(p1, p2, p3, p4):
    """Returns the four interior angles in radians of a quadrilateral.
    The Cartesian coordinates of the vertices of the quadrilateral are
    in the points p1, p2, p3, p4; each are 2-vectors.
    """
    if not ArePoints(p1, p2, p3, p4, n=2):
        raise ValueError("Not all arguments are points")
    x = [p1[0], p2[0], p3[0], p4[0]]
    y = [p1[1], p2[1], p3[1], p4[1]]
    # Equations from http://www.geometryatlas.com/entries/172 (click on
    # the circled M button).
    try:
        a = atan(
            (
                (
                    (((y[0] * (-1)) + y[3]) * ((x[2] * (-1)) + x[3]) * (-1))
                    + ((y[2] + (y[3] * (-1))) * (x[0] + (x[3] * (-1))))
                )
                * (
                    (((x[2] * (-1)) + x[3]) * (x[0] + (x[3] * (-1))))
                    + ((y[2] + (y[3] * (-1))) * ((y[0] * (-1)) + y[3]))
                )
                ** (-1)
            )
        )
    except ZeroDivisionError:
        a = pi / 2
    try:
        b = pi + (
            atan(
                (
                    (
                        ((y[0] + (y[1] * (-1))) * ((x[1] * (-1)) + x[2]) * (-1))
                        + ((y[1] + (y[2] * (-1))) * ((x[0] * (-1)) + x[1]))
                    )
                    * (
                        (((x[1] * (-1)) + x[2]) * ((x[0] * (-1)) + x[1]))
                        + ((y[1] + (y[2] * (-1))) * (y[0] + (y[1] * (-1))))
                    )
                    ** (-1)
                )
            )
            * (-1)
        )
    except ZeroDivisionError:
        b = pi / 2
    try:
        c = pi + (
            atan(
                (
                    (
                        ((y[0] + (y[1] * (-1))) * (x[0] + (x[3] * (-1))))
                        + (((y[0] * (-1)) + y[3]) * ((x[0] * (-1)) + x[1]) * (-1))
                    )
                    * (
                        (((x[0] * (-1)) + x[1]) * (x[0] + (x[3] * (-1))))
                        + (((y[0] * (-1)) + y[3]) * (y[0] + (y[1] * (-1))))
                    )
                    ** (-1)
                )
            )
            * (-1)
        )
    except ZeroDivisionError:
        c = pi / 2
    d = 2 * pi - (a + b + c)
    return (a, b, c, d)


def QuadrilateralDiagonals(p1, p2, p3, p4):
    """Returns the lengths of the two diagonals of a quadrilateral.
    The Cartesian coordinates of the vertices of the quadrilateral are
    in the points p1, p2, p3, p4; each are 2-vectors.
    """
    if not ArePoints(p1, p2, p3, p4, n=2):
        raise ValueError("Not all arguments are points")
    x = [p1[0], p2[0], p3[0], p4[0]]
    y = [p1[1], p2[1], p3[1], p4[1]]
    d1 = hypot(x[0] - x[2], y[0] - y[2])
    d2 = hypot(x[1] - x[3], y[1] - y[3])
    return (d1, d2)


if __name__ == "__main__":
    from lwtest import run, assert_equal, raises, Assert

    def TestDet():
        a = (1, 0, 0, 0, 1, 0, 0, 0, 1)
        assert_equal(Det(*a), 1)
        assert_equal(Det(*range(1, 10)), 0)

    def TestTriangleCircumscribedCircle():
        """Unit circle with center at origin."""
        p = ((-1, 0), (0, 1), (1, 0))
        r, c = TriangleCircumscribedCircle(*p)
        assert_equal(r, 1)
        assert_equal(c[0], 0)
        assert_equal(c[1], 0)
        p = ((0, 1), (1, 0), (-1, 0))
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
        """From a graphical construction; numbers in mm.  This was a 45
        degree isosceles right triangle with the right angle at the origin.
        The right-most point was p3 and the highest point was p2.  The
        measured incircle diameter was 28.6 mm with measured center at
        (28.5, 28.5).
        """
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
        for p in (
            (p1, p2, p3, p4),
            (p4, p1, p2, p3),
            (p3, p4, p1, p2),
            (p2, p3, p4, p1),
        ):
            A = QuadrilateralArea(*p)
            # print(p, A, a*a)
            assert_equal(A, a * a)

    exit(run(globals(), halt=0)[0])
