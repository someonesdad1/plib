"""
Quantifies how different two strings or bytestrings are
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # <programming> Quantifies how different two equal-sized strings or
    # bytestrings are.
    ##∞what∞#
    ##∞test∞# run #∞test∞#
    pass
if 1:  # Standard imports
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
    from f import flt
if 1:  # Core functionality

    def DiffFrac(seq1, seq2):
        """Return a decimal fraction on [0, 1] that represents how different
        the two sequences of characters or bytes are.   The fraction is
        produced by counting the number of elements (bytes or characters) that
        differ and dividing by n.  The fraction is a number in the sequence
        [0/n, 1/n, 2/n, ..., n/n] where n is the number of elements.
        """
        if 1:  # Check inputs
            e = TypeError("seq1 and seq2 are not the same type")
            if isinstance(seq1, str):
                is_string = True
                if not isinstance(seq2, str):
                    raise e
            elif isinstance(seq1, bytes):
                is_string = False
                if not isinstance(seq2, bytes):
                    raise e
            else:
                raise TypeError("Arguments must be strings or bytes")
            n = len(seq1)
            if not n == len(seq2):
                raise ValueError("Arguments are not the same length")
        if 1:  # Do calculation
            # Note:  more resolution can be gotten by changing 'bool' to
            # 'abs'.  However, you can then get fractions > 1, so you'll
            # want to divide by 255 for byte strings and e.g. the number of
            # Unicode characters for strings.  You'll also need to change
            # the algorithm in DiffNum().  Personally, I can't see any
            # practical utility in such a change.
            different_item_count = 0
            for item1, item2 in zip(seq1, seq2):
                if is_string:
                    different_item_count += bool(ord(item1) - ord(item2))
                else:
                    different_item_count += bool(item1 - item2)
            frac = flt(different_item_count / n)
            if not (0 <= frac <= 1):
                msg = f"Calculation bug:  frac = {frac} is not on [0, 1]"
                raise Exception(msg)
            return frac

    def DiffDigit(frac, n, how_many=9):
        """Returns a decimal digit from '0' to '9' representing how
        different two sequences were.  '0' represents no difference and '9'
        represents the maximum number of differences possible.  You can get
        higher "resolution" using a larger number for how_many and
        additional Unicode characters will be returned as needed.  If you
        just want '0' for equal and '1' for unequal, use how_many set to 2.
        """
        # Check arguments
        if not 0 <= frac <= 1:
            raise ValueError("frac must be on [0, 1]")
        if not isinstance(n, int) and n > 0:
            raise ValueError("n must be an integer > 0")
        if not isinstance(how_many, int) and how_many < 2:
            raise ValueError("how_many must be an integer > 1")
        if how_many > 0x23539 - ord("0"):
            # From https://en.wikipedia.org/wiki/List_of_Unicode_characters
            # for Unicode 14.  If you get this exception, you're probably
            # being doing something you don't need to do.
            raise UnicodeError("how_many is too large")
        # No checking for ridiculously large values of how_many is made.
        # Calculate
        base = ord("0")
        if not frac:
            return chr(base)
        i = int((how_many - 1) * frac) + 1
        assert 1 <= i <= how_many
        return chr(base + i)


if __name__ == "__main__":
    from lwtest import run, Assert, raises

    def Test():
        n = 9
        # Test for bytestrings
        std = b"a" * n
        for i in range(1, n + 1):
            s = b"b" * i + b"a" * (n - i)
            assert len(s) == n
            frac = DiffFrac(std, s)
            t = DiffDigit(frac, n)
            Assert(t == str(i))
        # Test for strings
        std = "a" * n
        for i in range(1, n + 1):
            s = "b" * i + "a" * (n - i)
            assert len(s) == n
            frac = DiffFrac(std, s)
            t = DiffDigit(frac, n)
            Assert(DiffDigit(frac, n) == str(i))
        # Check we get the expected exceptions
        raises(TypeError, DiffFrac, "a", b"a")
        raises(TypeError, DiffFrac, b"a", "a")
        raises(ValueError, DiffFrac, "a", "aa")
        raises(ValueError, DiffFrac, b"a", b"aa")

    def TestHowmany():
        n = 20
        frac = DiffFrac("a" * n, "b" * n)
        t = DiffDigit(frac, n, how_many=10)
        Assert(t == ":")

    exit(run(globals(), halt=1)[0])
