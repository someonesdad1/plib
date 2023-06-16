'''
Print out pill bottle dimensions
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2020 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Print out pill bottle dimensions
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        t.t = t("purl")
        t.o = t("ornl")
def PrintData():
    print(dedent(f'''
            {t.t}Wal-Mart Pill Bottle Sizes in mm{t.n}
                        ID      OD  
    {t.o}Small{t.n}
        Short (41.7 max OD) OAL = 80.3 CL, 82.7 CS
            Bottom      29.5    31.6
            Top         31      32.6
            Depth       70
        Long (41.6 max OD) OAL = 94.7 CL, 96.6 CS
            Bottom      29.5    31.6
            Top         31      32.4
            Depth       84
    {t.o}Large{t.n}
        Long (41.6 max OD) OAL = 146.9 CL, 148.5 CS
            Bottom      46.4    48.6
            Top         48.7    50.2
            Depth       135
        
    {t.o}Notes{t.n}
       - Depth is with cap off on inside.  If you measure with a rule,
         you'll get about 1 mm shorter because of a central step at the
         bottom.
       - Max OD ignores the locking tab (it's the OD if tab cut off)
       - CS = cap screwed on, CL = cap locked on
       - ID measured with 8" Fay calipers & rule
       - OD measured with digital electronic calipers
    '''))
if __name__ == "__main__":
    PrintData()
