'''
Set the mod time of a set of files to that of a reference file
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Set the mod time of a set of files to that of a reference file
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import os
if 1:   # Custom imports
    from wrap import dedent
def Usage(status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} mainfile file1 [file2 ...]
      Change the modification times of file1, file2, ... to be the same as
      mainfile.
    '''))
    exit(status)
if __name__ == "__main__": 
    args = sys.argv[1:]
    if len(args) < 2:
        Usage()
    mainfile = args[0]
    sd = os.stat(mainfile)
    times = (sd.st_atime, sd.st_mtime)
    for file in args[1:]:
        os.utime(file, times)
