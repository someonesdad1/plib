# encoding: utf-8
'''
Test the FPFormat class.  Lines that are likely to be platform
dependent are conditional upon the os.name attribute.  If you test on
an alternate platform or find some missing test cases that expose bugs,
please let me know via email.
'''

# Copyright (C) 2008, 2012 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

import sys
from fpformat import FPFormat
from os import name as platform
from lwtest import run

WindowsNT = "nt"
posix = "posix"
E = RuntimeError("Potential platform dependency -- please check")
def Assert(a, b):
    if a != b:
        s = "Expected %s, got %s" % (repr(b), repr(a))
        raise AssertionError(s)

def Test_sig():
    f = FPFormat()
    x = 1.2345678901234567890
    if 1:
        f.digits( 0); Assert(f.sig(x), "1")
        f.digits( 0); Assert(f.sig(-x), "-1")
        f.digits( 1); Assert(f.sig(x), "1.")
        f.digits( 1); Assert(f.sig(-x), "-1.")
        f.digits( 2); Assert(f.sig(x), "1.2")
        f.digits( 3); Assert(f.sig(x), "1.23")
        f.digits( 4); Assert(f.sig(x), "1.235")
        f.digits( 5); Assert(f.sig(x), "1.2346")
        if platform == WindowsNT:
            f.digits(20); Assert(f.sig(x), "1.2345678901234566904")
            f.digits(20); Assert(f.sig(-x), "-1.2345678901234566904")
        elif platform == posix:
            f.digits(20); Assert(f.sig(x), "1.2345678901234566904")
            f.digits(20); Assert(f.sig(-x), "-1.2345678901234566904")
        else: 
            raise E
        f.high = 2e6
        x *= 1e6
        f.digits( 0); Assert(f.sig(x), "1000000")
        f.digits( 0); Assert(f.sig(-x), "-1000000")
        f.digits( 1); Assert(f.sig(x), "1000000.")
        f.digits( 2); Assert(f.sig(x), "1200000.")
        f.digits( 3); Assert(f.sig(x), "1230000.")
        f.digits( 7); Assert(f.sig(x), "1234568.")
        f.digits( 8); Assert(f.sig(x), "1234567.9")
        if platform == WindowsNT:
            f.digits(20); Assert(f.sig(x),   "1234567.8901234567165")
            f.digits(20); Assert(f.sig(-x), "-1234567.8901234567165")
        elif platform == posix:
            f.digits(20); Assert(f.sig(x), "1234567.8901234567165")
            f.digits(20); Assert(f.sig(-x), "-1234567.8901234567165")
        else: 
            raise E
        x /= 1e12
        f.low = 1e-7
        f.digits( 0); Assert(f.sig(x), "0.000001")
        f.digits( 0); Assert(f.sig(-x), "-0.000001")
        f.digits( 1); Assert(f.sig(x), "0.000001")
        f.digits( 2); Assert(f.sig(x), "0.0000012")
        f.digits( 6); Assert(f.sig(x), "0.00000123457")
        if platform == WindowsNT:
            f.digits(20); Assert(f.sig(x),   "0.0000012345678901234567384")
            f.digits(20); Assert(f.sig(-x), "-0.0000012345678901234567384")
        elif platform == posix:
            f.digits(20); Assert(f.sig(x),   "0.0000012345678901234567384")
            f.digits(20); Assert(f.sig(-x), "-0.0000012345678901234567384")
        else: 
            raise E
        f.digits(2)
        x =  1.23456e3-1.23456e3j; Assert(f.sig(x),  "1200.-1200.i")
        x = -1.23456e3-1.23456e3j; Assert(f.sig(x), "-1200.-1200.i")
        x =  1.23456e3+1.23456e3j; Assert(f.sig(x),  "1200.+1200.i")
        x = -1.23456e3+1.23456e3j; Assert(f.sig(x), "-1200.+1200.i")
        x =  1.23456e-3-1.23456e-3j; Assert(f.sig(x),  "0.0012-0.0012i")
        x = -1.23456e-3-1.23456e-3j; Assert(f.sig(x), "-0.0012-0.0012i")
        x =  1.23456e-3+1.23456e-3j; Assert(f.sig(x),  "0.0012+0.0012i")
        x = -1.23456e-3+1.23456e-3j; Assert(f.sig(x), "-0.0012+0.0012i")
    # The following test came from the discovery of a bug on 14 Jan
    # 2012 (found while calculating the area of some paper in
    # paper.py).  The area was a square 39.37 inches on a side; the
    # area should have been 1 square meter, but came out as 0.1 m2.  It
    # also was off for conversion to cm2 and mm2.  This bug also showed
    # up 13 Oct 2014 in an old fpformat.py module in xfmpy when the
    # argument was -0.9999902 and rounding was to be to 4 significant
    # figures.
    f.digits(3)
    x = 0.999999
    Assert(f.sig(x), "1.00")
    Assert(f.sig(x*1e4), "10000.")
    Assert(f.sig(-x), "-1.00")
    Assert(f.sig(-x*1e4), "-10000.")

