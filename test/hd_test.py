import sys
from lwtest import run, assert_equal, raises
from hd import hexdump, StringIO

from pdb import set_trace as xx
if len(sys.argv) > 1:
    import debug
    debug.SetDebugger()

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
    assert_equal(t, s.strip())
    # Trying to dump an empty string returns an empty string
    assert_equal(hexdump(""), "")

def TestBoundaries():
    text = "abc"
    # Setting n to longer than the string should still work
    s = hexdump(text, n=2*len(text))
    t = "00000000  61 62 63                                          | abc\n"
    assert_equal(s, t)
    # Setting offset to longer than the string should return empty string
    s = hexdump(text, offset=2*len(text))
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
    text = u"abc±⧻"
    s = text.encode("utf-8")
    t = hexdump(s)
    e = ("00000000  61 62 63 c2 b1 e2 a7 bb                           "
         "| abc.....\n")
    assert_equal(t, e)

if __name__ == "__main__":
    exit(run(globals())[0])
