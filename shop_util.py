'''

Todo
    - Update to python 3 semantics where needed
    - This is for old /shop scripts.  This functionality should be in get.py.
        - The root & interp stuff should be in other files
    - Once done, this module can be eliminated.

'''

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
import math
import sys
from f import flt

debug = 0
ii = isinstance

def GetDouble(prompt, default, low, high):
    if debug:
        return flt(default)
    str = ""
    while True:
        str = input(prompt + " [" + default + "] ").strip()
        if str == "":
            return flt(default)
        elif str == "q":
            exit(0)
        try:
            choice = flt(eval(str))
            if choice < low or choice > high:
                raise Exception()
            return choice
        except Exception:
            print(("'%s' not an acceptable number.  Must lie between %f " +
                  "and %f.") % (str, low, high))
def GetInt(prompt, default, low, high):
    if debug:
        return default
    str = ""
    while True:
        str = input(prompt + " [" + repr(default) + "] ").strip()
        if not str:
            return default
        elif str == "q":
            exit(0)
        try:
            choice = int(eval(str))
            if choice < low or choice > high:
                raise Exception()
            return choice
        except Exception:
            print(("'%s' not an acceptable integer.  Must lie between %d " +
                  "and %d.") % (str, low, high))
def GetChoice(prompt, default, choices, quit="q"):
    if debug:
        return default
    ok = False
    while not ok:
        choice = input(prompt + " [" + default + "] ").strip()
        if choice == "":
            return default
        elif choice == quit:
            exit(0)
        if choice in choices:
            ok = True
        else:
            print("Not a valid answer.  Must be one of the following\n" +
                  "  " + repr(choices))
    return choice
def root_find(x0, x2, f, eps, itmax):
    '''A root finding routine.  See "All Problems Are Simple" by Jack Crenshaw, Embedded Systems
    Programming, May, 2002, pg 7-14, jcrens@earthlink.com.  Can be downloaded from
    www.embedded.com/code.htm.
 
    Translated from Crenshaw's C code modified by Don Peterson 20 May 2003.
 
    Crenshaw states this routine will converge rapidly on most functions, typically adding 4 digits
    to the solution on each iteration.  The method is something called "inverse parabolic
    interpolation".  The routine works by starting with x0, x2, and finding a third x1 by
    bisection.  The ordinates are gotten, then a horizontally- opening parabola is fitted to the
    points.  The parabola's root's abscissa is gotten, and the iteration is repeated.
 
    The function root_find will find a root of the function f(x) in the interval [x0, x2].  We must
    have that f(x0)*f(x2) < 0.
 
    The root value is returned.
 
    Root lies between x0 and x2.  f is the function to evaluate; it takes one float argument and
    returns a float.  eps is the precision to find the root to and itmax is the maximum number of
    iterations allowed.
 
    Returns a tuple (x, numits) where
        x is the root.
        numits is the number of iterations taken.
    The routine will throw an exception if it receives bad input data or it doesn't converge.
    '''
    x1 = y0 = y1 = y2 = b = c = temp = y10 = y20 = y21 = xm = ym = 0.0
    xmlast = x0
    assert(x0 < x2)
    assert(eps > 0.0)
    assert(itmax > 0)
    y0 = f(x0)
    if y0 == 0.0:
        return x0, 0
    y2 = f(x2)
    if y2 == 0.0:
        return x2, 0
    if y2 * y0 > 0.0:
        raise ValueError("Bad data: y0 = %f, y2 = %f\n" % (y0, y2))
    for i in range(itmax):
        x1 = 0.5 * (x2 + x0)
        y1 = f(x1)
        if (y1 == 0.0) or (math.fabs(x1 - x0) < eps):
            return x1, i+1
        if y1 * y0 > 0.0:
            temp = x0
            x0 = x2
            x2 = temp
            temp = y0
            y0 = y2
            y2 = temp
        y10 = y1 - y0
        y21 = y2 - y1
        y20 = y2 - y0
        if y2 * y20 < 2.0 * y1 * y10:
            x2 = x1
            y2 = y1
        else:
            b = (x1 - x0) / y10
            c = (y10 - y21) / (y21 * y20)
            xm = x0 - b * y0 * (1.0 - c * y1)
            ym = f(xm)
            if ((ym == 0.0) or (math.fabs(xm - xmlast) < eps)):
                return xm, i+1
            xmlast = xm
            if ym * y0 < 0.0:
                x2 = xm
                y2 = ym
            else:
                x0 = xm
                y0 = ym
                x2 = x1
                y2 = y1
    raise RuntimeError("No convergence")
