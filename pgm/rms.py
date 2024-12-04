'''
Calculations with RMS related things

    - Input a number x.  It is interpreted in a number of ways
        - It's a peak-to-peak value for sine wave
        - It's a 0-to-peak value for sine wave (i.e., mathematical definition of the
          amplitude of a sine wave)
        - It's an RMS value of a sine wave
            - Peak is then x*sqrt(2)
            - Peak-to-peak is then 2*x*sqrt(2)
        - Then equivalent measures are printed out
    - Options
        - -t x  Type of waveform
            -- cos       Cosine
            -- sin       Sine
            -- squ       Square
            -- tri       Triangle  (ramps are with symmetry 0 or 100)
            -- pul:n     Pulse with no DC with duty cycle n (0 to 100)
            -- pul0:n    0-based pulse with duty cycle n (0 to 100)
        - -d n  DC offset
        - -s n  Symmetry
        - -v    Validate the formulas in the RMS document

    - All waveforms are nominally about unit amplitude by default and will have an RMS value of
      around unity.  

    - This script uses the optional plotext library that does a good job of plotting in a terminal
      window, well enough to see basic behavior.  https://github.com/piccolomo/plotext/tree/master

'''
 
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import deque
        from functools import partial
        from math import pi, sqrt
        from pathlib import Path as P
        import getopt
        import numpy as np
        from numpy.fft import fft
        import numpy.random as random
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import run, Assert, check_equal, assert_equal
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
        # Get plotext for plotting in the terminal
        g.have_plotext = True
        try:
            import plotext as plt
        except ImportError:
            g.have_plotext = False
if 1:   # Utility
    def GetColors():
        t.err = t("redl")
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Get LINES & COLUMNS'
        g.H, g.W = int(os.environ.get("LINES", "50")), int(os.environ.get("COLUMNS", "80")) - 1
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Calculations related to RMS values.
        Options:
            -h      Print a manpage
            -v      Validate the formulas in the RMS document
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-v"] = False
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hv") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("v"):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
        return args
    def SlopeAndIntercept(x1, y1, x2, y2, numtype=float):
        '''Return (m, b) where m is the slope and b is the intercept of a line, gotten from the
        point-slope formula.  The slope is m = (y2 - y1)/(x2 - x1).  Then for any two points (x1,
        y1) and (x2, y2) on a line, the line's equation is (y - y1)/(x - x1) = m.  Thus, the
        intercept is b = y1 - m*x1.
        '''
        if not (x2 - x1):
            raise ValueError("Denominator is zero")
        m = numtype((y2 - y1)/(x2 - x1))
        return m, numtype(y1 - m*x1)
