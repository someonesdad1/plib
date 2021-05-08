'''
Implements a class that allows you to create arbitrarily long
bitfields.  The bits are numbered from 0 to N-1, where N is the
size of the bitfield.
 
The methods are:
    is_set()            Return 1 if specified bit is set
    is_clear()          Return 1 if specified bit is clear
    set_bit()           Set a specified bit
    clear_bit()         Clear a specified bit
    set_bit_range()     Set a range of bits to one
    clear_bit_range()   Set a range of bits to zero
    set_to_zeros()      Set all the bits to zero
    set_to_ones()       Set all the bits to one
    num_bytes_used()    How many bytes the representation takes
 
The implementation uses a list of strings for the bitfields.  You
can choose the size of the strings in the list.
 
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

'''
 
# Copyright (C) 2005 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
 
from __future__ import division
import sys

pyver = sys.version_info[0]
if pyver == 3:
    long = int
ii = isinstance

class bitfield(object):
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
        self.num_bits = long(num_bits)  # Allows ints, longs, floats
        if self.num_bits < 1:
            raise ValueError("number_of_bits must be > 0")
        if not ii(num_bits_in_row, (int, long)) or num_bits_in_row < 8:
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
    def set_bit_range(self, start, finish):
        '''These two functions are inefficient for a setting or
        clearing a large number of bits, but, boy, were they
        easy to write. :)
        '''
        if start > finish:
            raise ValueError("start must be less than finish")
        for bit_position in range(start, finish+1):
            self.__set_bit(bit_position, 1)
    def clear_bit_range(self, start, finish):
        for bit_position in range(start, finish+1):
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
        if (not ii(bit_position, (int, long)) or
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

if __name__ == "__main__": 
    from time import time
    import sys
    if len(sys.argv) > 1:
        # Print out the 10**9 times suitable for plotting
        print('''
# Year Time_in_s for the 10**9 size
1999 327
2002.92 42.2
2008.25 10.13
2011 3.57
2014.6 2.43
2017.4 0.26
'''[1:-1])
    else:
        for n in (6, 7, 8, 9):
            t0 = time()
            b = bitfield(10**n)
            t = time()
            print("Size {:.1e} time = {:.2f} sec".format(10.0**n, t - t0))
