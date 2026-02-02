'''
Hex dump utility
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Hex dump utility oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2008, 2017 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ run oo>
        <oo todo ∞ oo>
    '''
    if 1:  # Standard imports
        from io import StringIO, BytesIO
    if 1:  # Custom imports
        pass
    if 1:  # Global variables
        class G:
            pass
        g = G()
        g.bytes_per_line = 16
        g.nonprintable_char = ord(".")
if 1:  # Core functionality
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
        if n is not None and not isinstance(n, int):
            raise TypeError("n must be an integer")
        if not isinstance(offset, int):
            raise TypeError("offset must be an integer")
        if not isinstance(encoding, str):
            raise TypeError("encoding must be a string")
        def OutputLine(mybytes, offset):
            if len(mybytes) == 0:
                return
            stream.write("{:08x}  ".format(offset))
            # Print the hex values
            for i in range(g.bytes_per_line):
                if i < len(mybytes):
                    c = mybytes[i]
                    stream.write("{:02x} ".format(c))
                else:
                    stream.write("   ")
                if i == 7:
                    stream.write(" ")
            stream.write(" | ")
            # Print the ASCII representation
            for i in range(g.bytes_per_line):
                if i < len(mybytes):
                    c = mybytes[i]
                    if 32 <= c < 128:
                        stream.write("%c" % c)
                    else:
                        stream.write("%c" % g.nonprintable_char)
            stream.write("\n")
        # Turn input into bytes
        if isinstance(text, str):
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
        mybytes = src.read(g.bytes_per_line)
        count = 0
        while len(mybytes) != 0:
            if len(mybytes) + count >= n:
                mybytes = mybytes[: n - count]
            OutputLine(mybytes, offset)
            count = count + len(mybytes)
            if count >= n:
                break
            mybytes = src.read(g.bytes_per_line)
            offset = offset + g.bytes_per_line
        if out is None:
            return stream.getvalue()

if __name__ == "__main__":
    from lwtest import run, assert_equal, raises
    from wrap import dedent
    def TestBasic():
        out = StringIO()  # This also tests hexdump outputting to a stream
        text = "This is a sample string that is longer than 16 characters."
        out.write("Whole string:\n" + repr(text) + "\n")
        hexdump(text, out=out)
        # Offset by 1
        out.write("Offset of 1:\n")
        hexdump(text, offset=1, out=out)
        # Offset by 1 and 10 bytes
        out.write("Offset of 1 and n = 10 bytes:\n")
        hexdump(text, offset=1, n=10, out=out)
        s = dedent('''
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
        ''')
        t = out.getvalue().strip()
        assert_equal(t, s.strip())
        # Trying to dump an empty string returns an empty string
        assert_equal(hexdump(""), "")
    def TestBoundaries():
        text = "abc"
        # Setting n to longer than the string should still work
        s = hexdump(text, n=2 * len(text))
        t = "00000000  61 62 63                                          | abc\n"
        assert_equal(s, t)
        # Setting offset to longer than the string should return empty string
        s = hexdump(text, offset=2 * len(text))
        assert_equal(s, "")
        # Setting offset to one less than string length should put just one
        # character in the hex dump.
        s = hexdump(text, offset=len(text) - 1)
        t = "00000002  63                                                | c\n"
        assert_equal(s, t)
    def TestArguments():
        raises(TypeError, hexdump, 1)
        raises(TypeError, hexdump, "a", n="")
        raises(TypeError, hexdump, "a", n=1.2)
        raises(TypeError, hexdump, "a", offset="")
        raises(TypeError, hexdump, "a", offset=1.2)
        raises(TypeError, hexdump, "a", out=1)
        raises(TypeError, hexdump, "a", out="")
        raises(TypeError, hexdump, "a", encoding=1)
        raises(LookupError, hexdump, "a", encoding="kjdfkdkfj")
    def TestUnicode():
        text = "abc±⧻"
        s = text.encode("utf-8")
        t = hexdump(s)
        e = "00000000  61 62 63 c2 b1 e2 a7 bb                           | abc.....\n"
        assert_equal(t, e)
    exit(run(globals(), halt=1)[0])
