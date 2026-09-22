'''
This is a suggested script from Mike (Google's Gemini), proffered during my massive
reorg, refactoring, typing in March 2026.

Module          | Function Name             | Verified Calls
-------------------------------------------------------
trm.py          | print                     | 3007      
wrap.py         | dedent                    | 719       
debug.py        | print                     | 470       
trm.py          | list                      | 267       
f.py            | t                         | 211       
lwtest.py       | Assert                    | 192       
debug.py        | SetDebugger               | 172       
color.py        | Error                     | 169       
columnize.py    | Columnize                 | 163       
u.py            | Error                     | 150       
color.py        | Usage                     | 136       
debug.py        | C                         | 135       
f.py            | f                         | 126       
columnize.py    | Usage                     | 115       
color.py        | f                         | 108       
color.py        | ParseCommandLine          | 79        
columnize.py    | ParseCommandLine          | 73        
color.py        | P                         | 63        
u.py            | RoundOff                  | 58        
get.py          | GetNumber                 | 52        
trm.py          | out                       | 35        
lwtest.py       | assert_equal              | 33        
color.py        | Dbg                       | 30        
get.py          | GetLines                  | 29        
u.py            | ParseUnit                 | 28        
u.py            | dim                       | 24        
temperature.py  | ConvertTemperature        | 23        
si.py           | Error                     | 22        
sig.py          | P                         | 21        
color.py        | round                     | 20        
dpseq.py        | Dbg                       | 18        
lwtest.py       | run                       | 16        
debug.py        | f                         | 12        
lwtest.py       | raises                    | 12        
color.py        | GetColors                 | 11        
dpstr.py        | f                         | 11        
sig.py          | f                         | 10        
dputil.py       | Dbg                       | 10        
u.py            | to                        | 9         
f.py            | u                         | 9         
get.py          | GetWords                  | 8         
launch.py       | Error                     | 7         
wrap.py         | Dump                      | 7         
u.py            | fromto                    | 7         
dpstr.py        | Keep                      | 7         
launch.py       | Launch                    | 6         
sig.py          | GetSigFig                 | 6         
geom_prim.py    | sig                       | 6         
wire.py         | GetAmpacityData           | 6         
si.py           | NumberWithSISuffix        | 6         

Analysis:  This tool isn't discriminatory enough.  trm.py:print() is the most used and
this makes sense.  However, debug.py:print() is actually the print() method of class
AutoIndent and I simply don't use this tool.  Similarly, trm.py:list() is used a little,
but not as much as indicated.  Thus, this script needs some understanding and hacking to
turn it into a more meaningful tool.  For example, lwtest.Assert is heavily used in
testing code.

This shows that what's really needed is to find the symbols from the core modules, then
find the files that use these modules and see which have the symbols.  This deeply shows
the need of using the pattern of 'import x', then making all of x's references as x.y, 
allowing a text search tool to find them.

'''
import ast
from collections import Counter, defaultdict
from pathlib import Path

def analyze(lib_path_str: str, pgm_path_str: str):
    lib_root = Path(lib_path_str).resolve()
    pgm_root = Path(pgm_path_str).resolve()
    # 1. Catalog library: map {function_name: set(module_names)}
    lib_catalog = defaultdict(set)
    for path in lib_root.glob("*.py"):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            module_name = path.stem
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    #if module_name == "debug": #yy
                    #    if node.name == "print": #yy
                    #        print(node.lineno) #yy
                    lib_catalog[node.name].add(module_name)
        except Exception:
            continue
    # 2. Scan programs with namespace awareness
    call_counts = Counter() # dict:(module, function) -> count
    for path in pgm_root.glob("*.py"):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            imported_modules = set()
            func_to_mod = {} # Specific mappings from 'from mod import func'
            for node in ast.walk(tree):
                # Track 'import module'
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported_modules.add(alias.name)
                # Track 'from module import function'
                elif isinstance(node, ast.ImportFrom) and node.module:
                    for alias in node.names:
                        func_to_mod[alias.name] = node.module
                        imported_modules.add(node.module)
                # Track Calls
                elif isinstance(node, ast.Call):
                    func_name = ""
                    mod_hint = ""
                    if isinstance(node.func, ast.Name):
                        func_name = node.func.id
                        mod_hint = func_to_mod.get(func_name, "")
                    elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                        func_name = node.func.attr
                        mod_hint = node.func.value.id # e.g., 'trm' in 'trm.print()'
                    # Validation logic
                    if func_name in lib_catalog:
                        possible_mods = lib_catalog[func_name]
                        # If we have a direct hint (trm.print)
                        if mod_hint in possible_mods:
                            call_counts[(mod_hint, func_name)] += 1
                        # If it's a bare call (print), check if the module was imported
                        elif not mod_hint:
                            for mod in possible_mods:
                                if mod in imported_modules:
                                    call_counts[(mod, func_name)] += 1
                                    break # Assume first match for now
        except Exception:
            continue
    # 3. Report
    print(f"\n{'Module':<15} | {'Function Name':<25} | {'Verified Calls':<10}")
    print("-" * 55)
    results = sorted(call_counts.items(), key=lambda x: x[1], reverse=True)
    for (mod, func), count in results[:50]:
        print(f"{mod + '.py':<15} | {func:<25} | {count:<10}")

if __name__ == "__main__":
    analyze("/plib", "/plib/pgm")
