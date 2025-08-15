_pgminfo = '''
<oo 
    Utilities that work with binary bits
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat utility oo>
<oo test run oo>
<oo todo

- Find the fixed integer implementation for hc and include it here
- Move bitfield.py's classes into this file
- bitarray ('pip install bitarray') is a similar tool and probably worth 
  looking at, as it's mature and implemented in C.  You can specify the endianness of
  the representation, use sequence semantics (e.g. slice assignment and deletion), + and
  * operators, 'in' operator, len(), and bitwise operations ~ & | ^ << >>.  It also has
  frozenbitarray objects that are hashable.
  https://github.com/ilanschnell/bitarray 

oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        pass
    if 1:   # Custom imports
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        pass
if 1:   # Functions
    def IntBitReverse(x):
        'Return the integer x with its bits reversed'
        # Easy implementation for routine integers, but could be inefficient for large
        # integers because it converts to a string representation.  This would be faster
        # and more efficient using C, assuming the whole integer's bits are in
        # contiguous memory.
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        sign = "-" if x < 0 else ""
        return int(f"{sign}0b" + ''.join(reversed(f"{abs(x):b}")), 2)
    def ByteReverseDict():
        '''Return a dictionary that reverses the bits in a byte.  Example:
            di = ByteReverseDict()
            di[0b11001010] returns
               0b01010011
        '''
        # https://stackoverflow.com/questions/2602823/
        # in-c-c-whats-the-simplest-way-to-reverse-the-order-of-bits-in-a-bytbytee
        def f(num):
            num = (num & 0xf0) >> 4 | (num & 0x0f) << 4
            num = (num & 0xcc) >> 2 | (num & 0x33) << 2
            num = (num & 0xaa) >> 1 | (num & 0x55) << 1
            return num
        if not hasattr(ByteReverseDict, "dict"):
            di = {}
            for i in range(256):
                di[i] = f(i)
            ByteReverseDict.dict = di
        return ByteReverseDict.dict

if __name__ == "__main__":
    from lwtest import run, Assert, raises
    def Test_ReverseBitsInByte():
        di = ByteReverseDict()
        for i in range(256):
            Assert(f"{i:08b}" == ''.join(reversed(f"{di[i]:08b}")))
    def Test_IntBitReverse():
        raises(TypeError, IntBitReverse, 1.2)
        Assert(IntBitReverse(0b0) == 0b0)
        Assert(IntBitReverse(0b1) == 0b1)
        Assert(IntBitReverse(-0b1) == -0b1)
        Assert(IntBitReverse(0b11000000) == 0b11)
        Assert(IntBitReverse(-0b11000000) == -0b11)
        # Test some bigger integers
        for i in range(100):
            x = int("0x1" + "0"*i, 16)
            Assert(IntBitReverse(x) == 1)
            Assert(IntBitReverse(-x) == -1)
    exit(run(globals(), halt=True)[0])
