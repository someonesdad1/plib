'''
TODO
    * obj can be a pathlib.Path

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
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2020 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Python 3 hexdump module
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Imports
    import io
    from functools import partial
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
        From, To = bytes(range(256)), bytearray(range(256))
        for i in range(32):
            To[i] = ord(".")
        for i in range(0x7f, 0x100):
            To[i] = ord(".")
        # Translation table to convert bytes to ASCII characters
        hexdump.tt = bytes.maketrans(From, To)
    o = out if out else io.StringIO()
    # Make the input a stream of bytes
    msg = f"obj is an unsupported type = '{type(obj)}'"
    if isinstance(obj, str):
        in_stream = io.BytesIO(obj.encode(encoding))
    elif isinstance(obj, (bytes, bytearray)):
        in_stream = io.BytesIO(obj)
    elif hasattr(obj, "read"):
        if not isinstance(obj, (io.BytesIO, io.BufferedReader)):
            raise TypeError(msg)
        in_stream = obj
    else:
        raise TypeError(msg)
    bytes_read = 0
    bytes_printed = 0
    line_address = 0
    bytes_per_line, line_length  = 16, 41
    Print = partial(print, file=o, end="")
    # Correct for the offset
    if offset:
        in_stream.read(offset)
        bytes_read = offset
        line_address = offset
    data = in_stream.read(bytes_per_line)   # First line of data
    while data:
        bytes_read = len(data)
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
        s = ''.join(line)
        if asc and (len(s) < line_length):
            s += " "*(line_length - len(s))
        Print(s)
        # Add ASCII decode
        if asc:
            if truncated:
                data = data[:i + 1]
            Print(data.translate(hexdump.tt).decode("ASCII"))
        Print("\n")
        if length and bytes_printed >= length:
            break
        data = in_stream.read(bytes_per_line)   # Next line
    # We're done
    if out is None:
        return o.getvalue()
if __name__ == "__main__": 
    from lwtest import run, assert_equal, raises
    from io import StringIO
    from pdb import set_trace as xx 
    def Test():
        s = "abc"
        t = hexdump(s)
        e = "00000000: 6162 63                                  abc\n"
        assert(t == e)
        # Test out
        o = StringIO()
        t = hexdump(s, out=o)
        u = o.getvalue()
        assert(u == e)
        # Test offset
        t = hexdump(s, offset=1)
        e = "00000001: 6263                                     bc\n"
        assert(t == e)
        # Test length
        t = hexdump(s, length=2)
        e = "00000000: 6162                                     ab\n"
        assert(t == e)
        # Test asc
        t = hexdump(s, asc=False)
        e = "00000000: 6162 63\n"
        assert(t == e)
    exit(run(globals(), halt=1)[0])
