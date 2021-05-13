from lwtest import run
from brace import BraceExpansion
from itertools import product
from pdb import set_trace as xx


def TestSimple():
    s = ' '.join(BraceExpansion("a{d,c,b}e"))
    t = "ade ace abe"
    assert(s == t)

def TestCartesianProduct():
    s = ' '.join(BraceExpansion("{a,b,c}{d,e,f}"))
    t = ' '.join([i + j for i, j in product("abc", "def")])
    assert(s == t)
    s = str(BraceExpansion("{a,b}/*.{jpg,png}"))
    t = "['a/*.jpg', 'a/*.png', 'b/*.jpg', 'b/*.png']"
    assert(s == t)

def TestNested():
    s = ' '.join(BraceExpansion("{,a}{b,{c,d},e}"))
    t = "b c d e ab ac ad ae"
    assert(s == t)

if __name__ == "__main__":
    run(globals())
