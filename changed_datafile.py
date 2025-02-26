"""
This module lets an application have a function run when a file's contents
or modification time changes.

    A use case for this tool is an application that uses a data file for
    the application's data (e.g., a script that calculates the properties
    of an ideal gas).  The script user can edit the data file in one
    terminal window and the application can run in another window.  When
    the user saves the data file, the application's callback function is
    called, letting the application e.g. update the output screen by
    reading in the changed variables from the data file.

How it works:  The CheckFile function is run in another process and calls
the callback function when the datafile changes (either its MD5 hash or
modification time).

Usage:

    # file = datafile name
    # Callback = callback function to be called when datafile changes

    import changed_datafile
    import multiprocessing as mp

    # Use an integer variable to tell the child process to exit
    done = mp.Value("i", 0)

    p = mp.Process(target=changed_datafile.CheckFile,
                   args=(file, Callback, done))
    p.start()
        ... run main application code ...
    done.value = 1  # This signals child process to return
    p.join()        # Main process blocks until child process returns

Run this file as a script to see a demonstration.

"""

import hashlib
import os
import time
import pathlib

ii = isinstance


def CheckFile(file, func, done, hash=False):
    """Call the function func when the hash or mtime of file changes.
    done is a multiprocessing.Value variable for an integer; when it is
    True, this function returns.  Note func has no arguments.

    file can be a string or a pathlib.Path instance.

    Set CheckFile.delay in seconds to control how often the check is
    made.  You can experiment with the value to get the application
    response you need.

    Set CheckFile.dbg to True for debug printing to stdout.
    """

    def GetFileState(file, hash):
        if hash:
            m = hashlib.md5()
            b = open(file, "rb").read() if ii(file, str) else p.read_bytes()
            m.update(b)
            return m.digest()
        else:
            m = os.stat(file) if ii(file, str) else file.stat()
            return m.st_mtime

    if CheckFile.dbg:
        print(f"CheckFile child process started (pid = {os.getpid()})")
        print(f"  file = {file!r}")
        print(f"  func = {func}")
        print(f"  done = {done.value}\n")
    if done.value:
        if CheckFile.dbg:
            print(f"\nCheckFile child process exiting immediately")
        return
    old_state = GetFileState(file, hash)
    while True:
        if done.value:
            if CheckFile.dbg:
                print(f"\nCheckFile child process exiting (pid = {os.getpid()})")
            return
        time.sleep(CheckFile.delay)
        new_state = GetFileState(file, hash)
        if new_state != old_state:
            func()  # Alert other process file changed
            old_state = new_state
            time.sleep(CheckFile.delay)


CheckFile.delay = 0.5
CheckFile.dbg = False

if __name__ == "__main__":
    from timer import sw
    import multiprocessing as mp

    sw.reset()  # Use sw() to print out elapsed time

    def Callback():
        print(f"  Callback called at {sw()} s")

    done = mp.Value("i", 0)
    file = "aa"
    with open(file, "w") as fp:
        fp.write("Simple data file")
    runtime = 10
    print(f"Make changes to file {file!r} within {runtime} seconds\n")
    CheckFile.dbg = True  # Turn on debug messages
    if CheckFile.dbg:
        print(f"Parent process started (pid = {os.getpid()})")
    p = mp.Process(target=CheckFile, args=(file, Callback, done))
    p.start()
    while True:
        if sw() > runtime or not p.is_alive():
            done.value = 1  # Make check process return
            break  # Exit after this time
    p.join()
    if CheckFile.dbg:
        print(f"Parent process exit (pid = {os.getpid()})")
