_pgminfo = '''
<oo 
    Utilities that work with binary bits
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat utility oo>
<oo test -t oo>
<oo todo

- Fixed-size integers for python
- See https://graphics.stanford.edu/%7Eseander/bithacks.html for ideas

oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        import logging
    if 1:   # Custom imports
        have_bitarray = False
        try:
            from bitarray import bitarray
            from bitarray.util import int2ba, ba2int
            have_bitarray = True
        except ImportError:
            pass
        have_basencode = False
        try:
            import basencode
            have_basencode = True
        except ImportError:
            pass
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        ii = isinstance
if 1:   # Functions
    def IntBitReverse(x):
        'Return the integer x with its bits reversed'
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        sign = -1 if x < 0 else 1
        if have_bitarray:
            a = int2ba(abs(x))
            a.reverse()
            return sign*ba2int(a)
        else:
            return sign*int(f"0b" + ''.join(reversed(f"{abs(x):b}")), 2)
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
    def IntToBase(n, b, msd_first=True):
        '''Convert positive integer n to any integer base b > 1.  Return a tuple of
        integers with the most significant digit at the 0th position in the list if
        msd_first is True; otherwise, the most significant digit is last in the list.
        
        Examples:
            IntToBase(10017, 82) --> (1, 40, 13)
                Check:  13*82**0 + 40*82**1 + 1*82**2 = 10017
            IntToBase(10017, 82, msd_first=False) --> (13, 40, 1)
        
        For string interpolation of these returned tuples of integers, the basencode
        module can be used (https://github.com/prawnydagrate/basencode).
        
        Adapted from highest score answer to 
        https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-to-a-string-in-any-base/74324587#74324587
        '''
        if not isinstance(n, int) or not isinstance(b, int):
            raise TypeError("n and b must be integers")
        if b < 2:
            raise ValueError("b must be > 1")
        if n == 0:
            return (0,)
        digits = []
        while n:
            digits.append(n % b)
            n //= b
        return tuple(digits[::-1]) if msd_first else tuple(digits)
    def rBitarray(ba, base=2):
        '''Display a bitarray with the least significant bit on the right in base.
        Example:
            ba = int2ba(70)
            for b in (2, 5, 7, 8, 11, 16, 49):
                print(b, rBitarray(ba, b))
          produces
            2 rBitarray«2»('1000110')
            5 rBitarray«5»('240')
            7 rBitarray«7»('130')
            8 rBitarray«8»('106')
            11 rBitarray«11»('64')
            16 rBitarray«16»('46')
            49 rBitarray«17»('1l')
        '''
        i = basencode.Number(ba2int(ba))
        s = i.repr_in_base(base)
        return f"rBitarray«{base}»('{i.repr_in_base(base)}')"
if 0:   # Fixed-size integers
    class Int:
        '''This class implements immutable fixed-size integers.  You supply the number
        of bits to the constructor and this defines the maximum size of the integer.
        The integer can be signed or unsigned.
        
        Properties
            - nbits         Number of bits making up the integer
            - unsigned      Unsigned if True 
            - base          2-36 for string interpolation
        
        Int's use case is to simulate n-bit integer functionality.  If a binary
        operation is performed with two Int objects, an Int instance will be returned
        with the number of bits of the largest number of bits of the two operands.
        
        '''
        def __init__(self, value, numbits=32, unsigned=False):
            if not ii(numbits, int):
                raise TypeError("numbits must be an integer")
            if numbits < 1:
                raise ValueError("numbits must be > 0")
            try:
                val = int(value)
            except Exception:
                raise TypeError("value must be an object that can be converted to an integer")
            if 1:   # Set attributes
                self._nbits = n = numbits
                self._unsigned = bool(unsigned)
                self._base = 2**n if self._unsigned else 2**(n - 1)
                self._sign = 1
                if not self._unsigned and val < 0:
                    self._sign = -1
                val = abs(val)
            if 1:   # Truncate val if necessary
                if not (-self._base <= val <= self._base - 1):
                    logging.warn(f"Int:  truncated because value outside {numbits} bits range")
                    val &= self._base
            if 1:   # Set the Int's value
                self._value = val
                
        if 1:   # Methods
            def __abs__(self):
                pass
            def __add__(self, value):
                pass
            def __and__(self, value):
                pass
            def __bool__(self):
                pass
            def __ceil__(self):
                pass
            def __del__(self):
                pass
            def __dir__(self):
                pass
            def __divmod__(self, value):
                pass
            def __eq__(self, value):
                pass
            def __float__(self):
                pass
            def __floor__(self):
                pass
            def __floordiv__(self, value):
                pass
            def __ge__(self, value):
                pass
            def __gt__(self, value):
                pass
            def __hash__(self):
                pass
            def __index__(self):
                pass
            def __int__(self):
                pass
            def __invert__(self):
                pass
            def __le__(self, value):
                pass
            def __lshift__(self, value):
                pass
            def __lt__(self, value):
                pass
            def __mod__(self, value):
                pass
            def __mul__(self, value):
                pass
            def __ne__(self, value):
                pass
            def __neg__(self):
                pass
            def __or__(self, value):
                pass
            def __pos__(self):
                pass
            def __pow__(self, value, mod=None):
                pass
            def __radd__(self, value):
                pass
            def __rand__(self, value):
                pass
            def __rdivmod__(self, value):
                pass
            def __rfloordiv__(self, value):
                pass
            def __rlshift__(self, value):
                pass
            def __rmod__(self, value):
                pass
            def __rmul__(self, value):
                pass
            def __ror__(self, value):
                pass
            def __round__(self):
                pass
            def __rpow__(self, value, mod=None):
                pass
            def __rrshift__(self, value):
                pass
            def __rshift__(self, value):
                pass
            def __rsub__(self, value):
                pass
            def __rtruediv__(self, value):
                pass
            def __rxor__(self, value):
                pass
            def __sizeof__(self):
                pass
            def __sub__(self, value):
                pass
            def __truediv__(self, value):
                pass
            def __trunc__(self):
                pass
            def __xor__(self, value):
                pass
            def as_integer_ratio(self):
                pass
            def bit_count(self):
                pass
            def bit_length(self):
                pass
            def conjugate(self):
                pass
            def denominator(self):
                pass
            def imag(self):
                pass
            def numerator(self):
                pass
            def real(self):
                pass
        if 1:   # String, bytes & interpolation methods
            def __doc__(self):
                pass
            def __format__(self, format_spec):
                pass
            def __repr__(self):
                pass
            def __str__(self):
                s =  str(self._x)[11:-2]
                if self._signed:
                    return f"Int{self.n}(0b{s})"
                else:
                    return f"intu{self.n}(0b{s})"
            def from_bytes(self, bytes, byteorder='big', signed=False):
                pass
            def to_bytes(self, length=1, byteorder='big', signed=False):
                pass
        if 1:   # Properties
            @property
            def n(self):
                return self._numbits
        if 1:   # Notes on two's complement
            '''
            
            [1] https://en.wikipedia.org/wiki/Two%27s_complement
            [2] https://crystal.uta.edu/~carroll/cse2441/uploads/52503FE6-36D0-C662-55FF-CD571EA08D09_.pdf
            [3] https://www.electronicsmedia.info/2024/02/10/twos-complement/
            
            '''
    if 0: #xx
        x = Int(12)
        print(x)
        x = Int(12, 8)
        print(x)
        exit()

if __name__ == "__main__":
    from lwtest import run, Assert, raises
    from columnize import Columnize
    from color import t
    import sys
    if 1:   # Self-tests
        def Test_IntToBase():
            raises(TypeError, IntToBase, 1.2, 2)
            raises(TypeError, IntToBase, 2, 1.2)
            raises(ValueError, IntToBase, 2, 1)
            Assert(IntToBase(0, 2) == (0,))
            Assert(IntToBase(1, 2) == (1,))
            Assert(IntToBase(2, 2) == (1, 0))
            Assert(IntToBase(2, 2, msd_first=False) == (0, 1))
            Assert(IntToBase(10017, 82) == (1, 40, 13))
            Assert(IntToBase(10017, 82, msd_first=False) == (13, 40, 1))
        def Test_ByteReverseDict():
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
    if 1:   # Demo
        def Demo():
            t.print(f"{t.purl}Demo of some functions in {sys.argv[0]}")
            ind = " "*2
            if 1:   # Bit reversing
                o = []
                for x in range(0, 25):
                    w = len(int2ba(x))
                    o.append(f"{x:3d} {x:0{w}b} → {IntBitReverse(x):0{w}b}")
                t.print(f"{t.ornl}Bit reversing:  IntBitReverse(x)")
                for i in Columnize(o, indent=" "*2):
                    print(i)
            if 1:   # Showing a bitarray in a desired base using rBitarray
                t.print(f"{t.ornl}Showing a bitarray in a desired base using rBitarray()")
                ba = int2ba(70)
                for b in (2, 5, 7, 8, 10, 11, 16, 49):
                    print(f"{ind}{b:2d}  {rBitarray(ba, b)}")
            if 1:   # Integer representation in any base
                t.print(f"{t.ornl}Convert an integer to any base using IntToBase()")
                print(f"{ind}IntToBase(10017, 82) --> {IntToBase(10017, 82)}")
                print(f"{ind}  Check:  13*82**0 + 40*82**1 + 1*82**2 = 13 + 3280 + 6724 = 10017")
    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        exit(run(globals(), halt=True)[0])
    Demo()
