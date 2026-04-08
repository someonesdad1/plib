'''

Given a python file, print out a tree structure of its functions and classes.

    Based on a histogram of the number of lines in the functions in /plib and /plib/pgm,
    here are the choices I hade for colorizing the number of lines in a function:

    Num Lines       Symbol      Color, nm
    < 10 lines                  450
    10-20           *           470
    20-50           **          490
    50-100          ***         550
    100-200         ****        580
    200-500         *****       620
    > 500           ******      660

        
'''
if 1:  # Header
    if 1:   # Standard imports
        import ast
        import collections
        import getopt
        import os
        import pathlib
        import re
        import sys
    if 1:   # Custom imports
        import dptypes
        import trm
        import wl2rgb
        import wrap
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Core file gist information
        __gist__      = "Print tree structure of a module's functions & classes"
        __copyright__ = "Copyright © 2026 Don Peterson"
        __license__   = "MIT License (see /plib/_lic.mit)"
        __test__      = "notest"
        __category__  = "utility"
        __todo__      = '''
            
            - 
        
        '''
    if 1:   # Import symbols
        pass
    if 1:   # Global variables
        g = dptypes.Constant()
        g.dbg = False
        g.klass = "+"
        g.testing = "·"
        u = trm.TrmDPDP()
if 1:   # Utility
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )
    def GetColors():
        u.dbg = u.lil
        u.err = u.redl
        # Decorating colors
        u.klass = u.grnl
        u.test  = u.wht2
        u.normal = u.wht
        u.lines = u.pnkl
        u.file  = u.orn
        # Colors for number of lines
        u.w450 = u(450)
        u.w470 = u(470)
        u.w490 = u(490)
        u.w550 = u(550)
        u.w580 = u(580)
        u.w620 = u(620)
        u.w660 = u(660)
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
        print(wrap.dedent(f'''
        Usage: {sys.argv[0]} file1 [file2...]
          Print the functions and classes in the files.  Show the number of lines in the
          function/class and the line number where the item is after the name.
        Options
          -a    Colorize always, even if stdout is not a tty
          -c    Colorize output
          -p    Print % of total number of lines rather than number of lines
          -r    Print the function calling tree, not just the main nodes
        '''))
        exit(status)
    def ParseCommandLine():
        d["-a"] = False  # Colorize always
        d["-c"] = False  # Colorize
        d["-p"] = False  # Print % of total number of lines
        d["-r"] = False  # Use recursion to print whole tree
        try:
            opts, args = getopt.getopt(sys.argv[1:], "achpr")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("acpr"):
                d[o] = not d[o]
            elif o == "-h":
                Usage(status=0)
        GetColors()
        if d["-a"]:
            d["-c"] = True
            u.always = True
        u.on = True if d["-c"] else False
        g.W, g.L = GetScreen()
        if not args:
            Usage()
        return args
if 1:   # Core functionality
    def GetNumLinesColor(numlines):
        if numlines <= 10:
            return u.w450
        elif numlines <= 20:
            return u.w470
        elif numlines <= 50:
            return u.w490
        elif numlines <= 100:
            return u.w550
        elif numlines <= 200:
            return u.w580
        elif numlines <= 100:
            return u.w620
        else:
            return u.w660
    def GetNodeMass(node):
        'Calculate lines of code in an AST node'
        if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
            return node.end_lineno-node.lineno+1
        return 0
    def PrintTree(nodes, total_lines, prefix="", use_percent=False):
        'Recursively prints the tree structure'
        nodes.sort(key=lambda x: x[3])
        for i, (name, mass, children, lineno) in enumerate(nodes):
            is_last = (i == len(nodes)-1)
            if use_percent:
                percent = int((mass/total_lines)*100)
                display = f"{percent:>3}%" if percent > 0 else "    "
            else:
                display = f"{GetNumLinesColor(mass)}{mass:>4}{u.n}"
            #connector = "└── " if is_last else "├── "
            connector = "    "
            # Decorate a class name with color
            if name.startswith(f"{g.klass} class"):
                print(f" {display}  {prefix}{connector}{u.klass}{name}{u.n} {lineno}")
            elif name.startswith("  Test_"):
                name = name.replace(" ", g.testing, 1)
                print(f" {display}  {prefix}{connector}{u.test}{name}{u.n} {lineno}")
            else:
                print(f" {display}  {prefix}{connector}{name} {lineno}")
            #new_prefix = prefix+("    " if is_last else "│   ")
            new_prefix = prefix+("    " if is_last else "    ")
            if d["-r"]:
                PrintTree(children, total_lines, new_prefix, use_percent)
    def AnalyzeFile(filepath, use_percent=False):
        'Main entry point for file analysis'
        with filepath.open("r", encoding="utf-8") as f:
            sourcelines = f.readlines()
        source = ''.join(sourcelines)
        parsed_tree = ast.parse(source)
        total_lines = len(sourcelines)
        def FindDefinitions(parent):
            'Recursively dive through all blocks to find defs and classes'
            found = []
            for node in ast.iter_child_nodes(parent):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                    name = f"  {node.name}()" if not isinstance(node, ast.ClassDef) else f"{g.klass} class {node.name}"
                    mass = GetNodeMass(node)
                    sub_children = FindDefinitions(node)
                    found.append((name, mass, sub_children, node.lineno))
                elif isinstance(node, (ast.If, ast.Try, ast.With, ast.For, ast.While)):
                    found.extend(FindDefinitions(node))
            return found
        structure = FindDefinitions(parsed_tree)
        u.print(f"{u.lines}{total_lines:>4} lines{u.n} {u.file}{os.path.basename(filepath)}")
        if not structure:
            print("    (No definitions found.)")
        else:
            PrintTree(structure, total_lines, use_percent=use_percent)

if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine()
    for i, filename in enumerate(files):
        if i:
            print(f"{'-'*88}")
        filepath = pathlib.Path(filename)
        if not filepath.exists() and not filepath.suffix:
            # See if adding '.py' as extension helps
            filepath = pathlib.Path(filename + ".py")
            if not filepath.exists():
                raise FileNotFoundError(f"{filename!r} doesn't exist")
        AnalyzeFile(filepath, use_percent=d["-p"])
