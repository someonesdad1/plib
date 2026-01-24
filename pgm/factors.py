_pgminfo = '''
<oo 
    Print all factors of an integer
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat oo>
<oo test none oo>
<oo todo oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        import getopt
        import sys
        from itertools import combinations
    if 1:   # Custom imports
        from columnize import Columnize
        from primes import AllFactors, IsPrime, FactorList
        from wrap import dedent
        from color import t
    if 1:   # Global variables
        t.num = t.viol
        t.cnt = t.ornl
        t.prime = t.redl
        t.comp = t.wht
if 1:   # Utility
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} n1 [n2...]
          Print all factors of the indicated integers.  If an argument is not an integer,
          int() is used first to convert it to an integer and the absolute value is taken.
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
            if o == "-h":
                Usage()
        return args
if 1:   # Core functionality
    def PrintFactors(n):
        '''Print all the factors of n.  The first row will be the prime factors; the
        remaining rows will be the composite factors.
        
        The algorithm uses primes.AllFactors(), which by default uses /usr/bin/factor,
        so large numbers can be handled.  Then itertools.combinations produces all
        composite factors.
        '''
        assert isinstance(n, int)
        primes, composite = AllFactors(n, split=True)
        if not primes:
            t.print(f"{t.num}{n}{t.n}: {t.prime}prime" )
        else:
            m = 4   # Indent level
            # Print the number header
            t.print(f"{t.num}{n}{t.n}[{t.cnt}{m}{t.n}]:")
            # Print the prime factors
            print(f"{' '*m}{t.prime}Prime factors:")
            for i in Columnize([str(j) for j in primes], indent=" "*m):
                print(i)
            t.print(end="")
            # Print the composite factors
            print(f"{' '*m}{t.comp}Composite factors:")
            for i in Columnize([str(j) for j in composite], indent=" "*m):
                print(i)
            t.print(end="")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    for arg in args:
        try:
            PrintFactors(abs(int(arg)))
        except Exception:
            print(f"{arg!r} is not an integer")
