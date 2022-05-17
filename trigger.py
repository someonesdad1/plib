'''
Finds trigger strings in text files

    Run as a script to see an example.

    The basic purpose is to provide the ability to find and update
    "trigger" strings in a file.  An example of a trigger string in a
    python file might be 

        #∞license∞#
        # Licensed under the Open Software License version 3.0.
        # See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#

    To find this and similar trigger strings, you'd use the following code:

        import pathlib
        t = Trigger()
        p = pathlib.Path("myscript.py")
        t(p)  # Trigger.__call__

    The last statement reads the file's text in and parses the trigger
    strings.  The Trigger class is derived from dict, so the names of the
    trigger strings are the keys of the dict and the value for the key
    "license" is the text between the two occurrences of "#∞license∞#".

    You can change the text between the trigger strings:

        t["license"] = new_license_text

    and call t.write() to write the information back to the file.
'''
#∞test∞# ignore #∞test∞#
import pathlib
import re
from pdb import set_trace as xx 
P = pathlib.Path
class Trigger(dict):
    def __new__(cls, start="#∞", end="∞#", allowed="[A-Za-z0-9_]"):
        '''The trigger string will be the string X between the start and
        end strings.  The allowed string defines the python re
        characters allowed to be in the trigger string.
        '''
        instance = super().__new__(cls)
        instance.start = start
        instance.end = end
        instance.allowed = end
        instance.file = None
        instance.text = None
        instance.not_allowed = ValueError("Operation not allowed")
        regexp = f"{start}({allowed}+){end}"
        instance.r = re.compile(regexp)
        return instance
    def __call__(self, file):
        '''Given file (a str or pathlib.Path), get all trigger strings'
        text.
        '''
        self.clear()
        self.filled = False     # Allow changes
        # Get the file's string
        if isinstance(file, str):
            p = P(file)
        elif not isinstance(file, P):
            raise TypeError("file must be str or pathlib.Path")
        else:
            p = file
        self.text = p.read_text()
        self.file = p
        if p.resolve() == P("/plib/trigger.py"):
            return None
        # Get the file's trigger strings
        self.triggers = set(self.r.findall(self.text))
        # Get the text associated with each trigger string and put it
        # into the dictionary.  There must be only one string in the
        # file for each trigger string.
        for trigger in self.triggers:
            s = f"{self.start}{trigger}{self.end}"
            r = re.compile(f"{s}(.+?){s}", re.S)
            t = r.findall(self.text)
            if not t:
                msg = f"Trigger '{trigger}' only occurred once"
                raise ValueError(msg)
            elif len(t) != 1 or trigger in self:
                msg = f"{p}:  More than one string for trigger '{trigger}'"
                raise ValueError(msg)
            self[trigger] = t[0]
        self.filled = True
        return self
    def __delitem__(self, key):
        raise ValueError("Deletion not allowed")
    def __setitem__(self, key, value):
        if not self.filled:
            super().__setitem__(key, value)
            return
        if key not in self:
            raise KeyError(f"'{key}' not in dict")
        # Set the new value
        super().__setitem__(key, value)
    def write(self):
        '''Assuming the object has been filled, write the new object out
        to the file, including any changes made in the trigger string
        contents.
        '''
        if self.text is None:
            raise ValueError("call() on a file hasn't been done")
        # self.text contains the text of the file read in call().  This
        # file is self.file.
        for trigger in self.triggers:
            s = f"{self.start}{trigger}{self.end}"
            r = re.compile(f"{s}(.+?){s}", re.S)
            trig = f"{self.start}{trigger}{self.end}"
            repl = f"{trig}{self[trigger]}{trig}"
            self.text = r.sub(repl, self.text)
        #xx Need to test write functionality
        print("New text")
        pp(self.text)
        exit()
    ## Disable other dict methods
    def get(self, key, default=None): raise self.not_allowed
    def pop(self, key, default=None): raise self.not_allowed
    def popitem(self): raise self.not_allowed
    def setdefault(self, key, default=None): raise self.not_allowed
    def update(self, other=None): raise self.not_allowed
if __name__ == "__main__": 
    from pprint import pprint as pp
    from lwtest import raises
    p = None
    def Setup():
        global p
        p = pathlib.Path("/plib/trigger.tmpfile")
    def Teardown():
        p.unlink()
        assert(not p.is_file())
    def Separator():
        print(f"{'-'*70}")
    def CheckDisabled():
        'Show that the disabled methods result in an exception'
        text = "Dummy text"
        p.write_text(text)
        t = Trigger()
        t(p)    # Load the file
        key = "dummy"
        for i in ((t.get, key), (t.pop, key), (t.setdefault, key),
                  (t.popitem,), (t.update,)):
            raises(ValueError, *i)
    def ShowStrings():
        text = '''
        #∞who∞#
            This is the text between the trigger string pair.
            It can be multiple lines.  All of the whitespace
            is included.
        #∞who∞#
        #∞what∞# The text can be one line. #∞what∞# 
        '''
        print(f"Demo of {__file__}'s Trigger() object:\n")
        print("Here's our text:")
        print(text)
        p.write_text(text)
        t = Trigger()
        t(p)    # Load the file
        print("Here's the dictionary of extracted strings:\n")
        pp(t)
    def SingleTriggerStringException():
        Separator()
        text = "#∞how∞#"
        p.write_text(text)
        t = Trigger()
        print("You'll get a ValueError for a single trigger string:")
        try:
            t(p)    # Try to load the file
        except ValueError as e:
            print(f"  {e}")
    def ReplaceText():
        Separator()
        text = '''
        #∞who∞# 
            Who's text on
            multiple lines.
        #∞who∞#
        #∞what∞# What's text on one line. #∞what∞# 
        '''
        p.write_text(text)
        print("Showing how text can be replaced.  We'll exchange the 'who'")
        print("and 'what' values.\n")
        print("Original string:")
        pp(text)
        print()
        t = Trigger()
        t(p)    # Get our contents
        # Swap who and what strings
        tmp = t["who"]
        t["who"] = t["what"]
        t["what"] = tmp
        t.write()
        t.clear()
        t(p)    # Get our contents
        print("Swapped strings:")
        pp(t)
    Setup()
    CheckDisabled()
    ShowStrings()
    SingleTriggerStringException()
    ReplaceText()
    Teardown()
