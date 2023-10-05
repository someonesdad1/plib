'''
Generate passwords.
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Generate passwords.
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import math
        import os
        import random
        import secrets
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        from f import flt
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        class G:
            pass
        g = G()
        g.n = 1     # Number of passwords to generate
        g.words = None
        g.prg = secrets.choice
        t.inf = t("sky")
if 1:   # Utility
    def GetInt(option, x, low, high=None):
        try:
            n = int(x)
            if high is None:
                if n < low:
                    raise ValueError()
            else:
                if not (low <= n <= high):
                    raise ValueError()
            return n
        except ValueError:
            if high is None:
                Error(f"{option} option must be an integer >= {low}")
            else:
                Error(f"{option} option must be integer on [{low}, {high}]")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [n]
            Generate n passwords.  The passwords generated are not
            repeatable unless you use the -s option.
        Options:
            -c t    Cracking time in hours.  This gives an estimate of how
                    many word combinations must be tested per second to
                    find the password by brute force in t hours.
            -d f    Change dictionary file to f
            -j s    String to join words ['{d["-j"]}']
            -n n    Number of passwords to generate if not on command line
            -s s    Pseudorandom number generator seed
            -t m    Type of generator to use [{d["-t"]}]
            -w n    Number of words in password [{d["-w"]}]
        Generator types
          1   Dictionary words separated by '{d["-j"]}'
          2   7-bit ASCII characters
        Note:  estimate of cracking time is dependent on algorithms/cracker
        used.  If the password you want to crack is hashed, it's possible
        things like rainbow tables could be much faster than brute force.
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = 24        # Crack time in hours
        d["-d"] = None      # Dictionary file to use (None means default)
        d["-j"] = "."       # String to join words
        d["-n"] = 10        # Number of passwords to generate
        d["-s"] = None      # PRG seed
        d["-t"] = 1         # Which generator to use
        d["-w"] = 4         # Number of words
        try:
            opts, args = getopt.getopt(sys.argv[1:], "c:d:hj:n:s:t:w:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o == "-c":     # Crack time in hours
                d[o] = GetInt("-c", a, 1)
            elif o == "-d":     # Dictionary file
                d[o] = a
            elif o == "-j":     # String to join words
                d[o] = a
            elif o == "-n":     # Number of passwords to generate
                d[o] = GetInt("-n", a, 1)
                g.n = d[0]
            elif o == "-s":     # PRG seed
                random.seed(a)
                g.prg = random.choice
            elif o in "-t":     # Choose generator to use
                d[o] = GetInt("-n", a, 1, 2)
            elif o in "-w":     # Number of words
                d[o] = GetInt("-n", a, 2)
        if args:
            g.n = d["-n"] = int(args[0])
        return args
if 1:   # Core functionality
    def CrackSpeed(nw):
        '''Return how many passwords must be tested per second to 
        be able to crack the password using brute force in 24 hours.
        The returned string's units are Hz.
        '''
        seconds = flt(3600*d["-c"])
        cs = flt(nw)/seconds
        with cs:
            cs.N = 2
            return cs.sci
    def GetWords():
        if g.words is None:
            if d["-d"] is None:
                # This dict is from https://7esl.com/common-words/
                g.words = open("/pylib/pgm/words.x.1000.3").read().split("\n")
                g.words = [i for i in g.words if i and i[0] != "#" and len(i) > 2]
            else:
                g.words = open(d["-d"]).read().split("\n")
                g.words = [i for i in g.words if i and i[0] != "#" and len(i) > 2]
            if 1:
                # Print information on the passwords generated
                f = sys.stderr
                s = [len(i) for i in g.words]
                mx, mn = max(s), min(s)
                nw = len(g.words)
                np = float(nw)**d["-w"]    # Number of passwords generated
                s = P(sys.argv[0]).resolve()
                print(f"{t.inf}", file=f, end="")
                print(f"Script:  {s}", file=f)
                print(f"Seed:  {d['-s']}", file=f)
                print(f"Word list has {nw} words of [{mn}, {mx}] length", file=f)
                print(f"log10(number of possible passwords) = {math.log10(np):.1f}", file=f)
                print(f"Brute force cracking of password in {d['-c']} hours will take", file=f)
                print(f"  testing combinations at {CrackSpeed(np)} Hz.", file=f)
                t.print("", file=f)
            seed = d["-s"] if d["-s"] is not None else 0
            random.seed(seed)
            random.shuffle(g.words)
    def DictionaryWords(i, maxlen):
        GetWords()
        o = []
        for j in range(d["-w"]):
            o.append(g.prg(g.words))
        print(f"{i + 1:{maxlen}d}    {d['-j'].join(o)}")
    def ASCII_Characters():
        pass

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["-t"] == 1:
        g.n = int(args[0]) if args else 5
        for i in range(g.n):
            DictionaryWords(i, len(str(g.n)))
    elif d["-t"] == 2:
        ASCII_Characters()
    else:
        Error("-t number not recognized")
