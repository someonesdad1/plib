# encoding: utf-8

import sys
from astr import astr, alen
from lwtest import run, assert_equal, raises

from pdb import set_trace as xx 
py2 = sys.version_info[0] == 2

# Note the Unicode '∞' in the third line.
tststring = '''[1;37;42mstring1[0m
string2
[1;36mstring3∞[0m'''

def Test_len():
    for i, s in enumerate(tststring.split("\n")):
        a = astr(s)
        if i in (0, 1):
            assert_equal(len(a), 7)
            assert_equal(alen(s), 7)
        else:
            if py2:
                assert_equal(len(a), 10)
                assert_equal(alen(s), 10)
            else:
                assert_equal(len(a), 8)
                assert_equal(alen(s), 8)

if __name__ == "__main__":
    failed, messages = run(globals())
    exit(failed)
