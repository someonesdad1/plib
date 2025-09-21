'''
Split a file into pieces and print the SHA1 hash of the pieces
to stdout.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2008 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Split a file into chunks
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import os
    import hashlib
    from math import log10, ceil
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
def Error(*msg):
    print(*msg, file=sys.stderr)
    exit(1)
def Usage():
    print(
        dedent(f'''
    Usage:  {sys.argv[0]}  size_in_MB  prefix  file_to_split
      Splits a file into pieces of size_in_MB.  The files are named prefix00,
      prefix01, etc.  The SHA1 hashes of the pieces are printed to stdout.
      These hashes can be used with the cat.py script when reconstructing the
      input file -- they will validate that the file pieces haven't changed.
    ''')
    )
    exit(1)
def Process(buffer, prefix, number):
    file = f"{prefix}{number:0{digits}d}"
    # Check to see if file exists; if so, stop.
    if os.path.exists(file):
        Error(f"File '{file}' exists -- won't overwrite.")
        exit(1)
    output_stream = open(file, "wb")
    output_stream.write(buffer)
    output_stream.close()
    print(hashlib.sha1(buffer).hexdigest() + " " + file)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        Usage()
    try:
        chunk_size_in_bytes = int(float(sys.argv[1]) * 1e6)
    except Exception:
        Error("size_in_MB improper")
        exit(1)
    prefix, input_file = sys.argv[2:]
    file_size_in_bytes = int(os.stat(input_file)[6])
    num_files_to_write = file_size_in_bytes // chunk_size_in_bytes
    digits = ceil(log10(num_files_to_write))
    if num_files_to_write < 2:
        Error("File doesn't need splitting")
        exit(1)
    with open(input_file, "rb") as input_stream:
        print("SHA1 hashes for each file:")
        for i in range(num_files_to_write):
            buffer = input_stream.read(chunk_size_in_bytes)
            Process(buffer, prefix, i)
        # Process any remaining bytes
        buffer = input_stream.read()
        Process(buffer, prefix, num_files_to_write)