def Test_fix():
    f = FPFormat()
    x = 1.2345678901234567890
    f.digits( 0); Assert(f.fix(x), "1")
    f.digits( 1); Assert(f.fix(x), "1.2")
    f.digits( 2); Assert(f.fix(x), "1.23")
    f.digits( 3); Assert(f.fix(x), "1.235")
    if platform == WindowsNT:
        f.digits(20); Assert(f.fix(x),   "1.23456789012345669043")
        f.digits(20); Assert(f.fix(-x), "-1.23456789012345669043")
    elif platform == posix:
        f.digits(20); Assert(f.fix(x), "1.23456789012345669043")
        f.digits(20); Assert(f.fix(-x), "-1.23456789012345669043")
    else: 
        raise E
    x *= 1e9
    f.digits( 0); Assert(f.fix(x), "1234567890")
    f.digits( 1); Assert(f.fix(x), "1234567890.1")
    f.digits( 2); Assert(f.fix(x), "1234567890.12")
    f.digits( 3); Assert(f.fix(x), "1234567890.123")
    f.digits( 4); Assert(f.fix(x), "1234567890.1235")
    if platform == WindowsNT:
        f.digits(10); Assert(f.fix(x), "1234567890.1234567165")
    elif platform == posix:
        f.digits(10); Assert(f.fix(x), "1234567890.1234567165")
    else: 
        raise E
    x /= 1e12
    f.digits( 0); Assert(f.fix(x), "0")
    f.digits( 0); Assert(f.fix(-x), "-0")
    f.digits( 1); Assert(f.fix(x), "0.0")
    f.digits( 1); Assert(f.fix(-x), "-0.0")
    f.digits( 2); Assert(f.fix(x), "0.00")
    f.digits( 2); Assert(f.fix(-x), "-0.00")
    f.digits( 3); Assert(f.fix(x), "0.001")
    f.digits( 3); Assert(f.fix(-x), "-0.001")
    f.digits( 4); Assert(f.fix(x), "0.0012")
    f.digits( 5); Assert(f.fix(x), "0.00123")
    f.digits( 7); Assert(f.fix(x), "0.0012346")
    if platform == WindowsNT:
        f.digits(25); Assert(f.fix(x),   "0.0012345678901234567129835")
        f.digits(25); Assert(f.fix(-x), "-0.0012345678901234567129835")
    elif platform == posix:
        f.digits(25); Assert(f.fix(x), "0.0012345678901234567129835")
        f.digits(25); Assert(f.fix(-x), "-0.0012345678901234567129835")
    else: 
        raise E
    f.digits(2)
    x =  1.23456e3-1.23456e3j; Assert(f.fix(x),  "1234.56-1234.56i")
    x = -1.23456e3-1.23456e3j; Assert(f.fix(x), "-1234.56-1234.56i")
    x =  1.23456e3+1.23456e3j; Assert(f.fix(x),  "1234.56+1234.56i")
    x = -1.23456e3+1.23456e3j; Assert(f.fix(x), "-1234.56+1234.56i")
    f.digits(5)
    x =  1.23456e-3-1.23456e-3j; Assert(f.fix(x),  "0.00123-0.00123i")
    x = -1.23456e-3-1.23456e-3j; Assert(f.fix(x), "-0.00123-0.00123i")
    x =  1.23456e-3+1.23456e-3j; Assert(f.fix(x),  "0.00123+0.00123i")
    x = -1.23456e-3+1.23456e-3j; Assert(f.fix(x), "-0.00123+0.00123i")

