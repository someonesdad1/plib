'''
Makes a 'perfect' uniformly-distributed random bytes file by generating the
same number of bytes for each byte value.  This isn't what we'd normally
consider a random bytes file because it's ordered and the count frequencies
are the same.  The cnt.py script's chi-square statistic will be zero is
when used with the -r option.
'''

import sys

if len(sys.argv) != 3:
    print(f"Usage:  {sys.argv[0]} numbytes_per_byte output_file")
    exit(1)
b, n = b'', int(sys.argv[1])
for c in range(256):
    b += bytes([c]*n)
 open(sys.argv[2], "wb").write(b)
