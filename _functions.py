import ast
import sys
from pathlib import Path
def get_summary(node) -> str:
    '''Extracts the first line of a docstring from a Function or Class node.'''
    doc = ast.get_docstring(node)
    if not doc:
        return ""
    return doc.splitlines()[0].strip()
def process_file(filepath: str):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return
    print(f"\n--- Module: {Path(filepath).name} ---")
    
    # We only want to look at nodes that are at the top level 
    # OR inside your 'if 1/0' blocks.
    scan_nodes(tree.body, active=True)
def scan_nodes(nodes, active=True):
    '''Recursively scans nodes, diving into 'if' blocks but ignoring nested functions.'''
    for node in nodes:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            name = node.name
            doc = get_summary(node)
            
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
                    scan_nodes(node.body, active=(block_val == 1))
            else:
                # For standard 'if' statements, we treat the contents as active
                scan_nodes(node.body, active=active)
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} file1.py ...")
    else:
        for arg in sys.argv[1:]:
            process_file(arg)
