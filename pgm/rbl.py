'''
Remove blank lines from python scripts
    I use this tool in combination with the black formatter to format my
    python code.  I use 'black -S -l 75' followed by this script to remove
    the blank lines between functions/methods.
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
    # <utility> Removes empty lines from python scripts; writes back to the
    # file in place.
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Standard imports
    from io import BytesIO
    from collections import deque, namedtuple
    from token import tok_name
    from tokenize import tokenize
    import getopt
    import os
    import pathlib
    import sys
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

          Remove empty lines from python files.  The files are modified in
          place.  Use "-" as a file to process stdin and print its
          processed data to stdout.

          Note:  an empty line is determined by python's tokenizer.  A line
          containing space, tab, linefeed, return, or formfeed characters
          is considered emtpy.

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
    class RemoveEmptyLines:
        '''Machinery to remove empty lines from a file.  An empty line is
        one that contains only whitespace.
        Usage:
            rbl = RemoveEmptyLines(file)    # Tokenizes the file 
            bool(rbl)   --> True means there are blank lines to remove
            rbl.fix()   --> Removes blank lines and writes file
        '''
        # If the following class variable is True, then any line with only
        # whitespace on it is considered a blank line.  Thus, if
        # remove_blank_lines is True, a line is removed if line.strip() is
        # empty.  Otherwise, the line must be truly empty to be removed.
        remove_blank_lines = False
        def __init__(self, file, ws_is_empty=False):
            '''file is either a pathlib.Path object or "-" for stdin.  If
            ws_is_empty is True, then a line with any whitespace on it is
            considered empty.
            '''
            if file != "-":
                if not file.exists() and not file.is_file():
                    raise ValueError(f"'{file}' is bad file")
            self.file = file
            self.lines = self.FindBlankLines()
        def FindBlankLines(self):
            '''Return a list of integers representing the line numbers s
            that are blank (1-based numbering).  
            '''
            # Tokenize the file.  If you are interested in learning how
            # this is done, first run 'python -m tokenize' on a file and
            # see how the tokenize module does this.
            if self.file == "-":
                s = sys.stdin.read()            # Read stdin as a string
                stream = BytesIO(s.encode())    # Make it a bytes stream
                with BytesIO(s.encode()) as f:
                    tokens = deque(tokenize(f.readline))
            else:
                with open(self.file, 'rb') as f:
                    tokens = deque(tokenize(f.readline))
            # Make container have (linenumber, token_name) entries where
            # token_name is either ITEM or NL (for a newline).
            Entry = namedtuple("Entry", "n name".split())
            container = deque()
            while tokens:
                token = tokens.popleft()
                n = token.start[0]  # 1-based line number
                name = "NL" if token.type in (4, 56) else "ITEM"
                e = Entry(n, name)
                container.append(e)
                #print(e) #xx
            # Toss out ITEM/NL pairs using state machine.  Left over NL
            # items are blank line candidates.  Later, the line is only
            # removed if it is truly empty.
            blanklines = deque()
            last = None
            candidate = False
            while container:
                e = container.popleft()
                if e.name == "ITEM":
                    last = "ITEM"
                    candidate = False
                    continue
                elif e.name == "NL":
                    if candidate:
                        blanklines.append(e.n)  # Save line number
                    else:
                        if last == "ITEM":
                            candidate = True
                            continue
            blanklines = list(blanklines)
            # The list blanklines is now the list of blank lines
            print(' '.join([str(i) for i in blanklines]))
if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        rbl = RemoveEmptyLines(P(file) if file != "-" else "-")
