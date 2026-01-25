'''

Defines a Gist class to get gists from a string
    Vision

        The Gist class will be the basis of the information about my python scripts and
        modules.  The core information will be

            gist:   One line description of the purpose
            cat:    Category of the module.  These are the core subjects used to
                    classify both modules and scripts.
            desc:   Textual description of the file
            test:   How to test the module/script
            todo:   Things that need to be done to this file
            cr:     Copyright statement
            lic:    License for the use of this file

        The primary motivation of using the Gist class is to standardize the information
        in my modules and scripts to allow automated indexing, checking, and testing.

    Description
        A Gist object is a dictionary that contains the text in a string handed to the
        constructor.  The use case is to provide textual information on the description,
        copyright, license, category, and ToDo items in python modules and scripts.
        There's also information on how to test the module or script.

        A gist string is 

            <gist> ::= <element>+
            <element> ::= <begin> <spc> <key> <spc> <sep> <ws>* <value> <ws>* <end>
            <begin> ::= <char>+         Start of the element
            <key> ::= <char>+           Identifies the element
            <sep> ::= <char>+           Separates element into key & value
            <value> ::= <uchar>+        Description of the element
            <end> ::= <char>+           End of a gist element
            <ws> ::= <element of W>*
            <spc> ::= " "
            <uchar> ::= Any character in U
            <char> ::= Any character in C
            where
                U = set of all Unicode characters
                W = set of whitespace characters = set(" \t\n\r\f\v")
                C = set of other Unicode characters = U - W
            We must have
                <begin> != <keyword> != <sep> != <descr> != <end>
            
        Based on these definitions, the Gist class uses them to define a regular
        expression to split a string into a sequence of <element> tokens.  This sequence
        is used to produce a dictionary relating keywords to descriptions.

    Use
        While the Gist class can be used directly, it's easy to subclass for special
        uses as needed.  As of this writing, I don't have a particular need at the
        moment, but I can foresee possible needs in the future; subclassing would allow
        for new functionality without breaking the existing stuff.

        As an example, a python module that for some reason cannot have a global gist
        string like _pgminfo (the string I use by default) can instead have the same
        information string commented out at the beginning of the file, surrounded by
        e.g. a unique marker string.  This would allow the derived Gist class to read in
        the file's lines, strip off the comment character, and process the remaining
        string with the Gist clas machinery.

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
        import importlib
        import pathlib
        import re
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
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
            # Store our data
            self.gist = gist.strip()
            self.keywords = keywords
            self.super = super(Gist, self)
            # Handle the empty case
            if not self.gist:
                if self.keywords:
                    raise ValueError(f"Empty gist string, but keywords not empty")
                self.super.__init__(tuple())
                return
            self.strict = strict
            if 1:   # Get our key/value pairs
                r = "(" + Gist.begin + ".*?" + Gist.end + ")"
                fields = []
                for item in re.split(r, self.gist, re.S):
                    u = item.strip()
                    if not u:   # Ignore bare newlines
                        continue
                    fields.append(u)
                # Check an invariant
                if strict:
                    s = '\n'.join(fields)
                    if s != self.gist:
                        raise ValueError("Bug: can't reconstruct invariant")
            if 1:   # Parse each field by splitting on Gist.sep
                key_value_pairs = []
                for i, field in enumerate(fields):
                    field = field.replace(Gist.begin, "").replace(Gist.end, "")
                    f = field.split(Gist.sep, 1)
                    if len(f) != 2:
                        msg = (f"Error:  field {i} didn't split on {Gist.sep!r} into 2 parts:\n"
                            f"field = {field!r}")
                        raise ValueError(msg)
                    key, value = f
                    key = key.strip()
                    key_value_pairs.append((key, value))
            # Initialize the dictionary
            self.super.__init__(key_value_pairs)
            # Check that we have the required fields
            for kw in self.keywords:
                if kw not in self:
                    raise ValueError(f"{kw!r} not a keyword in Gist dictionary")
            if strict:
                if set(self) != set(keywords):
                    raise ValueError(f"Gist keys do not match those strings in keywords list")
            # See that we can reconstruct ourself via str()
            if self.strict and str(self) != "\n" + self.gist + "\n":
                raise ValueError("Can't reconstruct gist string (strict == True)")
        def __str__(self):
            '''Returns a string representing the Gist instance.  This string
            representation will be close to what was encountered in the constructor's
            gist variable, but it's not guaranteed to be the same.  The key/value pairs
            will be in the same order they were in the original gist string, guaranteed
            by the LIFO order of dict's storage.
            '''
            if not self:
                return ""
            u, sp = "", " "
            for key in self:
                u += Gist.begin + sp + key + sp + Gist.sep + self[key] + Gist.end + "\n"
            return "\n" + u

if 1:   # Utility functions
    def GetGistString(file, varname="_pgminfo"):
        '''Return the Gist string for this file (a string or pathname.Path instance).
        varname is the name of the global variable used to hold the gist, a string.
        None is returned if varname can't be read.
        '''
        # If the import method eventually has a problem, define the use_import keyword
        # and write the second method.
        use_import = True
        filename = str(file) if isinstance(file, pathlib.Path) else file
        if use_import:
            if filename.endswith(".py"):
                filename = filename[:-3]
            global GetGist_imported_module
            try:
                GetGist_imported_module = importlib.import_module(filename)
                var = eval(f"GetGist_imported_module.{varname}")
                return var
            except Exception:
                return None
        else:
            pass

if 0:   # Test area for code development
    g = GetGist("aa.py", varname="_aainfo", use_import=True)

    # Test objective:  show that an indented string can still be processed normally
    # The following shows the indentation messes up the output string form.  This
    # indicates that the common leading indent string of each line has to be found.
    # I'm going to unilaterally assume that the indentation is only done with space
    # characters; any tab characters found in the indentation will result in an
    # exception.
    x = '''
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
    import dpstr
    from textwrap import dedent as Dedent
    nl = "\n"
    n = dpstr.CountLeadingSpaces(x)
    lines = dpstr.PrepareMultilineString(x).split(nl)
    if 1:
        # The following demonstrates successful dedenting
        for i in range(len(lines)):
            lines[i] = lines[i][n:]
            #print(lines[i])
    a = repr(nl + nl.join(lines) + nl)
    #t.print(f"{t.ornl}{a}")
    u = Dedent(x)
    b = repr(u)
    #t.print(f"{t.purl}{b}")
    assert(a == b)
    if 0:
        gist = Gist(x)
        pp(gist)
        print(gist)
    exit()

if __name__ == "__main__":  
    from lwtest import run, raises, Assert
    from wrap import dedent
    def Test_GetGistString():
        s = GetGistString("gist.py")
        Assert(s == _pgminfo)
    def Test_Gist_Basics():
        if 1:   # Empty string
            s = ""
            gi = Gist(s)
            Assert(str(gi) == "")
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
            Assert(str(gi) == '\n<oo a ∞ a_value oo>\n')
            Assert(len(gi) == 1)
            # Only one split on separator
            s = "<oo a ∞ ∞ a_value oo>"
            gi = Gist(s, [])
            Assert(gi["a"] == " ∞ a_value ")
    def Test_Gist_TwoFields():
        s = dedent('''
            <oo a ∞ a_value oo>
            <oo b ∞ b_value
            oo>
        ''')
        gi = Gist(s, [])
        Assert(gi["a"] == " a_value ")
        Assert(gi["b"] == " b_value\n")
        Assert(str(gi) == '\n<oo a ∞ a_value oo>\n<oo b ∞ b_value\noo>\n')
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
    exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])
