if __name__ == "__main__": 
    '''
    Drop this template into a module to:
        * Create a normal script.
        * Print examples of use when run as a script (use --example).
        * Run selftests when --test is given.
        * Run external test file when --Test is given.
    '''
    # Standard library modules
    import getopt
    import os
    import pathlib
    import sys
    import textwrap 
    from pdb import set_trace as xx
    # Custom modules
    try:
        from lwtest import run, raises, assert_equal
        _have_lwtest = True
    except ImportError:
        # Get it from
        # https://someonesdad1.github.io/hobbyutil/prog/lwtest.zip
        _have_lwtest = False
    if 1:   # Script base code
        def Error(msg, status=1):
            print(msg, file=sys.stderr)
            exit(status)
        def Usage(d, status=1):
            name = sys.argv[0]
            s = textwrap.dedent(f'''
        Usage:  {name} [options] etc.
        Explanations...
        
        Options:
            -h          Print a manpage
            --self      Run self tests
            --test      Run regression test file named test/X_test.py 
                        where X is the name of this script
            --Test f    Run regression test file f
            '''[1:].rstrip())
            print(s)
            exit(status)
        def ParseCommandLine(d):
            d["-a"] = False             # Not used yet
            d["--example"] = False      # Run examples
            d["--self"] = False         # Run self tests
            d["--test"] = False         # Run tests in test/
            d["--Test"] = None          # Run tests in another file
            d["special"] = False        # If True, one of --example,
                                        # --self, or --test was given
            try:
                opts, args = getopt.getopt(sys.argv[1:], "ah", 
                    "example help self test Test=".split())
            except getopt.GetoptError as e:
                print(str(e))
                exit(1)
            for o, a in opts:
                if o[1] in list("a"):
                    d[o] = not d[o]
                elif o in ("-h", "--help"):
                    Usage(d, status=0)
                elif o == "--example":
                    d["--example"] = True
                elif o == "--test":
                    d["--test"] = True
                elif o == "--Test":
                    d["--Test"] = a
                elif o == "--self":
                    d["--self"] = True
            d["special"] = (d["--example"] or d["--self"] or d["--test"]
                            or d["--Test"])
            if not args and not d["special"]:
                Usage(d)
            return args
    if 1:   # Test code 
        def Assert(cond):
            '''Same as assert, but you'll be dropped into the debugger on an
            exception if you include a command line argument.
            '''
            if not cond:
                if args:
                    print("Type 'up' to go to line that failed")
                    xx()
                else:
                    raise AssertionError
        def Test_1():
            pass
    if 1:   # Example code 
        def Example_1():
            print("example 1")
            pass
    # ----------------------------------------------------------------------
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["special"]:
        if d["--self"]:
            if not _have_lwtest:
                raise RuntimeError("lwtest.py missing")
            r = r"^Test_"
            failed, messages = run(globals(), regexp=r)
        elif d["--example"]:
            if not _have_lwtest:
                raise RuntimeError("lwtest.py missing")
            r = r"^Example_"
            failed, messages = run(globals(), regexp=r, quiet=True)
        elif d["--Test"]:
            # Execute external test file
            e = sys.executable
            st = os.system(f"{e} {d['--Test']}")
            exit(st)
        elif d["--test"]:
            # Execute test file in test/
            e = sys.executable
            p = pathlib.Path(sys.argv[0])
            name = p.stem
            testfile = f"test/{name}_test.py"
            st = os.system(f"{e} {testfile}")
            exit(st)
    else:
        # Normal execution
        pass
