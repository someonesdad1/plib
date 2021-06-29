'''
Python version of UNIX cat program.  Includes ability to validate
the input files via their SHA1 hashes as produced by the split.py
script.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2008 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Python version of UNIX cat program
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import hashlib
    import getopt
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
if 1:   # Global variables
    hash_file = ""
    output_file = ""
def Usage():
    print(dedent(f'''
    Usage:  {sys.argv[0]} [-f SHA_hash_file] file1 file2 [file3...] output_file
      Concatenates file1, file2, ... into a single output_file.  
    
      If you use the option -f to specify the hash file, you don't need to
      specify the input files on the command line.  In this case, the hashes
      of the file pieces will be checked before creating the output file.
  
      The -f option with the SHA1 hash file is to be used in conjuction with
      the split.py utility.
    '''))
    exit(1)
def ParseCommandLine():
    if len(sys.argv) < 2:
        Usage()
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "f:")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        exit(1)
    for opt in optlist:
        if opt[0] == "-f":
            global hash_file
            hash_file = opt[1]
        elif opt[0] == "-h":
            print(manual)
            exit(0)
    global output_file
    if hash_file:
        if len(args) != 1:
            Usage()
        output_file = args[0]
        input_files = ProcessHashFile()
    else:
        if len(args) < 3:
            Usage()
        input_files = args[:-1]
        output_file = args[-1]
    return input_files
def ProcessHashFile():
    '''Read the hash file and check the hashes of each file.  Then return a
    list of the file names.
    '''
    try:
        lines = open(hash_file).readlines()[1:]
    except:
        print("Hash file couldn't be read or it is improper", file=sys.stderr)
        exit(1)
    if len(lines) < 2:
        print("Hash file must be at least three lines long", file=sys.stderr)
        exit(1)
    input_files = []
    for line in lines:
        hash, file = line.strip().split()
        input_files.append(file)
        new_hash = hashlib.sha1(open(file, "rb").read()).hexdigest()
        if hash != new_hash:
            print("Hash error on file '{}'".format(file), file=sys.stderr)
            exit(1)
    return input_files
if __name__ == "__main__": 
    input_files = ParseCommandLine()
    output_stream = open(output_file, "wb")
    for file in input_files:
        try:
            output_stream.write(open(file, "rb").read())
        except Exception:
            print("Couldn't open '{}'".format(file), file=sys.stderr)
            exit(1)
    output_stream.close()
    exit(0)
