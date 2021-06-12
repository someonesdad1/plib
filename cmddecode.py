'''
Decode user command strings, even if they are incomplete.
 
This module provides the CommandDecode object which, when initialized
with a sequence of allowed command strings, will allow you to find a
given command string when given just a prefix of the string.  If there
is enough of the command string given, you'll get a unique string in
return.  Otherwise, you'll get a list of candidates that matched.
Getting an empty sequence in return means the given string didn't match
anything.  The comparisons can be made on a case-insensitive basis if
you wish.
 
Example usage:
 
    s = set(("one", "two", "three"))
    c = CommandDecode(s)
    # Results for different user inputs:
    c("o") --> gives ["one"]
    c("t") --> gives ["two", "three"]
    c("x") --> gives []
 
Run this file as a script to get an interactive demo.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2006 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <programming> Decode user command strings.  When initialized with
    # a sequence of command strings, calling the object with a string
    # will return a list of 0, 1 or many strings.  0 means no match, 1
    # is a unique match, and many means more than one match.  The
    # constructor lets you choose to ignore the command's case or not.
    #∞what∞#
    #∞test∞# ["test/cmddecode_test.py"] #∞test∞#
    pass
if 1:  # Imports
    import re
    import sys
    from collections import defaultdict
    from pdb import set_trace as xx
class CommandDecode:
    '''Instantiate the class with a sequence of command strings.  Then
    call the object with a command candidate; the returned list will
    have either 0, 1, or multiple commands that matched.
    '''
    def __init__(self, commands, ignore_case=False):
        '''commands is a sequence that contains a unique set of strings.
        If you set ignore_case to True, then the commands will all be
        converted to lower case; if this lower-case set doesn't contain
        the same number of elements as commands, then you'll get a
        ValueError.
        '''
        self.ignore_case = ignore_case
        # See if we can convert commands to a set
        try:
            c = set(commands)
            if len(c) != len(commands):
                raise ValueError("commands container has replicates")
        except TypeError:
            raise ValueError("commands must be a sequence of strings")
        if not c:
            raise ValueError("commands must contain at least one command")
        if ignore_case:
            self.commands = set([i.lower() for i in c])
            if len(self.commands) != len(commands):
                msg = ("Some commands are not unique after conversion "
                       "to lower case")
                raise ValueError(msg)
        else:
            self.commands = c
        self.commands.discard("")
        # Build index dictionary; each key is the first letter of the
        # command and each element is a list of commands that have that
        # first letter.
        self.index = defaultdict(list)
        for cmd in self.commands:
            first_char = cmd[0]
            self.index[first_char].append(cmd)
        self.first_char_list = self.index.keys()
    def __str__(self):
        s = ' '.join(sorted(self.commands))
        ic = "ignore_case=True"
        return f"CommandDecode({s}, ignore_case={self.ignore_case})"
    def __call__(self, user_string):
        if not isinstance(user_string, str):
            raise ValueError("Input must be a string")
        s = user_string.strip()
        if not s:
            return []
        if self.ignore_case:
            s = s.lower()
        if s in self.commands:
            return [user_string]
        first_char = s[0]
        if first_char not in self.first_char_list:
            return []
        possible_commands = self.index[first_char]
        if self.ignore_case:
            regexp = re.compile("^" + s, re.I)
        else:
            regexp = re.compile("^" + s)
        matches = []
        for cmd in possible_commands:
            if regexp.match(cmd):
                matches.append(cmd)
        if len(matches) == 0:
            return []
        if len(matches) == 1:
            return [matches[0]]
        return matches
if __name__ == "__main__":
    # Demonstrate the class; use some typical UNIX program names.
    cmds, d = '''
        ar awk banner basename bc cal cat cc chmod cksum clear cmp
        compress cp cpio crypt ctags cut date dc dd df diff dirname du
        echo ed egrep env ex expand expr false fgrep file find fmt
        fold getopt grep gzip head id join kill ksh ln logname ls m4
        mailx make man mkdir more mt mv nl nm od paste patch perl pg
        pr printf ps pwd rev rm rmdir rsh sed sh sleep sort spell
        split strings strip stty sum sync tail tar tee test touch tr
        true tsort tty uname uncompress unexpand uniq uudecode
        uuencode vi wc which who xargs zcat
    ''', []
    for i in cmds.replace("\n", "").split():
        d.append((i, ""))
    c, prompt = CommandDecode(dict(d), ignore_case=True), "> "
    print("Enter some UNIX commands, 'q' to quit, '.' to list all:")
    while True:
        cmd = input(prompt)
        if cmd == "q":
            break
        elif cmd == ".":
            for i in list(c.commands):
                print(i, end=" ")
            print()
        else:
            x = c(cmd)
            if not x:
                print("'%s' unrecognized" % cmd)
            elif len(x) == 1:
                print("'%s' was an exact match to '%s'" % (cmd, x[0]))
            else:
                x.sort()
                print("'%s' is ambiguous:  %r" % (cmd, x))
