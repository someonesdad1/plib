"""
This script tests hashing speeds and will run under python 2.7 and 3.

Test hashing speeds of some hash algorithms.
    Results Mon 23 Jun 2014 03:25:00 PM on an Xubuntu 14.04 system with
        2.5 GHz quad core Intel processor:
            md5     : 3.72 s, 4.184 ns/byte
            sha1    : 3.98 s, 4.466 ns/byte
            sha224  : 8.44 s, 9.448 ns/byte     ** (Truncated form of sha256)
            sha256  : 8.42 s, 9.423 ns/byte     **
            sha384  : 8.87 s, 9.937 ns/byte     ** (Truncated form of sha512)
            sha512  : 8.90 s, 9.969 ns/byte     **
        Repeat:
            md5     : 3.72 s, 4.181 ns/byte
            sha1    : 3.95 s, 4.431 ns/byte
            sha224  : 8.30 s, 9.294 ns/byte     ** (Truncated form of sha256)
            sha256  : 8.26 s, 9.250 ns/byte     **
            sha384  : 8.74 s, 9.789 ns/byte     ** (Truncated form of sha512)
            sha512  : 8.75 s, 9.793 ns/byte     **

    Tue 15 Feb 2022 12:51:35 PM On Windows box built in 2016
        python 2.7.18:
            md5     : 4.11 s, 4.622 ns/byte
            sha1    : 3.99 s, 4.477 ns/byte
            sha224  : 5.00 s, 5.599 ns/byte
            sha256  : 5.00 s, 5.604 ns/byte
            sha384  : 5.78 s, 6.475 ns/byte
            sha512  : 5.78 s, 6.475 ns/byte
        python 3.7.12:
            md5     : 2.15 s, 2.380 ns/byte
            sha1    : 2.03 s, 2.245 ns/byte
            sha224  : 3.08 s, 3.395 ns/byte
            sha256  : 3.07 s, 3.387 ns/byte
            sha384  : 3.87 s, 4.270 ns/byte
            sha512  : 3.87 s, 4.268 ns/byte

    Conclusions as of 2022:

        * sha1 is considered insecure since 2005
        * sha224, sha256, sha384, sha512 are practically equivalent, so
        use which produces the output you want.

        Since MD5 and SHA1 are considered cryptographically broken (see
        wikipedia's MD5 page), the US government recommends SHA-2 hash
        functions (** in the above table).  Further, since there's no
        significant time difference between them, it makes sense to calculate
        sha512 and chop off the bytes from the hash that you need.

        Note "cryptographically broken" doesn't mean a hash collision has been
        found; it just means that an algorithm faster than brute force has
        been discovered for that hash algorithm.  No one has ever found a
        collision for SHA-1 yet.

        Note that Mercurial, git, etc. all use SHA-1 for their hashing needs
        (i.e., they identify file revisions with these hashes).
"""

from __future__ import print_function, division
from timeit import timeit
import sys
from pdb import set_trace as xx

py3 = sys.version_info.major == 3

if py3:
    s = '''
import hashlib
h=hashlib.%s()
t = """
This module implements a common interface to many different secure
hash and message digest algorithms. Included are the FIPS secure hash
algorithms SHA1, SHA224, SHA256, SHA384, and SHA512 (defined in FIPS
180-2) as well as RSA's MD5 algorithm (defined in Internet RFC 1321).
The terms secure hash and message digest are interchangeable. Older
algorithms were called message digests. The modern term is secure
hash.  This module implements a common interface to many different
secure hash and message digest algorithms. Included are the FIPS
secure hash algorithms SHA1, SHA224, SHA256, SHA384, and SHA512
(defined in FIPS 180-2) as well as RSA's MD5 algorithm (defined in
Internet RFC 1321).  The terms secure hash and message digest are
interchangeable. Older algorithms were called message digests. The
modern term is secure hash.
"""
h.update(t.encode())
    '''
else:
    s = '''
import hashlib
h=hashlib.%s()
t = """
This module implements a common interface to many different secure
hash and message digest algorithms. Included are the FIPS secure hash
algorithms SHA1, SHA224, SHA256, SHA384, and SHA512 (defined in FIPS
180-2) as well as RSA's MD5 algorithm (defined in Internet RFC 1321).
The terms secure hash and message digest are interchangeable. Older
algorithms were called message digests. The modern term is secure
hash.  This module implements a common interface to many different
secure hash and message digest algorithms. Included are the FIPS
secure hash algorithms SHA1, SHA224, SHA256, SHA384, and SHA512
(defined in FIPS 180-2) as well as RSA's MD5 algorithm (defined in
Internet RFC 1321).  The terms secure hash and message digest are
interchangeable. Older algorithms were called message digests. The
modern term is secure hash.
"""
h.update(t)
    '''


def GetTime(statement, hash_fn, n=1000000):
    """Print the time to hash in s and the normalized time in ns/byte."""
    st = statement % hash_fn
    t = timeit(stmt=st, number=n)
    bytes = len(st)
    print("%-8s: %.2f s, %.3f ns/byte" % (hash_fn, t, (t / n * 1e9) / bytes))


n = 1000000
GetTime(s, "md5", n=n)
GetTime(s, "sha1", n=n)
GetTime(s, "sha224", n=n)
GetTime(s, "sha256", n=n)
GetTime(s, "sha384", n=n)
GetTime(s, "sha512", n=n)
