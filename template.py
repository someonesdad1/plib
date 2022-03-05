if __name__ == "__main__": 
    #∞test∞# ignore #∞test∞#
    '''Drop this template into a module to:
        * Create a normal script or print examples of use when run as a
          script
        * Run regression tests when --test option is given
    '''
    if 1:   # Imports
        # Standard library modules
        import getopt
        import os
        import pathlib
        import sys
        from pdb import set_trace as xx
    if 1:   # Custom modules
        from wrap import dedent
        from lwtest import run, raises, assert_equal, Assert
    if 1:   # Global variables
        d = {}      # Options dictionary
        P = pathlib.Path
        if 0:
            G = Global()
            from globalcontainer import Global, Variable, Constant
            def MakeGlobals():
                global G
                G.ro = Constant()
                # Root of filesystem for these files
                G.ro.root = P("/plib")
                # Directory of script relative to root
                p = P(sys.argv[0]).resolve()
                G.ro.name = p.relative_to(G.ro.root)
                G.ro.category = "[utility]"
            MakeGlobals()
    if 1:   # Module's base code
        def Error(msg, status=1):
            print(msg, file=sys.stderr)
            exit(status)
        def Usage(d, status=1):
            name = sys.argv[0]
            print(dedent(f'''
            Usage:  {name} [options] etc.
              Explanations...
             
            Options:
              --test      Run internal self tests
            '''))
            exit(status)
        def ParseCommandLine(d):
            d["--test"] = False         # Run self tests
            try:
                opts, args = getopt.getopt(sys.argv[1:], "h", 
                    "test".split())
            except getopt.GetoptError as e:
                print(str(e))
                exit(1)
            for o, a in opts:
                if o in ("-h", "--help"):
                    Usage(d, status=0)
                elif o == "--test":
                    d["--test"] = True
            #if not args:
            #    Usage(d)
            return args
    if 1:   # Test code 
        def Test_1():
            pass
    args = ParseCommandLine(d)
    if d["--test"]:
        exit(run(globals(), regexp=r"Test_", halt=1)[0])
    else:
        # Normal execution
        pass
