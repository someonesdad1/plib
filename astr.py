'''
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
'''

import re
import sys

py3 = sys.version_info[0] == 3
if 0 and not py3:
    # The algorithm won't get correct string lengths for unicode strings
    # under python 2 (it apparently counts bytes instead of characters,
    # so the returned lengths will be too large for strings that contain
    # non-7-bit characters).
    raise RuntimeError("This module won't work under python 2")

class astr(str):
    '''This is a string object that uses a regular expression to remove
    ANSI color-coding strings before calculating the string length.
    '''
    # This regexp replaces each color-coding escape sequence with the empty
    # string.  See https://en.wikipedia.org/wiki/ANSI_escape_code.
    r = re.compile(r"\x1b\[[0-?]*[ -\/]*[@-~]")
    def __len__(self):
        return len(astr.r.sub("", str(self)))

# Use the alen() function to get the string's length instead if you don't
# want to instantiate an astr object.

def alen(s):
    return len(astr.r.sub("", s))
