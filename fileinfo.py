'''
Provide a more readable interface to file information than os.stat().
'''
# Copyright (C) 2020 Don Peterson
# Contact:  gmail.com@someonesdad1

# 
# Licensed under the Academic Free License version 3.0.
# See http://opensource.org/licenses/AFL-3.0.
# 

from collections import namedtuple
import os
import time 
import pathlib

class FileInfo:
    def __init__(s, file):
        s.file = file
        s.abs = pathlib.Path(file).resolve()
        st = os.stat(file)
        s.perm = oct(st.st_mode & 0o777)
        s.inode = hex(st.st_ino)
        s.dev = hex(st.st_dev)
        s.nlinks = st.st_nlink
        s.uid = st.st_uid
        s.gid = st.st_gid
        s.size = st.st_size
        s._atime = st.st_atime
        s._mtime = st.st_mtime
        s._ctime = st.st_ctime
        s.atime = s.Tm(st.st_atime)
        s.mtime = s.Tm(st.st_mtime)
        s.ctime = s.Tm(st.st_ctime)
    def Tm(self, x):
        s = "%Y%b%d:%H%M%S"     # 2018Jul27:153416
        s = "%d%b%Y-%H:%M:%S"   # 27Jul2018-15:34:16
        return time.strftime(s, time.localtime(x))
    def __str__(s):
        return f"FileInfo({s.file})"
    def __repr__(s):
        return f"FileInfo({s.abs}, {s.perm}, {s.size}B, {s.mtime})"

def GetFileInfo(file):
    '''file can either be a string or a sequence and this function will
    return either a single FileInfo object or a list of them for the
    corresponding files.
    '''
    f = FileInfo
    return f(file) if isinstance(file, str) else [f(i) for i in file]

def Now():
    'Convenience function to return time.time().'
    return time.time()
