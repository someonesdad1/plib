'''
Defines a Gist class to get gists from a string
    Use:  The default class parses a string such as
        
            _pgminfo = """
                <oo gist ∞ One line explanation of purpose oo>
                <oo desc ∞ Module details oo>
                <oo copy ∞ Copyright message oo>
                <oo lic ∞ License message oo>
                <oo cat ∞ category oo>
                <oo test ∞ How to file's self-tests oo>
                <oo todo ∞ To Do list for this code oo>
            """
        
        When instantiated with such a string, the Gist class becomes a dictionary that
        gives you access to the text in each field.  Here, "<oo" and "oo>" delimit
        fields and ∞ separates the dictionary's keywords from the values:
        
            gist = Gist(_pgminfo)
            print(gist["desc"])
        
        prints the string " Module description ".
        
        You can modify the dictionary as needed, then write the modified form to a
        stream by e.g. "print(str(gist), file=stream)".
        
        The primary use case for the Gist class is to standardize the information in my
        modules and scripts to allow automated indexing, checking, and testing.
        
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Module to get the gist data in a text file oo>
        <oo desc ∞ See docstring oo>
        <oo copy ∞ Copyright © 2026 Don Peterson oo>
        <oo lic ∞ 
            MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ util oo>
        <oo test ∞ run oo>
        <oo todo ∞ 
            - ∞∞1 Include an 'ind' field that defines the indent level of the gist in the
              file.  This gets around the vagaries of removing and putting the
              whitespace back.
        oo>
    '''
    if 1:   # Standard imports
        import importlib
        import pathlib
        import re
    if 1:   # Custom imports
        import dpstr
        from wrap import dedent
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
        'Take a gist string apart and store it as a dictionary'
        begin, end, sep = "<oo", "oo>", "∞"
        def __init__(self, gist, keywords=[], strict=False):
            '''gist is the string to parse to get the dictionary elements.  If keywords
            is not empty, then it's a list of strings that must be keywords in the gist
            string or an exception will be raised.  If strict is True, then the set of
            keyword strings in keywords must match the keys of the Gist dictionary.
            '''
            # Check class variables
            if not all(ii(i, str) for i in (Gist.begin, Gist.end, Gist.sep)):
                raise TypeError("Gist class variables must be strings")
            if not all(bool(i) for i in (Gist.begin, Gist.end, Gist.sep)):
                raise ValueError("Gist class variables must not be empty")
            if not (Gist.begin != Gist.end != Gist.sep):
                raise ValueError("Gist class variables must be unequal")
            # Check arguments
            if not ii(gist, str):
                raise TypeError("gist argument must be a string")
            if keywords:
                if not all(ii(i, str) for i in keywords):
                    raise TypeError("keywords elements must be strings")
                if any(i.strip() == "" for i in keywords):
                    raise ValueError("keywords cannot be empty or only space characters")
            # Store our data
            self.gist = gist.strip()
            self.keywords = keywords
            self.super = super(Gist, self)
            self.strict = bool(strict)
            # Handle the empty case
            if not self.gist:
                if self.keywords:
                    raise ValueError(f"Empty gist string, but keywords not empty")
                self.super.__init__(tuple())
                return
            if 1:   # Get our key/value pairs
                regex = "(" + Gist.begin + ".*?" + Gist.end + ")"
                fields = []
                for item in re.split(regex, self.gist, re.S):
                    u = item.strip()
                    if not u:   # Ignore bare newlines
                        continue
                    fields.append(u)
            if 1:   # Parse each field by splitting on Gist.sep
                key_value_pairs = []
                for i, field in enumerate(fields):
                    # Strip off field begin/end strings
                    field = field.replace(Gist.begin, "").replace(Gist.end, "")
                    f = field.split(Gist.sep, 1)
                    if len(f) != 2:
                        msg = (f"Error:  field {i} didn't split on {Gist.sep!r} into 2 parts:\n"
                            f"field = {field!r}")
                        raise ValueError(msg)
                    key, value = f
                    key_value_pairs.append((key.strip(), value))
            # Initialize the dictionary
            self.super.__init__(key_value_pairs)
            # Check that we have the required fields
            for kw in self.keywords:
                if kw.strip() not in self:
                    raise ValueError(f"{kw!r} not a keyword in Gist dictionary")
            if strict:
                if set(self) != set(keywords):
                    raise ValueError(f"Gist keys do not match those strings in keywords list")
        @classmethod
        def GetGistString(cls, file, varname="_pgminfo"):
            '''Return the Gist string for a file (a string or pathname.Path instance).
            varname is the name of the global variable used to hold the gist, a string.
            None is returned if varname can't be read.
            '''
            filename = str(file) if isinstance(file, pathlib.Path) else file
            if filename.endswith(".py"):
                filename = filename[:-3]
            global GetGistString_imported_module
            try:
                GetGistString_imported_module = importlib.import_module(filename)
                var = eval(f"GetGistString_imported_module.{varname}")
                return var
            except Exception:
                return None
        @classmethod
        def TestGist(cls):
            'This is a simple gist intended for basic testing'
            return dedent('''
                <oo key1 ∞ value1 oo>
                <oo key2 ∞ value2 oo>'''[1:])
        @classmethod
        def DefaultGist(cls):
            return dedent('''
                <oo gist ∞ One line description of file/module oo>
                <oo desc ∞ Description oo>
                <oo copy ∞ Copyright © 2026 Don Peterson oo>
                <oo lic ∞ 
                    MIT License
                    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
                    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
                    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
                oo>
                <oo ind ∞ 8 indent oo>
                <oo cat ∞ category oo>
                <oo test ∞ notest oo>
                <oo todo ∞ Todo items oo>'''[1:])

