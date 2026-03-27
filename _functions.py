'''
Utility to find the top-level functions and classes in a file and list them, showing the
first line of their docstring.

Features
    - Color coding
        - Function
            - Active: skyl
            - Inactive:  sky2
        - Class
            - Active: grnl
            - Inactive:  sky2
        - After if __name__ == "__main__":  
            - Test_ functions: yell
            - Other:  none

Options
    - Show test functions
    - Identify functions that don't have a matching test

'''
import ast
import sys
from pathlib import Path
def GetFirstLine(node) -> str:
    '''Extracts the first line of a docstring from a Function or Class node.'''
    doc = ast.get_docstring(node)
    if not doc:
        return ""
    return doc.splitlines()[0].strip()
def ProcessFile(filepath: str) -> None:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return
    print(f"\n--- Module: {Path(filepath).name} ---")
    # We only want to look at nodes that are at the top level 
    # OR inside your 'if 1/0' blocks.
    ScanNodes(tree.body, active=True)
def ScanNodes(nodes, active: bool=True):
    '''Recursively scans nodes, diving into 'if' blocks but ignoring nested functions.'''
    for node in nodes:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            name = node.name
            doc = GetFirstLine(node)
            if isinstance(node, ast.FunctionDef):
                symbol = "!" if active else "!!"
            else:
                symbol = "~" if active else "~~"
            print(f"{name:<20} {symbol:<4} {doc}")
        elif isinstance(node, ast.If):
            # Check for your "if 1:" or "if 0:" pattern
            # In AST, '1' is a Constant. We check its value.
            if isinstance(node.test, ast.Constant):
                block_val = node.test.value
                if block_val in (0, 1):
                    # Recurse into the block
                    ScanNodes(node.body, active=(block_val == 1))
            else:
                # For standard 'if' statements, we treat the contents as active
                ScanNodes(node.body, active=active)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} file1.py ...")
    else:
        for arg in sys.argv[1:]:
            ProcessFile(arg)
