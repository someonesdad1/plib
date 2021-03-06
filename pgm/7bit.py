'''
Find non-7-bit characters in files
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014, 2018 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Find non-7-bit characters in files
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import os
    import sys
    import traceback
    import textwrap
    from collections import defaultdict
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    if 0:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    control_chars = {
        0:"nul", 1:"soh", 2:"stx", 3:"etx", 4:"eot", 5:"enq", 6:"ack", 7:"bel",
        8:"bs", 9:"ht", 10:"nl", 11:"vt", 12:"ff", 13:"cr", 14:"so", 15:"si",
        16:"dle", 17:"dc1", 18:"dc2", 19:"dc3", 20:"dc4", 21:"nak", 22:"syn",
        23:"etb", 24:"can", 25:"em", 26:"sub", 27:"esc", 28:"fs", 29:"gs",
        30:"rs", 31:"us",
    }
if 1:   # Utility
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        name = sys.argv[0]
        print(dedent(f'''
        Usage:  {name} [options] file1 [file2 ...]
            Show the non-ASCII characters in the files by character with the line
            numbers that character occurs on.  Column and line numbers are 1-based.
            Whitespace is ignored.
        Options
            -c  Show column numbers too with line_number:column_number format.
            -l  Just print out the file name if a non-ASCII character is found.
            -w  Wrap lines to make easier to read.
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = False     # Use linenum:col format
        d["-l"] = False     # Only print the filename
        d["-w"] = False     # Wrap lines
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "chlw")
        except getopt.GetoptError as str:
            msg, option = str
            Error(msg)
        for o, a in optlist:
            if o[1] in list("clw"):
                d[o] = not d[o]
            elif o == "-h":
                Usage(0)
        if not args:
            Usage()
        return args
if 1:   # Core functionality
    def Codepoint(c):
        '''Return a hex string representing the codepoint.  The string will 
        be 9 characters long.
        '''
        h = f"U+{c:05x}:" if c > 0xffff else f"U+{c:04x}:"
        return f"{h:9s}"
    def RemoveASCII(s):
        'Return True if the string of bytes s has a non-ASCII character in it'
        # Create a str.translate tool in RemoveASCII.func to remove the
        # ASCII characters in a string.
        if not hasattr(RemoveASCII, "func"):
            delete = ""
            for i in range(0x20, 0x80):
                delete += f"{i:02x}"
            # Also remove whitespace characters
            for i in (9, 10, 11, 12, 13):
                delete += f"{i:02x}"
            delete = bytes.fromhex(delete)
            RemoveASCII.func = lambda s: s.translate(None, delete)
        return bool(RemoveASCII.func(s))
    def Header(c):

        '''c is an integer from 0 to 255.  Return a header string of the
        form e.g.
            ' ∞  U+221e:'
            --- ------
            a    b
        where a is the 3-character string representing the non-ASCII
        character (either the Unicode character or e.g. 'esc' for the escape
        character) and b is the Unicode codepoint form.
        '''
        char = control_chars[c] if c in control_chars else chr(c)
        cp = Codepoint(c)
        return f"  {char:^3s} {cp}"
    def GetLines(file):
        '''Read the data in from the file as binary.  Split on newlines and
        return the list of byte strings representing each line.
        '''
        return open(file, "rb").read().split(b'\n')
    def ProcessLine(line, file, linenum, nonascii):

        '''For the line of the indicated file (line is a bytes object),
        find any bytes that are not 7-bit ASCII characters and put them
        into the dict nonascii.  nonascii is keyed by the non-7-bit
        character and each value is a list of the file and line number
        where the offending byte was found.

        '''
        for i, c in enumerate(line):
            if not (0x20 <= c < 0x80):
                # d["-c"] means to show column numbers too
                value = f"{linenum}:{i + 1}" if d["-c"] else f"{linenum}"
                nonascii[c].append(value)
    def ProcessFile(file, d):
        # Dictionary to keep track of non-ASCII bytes found
        nonascii = defaultdict(list)
        for linenum, line in enumerate(GetLines(file)):
            if RemoveASCII(line):
                if d["-l"]: 
                    print(file)
                    return
                ProcessLine(line, file, linenum + 1, nonascii)
        if nonascii:
            print(file)
            for c in sorted(nonascii):
                header = Header(c)
                linenumbers = ' '.join(nonascii[c])
                if d["-w"]:
                    # Wrap line numbers so they are easily readable.
                    # The lines must be indented 16 characters.
                    cols = int(os.environ["COLUMNS"])
                    width = cols - 16 - 1
                    lines = textwrap.wrap(linenumbers, width=width)
                    print(f"{Header(c)}", end="")
                    for i, line in enumerate(lines):
                        if i:
                            print(f"{' '*15}{line}")
                        else:
                            print(line)
                else:
                    print(f"{Header(c)}{linenumbers}")
if __name__ == "__main__":
    d = {}
    files = ParseCommandLine(d)
    for file in files:
        ProcessFile(file, d)
