# encoding: utf-8
'''
Hex dump utility.
'''

# Copyright (C) 2008, 2017 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

from __future__ import print_function, division
import sys

from pdb import set_trace as xx
if len(sys.argv) > 1:
    import debug
    debug.SetDebugger()

py3 = sys.version_info[0] == 3
String = (str,) if py3 else (str, unicode)
Int = (int,) if py3 else (int, long)
if py3:
    from io import StringIO
else:
    from StringIO import StringIO
from io import BytesIO

# Global variable convenience container
class G:
    bytes_per_line = 16
    nonprintable_char = ord(".")
    ii = isinstance

def hexdump(text, n=None, offset=0, out=None, encoding="utf-8"):
    '''Return an ASCII string hexdump of text.  text can be either a
    string, bytes, or bytearray.  If n is not None, limit the number of
    bytes in the output to that number.  Start the dump at the indicated
    offset.  If out is not None, then it must be a stream, so send the
    ASCII hexdump string to the stream and return None.  If text is a
    string object, then it is decoded into a bytes object using the
    indicated encoding.
 
    This routine has been tested with python 2.7.6 and 3.4.0.
    '''
    stream = StringIO() if out is None else out
    # Check argument types
    if not hasattr(stream, "write"):    
        raise TypeError("out must be a stream-like object")
    if n is not None and not isinstance(n, Int):
        raise TypeError("n must be an integer")
    if not isinstance(offset, Int):
        raise TypeError("offset must be an integer")
    if not isinstance(encoding, String):
        raise TypeError("encoding must be a string")
    def OutputLine(mybytes, offset):
        if len(mybytes) == 0:
            return
        stream.write("{:08x}  ".format(offset))
        # Print the hex values
        for i in range(G.bytes_per_line):
            if i < len(mybytes):
                c = mybytes[i] if py3 else ord(mybytes[i])
                stream.write("{:02x} ".format(c))
            else:
                stream.write("   ")
            if i == 7:
                stream.write(" ")
        stream.write(" | ")
        # Print the ASCII representation
        for i in range(G.bytes_per_line):
            if i < len(mybytes):
                c = mybytes[i] if py3 else ord(mybytes[i])
                if 32 <= c < 128:
                    stream.write("%c" % c)
                else:
                    stream.write("%c" % G.nonprintable_char)
        stream.write("\n")
    # Turn input into bytes
    if isinstance(text, String):
        try:
            text = text.encode(encoding)
        except UnicodeDecodeError:
            # This can happen under python 2 when 8-bit characters 
            # are in text.
            text = bytearray(text)
    elif not isinstance(text, (bytes, bytearray)):
        raise TypeError("text must be a string or bytes/bytearray")
    # Convert the bytes to a stream object using io.BytesIO for
    # convenience.
    src = BytesIO(text)
    n = 2**31 if n is None else n
    if offset:
        src.read(offset)
    mybytes = src.read(G.bytes_per_line)
    count = 0
    while len(mybytes) != 0:
        if len(mybytes) + count >= n:
            mybytes = mybytes[:n - count]
        OutputLine(mybytes, offset)
        count = count + len(mybytes)
        if count >= n:
            break
        mybytes = src.read(G.bytes_per_line)
        offset = offset + G.bytes_per_line
    if out is None:
        return stream.getvalue()

if __name__ == "__main__":
    # Run tests
    out = StringIO()
    text = "This is a sample string that is longer than 16 characters."
    out.write("Whole string:\n" + repr(text) + "\n")
    hexdump(text, out=out)
    # Offset by 1
    out.write("Offset of 1:\n")
    hexdump(text, offset=1, out=out)
    # Offset by 1 and 10 bytes
    out.write("Offset of 1 and n = 10 bytes:\n")
    hexdump(text, offset=1, n=10, out=out)
    s = '''
Whole string:
'This is a sample string that is longer than 16 characters.'
00000000  54 68 69 73 20 69 73 20  61 20 73 61 6d 70 6c 65  | This is a sample
00000010  20 73 74 72 69 6e 67 20  74 68 61 74 20 69 73 20  |  string that is 
00000020  6c 6f 6e 67 65 72 20 74  68 61 6e 20 31 36 20 63  | longer than 16 c
00000030  68 61 72 61 63 74 65 72  73 2e                    | haracters.
Offset of 1:
00000001  68 69 73 20 69 73 20 61  20 73 61 6d 70 6c 65 20  | his is a sample 
00000011  73 74 72 69 6e 67 20 74  68 61 74 20 69 73 20 6c  | string that is l
00000021  6f 6e 67 65 72 20 74 68  61 6e 20 31 36 20 63 68  | onger than 16 ch
00000031  61 72 61 63 74 65 72 73  2e                       | aracters.
Offset of 1 and n = 10 bytes:
00000001  68 69 73 20 69 73 20 61  20 73                    | his is a s
'''[1:-1]
    t = out.getvalue().strip()
    assert(t == s.strip())

    # Check with Unicode
    text = u"abc\xb1\u29fb"
    s = text.encode("utf-8")
    t = hexdump(s)
    e = ("00000000  61 62 63 c2 b1 e2 a7 bb                           "
         "| abc.....\n")
    assert(t == e)
