'''
Short function to get a float to an indicated number of significant
figures.
'''

from decimal import Decimal, localcontext

from pdb import set_trace as xx
if 0:
    import debug
    debug.SetDebugger()

def fsig(x, digits=3, low=1e-6, high=1e6):
    '''Return a string representing the number x to the indicated number
    of signifcant digits.  If x is < low or > high, convert to
    scientific notation.
    '''
    if not (int(digits) > 0):
        raise ValueError("digits must be > 0")
    y = Decimal(x)
    with localcontext() as ctx:
        ctx.prec = digits
        y = +y
    if isinstance(x, int):
        return int(y)
    # Convert back to float
    if not (low <= y <= high):
        return f"{float(y):.{digits - 1}e}"
    # Remove trailing zeros after decimal point
    s = f"{y:f}"
    while "." in s and s[-1] == "0" and s[-1] != ".":
        s = s[:-1]
    return s

# Demo
if __name__ == "__main__": 
    from math import pi
    n = 8
    def P(x, digits):
        print("   ", fsig(pi*10**e, digits=digits))
    print("3 digits:")
    for e in range(-n, n + 1):
        P(pi*10**e, 3)
    print("\n5 digits:")
    for e in range(-n, n + 1):
        P(pi*10**e, 5)
