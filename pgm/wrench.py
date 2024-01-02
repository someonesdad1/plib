'''
Print out wrench sizes
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Print out wrench sizes
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from fractions import Fraction
    # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from columnize import Columnize
    # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        # Colors
        t.ti = t("yell")
        t.notes = t("purl")
        t.hdr = t("lip")
        t.mm = t("roy")
        t.inch = t("yel")

if 1:   # Core functionality
    def PF(frac):
        '''Return the indicated fraction as a proper fraction.
        '''
        if frac == int(frac):
            return str(int(frac))
        if frac > 1:
            n, d = frac.numerator, frac.denominator
            i, r = divmod(n, d)
            return "{}-{}/{}".format(i, r, d)
        else:
            return "{}/{}".format(frac.numerator, frac.denominator)
    def WrenchSizes(sizes="inch", all=False):
        '''Return a list of the form
            [
                [nominal_size, size_string, min, max, sizes],
                ...
            ]
        for wrenches of the indicated types.  nominal, min, and max are in
        mils.  sizes can be "inch" or "metric".
    
        Machinery's Handbook 19th ed. (1971) gives the wrench openings for the
        nominal size w as [w0, w1] where 
            w0 = 1.005*w + 0.001
            w1 = w0 + 0.005*w + 0.004
        '''
        d = []
        # Rounding an inch dimension in mils to the nearest mil
        def rnd(x):
            return int(round(x, 0))
        if sizes == "inch":
            # Inch sizes are in 32nds
            inches = list(range(4, 13)) + list(range(14, 33, 2))
            if all:
                inches += list(range(34, 65, 2))
            for i in inches:
                w = Fraction(i, 32)
                # Get size in integer mils, rounded to nearest mil
                f = rnd(1000*float(w))
                w0 = rnd(1.005*f + 0.001)
                w1 = rnd(w0 + 0.005*f + 0.004)
                d.append((f, PF(w), w0, w1, sizes))
        else:
            mm = list(range(3, 25))
            if all:
                # The following are my 3/4" drive sockets
                mm += [26, 27, 28, 30, 32, 34, 36, 38, 41, 42, 45, 46, 48, 50]
            for m in mm:
                w = rnd(1000*m/25.4)
                w0 = rnd(1.005*w + 0.001)
                w1 = rnd(w0 + 0.005*w + 0.004)
                d.append((w, str(m), w0, w1, sizes))
        return d

if __name__ == "__main__": 
    sizes = sorted(WrenchSizes(sizes="inch", all=True) +
                   WrenchSizes(sizes="mm", all=True))
    if 0:
        from pprint import pprint as pp
        pp(sizes)
        exit() 
    t.print(f"{t.ti}{'Wrench Opening Sizes in Mils':^{W}s}")
    t.print(f'''
    {t.notes}Nom = nominal size in mils
    Min = 1.005*Nom + 0.001
    Max = Min + Diff
    Diff = 0.005*Nom + 0.004 = allowable variation in wrench opening
    From MH 19th ed 1971
    '''[1:-1])
    sz = [f"{t.hdr}   Size      Nom   Min   Max   Diff "]
    n = 9
    for w, nom, w0, w1, im in sizes:
        if im == "mm":
            nom += " mm"
            s = f"{t.mm}{nom:>{n}s}  {w:5d} {w0:5d} {w1:5d} {w1 - w0:5d}{t.n}"
        else:
            s = f"{t.inch}{nom:{n}s}  {w:5d} {w0:5d} {w1:5d} {w1 - w0:5d}{t.n}"
        sz.append(s)
    for i in Columnize(sz):
        print(i)
    print(dedent(f'''
    {t('whtl')}Interchangeable sizes:{t.n}
        5/32        4 mm
        {t('ornl')}5/16        8 mm{t.n}
        {t(Color(254,   1, 154))}3/4        19 mm{t.n}
        1-1/16     27 mm
        1-13/16    46 mm
    '''))
