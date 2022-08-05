'''
class Tee:    Class to let you tee streams' output to a file
Print():      A simpler way to do the same thing
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <programming> Tee streams' output to other streams.
    #∞what∞#
    #∞test∞# --test #∞test∞#
    pass
if 1:   # Standard imports
    import sys

def Print(*p, **kw):
    '''Print like the builtin print() and then print to any streams in
    Print.streams.  Here's a typical use case:  we want a script's
    output to go to stdout and a file, acting like a tee.
 
        # We want the script's output to go to stdout and a file,
        # acting like a tee.  Without Print's features, this could be a
        # lot of code editing.  Here's the easy way:
            Print.print = print     # Save the original print function
            print = Print           # Substitute our function
            Print.streams = [open(file, "w")]   # Add another stream
        # Now your code uses 'print' as you're accustomed to and
        # there's no need need to change any code).  Because you're
        # really calling Print() behind the scenes, the output is also
        # going to the opened file stream.
            <Code using 'print'>
        # We're finished.  You can either exit or fix the plumbing to
        # go back to regular behavior.
            Print.streams.clear()
            print = Print.print
        # Now we're back to standard python behavior.  Note we left
        # Print.print defined in case we want it again.
 
    print's keyword dictionary is only allowed to have the four keys
    'sep', 'end', 'file', and 'flush'.  Sometimes I like to define
    other functions with parameters similar to print, but allowing more
    keywords.  Without the True conditional, a call to print() with
    unsupported keywords will result in an exception.
    '''
    Print.print(*p, **kw)
    k = kw.copy() if Print.streams else None # Don't mess up caller's kw
    if True:
        if not hasattr(Print, "allowed"):
            Print.allowed = set("sep end file flush".split())
        for key in k:
            if key not in Print.allowed:
                del k[key]
    for stream in Print.streams:
        k["file"] = stream
        Print.print(*p, **k)
Print.print = print     # Make sure print() is stored away

class Tee:
    '''This behaves like an output stream object.  Run this file as a
    script to see an example.
    '''
    # Idea from https://shallowsky.com/blog/programming/python-tee.html
    def __init__(self, *streams):
        self.streams = streams
        # Check for needed methods
        for i in self.streams:
            for m in "write flush __del__".split():
                if not hasattr(i, m):
                    raise ValueError(f"Argument '{i}' lacks stream methods")
    def __del__(self):
        for i in self.streams:
            if i != sys.stdout and i != sys.stderr:
                i.close()
    def write(self, s):
        for i in self.streams:
            i.write(s)
    def flush(self):
        for i in self.streams:
            i.flush()

if 1:   # Demo code
    def SetUp():
        # Colorize the output to the streams to identify them.
        t.s = t("grnl")     # Things sent to stdout are green
        t.e = t("redl")     # Things sent to stderr are red
        t.o = t("cynl")     # The 'other' messages are cyan
        # This is the file where we'll send the data
        g.file = "tee.test"
    def DemoPrint():
        SetUp()
        # Hook up plumbing
        stream = open(g.file, "w")
        Print.streams = [stream]
        print = Print 
        # Send our data to the screen and the file
        print(f"{t.s}Message to stdout{t.n}")
        print(f"{t.e}Message to stderr{t.n}", file=sys.stderr)
        # Now should have green and red lines on screen and in the file.
        # Hook the plumbing back the way it was.
        Print.streams.clear()
        stream.close()
        print = Print.print
        # These messages should not show up in the file, demonstrating the tees
        # have been disconnected.
        print(f"{t.o}Last message to stdout{t.n}")
        print(f"{t.o}+ Last message to stderr{t.n}", file=sys.stderr)
    def DemoTee():
        SetUp()
        # Save the original streams
        saved = sys.stdout, sys.stderr
        # We want output to go to this file and the screen
        out = open(file, "w")
        # Tee stdout and the file together
        tee_stdout = Tee(out, sys.stdout)
        sys.stdout = tee_stdout
        # Tee stderr and the file together
        tee_stderr = Tee(out, sys.stderr)
        sys.stderr = tee_stderr
        # Now the script' output is sent to these Tee instances by normal use
        # of the print() method.
        print(f"{t.s}Message to stdout{t.n}")
        print(f"{t.e}Message to stderr{t.n}", file=sys.stderr)
        # We're done with output to the file.  Hook up the original plumbing
        # and make sure the tees aren't around.
        sys.stdout, sys.stderr = saved
        try:
            del tee_stdout
        except NameError:
            pass
        try:
            del tee_stderr
        except NameError:
            pass
        # These messages should not show up in the file, demonstrating the tees
        # have been disconnected.
        print(f"{t.o}Last message to stdout{t.n}")
        print(f"{t.o}+ Last message to stderr{t.n}", file=sys.stderr)
    def ShowFileResults():
        # Print the contents of the file to stdout to show we captured what was
        # intended.
        print("-"*40)
        print("Contents of the file that captured the data:")
        print(open(g.file).read(), end="")
        os.unlink(g.file)     # Delete the file

if __name__ == "__main__": 
    # Tee test
    import os
    from color import TRM as t
    import tempfile
    from lwtest import run, raises, Assert
    from io import StringIO
    from pdb import set_trace as xx 
    class g:
        pass
    # Note:  I haven't written a test for the Tee class because I prefer to
    # use the Print function.
    def TestPrint():
        '''Send output to both a file and a StringIO object and verify 
        they are the same.
        '''
        file = tempfile.mkstemp(text=True)[1]
        st = open(file, "w")
        strm = StringIO()
        s = "Test string"
        Print.streams = [strm]
        Print(s, file=st)
        st.close()
        file_string = open(file).read()
        strm_string = strm.getvalue()
        Assert(file_string == s + "\n")
        Assert(file_string == strm_string)
        os.unlink(file)
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        exit(run(globals(), halt=True)[0])
    else:
        print("Example of Print() use")
        DemoPrint()
        ShowFileResults()
