"""

- 26 Jul 2022: this worked under 3.7, but not under 3.9

Module to find empty lines in a bytes stream
    Example of use on a python file:
        file = "pythonfile.py"
        bytes_stream = open(file, "rb")
        empty_lines = GetEmptyLineList(bytes_stream)
        print(empty_lines)
"""

# On my older Windows machine, this tokenizer runs at around 25
# klines/second.
if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # <programming> Returns a list of 1-based line numbers of empty lines
    # in a bytes stream.
    ##∞what∞#
    ##∞test∞# run #∞test∞#
    # Standard imports
    from collections import deque, namedtuple
    from token import tok_name
    from tokenize import tokenize
    import getopt
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx

    # Custom imports
    from wrap import wrap, dedent
    from color import TRM as t

    # Global variables
    P = pathlib.Path
    ii = isinstance
    t.nl = t("ornl")
    t.cmt = t("magl")
    # Need to have version, as token numbers were changed between 3.7
    # and 3.9
    vi = sys.version_info
    ver = f"{vi[0]}.{vi[1]}"


def GetEmptyLines(bytes_stream, debug=None):
    """Return a tuple of 1-based line numbers that python's tokenizer
    considers empty lines.  An empty line can contain one or more
    whitespace characters in string.whitespace except for the vertical tab.
    Empty lines inside multiline strings are not considered empty nor are
    empty lines in between comments.  The stream will be closed at exit.
    If debug is not None, it must be a stream; write the token information
    to this stream.

    When the tokenizer raises an exception, the python script probably has
    a syntax error; find the offending line by running the script.
    """
    # Tokenize the file.  If you are interested in learning how this is
    # done, run 'python -m tokenize' on a file and see how the tokenize
    # module does this.
    with bytes_stream as s:
        tokens = deque(tokenize(s.readline))
    # Make container have (linenumber, token_name) entries where token_name
    # is either 'ITEM' (for anything but a newline), 'COMMENT', or 'NL'
    # (for a newline).
    Entry = namedtuple("Entry", "linenumber name".split())
    container = deque()
    nltokens = (4, 56)  # Known to work on python 3.7
    if ver == "3.9":
        nltokens = (4, 61)  # Known to work on python 3.7
    while tokens:
        token = tokens.popleft()
        linenumber = token.start[0]  # 1-based line number
        name = "NL" if token.type in nltokens else "ITEM"
        e = Entry(linenumber, name)
        if debug:
            # Send the line number and token string to debug stream
            if name == "NL":
                msg = f"{t.nl}"
            elif token.type == 60:  # Comment
                msg = f"{t.cmt}"
            else:
                msg = ""
            msg += f"{token.start[0]}: "
            msg += f"{tok_name[token.type]} (tt={token.type}) "
            s = token.string
            q = s if s != "\n" else '"\\n"'
            msg += f"{q}{t.n}\n"
            debug.write(msg)
        if token.type == 60:
            container.append(Entry(linenumber, "COMMENT"))
        else:
            container.append(e)
    # Toss out ITEM/NL and COMMENT/NL pairs using a state machine.  Any
    # leftover NL items are blank line candidates.  Note that any newlines
    # between comments are always left alone.
    blanklines = deque()
    last, candidate, start = None, False, True
    while container:
        e = container.popleft()
        if e.name == "ITEM":
            if start:  # This handles a first blank line in the file
                last, candidate = "ITEM", True
                start = False
            else:
                last, candidate = "ITEM", False
        elif e.name == "NL":
            if candidate:
                blanklines.append(e.linenumber)  # Save line number
            else:
                if last == "ITEM":
                    candidate = True
                elif last == "COMMENT":
                    candidate = False
        elif e.name == "COMMENT":
            last, candidate = "COMMENT", False
    return tuple(blanklines)


if __name__ == "__main__":
    # Run a basic test case
    from wrap import dedent
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
    """)
    stream = BytesIO(s.encode())
    # ln = GetEmptyLines(stream, debug=sys.stderr)
    ln = GetEmptyLines(stream)
    Assert(ln == (6, 8, 10))
