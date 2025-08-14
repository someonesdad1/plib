'''
Implements a class that allows you to create large bitfields.  The bits are numbered
from 0 to n - 1, where n is the size of the bitfield.  There are three implementations:  
    - sbitfield uses a list of string characters 
    - bitfield is derived from an integer
    - bbitfield uses a bytearray
'''
if 1:   # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2005 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # <programming> Class for arbitrarily long bitfields.  There are two
        # implementation classes:  one uses lists of strings to store the
        # data (and thus more memory); the other is derived from an int.
        # The int-derived one has simpler code, but it's slower than the
        # string implementation.
        ##∞what∞#
        ##∞test∞# run #∞test∞#
        pass
    if 1:   # Standard imports
        import os
        import sys
        import subprocess
        import tempfile
        from pathlib import Path
    if 1:   # Custom imports
        from util import NumBitsInByte
        if len(sys.argv) > 1:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        ii = isinstance
        __all__ = ["sbitfield", "bitfield", "bbitfield"]
if 0:   # Obsolete classes
    class sbitfield(object):
        '''Lets you define arbitrary bit fields.   All bit fields can be initialized to all
        zeros or all ones.  If you choose to use a large bit field, the most time consuming
        tasks are creation of and changing a large range.
        
        A list of strings is used to implement the bit field.  Each character in a string
        represents 8 bits and each list element represents self.num_rows*8 bits.  You can
        specify the number of bits in each row if you like (list element 0 is row 1, list
        element 1 is row 2, etc.).
        '''
        def __init__(self, num_bits, init_with_ones=False, num_bits_in_row=64*8):
            self.errorstr = "Error"
            self.num_bits = int(num_bits)
            if self.num_bits < 1:
                raise ValueError("number_of_bits must be > 0")
            if not ii(num_bits_in_row, int) or num_bits_in_row < 8:
                raise ValueError("num_bits_in_row must be an integer >= 8")
            if num_bits_in_row % 8 != 0:
                raise ValueError("num_bits_in_row must be divisible by 8")
            self.num_bits_in_row = num_bits_in_row
            self.num_bytes_in_row = int(num_bits_in_row / 8)
            self.num_rows = int(
                self.num_bits / num_bits_in_row + (self.num_bits % num_bits_in_row != 0)
            )
            self.dot = 0  # Set to != 0 for '.' and '|' representation.
            self.bitstr = []
            self.zero = chr(0) * int(self.num_bits_in_row / 8)
            self.one = chr(255) * int(self.num_bits_in_row / 8)
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
            return not (not (ord(self.bitstr[row][byte]) & (1 << bit)))
        def is_clear(self, bit_position):
            return not self.is_set(bit_position)
        def set_bit(self, bit_position):
            self.__set_bit(bit_position, 1)
        def clear_bit(self, bit_position):
            self.__set_bit(bit_position, 0)
        def __set_bit(self, bit_position, value):
            row, byte, bit = self.__get_index(bit_position)
            s = self.bitstr
            assert value == 0 or value == 1
            if value == 1:
                new_byte = chr(ord(s[row][byte]) | (1 << bit))
            else:
                new_byte = chr(ord(s[row][byte]) & (~(1 << bit)))
            if byte == 0:
                if len(s[row]) > 1:
                    s[row] = new_byte + s[row][1:]
                else:
                    s[row] = new_byte
            elif byte == self.num_bytes_in_row - 1:
                s[row] = s[row][:-1] + new_byte
            else:
                s[row] = s[row][:byte] + new_byte + s[row][byte + 1 :]
            assert len(s[row]) == self.num_bytes_in_row
        def set_bit_range(self, start, end):
            "Set a range of bits"
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
            if (
                not ii(bit_position, int)
                or bit_position < 0
                or bit_position > self.num_bits - 1
            ):
                raise ValueError(
                    "bit position must be >= 0 and <= %d" % (self.num_bits - 1)
                )
        def __repr__(self):
            '''Returns binary representation with LSB to right.  Set self.dot
            to nonzero to use an alternative form from 1's and 0's that's
            sometimes easier to read.
            '''
            str = ""
            on = "1"
            off = "0"
            if self.dot:
                on = "|"
                off = "."
            for i in range(self.num_bits - 1, -1, -1):
                if self.is_set(i):
                    str = str + on
                else:
                    str = str + off
            return str
        def num_bytes_used(self):
            tmp = self.num_bytes_in_row*self.num_rows
            try:
                retval = int(tmp)
            except ValueError:
                retval = tmp
            return retval
        def __eq__(self, o):
            if type(o) is not type(self):
                raise ValueError("object is not a bitfield")
            if o.num_bits != self.num_bits:
                return False
            for i in range(self.num_rows):
                if o.bitstr[i] != self.bitstr[i]:
                    return False
            return True
        def __cmp__(self, o):
            "Implements ==, != only"
            if type(o) is not type(self):
                raise ValueError("object is not a bitfield")
            if o.num_bits != self.num_bits:
                return 1
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
            "Note the number of bits is ignored as long as values are equal"
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
            self._value |= 1 << n
        def clear_bit(self, n):
            self._check_n(n)
            self._value |= 1 << n  # Turns bit on
            self._value ^= 1 << n  # Turns bit off
        def set_bit_range(self, start, end):
            self._check_n(start, name="start")
            self._check_n(end, name="end")
            if start > end:
                raise ValueError("start must be less than end")
            for i in range(start, end + 1):
                self._value |= 1 << i
        def clear_bit_range(self, start, end):
            self._check_n(start, name="start")
            self._check_n(end, name="end")
            if start > end:
                raise ValueError("start must be less than end")
            for i in range(start, end + 1):
                self._value |= 1 << i
                self._value ^= 1 << i
        def set_to_zeros(self):
            self._value = 0
        def set_to_ones(self):
            self._value = self
        @property
        def bits(self):
            return self._bits
        @property
        def value(self):
            "Returns the current integer value of the bitfield"
            return int(self._value)
        @value.setter
        def value(self, val):
            "Sets the current value of the bitfield"
            if not ii(val, int) or val < 0:
                raise ValueError("val must be an integer >= 0")
            self._value = int(val & self)
