'''
Given a python file, print out a tree structure of its functions and classes.

Analyzing all of /plib/*.py gave the following resulting counts of the number of lines
in functions
    1: 30      20: 40     39: 18     58: 4      77: 4      99: 2      124: 2     161: 1     294: 1
    2: 552     21: 58     40: 15     59: 8      78: 3      101: 1     125: 2     169: 2     298: 2
    3: 383     22: 43     41: 22     60: 7      79: 3      102: 2     126: 1     170: 1     310: 2
    4: 234     23: 49     42: 10     61: 10     80: 4      103: 3     129: 4     175: 2     315: 1
    5: 195     24: 38     43: 12     62: 4      81: 2      105: 2     130: 3     180: 1     337: 1
    6: 181     25: 39     44: 10     63: 8      82: 5      106: 3     133: 1     202: 1     345: 1
    7: 147     26: 23     45: 19     64: 7      83: 1      107: 2     135: 1     203: 1     348: 1
    8: 136     27: 32     46: 15     65: 6      84: 4      109: 5     136: 1     204: 2     356: 1
    9: 119     28: 32     47: 15     66: 7      86: 3      110: 2     137: 1     205: 1     364: 1
    10: 119    29: 25     48: 12     67: 6      88: 2      111: 2     139: 3     216: 1     381: 1
    11: 100    30: 30     49: 12     68: 3      89: 3      112: 3     140: 2     229: 1     406: 1
    12: 94     31: 27     50: 12     69: 3      90: 3      114: 2     145: 1     241: 1     454: 1
    13: 72     32: 12     51: 8      70: 4      91: 3      115: 4     146: 1     242: 1     555: 1
    14: 71     33: 19     52: 5      71: 2      92: 5      116: 1     148: 2     266: 1     690: 1
    15: 78     34: 19     53: 5      72: 1      93: 4      117: 1     151: 1     267: 1     698: 1
    16: 77     35: 19     54: 12     73: 3      95: 4      119: 1     155: 1     269: 1     929: 1
    17: 61     36: 19     55: 12     74: 5      96: 1      120: 2     157: 2     272: 1     986: 1
    18: 61     37: 20     56: 9      75: 2      97: 1      121: 2     158: 1     273: 1     1616: 1
    19: 48     38: 15     57: 5      76: 9      98: 2      122: 3     159: 1     282: 1     2036: 1

Inspection of this table shows the following could be a decent heuristic summary
histogram:

Num Lines       Symbol      Color
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
import trm
import wl2rgb
t = trm.Trm()
# Decorating colors
t.klass = t.grnl
t.test  = t.wht2
t.normal = t.wht
t.lines = t.pnkl
t.file  = t.orn
def GetNumLinesColor(numlines):
    if numlines <= 10:
        return t(450)
    elif numlines <= 20:
        return t(470)
    elif numlines <= 50:
        return t(490)
    elif numlines <= 100:
        return t(550)
    elif numlines <= 200:
        return t(580)
    elif numlines <= 100:
        return t(620)
    else:
        return t(660)
def GetNodeMass(node):
    'Calculate lines of code in an AST node'
    if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
        return node.end_lineno-node.lineno+1
    return 0
def PrintTree(nodes, total_lines, prefix="", use_percent=True):
    'Recursively prints the tree structure'
    nodes.sort(key=lambda x: x[3])
    for i, (name, mass, children, lineno) in enumerate(nodes):
        is_last = (i == len(nodes)-1)
        if use_percent:
            percent = int((mass/total_lines)*100)
            display = f"{percent:>3}%" if percent > 0 else "    "
        else:
            display = f"{GetNumLinesColor(mass)}{mass:>4}{t.n}"
        #connector = "└── " if is_last else "├── "
        connector = "    "
        # Decorate a class name with color
        if name.startswith("Class"):
            t.print(f" {display}  {prefix}{connector}{t.klass}{name}{t.n} {lineno}")
        elif name.startswith("Test_"):
            t.print(f" {display}  {prefix}{connector}{t.test}{name}{t.n} {lineno}")
        else:
            t.print(f" {display}  {prefix}{connector}{t.normal}{name}{t.n} {lineno}")
        #new_prefix = prefix+("    " if is_last else "│   ")
        new_prefix = prefix+("    " if is_last else "    ")
        PrintTree(children, total_lines, new_prefix, use_percent)
def AnalyzeFile(filepath, use_percent=True):
    'Main entry point for file analysis'
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        sourcelines = f.readlines()
    source = "".join(sourcelines)
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
    t.print(f"{t.lines}{total_lines:>4} lines{t.n} {t.file}{os.path.basename(filepath)}")
    if not structure:
        print("    (No definitions found.)")
    else:
        PrintTree(structure, total_lines, use_percent=use_percent)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} file1 [file2...]")
    else:
        show_pct = "-p" in sys.argv
        for i, filename in enumerate([arg for arg in sys.argv[1:] if arg != "-p"]):
            if i:
                print(f"{'-'*88}")
            AnalyzeFile(filename, use_percent=show_pct)
