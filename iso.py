'''
Provides the ISO object which will give you current date and time in
standard ISO format.

    iso = ISO()
    print(iso)      20210414-08:42:44
    print(iso.d)    14Apr2021
    print(iso.t)    8:42:44am
'''
if 1:  # Copyright, license
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
    pass
if 1:   # Imports
    import time
class ISO(object):
    def __str__(self):
        return time.strftime("%Y%m%d-%H:%M:%S")
    @property
    def dt(self):
        return self.d + " " + self.t
    @property
    def d(self):
        return time.strftime("%d %b %Y %a")
    @property
    def t(self):
        h = time.strftime("%I")
        if h[0] == "0":
            h = h[1:]
        return h + time.strftime(":%M:%S %p").lower()
