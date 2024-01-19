'''
Supplies the wsl variable, a boolean that is True if WSL is defined to be 1
in the environment.
'''
import os
wsl = bool(int(os.environ.get("WSL", 0)))
