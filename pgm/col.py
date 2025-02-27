"""Fixup for cygwin man pages.  This allows you to get a plain ASCII
version of a man page.  There used to be a /bin/col command that you
used to use like 'col -b' or somesuch, but it's not there anymore and I
don't know what package contains it.  No matter, this is a quick hack
that gets mostly there.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Cygwin manpage fixup
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
if __name__ == "__main__":
    s = sys.stdin.read()
    # The following is used for the vertical pipe symbols
    s = s.replace("\xe2\x8e\xaa\x08\xe2\x8e\xaa", "|")
    # The following is for bulleted lists
    s = s.replace("\xc2\xb7", "*")
    # Underlining is done by e.g. _^HK_^Ho_^Hr_^Hn, so replace all occurrences
    # of _^H by the empty string.
    s = s.replace("_\x08", "")
    out = sys.stdout.write
    i = 0
    while i < len(s):
        c = s[i]
        if ord(c) == 0xE2:  # It's a hyphen, so swallow remainder to newline
            out("-")
            while c != "\n" and i < len(s):
                i += 1
                c = s[i]
        elif ord(c) == 0x08:  # Backspace
            i += 2
            continue
        out(c)
        i += 1
