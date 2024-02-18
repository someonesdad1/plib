'''
Supplies the wsl variable, a boolean that is True if 'dpwsl' is defined to be 1
in the environment.

    This identifies that we're running under the Windows Subsystem for Linux.
'''
import os
wsl = bool(int(os.environ.get("dpwsl", 0)))
