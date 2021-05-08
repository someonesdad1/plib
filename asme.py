'''
Provides a thread class that will calculate the dimensions of Unified
National thread forms in inches.  Formulas taken from ASME B1.1-1989.
'''

# Copyright (C) 2007 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

class UnifiedThread:
    '''Initialize with basic diameter in inches, threads per inch,
    class, and length of engagement in units of the basic diameter.
    You'll need to refer to the ASME standard for lengths of engagement
    greater than 1.5 times the major diameter.
    '''
    def __init__(self, basic_diameter, tpi, Class=2, length_of_engagement=1):
        if basic_diameter <= 0:
            raise ValueError("Basic diameter must be > 0")
        if tpi <= 0:
            raise ValueError("Threads per inch (tpi) must be > 0")
        if Class not in (1, 2, 3):
            raise ValueError("Invalid value for Class (must be 1, 2, or 3)")
        if not (0.1 <= length_of_engagement <= 1.5):
            msg = "Length of engagement must be between 0.1 and 1.5"
            raise ValueError(msg)
        # Basic diameter
        self.D = basic_diameter
        # Pitch
        self.P = 1/tpi
        # H = fundamental height of vee thread
        self.H = 3**0.5/2*self.P
        self.Class = Class
        self.length_of_engagement = length_of_engagement
    def Allowance(self):
        if self.Class == 3:
            return 0
        return 0.3*self.Class2PDtol()
    def Class2PDtol(self):
        return 0.0015*(self.D**(1/3) +
                       (self.length_of_engagement*self.D)**0.5 +
                       10*self.P**(2/3))
    def Dmax(self):
        'External thread max major diameter'
        return self.D - self.Allowance()
    def Dmin(self):
        'External thread min major diameter'
        c = 0.09 if self.Class == 1 else 0.06
        return self.Dmax() - c*self.P**(2/3)
    def Emax(self):
        'External thread max pitch diameter'
        return self.D - self.Allowance() - 3*3**0.5*self.P/8
    def Emin(self):
        'External thread min pitch diameter'
        c = 3/2 if self.Class == 1 else 1 if self.Class == 2 else 3/4
        return self.Emax() - c*self.Class2PDtol()
    def dmax(self):
        'Internal thread max minor diameter'
        if self.Class in (1, 2):
            if self.D < 1/4:
                tol = 0.05*self.P**(2/3) + 0.03*self.P/self.D - 0.002
                tol = min(tol, 0.394*self.P)
                tol = max(tol, self.P/4 - 2*self.P*self.P)/5
            else:
                if 1/self.P >= 4:
                    tol = self.P/4 - 2*self.P*self.P/5
                else:
                    tol = 3*self.P/20
        else:
            tol = 0.05*self.P**(2/3) + 0.03*self.P/self.D - 0.002
            tol = min(tol, 0.394*self.P)
            if 1/self.P >= 13:
                tol = max(tol, 0.23*self.P - 3*self.P*self.P/2)
            else:
                tol = max(tol, 0.120*self.P)
        return tol + self.dmin()
    def dmin(self):
        'Internal thread min minor diameter'
        return self.D - 5*3**0.5*self.P/8
    def emax(self):
        'Internal thread max pitch diameter'
        c = 1.95 if self.Class == 1 else 1.3 if self.Class == 2 else 0.975
        return self.emin() + c*self.Class2PDtol()
    def emin(self):
        'Internal thread min pitch diameter'
        return self.dmin() + 3**0.5/4*self.P
    def dext(self):
        'External thread minor diameter'
        return 2*(self.Dmax()/2 - 17/24*self.H)
    def Dint(self):
        'Internal thread major diameter'
        return self.D
    def __str__(self):
        return ("UnifiedThread(D={0}, tpi={1})".format(str(self.D),
                str(1/self.P)))
    def TapDrill(self, percent_thread=75):
        if not (0 <= percent_thread <= 100):
            raise ValueError("percent_thread must be between 0 and 100.")
        # A 100% thread is one with height of 6/8 of H
        h = (6/8)*self.H*percent_thread/100
        return round(self.D - 2*h, 4)
    def SellersRecommendedTPI(self):
        '''Returns the recommended threads per inch via a formula from
        Sellers (proposed in 1864).  In "Handbook of Small Tools", 1908, pg
        7, is given the formula for pitch of a US Standard thread; the
        formula is due to Sellers:
 
            pitch in inches = a*sqrt(D + 5/8) - 0.175
 
        where D is the screw diameter in inches and a is 0.24.  This
        applies for D >= 1/4 inch.  For smaller D's, use a = 0.23.
        '''
        a = 0.23 if self.D < 1/4 else 0.24
        pitch = a*(self.D + 5/8)**0.5 - 0.175
        return round(1/pitch, 2)
    def DoubleDepth(self):
        '''Returns the double depth of the unified thread in inches.
        '''
        return round(3.0/2*self.H, 4)
    def NumberSize(self, n):
        '''A convenience function to return the diameter in inches of a
        number-size thread.  n must be between 0 and 500, although
        about the only sizes encountered in the wild are between 0 and 14
        inclusive.
        '''
        n = int(n)
        if not (0 <= n <= 500):
            raise ValueError("n must be between 0 and 500")
        return 0.06 + 0.013*n
