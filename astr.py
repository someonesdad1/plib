"""
Derived string class to allow embedded ANSI escape sequences used for
color-coding to not add to the string's length.

Example:
    s = astr("^[[00mtags^[[0m")
    print(len(s))

produces 4, the length of 'tags'.

You can instead use the function alen() to get the length of strings with
ANSI escape codes in them.

----------------------------------------------------------------------

NOTE:  The algorithm used below is to remove ANSI color-coding strings
before calculating the length.  The regular expression used to do this may
or may not be the most general, as the Wikipedia page is poorly written and
the ECMA standard is too annoyingly complicated for me to want to wade
through it.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # <programming> String class that ignores length of escape
    # sequences.  This lets you position strings on the page that are
    # colored without regard to the extra escape code information.
    ##∞what∞#
    ##∞test∞# run #∞test∞#
    pass
if 1:  # Imports
    import re


class astr(str):
    """This is a string object that uses a regular expression to remove
    ANSI color-coding strings before calculating the string length.
    """

    # This regexp replaces each color-coding escape sequence with the empty
    # string.  See https://en.wikipedia.org/wiki/ANSI_escape_code.
    r = re.compile(r"\x1b\[[0-?]*[ -\/]*[@-~]")

    def __len__(self):
        return len(astr.r.sub("", str(self)))


# Use the alen() function to get the string's length instead if you don't
# want to instantiate an astr object.


def alen(s):
    return len(astr.r.sub("", s))


if __name__ == "__main__":
    from lwtest import run, raises, assert_equal

    # Note the Unicode '∞' in the third line.
    tststring = """[1;37;42mstring1[0m
string2
[1;36mstring3∞[0m"""

    def Test_len():
        for i, s in enumerate(tststring.split("\n")):
            a = astr(s)
            if i in (0, 1):
                assert_equal(len(a), 7)
                assert_equal(alen(s), 7)
            else:
                assert_equal(len(a), 8)
                assert_equal(alen(s), 8)

    failed, messages = run(globals())
    exit(failed)
