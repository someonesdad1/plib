'''
Provides the ISO object which will give you current date and time in
standard ISO format.  Run as a script for a demo.
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # <utility> Provides the ISO object to provide current date and time
        # in standard ISO format.
        #∞what∞#
        #∞test∞# ignore #∞test∞#
    # Imports
        from time import time, localtime, gmtime, struct_time, strftime
        from pdb import set_trace as xx 
    # Global variables
        ii = isinstance
class ISO(object):
    def __init__(self, zulu=False, rm_zero=True):
        'Initialize with now.  If zulu is True, use GMT.'
        self._tm = gmtime() if zulu else localtime()
        self._rm0 = rm_zero
    def __str__(self):
        return strftime("%Y%m%d-%H:%M:%S", self._tm)
    def set(self, tm):
        'Set to a new struct_time'
        if not ii(tm, struct_time):
            raise TypeError("tm must be a time.struct_time instance")
        self._tm = tm
    @property
    def date(self):
        '''This returns the date in the form I use the most; e.g. 
        '12 Aug 2019'.
        '''
        s = strftime("%d %b %Y", self._tm)
        if self._rm0 and s[0] == "0":
            s = s[1:]
        return s
    @property
    def dt(self):
        return self.d + " " + self.t
    @property
    def d(self):
        s = strftime("%d %b %Y %a", self._tm)
        if self._rm0 and s[0] == "0":
            s = s[1:]
        return s
    @property
    def t(self):
        h = strftime("%I", self._tm)
        if h[0] == "0":
            h = h[1:]
        return h + strftime(":%M:%S %p", self._tm).lower()
if __name__ == "__main__": 
    from collections import namedtuple
    from wrap import dedent
    def P(t, iso):
        print(t)
        print("  Date and time: ", iso)
        print("  Date:          ", iso.d)
        print("  Time:          ", iso.t)
    t = time()
    iso = ISO()
    iso.set(localtime(t))
    P("Local time now: (str(iso_instance))", iso)
    iso1 = ISO(zulu=True)
    P("GMT time now: (zulu=True in constructor)", iso1)
    # Change to about 5 years before
    sec_per_year = 31556925.9746784     # From GNU units
    empirical_correction = 5*3600 + 4*60
    tm = localtime(t - 5*sec_per_year + empirical_correction)
    iso.set(tm)
    P("About 5 years before now:", iso)
    # 
    print(dedent(f'''
    ISO instance's properties (for current time):
      str(iso)        {iso}
      iso.date        {iso.date}
      iso.d           {iso.d}
      iso.dt          {iso.dt}
      iso.t           {iso.t}
    '''))
