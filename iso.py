'''
Provides the iso object which will give you current data and time.

    print(iso)      20210414-08:42:44
    print(iso.d)    14Apr2021
    print(iso.t)    8:42:44am
'''

import time
import datetime

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

iso = ISO()

if __name__ == "__main__": 
    print("str(iso) ", iso)
    print("iso.d    ", iso.d)
    print("iso.t    ", iso.t)
    print("iso.dt   ", iso.dt)
