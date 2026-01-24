'''

Defines a Gist class to get gists from a string

Vision
    The Gist class will be the basis of the information about my python scripts
    and modules.  The core information will be

        gist:   One line description of the purpose
        cat:    Category of the module.  These are the core subjects used to classify
                both modules and scripts.
        desc:   Textual description of the file
        test:   How to test the module/script
        todo:   Things that need to be done to this file
        cr:     Copyright statement
        lic:    License for the use of this file

    The primary motivation of using the Gist class is to standardize the information in
    my modules and scripts to allow automated indexing, checking, and testing.

Description
    A Gist object is a dictionary that contains the text in a string handed to the
    constructor.  The use case is to provide textual information on the description,
    copyright, license, category, and ToDo items in python modules and scripts.  There's
    also information on how to test the module or script.

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
        
    Based on these definitions, the Gist class uses them to define a regular expression
    to split a string into a sequence of <element> tokens.  This sequence is used to
    produce a dictionary relating keywords to descriptions.

Use
    While the Gist class can be used directly, it's easy to subclass for special uses as
    needed.  As of this writing, I don't have a particular need at the moment, but I can
    foresee possible needs in the future; subclassing would allow for new functionality
    without breaking the existing stuff.

    As an example, a python module that for some reason cannot have a global gist string
    like _pgminfo (the string I use by default) can instead have the same information
    string commented out at the beginning of the file, surrounded by e.g. a unique
    marker string.  This would allow the derived Gist class to read in the file's lines,
    strip off the comment character, and process the remaining string with the Gist clas
    machinery.

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
        import re
    if 1:   # Custom imports
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
        'Take a gist string apart and store it as a dictionary'
        begin, end, sep = "<oo", "oo>", "∞"
        def __init__(self, gist, keywords=[]):
            self.gist = gist
            self.keywords = keywords
            # Initial checks
            if not all(ii(i, str) for i in (Gist.begin, Gist.end, Gist.sep)):
                raise TypeError("Gist class variables must be strings")
            if not (Gist.begin != Gist.end != Gist.sep):
                raise ValueError("Gist class variables must be unequal")
        def __str__(self):
            '''Returns a string representing the Gist instance.  This string
            representation will be close to what was encountered in the constructor's
            gist variable, but it's not guaranteed to be the same.  The key/value pairs
            will be in the same order they were in the original gist string, guaranteed
            by the LIFO order of dict's storage.
            '''
    gi = Gist("", [])

if 1:   # Experiment to parse elements
    S = dedent('''
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
    ''')
    t.even = t.wht
    t.odd = t.whtl
    t.key = t.ornl
    t.value = t.sky
    s = S.strip()
    if 1:   # Step 1:  separate into fields
        begin, end = "<oo", "oo>"
        fields = []
        assert begin != end
        r_element = "(" + begin + ".*?" + end + ")"
        f = re.split(r_element, s, re.S)
        for item in f:
            u = item.strip()
            if not u:
                continue
            fields.append(u)
        if 1:
            for i, field in enumerate(fields):
                c = t.odd if i % 2 else t.even
                t.print(f"{c}{i}: {field!r}")
        if 1:   # Check invariant
            s1 = '\n'.join(fields)
            if s != s1:
                raise ValueError("Bug: can't reconstruct invariant")
    if 1:   # Step 2:  parse each field by splitting on sep
        sep, di = "∞", {}
        assert sep != begin and sep != end
        print("-"*80)
        for i, field in enumerate(fields):
            field = field.replace(begin, "").replace(end, "")
            f = field.split(sep)
            if len(f) != 2:
                msg = f"{t.redl}Error:  field {i} didn't split on {sep!r} into 2 parts{t.n}"
                raise ValueError(msg)
            key, value = f
            key = key.strip()
            if key in di:
                msg = f"{t.redl}Error:  key {key!r} already in dictionary{t.n}"
                raise ValueError(msg)
            di[key.strip()] = value
        # Print the dict
        t.print(f"{t.purl}gist Dictionary contents:")
        for key, value in di.items():
            t.print(f"{t.key}{key}{t.n}:  {t.value}{value!r}")
    exit()

if 1:
    class Gist_(dict):
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
            myvalues = self.parse(s)
            self.n = len(fieldnames)
            if self.n:
                Assert(len(myvalues) >= Gist.numfields)
            # Get our keys & values
            key_value_pairs = []    # Use for dict constructor
            self.mykeys = []        # Remember key order
            for i in myvalues:
                f = i.split(Gist.sep)
                if len(f) != 2:
                    raise ValueError(f"Field {i!r} is missing separator {Gist.sep!r}")
                Assert(len(f) == 2)
                key = f[0].strip()
                self.mykeys.append(key)
                value = f[1].replace(Gist.end.lstrip(), "")
                key_value_pairs.append((key, value))
            # If fieldnames is not empty, check that we have the required fields
            for field in fieldnames:
                if field not in self:
                    raise ValueError(f"Field {field!r} missing")
            # Construct our dict
            self.super = super(Gist, self)
            self.super.__init__(key_value_pairs)
        def parse(self, pgminfo):
            'Return a list of the groups'
            a = re.split(Gist.regex, pgminfo, flags=re.S)
            b = [i for i in a if i != "\n" and i]
            return [i.replace(Gist.begin, "").replace(Gist.end, "") for i in b]
        def __str__(self):
            'Return form that will be stored in a file'
            b, e, sep, u = Gist.begin, Gist.end, Gist.sep, ""
            for key in self.mykeys:
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
