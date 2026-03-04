'''
Provides the ISO object which will give you current date and time in
standard ISO format.  Run as a script for a demo.
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Current data/time in ISO format oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2021 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ notest oo>
        <oo todo ∞ 
        
            - ∞∞2 Combine with other time-related modules
        
        oo>
    '''
    if 1:  # Standard imports
        from time import time, localtime, gmtime, struct_time, strftime
    if 1:  # Custom imports
        pass
    if 1:  # Global variables
        pass
if 1:  # ISO class:  gives current date and time in standard ISO format
    class ISO(object):
        def __init__(self, zulu=False, rm_zero=True):
            "Initialize with now.  If zulu is True, use GMT."
            self._tm = gmtime() if zulu else localtime()
            self._rm0 = rm_zero
        def __str__(self):
            return strftime("%Y%m%d-%H:%M:%S", self._tm)
        def set(self, tm):
            "Set to a new struct_time"
            if not isinstance(tm, struct_time):
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
    sec_per_year = 31556925.9746784  # From GNU units
    empirical_correction = 5 * 3600 + 4 * 60
    tm = localtime(t - 5 * sec_per_year + empirical_correction)
    iso.set(tm)
    P("About 5 years before now:", iso)
    #
    print(
        dedent(f'''
    ISO instance's properties (for current time):
      str(iso)        {iso}
      iso.date        {iso.date}
      iso.d           {iso.d}
      iso.dt          {iso.dt}
      iso.t           {iso.t}
    ''')
    )