def Test_sci():
    f = FPFormat()
    f.expsign = True
    x = 1.2345678901234567890
    f.digits( 0); Assert(f.sci( x), "1e+00")
    f.digits( 0); Assert(f.sci(-x), "-1e+00")
    f.digits( 1); Assert(f.sci(x), "1e+00")
    f.digits( 1); Assert(f.sci(-x), "-1e+00")
    f.digits( 2); Assert(f.sci(x), "1.2e+00")
    f.digits( 3); Assert(f.sci(x), "1.23e+00")
    f.digits( 3); Assert(f.sci(-x), "-1.23e+00")
    if platform == WindowsNT:
        f.digits(20); Assert(f.sci(x), "1.2345678901234566904e+00")
    elif platform == posix:
        f.digits(20); Assert(f.sci(x), "1.2345678901234566904e+00")
    else: 
        raise E
    x *= 1e9
    f.digits( 0); Assert(f.sci(x), "1e+09")
    f.digits( 0); Assert(f.sci(-x), "-1e+09")
    f.digits( 1); Assert(f.sci(x), "1e+09")
    f.digits( 2); Assert(f.sci(x), "1.2e+09")
    f.digits( 2); Assert(f.sci(-x), "-1.2e+09")
    x /= 1e18
    f.digits( 0); Assert(f.sci(x), "1e-09")
    f.digits( 1); Assert(f.sci(x), "1e-09")
    f.digits( 2); Assert(f.sci(x), "1.2e-09")
    if platform == WindowsNT:
        f.digits(20); Assert(f.sci( x),  "1.2345678901234566209e-09")
        f.digits(20); Assert(f.sci(-x), "-1.2345678901234566209e-09")
    elif platform == posix:
        f.digits(20); Assert(f.sci( x), "1.2345678901234566209e-09")
        f.digits(20); Assert(f.sci(-x), "-1.2345678901234566209e-09")
    else: 
        raise E
    f.digits(2)
    x =  1.23456e6-1.23456e6j; Assert(f.sci(x),  "1.2e+06-1.2e+06i")
    x = -1.23456e6-1.23456e6j; Assert(f.sci(x), "-1.2e+06-1.2e+06i")
    x =  1.23456e6+1.23456e6j; Assert(f.sci(x),  "1.2e+06+1.2e+06i")
    x = -1.23456e6+1.23456e6j; Assert(f.sci(x), "-1.2e+06+1.2e+06i")
    # Check for 14 Jan 2012 bug for mantissas just under 1
    x = 0.999999
    f.digits(2)
    Assert(f.sci(x), "1.0e+00")
    Assert(f.sci(x*1e9), "1.0e+09")
    Assert(f.sci(x/1e9), "1.0e-09")
    Assert(f.sci(x*1e120), "1.0e+120")
    # Check that expsign and expdigits work
    x = 1.2345678901234567890e9
    f.expsign = True
    f.digits( 3); Assert(f.sci(x), "1.23e+09")
    f.expsign = False
    Assert(f.sci(x), "1.23e09")
    f.expdigits = -88  # Negative values are same as zero
    Assert(f.sci(x), "1.23e9")
    f.expdigits = 0
    Assert(f.sci(x), "1.23e9")
    f.expdigits = 1
    Assert(f.sci(x), "1.23e9")
    f.expdigits = 3
    Assert(f.sci(x), "1.23e009")
    f.expsign = True
    Assert(f.sci(x), "1.23e+009")

