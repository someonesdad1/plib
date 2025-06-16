'''
Launch files with their registered applications

    Windows:  You can compile the C++ application given below; it worked with Windows NT systems in
    the 1990's and 2000's.  The start.exe application can do the same thing and it's supplied with
    Windows.
    
    cygwin:  The cygstart.exe program does the work.
    
    Linux:  On a real Linux system, xdg-open works.  On WSL, you have to call explorer.exe on the
    file, but the twist is you have to cd to the file's directory first because Explorer is a
    strange application.
    
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # <utility> Launch files with their registered applications.  Works
        # on cygwin/Linux/Windows.
        ##∞what∞#
        ##∞test∞# ignore #∞test∞#
        pass
    if 1:  # Standard imports
        from pathlib import Path as P
        import getopt
        import os
        import platform
        import subprocess
        import sys
    if 1:  # Custom imports
        from wrap import dedent
        from wsl import wsl  # If wsl is 1, we're running under WSL under Windows
    if 1:  # Global variables
        ii = isinstance
        class G:
            pass
        g = G()
        g.system = None
if 0:  # C++ source code old Windows launcher app.exe
    '''
    Note:  the above Windows application can be used to launch files.
    Here's its source code:
    
    /****************************************************************************
    For each file on the command line, launch it with its registered
    application.  For Windows computers only.
    
    Compiled and tested with the 3.2.3 version of the MinGW g++ compiler:
        g++ -o app.exe app.cpp
        
    ----------------------------------------------------------------------
    
    Copyright (C) 2006 Don Peterson
    Contact:  gmail.com@someonesdad1
    
                    The Wide Open License (WOL)
    
    Permission to use, copy, modify, distribute and sell this software and
    its documentation for any purpose is hereby granted without fee,
    provided that the above copyright notice and this license appear in
    all copies.  THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT EXPRESS OR
    IMPLIED WARRANTY OF ANY KIND. See
    http://www.dspguru.com/wide-open-license for more information.
    ****************************************************************************/
    
    #include <iostream>
    #include <string>
    #include <cstdlib>
    #include <windows.h>
    
    using std::cerr;
    using std::string;
    using std::endl;
    
    const string edit    = "edit";
    const string explore = "explore";
    const string find    = "find";
    const string open    = "open";
    const string print   = "print";
    
    string program_name = "";
    
    // ----------------------------------------------------------------------
    
    void Usage(void)
    {
        cerr << "Usage:  " << program_name 
            << " [-a action] file1 [file2...]" << endl
            << "Launches each file with its registered application." << endl
            << "  Actions are:" << endl
            << "    edit" << endl
            << "    explore" << endl
            << "    find" << endl
            << "    open (this is the default)" << endl
            << "    print" << endl;
        exit(1);
    }
    
    // ----------------------------------------------------------------------
    
    void ErrorMessage(const char * file_to_launch, const string message)
    {
        cerr << file_to_launch << ":  " << message << endl;
    }
    
    // ----------------------------------------------------------------------
    
    void LaunchFile(const char * file_to_launch, const string action)
    {
        const char * command_parameters = "";
        const char * working_directory  = "";    
        const int open_in_normal_window = 1;
        
        HINSTANCE ret = ShellExecute(
                                    0,
                                    action.c_str(),
                                    file_to_launch,
                                    command_parameters,
                                    working_directory,
                                    open_in_normal_window
                                    );
                                    
        int return_value = int(ret);
        const int failed_status = 32;
        if (return_value > failed_status)
            return;  // Successfully executed
            
        // The call did not succeed; inform the user of the problem.  These
        // ShellExecute return values are from the MSDN help shipped with the
        // Visual C++ 2003 package.
        
        switch (return_value)
        {
            case 0:                    // Fall through intentional
            case SE_ERR_OOM:
                ErrorMessage(file_to_launch, "Out of memory");
                break;
            case ERROR_FILE_NOT_FOUND:
                ErrorMessage(file_to_launch, "File not found");
                break;
            case ERROR_PATH_NOT_FOUND:
                ErrorMessage(file_to_launch, "Path not found");
                break;
            case ERROR_BAD_FORMAT:
                ErrorMessage(file_to_launch, "EXE file is invalid");
                break;
            case SE_ERR_ACCESSDENIED:
                ErrorMessage(file_to_launch, "Access denied");
                break;
            case SE_ERR_ASSOCINCOMPLETE:
                ErrorMessage(file_to_launch, 
                            "File name association incomplete or invalid");
                break;
            case SE_ERR_DDEBUSY:
                ErrorMessage(file_to_launch, "DDE busy");
                break;
            case SE_ERR_DDEFAIL:
                ErrorMessage(file_to_launch, "DDE failed");
                break;
            case SE_ERR_DDETIMEOUT:
                ErrorMessage(file_to_launch, "DDE timed out");
                break;
            case SE_ERR_DLLNOTFOUND:
                ErrorMessage(file_to_launch, "DLL not found");
                break;
            case SE_ERR_NOASSOC:
                ErrorMessage(file_to_launch, 
                            "No application associated with file");
                break;
            case SE_ERR_SHARE:
                ErrorMessage(file_to_launch, "Sharing violation");
                break;
            default:
                break;
        }
    }
    
    int main(int argc, char** argv)
    {
        program_name  = argv[0];
        string action = open;    // Default action is to open the file
        
        if (argc < 2)
            Usage();
            
        // Check for -a option
        argv++;
        if (argv[0][0] == '-' and argv[0][1] == 'a')
        {
            argv++;
            if (not *argv)
                Usage();
                
            // Make sure the action is allowed
            string action = *argv;
            if (action != edit    and 
                action != explore and 
                action != find    and 
                action != open    and 
                action != print)
            {
                Usage();
            }
            argv++;
            if (not *argv)
                // Need at least one file
                Usage();
        }
        
        while (*argv)
        {
            LaunchFile(*argv, action);
            argv++;
        }
        
        return 0;
    }
    '''
if 1:  # Core functionality
    def GetSystem():
        '''Set g.system to one of the following strings:
            cygwin      Running under cygwin
            linux       Running under a real Linux system, not WSL
            wsl         Running Linux under WSL
            mac       * Running under Apple's UNIX
            windows   * Running under Windows
        Note * means not supported yet.
        '''
        s = platform.system()
        if s.startswith("CYGWIN_NT"):
            g.system = "cygwin"
        elif s.startswith("Linux"):
            g.system = "wsl" if wsl else "linux"
        else:
            raise ValueError("{s!r} not supported for platform.system()")
    def RegisteredOpen(file):
        '''Open the indicated file with its registered application.  file must be a string
        or a Path instance.
        '''
        if ii(file, str):
            p = P(file)
        elif ii(file, P):
            p = file
        else:
            raise TypeError(f"'{file}' must be a string or a pathlib.Path instance")
        if not p.exists():
            raise ValueError(f"'{p}' does not exist")
        cwd = os.getcwd()
        try:
            dirname = p.parent
            filename = p.name
            os.chdir(dirname)
            if g.system == "wsl":
                # Running under Windows in Windows Subsystem for Linux.  The method is to use
                # explorer.exe to open files.  To get this to work, we have to cd to the file's
                # directory.  It appears Explorer returns 1 under all conditions.
                r = subprocess.run(f"explorer.exe {filename}", shell=True)
            elif g.system == "cygwin":
                # Must be cygwin; file can be opened with cygstart.exe.
                r = subprocess.run(f"cygstart {filename}", shell=True)
            elif g.system == "linux":
                # Older method worked a decade or two ago, needs to be tested on a Linux box
                subprocess.call(("xdg-open", filename))
            else:
                raise ValueError(f"{g.system!r} not supported yet")
        except Exception as e:
            print(f"{e}", file=sys.stderr)
        finally:
            os.chdir(cwd)
    def Launch(*files):
        for file in files:
            RegisteredOpen(file)
    # Make sure we know the system when we get imported
    GetSystem()
if __name__ == "__main__":
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        name = sys.argv[0]
        print(
            dedent(f'''
        Usage:  {name} [options] file1 [file2 ...]
          Launch the files with their registered applications. 
        ''')
        )
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        if not args:
            Usage()
        return args
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    Launch(*files)
