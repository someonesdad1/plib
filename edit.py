"""
Provide Edit(*p) to allow for editing a file.
"""

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
    ##∞test∞# ignore #∞test∞#
    pass
if 1:  # Standard imports
    import os
    import pathlib
    import subprocess
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import wrap, dedent
if 1:  # Global variables
    P = pathlib.Path
    ii = isinstance
    editor = os.environ["EDITOR"]


def Edit(*files, strict=False):
    """Launch editor on those files that exist.  If strict is True, raise
    an exception if there are no files.  Otherwise, just return quietly.
    """
    keep = []
    for file in files:
        p = P(file)
        if p.exists():
            keep.append(file)
    if not keep:
        if strict:
            raise ValueError("No files to edit")
        return
    e = [editor] + keep
    subprocess.call(e)


if __name__ == "__main__":
    # Test with files from command line
    if len(sys.argv) == 1:
        print("Include files to edit on command line")
    else:
        Edit(*sys.argv[1:])
