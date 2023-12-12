import sys
from wrap import dedent

def Usage():
    print(dedent(f'''
    Usage:  {sys.argv[0]} numbytes_per_byte output_file
      Makes a 'perfect' uniformly-distributed random bytes file by
      generating the same number of bytes for each byte value.  This isn't
      what we'd normally consider a random bytes file because it's ordered
      and the count frequencies are the same.  The cnt.py script's
      chi-square statistic will be zero is when used with the -r option.
    '''))
    exit(1)

if len(sys.argv) != 3:
    Usage()
b, n = b'', int(sys.argv[1])
for c in range(256):
    b += bytes([c]*n)
open(sys.argv[2], "wb").write(b)
