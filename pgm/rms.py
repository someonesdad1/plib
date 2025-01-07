'''

Todo
    - plot:  use fixed aspect ratio and % of W
    - Use cases to address
        - Be able to enter amplitudes like pp, pk, rms, arms, ar, aa
            - One way to do this might be to use a root finder with setting the 0-peak value until
              you get the desired functional.
        - Add zb keyword again for zero-based waveforms (overrides the DC setting)

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
    
    - This script uses the optional plotext library that does a good job of plotting in a
      text-based terminal window, well enough to see basic behavior.  You can get it with 'pip
      install plotext' (see https://github.com/piccolomo/plotext/tree/master).
    
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
        from pathlib import Path as P
        from pprint import pprint as pp
        import getopt
        import math
        import statistics
        import numpy as np
        from numpy.fft import fft
        import numpy.random as random
        import os
        import re
        import sys
    if 1:   # Custom imports
        from columnize import Columnize
        from f import flt
        from wrap import dedent
        from color import t
        from roundoff import RoundOff
        from lwtest import run, Assert, check_equal, assert_equal
        import cmddecode
        import root
        import si
        #if len(sys.argv) > 1:
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
            print(dedent('''
                Use 'pip install plotext' to install the plotext library which allows plotting
                with text characters in the terminal.
            '''))
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
    def Manpage():
        print(dedent(f'''

        This script allows you to enter a waveform type and amplitude and see the various
        functionals associated with that waveform:
         
            Vdc     DC offset voltage
            Varms   AC-coupled RMS voltage
            Vdrms   DC-coupled RMS voltage
            Vpk     Peak voltage (mathematical amplitude)
            Vpp     Peak-to-peak voltage
            Vaa     Absolute average voltage
            Var     Average-responding voltmeter value (voltmeter with infinite bandwidth)
            CF      Crest factor

        The allowed input amplitude names are
            
            ampl    Mathematical amplitude
            pk      Same as ampl
            pp      Peak-to-peak (e.g., measured with a scope)
            rms     DC-coupled RMS 
            arms    AC-coupled RMS (no DC component)
            ar      Average-responding voltmeter value
            aa      Absolute average

        Use cases

        - Converting measured values
            - I measured a square wave with an HP 400EL average-responding meter as 2.25 V.  What
              is the ARMS value of this waveform?
                - Use the command line = 'sq ar=2.5'
                - The result is Varms = 2.02
                - The HP 3400A measured 2.02 V
                - Note the script doesn't assume any units for the amplitude, but much of the time
                  you'll probably want to assume volts or amps.
                - Note:  these are measured results with HP 400 EL and 3400A voltmeters for a
                  square wave at 100 Hz.  Changing to 1 MHz gave 2.26 V on the 400EL and 2.05 V
                  mV on the 3400A.  This script would predict the ARMS value of 2.034 V for such
                  a Var measurement.  Thus, you must be cognizant of the instruments' bandwidths
                  to make meaningful comparisons.
                - For the 100 Hz signal, a Simpson 260-7 measured 2.19 V; it's also an
                  average-responding voltmeter.

        '''))
        exit(0)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] waveform A=1 f=1 D=0.5 DC=0
          Calculations related to RMS values.  waveform can be 
                sine   square   triangle   noise   ramp   halfsine
          A sets the amplitude.  It can be one of
            a       Mathematical amplitude
            pk      0-to-peak (mathematical amplitude)
            pp      Peak-to-peak
            rms     DC-coupled RMS value
            arms    AC-coupled RMS value
            aa      Absolute average
            ar      Average-responding voltmeter value
          The subsequent parameters are optional:
                f           Frequency
                T           Period (overrides f)
                n           Number of points in waveform
                D           Duty cycle (triangle, square only)
                DC          DC offset
          You can include a single cuddled SI prefix as the last character, which is stripped and
          the remaining string is evaluated as an expression (the math module's symbols are in
          scope).  A report is printed with the common functionals and statistics.
        Options:
            -d n    Set number of digits [{d['-d']}]
            -h      Print a manpage
            -f      Plot the FFT
            -p      Plot the graph
            -v      Validate the formulas in the RMS document
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 3         # Number of digits in report
        d["-f"] = False     # Plot FFT
        d["-p"] = False     # Plot waveform
        d["-v"] = False     # Validate formulas in the RMS document
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:fhpv") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("fpv"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    Error("-d option's argument must be an integer between 1 and 15")
            elif o == "-h":
                Manpage()
        flt(0).N = d["-d"]
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
    def Check(a, b, reltol=1e-3, p=True):
        if a:
            tol = RoundOff(abs(a - b)/a)
        else:
            if not b:
                return
            tol = RoundOff(abs(a - b)/b)
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
        Check(w.Vdrms, math.sqrt(1/2))
        Check(w.Varms, math.sqrt(1/2))
        Check(w.Vdc, 0, p=1)
        Check(w.Vpp, 2)
        Check(w.Vpk, 1)
        Check(w.Vaa, 2/math.pi)
        Check(w.CF, math.sqrt(2))
        # With DC offset
        DC = 2
        w = Waveform("sine", n=g.numpoints, DC=DC)
        Check(w.Vdrms, math.sqrt(1/2 + DC**2))
        Check(w.Varms, math.sqrt(w.Vdrms**2 - w.Vdc**2))
        Check(w.Vdc, DC)
        Check(w.Vpp, 2 + DC)
        Check(w.Vpk, 1 + DC)
        Check(w.CF, math.sqrt(2))
        # xx Why is this failing?  The Vaa value should be the DC value plus the 2/pi for the no DC
        # offset case.
        # w.Vaa = 2.002002002002001
        # 2/pi = 0.6366197723675814
        # 2/pi + DC = 2.6366197723675815
        w = Waveform("sine", n=100, DC=DC)
        breakpoint() #xx 
        Check(w.Vaa, 2/math.pi + DC, p=0)
if 1:   # Waveform class
    class Waveform:
        '''Construct a basic waveform in a numpy array (the t and V properties have the arrays).
        The resulting object instance then has the following functionals (all are flt type):
        
            Vdc     DC offset voltage
            Varms   AC-coupled RMS voltage
            Vdrms   DC-coupled RMS voltage
            Vpk     Peak voltage (mathematical amplitude)
            Vpp     Peak-to-peak voltage
            Vaa     Absolute average voltage
            Var     Average-responding voltmeter value
            CF      Crest factor
            
        You can set the following properties of the waveform (* means read-only)
        
            n       (int)   Number of points in waveform (must be > 0)
            ampl    (flt)   Mathematical amplitude (must be > 0)
            f       (flt)   Frequency (must be > 0)
            T     * (flt)   Period = 1/f (must be > 0)
            DC      (flt)   DC offset
            D       (flt)   Duty cycle on (0, 1)
        
        The physical units for these properties are unspecified, but it's fine to assume volts for
        amplitude/DC and seconds for time because the intent is to model voltage waveforms as a
        function of time (hence the V and t property arrays).
        
        One period of the waveform contains n points, but the endpoint is missing.  Thus, for a
        sine wave, the "natural" thing to do would be to include the points from 0 to 2*pi
        inclusive.  However, by eliminating the last point, the arrays can be concatenated to
        make multiple periods.
        
        Print the waveform instance to stdout to get a report on its attributes and functionals.
        '''
        names = set((
            "sine",
            "square",
            "triangle",
            "ramp",
            "noise",
            "halfsine",
        ))
        def __init__(self, name="sine", n=100, ampl=1, f=1, T=None, DC=0, D=0.5, zb=False):
            '''Keywords:
                name (str)      Name of waveform
                n    (int)      Number of points in one period
                ampl (flt)      Mathematical amplitude (0-to-peak amplitude)
                f    (flt)      Frequency
                T    (flt)      Period (setting T overrides f's value)
                DC   (flt)      DC offset
                D    (flt)      Duty cycle
                zb   (bool)     If true, use a zero baseline (overrides DC)
            
            These keyword arguments can also be a string and may have an SI prefix as a suffix to
            indicate magnitudes.  This prefix must only be one character and must be the last
            character (excluding whitespace).  After this optional SI prefix is stripped off, the
            string is evaluated as an expression with the math module's symbols in scope.
            '''
            # Set the defining attributes
            self._name = name
            self._n = self.interpret(n, typ=int)
            self._ampl = self.interpret(ampl)
            self._f = 1/self.interpret(T) if T is not None else self.interpret(f)
            self._DC = self.interpret(DC)
            self._D = self.interpret(D)
            self._zb = bool(zb)
            self.validate_attributes()
            # Make the waveform
            if name in Waveform.names:
                self.construct()
            else:
                raise ValueError(f"Waveform name {name!r} is not recognized")
        def interpret(self, value, typ=flt):
            '''Return a number of type typ representing what was in value.  value can be either a
            number or string convertible to typ.  If it's a string, search for an SI prefix as a
            suffix used to indicate magnitude.
            '''
            # Import math symbols
            from math import acos, acosh, asin, asinh, atan, atan2, atanh, cbrt, ceil, copysign, cos
            from math import cosh, degrees, dist, erf, erfc, exp, exp2, expm1, fabs, factorial, floor
            from math import fmod, frexp, fsum, gamma, gcd, hypot, isclose, isfinite, isinf, isnan
            from math import isqrt, lcm, ldexp, lgamma, log, log1p, log10, log2, modf, pow, radians
            from math import remainder, sin, sinh, sqrt, tan, tanh, trunc, prod, perm, comb, nextafter
            from math import ulp, pi, e, tau, inf, nan
            if not ii(value, str):
                return typ(value)
            # It's a string
            s = value.strip()
            if not s:
                raise ValueError("Argument needs to be a non-empty string")
            # Look for an SI prefix as a suffix ('d', 'c', 'da', 'h' are not allowed)
            last_char = s[-1]
            if last_char in si.si:
                factor = 10**si.si[last_char]
                s = s[:-1]
            value = eval(s)
            return typ(factor*value)
        def validate_attributes(self):
            if not ii(self._name, str):
                raise TypeError(f"name must be a string")
            if self._n <= 0 or not ii(self._n, int):
                raise ValueError(f"n = number of points must be integer > 0")
            if self._ampl <= 0:
                raise ValueError(f"ampl = mathematical amplitude must be > 0")
            if self._f <= 0:
                raise ValueError(f"Frequency f and period T must be > 0")
            if not (0 < self._D < 1):
                raise ValueError(f"D = duty cycle must be between 0 and 1 exclusive")
        def __str__(self):
            'Return a string representing the waveform with functionals and basic statistics'
            header = repr(self) + "\n"
            # Put the following in columns
            o = []
            o.append(f"Vdc   = {self.Vdc}")
            o.append(f"Varms = {self.Varms}")
            o.append(f"Vdrms = {self.Vdrms}")
            o.append(f"Vpk   = {self.Vpk}")
            o.append(f"Vpp   = {self.Vpp}")
            o.append(f"Vaa   = {self.Vaa}")
            o.append(f"Var   = {self.Var}")
            o.append(f"CF    = {self.CF}")
            o.append(f"")
            o.append(f"  Statistics")
            o.append(f"mean  = {flt(self.y.mean())}")
            o.append(f"s     = {flt(self.y.std())}")
            o.append(f"var   = {flt(self.y.var())}")
            o.append(f"max   = {flt(self.y.max())}")
            o.append(f"min   = {flt(self.y.min())}")
            o.append(f"range = {flt(abs(self.y.max() - self.y.min()))}")
            o.append(f"")
            o.append(f"  Deciles")
            dec = statistics.quantiles(self.y, n=10)
            for i in range(1, 10):
                o.append(f"{10*i}%   = {RoundOff(flt(dec[i - 1]))}")
            W = int(os.environ.get("COLUMNS", "80")) - 1
            out = []
            for i in Columnize(o, columns=3, col_width=W//4, indent=" "*2):
                out.append(i)
            return header + '\n'.join(out)
        def __repr__(self):
            s = (f"Waveform({self._name!r}, n={self._n}, ampl={self._ampl}, f={self._f}, "
                 f"DC={self.DC}")
            if self._name not in ("sine", "noise"):
                s += f", D={self.D}"
            s += f")"
            return s
        def construct(self):
            '''Construct the numpy arrays for the waveform:  
                self.x      Contains the abscissas of one period
                self.y      Contains the ordinates of one period
                self.t      Contains the time values (abscissas) for all periods
                self.V      Contains the voltages (ordinates) for all periods
            
            self.x and self.y are kept because they are needed to calculate the functionals for
            the waveform.
            
            self.t and self.V contain all the points specified for the waveform.
            
            As of this writing, the only waveforms affected by duty cycle are 'square' and
            'triangle'.  For the triangle wave, changing D really affects the symmetry, not the
            duty cycle.
            
            'ramp' could be a candidate for this, where the result would be a plain
            ramp for D == 1 and ramp pulses for D < 1.
            '''
            n, D, T = self._n, self._D, 1/self._f
            dx = 1/n
            x = np.arange(0, 1, dx)     # This will become self.x
            if 1:   # Construct an array of one period
                if self._name == "sine":
                    x = np.arange(0, 2*math.pi, 2*math.pi*dx)
                    self.y = np.sin(x)
                elif self._name == "square":
                    npos = int(D*n)     # Number of points in positive portion
                    nneg = n - npos     # Number of points in negative portion
                    first = np.arange(0, npos)*0.0 + 1.0
                    second = np.arange(0, nneg)*0.0 - 1.0
                    self.y = np.concatenate((first, second), axis=None)
                elif self._name == "triangle":
                    # The five key points on the waveform are:
                    # (0, 0) and ((D*T/2, 1)            From 0 to n1        Section 1
                    # (D*T/2, 1) and (T/2, 0)           From n1 + 1 to n2   Section 2
                    # (T/2, 0) and (T*(1 - D/2), -1)    From n2 + 1 to n3   Section 3
                    # (T*(1 - D/2), -1) and (0, T)      From n3 + 1 to n    Section 4
                    T = x[-1] - x[0] + dx     # "period" in x space
                    # Indexes of the key points
                    n1 = int(round(D*n/2, 0))
                    n2 = int(round(n/2, 0))
                    n3 = n - n1
                    # Section 1
                    m, b = SlopeAndIntercept(0, 0, D*T/2, 1)
                    y1 = m*x[0:n1 + 1] + b
                    # Section 2
                    m, b = SlopeAndIntercept(D*T/2, 1, T/2, 0)
                    y2 = m*x[n1 + 1:n2 + 1] + b
                    # Section 3
                    m, b = SlopeAndIntercept(T/2, 0, T*(1 - D/2), -1)
                    y3 = m*x[n2 + 1:n3 + 1] + b
                    # Section 4
                    m, b = SlopeAndIntercept(T*(1 - D/2), -1, T, 0)
                    y4 = m*x[n3 + 1:] + b
                    # Put waveform's sections together
                    self.y = np.concatenate((y1, y2, y3, y4), axis=None)
                elif self._name == "ramp":
                    # The key points on the waveform are:
                    # (0, -1) and (T, 1)
                    T = x[-1] - x[0] + dx
                    m, b = SlopeAndIntercept(0, -1, T, 1)
                    self.y = m*x + b
                elif self._name == "noise":
                    self.y = random.normal(size=self.n)
                elif self._name == "halfsine":
                    self._name = "sine"
                    self.construct()
                    self._name = "halfsine"
                    # Set the negative elements to zero
                    self.y = np.where(self.y >= 0, self.y, 0)
                else:
                    raise RuntimeError(f"Bug:  {self._name!r} is unknown waveform name")
            if 1:   # Scale waveform to proper amplitude and add DC offset
                self.y *= self._ampl
                if self._DC:
                    self.y += self._DC
                self.x = x
            if 1:   # Generate time waveform self.t
                self.t = np.arange(0, T, T/n)
            if 1:   # Check invariants
                Assert(len(self.x) == n)
                Assert(len(self.y) == n)
                Assert(len(self.t) == n)
        def multiple_periods(self, num_periods):
            'Return two numpy arrays t and V that contain the desired number of periods'
            if not ii(num_periods, (flt, float, int)) or num_periods <= 0:
                raise TypeError("num_periods must be an int, float, or flt")
            if num_periods <= 0:
                raise ValueError("num_periods must be > 0")
            assert len(self.y) == self._n, "Incorrect number of points in waveform"
            nper = float(num_periods)
            self.z = self.y.copy()
            frac_part, int_part = math.modf(nper)
            # Integer number of concatenations
            for i in range(int(int_part) - 1):
                self.z = np.concatenate((self.z, self.y), axis=None)
            # Fractional number of concatenations
            m = int(round(self._n*frac_part, 0))
            assert m >= 0
            if m:
                self.z = np.concatenate((self.z, self.y[:m]), axis=None)
            # Check we have the right number of points
            npoints = int(round(nper*self._n, 0))
            # Make the voltage waveform V
            V = self.z
            Assert(len(V) == npoints)
            # Generate time waveform t
            total_time = nper/self._f
            dt = total_time/self._n
            t = np.arange(0, total_time, dt)
            # Return the arrays
            Assert(len(t) == npoints)
            return t, V
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
            dft, t = dft[:half], self.t[:half]
            # Double every element except the first, which is DC
            dc = dft[0]
            dft *= 2
            dft[0] = dc
            # Make a bar chart
            plt.bar(t, np.abs(dft))
            if title:
                plt.title(title)
            else:
                plt.title("FFT")
            plt.xlabel("Frequency")
            plt.ylabel("Voltage²")
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
            #plt.plot(self.t, self.y)
            plt.scatter(self.t, self.y)
            if title:
                plt.title(title)
            plt.xlabel("Time")
            plt.ylabel("Voltage")
            plt.grid()
            if fit:
                GetScreen()
                W, H = g.W, g.H
            plt.plot_size(W, H)
            plt.show()
        def remove_DC(self):
            self.y -= self.Vdc
        def copy(self):
            'Return a copy of this waveform'
            w = Waveform(self.name)
            w._ampl = self._ampl
            w._f = self._f
            w._n = self._n
            w._D = self._D
            w._DC = self._DC
            w.construct()
            w.t = self.t
            w.y = self.y
            return w
        if 1:   # Writable properties
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
            # Amplitude
            @property
            def ampl(self):
                return self._ampl
            @ampl.setter
            def ampl(self, value):
                self._ampl = flt(value)
                self.construct()
            # Frequency
            @property
            def f(self):
                return self._f
            @f.setter
            def f(self, value):
                self._f = flt(value)
                self.construct()
            # Period
            @property
            def T(self):
                return 1/self._f
            @T.setter
            def T(self, value):
                self._f = 1/flt(value)
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
                self.construct()
            # zb (zero baseline)
            @property
            def zb(self):
                return self._zb
            @zb.setter
            def zb(self, value):
                self._zb = bool(value)
                self.construct()
        if 1:   # Read-only properties
            # Period
            @property
            def T(self):
                return flt(self.x[-1] - self.x[0])
        if 1:   # Functionals
            @property
            def Vpp(self):
                'Return the peak-to-peak value'
                return flt(abs(max(self.y)) + abs(min(self.y)))
            @property
            def Vpk(self):
                'Return the 0-to-peak value (mathematical amplitude)'
                return flt(max(abs(max(self.y)), abs(min(self.y))))
            @property
            def Vdrms(self):
                'Return the DC-coupled RMS value'
                dx = self.x[1] - self.x[0]  # Needed to use the integral definition
                return flt(np.sqrt(np.sum(dx*np.square(self.y))/self.T))
            @property
            def Varms(self):
                'Return the AC-coupled RMS (ARMS) value'
                diff = self.Vdrms**2 - self.Vdc**2
                # Take the absolute value to protect against situations like a square wave with
                # duty cycle of D = 1e-6, where the diff will be -1.0000196170922848e-05; this
                # is essentially zero, but results in a runtime warning.
                return flt(np.sqrt(abs(diff)))
            @property
            def Vaa(self):
                '''Return the absolute average value.  This is the integral of the absolute value
                over the period.
                '''
                dx = self.x[1] - self.x[0]
                return flt(np.sum(np.abs(dx*self.y))/self.T)
            @property
            def Var(self):
                '''Calculate what an average-responding voltmeter would measure:  
                    - Remove any DC component
                    - Calculate Vaa = integral over period of absolute value of waveform
                    - Return Vaa*pi/(2*math.sqrt(2))
                This gives the RMS value for a sine wave.
                '''
                w = self.copy()
                w.DC = 0        # Remove any DC offset
                const = math.pi/(2*math.sqrt(2))   # = 1.11072
                return flt(w.Vaa*const)
            @property
            def CF(self):
                '''Calculate the crest factor.  The definition is Vpk/Vdrms.  If Vdrms is zero, this
                will return a crest factor of zero.
                '''
                return self.Vpk/self.Vdrms if self.Vdrms else flt(0)
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
            @property
            def CF(self):
                pk = self.Vpk
                rms = self.Varms
                return flt(pk/rms) if rms else flt(1)
if 1:   # Core functionality
    def GetKeyword(s):
        '''A form of name=val is expected.  Return (name, flt(val)).
        name must be 
            a pk pp rms arms aa ar f T n D DC zb
        '''
        allowed = "a pk pp rms arms aa ar f T n D DC zb"
        try:
            name, value = s.split("=")
        except Exception:
            Error(f"Parameter {s!r} is of improper form")
        if name not in allowed.split():
            Error(f"Name {name!r} not one of '{allowed}'")
        # Process value
        # Look for an SI prefix as a suffix ('d', 'c', 'da', 'h' are not allowed)
        last_char = value[-1]
        factor = 1
        if last_char in si.si:
            factor = 10**si.si[last_char]
            value = value[:-1]
        value = factor*eval(value)
        if name == "n":
            value = int(value)
        elif name == "zb":
            value = bool(value)
        else:
            value = flt(value)
        return name, value
    def GetWaveformParameters(**kw):
        '''Return a dict of the needed waveform parameters:
            name n ampl f DC D zb
        '''
        name = kw["name"]
        # Calculate the mathematical amplitude from the given functional value
        if "ar" in kw:
            pass
        elif "aa" in kw:
            pass
        elif "arms" in kw:
            pass
        elif "rms" in kw:
            pass
        elif "pp" in kw:
            pass
        elif "pk" in kw:
            pass
        elif "a" in kw:
            pass

        exit() #xx
if 0:
    np.set_printoptions(
        precision=4,
        threshold=201,
        linewidth=int(os.environ.get("COLUMNS", "80")) - 1,
        suppress=True,
    )
    w = Waveform("sine", ampl="sin(1.2)m", n=1000, f=1, DC=0.5)

    if 0:
        w.plot()
        print()
    if 0:
        w.remove_DC()
        w.fft()
    print(w)
    exit()
if __name__ == "__main__":
    getname = cmddecode.CommandDecode(Waveform.names)
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["-v"]:
        Setup_Test_RMS()
        exit(run(globals(), halt=True, regexp="^Test_RMS")[0])
    else:
        # Get waveform name
        name = args[0]
        x = getname(name)
        if not x:
            Error(f"Waveform {name!r} unrecognized")
        elif len(x) > 1:
            # Ambiguous, so must have been 's' for sine or square
            name = "sine"
            #Error(f"{name!r} is ambiguous:  {x}")
        else:
            name = x[0]
        kw = {}
        kw["name"] = name
        # Get other parameters
        for i in args[1:]:
            param, value = GetKeyword(i)
            kw[param] = value
        kw = GetWaveformParameters(**kw)
        # Construct waveform
        w = Waveform(name, **kw)
        if d["-p"]:
            w.plot()
        if d["-f"]:
            w.fft()
        print(w)
