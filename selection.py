'''
Module to provide Select(), a function to help a user select a set of
integers.
'''

from lwtest import run, raises, assert_equal, Assert
from collections import deque
ii = isinstance

def Select(user_input, seq_of_integers):
    '''Given the user's input string, find the integers in the string that
    are in the sequence seq_of_integers.  Returns the tuple (found,
    not_found) where found is the list of integers found and not_found is
    the list of integers or strings not found.  Note not_found can contain
    strings as when a string token in the user_input doesn't represent an
    integer.
 
    user_input is split on whitespace after replacing ',' and ';' by space
    characters.  Then it must contain only valid integer strings or either 
    "n-m" or "n:m:q" where n, m, and q are integers.
 
        n-m     Represents the sequence [n, n+1, ..., m-1, m].
        n:m:q   Represents list(range(n, m, q))
 
    Example:  Select("1 2-4 6:9:2", range(12)) 
        The seq_of_integers is (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12).
        The string represents  (   1, 2, 3, 4,    6,    8), so the returned
        tuples are
            found = (1, 2, 3, 4, 6, 8)
            not_found = (0, 5, 7, 9, 10, 11, 12)
    '''
    Assert(ii(user_input, str))
    int_set = set(seq_of_integers)

    found, not_found = set(), set()
    s = user_input.strip()
    if not s:
        return [], []
    # Change ',' and ';' to space characters
    for i in ",;":
        s = s.replace(i, " ")
    # Process the items in user_input
    for item in s.split():
        # item will be:  1) plain int, 2) a-b sequence, 3) a:b range sequence
        try:
            x = int(item)
            isint = True
        except Exception:
            isint = False
        if isint:
            found.add(x)
        elif ":" in item:   # It's a range form
            try:
                found.update(Form2(item))
            except Exception:
                not_found.add(item)
        else:               # It's an a-b form
            try:
                found.update(Form1(item))
            except Exception:
                not_found.add(item)
    # Categorize the output
    out = set()
    for i in found:
        Assert(ii(i, int))
        if i in int_set:
            out.add(i)
        else:
            not_found.add(i)
    out = list(sorted(out))
    not_found = list(sorted(not_found))
    print("xx", list(sorted(int_set)))
    return out, not_found

if 1:
    def Form1(string):
        '''This is where the string contained "-" but no ":".  Unusual
        forms like "-8--3", "-8-3", "-3--8" need to be handled.  The
        method used is to convert these expressions to a suitable range()
        statement.
        '''
        # Check string
        Assert(len(string) > 2)     # Need 3 or more characters
        S = set(string)
        Assert("-" in S)
        Assert(":" not in S)
        Assert(S <= set("0123456789-"))
        # Split into two strings on "-"
        c = string[0]
        s0, s1 = string[1:].split("-", 1) if c == "-" else string.split("-", 1)
        s0 = "-" + s0 if c == "-" else s0
        # Convert to integers
        try:
            n0, n1 = int(s0), int(s1)
        except Exception as e:
            raise ValueError(f"{string!r}:  got exception:\n {e}")
        if n0 > n1:
            n0, n1 = n1, n0
        n1 += 1     # Include endpoint unlike range()
        return list(range(n0, n1))
    def Form2(string):
        'string contained ":"'
        Assert(":" in string)
        n = string.count(":")
        Assert(n in (1, 2))
        step = 1
        if n == 2:
            start, stop, step = string.split(":")
        else:
            start, stop = string.split(":")
        try:
            start, stop, step = [int(i) for i in (start, stop, step)]
        except Exception as e:
            raise ValueError(f"{string!r}:  got exception:\n {e}")
        if not step :
            raise ValueError(f"{string!r}:  step is zero")
        if start > stop and step > 0:
            raise ValueError(f"{string!r}:  positive step won't terminate sequence")
        if start < stop and step < 0:
            raise ValueError(f"{string!r}:  negative step won't terminate sequence")
        return list(range(start, stop, step))

if 0:   # Test
    if 1:
        f, z = Form1, [0]
        Assert(f("1-3") == [1, 2, 3])
        Assert(f("3-1") == [1, 2, 3])
        Assert(f("-1--3") == [-3, -2, -1])
        Assert(f("-3--1") == [-3, -2, -1])
        Assert(f("-3-2") == [-3, -2, -1, 0, 1, 2])
        Assert(f("2--3") == [-3, -2, -1, 0, 1, 2])
        Assert(f("2-2") == [2])
        Assert(f("-2--2") == [-2])
        Assert(f("0-0") == z)
        Assert(f("-0--0") == z)
        # Need length of 3
        for i in ("", " ", "  "):
            raises(AssertionError, f, i)
        raises(AssertionError, f, "111")    # No "-"
        raises(AssertionError, f, "11:")    # Can't contain ":"
        raises(AssertionError, f, "a11-")   # Can't contain non-digit
        raises(ValueError, f, "1---2")      # Bad int
    if 0:
        f, mt = Form2, []
        Assert(f("1:3") == [1, 2])
        Assert(f("3:1:-1") == [3, 2])
        Assert(f("-1:-3:-1") == [-1, -2])
        Assert(f("-3:-1") == [-3, -2])
        Assert(f("-3:2") == [-3, -2, -1, 0, 1])
        Assert(f("2:-3:-1") == [2, 1, 0, -1, -2])
        Assert(f("2:2") == mt)
        Assert(f("-2:-2") == mt)
        Assert(f("0:0") == mt)
        Assert(f("-0:-0") == mt)
        # Need length of 3
        for i in ("", " ", "  "):
            raises(AssertionError, f, i)
        # 
        raises(AssertionError, f, "111")    # No ":"
        raises(AssertionError, f, ":::")    # Too many ":"
        raises(ValueError, f, "a:1")        # Bad int
        raises(ValueError, f, "1:2:0")      # Zero step
        raises(ValueError, f, "3:1:1")      # Nonconverging
        raises(ValueError, f, "1:3:-1")     # Nonconverging
    exit()

if 1:   # Test
    print(Select("14 1-3 5:10:2", range(15)))
    exit()

if __name__ == "__main__":  
    from lwtest import run, assert_equal, raises
    def Test():
        s = range(20)
        t = "2:10:2 21 88 12-13,14"
        found, not_found = Select(t, s)
        assert(found == [2, 4, 6, 8, 12, 13, 14])
        assert(not_found == [21, 88])
    def Test_corner():
        found, not_found = Select("", [])
        assert(not found)
        assert(not not_found)
        found, not_found = Select("", range(20))
        assert(not found)
        assert(not not_found)
        found, not_found = Select("100 101 102", range(20))
        assert(not found)
        assert(not_found == [100, 101, 102])
    def Test_negative():
        s = [-1, 0, 1, 2]
        t = "-1 3"
        found, not_found = Select(t, s)
        assert(found == [-1])
        assert(not_found == [3])
    def Test_large():
        n = 1000000
        s = range(n)
        t = [str(i) for i in range(n - 10, n + 11)]
        found, not_found = Select(' '.join(t), s)
        assert(found == list(range(n - 10, n)))
        assert(not_found == list(range(n, n + 11)))
    if __name__ == "__main__":
        exit(run(globals(), halt=True)[0])
