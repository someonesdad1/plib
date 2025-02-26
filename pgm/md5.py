"""
Print md5 hashes for files on command line.
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import os
import hashlib

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#


def Usage(status=1):
    name = sys.argv[0]
    s = """Usage:  {name} file1 [file2...]
  Prints the MD5 checksum for each file on the command line.  The
  file's size in bytes is shown in angle brackets after the name.
"""[:-1]
    print(s.format(**locals()))
    sys.exit(status)


def ProcessFile(file):
    # Ignore things that aren't files
    if not os.path.isfile(file):
        return
    m, s = hashlib.md5(), []
    m.update(open(file, "rb").read())
    s = [m.hexdigest(), file]
    size = os.stat(file)[6]
    s += ["<%d>" % size]
    print(" ".join(s))


if __name__ == "__main__":
    d = {}  # Options dictionary
    if len(sys.argv) < 2:
        Usage()
    args = sys.argv[1:]
    for file in args:
        ProcessFile(file)
