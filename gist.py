'''

A Gist object is a dictionary that contains the text in a string handed to the
constructor.  The use case is to provide textual information on the description,
copyright, license, category, and ToDo items in python modules and scripts that I write.
There's also information on how to test the module or script.

'''
_pgminfo = '''
<oo desc ∞
    Module to get the gist data in a file
oo>
<oo cr ∞ Copyright © 2026 Don Peterson oo>
<oo license ∞
    Licensed under the Open Software License version 3.0.
    See http://opensource.org/licenses/OSL-3.0.
oo>
<oo cat ∞ util oo>
<oo test ∞ run oo>
<oo todo ∞ oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:   # Classes
    class Gist(dict):
        '''Take a gist string apart and store it as a dictionary, giving access to the
        fields of the gist string.   To store the data back to a stream (e.g., a file
        being modified), print the instance to the stream.
    
        For this string
            _pgminfo = """
            <oo desc ∞
                Type program description here
            oo>
            <oo cr ∞ Copyright © 2026 Don Peterson oo>
            <oo license ∞   
                Licensed under the Open Software License version 3.0.
                See http://opensource.org/licenses/OSL-3.0.
            oo>
            <oo cat ∞ category oo>
            <oo test ∞ none oo>
            <oo todo ∞
    
                - List of todo items here
    
            oo>
            """
        the returned dictionary will be:
            {'cat': ' category ',
            'cr': ' Copyright © 2026 Don Peterson ',
            'desc': '\n    Type program description here\n',
            'license': '   \n'
                        '    Licensed under the Open Software License version 3.0.\n'
                        '    See http://opensource.org/licenses/OSL-3.0.\n',
            'test': ' none ',
            'todo': '\n\n    - List of todo items here\n\n'}
        '''
        begin, end, sep = "<oo ", "oo>", "∞"
        regex = "(" + begin + r".*?[ \n]" + end + ")"
        numfields = 6
        def __init__(self, s, fieldnames=[]):
            '''s is the string to be parsed.  fieldnames is a sequence of allowed
            fieldnames that must be present or an exception will be raised.
            '''
            self.s = s
            a = self.parse(s)
            self.n = len(fieldnames)
            if self.n:
                Assert(len(a) >= n)
            if 0:   # Print out the separated string list
                print(f"{t.lill}Parsed string:")
                for i, u in enumerate(s):
                    print(f"{i}: {u!r}")
                t.print(end="")
                exit()
            # Get our keys & values
            key_value_pairs = []    # Use for dict constructor
            self.mykeys = []        # Remember key order
            for i in a:
                f = i.split(Gist.sep)
                if len(f) != 2:
                    raise ValueError(f"Field {i!r} is missing separator {Gist.sep!r}")
                Assert(len(f) == 2)
                key = f[0].strip()
                self.mykeys.append(key)
                value = f[1].replace(Gist.end.lstrip(), "")
                key_value_pairs.append((key, value))
            if 0:
                print(f"Key-value pairs:\n{t.sky}", end="")
                pp(key_value_pairs)
                t.print()
            # If fieldnames is not empty, check that we have the required fields
            for field in fieldnames:
                if field not in self:
                    raise ValueError(f"Field {field!r} missing")
            # Construct our dict
            self.super = super(Gist, self)
            self.super.__init__(key_value_pairs)
            if 0:
                print(f"Dump of dict:\n{t.lill}", end="")
                pp(self)
                t.print()
            # Dump reconstituted string in color ornl
            if 0:
                print(f"{t.ornl}", end="")
                print(Decorate(str(self)))
                t.print()
        def parse(self, pgminfo):
            'Return a list of the groups'
            a = re.split(Gist.regex, pgminfo, flags=re.S)
            b = [i for i in a if i != "\n" and i]
            return [i.replace(Gist.begin, "").replace(Gist.end, "") for i in b]
        def __str__(self):
            'Return form that will be stored in a file'
            b, e, sep, u = Gist.begin, Gist.end, Gist.sep, ""
            for key in self.mykeys:
                n = "" if self[key].startswith("\n") else " "
                u += b + key + " " + sep + self[key] + e + "\n"
            return "\n" + u

if __name__ == "__main__":  
    from lwtest import run, Assert
    from wrap import dedent

    def Test_GistInit():
        nl = "\n"
        s = dedent('''
        <oo desc ∞
            Type program description here
        oo>
        <oo cr ∞ Copyright © 2026 Don Peterson oo>
        <oo license ∞
            Licensed under the Open Software License version 3.0.
            See http://opensource.org/licenses/OSL-3.0.
        oo>
        <oo cat ∞ category oo>
        <oo test ∞ none oo>
        <oo todo ∞

            - List of todo items here

        oo>''')
        gist = Gist(s)
        Assert(str(gist) == nl + s + nl)
    exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])