if 1:   # Classes
    class bbitfield:
        '''This is a bitfield implemented with a bytearray, a mutable sequence of bytes.
        Byte 0 is the first byte, byte 1 is the second, etc.  A two-byte bitfield would
        have the bytes
        
              76543210 fedcba98     <-- bitfield index for bit
                 0        1         <-- byte number
            0b00000000·00000000
              7      0 7      0     <-- array bit numbers
        
        where the dot denotes a byte boundary.  This is "natural" numbering because of
        the convention of numbering the bits in a byte from left to right in terms of
        bit number.
        
        Overall, the bit numbering in the bitfield runs from 0 to n - 1, where n is the
        total number of bits in the bitfield.
        
        For large bitfields, the display method of choice is probably the dump() method,
        as this uses /usr/bin/xxd to send a binary or hex dump to stdout and, if most
        bits are zero, this won't be a large listing because the -a option is used.

        Timing 14 Aug 2025 on my 4 core Windows box new in 2016 under WSL using python
        3.11.5 to create a new bitfield:
            10**6 bits:  time = 0.0107 ms
            10**7 bits:  time = 0.532 ms
            10**8 bits:  time = 3.35 ms
            10**9 bits:  time = 29.7 ms
            10**10 bits:  time = 292 ms
        For 10**11 bits, there was a memory error.
        
        Times to set all the bits (done by a loop that sets a byte at a time):
            Set 10**6 bits:  time = 0.00478 s
            Set 10**7 bits:  time = 0.0401 s
            Set 10**8 bits:  time = 0.419 s
            Set 10**9 bits:  time = 3.98 s
            Set 10**10 bits:  time = 42.5 s

        Times to set 1% of the bits:
            10**6 bits:  time = 0.00281 s to set 10**4 bits
            10**7 bits:  time = 0.0269 s to set 10**5 bits
            10**8 bits:  time = 0.273 s to set 10**6 bits
            10**9 bits:  time = 2.72 s to set 10**7 bits
        
        These times indicate that this data structure could be handy for sparse bit
        arrays.  An example would be a datafile contining 1e9 bits that would indicate
        the prime numbers:  if primes[n] is True, then n is a prime.

        Properties
          n         Number of bits in the bitfield
          numbytes  Number of bytes in the bitfield
          excess    Unused bits in the last byte of the bytestring
        
        Attributes
          dot       Set to True for an easier to read string form
        
        Invariants
            self.n + self.excess = 8*self.bytes
        '''
        def __init__(self, nbits, all_ones=False):
            '''Array of bits from 0 to nbits - 1.  Initialized to all zeros unless
            all_ones is True.
            '''
            self.dot = False    # Set to True for an easier to read string form
            self._nbits = int(nbits)
            if self._nbits <= 0:
                raise ValueError("nbits must be > 0")
            self._nbytes = self._nbits//8
            if self._nbits % 8:
                self._nbytes += 1
            self._excess = self._nbytes*8 - self._nbits
            self._bytes = bytearray(self._nbytes)
            if all_ones:
                self.set_all(1)
        if 1:   # Internal-only methods
            def __is_valid_bit_position(self, bit_position):
                if not isinstance(bit_position, int):
                    raise TypeError("bit_position must be an int")
                if not (0 <= bit_position <= self._nbits - 1):
                    raise IndexError(f"bit_position must be >= 0 and <= {self._nbits - 1}")
            def __get_index(self, bit_position):
                '''Return a tuple (i, j).  i is the byte the bit is in.  j is the bit position
                in that byte.
                '''
                self.__is_valid_bit_position(bit_position)
                return divmod(bit_position, 8)
        if 1:   # Methods
            def get_bit(self, bit_position):
                'Return the value of the bit at the indicated position'
                byte, bit = self.__get_index(bit_position)
                return bool(self._bytes[byte] & (1 << bit))
            def set_bit(self, bit_position, value):
                'Set indicated bit to the desired value'
                byte, bit = self.__get_index(bit_position)
                if bool(value):     # Set the bit
                    self._bytes[byte] |= (1 << bit)     # Set the bit
                else:
                    self._bytes[byte] &= ~(1 << bit)    # Clear the bit
            def set_bit_range(self, start, end, value=0):
                'Set a range of bits'
                self.__is_valid_bit_position(start)
                self.__is_valid_bit_position(end)
                if start > end:
                    raise ValueError("start must be less than end")
                for bit_position in range(start, end + 1):
                    self.set_bit(bit_position, value)
            def set_all(self, value=0):
                'Set all bits to the indicated value'
                for i in range(len(self._bytes)):
                    self._bytes[i] = 0xff if value else 0
            def num_set(self):
                'Return the number of bits set'
                count = 0
                for i in self._bytes:
                    count += 

            def dump(self, binary=True):
                '''Use /usr/bin/xxd to produce a dump to stdout (if binary is False, it
                will be a hexdump).
                '''
                file = tempfile.NamedTemporaryFile(delete=False, prefix="bbitfield", suffix=".tmp")
                file.write(self._bytes)
                file.close()
                cmd = ["/usr/bin/xxd", "-a", file.name]
                if binary:
                    cmd = ["/usr/bin/xxd", "-a", "-b", file.name]
                subprocess.run(cmd)
                os.unlink(file.name)
        if 1:   # Properties
            @property
            def numbytes(self):
                'Number of bytes'
                return self._nbits
            @property
            def n(self):
                'Number of bits'
                return self._nbits
            @property
            def excess(self):
                'Number of excess bits in last byte'
                return self._excess
        if 1:   # Object methods
            def __len__(self):
                'Returns number of bits in bitfield'
                return self._nbits
            def __getitem__(self, bit_index):
                '''Access the value of a particular bit by the syntax
                    value = self[bit_index]
                '''
                return self.get_bit(bit_index)
            def __setitem__(self, bit_index, value):
                '''Set the value of a particular bit by the syntax
                    self[bit_index] = value
                '''
                self.set_bit(bit_index, value)
            def __str__(self):
                '''Returns binary representation with LSB to right.  Example:
                if bb = bbitfield(5), then str(bb) is '00000'.  After executing 'bb[1] =
                1', then str(bb) is '00010'.  Executing bb.dot = True, str(bb) is '...|.'.
                '''
                s, on, off = "", "1", "0"
                if self.dot:
                    on, off = "|", "."
                for i in range(self.n - 1, -1, -1):
                    s = s + on if self[i] else s + off
                return s
            def __repr__(self):
                return f"bbitfield({self.n})"
            def __eq__(self, o):
                if type(o) is not type(self):
                    raise ValueError("object is not a bbitfield")
                if o.num_bits != self.num_bits:
                    return False
                # Check bytes for equality
                numbytes, excess = divmod(self._nbits, 8)
                for i in range(numbytes):
                    if o._bytes[i] != self._bytes[i]:
                        return False
                # If there's a partial number of bits, check them too
                nbits = 8*(self._bytes)
                for i in range(nbits, nbits + excess):
                    if o[i] != self[i]:
                        return False
                return True
            def __cmp__(self, o):
                "Implements ==, != only"
                if type(o) is not type(self):
                    raise ValueError("object is not a bbitfield")
                if o.num_bits != self.num_bits:
                    return 1
                for i in range(self.num_rows):
                    if o.bitstr[i] != self.bitstr[i]:
                        return 1
                return 0

