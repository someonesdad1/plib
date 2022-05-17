'''
Interactive script for various circle calculations:
    1. Circle through three points
    2. Segment area
    3. Sector area
    4. 3 mutually tangent circles given their centers
 
See http://mathworld.wolfram.com/TangentCircles.html for details.
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
    # Program description string
    #∞what∞#
    #∞test∞# --test #∞test∞#
    pass
if 1:   # Imports
    import sys
    from math import *
    from fractions import Fraction
    import getopt
    from pdb import set_trace as xx
if 1:   # Custom imports
    from get import GetNumber
    from wrap import dedent
    from roundoff import RoundOff
    from lwtest import run, assert_equal, raises
def Error(msg, status=1, end=True):
    print(msg, file=sys.stderr)
    exit(status)
def Det(matrix):
    '''Calculate the determinant of a 3x3 matrix.  matrix must be a
    sequence of 3 sequences containing numbers.
    '''
    a1, a2, a3 = matrix[0]
    a4, a5, a6 = matrix[1]
    a7, a8, a9 = matrix[2]
    d = a1*(a5*a9 - a6*a8) - a2*(a4*a9 - a6*a7) + a3*(a4*a8 - a5*a7)
    return RoundOff(d)
def Circ3Pts(p1, p2, p3):
    '''Equations from http://mathworld.wolfram.com/Circle.html
    '''
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    hyp = lambda a, b:  a*a + b*b
    h1, h2, h3 = hyp(x1, y1), hyp(x2, y2), hyp(x3, y3)
    a = Det(((x1, y1, 1), (x2, y2, 1), (x3, y3, 1)))
    d = -Det(((h1, y1, 1), (h2, y2, 1), (h3, y3, 1)))
    e = Det(((h1, x1, 1), (h2, x2, 1), (h3, x3, 1)))
    f = -Det(((h1, x1, y1), (h2, x2, y2), (h3, x3, y3)))
    if not a:
        raise ValueError("Points are collinear")
    IfNearZero = lambda x:  0 if abs(x) < 1e-15 else x
    x = RoundOff(-d/(2*a))
    y = RoundOff(-e/(2*a))
    r = RoundOff((d*d + e*e)/(4*a*a) - f/a)
    if r < 0:
        raise ValueError("r is negative = " + str(r))
    return x, y, r
def Circle3Points():
    print("\nEnter the three points:")
    p1 = GetPoint("(x1, y1) = ? ")
    p2 = GetPoint("(x2, y2) = ? ")
    p3 = GetPoint("(x3, y3) = ? ")
    print("\nValues input:")
    print("  (x1, y1) =", str(p1))
    print("  (x2, y2) =", str(p2))
    print("  (x3, y3) =", str(p3))
    x, y, r = Circ3Pts(p1, p2, p3)
    print("\nResults:")
    print("  Center is", str((x, y)))
    print("  Radius is", r)
    print("  Diameter is", 2*r)
def TangentCenters(p1, p2, p3):
    '''Given three noncollinear points p1, p2, and p3, these points
    determine three circles that are mutually tangent.  Return a
    sequence (r1, r2, r3) of the radii of these circles.
 
    Ref.  http://mathworld.wolfram.com/TangentCircles.html, equations
    5, 6, 7.
    '''
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    D = Det(((x1, y1, 1), (x2, y2, 1), (x3, y3, 1)))
    if not D:
        raise ValueError("Points are collinear")
    # Calculate the lengths of the sides
    a = hypot(x1 - x2, y1 - y2)
    b = hypot(x2 - x3, y2 - y3)
    c = hypot(x3 - x1, y3 - y1)
    # Equations 5, 6, 7
    ra = (-a + b + c)/2
    rb = (a - b + c)/2
    rc = (a + b - c)/2
    return ra, rb, rc
def ThreeTangentCenters():
    print("\nEnter the circle's center points:")
    p1 = GetPoint("(x1, y1) = ? ")
    p2 = GetPoint("(x2, y2) = ? ")
    p3 = GetPoint("(x3, y3) = ? ")
    r = TangentCenters(p1, p2, p3)
    print("\nCircle radii =", str(r).replace("(", "").replace(")", ""))
def CircleSegment():
    CircleSector(segment=True)
def GetPoint(prompt, default_response="", test=None):
    '''Return a tuple (x, y) gotten from prompting the user.  If you
    use a comma, you can use expressions with spaces in them.
 
    If test is not None, then it is the string that is parsed.
    '''
    while True:
        if test:
            s = test
        else:
            if prompt:
                print(prompt, end="")
            if default_response:
                print("[{}]".format(default_response), end="")
            s = input().strip().lower()
        if s == "q":
            exit(0)
        elif not s:
            s = default_response
        # Split the string
        eval_expr = False
        if "," in s:
            f = [i.strip() for i in s.split(",")]
            eval_expr = True
        else:
            f = s.split()
        # Must have two components
        if len(f) != 2:
            print(dedent('''
            You must enter two numbers or expressions separated by a space or comma.
            If you use a comma, the two expressions can contain spaces.
            '''))
            continue
        # Convert them to numbers
        try:
            x = eval(f[0])
            y = eval(f[1])
        except Exception:
            print("'{}' contains an invalid expression".format(s))
            continue
        return (x, y)
def GetInput(prompt, default_response="", acceptable=[], lower=True):
    '''Prompt the user and get a response.  If default_response is
    given, it's what is returned if the user just hits the Enter key.
    If acceptable is not empty, then the responses must be in this
    container.  If lower is True, convert the responses to lower case
    before testing.
    '''
    while True:
        answer = input(prompt).strip()
        ans = answer.lower() if lower else answer
        if ans == "":
            return default_response
        elif ans in acceptable:
            return answer
        elif ans == "q":
            exit(0)
        print("'{}' is not a proper response.".format(answer))
def CircleSector(segment=False):
    name = "segment" if segment else "sector"
    print('''
