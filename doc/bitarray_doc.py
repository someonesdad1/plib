'''
Prints out a small tutorial on the behavior of bitarray objects.
'''
from color import t
from wrap import dedent
from bitarray import bitarray
if 1:   # Variables
    t.url = t.purl
    t.ex = t.sky
    t.res = t.brnl
if 1:   # Functions
    def Print(s, color=t.ex):
        if color is None:
            print(s)
        else:
            if color == t.res:
                print("  ", end="")
            t.print(f"{color}{s}")
if 1:   # Basic behavior
    if 0:
        print(dedent(f'''

            A bitarray is a mutable sequence of boolean values.  You can get the module with
            'pip install bitarray'; then you'd be wise to go to
            {t.url}https://github.com/ilanschnell/bitarray{t.n} to view some initial examples.  Much of
            what you know about lists will be relevant.  

            In particular, setting a regular pattern of 1 bits in the array can be done with
            slice notation; coupled with being able to set a range to a 0 or 1 lets you
            construct arrays efficiently.

            As an example, suppose we want a 20-bit bitarray where every even-index bit is 1 and
            the last 10 bits are zero:

        '''))
    n = 20
    b = bitarray(n)
    print()
    Print(f"b = bitarray(30)")
    Print(f">>> {str(b)}", t.brnl)
    Print(f"b[0:-1:2] = 1")
    b[0:-1:2] = 1
    Print(f">>> {str(b)}", t.brnl)
    Print(f"b[{n} - 10:-1] = 0")
    b[n - 10:-1] = 0
    Print(f">>> {str(b)}", t.brnl)

