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
        c, prompt = CommandDecode(s), "> "
        print(". to list choices, q to exit")
        while True:
            cmd = input(prompt)
            if cmd == "q":
                break
            elif cmd == ".":
                for i in c.commands:
                    print(i, end=" ")
                print()
            else:
                x = c(cmd)
                if not x:
                    print(f"'{cmd}' unrecognized")
                elif len(x) == 1:
                    print(f"'{cmd}' was an exact match to '{x[0]}'")
                else:
                    x.sort()
                    print(f"'{cmd}' is ambiguous:  {x}")
                    
        # Results for different user inputs:
        c("o") --> gives ["one"]
        c("t") --> gives ["two", "three"]
        c("x") --> gives []
        
    Run this file as a script to get an interactive demo.
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Decode user command strings oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2006 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility  oo>
        <oo test ∞ testdir oo>
        <oo todo ∞ 
            
            - 
            
        oo>
    '''
    if 1:  # Standard imports
        import re
        from collections import defaultdict
    if 1:  # Custom imports
        pass
if 1:   # Classes
    class CommandDecode:
        '''Decode user command strings, even if they are incomplete.
        Instantiate the class with a sequence of command strings.  Then call the object
        with a command candidate; the returned list will have either 0, 1, or multiple
        commands that matched.
        '''
        def __init__(self, commands, ignore_case=False):
            '''commands is a sequence that contains a unique set of strings.
            If you set ignore_case to True, then the commands will all be
            converted to lower case; if this lower-case set doesn't contain
            the same number of elements as commands, then you'll get a
            ValueError.
            '''
            self.ic = ignore_case
            # See if we can convert commands to a set
            try:
                c = set(commands)
                if len(c) != len(commands):
                    raise ValueError("commands container has replicates")
            except TypeError:
                raise ValueError("commands must be a sequence of strings")
            if not c:
                raise ValueError("commands must contain at least one command")
            # Build self.commands_set, a set of allowed commands
            if ignore_case:
                self.command_set = set([i.lower() for i in c])
                if len(self.command_set) != len(commands):
                    msg = "Some commands are not unique after conversion to lower case"
                    raise ValueError(msg)
            else:
                self.command_set = c
            self.command_set.discard("")   # Get rid of empty string
            if 1:
                # Build index dictionary:  each key is the first character of the
                # command and each element is a list of commands that have that first
                # character.  This is a simple method to reduce the amount of searching
                # for command matches.
                self.index = defaultdict(list)
                for cmd in self.command_set:
                    first_char = cmd[0]
                    self.index[first_char].append(cmd)
                self.first_char_list = self.index.keys()
        def __str__(self):
            s = " ".join(sorted(self.command_set))
            return f"CommandDecode({s}, ignore_case={self.ic})"
        def __call__(self, string):
            'Return a list of the commands string matches'
            if not isinstance(string, str):
                raise ValueError("Input must be a string")
            user_string = string.strip()
            if not user_string:
                return []
            user_string = user_string.lower() if self.ic else user_string
            if user_string in self.command_set:
                return [user_string]
            if user_string[0] not in self.first_char_list:
                return []
            # Return a list of the possible matches
            r = "^" + user_string
            regex, matches = re.compile(r, re.I) if self.ic else re.compile(r), []
            for cmd in self.index[user_string[0]]:
                if regex.match(cmd):
                    matches.append(cmd)
            return matches

if __name__ == "__main__":
    import sys
    from lwtest import run, assert_equal, raises
    def Demo():
        # Demonstrate the class; use some typical UNIX program names.
        cmds, d = (
            '''
            ar awk banner basename bc cal cat cc chmod cksum clear cmp
            compress cp cpio crypt ctags cut date dc dd df diff dirname du
            echo ed egrep env ex expand expr false fgrep file find fmt
            fold getopt grep gzip head id join kill ksh ln logname ls m4
            mailx make man mkdir more mt mv nl nm od paste patch perl pg
            pr printf ps pwd rev rm rmdir rsh sed sh sleep sort spell
            split strings strip stty sum sync tail tar tee test touch tr
            true tsort tty uname uncompress unexpand uniq uudecode
            uuencode vi wc which who xargs zcat
        ''',
            [],
        )
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
    def Test_CommandDecode_Exceptions():
        commands = set(("a", "Aaa", "Aab", "aaa", "aab"))
        # Case-insensitive instantiation results in an exception ('Aaa' and
        # 'aaa' collide).
        raises(ValueError, CommandDecode, commands, ignore_case=True)
        # commands not a dict/set
        raises(ValueError, CommandDecode, 4)
        # Empty dict/set
        raises(ValueError, CommandDecode, {})
        raises(ValueError, CommandDecode, set())
        # Cannot contain empty string
        raises(ValueError, CommandDecode, set("",))
        # Call's argument must be a string
        cmd = CommandDecode(commands)
        raises(ValueError, cmd, 4)
        # Can't make empty call
        raises(TypeError, cmd)
    def Test_CommandDecode():
        commands = set(("a", "Aaa", "Aab", "aaa", "aab"))
        cmd = CommandDecode(commands, ignore_case=False)
        assert set(cmd("a")) == set(["a"])
        assert set(cmd("ax")) == set([])
        assert set(cmd("aa")) == set(["aaa", "aab"])
        assert set(cmd("Aa")) == set(["Aaa", "Aab"])
        assert set(cmd("Aab")) == set(["Aab"])
        # Case insensitive
        commands = set(("A", "AAA", "AAB"))
        cmd = CommandDecode(commands, ignore_case=True)
        assert set(cmd("a")) == set(["a"])
        assert set(cmd("ax")) == set([])
        assert set(cmd("AX")) == set([])
        assert set(cmd("aa")) == set(["aaa", "aab"])
        assert set(cmd("Aa")) == set(["aaa", "aab"])
        assert set(cmd("Aab")) == set(["Aab"])
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])
    else:
        Demo()
