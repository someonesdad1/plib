'''
Script to show current shell aliases.
'''

from __future__ import print_function
import sys
import os
from columnize import Columnize

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
def GetAliasNames(lines):
    aliases = []
    for line in lines:
        if not line.strip():
            continue
        f = line.split()
        aliases.append(f[1].split("=")[0])
    return aliases

if __name__ == "__main__":
    lines = [i.strip() for i in sys.stdin.readlines()]
    for i in Columnize(GetAliasNames(lines)):
        print(i.strip())
