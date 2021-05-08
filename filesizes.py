'''

Module to return file information in a more human-readable form than
os.stat().  
'''

from collections import namedtuple
from collections.abc import Iterable
import hashlib
import os
import pathlib
from datetime import datetime

Filesize = namedtuple("Filesize", '''size perm inode hardlinks atime
                      mtime ctime hash''')

def IsIterable(x):
    'Return True if x is an iterable and not a string'
    if isinstance(x, str):
        return False
    return isinstance(x, Iterable)

def GetFileData(p, gethash=None):
    'Return the Filesize object with the stat data'
    st = os.stat(p)
    h = None
    if gethash:
        with open(p, "rb") as fp:
            m = gethash()
            m.update(fp.read())
            h = m.hexdigest()
    f = Filesize(st.st_size, oct(st.st_mode), st.st_ino, st.st_nlink, 
            datetime.fromtimestamp(st.st_atime),
            datetime.fromtimestamp(st.st_mtime),
            datetime.fromtimestamp(st.st_ctime),
            h)
    return f

def FileInfo(names, gethash=hashlib.sha1):
    '''Return a dictionary of the file names specified in names, which
    can be a single string or a sequence of strings and/or pathlib
    globbing patterns.  
 
    The hash returned is defined by the constructor defined in the
    gethash keyword (or use None for faster execution).  The globbing
    patterns are relative to the current directory.
 
    The returned dictionary is keyed by pathlib objects whose values are
    named tuples with the following attributes:
 
      size            Size of file in bytes
      perm            Permissions as an octal string
      inode           Inode integer (or file index on Windows)
      hardlinks       Number of hard links
      atime           Most recent access time  (datetime.datetime object)
      mtime           Most recent modification (datetime.datetime object)
      ctime           Most recent metadata change time on UNIX or creation
                      time on Windows (datetime.datetime object)
      hash            Hex string hash of file's contents or None
 
    Note:  In hashlib, the SHA1 method is the fastest with MD5 a close
    second.  The others from openssl are roughly 10% to 20% slower.  On
    my older computer with a ramdisk, the hashing speed is about 75
    Mbytes per second for cached file information and about 10 times
    slower for uncached data.  Since most calls to FileInfo will likely
    be for a relatively small number of files, I decided to leave
    hashing turned on with SHA1 the default.  If you turn hashing off,
    the time is reduced by about one-third.  My tests were based on
    around 1130 python files in my /pylib directory tree that totaled
    about 50 Mbytes in size.
 
    Example:
        To get the size in bytes of a file named "abc" in the current
        directory, use
            FileInfo("abc").size
    '''
    results = r = {}
    p = pathlib.Path(".")
    if IsIterable(names):
        for file in names:
            results.update(FileInfo(file))
    else:
        if pathlib._is_wildcard_pattern(names):
            for file in p.glob(names):
                if file.exists():
                    r[file] = GetFileData(file, gethash=gethash)
        else:
            file = p/names
            r[file] = GetFileData(file, gethash=gethash)
    return results
