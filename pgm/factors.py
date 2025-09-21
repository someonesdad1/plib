'''
Print factors of an integer
'''
_pgminfo = '''
<oo 
    Print factors of an integer
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
    if 1:   # Custom imports
        from primes import AllFactors
        from wrap import dedent
if 1:   # Utility
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] n1 [n2...]
          Print factors of the indicated integers.  If an argument is not an integer,
          int() is used first to convert it to an integer and the absolute value is
          taken.
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
        assert isinstance(n, int)
        f = AllFactors(n)
        m = len(f)
        s = ' '.join(str(i) for i in AllFactors(n))
        if not s:
            print(f"{n}: prime" )
        else:
            print(f"{n}[{m}]: {s}" )

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    for arg in args:
        try:
            PrintFactors(abs(int(arg)))
        except Exception:
            print(f"{arg!r} is not an integer")
