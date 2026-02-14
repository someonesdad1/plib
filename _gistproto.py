'''
10 Feb 2026 
New thinking about how to use gists in python files

Every python module/script will get a function _GetGist() that returns an instance of the
Gist class, which is a dictionary of required gist keys.  The leading underscore in the
name indicates that it's not intended to be a part of the file's public interface and
probably shouldn't be used by users of the file unless they know what the function does.



Description of problems
- I seem to be running into a thorny problem where some of the files like
    novas.py and eevblog.py cannot have their _pgminfo variables read.  Online
    docs say python doesn't enforce the custom of such a variable being private,
    but I can't figure out why 6 files are still having problems.
- When I changed "_pgminfo" in eevblog.py to "pgminfo", the variable was read in
    just fine.  This feels like a troubling deep bug in python.
    - All the files can be imported in the REPL without error
- Options
    - Rename _pgminfo to pgminfo
    - Put a function GetGist() into every file that's used to get the gist
        - This has the benefit of making it trivial to find files that don't
            have a gist
- GetGist() function in each file
    - Copyright and license will go into python comments at the top of the file
    - It's after the if __name__ == "__main__":  line, but it's in the global
        namespace
    - awk or grep can find it quickly; there's no need to import the file.  However,
      importing the file and running the function give you the gist dict, letting the
      script vet the data.
    - This should always work and be out of the way.  A line inside the function 
        can be 'import gist' to get the needed instance of class Gist.  This then
        just is a dict with the required parameters
        - gist *
        - desc
        - cat *
        - test *
        - todo
        - * means required
            - 

'''
from color import t

class Gist(dict):
    '''Dictionary to store the data for a gist.  Usage:
        - Create an instance
        - Call the empty() method
        - Fill out key 'gist' with a non-empty string
        - Fill out key 'test' with one of Gist.test entries
        - Call check() method:  if no exception, gist is OK
    The required keywords are
        gist    A one-line string that explains the content's purpose
        desc    A free-form textual description of the features
        cat     One or more category tokens for classification
        test    Token to describe how the module/script is tested
        todo    Tasks that need to be done
    '''
    # Required keywords
    required = "gist desc cat test todo".split()
    # Keywords that can only have these allowed values
    test = "notest run --test".split()
    def empty(self):
        'Create with required keywords that are empty strings'
        for i in Gist.required:
            self[i] = ""
    def check(self):
        'Verify has proper keys and values'
        o, n = t.sky, t.n
        # Must have required keys
        for i in Gist.required:
            if i not in self:
                raise ValueError(f"{o}Gist(dict) instance requires {i!r} keyword{n}")
        # The test key must have specific words
        s = self["test"]
        if s not in Gist.test:
            raise ValueError(f"{o}Gist(dict):  {s!r} not allowed key:\n  "
                                f"{' '.join(Gist.test)!r} are allowed{n}")
        # The 'gist' key must not be only whitespace
        s = self["gist"].strip()
        if not s:
            raise ValueError(f"{o}Gist(dict):  'gist' key must not be only whitespace")
    def __str__(self):
        s = []
        for i in Gist.required:
            s.append(f"{i!r}:  {self[i]}")
        return '\n'.join(s)

def GetGist():
    '''Construct the /plib/gist.Gist instance for this file.  This gist is 
    a dictionary used to capture essential information about the module or script to
    allow automated tools to summarize the module/script.
    '''
    gist = Gist()
    gist.empty()
    gist["test"] = "notest"
    gist["gist"] = "x"
    gist.check()
    return gist

print(GetGist())
