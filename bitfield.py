'''

Implements a class that allows you to create large bitfields.  The bits
are numbered from 0 to n - 1, where n is the size of the bitfield.

There are two implementations:  sbitfield uses a list of string
characters and bitfield is derived from an integer.  The code for
bitfield is simpler, but it's slower for larger numbers of bits.
 
Here are some creation times for a 166 MHz Pentium with 32 MB of RAM
running Windows NT 4.0 (probably around 1999):
    size = 10^6 bits, creation time = 0.05 sec
    size = 10^7 bits, creation time = 0.5 sec
    size = 10^8 bits, creation time = 7.2 sec
    size = 10^9 bits, creation time = 327 sec
 
Probably tested in Nov 2002, as that's the earliest RCS entry.
Here are some creation times of larger bitfields on a laptop PC
(approx. 800 MHz Pentium machine with 256 MB RAM and Windows 2000):
    size = 10^6 bits, creation time = 0.04 sec
    size = 10^7 bits, creation time = 0.37 sec
    size = 10^8 bits, creation time = 4.16 sec
    size = 10^9 bits, creation time = 42.2 sec
 
11 Apr 2008 on dual AMD machine:
    Size 1.0e+006 time = 0.00 sec
    Size 1.0e+007 time = 0.09 sec
    Size 1.0e+008 time = 1.05 sec
    Size 1.0e+009 time = 10.13 sec
 
30 Dec 2010 on quad Pentium 2.5 GHz running Windows 7:
    Size 1.0e+06 time = 0.00 sec
    Size 1.0e+07 time = 0.03 sec
    Size 1.0e+08 time = 0.35 sec
    Size 1.0e+09 time = 3.57 sec
 
9 Aug 2014 on quad Pentium 2.5 GHz running Ubuntu 14.04:
    Size 1.0e+06 time = 0.00 sec
    Size 1.0e+07 time = 0.02 sec
    Size 1.0e+08 time = 0.24 sec
    Size 1.0e+09 time = 2.43 sec

9 May 2017 on quad core 3.5 GHz machine purchased Apr 2017 running Windows 10:
    Size 1.0e+06 time = 0.00 sec
    Size 1.0e+07 time = 0.00 sec
    Size 1.0e+08 time = 0.03 sec
    Size 1.0e+09 time = 0.26 sec

----------------------------------------------------------------------
8 Jun 2021 on quad core 3.5 GHz machine purchased Apr 2017 running Windows 10:
    Running python 3.7.7 using the sbitfield class:
    Size 1.0e+06 time = 0.00 sec
    Size 1.0e+07 time = 0.00 sec
    Size 1.0e+08 time = 0.02 sec
    Size 1.0e+09 time = 0.23 sec
    Size 1.0e+10 time = 2.51 sec
    Size 1.0e+11 time = 25.87 sec

On 8 Jun 2021 I reimplemented the class bitfield as derived from an
integer, as it makes the implementation simpler.  However, it's slower
for larger bitfields:
    Size 1.0e+06 time = 0.01 sec
    Size 1.0e+07 time = 0.05 sec
    Size 1.0e+08 time = 0.69 sec
    Size 1.0e+09 time = 9.50 sec
'''
 
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2005 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <programming> Class for arbitrarily long bitfields.  There are two
    # implementation classes:  one uses lists of strings to store the
    # data (and thus more memory); the other is derived from an int.
    # The int-derived one has simpler code, but it's slower than the
    # string implementation.
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Imports
    from pdb import set_trace as xx 
if 1:   # Global variables
    ii = isinstance
    __all__ = ["sbitfield", "bitfield"]
