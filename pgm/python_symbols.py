'''
Print the set of characters that are allowed as python symbols.
'''

import uni
from columnize import Columnize

# Options dictionary in uni.py (keys needed by uni.GetCharacterSet)
d = {
    "-a": True,     # Use all characters
    "-e": True,     # Remove non-English characters
    "-v": False,    # Verbose
}

allowed = []
for cp in uni.GetCharacterSet(d):
    if cp in set((9, 12, 32, 35)):
        continue
    try:
        # Method:  see if the expression '_x = 0' where x is the Unicode
        # character is accepted by the parser
        s = f"_{chr(cp)} = 0"
        exec(s)
        allowed.append(chr(cp))
    except Exception:
        pass
for line in Columnize(allowed, horiz=True):
    print(line)

