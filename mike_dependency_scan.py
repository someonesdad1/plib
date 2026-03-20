'''
This is a suggested script from Mike (Google's Gemini), proffered during my massive
reorg, refactoring, typing in March 2026.
'''
import ast
from collections import Counter, defaultdict
from pathlib import Path

def analyze_ceo_view(lib_path_str: str, pgm_path_str: str):
    lib_root = Path(lib_path_str).resolve()
    pgm_root = Path(pgm_path_str).resolve()

    # 1. Catalog Library: Map {function_name: set(module_names)}
    lib_catalog = defaultdict(set)
    for path in lib_root.rglob("*.py"):
        if pgm_root in path.parents: continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            module_name = path.stem
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    lib_catalog[node.name].add(module_name)
        except Exception: continue

    # 2. Scan Programs with Namespace Awareness
    call_counts = Counter() # (module, function) -> count

    for path in pgm_root.rglob("*.py"):
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

                    # VALIDATION LOGIC
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
        except Exception: continue

    # 3. CEO REPORT
    print(f"\n{'Module':<15} | {'Function Name':<25} | {'Verified Calls':<10}")
    print("-" * 55)

    results = sorted(call_counts.items(), key=lambda x: x[1], reverse=True)
    for (mod, func), count in results[:50]:
        print(f"{mod + '.py':<15} | {func:<25} | {count:<10}")

if __name__ == "__main__":
    analyze_ceo_view("./", "./pgm")
