'''
Provides SetDebugger.  Use this module when debugging things like color.py,
which will cause a circular import if you try to call debug.SetDebugger().
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Debugging with circular imports oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2009, 2014 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ notest oo>
        <oo todo ∞ oo>
    '''
    if 1:   # Standard imports
        import sys
        import traceback as TB
        import bdb
        import pdb
    if 1:   # Custom imports
        pass
if 1:   # Core functionality
    def TraceInfo(type, value, traceback):
        '''Start the debugger after an uncaught exception.  From Thomas
        Heller's post on 22 Jun 2001 http://code.activestate.com/recipes/65287
        Also see page 435 of "Python Cookbook".
        '''
        # Updated first test logic from https://gist.github.com/rctay/3169104
        if (
            hasattr(sys, "ps1")
            or not sys.stderr.isatty()
            or not sys.stdout.isatty()
            or not sys.stdin.isatty()
            or issubclass(type, bdb.BdbQuit)
            or issubclass(type, SyntaxError)
        ):
            # You are in interactive mode or don't have a tty-like device,
            # so call the default hook.
            sys.__excepthook__(type, value, traceback)
        else:
            # You are not in interactive mode; print the exception.
            TB.print_exception(type, value, traceback)
            print()
            # Now start the debugger
            pdb.pm()
    def SetDebugger():
        '''If you execute this function, TraceInfo() will be called when
        you get an unhandled exception and you'll be dumped into the
        debugger.
        '''
        sys.excepthook = TraceInfo
