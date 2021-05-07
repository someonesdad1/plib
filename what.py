if __name__ == "__main__": 
    if 1:   # Imports
        # Standard library modules
        from collections import deque, defaultdict
        import getopt
        import os
        import pathlib
        import re
        import subprocess
        import sys
        from pdb import set_trace as xx
    if 1:   # Custom modules
        from wrap import wrap, dedent, indent, Wrap
        from globalcontainer import Global, Variable, Constant
        try:
            from lwtest import run, raises, assert_equal
            _have_lwtest = True
        except ImportError:
            # Get it from
            # https://someonesdad1.github.io/hobbyutil/prog/lwtest.zip
            _have_lwtest = False
    if 1:   # Global variables
        G = Global()
        P = pathlib.Path
        def MakeGlobals():
            global G
            G.ro = Constant()
            # Root of filesystem for these files
            G.ro.root = P("/plib")
            # Directory of script relative to root
            p = P(sys.argv[0]).resolve()
            G.ro.name = p.relative_to(G.ro.root)
            G.ro.category = "[utility]"
            G.ro.python = sys.executable
        MakeGlobals()
    if 1:   # Utility
        def Error(msg, status=1):
            print(msg, file=sys.stderr)
            exit(status)
        def Usage(d, status=1):
            name = sys.argv[0]
            print(dedent(f'''
            Usage:  {name} [options] files...
              Show the --what string for each file.
             
            Options:
              -a        Show for all files
              --what    Brief description of module's purpose
            '''))
            exit(status)
        def ParseCommandLine(d):
            d["-a"] = False             # All files
            d["--what"] = False         # Print short description
            try:
                opts, args = getopt.getopt(sys.argv[1:], "ah", 
                    "what".split())
            except getopt.GetoptError as e:
                print(str(e))
                exit(1)
            for o, a in opts:
                if o[1] in list("a"):
                    d[o] = not d[o]
                elif o in ("-h", "--help"):
                    Usage(d, status=0)
                elif o == "--what":
                    d["--what"] = not d["--what"]
            if not args and not d["--what"] and not d["-a"]:
                Usage(d)
            return args
        def What():
            print(f"{G.ro.category} {G.ro.name}")
            w = Wrap(rmargin=2)
            w.i = " "*2
            print(w('''
                This script prints out the --what string for each file
                given on the command line to give you a short
                description of the file's purpose.
            '''))
    if 1:   # Core functionality
        def GetFiles(regexps: list) -> deque:
            all, keep = deque(G.ro.root.rglob("*.py")), deque()
            R = [re.compile(regexp, re.I) for regexp in regexps]
            if not d["-a"]:
                while all:
                    file = all.popleft()
                    for r in R:
                        if r.search(str(file)):
                            keep.append(file)
                            break
            else:
                keep = all
            # keep contains the files to list
            return keep
        def HasWhat(file):
            "Return True if file has string '--what'"
            return "--what" in file.read_text()
        def GetWhatString(file: pathlib.Path, container: deque):
            '''Given the pathlib.Path file and deque, capture the output
            of the --what option and put it in the deque.  This will let
            us sort the output by categories.
            '''
            args = [G.ro.python, str(file), "--what"]
            cp = subprocess.run(args, capture_output=True, encoding="UTF-8")
            if not cp.returncode:
                output = cp.stdout
                s = output.replace("\n", "")
                container.append(s)
        def LoadDict(container: deque, dict: defaultdict):
            while container:
                fields = container.pop().split()
                key = fields[0]
                filename = fields[1]
                dict[key].append([filename, ' '.join(fields[2:])])
        def Report(dict):
            items = list(sorted(dict.items()))
            w = Wrap(rmargin=3)
            w.i = " "*2
            for key, value in items:
                for filename, s in value:
                    print(key, filename)
                    s = w(s)
                    print(w(s))

    # ----------------------------------------------------------------------
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["--what"]:
        What()
    else:
        # Normal execution
        files = GetFiles(args)
        container = deque()
        for file in sorted(files):
            if HasWhat(file):
                GetWhatString(file, container)
        dict = defaultdict(list)
        LoadDict(container, dict)
        Report(dict)
