'''
checkgist.py: Validate and print metadata dunders in Python files.
'''
if 1:  # Header
    if 1:   # Standard imports
        import ast
        import sys
        import argparse
        from pathlib import Path
        from typing import Dict, Any, List, Set, Union
    if 1:   # Custom imports
        import columnize
        import dpstr
        import dptypes
        import f
        import trm
        import wrap
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        t = trm.Trm()
        g = dptypes.Constant()
        g.dbg = False
        with g:
            g.required_dunders = {"__gist__", "__copyright__", "__license__", 
                "__test__", "__category__", "__todo__"}
            g.allowed_test = {"notest", "--test", "run"}
            g.allowed_category = {"util", "utility", "math", "physics", "ui", "internal", ""}
            g.ignored_files: Set[str] = {
                "__init__.py", "rgbdata.py"
            }
if 1:   # Core class
    class GistAnalyzer:
        def __init__(self, print_mode: bool = False):
            self.print_mode = print_mode
            self.results = {
                "Proper": [],
                "Improper": [],
                "Ignored": []
            }
        def analyze_file(self, filepath: Path) -> None:
            # 1. Basic filtering
            if filepath.name in g.ignored_files or filepath.suffix != ".py":
                self.results["Ignored"].append(filepath)
                return
            # 2. AST Parsing
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
            except Exception as e:
                self.results["Improper"].append((filepath, f"Parse Error: {e}"))
                return
            found_data: Dict[str, Any] = {}
            def walk_and_find(nodes: List[ast.stmt]) -> None:
                for node in nodes:
                    # Catch assignments: __gist__ = "..."
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and target.id in g.required_dunders:
                                try:
                                    found_data[target.id] = ast.literal_eval(node.value)
                                except (ValueError, TypeError, SyntaxError):
                                    found_data[target.id] = "<Non-Literal Value>"
                    # Catch truthy IF blocks: if 1: or if True:
                    elif isinstance(node, ast.If):
                        is_truthy = False
                        # Modern AST (Python 3.8+)
                        if isinstance(node.test, ast.Constant):
                            if bool(node.test.value):
                                is_truthy = True
                        # Legacy / Manual check for Name(True) or Num(1)
                        elif isinstance(node.test, ast.Name) and node.test.id == "True":
                            is_truthy = True
                        elif isinstance(node.test, ast.Num) and node.test.n == 1:
                            is_truthy = True
                        if is_truthy:
                            walk_and_find(node.body)
            # 3. Execute recursive search
            walk_and_find(tree.body)
            # 4. Validation Logic
            missing = g.required_dunders - set(found_data.keys())
            errors = []
            if missing:
                errors.append(f"Missing: {', '.join(sorted(missing))}")
            else:
                test_val = found_data.get("__test__")
                cat_val = found_data.get("__category__")
                if test_val not in g.allowed_test:
                    errors.append(f"Invalid __test__: {test_val!r}")
                if cat_val not in g.allowed_category:
                    errors.append(f"Invalid __category__: {cat_val!r}")
            # 5. Record findings
            if errors:
                self.results["Improper"].append((filepath, " | ".join(errors)))
            else:
                self.results["Proper"].append(filepath)
            # 6. Optional detail printing
            if self.print_mode:
                self.print_gist(filepath, found_data, errors)
        def print_gist(self, path: Path, data: Dict[str, Any], errors: List[str]) -> None:
            status = "[IMPROPER]" if errors else "[PROPER]"
            print(f"\n--- {path} {status} ---")
            for key in sorted(g.required_dunders):
                val = data.get(key, "MISSING")
                # Truncate long strings for cleaner -p output
                display_val = str(val).replace('\n', ' ')
                if len(display_val) > 60:
                    display_val = display_val[:57] + "..."
                print(f"  {key:15}: {display_val}")
            if errors:
                print(f"  ERRORS         : {errors}")
        def report(self) -> None:
            if self.print_mode:
                # If printing individual gists, just show a summary count at the end
                print("\n" + "="*30)
                print(f"Proper: {len(self.results['Proper'])} | Improper: {len(self.results['Improper'])} | Ignored: {len(self.results['Ignored'])}")
                return
            print("Gist Check Report")
            print(f"Proper gist   : {len(self.results['Proper'])}")
            print(f"Ignored       : {len(self.results['Ignored'])}")
            print(f"Improper gist : {len(self.results['Improper'])}")
            if self.results["Improper"]:
                print(f"--- Improper Gist Details ---")
                for path, err in self.results["Improper"]:
                    print(f"{path}: {err}")
    def Analyze():
        parser = argparse.ArgumentParser(description="Check Python file gists.")
        parser.add_argument("paths", nargs="*", help="Files or directories to check")
        parser.add_argument("-p", "--print", action="store_true", help="Print gist info for each file")
        parser.add_argument("-r", "--recursive", action="store_true", help="Operate recursively on directories")
        args = parser.parse_args()
        analyzer = GistAnalyzer(print_mode=args.print)
        # Default to current directory if no paths provided
        search_paths = args.paths if args.paths else ["."]
        for p in search_paths:
            path_obj = Path(p)
            if path_obj.is_file():
                analyzer.analyze_file(path_obj)
            elif path_obj.is_dir():
                pattern = "**/*.py" if args.recursive else "*.py"
                for f in path_obj.glob(pattern):
                    analyzer.analyze_file(f)
            else:
                print(f"Warning: {p} is not a valid file or directory.", file=sys.stderr)
        analyzer.report()

if __name__ == "__main__":
    Analyze()
