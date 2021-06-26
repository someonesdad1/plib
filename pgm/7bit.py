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
    from get import GetLines
if 1:   # Global variables
    control_chars = {
        0:"nul", 1:"soh", 2:"stx", 3:"etx", 4:"eot", 5:"enq", 6:"ack", 7:"bel",
        8:"bs", 9:"ht", 10:"nl", 11:"vt", 12:"ff", 13:"cr", 14:"so", 15:"si",
        16:"dle", 17:"dc1", 18:"dc2", 19:"dc3", 20:"dc4", 21:"nak", 22:"syn",
        23:"etb", 24:"can", 25:"em", 26:"sub", 27:"esc", 28:"fs", 29:"gs",
        30:"rs", 31:"us",
    }
def RemoveASCII(s):
    '''Return True if the string s has a non-ASCII character in it.
    '''
    if not hasattr(RemoveASCII, "func"):
        # Create a dictionary for str.translate to remove ASCII
        # characters.
        mapping = {}
        for i in range(0x20, 0x80):
            mapping[i] = None
        # Also remove whitespace characters
        for i in (9, 10, 11, 12, 13):
            mapping[i] = None
        RemoveASCII.func = lambda s: s.translate(mapping)
    return bool(RemoveASCII.func(s))

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
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def ParseCommandLine(d):
    d["-c"] = False     # Use linenum:col format
    d["-l"] = False     # Only print the filename
    d["-w"] = False     # Wrap lines
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "clw")
    except getopt.GetoptError as str:
        msg, option = str
        Error(msg)
    for o, a in optlist:
        if o[1] in list("clw"):
            d[o] = not d[o]
    if not args:
        Usage()
    return args
def Codepoint(c):
    '''Return a hex string representing the codepoint.  The string will 
    be 9 characters long.
    '''
    if c > 0xffff:
        h = f"U+{c:05x}:"
    else:
        h = f"U+{c:04x}:"
    return f"{h:9s}"
def ProcessLine(line, file, linenum, nonascii, d):
    for i, c in enumerate(line):
        if not (0x20 <= ord(c) < 0x80):
            ln = f"{linenum}:{i + 1}" if d["-c"] else f"{linenum}"
            nonascii[ord(c)].append(ln)
def Header(c):
    '''Return a header string of the form e.g.
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
def ProcessFile(file, d):
    # Dictionary to keep track of non-ASCII characters found
    nonascii = defaultdict(list)
    try:
        for linenum, line in enumerate(GetLines(file)):
            if RemoveASCII(line):
                if d["-l"]: 
                    print(file)
                    return
                ProcessLine(line, file, linenum + 1, nonascii, d)
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
    except Exception as e:
        print(f"{file}:  {str(e)}", file=sys.stderr)
if __name__ == "__main__":
    d = {}
    files = ParseCommandLine(d)
    for file in files:
        ProcessFile(file, d)