if 1:   # Waveform class
    class Waveform:
        '''Construct a basic waveform in a numpy array (the x and y properties have the arrays).
        Methods then can be used to get
            Vdc
            Varms
            Vrms
            Vpk
            Vpp
        '''
        names = set((
            "sine",
            "square",
            "triangle",
            "ramp",
            "noise",
            "halfsine",
        ))
        def __init__(self, name, n=100, D=0.5, DC=0, zero_baseline=False):
            '''Attributes
            n   (int)   Number of points [100]
            D   (flt)   Duty cycle
            DC  (flt)   DC offset
            zero_baseline (bool)  Set to True for a 0 baseline (sets DC offset)
            '''
            self._ready = False     # Don't construct waveform yet
            self.name = name
            self._n = self._D = self._DC = self._zero_baseline = self.x = self.y = None
            self.n = n
            self.D = D
            self.DC = DC
            self.zero_baseline = zero_baseline
            self._ready = True
            if name in Waveform.names:
                self.construct()
            else:
                raise ValueError(f"{name!r} is not recognized")
        def __str__(self):
            s = (f"Waveform({self.name!r}, n={self.n}, D={self.D}, "
                 f"DC={self.DC}, zero_baseline={self.zero_baseline})")
            return s
        def construct(self):
            '''self.x contains the abscissas, self.y contains the ordinates.
            T is the period.
            '''
            if not self._ready:
                return
            n, D = self._n, self._D
            dx = 1/n
            # Get x on [0, 1]
            self.x = np.arange(0, 1, dx)
            if self._name == "sine":
                twopi = 2*pi
                x = np.arange(0, twopi, twopi*dx)
                self.y = np.sin(x)
                self.y += self._DC
                if self._zero_baseline:
                    self.y += 1
            elif self._name == "square":
                # Positive portion
                first = np.arange(0, int(D*n))*0.0 + 1.0
                # Negative portion
                second = np.arange(0, int((1 - D)*n))*0.0 - 1.0
                self.y = np.concatenate((first, second), axis=None)
                if self._DC:
                    self.y += self._DC
                elif self._zero_baseline:
                    first = np.arange(0, n)*0.0 + 1.0
                    second = np.arange(0, m)*0.0
                    self.y = np.concatenate((first, second), axis=None)
            elif self._name == "triangle":
                # The five key points on the waveform are:
                # (0, 0) and ((D*T/2, 1)            From 0 to n1        Section 1
                # (D*T/2, 1) and (T/2, 0)           From n1 + 1 to n2   Section 2
                # (T/2, 0) and (T*(1 - D/2), -1)    From n2 + 1 to n3   Section 3
                # (T*(1 - D/2), -1) and (0, T)      From n3 + 1 to n    Section 4
                T = self.x[-1] - self.x[0] + dx
                # Indexes of the key points
                n1 = int(round(D*n/2, 0))
                n2 = int(round(n/2, 0))
                n3 = n - n1
                # Section 1
                m, b = SlopeAndIntercept(0, 0, D*T/2, 1)
                y1 = m*self.x[0:n1 + 1] + b
                # Section 2
                m, b = SlopeAndIntercept(D*T/2, 1, T/2, 0)
                y2 = m*self.x[n1 + 1:n2 + 1] + b
                # Section 3
                m, b = SlopeAndIntercept(T/2, 0, T*(1 - D/2), -1)
                y3 = m*self.x[n2 + 1:n3 + 1] + b
                # Section 4
                m, b = SlopeAndIntercept(T*(1 - D/2), -1, T, 0)
                y4 = m*self.x[n3 + 1:] + b
                # Put waveform's sections together
                self.y = np.concatenate((y1, y2, y3, y4), axis=None)
            elif self._name == "ramp":
                # The key points on the waveform are:
                # (0, -1) and (T, 1)
                T = self.x[-1] - self.x[0] + dx
                m, b = SlopeAndIntercept(0, -1, T, 1)
                self.y = m*self.x + b
            elif self._name == "noise":
                self.y = random.normal(size=self.n)
                if self._DC:
                    self.y += self._DC
            elif self._name == "halfsine":
                self._name = "sine"
                self.construct()
                self._name = "halfsine"
                # Set the negative elements to zero
                self.y = np.where(self.y >= 0, self.y, 0)
            else:
                raise RuntimeError(f"Bug:  {self._name!r} is unknown waveform name")
            if len(self.y) != self.n:
                raise ValueError(f"len(self.y) = {len(self.y)} is not equal to {n}")
        def fft(self, title="", W=60, H=30, fit=False):
            'Plot the FFT of the waveform.  If fit is True, fit to the whole screen.'
            if not g.have_plotext:
                print("plotext library not installed", file=sys.stderr)
                return
            plt.clear_figure()
            plt.theme("clear")
            # Get FFT:  it's a complex array, so take the magnitude
            dft = np.abs(fft(self.y))
            # Cut it in half, as the two halves are redundant
            half = len(dft)//2
            dft, x = dft[:half], self.x[:half]
            # Double every element except the first, which is DC
            dc = dft[0]
            dft *= 2
            dft[0] = dc
            # Make a bar chart
            plt.bar(x, np.abs(dft))
            if title:
                plt.title(title)
            plt.grid()
            if fit:
                GetScreen()
                W, H = g.W, g.H
            plt.plot_size(W, H)
            plt.show()
        def plot(self, title="", W=60, H=30, fit=False):
            'Plot the waveform.  If fit is True, fit to the whole screen.'
            if not g.have_plotext:
                print("plotext library not installed", file=sys.stderr)
                return
            plt.clear_figure()
            plt.theme("clear")
            plt.plot(self.x, self.y)
            if title:
                plt.title(title)
            plt.grid()
            if fit:
                GetScreen()
                W, H = g.W, g.H
            plt.plot_size(W, H)
            plt.show()
        def remove_DC(self):
            self.y -= self.Vdc
        if 1:   # Properties
            # Name of waveform
            @property
            def name(self):
                return self._name
            @name.setter
            def name(self, name):
                if name not in Waveform.names:
                    raise ValueError(f"{self._name!r} is unknown waveform name")
                self._name = name
                self.construct()
            # Number of points in waveform
            @property
            def n(self):
                return self._n
            @n.setter
            def n(self, value):
                n = int(value)
                if n <= 0:
                    raise ValueError("Property n must be integer > 0")
                self._n = n
                self.construct()
            # Duty cycle
            @property
            def D(self):
                return self._D
            @D.setter
            def D(self, value):
                D = flt(value)
                if not 0 < D < 1:
                    raise ValueError("Duty cycle D must be float on (0, 1)")
                self._D = D
                self.construct()
            # DC offset
            @property
            def DC(self):
                return flt(self._DC)
            @DC.setter
            def DC(self, value):
                dc = flt(value)
                self._DC = dc
                self._zero_baseline = False
                self.construct()
            # Crest factor
            @property
            def CF(self):
                pk = self.Vpk
                rms = self.Varms
                return flt(pk/rms) if rms else flt(1)
            # Zero baseline
            @property
            def zero_baseline(self):
                return self._zero_baseline
            @zero_baseline.setter
            def zero_baseline(self, value):
                zbl = bool(value)
                if self._zero_baseline == zbl:
                    return
                self._zero_baseline = zbl
                self._DC = 0
                self.construct()
        if 1:   # Functionals
            @property
            def Vpp(self):
                return flt(abs(max(self.y)) + abs(min(self.y)))
            @property
            def Vpk(self):
                return flt(max(abs(max(self.y)), abs(min(self.y))))
            @property
            def Vrms(self):
                'Calculate the RMS integral'
                dx = self.x[1] - self.x[0]
                T = self.x[-1] - self.x[0]
                return flt(np.sqrt(sum(dx*self.y**2)/T))
            @property
            def Varms(self):
                return flt(np.sqrt(self.Vrms**2 - self.Vdc**2))
            @property
            def Vaa(self):
                'Calculate the absolute average integral'
                dx = self.x[1] - self.x[0]
                T = self.x[-1] - self.x[0]
                return flt(sum(np.abs(dx*self.y))/T)
            @property
            def CF(self):
                '''Calculate the crest factor.  If Vrms is zero, this will return a crest factor
                of zero.
                '''
                if not self.Vrms:
                    return flt(0)
                else:
                    return self.Vpk/self.Vrms
            @property
            def Vdc(self):
                'Calculate the average integral'
                dx = self.x[1] - self.x[0]
                T = self.x[-1] - self.x[0]
                avg = flt(sum(dx*self.y)/T)
                dc = round(avg, 15)
                if not dc:
                    # Sometimes is -0
                    dc = abs(dc)
                return flt(dc)