class sbitfield(object):
    '''Lets you define arbitrary bit fields.   All bit fields can be
    initialized to all zeros or all ones.  If you choose to use a
    large bit field, the most time consuming tasks are creation of
    and changing a large range.

    A list of strings is used to implement the bit field.  Each character
    in a string represents 8 bits and each list element represents
    self.num_rows*8 bits.  You can specify the number of bits in each
    row if you like (list element 0 is row 1, list element 1 is row 2,
    etc.).
    '''
    def __init__(self, num_bits, init_with_ones=0, num_bits_in_row=64*8):
        self.errorstr = "Error"
        self.num_bits = int(num_bits)
        if self.num_bits < 1:
            raise ValueError("number_of_bits must be > 0")
        if not ii(num_bits_in_row, int) or num_bits_in_row < 8:
            raise ValueError("num_bits_in_row must be an integer >= 8")
        if num_bits_in_row % 8 != 0:
            raise ValueError("num_bits_in_row must be divisible by 8")
        self.num_bits_in_row = num_bits_in_row
        self.num_bytes_in_row = int(num_bits_in_row/8)
        self.num_rows = int(self.num_bits/num_bits_in_row +
                            (self.num_bits % num_bits_in_row != 0))
        self.dot = 0    # Set to != 0 for '.' and '|' representation.
        self.bitstr = []
        self.zero = chr(0)*int(self.num_bits_in_row/8)
        self.one = chr(255)*int(self.num_bits_in_row/8)
        if init_with_ones:
            for i in range(self.num_rows):
                self.bitstr.append(self.one)
        else:
            for i in range(self.num_rows):
                self.bitstr.append(self.zero)
    def __get_index(self, bit_position):
        '''Return a tuple; the first element is which row the bit is in,
        the next element is which byte, and the next is which bit in
        that byte.
        '''
        self.__within_range(bit_position)
        row, bit_in_row = divmod(bit_position, self.num_bits_in_row)
        byte_in_row, bit_in_byte = divmod(bit_in_row, 8)
        return (row, byte_in_row, bit_in_byte)
    def is_set(self, bit_position):
        row, byte, bit = self.__get_index(bit_position)
        return not(not(ord(self.bitstr[row][byte]) & (1 << bit)))
    def is_clear(self, bit_position):
        return not self.is_set(bit_position)
    def set_bit(self, bit_position):
        self.__set_bit(bit_position, 1)
    def clear_bit(self, bit_position):
        self.__set_bit(bit_position, 0)
    def __set_bit(self, bit_position, value):
        row, byte, bit = self.__get_index(bit_position)
        s = self.bitstr
        assert(value == 0 or value == 1)
        if value == 1:
            new_byte = chr(ord(s[row][byte]) | (1 << bit))
        else:
            new_byte = chr(ord(s[row][byte]) & (~ (1 << bit)))
        if byte == 0:
            if len(s[row]) > 1:
                s[row] = new_byte + s[row][1:]
            else:
                s[row] = new_byte
        elif byte == self.num_bytes_in_row - 1:
            s[row] = s[row][:-1] + new_byte
        else:
            s[row] = s[row][:byte] + new_byte + s[row][byte+1:]
        assert(len(s[row]) == self.num_bytes_in_row)
    def set_bit_range(self, start, end):
        'Set a range of bits'
        if start > end:
            raise ValueError("start must be less than end")
        for bit_position in range(start, end + 1):
            self.__set_bit(bit_position, 1)
    def clear_bit_range(self, start, end):
        for bit_position in range(start, end + 1):
            self.__set_bit(bit_position, 0)
    def set_to_zeros(self):
        self.bitstr = []
        for i in range(self.num_rows):
            self.bitstr.append(self.zero)
    def set_to_ones(self):
        self.bitstr = []
        for i in range(self.num_rows):
            self.bitstr.append(self.one)
    def __within_range(self, bit_position):
        if (not ii(bit_position, int) or
                bit_position < 0 or
                bit_position > self.num_bits - 1):
            raise ValueError("bit position must be >= 0 and <= %d" %
                            (self.num_bits - 1))
    def __repr__(self):
        '''Returns binary representation with LSB to right.  Set self.dot
        to nonzero to use an alternative form from 1's and 0's that's
        sometimes easier to read.
        '''
        str = ""
        on = '1'
        off = '0'
        if self.dot:
            on = '|'
            off = '.'
        for i in range(self.num_bits-1, -1, -1):
            if self.is_set(i):
                str = str + on
            else:
                str = str + off
        return str
    def num_bytes_used(self):
        tmp = self.num_bytes_in_row*self.num_rows
        try:
            retval = int(tmp)
        except:
            retval = tmp
        return retval
    def __eq__(self, o):
        if type(o) != type(self):
            raise ValueError("object is not a bitfield")
        if o.num_bits != self.num_bits:
            return False
        for i in range(self.num_rows):
            if o.bitstr[i] != self.bitstr[i]:
                return False
        return True
    def __cmp__(self, o):
        "Implements ==, != only"
        if type(o) != type(self):
            raise ValueError("object is not a bitfield")
        if o.num_bits != self.num_bits:
            return 1
        match = 0
        for i in range(self.num_rows):
            if o.bitstr[i] != self.bitstr[i]:
                return 1
        return 0
