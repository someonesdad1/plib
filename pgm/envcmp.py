'''
Tool to compare shell environment variables and functions.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2005, 2011 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Compare environment variables and functions
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import re
    import getopt
    import os
    import tempfile
    import subprocess
    import time
if 1:   # Custom imports
    from wrap import dedent
if 1:   # Global variables
    # Set wdiff to a program like kdiff3 or WinMerge.  If you don't have
    # such a program, set it to None.
    wdiff = "d:/bin/TortoiseHg104/kdiff3.exe"
    wdiff = None
    wdiff = "d:/bin/winmerge/WinMergeU.exe"
    # Regular expressions 
    bash_func = re.compile("^.* \(\)$")
    bash_env = re.compile("^.*=.*$")
    # The following string is used to identify the functions dictionary
    # in the dictionary containing the environment variables.  It is a
    # string that is not allowed as a shell variable name.
    func_key = "\nfunc"
def GetTempFilename(filename):
    '''Get a temporary file name and append filename to the file's name.
    This is intended to provide a temporary file for use with displaying
    differences in the visual diff program.
    '''
    t = tempfile.NamedTemporaryFile(delete=False)
    name = t.name
    head, tail = os.path.split(name)
    return os.path.join(head, ''.join([tail, ".", filename]))
def Usage():
    print(dedent(f'''
    Usage:  {sys.argv[0]}  A  B
      Compares two files A and B containing the output of a bash shell 'set'
      command and reports:
        * Those environment variables in A but not in B
        * Those environment variables in B but not in A
        * Those environment variables that are common and equal
        * Those environment variables that are common but unequal
      Note that shell functions are ignored; use the -f option if you want
      them compared.
    Options
        -A      Do not show those only in A
        -B      Do not show those only in B
        -e      Do not show common and equal
        -f      Compare only the shell functions in the listing.
        -u      Do not show common and unequal
        -v      Show the values of the environment variables in the output.
        -w      Create a visual diff viewing of the common but unequal variables
                or functions.
    '''))
    exit(1)
def Categorize(dictA, dictB):
    '''Return four sets that encapsulate the sameness and
    differences of the two given dictionary's keys.  The keys are either
    the function name lines or the environment variable names.  The values
    are the values of the environment variables or the function body
    strings.
    '''
    common_equal = set()
    common_unequal = set()
    only_in_A = set()
    only_in_B = set()
    all_keys = set()
    Akeys = list(dictA.keys())
    Bkeys = list(dictB.keys())
    for key in Akeys + Bkeys:
        if key != func_key:
            all_keys.add(key)
    for key in all_keys:
        if key in dictA:
            if key in dictB:
                if dictA[key] == dictB[key]:
                    common_equal.add(key)
                else:
                    common_unequal.add(key)
            else:
                only_in_A.add(key)
        else:
            only_in_B.add(key)
    return common_equal, common_unequal, only_in_A, only_in_B
def Compare(dictA, dictB, d):
    if d["-f"]:
        CompareFunc(dictA, dictB, d)
    else:
        CompareEnv(dictA, dictB, d)
def CompareEnv(dictA, dictB, d):
    '''dictA and dictB are dictionaries that are keyed by environment
    variable names.  However, the entry keyed by the string in the global
    variable func_key is another dictionary that is keyed by the function
    names; the values are lists of the function's lines.
 
    d is a dictionary of the command line settings.
    '''
    common_equal, common_unequal, only_in_A, only_in_B = \
        Categorize(dictA, dictB)
    if d["-w"]:
        # Send common_unequal variables to visual diff program
        tmpfileA = GetTempFilename(d["fileA"])
        tmpfileB = GetTempFilename(d["fileB"])
        DumpEnvToFile(tmpfileA, common_unequal, dictA)
        DumpEnvToFile(tmpfileB, common_unequal, dictB)
        subprocess.Popen([wdiff, tmpfileA, tmpfileB])
        # Delay for a bit, then delete the files
        time.sleep(1)
        try:
            os.remove(tmpfileA)
            os.remove(tmpfileB)
        except Exception:
            pass
    else:
        # Print report
        if not d["-e"] and common_equal:
            print("Common and equal variables:")
            PrintKeys(common_equal, d, dictA)
        if not d["-u"] and common_unequal:
            print("Common and unequal variables:")
            PrintKeys(common_unequal, d)
        if not d["-A"] and only_in_A:
            print("Only in file %s:" % d["fileA"])
            PrintKeys(only_in_A, d, dictA)
        if not d["-B"] and only_in_B:
            print("Only in file %s:" % d["fileB"])
            PrintKeys(only_in_B, d, dictB)
def DumpEnvToFile(file, variables, dict):
    ofp = open(file, "w")
    vars = list(variables)
    vars.sort()
    for var in vars:
        ofp.write("%s=%s\n" % (var, dict[var]))
def CompareFunc(dictA, dictB, d):
    '''dictA and dictB are dictionaries that are keyed by function
    names; the values are lists of the function's lines.
 
    d is a dictionary of the command line settings.
    '''
    # Get dictionaries of the functions
    A, B = dictA[func_key], dictB[func_key]
    common_equal, common_unequal, only_in_A, only_in_B = Categorize(A, B)
    if d["-w"]:
        # Send common_unequal variables to visual diff program
        tmpfileA = GetTempFilename(d["fileA"])
        tmpfileB = GetTempFilename(d["fileB"])
        DumpFuncToFile(tmpfileA, common_unequal, A)
        DumpFuncToFile(tmpfileB, common_unequal, B)
        subprocess.Popen([wdiff, tmpfileA, tmpfileB])
        # Delay for a bit, then delete the files
        time.sleep(1)
        try:
            os.remove(tmpfileA)
            os.remove(tmpfileB)
        except Exception:
            pass
    else:
        # Print report
        if not d["-e"] and common_equal:
            print("Common and equal functions:")
            PrintKeys(common_equal, d)
        if not d["-u"] and common_unequal:
            print("Common and unequal functions:")
            PrintKeys(common_unequal, d)
        if not d["-A"] and only_in_A:
            print("Only in file %s:" % d["fileA"])
            PrintKeys(only_in_A, d)
        if not d["-B"] and only_in_B:
            print("Only in file %s:" % d["fileB"])
            PrintKeys(only_in_B, d)
def DumpFuncToFile(file, functions, dict):
    '''Write the indicated functions to a file.
    functions is a set of function names.
    dict is a dictionary containing the function's lines.
    '''
    ofp = open(file, "w")
    funcs = list(functions)
    funcs.sort()
    for func in funcs:
        ofp.write("%s\n" % func)
        for i in dict[func]:
            ofp.write("  %s\n" % i)
        ofp.write("\n")
def PrintKeys(set_of_keys, settings, dict=None):
    '''Print the set_of_keys after sorting them alphabetically.  If
    settings["-v"] is True, then also print the environment variables'
    values after them (this won't be done unless the associated dictionary
    in dict is also given).
    '''
    keys, indent = list(set_of_keys), "  "
    keys.sort()
    for key in keys:
        if settings["-v"] and dict is not None:
            print(' = '.join([indent + key, dict[key]]))
        else:
            print(''.join([indent, key]))
def BuildDict(file):
    lines = [i.strip() for i in open(file).readlines()]
    dict = {}
    for i in range(len(lines)):
        if bash_env.match(lines[i]):
            loc = lines[i].find("=")
            if loc == -1:
                msg = "Error:  bad line %d in file '%s'\n" % (i + 1, file)
                sys.stderr.write(msg)
                exit(1)
            name, value = lines[i][:loc], lines[i][loc + 1:]
            dict[name] = value
        else:
            dict[func_key] = ParseFunctions(lines[i:])
            break
    return dict
def ParseCommandLine(d):
    options = "ABefuvw"
    for i in options:
        d["-" + i] = False
    if len(sys.argv) < 3:
        Usage()
    try:
        optlist, args = getopt.getopt(sys.argv[1:], options)
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        exit(1)
    for o, a in optlist:
        d[o] = not d[o]
    if len(args) != 2:
        Usage()
    return args
def ParseFunctions(lines):
    '''Return a dictionary keyed by function name and whose values are the
    remaining lines of the function.  The first line in the sequence lines
    is expected to be a function name line.
    '''
    assert bash_func.match(lines[0])
    i, d, n = 0, {}, len(lines)
    while True:
        key, funclines = lines[i], []
        i += 1
        while i < n and not bash_func.match(lines[i]):
            funclines.append(lines[i])
            i += 1
        d[key] = funclines
        if i >= n - 1:
            return d
if __name__ == "__main__": 
    d = {}      # Options dictionary
    fileA, fileB = ParseCommandLine(d)
    d["fileA"], d["fileB"] = fileA, fileB
    dictA, dictB = BuildDict(fileA), BuildDict(fileB)
    if d["-w"] and wdiff is None:
        msg = "Error:  need a graphical diff program in wdiff variable\n"
        sys.stderr.write(msg)
        exit(1)
    Compare(dictA, dictB, d)
