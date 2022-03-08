'''
Module to find empty lines in a bytes stream
    Example of use on a python file:
        file = "pythonfile.py"
        bytes_stream = open(file, "rb")
        empty_lines = GetEmptyLineList(bytes_stream)
        print(empty_lines)
'''
# On my older Windows machine, this tokenizer runs at around 25
# klines/second. 
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <programming> Returns a list of 1-based line numbers of empty lines
    # in a bytes stream.
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Standard imports
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
def GetEmptyLines(bytes_stream, debug=None):
    '''Return a tuple of 1-based line numbers that python's tokenizer
    considers empty lines.  An empty line can contain one or more
    whitespace characters in string.whitespace except for the vertical
    tab.  Empty lines inside multiline strings are not considered empty.
    The stream will be closed at exit.  If debug is not None, it must be a
    stream; write the token information to this stream.
 
    When the tokenizer raises an exception, the python script probably has
    a syntax error; find the offending line by running the script.
    '''
    # Tokenize the file.  If you are interested in learning how this is
    # done, run 'python -m tokenize' on a file and see how the tokenize
    # module does this.
    with bytes_stream as s:
        tokens = deque(tokenize(s.readline))
    # Make container have (linenumber, token_name) entries where
    # token_name is either item or nl (for a newline).
    item, nl = "ITEM", "NL"
    Entry = namedtuple("Entry", "linenumber name".split())
    container = deque()
    while tokens:
        token = tokens.popleft()
        linenumber = token.start[0]  # 1-based line number
        name = nl if token.type in (4, 56) else item
        e = Entry(linenumber, name)
        if debug:
            # Send the line number and token string to debug stream
            msg = f"{token.start[0]}: "
            msg += f"{tok_name[token.type]} "
            s = token.string
            t = s if s != "\n" else '"\\n"'
            msg += f"{t}\n"
            debug.write(msg)
        container.append(e)
    # Toss out ITEM/NL pairs using a state machine.  Left over NL items are
    # blank line candidates.  Later, the line is only removed if it is
    # truly empty.
    blanklines, last, candidate = deque(), None, False
    while container:
        e = container.popleft()
        if e.name == item:
            last, candidate = item, False
            continue
        elif e.name == nl:
            if candidate:
                blanklines.append(e.linenumber)  # Save line number
            else:
                if last == item:
                    candidate = True
                    continue
    return tuple(blanklines)
if 0:
    s = open("toks")
    from pprint import pprint as pp
    pp(dir(s))
    print(type(s))
    help(s)
    exit()
if __name__ == "__main__": 
    # Run a basic test case
    from textwrap import dedent
    from io import BytesIO
    from lwtest import Assert
    # Note the stream doesn't have to contain syntactically-correct python;
    # it's only being tokenized.
    s = dedent("""
    '''
    Arbitrary text
    '''
    if 1:  # A comment
    # Comment with a blank line
  
    # Comment with a blank line
 
    import os
 
    a = kjdf kdf jdkieoroj dfkuj
    print(a)
    """.rstrip()[1:])
    stream = BytesIO(s.encode())
    ln = GetEmptyLines(stream)
    Assert(ln == (6, 8, 10))