class bitfield(int):
    '''This implementation derives from integer.  The instantiated
    integer value is the equivalent integer of all bits set for the
    given number of bits.  Internally, the current value of the integer
    is stored, as it can change over time.

    An advantage of this implementation over the old one with an array
    of string characters is that it uses python's built-in machinery to
    deal with integers.  A disadvantage is that it's slower, but it
    would be rare to need a bitfield over, say, a million bits, so this
    isn't a big hardship.  If you need e.g. a billion bits, use the
    sbitfield class.
    '''
    def __new__(cls, bits, value=0):
        '''The bits of value are used to initialize the bitfield's
        value, which is stored in the value attribute.
        '''
        if not ii(bits, int) or bits < 1:
            raise ValueError("bits must be integer > 0")
        if not ii(value, int) or value < 0:
            raise ValueError("value must be integer >= 0")
        instance = super(bitfield, cls).__new__(cls, 2**bits - 1)
        instance._bits = bits
        instance._value = value & int(instance)
        return instance
    def __str__(self):
        return f"bitfield(<bits={self._bits}>{bin(self._value)})"
    def __repr__(self):
        return f"bitfield({self._bits})"
    def __eq__(self, other):
        'Note the number of bits is ignored as long as values are equal'
        if not ii(other, bitfield):
            raise ValueError("other is not a bitfield")
        return int(self._value) == int(other._value)
    def _check_n(self, n, name="n"):
        if not ii(n, int) or n < 0 or n >= self.bits:
            m = f"{name} must be integer and 0 <= n < {self.bits}"
            raise ValueError(m)
    def is_set(self, n):
        self._check_n(n)
        return self._value & (1 << n)
    def is_clear(self, n):
        self._check_n(n)
        return not self.is_set(n)
    def set_bit(self, n):
        self._check_n(n)
        self._value |= (1 << n)
    def clear_bit(self, n):
        self._check_n(n)
        self._value |= (1 << n)     # Turns bit on
        self._value ^= (1 << n)     # Turns bit off
    def set_bit_range(self, start, end):
        self._check_n(start, name="start")
        self._check_n(end, name="end")
        if start > end:
            raise ValueError("start must be less than end")
        for i in range(start, end + 1):
            self._value |= (1 << i)
    def clear_bit_range(self, start, end):
        self._check_n(start, name="start")
        self._check_n(end, name="end")
        if start > end:
            raise ValueError("start must be less than end")
        for i in range(start, end + 1):
            self._value |= (1 << i)
            self._value ^= (1 << i)
    def set_to_zeros(self):
        self._value = 0
    def set_to_ones(self):
        self._value = self
    def is_set(self, n):
        self._check_n(n)
        return self._value & (1 << n)
    def is_clear(self, n):
        return not self.is_set(n)
    @property
    def bits(self):
        return self._bits
    @property
    def value(self):
        'Returns the current integer value of the bitfield'
        return int(self._value)
    @value.setter
    def value(self, val):
        'Sets the current value of the bitfield'
        if not ii(val, int) or val < 0:
            raise ValueError("val must be an integer >= 0")
        self._value = int(val & self)
if __name__ == "__main__": 
    import sys
    from lwtest import run, raises, Assert
    from timer import Timer
    def CheckTiming(name, cls):
        timer = Timer()
        print(f"{name} timing:")
        for n in (6, 7, 8, 9):
            start = timer.start
            b = cls(10**n)
            stop = timer.stop
            print(f"  Size {10**n:.1e} time = {timer.et:.2f} sec")
    if len(sys.argv) > 1:
        CheckTiming("sbitfield", sbitfield)
        CheckTiming("bitfield", bitfield)
        exit()
    def Check_bitfield(size, cls):
        size = int(size)
        if ii(cls, sbitfield):
            a = sbitfield(size)
            b = sbitfield(size, init_with_ones = 0)
            ones = sbitfield(size, init_with_ones = 1)
        else:
            a = bitfield(size)
            b = bitfield(size)  # All zeroes
            ones = bitfield(size) 
            ones.value = ones         # All ones
        # Tests
        err = Exception(f"Check_bitfield failed for size {size} cls {cls}")
        b.set_bit(size - 1)
        assert(b.is_set(size - 1))
        b.clear_bit(size - 1)
        assert(b.is_clear(size - 1))
        b.set_bit(size - 2)
        Assert(b.is_set(size - 2))
        b.clear_bit(size - 2)
        Assert(b.is_clear(size - 2))
        b.set_bit(0)
        Assert(b.is_set(0))
        b.clear_bit(0)
        Assert(b.is_clear(0))
        b.set_bit(1)
        Assert(b.is_set(1))
        b.clear_bit(1)
        Assert(b.is_clear(1))
        Assert(a == b)
        b.set_to_ones()
        Assert(b == ones)
        b.set_to_zeros()
        Assert(a == b)
    def Test_checks():
        sizes = (2, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7)
        for size in sizes:
            Check_bitfield(size, sbitfield)
        for size in sizes:
            Check_bitfield(size, bitfield)
    def Test4bit():
        n = 4
        b = bitfield(n)
        Assert(f"{b!s}" == "bitfield(<bits=4>0b0)")
        Assert(f"{b!r}" == "bitfield(4)")
        Assert(b.value == 0)
        x = 0
        # Test set_bit() and is_set()
        for i in range(b.bits):
            b.set_bit(i)
            x |= (1 << i)
            Assert(b.value == x)
            Assert(b.is_set(i))
        # Test clear_bit() and is_clear()
        for i in range(b.bits):
            b.clear_bit(i)
            x |= (1 << i)
            x ^= (1 << i)
            Assert(b.value == x)
            Assert(b.is_clear(i))
        # Test set_to_ones()
        b.set_to_ones()
        Assert(b.value == 2**n - 1)
        # Test set_to_zeros()
        b.set_to_zeros()
        Assert(b.value == 0)
        # Test set_bit_range()
        b.set_bit_range(0, n - 1)
        Assert(b.value == 2**n - 1)
        # Test clear_bit_range()
        b.clear_bit_range(0, n - 1)
        Assert(b.value == 0)
    exit(run(globals())[0])
