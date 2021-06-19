'''
Text formatter: Develop a mini-language for formatting strings.

    The main use case is to be able to get formatted output for the help
    strings used in scripts.

    A line containing a formatter command begins with a "." after
    stripping off whitespace.  If you want a line to begin with a
    period, escape it with a backslash.

    In the following, the leading '.' to the commands is not shown.

    Python code blocks and variables

        { and } delimit code blocks.  Common indentation is removed and the
        lines are executed one at a time with exec(line, globals(), vars)
        where vars is a maintained local variables dictionary.

        del x:  Delete the variable named x from vars.

        clear:  Clears the vars dictionary.  If you .pop, the old vars
        dictionary will be restored.

    State 

        The saved states are in a dictionary that is independent of the
        variables in vars and code.  This dictionary gets put onto a stack
        when you .push.

        format x/on/off:  If off, the output is not formatted; it is
        output as it is found in the line.  Otherwise, each line is
        formatted per the current state.  If the argument is x, it is
        bool(vars["x"]).

        out x/on/off:  Turn output on/off.  If it is off, no lines are
        output until the next '.output on' is seen.  This is a handy way to 
        comment out a chunk of text.  If the argument is x, it is
        bool(vars["x"]).

        push:  Save the current state.  Note vars is part of the state, so a
        subsequent '.clear' will be "forgotten" when you .pop or .restore an
        older state.  A shallow copy of vars is made for the new state.

        pop:  Restore the previously pushed state

        State variables:

            Left margin:        integer >= 0
            Right margin:       integer >= 0
            Width               integer >= 0
            Prefi               string
            Suffi               string
            Justification:      {left, right, center}

    Margins

        lm n:  Set left margin.  Set to 0 to have text start at column 1.
        Default 0.

        width n:  0 means wrap to width from COLUMNS.  'n' means to wrap to
        int(n) columns.  Default 0.

    Justification
        <:      Left justification
        >:      Right justification
        ^:      Center the lines
        wrap x/on/off:   Wrap paragraphs to current margins

    Other commands
        empty n:  A line with no whitespace is replaced by one with n space
        characters.

        #:  This line is a comment and won't make it to the output

    Commands with arguments:
        exec del verbatim out save load remove lm rm width prefix suffix
        emtpy

    Commands with no arguments:
        { } clear push pop 

    Commands with optional arguments
        < > ^ #

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
    from pdb import set_trace as xx 
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    class G: pass
    G.nl = "\n"
class IdentifyCmd:
    '''Call the identify method with the candidate line and it will
    return the parsed command if it is a command; otherwise None is
    returned.
    '''
    def __init__(self):
        self.no_args = set("{ } clear push pop".split())
        self.opt_args = set("< > ^ #".split())
        self.args = set('''exec del verbatim out save load 
            remove lm rm width prefix suffix emtpy'''.split())
        self.all = self.no_args | self.opt_args | self.args
    def identify(self, line):
        '''Return None if not a command; otherwise return list of 
        [cmd, arg1, ...].
        '''
        s = line.strip()
        if not s.startswith("."):
            return None
        f = s[1:].split()
        candidate = f[0]
        if candidate not in self.all:
            return None
        elif candidate in self.no_args:
            return [candidate]
        elif candidate in self.opt_args or candidate in self.args:
            return f

def dedent(s, empty=True, trim_leading=True, trim_trailing=False,
           trim_end=True):
    '''For the multiline string s, remove the common leading space
    characters and return the modified string.

    empty               Consider empty lines to have an infinite number
                        of spaces.  They will be empty lines in the
                        output string.
    trim_leading        Remove the first line if it only consists of
                        space characters.
    trim_trailing       Remove the last line if it only consists of
                        space characters.
    trim_end            Remove any trailing whitespace.
    '''
    def LeadingSpaces(s):
        'Return the number of space characters at the beginning of s'
        t, count = deque(s), 0
        while t:
            c = t.popleft()
            if c == " ":
                count += 1
            else:
                return count
        return 0
    t = s.strip()
    if not t:
        return ""
    if trim_end:
       s = s.rstrip()
    lines = s.split(G.nl)   # Splitting on a newline always returns a list
    if len(lines) == 1:
        return s.lstrip()
    if not trim_end and trim_trailing:
        if set(lines[-1]) == set(" "):
            del lines[-1]
    if len(lines) > 1 and trim_leading:
        t = set(lines[0])
        if not t or t == set(" "):
            del lines[0]
    # Get sequence of the number of beginning spaces on each line
    o = [LeadingSpaces(i) for i in lines]
    if empty:
        # Decorate the blank lines
        m = max(o)
        o = [i if i else m + 1 for i in o]  
    n = min(o)
    if n:
        o = [i[n:] for i in lines]
    return G.nl.join(o)

s = '''    
        Here's line 1
            Here's line 2 with following empty line




    '''
print("Original:")
for i in s.split(G.nl):
    print(repr(i))
print("-"*70)
t = dedent(s, trim_end=True)
print("Dedented:")
for i in t.split(G.nl):
    print(repr(i))
exit()

test = '''
    .{
    .}
    .exec a
    .< b
    .^ c

    .exece a
    .kjdk
    .<< b
'''
if 0:
    # Use a regexp to identify a candidate line.  Then split the line
    # into tokens and search in a set.
    commands = r'''{ } exec del clear verbatim out push pop save load
        remove lm rm width prefix suffix < > ^ empty # '''.split()
    # Recognizing commands
    r = re.compile(r"^\s*\.")
    def Cmd(line):
        if not r.search(line):
            return None
        f = line.strip().split()
        c = f[0]
        if c[1:] in commands:
            print(f"Command = {line.strip()}")
        else:
            print(f"'{c}' not recognized")
    for i in test.split("\n"):
        Cmd(i)
    exit()

if 1:
    c = IdentifyCmd()
    for i in test.split("\n"):
        t = c.identify(i)
        if t is not None:
            print(f"{i:20s}    command = {t}")
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
