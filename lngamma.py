# Copyright (C) 2008 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

from __future__ import division, print_function
import math
import cmath

def lngamma(z):
    '''Routine to calculate the logarithm of the gamma function.
    Translated from C.  See page 160 of "Numerical Recipes".  This is
    Lanczos' remarkable formula.  |error| < 2e-10 everywhere Re x > 0.
    '''
    stp = 2.50662827465
    if isinstance(z, complex):
        if z.real <= 0:
            raise ValueError("Argument's real part must be > 0")
        x = z - 1
        tmp = x + 5.5
        tmp = (x + 0.5)*cmath.log(tmp) - tmp
        ser = (1 + 76.18009173/(x + 1) - 86.50532033/(x + 2) +
               24.01409822/(x + 3) - 1.231739516/(x + 4) +
               0.120858003e-2/(x + 5) - 0.536382e-5/(x + 6))
        return tmp + cmath.log(stp*ser)
    else:
        if z <= 0:
            raise ValueError("Argument must be > 0")
        x = z - 1
        tmp = x + 5.5
        tmp = (x + 0.5)*math.log(tmp) - tmp
        ser = (1 + 76.18009173/(x + 1) - 86.50532033/(x + 2) +
               24.01409822/(x + 3) - 1.231739516/(x + 4) +
               0.120858003e-2/(x + 5) - 0.536382e-5/(x + 6))
        return tmp + math.log(stp*ser)
