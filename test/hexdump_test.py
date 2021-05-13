from hexdump import hexdump as hd
from lwtest import run, assert_equal, raises
from io import StringIO
from pdb import set_trace as xx 

def Test():
    s = "abc"
    t = hd(s)
    e = "00000000: 6162 63                                  abc\n"
    assert(t == e)
    # Test out
    o = StringIO()
    t = hd(s, out=o)
    u = o.getvalue()
    assert(u == e)
    # Test offset
    t = hd(s, offset=1)
    e = "00000001: 6263                                     bc\n"
    assert(t == e)
    # Test length
    t = hd(s, length=2)
    e = "00000000: 6162                                     ab\n"
    assert(t == e)
    # Test asc
    t = hd(s, asc=False)
    e = "00000000: 6162 63\n"
    assert(t == e)

if __name__ == "__main__":
    run(globals())