Find {name}'s area given:
  1.  Angle and diameter.
  2.  Arc length and diameter.
  3.  Width and diameter.'''.format(**locals()))
    choices = ("1", "2", "3")
    ans = GetInput("Problem choice? [1] ", default_response="1",
                   acceptable=choices)
    if ans == "1":
        r = GetNumber("What is the diameter? ", low=0, low_open=True)/2
        theta_deg = GetNumber("What is the angle in degrees? ", low=0)
        theta = (2*pi if theta_deg == 360 else
                 fmod(theta_deg, 360)*pi/180)
        area = SectorArea_r_theta(r, theta, segment=segment)
    elif ans == "2":
        r = GetNumber("What is the diameter? ", low=0, low_open=True)/2
        max_b = 2*pi*r
        b = GetNumber("What is the arc length? ", low=0, high=max_b)
        area = SectorArea_r_b(r, b, segment=segment)
    elif ans == "3":
        r = GetNumber("What is the diameter? ", low=0, low_open=True)/2
        s = GetNumber("What is the width? ", low=0, low_open=True)
        area = SectorArea_r_s(r, s, segment=segment)
    else:
        raise Exception("Bug")
    print("\nArea =", RoundOff(area))
def SectorArea_r_theta(r, theta, segment=False):
    '''Sector/segment area given angle and diameter.
    '''
    area = r**2*theta/2
    if segment:
        area -= r**2*sin(theta)/2
    return area
def SectorArea_r_b(r, b, segment=False):
    '''Sector/segment area given arc length and diameter.
    '''
    area = r*b/2
    if segment:
        area -= r**2*sin(b/r)/2
    return area
def SectorArea_r_s(r, s, segment=False):
    '''Sector/segment area given width and diameter.
    '''
    theta = 2*asin(s/(2*r))
    area = r**2*theta/2
    if segment:
        area -= r**2*sin(theta)/2
    return area
if 1:   # Unit-test functions
    def TestSectorArea():
        # Radius, angle
        r, theta = 1, 2*pi      # Unit circle
        for n in range(1, 11):
            assert_equal(SectorArea_r_theta(r, theta/n), pi/n)
        # Radius, arc length
        r, b = 1, 2*pi
        assert_equal(SectorArea_r_b(r, b), pi*r**2)
        # Radius, width
        r, s = 1, 2     # Unit circle, on diameter
        assert_equal(SectorArea_r_s(r, s), pi*r**2/2)
    def TestSegmentArea():
        # Radius, angle
        r, theta = 1, pi/2
        A = (theta - 1)/2
        assert_equal(SectorArea_r_theta(r, theta, segment=True), A)
        # Radius, arc length
        r, b = 1, 2*pi
        assert_equal(SectorArea_r_b(r, b, segment=True), pi*r**2)
        r, b = 1, pi/2
        assert_equal(SectorArea_r_b(r, b, segment=True), A)
        # Radius, width
        r, s = 1, 2     # Unit circle, on diameter
        assert_equal(SectorArea_r_s(r, s, segment=True), pi*r**2/2)
        r, s = 1, sqrt(2)     # Unit circle, 90 degrees
        assert_equal(SectorArea_r_s(r, s, segment=True), A, abstol=1e-15)
    def TestCircleThroughThreePoints():
        # Unit circle at origin
        x, y, r = Circ3Pts((1, 0), (0, 1), (-1, 0))
        assert_equal(x, 0)
        assert_equal(y, 0)
        assert_equal(r, 1)
    def TestTangentCenters():
        # Equilateral triangle with base of length 2 centered on x axis;
        # each circle will be a unit circle.
        p1, p2, p3 = (-1, 0), (1, 0), (0, sqrt(3))
        for i in TangentCenters(p1, p2, p3):
            assert_equal(i, 1, reltol=1e-15)
    def TestGetPoint():
        x, y = GetPoint("", test="0 0")
        assert(not x and not y)
        x, y = GetPoint("", test="1 0")
        assert(x == 1 and not y)
        x, y = GetPoint("", test="1 2")
        assert(x == 1 and y == 2)
        x, y = GetPoint("", test="1 sqrt(3)")
        assert(x == 1 and y == sqrt(3))
    def TestDet():
        d = Det(((1, 0, 0), (0, 1, 0), (0, 0, 1)))
        assert_equal(d, 1)
        d = Det(((-1, 0, 0), (0, -1, 0), (0, 0, -1)))
        assert_equal(d, -1)
        # 3x3 Hilbert matrix
        d = Det(((1, 1/2, 1/3), (1/2, 1/3, 1/4), (1/3, 1/4, 1/5)))
        f = lambda x: Fraction(1, x)
        ans = f(15) - f(16) - f(20) + f(12) - f(27)
        assert_equal(d, float(ans), reltol=1e-13)
if __name__ == "__main__":
    problems = (
        ("Circle through three points", Circle3Points),
        ("Segment area", CircleSegment),
        ("Sector area", CircleSector),
        ("3 mutually tangent circles given their centers",
         ThreeTangentCenters),
    )
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run(globals())
    else:
        print("Choose the problem to solve (q to quit):")
        d = {}
        for i, (name, function) in enumerate(problems):
            d[str(i + 1)] = (name, function)
            print("{0:4d}. {1}".format(i + 1, name))
        ok = False
        while not ok:
            ans = input("Which problem [1]? ").strip()
            if ans == "":
                ok = True
                ans = "1"
            elif ans in d:
                ok = True
            elif ans == "q":
                exit(0)
            if not ok:
                print("'{}' is not a proper response.".format(ans))
        function = d[ans][1]
        function()