if __name__ == "__main__":  
    import edit
    import sys
    import textwrap
    from lwtest import run, raises, Assert
    from wrap import dedent, Dedent
    from color import t
    def Test_GetGistString():
        s = Gist.GetGistString("gist.py")
        Assert(s == _pgminfo)
    def Test_Gist_Basics():
        if 1:   # Empty string
            s = ""
            gi = Gist(s)
            Assert(str(gi) == "{}")
            Assert(len(gi) == 0)
        if 1:   # Type of sequence unimportant
            for i in (tuple(), {}, set(), ""):
                Gist("", i)
            # But keywords argument can't be nonempty with an empty gist string
            raises(ValueError, Gist, "", "abc")
        if 1:   # One field
            s = "<oo a ∞ a_value oo>"
            gi = Gist(s, [])
            Assert(gi["a"] == " a_value ")
            Assert(str(gi) == "{'a': ' a_value '}")
            Assert(len(gi) == 1)
        if 1:   # Keyword testing
            # Missing a keyword
            s = "<oo a ∞ a_value oo>"
            raises(ValueError, Gist, s, ["a", "b"])
            # Use 3 keywords
            s = '''<oo a ∞ a oo><oo b ∞ b oo><oo c ∞ c oo>'''
            gi = Gist(s, [])
            Assert(str(gi) == "{'a': ' a ', 'b': ' b ', 'c': ' c '}")
            # OK if two required keywords are present ('c' is an OK extra keyword)
            Gist(s, ["a", "b"])     # No exception, as a and b are keywords
            # But if strict is True, then get exception
            raises(ValueError, Gist, s, ["a", "b"], strict=True)
    def Test_Gist_TwoFields():
        s = dedent('''
            <oo a ∞ a_value oo>
            <oo b ∞ b_value
            oo>
        ''')
        gi = Gist(s, [])
        Assert(gi["a"] == " a_value ")
        Assert(gi["b"] == " b_value\n")
        Assert(str(gi) == "{'a': ' a_value ', 'b': ' b_value\\n'}")
        Assert(len(gi) == 2)
        # Things work when strict == False
        gi = Gist(s, keywords=[], strict=False)
        gi = Gist(s, keywords=["a"], strict=False)
        gi = Gist(s, keywords=["b"], strict=False)
        gi = Gist(s, keywords=["a", "b"], strict=False)
        # Exception because "c" not in dictionary
        raises(ValueError, Gist, s, keywords="c".split(), strict=False)
        raises(ValueError, Gist, s, keywords="b c".split(), strict=False)
        raises(ValueError, Gist, s, keywords="a b c".split(), strict=False)
        # Problems when strict == True
        gi = Gist(s, keywords="a b".split(), strict=True)   # No exception
        raises(ValueError, Gist, s, keywords=[], strict=True)
        raises(ValueError, Gist, s, keywords=["a"], strict=True)
        raises(ValueError, Gist, s, keywords="a c".split())
        raises(ValueError, Gist, s, keywords="c".split())
    def Test_Gist_BadConstructorData():
        # The gist argument must be a string
        raises(TypeError, Gist, 1)
        raises(TypeError, Gist, 1.0)
        raises(TypeError, Gist, b'')
    def Test_DifferentClassVariables():
        Gist.begin, Gist.end, Gist.sep = ">oo", "<oo", "©"
        s = ">oo a © a_value <oo"
        gi = Gist(s, [])
        expected = " a_value "
        Assert(gi["a"] == expected)
        # Back to defaults
        Gist.begin, Gist.end, Gist.sep = "<oo", "oo>", "∞"
        s = "<oo a ∞ a_value oo>"
        Assert(gi["a"] == expected)
    def Boilerplate():
        'Print out boilerplate for my python scripts'
        print("'''\n'''")   # Space for docstring
        # Header with gist, imports, global variables
        print(dedent("""
            if 1:  # Header
        """))
        print("    _pgminfo = '''")
        gist = Gist.DefaultGist()
        print(textwrap.indent(gist, " "*8))
        print("    '''")
        print(Dedent('''
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
        ''', n=12))
        # Remaining code
        print(dedent("""
            if 1:   # Utility
                def GetColors():
                    t.stuff = t.lill
                    t.err = t.redl
                    t.dbg = t.lill if g.dbg else ""
                    t.N = t.n if g.dbg else ""
                def GetScreen():
                    'Return (LINES, COLUMNS)'
                    return (
                        int(os.environ.get("LINES", "50")),
                        int(os.environ.get("COLUMNS", "80")) - 1
                    )
                def Dbg(*p, **kw):
                    if g.dbg:
                        print(f"{t.dbg}", end="")
                        print(*p, **kw)
                        print(f"{t.N}", end="")
                def Warn(*msg, status=1):
                    print(*msg, file=sys.stderr)
                def Error(*msg, status=1):
                    Warn(*msg)
                    exit(status)
                def Usage(status=0):
                    print(dedent(f'''
                    Usage:  {sys.argv[0]} [options] etc.
                      Explanations...
                    Options:
                      -h      Print a manpage
                    '''))
                    exit(status)
                def ParseCommandLine(d):
                    d["-a"] = False     # Need description
                    d["-d"] = 3         # Number of significant digits
                    if len(sys.argv) < 2:
                        Usage()
                    try:
                        opts, args = getopt.getopt(sys.argv[1:], "ad:h") 
                    except getopt.GetoptError as e:
                        print(f"{sys.argv[0]}:  {e}")
                        exit(1)
                    for o, a in opts:
                        if o[1] in list("a"):
                            d[o] = not d[o]
                        elif o == "-d":
                            try:
                                d[o] = int(a)
                                if not (1 <= d[o] <= 15):
                                    raise ValueError()
                            except ValueError:
                                Error(f"-d option's argument must be an integer between 1 and 15")
                        elif o == "-h":
                            Usage()
                    GetColors()
                    return args
            if 1:   # Core functionality
                pass

            if __name__ == "__main__":
                d = {}      # Options dictionary
                args = ParseCommandLine(d)
        """))
    def Help():
        print(dedent('''
        Help for module gist:
            cmd       Action
            e         Edit this file
            h         See this help
            g         Print default gist string
            bp        Print python boilerplate
        '''))
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "e":
            edit.Edit(sys.argv[0], opt=["-c", "/def Boilerplate"])
        elif cmd == "h":
            Help()
        elif cmd == "g":
            print(Gist.DefaultGist())
        elif cmd == "bp":
            Boilerplate()
        else:
            t.print(f"{t.sky}{cmd!r} not recognized")
            Help()
    else:
        # Run module tests
        exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])
