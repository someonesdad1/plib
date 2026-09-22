'''
Provide Edit(*p) to allow for editing a file.

    Example:  suppose you want to use /usr/bin/vi (which is vim) and you want to use the
    -c option to position the editor on the first line of the file myfile.py that is
    found by the search for 'def MyFunction'.  You'd use the following call to Edit:

            edit.Edit("myfile.py", opt=["-c", "/def MyFunction"])

    after making sure the global variable 'editor' is set to "/usr/bin/vi".  Each one of
    the strings in opt wind up being inserted as command options just after the call to
    vi.
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Provides Edit() for editing a file oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2021 Don Peterson oo>
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
        import os
        import pathlib
        import subprocess
        import sys
    if 1:  # Custom imports
        pass
    if 1:  # Global variables
        P = pathlib.Path
        editor = os.environ["EDITOR"]
if 1:  # Core functionality
    def Edit(*files, strict=False, opt=None):
        '''Launch editor on those files that exist.  If strict is True, raise an
        exception if there are no files or a file doesn't exist.  Otherwise, just return
        quietly.  opt is a list of option strings to append before the list of files.
        '''
        files_to_edit = []
        for file in files:
            p = P(file)
            if p.exists():
                files_to_edit.append(file)
            else:
                if strict:
                    raise ValueError(f"{file!r} doesn't exist")
        if not files_to_edit:
            if strict:
                raise ValueError("No files to edit")
            return
        # Construct editing string
        e = [editor]
        if opt:
            if isinstance(opt, (list, tuple)):
                e.extend(list(opt))
            elif isinstance(opt, str): 
                e += [opt]
            else:
                raise TypeError("opt must be string or list/tuple of strings")
        e += files_to_edit
        subprocess.call(e)

if __name__ == "__main__":
    # Test with files from command line
    if len(sys.argv) == 1:
        print("Include files to edit on command line")
    else:
        Edit(*sys.argv[1:], strict=True)
