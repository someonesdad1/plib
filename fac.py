'''
Use /usr/bin/factor to provide the prime factorization of integers
    Factor(3141596, unicode=True) produces 2²·37·21227
    Factor(3141596) produces 2^2*37*21227
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Use /usr/bin/factor to factor integers oo>
        <oo desc ∞ 
            Benefit:  handles large integers; weakness is speed for lots of
            factorings
        oo>
        <oo copy ∞ Copyright © 2023 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ math oo>
        <oo test ∞ --test oo>
        <oo todo ∞ 
        
            - ∞∞2 Move to primes.py?
        
        oo>
    '''
    if 1:  # Standard imports
        import collections
        import subprocess
    if 1:  # Custom imports
        pass
    if 1:  # Global variables
        pass
if 1:  # Core functionality
    def Factor(x, unicode=False):
        '''Return the string representing the prime factorization of integer x.  If
        unicode is True, use Unicode to represent the factorization.  Return None if
        something goes wrong.
        '''
        e = dict(zip(list(range(10)), "⁰¹²³⁴⁵⁶⁷⁸⁹"))    # Unicode representation
        if not (isinstance(x, int)):
            raise TypeError("x must be an integer")
        cmd = ["/usr/bin/factor", str(x)]
        try:
            r = subprocess.run(cmd, capture_output=True)
        except Exception:
            return None
        # Get list of prime factors
        s = r.stdout.decode("UTF-8").strip().split(":")[1].strip().split()
        factors = collections.deque(int(i) for i in s)
        if not factors:
            factors = collections.deque([1])
        d = collections.defaultdict(int)
        while factors:
            n = factors.popleft()
            d[n] += 1
        o = []
        # Generate ASCII form to check calculation
        for i in d:
            if d[i] > 1:
                o.append(f"{i}**{d[i]}")
            else:
                o.append(str(i))
        r = "*".join(o)
        assert eval(r) == x
        r = r.replace("**", "^")
        # Return the needed value
        if unicode:
            # Unicode form
            o = []
            for i in d:
                if d[i] > 1:
                    s = ""
                    for k in str(d[i]):
                        s += e[int(k)]
                    o.append(str(i) + s)
                else:
                    o.append(str(i))
            return "·".join(o)
        else:
            return r

if __name__ == "__main__":
    from math import factorial
    if 1:  # Header
        if 1:   # Standard imports
            import getopt
            import os
            import pprint
            import sys
        if 1:   # Custom imports
            import dptypes
            import wrap
            import trm
            import lwtest
            pp = pprint.pprint
            if 0:
                import debug
                debug.SetDebugger()
        if 1:   # Global variables
            t = trm.Trm()
            g = dptypes.Constant()
            g.dbg = False
    if 1:   # Utility
        def Test_Factor():
            x = factorial(100)
            s = (
                "2^97*3^48*5^24*7^16*11^9*13^7*17^5*19^5*23^4*29^3*31^3*"
                "37^2*41^2*43^2*47^2*53*59*61*67*71*73*79*83*89*97"
            )
            lwtest.Assert(Factor(x, unicode=False) == s)
            s = (
                "2⁹⁷·3⁴⁸·5²⁴·7¹⁶·11⁹·13⁷·17⁵·19⁵·23⁴·29³·31³·37²·41²·"
                "43²·47²·53·59·61·67·71·73·79·83·89·97"
            )
            lwtest.Assert(Factor(x, unicode=True) == s)
    if 1:   # Utility
        def GetColors():
            t.convert = t.purl
            t.num = t.yell
            t.num_prime = t.ornl 
            t.factors = t.whtl
            t.err = t.redl
        def GetScreen():
            'Return (LINES, COLUMNS)'
            return (
                int(os.environ.get("LINES", "50")),
                int(os.environ.get("COLUMNS", "80")) - 1
            )
        def Warn(*msg, status=1):
            print(*msg, file=sys.stderr)
        def Error(*msg, status=1):
            Warn(*msg)
            exit(status)
        def Usage(status=0):
            print(wrap.dedent(f'''
            Usage:  {sys.argv[0]} [options] num1 [num2...]
              Print the factorization of the indicated integers.  The numbers can be
              expressions and the math module is in scope.  If the argument is a float x,
              it is converted to an integer with int(round(x, 0)).
            Options:
                -h      Print a manpage
                --test  Run selftests
            '''))
            exit(status)
        def ParseCommandLine(d):
            do_test = False
            if len(sys.argv) < 2:
                Usage()
            try:
                opts, args = getopt.getopt(sys.argv[1:], "h", "test") 
            except getopt.GetoptError as e:
                print(str(e))
                exit(1)
            for o, a in opts:
                if o == "-h":
                    Usage()
                elif o == "--test":
                    do_test = True
            GetColors()
            if do_test:
                exit(lwtest.run(globals(), halt=True)[0])
            return args
    if 1:   # Core functionality
        def Report(n):
            s, is_float = "", False
            if isinstance(n, float):
                is_float = True
                s = "  "
            else:
                if not isinstance(n, int) or n < 1:
                    t.print(f"{t.err}{item!r} is not a positive integer > 0")
                    return
            factors = Factor(int(round(n, 0) if is_float else n), unicode=True)
            N = int(round(n, 0))
            is_prime = factors == str(N)
            # Print results
            if is_prime:
                if is_float:
                    t.print(f"{t.convert}{item} --> {n} --> {t.num_prime}{N}")
                    t.print(f"{s}{t.num_prime}{N} is prime")
                else:
                    t.print(f"{s}{t.num_prime}{n} is prime")
            else:
                N = int(round(n, 0))
                if is_float:
                    t.print(f"{t.convert}{item} --> {n} --> {t.num}{N}")
                t.print(f"{s}{t.num}{N}:  {t.factors}{factors}")
        d: dict[object, object] = {}  # Options dictionary
        args = ParseCommandLine(d)
        for item in args:
            Report(eval(item))
