'''
Tool from https://gemini.google.com/app/33bd3d7229385f0e.  
13 Mar 2026 

To identify your "leaf" nodes, we need to treat your directory of modules as a Directed
Acyclic Graph (DAG). A "leaf" node in this context is a module that nothing else depends
on (at the top of the chain) or, more helpfully for your typing strategy, a module that
depends on nothing else (the foundation).

For your purposes, we want the foundation modules: those that import only standard
libraries or external packages (like mpmath) but none of your other 140 modules.

The "Dependency Mapper" Script

This script uses Python's built-in ast (Abstract Syntax Tree) module. It’s safer than
grep because it actually understands Python's import logic.

'''
if 1:   # Header
    if 1:   # Standard imports
        import ast
        import os
        from pathlib import Path
        import sys
    if 1:   # Custom imports
        import columnize
        import trm
    if 1:   # Import symbols
        Columnize = columnize.Columnize
        t = trm.Trm()
if 1:   # Core functionality
    def GetInternalImports(file_path, all_module_names):
        'Parses a file and returns a set of internal modules it imports'
        internal_deps = set()
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
            for node in ast.walk(tree):
                # Handle 'import module'
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        name = alias.name.split('.')[0]
                        if name in all_module_names:
                            internal_deps.add(name)
                # Handle 'from module import ...'
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        name = node.module.split('.')[0]
                        if name in all_module_names:
                            internal_deps.add(name)
        except Exception as e:
            print(f"Could not parse {file_path}: {e}")
        return internal_deps
    def Original(directory):
        '''This is the original main module.  It will look for modules in directory and
        print out the results.
        '''
        path = Path(directory)
        # 1. Map out all your python files
        py_files = list(path.glob("*.py"))
        all_module_names = {f.stem for f in py_files}
        dep_graph = {}
        # 2. Build the dependency map
        for py_file in py_files:
            module_name = py_file.stem
            deps = GetInternalImports(py_file, all_module_names)
            # Remove self-imports if they exist
            deps.discard(module_name)
            dep_graph[module_name] = deps
        # 3. Identify the "Foundations" (Nodes with 0 internal dependencies)
        foundations = [m for m, d in dep_graph.items() if len(d) == 0]
        # 4. Identify "High-Impact" modules (Heavily imported by others)
        usage_counts = {m: 0 for m in all_module_names}
        for deps in dep_graph.values():
            for d in deps:
                usage_counts[d] += 1
        print("--- 🏗️ FOUNDATION MODULES (Start Typing Here) ---")
        print("These depend on no other internal modules:")
        for m in sorted(foundations):
            print(f"  [ ] {m}.py")
        print("\n--- 🚀 HIGH-IMPACT MODULES ---")
        print("These are the most 'popular' in your codebase (number of dependents):")
        sorted_impact = sorted(usage_counts.items(), key=lambda x: x[1], reverse=True)
        for m, count in sorted_impact[:20]:
            if count > 0:
                print(f"  {m}.py is used by {count} other modules")
    def AnalyzePlib():
        '''This function prints a report that analyzes all the files in /plib,
        and /plib/data, then prints out the results.
        '''
        t.print(f"{t.yel}Analysis of the most important /plib modules\n")
        # 1. Get list of all python files
        py_files, all_module_names = [], set()
        for dir in "/plib /plib/data".split():
            path = Path(dir)
            py_files.extend(list(path.glob("*.py")))
            all_module_names.update({f.stem for f in py_files})
        # 2. Build the dependency map
        dep_graph = {}
        for py_file in py_files:
            module_name = py_file.stem
            deps = GetInternalImports(py_file, all_module_names)
            # Remove self-imports if they exist
            deps.discard(module_name)
            dep_graph[module_name] = deps
        # 3. Identify the "Foundations" (Nodes with 0 internal dependencies)
        foundations = [m for m, d in dep_graph.items() if len(d) == 0]
        t.print(f"{t.sky}Files that depend on no other internal modules:")
        for i in Columnize(sorted(foundations), indent=" "*2):
            print(i)
        # 4. Identify "High-Impact" modules (Heavily imported by others)
        usage_counts = {m: 0 for m in all_module_names}
        for deps in dep_graph.values():
            for d in deps:
                usage_counts[d] += 1
        t.print(f"{t.orn}Most used modules:")
        sorted_impact = sorted(usage_counts.items(), key=lambda x: x[1], reverse=True)
        for m, count in sorted_impact[:20]:
            if count > 0:
                print(f"{count:6d} {m}.py")

if __name__ == "__main__":  
    AnalyzePlib()
