'''
This script provides Modified(), which prints a colored string to stderr
to notify of a change in a file.

    Use case:  If you're working on a modification to a core library file,
    it's common to put mainline test code in to test your changes, often
    followed by an exit() call.  However, this then breaks a lot of scripts
    that depend on this library.  If you use e.g.
    Modified(Path(Path("myscript.py"), "Working on bug fix")) just before
    the exit() call, the message will be seen when other code tries to use
    that library and you'll be able to fix things.
    
Example usage:

    from modified import Modified, Path
    Modified(Path("myscript.py"))
    exit()
    
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Function to notify of modified script oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2023 Don Peterson oo>
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
    if 1:  # Standard imports
        from pathlib import Path
    if 1:  # Custom imports
        from color import t
    if 1:  # Global variables
        pass
if 1:  # Core functionality
    def Modified(file, msg=None):
        '''file must be a valid Path object.  Prints msg in color to stderr if
        it's present.
        '''
        assert isinstance(file, Path)
        if msg is None:
            t.print(f"{t('redl')}{file.resolve()} is modified")
        else:
            t.print(f"{t('magl')}{file.resolve()} {msg}")
