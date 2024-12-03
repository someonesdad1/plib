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
        from pathlib import Path as P
        import getopt
        import numpy as np
        import numpy.random as random
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
        g.have_plotext = True
        try:
            import pplotext as plt
        except ImportError:
            g.have_plotext = False
        g.have_plotext = False
if 1:   # Utility
    def GetColors():
        t.err = t("redl")
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
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
if 1:   # RMS formula validation
    class Waveform:
        '''Construct a basic waveform in a numpy array (the .data property has the array).
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
        def __init__(self, name):
            '''Attributes
            N           (int)   Number of points [100]
            D           (flt)   Duty cycle
            DC          (flt)   DC offset
            CF          (flt)   Crest factor (adjusts D to get desired CF)
            zero_baseline (bool)  Set to True for a 0 baseline (sets DC offset)
            '''
            self._name = name
            self.reset()
            if name in Waveform.names:
                self.construct()
            else:
                raise ValueError(f"{name!r} is not recognized")
        def reset(self):
            'Set attributes to defaults'
            self.x = None
            self.y = None
            self._N = 1000
            self._D = flt(0.5)
            self._DC = flt(0)
            self._CF = None
            self._zero_baseline = False
        def construct(self):
            if self._name == "sine":
                x = 2*np.pi
                # Need to include endpoint at 2*pi to get proper integration
                dx = x/(self.N + 1)
                self.x = np.arange(0, x + dx, x/self.N)
                self.y = np.sin(self.x)
                if self._DC:
                    self.y += self._DC
                elif self._zero_baseline:
                    self.y += 1
            elif self._name == "square":
                self.x = np.arange(0, 1, 1/self.N)
                n = int(self._D*self.N)
                first = np.arange(0, n)*0.0 + 1.0
                m = int((1 - self._D)*self.N)
                second = np.arange(0, m)*0.0 - 1.0
                self.y = np.concatenate((first, second), axis=None)
                if self._DC:
                    self.y += self._DC
                elif self._zero_baseline:
                    first = np.arange(0, n)*0.0 + 1.0
                    second = np.arange(0, m)*0.0
                    self.y = np.concatenate((first, second), axis=None)
            elif self._name == "triangle":
                self.x = np.arange(0, 1, 1/self.N)
            elif self._name == "ramp":
                breakpoint() #xx
            elif self._name == "noise":
                self.x = np.arange(0, 1, 1/self.N)
                self.y = random.normal(size=self.N)
                if self._DC:
                    self.y += self._DC
            elif self._name == "halfsine":
                breakpoint() #xx
            else:
                raise RuntimeError(f"Bug:  {self._name!r} is unknown waveform name")
        def plot(self, title="", W=40, H=15):
            if not g.have_plotext:
                print("plotext library not installed", file=sys.stderr)
                return
            plt.theme("clear")
            plt.plot(self.x, self.y)
            if title:
                plt.title(title)
            plt.grid()
            plt.plot_size(W, H)
            plt.show()
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
            # Number of points in waveform
            @property
            def N(self):
                return self._N
            @N.setter
            def N(self, value):
                n = int(value)
                if n <= 0:
                    raise ValueError("Property N must be integer > 0")
                self._N = n
                self.construct()
            # Duty cycle
            @property
            def D(self):
                return self._D
            @D.setter
            def D(self, value):
                D = flt(value)
                if not 0 <= D <= 1:
                    raise ValueError("Property D must be flt on [0, 1]")
                self._D = D
                self.construct()
            # DC offset
            @property
            def DC(self):
                return flt(self._DC)
            @DC.setter
            def DC(self, value):
                self._DC = flt(value)
                self._zero_baseline = False
                self.construct()
            # Crest factor
            @property
            def CF(self):
                return self._CF
            @CF.setter
            def CF(self, value):
                cf = flt(value)
                if cf < 1:
                    raise ValueError("Property CF must be >= 1")
                self._D = cf
                self.construct()
            # Zero baseline
            @property
            def zero_baseline(self):
                return self._zero_baseline
            @zero_baseline.setter
            def zero_baseline(self, value):
                self._zero_baseline = bool(value)
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
                return flt(sum(abs(dx*self.y))/T)
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

    for name in Waveform.names:
        if name in ("triangle", "ramp", "halfsine"):
            continue
        w = Waveform(name)
        w.N = 100
        if 0:
            w.plot(W=80, H=20)
        print(f"Name = {w.name}")
        print(f"  Vpp   = {w.Vpp}")
        print(f"  Vpk   = {w.Vpk}")
        print(f"  Vrms  = {w.Vrms}")
        print(f"  Varms = {w.Varms}")
        print(f"  Vaa   = {w.Vaa}")
        print(f"  Vdc   = {w.Vdc}")
    exit()

    def ValidateFormulas():
        '''The RMS.odt document that discusses RMS measurements for hobbyists has a number of
        formulas for particular waveforms.  When giving such things, it's important that the
        equations be validated to to avoid wasting the reader's time or helping them make a
        mistaken decision or statement.

        In the document, the formulas are given a caption number of category "Formulas" and there
        is a string name of the formula after the "Formula X" part, where X is an integer.  This
        name is used here to identify the formula (I don't use the number because reorganization 
        or insertion of a new section will mess up the numbering).

        '''
        print("Validating formulas")

if 1:   # Core functionality
    pass

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["-v"]:
        ValidateFormulas()
    else:
        print("Functionality needs to be written")
