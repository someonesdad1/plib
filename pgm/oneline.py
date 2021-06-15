'''
Read in stdin as a string, remove all newlines, and change to a
one-space separated list of names.  Escape embedded space characters.
Use case:  put all the lines from stdin onto one line for subsequent
call to a command line function.  Note bash does this readily enough,
but this might be of use for old Bourne shells.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Read in stdin as a string, remove all newlines, and change to a
    # one-space separated list of names.  Escape embedded space
    # characters.  Use case:  put all the lines from stdin onto one line
    # for subsequent call to a command line function.
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
if __name__ == "__main__": 
    # Get lines from files passed on command line or stdin
    lines = []
    if len(sys.argv) > 1:
        for file in sys.argv[1:]:
            lines += [i.strip() for i in open(filename).readlines()]
            lines.append(open(file).read())
    else:
        lines = [sys.stdin.read()]
    # Escape embedded spaces
    print(' '.join(lines).replace(" ", "\\ "))
