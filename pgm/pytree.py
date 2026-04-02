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
import ast
import sys
import os
import pathlib
import trm
import wl2rgb
u = trm.Trm()
# Decorating colors
u.klass = u.grnl
u.test  = u.wht2
u.normal = u.n
u.lines = u.pnkl
u.file  = u.orn

def GetNumLinesColor(numlines):
    if numlines <= 10:
        return u(450)
    elif numlines <= 20:
        return u(470)
    elif numlines <= 50:
        return u(490)
    elif numlines <= 100:
        return u(550)
    elif numlines <= 200:
        return u(580)
    elif numlines <= 100:
        return u(620)
    else:
        return u(660)
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
        if name.startswith("Class"):
            print(f" {display}  {prefix}{connector}{u.klass}{name}{u.n} {lineno}")
        elif name.startswith("Test_"):
            print(f" {display}  {prefix}{connector}{u.test}{name}{u.n} {lineno}")
        else:
            print(f" {display}  {prefix}{connector}{name} {lineno}")
        #new_prefix = prefix+("    " if is_last else "│   ")
        new_prefix = prefix+("    " if is_last else "    ")
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
                name = f"{node.name}()" if not isinstance(node, ast.ClassDef) else f"Class {node.name}"
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
    from wrap import dedent
    if len(sys.argv) < 2:
        print(dedent(f'''
        Usage: {sys.argv[0]} file1 [file2...]
          This utility reads the indicated python files and prints out a listing of the
          classes and functions found in the file.  An indented name under another name
          means that class or function is inside the first.

          The number of lines in the class or routine are printed in color to the left
          of the name.  Colors at the blue end of the spectrum indicate a small number
          of lines, which orange and red indicate large numbers of lines.  After each
          token name the line number where it appears is given.

          Classes are printed in light green and Test_* functions are dimmed somewhat.
        Options
          -p    Print % of total number of lines rather than number of lines
        '''))
    else:
        show_pct = "-p" in sys.argv
        for i, filename in enumerate([arg for arg in sys.argv[1:] if arg != "-p"]):
            if i:
                print(f"{'-'*88}")
            filepath = pathlib.Path(filename)
            if not filepath.exists() and not filepath.suffix:
                # See if adding '.py' as extension helps
                filepath = pathlib.Path(filename + ".py")
                if not filepath.exists():
                    raise FileNotFoundError(f"{filename!r} doesn't exist")
            AnalyzeFile(filepath, use_percent=show_pct)
