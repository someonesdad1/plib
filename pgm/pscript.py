'''
Execute a python script when it changes.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2016 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Execute a python script when it changes
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import os
    import sys
    import time
    import hashlib
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
if 1:   # Global variables
    python = sys.executable
    ii = isinstance
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] script_name
      Monitor the python script with the name script_name; when it changes,
      run it.
    Options:
      -s    Use a hash to determin when the file has changed
      -t d  Set the delay in seconds between checks for changes
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-s"] = False     # Use hash if True
    d["-t"] = 0.25
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:hs:")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-n",):
            try:
                d["-n"] = abs(int(a))
                if not d["-n"]:
                    raise ValueError()
            except ValueError:
                Error("'{}' isn't a valid integer > 0".format(a))
        elif o in ("-t",):
            try:
                d["-t"] = abs(float(a))
            except ValueError:
                Error("'{}' isn't a valid float".format(a))
        elif o in ("-s",):
            d["-s"] = not d["-s"]
        elif o in ("-h", "--help"):
            Usage(d, status=0)
    if len(args) != 1:
        Usage(d)
    return args[0]
def Hash(d):
    '''Return an object used to determine if the file has changed.
    The default is to use the modification time; if you use the -s
    option, it will use a hash instead.
    '''
    if d["-s"]:
        h = hashlib.sha1()
        h.update(open(script_name, "rb").read())
        return h.hexdigest()
    else:
        return os.stat(script_name).st_mtime
if __name__ == "__main__":
    d = {}      # Options dictionary
    script_name = ParseCommandLine(d)
    hash0 = Hash(d)
    while True:
        time.sleep(d["-t"])
        hash = Hash(d)
        if hash != hash0:
            print("+")
            retval = os.system("{} {}".format(python, script_name))
            if retval:
                Error(f"'{script_name}' returned non-zero value")
            hash0 = hash
