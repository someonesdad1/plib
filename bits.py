_pgminfo = '''
<oo 
    Utilities that work with binary bits
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat utility oo>
<oo test -t oo>
<oo todo

- bitarray implementation of fixed-size integers for python
    - Probably should derive from int
    - Allow signed (default) or unsigned
- See https://graphics.stanford.edu/%7Eseander/bithacks.html for ideas

oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        pass
    if 1:   # Custom imports
        have_bitarray = False
        try:
            from bitarray import bitarray
            from bitarray.util import int2ba, ba2int
            have_bitarray = True
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
if 1:   # Fixed-size integers
    class intf:

        '''This class implements immutable fixed-size integers.  

        Properties
            - n     number of bits making up the integer; mutable
            - u     Unsigned if true 

        Features

        - Implemented with bitarray, so fast and can have arbitrary size
        - Immutable
        - Closure:  inst1 and inst2 combined via a binary operature will return another 
          intf; result.n = max(isnt1.n, inst2.n)
            - Otherwise, in an operation with another numeric type, the instance is
              converted to and int and the operation proceeds
        - Arithmetic is 2's complement

        Their primary use case is to simulate n-bit integer functionality.  If a binary
        operation is performed with two intf objects, a bitf instance will be returned
        with the number of bits of the largest number of bits of the two operands.

        Operations can be performed with other numerical objects, but the same intf
        instance type will be returned, regardless of the numerical type of the other
        operand.  Thus, a regular python integer or float can be added to an intf
        instance, but the integer or float will first be converted to the same type of
        intf object; thus, an intf object is returned.

        Integer methods (from int(0).__dir__(); the ones that should be implemented are
        the ones detailed in `pd int`)

            Should implement

            Don't need to implement

                __class__
                __getattribute__
                __getnewargs__
                __getstate__
                __init__
                __init_subclass__
                __new__
                __reduce__
                __reduce_ex__
                __setattr__
                __subclasshook__

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
            # Mask off val to numbits
            self._x = bitarray(numbits)
            self._u = bool(unsigned)
            self._sign = -1 if value < 0 else 1
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
                pass
            def from_bytes(self, bytes, byteorder='big', signed=False):
                pass
            def to_bytes(self, length=1, byteorder='big', signed=False):
                pass
        if 1:   # Properties
            pass
        if 1:   # Notes on two's complement
            '''
            
            [1] https://en.wikipedia.org/wiki/Two%27s_complement
            [2] https://crystal.uta.edu/~carroll/cse2441/uploads/52503FE6-36D0-C662-55FF-CD571EA08D09_.pdf
            [3] https://www.electronicsmedia.info/2024/02/10/twos-complement/

            '''

    if 1: #xx
        x = intf(12, 8)
        print(x)
        exit()

if __name__ == "__main__":
    from lwtest import run, Assert, raises
    from columnize import Columnize
    from color import t
    import sys
    if 1:   # Self-tests
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
    def Demo():
        t.print(f"{t.purl}Demo of some functions in {sys.argv[0]}")
        o = []
        for x in range(0, 49):
            w = len(int2ba(x))
            o.append(f"{x:3d} {x:0{w}b} {IntBitReverse(x):0{w}b}")
        t.print(f"{t.ornl}Bit reversing")
        for i in Columnize(o, indent=" "*2):
            print(i)
    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        exit(run(globals(), halt=True)[0])
    Demo()
    print("Use -t option to run self-tests")