if 1:   # RMS formula validation

    '''The RMS.odt document that discusses RMS measurements for hobbyists has a number of formulas
    for particular waveforms.  When giving such things, it's important that the equations be
    validated to to avoid wasting the reader's time or helping them make a mistaken decision or
    statement.

    In the document, the formulas are given a caption number of category "Formulas" and there is a
    string name of the formula after the "Formula X" part, where X is an integer.  This name is
    used here to identify the formula (I don't use the equation number because insertion of a new
    equation will mess up the numbering).

    '''

    def Check(a, b, reltol=1e-3, p=False):
        if a:
            tol = abs(a - b)/a
        else:
            if not b:
                return
            tol = abs(a - b)/b
        if p:
            Assert(tol <= reltol)
        else:
            fail = check_equal(a, b, reltol=reltol)
            if fail:
                fail = [f"{t.ornl}Arguments not equal:{t.n}", f"  a = {a!r}", f"  b = {b!r}"] + fail
                print('\n'.join(fail))
                exit(0)
    def Setup_Test_RMS():
        g.numpoints = 1000
        g.reltol = 1e-3     # Relative tolerance for comparisons
    def Test_RMS_sine():
        # No DC offset
        w = Waveform("sine", n=g.numpoints)
        Check(w.Vrms, sqrt(1/2))
        Check(w.Varms, sqrt(1/2))
        Check(w.Vdc, 0, p=1)
        Check(w.Vpp, 2)
        Check(w.Vpk, 1)
        Check(w.Vaa, 2/pi)
        Check(w.CF, sqrt(2))
        # With DC offset
        DC = 2
        w = Waveform("sine", n=g.numpoints, DC=DC)
        Check(w.Vrms, sqrt(1/2 + DC**2))
        Check(w.Varms, sqrt(w.Vrms**2 - w.Vdc**2))
        Check(w.Vdc, DC)
        Check(w.Vpp, 2 + DC)
        Check(w.Vpk, 1 + DC)
        Check(w.CF, sqrt(2))

        # Why is this failing?  The Vaa value should be the DC value plus the 2/pi for the no DC
        # offset case.
        # w.Vaa = 2.002002002002001
        # 2/pi = 0.6366197723675814
        # 2/pi + DC = 2.6366197723675815
        w = Waveform("sine", n=100, DC=DC)
        breakpoint() #xx 
        Check(w.Vaa, 2/pi + DC, p=0)

if 1:   # Core functionality
    pass

if 0:
    w = Waveform("sine", n=100)
    flt(0).N = 3
    if 0:
        w.plot()
    elif 1:
        w.remove_DC()
        w.fft()
    print(w)
    print(f"Name = {w.name}")
    print(f"  Vpp   = {w.Vpp}")
    print(f"  Vpk   = {w.Vpk}")
    print(f"  Vrms  = {w.Vrms}")
    print(f"  Varms = {w.Varms}")
    print(f"  Vaa   = {w.Vaa}")
    print(f"  Vdc   = {w.Vdc}")
    exit()

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["-v"]:
        Setup_Test_RMS()
        exit(run(globals(), halt=True, regexp="^Test_RMS")[0])
    else:
        print("Functionality needs to be written")
