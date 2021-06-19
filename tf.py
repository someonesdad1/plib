'''

Text formatter: Develop a mini-language for formatting strings.  The
formatting commands get stripped out of the output.

The main use case is to be able to get formatted output for the help
strings used in scripts, as I need this a lot.

Commands to the formatter will match the regexp '^\s*[^\\]\.' followed
by a command token.  If you want a line to begin with a period, escape
it with a backslash.

In the following, the preceding '.' to the commands is not shown.

It would be nice to include a simple class that ignores the formatting
commands in a string and just lets it be printed to stdout.  This could
be done with a regexp that is used on every line of the string.  This
means that someone will still see the output, though it won't look like
it was intended; this could happen if a user didn't get a copy of the
tf.py script.

    Idea:  would it be possible to make the documentation string python
    code that the script would execute a line at a time?  This would be
    cool and portable, but probably a lot of work and complex.

Python code blocks and variables

    { and } delimit code blocks.  Common indentation is removed and the
    lines are executed one at a time with exec(line, globals(), vars)
    where vars is a maintained local variables dictionary.

    exec s:  Execute the statement s with exec(s, globals(), vars).

    del x:  Delete the variable named x from vars.

    clear:  Clears the vars dictionary.  If you .restore or .pop, the
    old vars dictionary will be restored.

State 

    The saved states are in a dictionary that is independent of the
    variables in vars and code.

    verbatim x/on/off:  If on, the output is not formatted; it is output
    as it is found in the line.  If the argument is x, it is
    bool(vars["x"]).

    out x/on/off:  Turn output on/off.  If it is off, no lines are
    output until the next '.output on' is seen.  This is a handy way to 
    comment out a chunk of text.  If the argument is x, it is
    bool(vars["x"]).

    push:  Save the current state.  Note vars is part of the state, so a
    subsequent '.clear' will be "forgotten" when you .pop or .restore an
    older state.  A shallow copy of vars is made for the new state.

    pop:  Restore the previously pushed state

    save x:  Save the current state to name x.  Same vars semantics as
    .push.

    load x:  Restore the state with name x

    remove x:  Remove the saves state named x

Margins

    lm n:  Set left margin.  Set to 0 to have text start at column 1.
    Default 0.

    rm n:  Set right margin.  Set to 0 to make it be determined by the
    .width command; it will be (width - lm).  Default 0.

    width n:  0 means wrap to width from COLUMNS.  'n' means to wrap to
    int(n) columns.  Default 0.

    prefix s:  String to prefix before each line.  Default "".

    suffix s:  String to append to each line.  Default "".

Justification
    If n is given, it's for the following n lines, then return to the
    previous state.  If n is not given, then it's "sticky" and remains
    set.  Left justification is the default.  

    < [n]:  Left justification

    > [n]:  Right justification

    ^ [n]:  Center the lines

Other commands
    empty n:  A line with no whitespace is replaced by one with n space
    characters.

    #:  This line is a comment and won't make it to the output



'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <programming> Provides a basic text formatting language for use in 
    # formatting text for python script output to a terminal.
    #∞what∞#
    #∞test∞# --test #∞test∞#
    pass
if 1:   # Imports
    from collections import deque
    import os
    import pathlib
    import re
    import sys
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    class G: pass
    G.commands = r'''{ } exec del clear verbatim out push pop save load
        remove lm rm width prefix suffix < > \^ empty # '''.split()
    # For debugging
    G.commands = r'''{ } exec del clear < \^ # '''.split()

if 1:
    # Build up a regexp to recognize commands
    s = []
    for cmd in G.commands:
        s.append(f"^\\s*\\.{cmd}")
    t = '|'.join(s)
    r = re.compile(t)
    a = '''
    .{
    .}
    .exec a
    .< b
    .^ c
    .kjdk
    me
    you
    '''
    for i in a.split("\n"):
        if r.search(i):
            print(i)
    exit()

if __name__ == "__main__": 
    # Run the selftests
    from lwtest import run, Assert
    import sys
    from pdb import set_trace as xx
    def Test1():
        pass
    if "--test" in sys.argv:
        exit(run(globals(), halt=1)[0])
if __name__ == "__main__": 
    # Run the demos
    def Example1():
        pass
    run(globals(), regexp=r"^Example\d\d?", quiet=True)
