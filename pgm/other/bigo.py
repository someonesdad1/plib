'''
Compare growth of common big-O functions
    
    lg(n)
    sqrt(n)
    n
    n*lg(n)
    n**2
    2**n
    n!
'''

from mpmath import mpf, sqrt, factorial, log, nstr
if 1:
    import debug
    debug.SetDebugger()

def F(x):
    'Short sci notation for mpf'
    s = str(mpf(x))
    if "e" in s:
        m, e = s.split("e")
    else:
        m, e = f"{float(x):e}".split("e")
    e = int(e)
    return m[0] + "e" + str(e)
def lg(x):
    return log(x)/log(2)

w = 10
s = f">{w}s"
for t in "n lg sqrt n n*lg(n) n*n 2**n n!".split():
    print(f"{t:>{w}s}", end=" ")
print()
for m in range(1, 6):
    for n in (1, 2, 5):
        x = n*10**m
        print(f"{x:{w}d} {F(lg(x)):{s}} {F(sqrt(x)):{s}} {F(x):{s}} {F(x*lg(x)):{s}} "
            f"{F(x*x):{s}} {F(2**x):{s}} {F(factorial(x)):{s}}")
