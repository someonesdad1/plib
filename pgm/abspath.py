'''
Return the paths on the command line as an absolute paths
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
    # Return the paths on the command line as an absolute paths
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import pathlib
    import sys
    from pdb import set_trace as xx
if __name__ == "__main__": 
    if len(sys.argv) == 1:
        print("Need a path argument", file=sys.stderr)
        exit(1)
    out = []
    for file in sys.argv[1:]:
        p = pathlib.Path(file).resolve()
        out.append(p)
    print(' '.join([str(i) for i in out]))
