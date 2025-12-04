'''
Print md5 hashes for files on command line.
'''
if 1:   # Header
    import sys
    import os
    import hashlib
    from wrap import dedent
    from color import t
    import termtables as tt
    from dpprint import PP
    pp = PP()   # Get pprint with current screen width
    # Copyright (C) 2014, 2025 Don Peterson
    # Contact:  gmail.com@someonesdad1
    #
    # Licensed under the Open Software License version 3.0.
    # See http://opensource.org/licenses/OSL-3.0.
    #
def Usage():
    name = sys.argv[0]
    print(dedent(f'''
    Usage:  {name} file1 [file2...]
        Prints the MD5 checksum for each file on the command line.  The
        file's size in bytes is shown in angle brackets after the name.
    '''))
    exit(0)
def ProcessFile(file):
    'Print the filename, size in bytes, hash'
    # Ignore things that aren't files
    if not os.path.isfile(file):
        return
    m, s = hashlib.md5(), []
    try:
        m.update(open(file, "rb").read())
    except Exception:
        t.print(f"{t.ornl}Could not read {file!r}")
        return None
    size = os.stat(file)[6]
    return [file, str(size), m.hexdigest()]
def Report(results):
    'Print so that columns are aligned'
    w0 = max(len(i[0]) for i in results)
    w1 = max(len(i[1]) for i in results)
    w2 = max(len(i[2]) for i in results)
    s = [["File", "Bytes", "MD5 Hash"]]
    s.append(["-"*w0, "-"*w1, "-"*w2])
    s.extend(results)
    tt.print(s,
             header=None,
             padding=(0, 0),
             style=" "*15,
             alignment="lll")

if __name__ == "__main__":
    d = {}  # Options dictionary
    if len(sys.argv) < 2:
        Usage()
    args = sys.argv[1:]
    results = []
    for file in args:
        result = ProcessFile(file)
        if result is not None:
            results.append(result)
    Report(results)