if 1: #xx
    import timer
    tm = timer.Timer()
    # Measure time to set a string of bits that's 10% of size of bitfield
    for n in range(6, 10):
        bb = bbitfield(10**n)
        n_delta = 2
        sz = 10**(n - n_delta)
        tm.start
        bb.set_bit_range(0, sz, value=1)
        tm.stop
        print(f"10**{n} bits:  time = {tm.et} s to set 10**{n - n_delta} bits")
    exit()
    bb.dot = 0
    bb[1] = bb[3] = 8
    #print(bb)
    bb.dump()
    exit()

if __name__ == "__main__":
    import sys
    from lwtest import run, Assert
    from timer import Timer
    def CheckTiming(name, cls, nums=(6, 7, 8, 9)):
        timer = Timer()
        print(f"{name} timing:")
        for n in nums:
            timer.start
            cls(10**n)
            timer.stop
            print(f"  Size {10**n:.1e} time = {timer.et:.2f} sec")
    if len(sys.argv) > 1:
        CheckTiming("sbitfield", sbitfield, nums=(6, 7, 8, 9, 10, 11))
        CheckTiming("bitfield", bitfield)
        exit()
    def Check_bitfield(size, cls):
        size = int(size)
        if ii(cls, sbitfield):
            a = sbitfield(size)
            b = sbitfield(size, init_with_ones=0)
            ones = sbitfield(size, init_with_ones=1)
        else:
            a = bitfield(size)
            b = bitfield(size)  # All zeroes
            ones = bitfield(size)
            ones.value = ones  # All ones
        # Tests
        b.set_bit(size - 1)
        assert b.is_set(size - 1)
        b.clear_bit(size - 1)
        assert b.is_clear(size - 1)
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
            Check_bitfield(size, bitfield)
            Check_bitfield(size, bbitfield)
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
            x |= 1 << i
            Assert(b.value == x)
            Assert(b.is_set(i))
        # Test clear_bit() and is_clear()
        for i in range(b.bits):
            b.clear_bit(i)
            x |= 1 << i
            x ^= 1 << i
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
