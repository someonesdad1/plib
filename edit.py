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
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # <utility> Allows editing one or more files with Edit(*files).
    ##∞what∞#
    ##∞test∞# notest #∞test∞#
    pass
if 1:  # Standard imports
    import os
    import pathlib
    import subprocess
    import sys
if 1:  # Custom imports
    pass
if 1:  # Global variables
    P = pathlib.Path
    ii = isinstance
    editor = os.environ["EDITOR"]
def Edit(*files, strict=False, opt=None):
    '''Launch editor on those files that exist.  If strict is True, raise
    an exception if there are no files.  Otherwise, just return quietly.
    '''
    files_to_edit = []
    for file in files:
        p = P(file)
        if p.exists():
            files_to_edit.append(file)
    if not files_to_edit:
        if strict:
            raise ValueError("No files to edit")
        return
    e = [editor]
    if opt:
        if ii(opt, (list, tuple)):
            e.extend(list(opt))
        elif ii(opt, str): 
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
        Edit(*sys.argv[1:])
