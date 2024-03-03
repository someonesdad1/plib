'''
Provides RegisteredOpen(), which lets you open a file with its registered application

    This should be trivial, but there's no OS-independent way to do it in python.  This module
    covers cygwin and WSL, the two environments I currently work in.  Extending to Linux and Mac
    should be pretty trivial.

'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Module to open a file with its registered application
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from pathlib import Path as P
        import os
        import subprocess
        import sys
    if 1:   # Custom imports
        from wsl import wsl     # wsl is True when running under WSL Linux
    if 1:   # Global variables
        ii = isinstance
if 1:   # Core functionality
    def RegisteredOpen(file):
        '''Open the indicated file with its registered application.  file must be a string
        or a Path instance.
        '''
        if ii(file, str):
            p = P(file)
        elif ii(file, P):
            p = file
        else:
            raise TypeError(f"{file} must be a string or a pathlib.Path instance")
        if not p.exists():
            raise ValueError(f"{str(p)!r} does not exist")
        cwd = os.getcwd()
        try:
            dirname = p.parent
            filename = p.name
            os.chdir(dirname)
            if wsl:
                # Running under Windows in Windows Subsystem for Linux.  The method is to use
                # explorer.exe to open files.  To get this to work, we have to cd to the file's
                # directory.  It appears Explorer returns 1 under all conditions.
                cmd = f"explorer.exe {filename}"
                r = subprocess.run(cmd, shell=True)
            else:
                # Must be cygwin; file can be opened with cygstart.exe.
                cmd = f"cygstart {filename}"
                r = subprocess.run(cmd, shell=True)
        except Exception as e:
            print(f"{e}")
        finally:
            os.chdir(cwd)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} [file1 [file2 ...]]")
        print(f"  Opens files with registered applications.")
        exit(1)
    else:
        status = 0
        for file in sys.argv[1:]:
            try:
                RegisteredOpen(file)
            except Exception as e:
                print(f"{e}")
                status += 1
        # Returned status is number of files that couldn't be opened
        exit(status)
