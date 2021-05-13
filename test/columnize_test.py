import sys
from columnize import Columnize
from lwtest import run, assert_equal, raises
from pdb import set_trace as xx

nl = "\n"

def TestBasicBehavior():
    strings = ["12345678"]*30
    result = Columnize(strings, width=80, col_width=9)
    # Construct expected result
    e = ["12345678  "]
    row = ''.join(e*8).rstrip()
    expected = [row]*3 + [''.join(e*6).rstrip()]
    # Check they're the same
    assert(result == expected)

def TestHoriz():
    seq = [str(i) for i in range(32)]
    result = Columnize(seq, width=20, columns=4, horiz=False)
    expected = [i.lstrip() for i in '''
        0    8    16   24
        1    9    17   25
        2    10   18   26
        3    11   19   27
        4    12   20   28
        5    13   21   29
        6    14   22   30
        7    15   23   31
'''[1:-1].split(nl)]
    assert(result == expected)
    result = Columnize(seq, width=20, columns=4, horiz=True)
    s = '''
        0    1    2    3
        4    5    6    7
        8    9    10   11
        12   13   14   15
        16   17   18   19
        20   21   22   23
        24   25   26   27
        28   29   30   31
'''[1:-1]
    expected = [i.lstrip() for i in s.split(nl)]
    assert(result == expected)
    # Now check that we can use the to_string keyword to get a string
    # equivalent.
    string = result = Columnize(seq, width=20, columns=4, horiz=True,
        to_string=True)
    assert(string == nl.join(expected))

def TestIdentityXfm():
    seq = [str(i) for i in range(12)]
    result = Columnize(seq, ignore=True)
    assert(seq == result)

def TestSeparator():
    seq = [str(i) for i in range(12)]
    result = Columnize(seq, width=12, columns=4, sep="|")
    expected = [i.lstrip() for i in '''
        0 |3 |6 |9
        1 |4 |7 |10
        2 |5 |8 |11
'''[1:-1].split(nl)]
    assert(result == expected)

def TestIndent():
    seq = [str(i) for i in range(12)]
    result = Columnize(seq, width=18, columns=4, indent="xxx")
    expected = [i.lstrip() for i in '''
        xxx0   3   6   9
        xxx1   4   7   10
        xxx2   5   8   11
'''[1:-1].split(nl)]
    assert(result == expected)

def TestTruncation():
    seq = [str(i) for i in range(12)]
    result = Columnize(seq, col_width=1, columns=4, trunc=True)
    expected = [i.lstrip() for i in '''
        0 3 6 9
        1 4 7 1
        2 5 8 1
'''[1:-1].split(nl)]
    assert(result == expected)

def TestAlignment():
    seq = [str(i) for i in range(12)]
    result = Columnize(seq, col_width=10, columns=4, sep="|")
    expected = [i.lstrip() for i in '''
        0         |3         |6         |9
        1         |4         |7         |10
        2         |5         |8         |11
'''[1:-1].split(nl)]
    assert(result == expected)
    # Show this is the same as left alignment
    result = Columnize(seq, col_width=10, columns=4, sep="|", align="left")
    assert(result == expected)
    result = Columnize(seq, col_width=10, columns=4, sep="|", align="<")
    assert(result == expected)
    # Centered
    result = Columnize(seq, col_width=10, columns=4, sep="|", align="^")
    expected = [i for i in '''
    0     |    3     |    6     |    9
    1     |    4     |    7     |    10
    2     |    5     |    8     |    11
'''[1:-1].split(nl)]
    assert(result == expected)
    result = Columnize(seq, col_width=10, columns=4, sep="|", align="center")
    assert(result == expected)
    # Right-aligned
    result = Columnize(seq, col_width=10, columns=4, sep="|", align=">")
    expected = [i for i in '''
         0|         3|         6|         9
         1|         4|         7|        10
         2|         5|         8|        11
'''[1:-1].split(nl)]
    assert(result == expected)
    result = Columnize(seq, col_width=10, columns=4, sep="|", align="right")
    assert(result == expected)

if __name__ == "__main__":
    exit(run(globals())[0])
