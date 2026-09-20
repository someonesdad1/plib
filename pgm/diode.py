'''

Output useful information about diodes.
        
'''
if 1:  # Header
    if 1:   # Standard imports
        import collections
        import getopt
        import os
        import pathlib
        import re
        import sys
    if 1:   # Custom imports
        import scipy
        import columnize
        import dpstr
        import dptypes
        import f
        import termtables as tt
        import trm
        import wrap
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Core file gist information
        __gist__      = "Output useful information about diodes"
        __copyright__ = "Copyright © 2026 Don Peterson"
        __license__   = "MIT License (see /plib/_lic.mit)"
        __test__      = "notest"
        __category__  = "elec"
        __todo__      = ''' '''
    if 1:   # Import symbols
        Path = pathlib.Path
        defaultdict = collections.defaultdict
        deque = collections.deque
        namedtuple = collections.namedtuple
        #
        Columnize = columnize.Columnize
        dedent = wrap.dedent
        flt = f.flt
    if 1:   # Global variables
        t = trm.Trm()
        g = dptypes.Constant()
        g.dbg = False
if 1:   # Utility
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )
    def GetColors():
        t.dbg = "lil"
        t.err = "redl"
    def Dbg(*p, **kw):
        if not hasattr(Dbg, "file"):
            Dbg.file = sys.stdout
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.n}", end="", file=Dbg.file)
    def Warning(*msg, **kw):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warning(f"{t.err}", end="")
        Warning(*msg)
        Warning(f"{t.n}")
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [i_mA_1 [i_mA_2...]]
          Print the corresponding voltage for the 1N4148 diode for the given currents in
          mA.
        Options:
            -4      Use 1N4004 diode
            -n n    Number of significant digits [{d["-n"]}]
            -t      Print a table of voltage & current values
            -v      Interpret the arguments as voltages; print the currents
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-4"] = False  # Use 1N4004 diode
        d["-n"] = 3      # Number of significant digits
        d["-t"] = False  # Print a table
        d["-v"] = False  # Interpret arguments as voltages
        try:
            opts, args = getopt.getopt(sys.argv[1:], "4hn:tv")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        if len(sys.argv) < 2:
            Usage()
        for o, a in opts:
            if o[1] in list("4tv"):
                d[o] = not d[o]
            elif o == "-n":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except Exception:
                    Error(f"{o!r} option must be an int between 1 and 15")
            elif o == "-h":
                Usage(status=0)
        GetColors()
        g.W, g.L = GetScreen()
        return args

if 1:   # Classes
    class Diode:
        def __init__(self, V_mV, i_mA, name):
            self.V_mV = V_mV
            self.i_mA = i_mA
            self.name = name
            self.V_vs_i = scipy.interpolate.interp1d(self.i_mA, self.V_mV)
            self.i_vs_V = scipy.interpolate.interp1d(self.V_mV, self.i_mA)
        def V(self, i_mA):
            return flt(self.V_vs_i(i_mA))
        def i(self, V_mV):
            return flt(self.i_vs_V(V_mV))
        def Table(self, voltage=False):
            'Print a table; if voltage is true, print i(V) else V(i)'
            if voltage:
                o = [["mV", "mA", "Ω"]]
                if self.name == "1N4148":
                    start = 400
                elif self.name == "1N4004":
                    start = 550
                stop = int(self.V_mV[-1])
                for V_mV in range(start, stop, 10):
                    try:
                        i_mA = self.i(V_mV)
                        o.append([f"{V_mV:3d}", f"{i_mA}", f"{V_mV/i_mA}"])
                        #print(f"  {V_mV:3d}    {i_mA}")
                    except Exception:
                        continue
            else:
                o = [["mA", "mV", "Ω"]]
                start, stop = int(self.i_mA[0]), int(self.i_mA[-1])
                # Microamp data (convert to mA)
                μA = [flt(i/1000) for i in (10, 20, 50, 100, 200, 500, 1000, 2000, 3000,
                    4000, 5000, 6000, 7000, 8000, 9000)]
                for i_mA in μA:
                    try:
                        V_mV = self.V(i_mA)
                        #print(f"  {i_mA}    {V_mV}")
                        o.append([f"{i_mA}", f"{V_mV}", f"{V_mV/i_mA}"])
                    except Exception:
                        continue
                for i_mA in range(start, stop, 10):
                    try:
                        V_mV = self.V(i_mA)
                        #print(f"  {i_mA:3d}    {V_mV}")
                        o.append([f"{i_mA:3d}", f"{V_mV}", f"{V_mV/i_mA}"])
                    except Exception:
                        continue
            tt.print(o, style=" "*15, alignment="c"*3)
if 1:   # Data
    # Voltage is in mV, current is in mA
    d4148_V = [401, 433, 476, 508, 541, 582, 614, 646, 691, 729,
               771, 835, 861, 902, 978]
    d4148_i = [0.010, 0.0198, 0.0502, 0.1, 0.206, 0.508, 1.01, 2, 5.02, 10, 20.1,
               50, 70, 100, 201]
    d4148 = Diode(d4148_V, d4148_i, "1N4148")
    d4004_V = [557, 590, 620, 660, 692, 721, 756, 775, 800, 818, 828]
    d4004_i = [0.5, 1.06, 2.02, 5.01, 10.1, 20.9, 50.9, 101, 203, 500, 1000]
    d4004 = Diode(d4004_V, d4004_i, "1N4004")
if 1:   # Functions
    def PrintTable(voltage=False):
        diode.Table(voltage)
        exit(0)

if __name__ == "__main__":  
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    # Get diode = which diode model to use
    if d["-4"]:
        print("Diode = 1N4004")
        diode = d4004
    else:
        print("Diode = 1N4148")
        diode = d4148
    if d["-t"]:
        PrintTable(d["-v"])
    if args:
        for arg in args:
            if d["-v"]:     # Arguments are voltage in mV
                try:
                    print(f"{arg} mV  {diode.i(arg)} mA")
                except ValueError:
                    print(f"{arg} mV is out of bounds")
            else:           # Arguments are current in mA
                try:
                    print(f"{arg} mA  {diode.V(arg)} mV")
                except ValueError:
                    print(f"{arg} mA is out of bounds")
