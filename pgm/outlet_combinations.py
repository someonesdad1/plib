'''
'''
_pgminfo = '''
<oo 
    Prints out combinatorial properties of 3-wire electrical systems such as that used in
    the usual 120 V appliances in US homes.
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat elec oo>
<oo test none oo>
<oo todo

    - The "standard" problem is 3 wires with four possible connections:  hot, neutral,
      ground, and no connection.  The assumption is the electrical supply is properly
      wired.
    - The rare problem is the above with five possible connections:  hot1, hot2,
      neutral, ground, and no connection.  Dennis D. told me that this has happened in
      some RV parks and is of course very damaging to an RV.

oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        from itertools import product
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from dpprint import PP
        import termtables as tt
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:   # Utility
    def GetColors():
        t.err = t.redl 
        t.hot = t.redl
        t.neu = t.yell
        t.gnd = t.grnl
        t.nc = t.blul
        t.hog = t.magl
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
    def Warn(*msg, status=1):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warn(*msg)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [case]
          Print out all combinations of wiring connections for the following cases:
            1   Hot, neutral, ground, no connection
        Comment:
          Case 1 shows the 4³ = 64 possible ways of wiring "H" (hot), "N" (neutral), "G"
          (ground), and "." (no connection) to the H, N, and G connection screws on a
          NEMA5-15 duplex outlet and the resulting lights of a typical outlet tester.
          Many of these states are unrealistic in that they would likely only result
          from a malicious person trying to cause harm or are situations that would only
          arise in an academic sense.  For example, the dangerous case 1 that lights up
          no outlet tester lights yet could be hazardous is someone touched a metallic
          appliance could only happen if a malicious person pig-tailed three conductors
          to hot and wired them to the N, N, and G screws in the outlet.  For a real
          outlet, the three wires coming into the outlet would each need to go to a
          screw; the miswired states of importance for these have a B under the Basic
          column in the report -- and these are the most likely incorrectly-wired
          situations you'll probably see.
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Need description
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
        GetColors()
        return args
if 1:   # Core functionality
    def GetState(connection):
        '''Return a number indicating the state of the indicator lights.
        connection will be a three-tuple of the characters 'H', 'N', 'G',
        or '.'.  An indicator light can be on if the connection is HN or
        HG.  The three lights are
            N-G     neutral to ground
            N-H     neutral to hot
            G-H     ground to hot
        Considering them as bits on or off, N-G is the MSB and G-H the LSB.
        We get the following 7 states from binary counting:
            State   Lights on
            0     None
            1     G-H
            2     N-H
            3     N-H, G-H
            4     N-G
            5     N-G, G-H
            6     N-G, N-H
            7     N-G, N-H, G-H
        '''
        def IsOn(a, b):
            '''Return 1 if the pair of signals a and b cause a light to be
            on.  a and b can have the values "H", "N", "G", and ".".  To
            be on, the pair must be H-N or H-G.
            '''
            assert len(a) == 1 and len(b) == 1 and a in "HNG." and b in "HNG."
            if (a == "H" and b in "NG") or (a in "NG" and b in "H"):
                return 1
            return 0
        H, N, G = connection
        bit2, bit1, bit0 = IsOn(N, G), IsOn(N, H), IsOn(G, H)
        return (bit2 << 2) + (bit1 << 1) + bit0
    def Lights(state):
        di = { 
            0: "○ ○ ○",
            1: "○ ○ ●",
            2: "○ ● ○",
            3: "○ ● ●",
            4: "● ○ ○",
            5: "● ○ ●",
            6: "● ● ○",
            7: "● ● ●",
        }
        return di[state]
    def Colorize(s):
        if s == "H":
            return f"{t.hot}H{t.n}"
        elif s == "N":
            return f"{t.neu}N{t.n}"
        elif s == "G":
            return f"{t.gnd}G{t.n}"
        elif s == ".":
            return f"{t.nc}.{t.n}"
        else:
            Error(f"{s!r} not recognized")
    def Basic(hot, neutral, ground):
        '''Return True if the arguments are H, N, and G, which would be e.g. what you'd
        have if each of the three wires had to be connected to an outlet's screws.
        '''
        assert len(hot) == 1 and len(neutral) == 1 and len(ground) == 1
        if hot == "H":
            if neutral == "N":
                if ground == "G":
                    return True
            elif neutral == "G":
                if ground == "N":
                    return True
        elif hot == "N":
            if neutral == "H":
                if ground == "G":
                    return True
            elif neutral == "G":
                if ground == "H":
                    return True
        elif hot == "G":
            if neutral == "N":
                if ground == "H":
                    return True
            elif neutral == "H":
                if ground == "N":
                    return True
        return False
    def Case1():
        'Hot, neutral, ground, no connection'
        items = "H N G .".split()
        number, o = 1, []
        for connection in product("HNG.", repeat=3):
            hot, neutral, ground = connection
            s_h = Colorize(hot)
            s_n = Colorize(neutral)
            s_g = Colorize(ground)
            hot_on_ground = f"{t.hog}*{t.n}" if ground == "H" else " "
            state = GetState(connection)
            lights = Lights(state)
            basic = "B" if Basic(hot, neutral, ground) else " "
            if hot == "H" and neutral == "N" and ground == "G":
                c = t.whtl
                o.append([c + str(number) + t.n, 
                            c + "H" + t.n, 
                            c + "N" + t.n, 
                            c + "G" + t.n,
                            c + "Correct wiring" + t.n,
                            str(state),
                            lights,
                            basic])
            else:
                o.append([str(number), s_h, s_n, s_g, hot_on_ground, str(state), lights, basic])
            number += 1
        header = "Number Hot Neutral Ground Dangerous State Lights Basic".split()
        copy = o.copy()
        copy.append(header)
        tt.print(copy, header=header, padding=(0, 0), style=" "*15, alignment="c"*len(o[0]))
        # Now print sorted by state
        f = lambda x: x[5]
        copy = sorted(o.copy(), key=f)
        copy.append(header)
        t.print(f"\n{t.ornl}Same list except sorted by state")
        tt.print(copy, header=header, padding=(0, 0), style=" "*15, alignment="c"*len(o[0]))

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    case = int(args[0])
    if case == 1:
        Case1()
    else:
        Error(f"Case {case} not recognized")
