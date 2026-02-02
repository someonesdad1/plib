'''
Python 3 hexdump module
    hexdump("abc") produces
        "00000000: 6162 63                                  abc\n"
    hexdump("abc", asc=False) produces
        "00000000: 6162 63\n"
    hexdump("abc", offset=1) produces
        "00000001: 6263                                     bc\n"
    hexdump("abc", length=2) produces
        "00000000: 6162                                     ab\n"
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Hexdump module oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2020 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ run oo>
        <oo todo ∞ 
        
            - obj can be a pathlib.Path
        
        oo>
    '''
    if 1:  # Standard imports
        import io
        from functools import partial
    if 1:  # Custom imports
        pass
    if 1:  # Global variables
        pass
if 1:  # Core functionality
    def hexdump(obj, offset=0, length=0, asc=True, out=None, encoding="UTF-8"):
        '''Return a string of the hexdump of obj.  If out is given, then
        send the hexdump string to it.
        
        obj can be a string, bytestring, or stream.  If it is a string, it
        is encoded to a bytestring with the indicated encoding.
        
        asc
            Include ASCII text if True.
        encoding
            How to decode obj when it is a text string.
        length
            Stop after this number of bytes if not zero.
        offset
            Where to start in the input stream.
        out
            Stream to send the output if not None.
            
        Compared to xxd, this function takes about 3.5 times as long for a
        hex dump of a 5.5 MB file.
        '''
        if not hasattr(hexdump, "tt"):
            # Make translation table to convert bytes to ASCII characters
            From, To = bytes(range(256)), bytearray(range(256))
            for i in range(32):
                To[i] = ord(".")
            for i in range(0x7F, 0x100):
                To[i] = ord(".")
            hexdump.tt = bytes.maketrans(From, To)
        o = out if out else io.StringIO()
        # Make the input a stream of bytes
        e = TypeError(f"obj is an unsupported type = '{type(obj)}'")
        if isinstance(obj, str):
            in_stream = io.BytesIO(obj.encode(encoding))
        elif isinstance(obj, (bytes, bytearray)):
            in_stream = io.BytesIO(obj)
        elif hasattr(obj, "read"):
            if not isinstance(obj, (io.BytesIO, io.BufferedReader)):
                raise e
            in_stream = obj
        else:
            raise e
        # Set our variables
        bytes_printed = 0
        line_address = 0
        bytes_per_line, line_length = 16, 41
        Print = partial(print, file=o, end="")
        # Correct for the offset
        if offset:
            in_stream.read(offset)
            line_address = offset
        data = in_stream.read(bytes_per_line)  # First line of data
        while data:
            Print(f"{line_address:08x}: ")
            line_address += bytes_per_line
            line = []
            truncated = False
            for i, byte in enumerate(data):
                line.append(f"{byte:02x}")
                if i and (i + 1) % 2 == 0:
                    line.append(" ")
                bytes_printed += 1
                if length and bytes_printed >= length:
                    truncated = True
                    break
            s = "".join(line)
            if asc and (len(s) < line_length):
                s += " " * (line_length - len(s))
            Print(s)
            # Add ASCII decode
            if asc:
                if truncated:
                    data = data[: i + 1]
                Print(data.translate(hexdump.tt).decode("ASCII"))
            Print("\n")
            if length and bytes_printed >= length:
                break
            data = in_stream.read(bytes_per_line)  # Next line
        # We're done.  Return a string if the output stream was None.
        if out is None:
            return o.getvalue()

if __name__ == "__main__":
    from lwtest import run
    from io import StringIO
    def Test():
        hd = hexdump
        s = "abc"
        e = "00000000: 6162 63                                  abc\n"
        assert hd(s) == e
        # Test out
        o = StringIO()
        hd(s, out=o)
        assert o.getvalue() == e
        # Test offset
        e = "00000001: 6263                                     bc\n"
        assert hd(s, offset=1) == e
        # Test length
        e = "00000000: 6162                                     ab\n"
        assert hd(s, length=2) == e
        # Test asc
        e = "00000000: 6162 63\n"
        assert hd(s, asc=False) == e
    exit(run(globals(), halt=1)[0])
