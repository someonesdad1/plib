'''
Remove blank lines from python scripts
    I use this tool in combination with the black formatter to format my
    python code.  I use 'black -S -l 75' followed by this script to remove
    the blank lines between functions/methods.  This is to get the most
    code possible in an editor window, as vertical real estate is the most
    precious.
'''
 
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <utility> Remove blank lines from python scripts
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Standard imports
    import getopt
    import os
    import pathlib
    import sys
    import tokenize as T
    from io import BytesIO
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [file1 [file2...]]
          Remove blank lines from python scripts.  Leaves multiline strings
          and comments alone.  The files are modified in place.
        Options:
            -n      Dry run:  show files that will be modified
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-n"] = False     # Dry run:  show what files will be modified
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hn")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("n"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args
if 1:   # Core functionality
    pass
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    ''' 
    How to do this:

    Put this in a file a.py
        if 1:   # Imports
            import time

        a = 7

    Then run 'p -m tokenize a.py' and capture output.   This is what you
    get:

        0,0-0,0:            ENCODING       'utf-8'        
        1,0-1,2:            NAME           'if'           
        1,3-1,4:            NUMBER         '1'            
        1,4-1,5:            OP             ':'            
        1,8-1,17:           COMMENT        '# Imports'    
        1,17-1,18:          NEWLINE        '\n'           
        2,0-2,4:            INDENT         '    '         
        2,4-2,10:           NAME           'import'       
        2,11-2,15:          NAME           'time'         
     *  2,15-2,16:          NEWLINE        '\n'           
     *  3,0-3,1:            NL             '\n'           
        4,0-4,0:            DEDENT         ''             
        4,0-4,1:            NAME           'a'            
        4,2-4,3:            OP             '='            
        4,4-4,5:            NUMBER         '7'            
        4,5-4,6:            NEWLINE        '\n'           
        5,0-5,0:            ENDMARKER      ''             

    Note the pattern NEWLINE followed by NL.  This is the clue where a
    double line exists.  Clearly, line 3 needs to be removed.
    '''

    # See u.py for tokenizing stuff
    lines = open(args[0]).readlines()
    for line in lines:
        s = BytesIO(line.encode("UTF-8")).readline
        g = T.tokenize(s)
        print(line, end="")
        for toknum, tokval, _, _, _ in g:
            print("  ", toknum, tokval)