def Test_eng():
    f = FPFormat()
    f.expdigits = 3
    x = 1.2345678901234567890
    f.expdigits = 3
    f.digits( 0); Assert(f.eng( x), "1e+000")
    f.digits( 0); Assert(f.eng(-x), "-1e+000")
    f.digits( 1); Assert(f.eng(x), "1.e+000")
    f.digits( 1); Assert(f.eng(-x), "-1.e+000")
    f.digits( 2); Assert(f.eng(x), "1.2e+000")
    f.digits( 3); Assert(f.eng(x), "1.23e+000")
    f.digits( 3); Assert(f.eng(-x), "-1.23e+000")
    x = 1.2345678901234567890e1
    f.digits( 0); Assert(f.eng( x), "10e+000")
    f.digits( 0); Assert(f.eng(-x), "-10e+000")
    f.digits( 1); Assert(f.eng(x), "10.e+000")
    f.digits( 1); Assert(f.eng(-x), "-10.e+000")
    f.digits( 2); Assert(f.eng(x), "12.e+000")
    f.digits( 3); Assert(f.eng(x), "12.3e+000")
    f.digits( 3); Assert(f.eng(-x), "-12.3e+000")
    x = 1.2345678901234567890e-1
    f.digits( 0); Assert(f.eng( x), "100e-003")
    f.digits( 0); Assert(f.eng(-x), "-100e-003")
    f.digits( 1); Assert(f.eng(x), "100.e-003")
    f.digits( 1); Assert(f.eng(-x), "-100.e-003")
    f.digits( 2); Assert(f.eng(x), "120.e-003")
    f.digits( 2); Assert(f.eng(-x), "-120.e-003")
    f.digits( 3); Assert(f.eng(x), "123.e-003")
    f.digits( 3); Assert(f.eng(-x), "-123.e-003")
    x = 1.2345678901234567890e2
    f.digits( 0); Assert(f.eng( x), "100e+000")
    f.digits( 0); Assert(f.eng(-x), "-100e+000")
    f.digits( 1); Assert(f.eng(x), "100.e+000")
    f.digits( 1); Assert(f.eng(-x), "-100.e+000")
    f.digits( 2); Assert(f.eng(x), "120.e+000")
    f.digits( 2); Assert(f.eng(-x), "-120.e+000")
    f.digits( 3); Assert(f.eng(x), "123.e+000")
    f.digits( 3); Assert(f.eng(-x), "-123.e+000")
    x = 1.2345678901234567890e-2
    f.digits( 0); Assert(f.eng( x), "10e-003")
    f.digits( 0); Assert(f.eng(-x), "-10e-003")
    f.digits( 1); Assert(f.eng(x), "10.e-003")
    f.digits( 1); Assert(f.eng(-x), "-10.e-003")
    f.digits( 2); Assert(f.eng(x), "12.e-003")
    f.digits( 3); Assert(f.eng(x), "12.3e-003")
    f.digits( 3); Assert(f.eng(-x), "-12.3e-003")
    x = 1.2345678901234567890e3
    f.digits( 0); Assert(f.eng( x), "1e+003")
    f.digits( 0); Assert(f.eng(-x), "-1e+003")
    f.digits( 1); Assert(f.eng(x), "1.e+003")
    f.digits( 1); Assert(f.eng(-x), "-1.e+003")
    f.digits( 2); Assert(f.eng(x), "1.2e+003")
    f.digits( 3); Assert(f.eng(x), "1.23e+003")
    f.digits( 3); Assert(f.eng(-x), "-1.23e+003")
    x = 1.2345678901234567890e-3
    f.digits( 0); Assert(f.eng( x), "1e-003")
    f.digits( 0); Assert(f.eng(-x), "-1e-003")
    f.digits( 1); Assert(f.eng(x), "1.e-003")
    f.digits( 1); Assert(f.eng(-x), "-1.e-003")
    f.digits( 2); Assert(f.eng(x), "1.2e-003")
    f.digits( 3); Assert(f.eng(x), "1.23e-003")
    f.digits( 3); Assert(f.eng(-x), "-1.23e-003")
    f.digits(2)
    x =  1.23456e6-1.23456e6j; Assert(f.eng(x),  "1.2e+006-1.2e+006i")
    x = -1.23456e6-1.23456e6j; Assert(f.eng(x), "-1.2e+006-1.2e+006i")
    x =  1.23456e6+1.23456e6j; Assert(f.eng(x),  "1.2e+006+1.2e+006i")
    x = -1.23456e6+1.23456e6j; Assert(f.eng(x), "-1.2e+006+1.2e+006i")
    # Check for mantissa-near-one rounding bug
    x = 0.999999
    f.digits(3)
    Assert(f.eng(x), "1.00e+000")
    Assert(f.eng(-x), "-1.00e+000")
    Assert(f.eng(1e9*x), "1.00e+009")
    Assert(f.eng(x/1e9), "1.00e-009")
    # Check that expsign and expdigits work
    x = 1.2345678901234567890e9
    f.expdigits = 2
    f.expsign = True
    f.digits( 3); Assert(f.eng(x), "1.23e+09")
    f.expsign = False
    Assert(f.eng(x), "1.23e09")
    f.expdigits = -88  # Negative values are same as zero
    Assert(f.eng(x), "1.23e9")
    f.expdigits = 0
    Assert(f.eng(x), "1.23e9")
    f.expdigits = 1
    Assert(f.eng(x), "1.23e9")
    f.expdigits = 3
    Assert(f.eng(x), "1.23e009")
    f.expsign = True
    Assert(f.eng(x), "1.23e+009")
    x *= 10; Assert(f.eng(x), "12.3e+009")
    x *= 10; Assert(f.eng(x), "123.e+009")
    f.trailing_decimal_point(False)
    Assert(f.eng(x), "123e+009")
    f.expdigits = 5
    Assert(f.eng(x), "123e+00009")
    f.expsign = False
    Assert(f.eng(x), "123e00009")

def Test_engsi():
    f = FPFormat()
    f.expdigits = 3
    f.digits(2)
    s = '''
        1.2e-027 12.e-027 120.e-027 1.2@y 12.@y 120.@y 1.2@z 12.@z 120.@z
        1.2@a 12.@a 120.@a 1.2@f 12.@f 120.@f 1.2@p 12.@p 120.@p 1.2@n
        12.@n 120.@n 1.2@μ 12.@μ 120.@μ 1.2@m 12.@m 120.@m 1.2@ 12.@ 120.@
        1.2@k 12.@k 120.@k 1.2@M 12.@M 120.@M 1.2@G 12.@G 120.@G 1.2@T
        12.@T 120.@T 1.2@P 12.@P 120.@P 1.2@E 12.@E 120.@E 1.2@Z 12.@Z
        120.@Z 1.2@Y 12.@Y 120.@Y 1.2e+027
    '''[1:-1]
    t = s.replace("\n", " ").split()
    for i, x in enumerate(range(-27, 28)):
        u = eval("1.23e{}".format(x))
        Assert(f.engsi(u), t[i].replace("@", " "))

if __name__ == "__main__":
    exit(run(globals())[0])
