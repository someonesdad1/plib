'''
Provides RegisteredOpen(), which lets you open a file with its registered application

    This should be trivial, but there's no OS-independent way to do it in python.  This module
    covers cygwin and WSL, the two environments I currently work in.  Extending to Linux and Mac
    should be pretty trivial.
    
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Open a file with its registered application oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2024 Don Peterson oo>
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
        from pathlib import Path as P
        import os
        import subprocess
        import sys
    if 1:  # Custom imports
        from wsl import wsl  # wsl is True when running under WSL Linux
    if 1:  # Global variables
        pass
if 1:  # Core functionality
    def RegisteredOpen(file):
        '''Open the indicated file with its registered application.  file must be a string
        or a Path instance.
        '''
        if isinstance(file, str):
            p = P(file)
        elif isinstance(file, P):
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
                subprocess.run(cmd, shell=True)
            else:
                # Must be cygwin; file can be opened with cygstart.exe.
                cmd = f"cygstart {filename}"
                subprocess.run(cmd, shell=True)
        except Exception as e:
            print(f"{e}")
        finally:
            os.chdir(cwd)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} [file1 [file2 ...]]")
        print("  Opens files with registered applications.")
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
