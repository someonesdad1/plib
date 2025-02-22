'''
Generate random passwords
'''
 
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright © 2025 Don Peterson #∞copyright∞#
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
        import os
        import re
        import secrets
        import string
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
        Usage:  {sys.argv[0]} [options] length [N]
          Generate random passwords of length bytes.  N is the number of passwords to generate and
          defaults to 1.  If you don't use any options, the behavior will be if you used '-c lLd'
          and -s.
        Options:
            -b      Return bytestring
            -c str  Only use characters coded in str [{d["-c"]}]
            -h      Return a hex number (you'll get 2*length hex digits)
            -i      Return a base 10 integer with 8*length bits
            -s      Return a character string defined by -c
            -u      Return URL-safe string
            -x n    Return an XKCD-style password using n words
        Coding for -c:
            l       lowercase letters
            L       uppercase letters
            d       digits
            p       punctuation
            w       whitespace
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-b"] = False     # Return bytestring
        d["-c"] = "lLdp"    # Only use characters coded in the string
        d["-d"] = "/words/words.beale.2of12inf"    # Default words file
        d["-h"] = False     # Return a hex number
        d["-i"] = False     # Return an integer
        d["-s"] = False     # Return an character string defined by -c
        d["-u"] = False     # Return a URL-safe string
        d["-w"] = []        # Additional words files
        d["-x"] = False     # Return an XKCD-style password using length words
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "bc:d:hisuw:x") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("bhisux"):
                d[o] = not d[o]
                found = True
            elif o == "-c":
                s = set(a)
                if not s.issubset(set("lLdpw")):
                    Error("Only the letters lLdpw are allowed for -c option")
                d[o] = s
                found = True
            elif o == "-d":
                d[o] = a
            elif o == "-w":
                d[o].append(a)
        return args
if 1:   # Core functionality
    def Bytestring(length, N):
        for i in range(N):
            print(secrets.token_bytes(length))
    def HexNumber(length, N):
        for i in range(N):
            print(secrets.token_hex(length))
    def Integer(length, N):
        for i in range(N):
            print(secrets.randbits(8*length))
    def CharacterString(length, N):
        s = ""
        if "l" in d["-c"]:
            s += string.ascii_lowercase
        if "L" in d["-c"]:
            s += string.ascii_uppercase
        if "d" in d["-c"]:
            s += string.digits
        if "p" in d["-c"]:
            s += string.punctuation
        if "w" in d["-c"]:
            s += string.whitespace
        for i in range(N):
            pw = ''.join(secrets.choice(s) for j in range(length))
            print(pw)
    def URLSafeString(length, N):
        for i in range(N):
            print(secrets.token_urlsafe(length))
    def XKCDStyle(length, N):
        words = []
        with open(d["-d"]) as f:
            words.extend(list(word.strip() for word in f))
        for file in d["-w"]:
            with open(file) as f:
                words.extend(list(word.strip() for word in f))
        words = list(set(words))
        for i in range(N):
            password = ' '.join(secrets.choice(words) for i in range(length))
            print(password)

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    length = int(args[0])
    N = 1
    if len(args) == 2:
        N = int(args[1])
    if d["-b"]:
        Bytestring(length, N)
    elif d["-h"]:
        HexNumber(length, N)
    elif d["-i"]:
        Integer(length, N)
    elif d["-s"]:
        CharacterString(length, N)
    elif d["-u"]:
        URLSafeString(length, N)
    elif d["-x"]:
        XKCDStyle(length, N)
    else:
        d["-c"] = "lLd"
        CharacterString(length, N)
