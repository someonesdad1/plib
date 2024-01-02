'''
Don Peterson 8/3/99

Print the binary differences between two files.  Any differences
will be shown as hex dumps of the differing bytes.

If the file sizes are different, then the files are only compared up
to the size of the smaller file.

The files are read into buffers of chunk size chunksizeG.  These
buffers are compared; if they are not equal, then the corresponding
bytes are compared with each other.  Then the unequal bytes are
found and a list of offset ranges is generated for this chunk that
indicates where the differences are.  This list of differences then
has contiguous ranges collapsed into one range.  Once the list of
differences is found, then the corresponding bytes are printed to
stdout using the hexdump() routine.

The basic algorithm for generating the ranges is based on a state
machine.  The main variables are offset (the position of the pointer
into the file stream), start, the beginning of a range, and end,
the end of a range.  The states are:

    S0       Beginning state
    S1       Range on state
    S2       Range off state
    S3       Ending state (chunk processing finished)

The state transitions and their actions are:

    Initialize:  set start = end = INVALID_VALUE
    S0-S1    Set start = end = offset
    S0-S2    No action
    S1-S1    Set end = offset
    S1-S2    Append [start, end] to range list.
             Then set start = end = INVALID_VALUE
    S1-S3    If start != INVALID_VALUE append [start, end] to range list.
    S2-S1    Set start = end = offset
    S2-S2    No action
    S2-S3    No action

(This looks a little cleaner on a state machine diagram.)
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 1999 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Print the binary differences between two files
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import os
    import string
    import sys
    from io import StringIO
    from pdb import set_trace as xx 
if 1:   # Global variables
    file1G = ""
    file2G = ""
    # There is an interesting tradeoff between the chunksize and the number
    # differences in a file.  For two files with no differences, the
    # performance increases up to around 1<<13 or so.  But as differences
    # occur between the two files, performance goes up as the chunk size
    # drops (because most of the smaller comparisons are going to be done
    # by the C string comparison, not the python for loop).  The selected
    # value works reasonably for both situations.
    #
    # Determined to be an empirically decent value by testing on a 3.4 MB
    # binary (the emacs binary).
    chunksizeG = 1 << 12
    debugG = 0
    sepG = "=" * 78
def Debug(s):
    if debugG:
        print(s)
def CheckSizes():
    '''Compare the file sizes; if they are different, print out a message
    to stdout to this effect.  Return a tuple of the smallest size followed
    by the two sizes.  If one of the file sizes is zero, print and error
    message and exit.
    '''
    import stat
    size1 = os.stat(file1G)[stat.ST_SIZE]
    size2 = os.stat(file2G)[stat.ST_SIZE]
    if size1 == 0:
        print("File %s has zero size" % file1G)
        exit(2)
    if size2 == 0:
        print("File %s has zero size" % file2G)
        exit(2)
    Debug("size of %s = %d" % (file1G, size1))
    Debug("size of %s = %d" % (file2G, size2))
    if size1 < size2:
        return size1, size1, size2
    elif size1 > size2:
        return size2, size1, size2
    return size1, size1, size2
def Usage():
    print("Usage:  %s file1 file2" % sys.argv[0])
    print("  Performs a binary file comparison between two files")
    exit(1)
def FixContiguousRanges(ranges):
    '''Go through the list of ranges and collapse contiguous ranges
    into one range.
    '''
    if len(ranges) == 0:
        Debug("FixContiguousRanges:  empty ranges")
        return []
    if len(ranges) == 1:
        Debug("FixContiguousRanges:  one range")
        return ranges
    range_list = [ranges[0]]
    del ranges[0]
    for r in ranges:
        last_range = range_list[-1]
        if last_range[1] == r[0] - 1:
            last_range[1] = r[1]
            range_list[-1] = last_range
        else:
            range_list.append(r)
    return range_list
def CompareBytes(ifp1, ifp2, filesize):
    '''Compare the bytes of the two files up to the number of bytes in
    filesize.  Generate and return a list of ranges of the bytes that
    are different.  Each range is a list of two integers, the beginning
    and ending 0-based offset of the range.  Return a list that represents
    all the differences in the file.
    '''
    list = []
    Debug("filesize = %d" % filesize)
    numchunks = filesize//chunksizeG + 1
    Debug("Number of chunks = %d, chunksize = %d" % (numchunks, chunksizeG))
    all_ranges = []
    for chunk in range(numchunks):
        str1 = ifp1.read(chunksizeG)
        str2 = ifp2.read(chunksizeG)
        Range = CompareChunk(str1, str2, chunk)
        if len(Range) != 0:
            all_ranges.append(Range)
    # Collapse all of the ranges into one list
    Range = []
    for r in all_ranges:
        if len(r) != 0:
            Range = Range + r
    Range = FixContiguousRanges(Range)
    return Range
def CompareChunk(str1, str2, chunk):
    '''Compare the two chunks in str1 and str2.  If they are not equal,
    put the differences in a ranges list and return the list; otherwise,
    return an empty list.  The chunk value is used to calculate the
    actual offsets in the file.
    '''
    if str1 == str2:
        Debug("++++++ Chunk %d the same +++++" % chunk)
        return []
    # They're different, so compare
    START = 0
    RANGE_ON = 1
    RANGE_OFF = 2
    END = 3
    INVALID_VALUE = -1
    size = len(str1)
    if len(str1) > len(str2):
        size = len(str2)
    old_state = new_state = START
    ranges = []
    start = end = INVALID_VALUE
    Debug("+++++++++++++++++++ Start compare chunk %d "
          "+++++++++++++++++++++++++" % chunk)
    Debug("Offset will be from %d to %d"
          % (chunk*chunksizeG, chunk*chunksizeG + chunksizeG-1))
    Debug("Starting state = START")
    for i in range(size):
        offset = i + chunk*chunksizeG
        try:
            Debug("Offset = %d, str1 = %c, str2 = %c" %
                  (offset, str1[i], str2[i]))
        except Exception:
            print("i =", i)
            print("len(str1) =", len(str1))
            print("len(str2) =", len(str2))
            exit(1)
        equal = (str1[i] == str2[i])
        Debug("  equal = %d" % equal)
        if old_state == START:
            if equal:
                new_state = RANGE_OFF
                Debug("  New state = RANGE_OFF")
            else:
                new_state = RANGE_ON
                start = end = offset
                Debug("  New state = RANGE_ON at offset %d" % offset)
        elif old_state == RANGE_ON:
            if equal:
                new_state = RANGE_OFF
                if len(ranges) == 0:
                    ranges = [[start, end]]
                else:
                    ranges.append([start, end])
                Debug("  Found range [%d, %d]" % (start, end))
                start = end = INVALID_VALUE
                Debug("  New state = RANGE_OFF")
            else:
                new_state = RANGE_ON
                end = offset
                Debug("  New state = RANGE_ON")
        elif old_state == RANGE_OFF:
            if equal:
                new_state = RANGE_OFF
                Debug("  New state = RANGE_OFF")
            else:
                new_state = RANGE_ON
                start = end = offset
                Debug("  New state = RANGE_ON")
        old_state = new_state
    # End of chunk signifies transition to state END
    Debug("New state = END")
    if old_state == RANGE_ON:
        if start != INVALID_VALUE:
            if len(ranges) == 0:
                ranges = [[start, end]]
            else:
                ranges.append([start, end])
    Debug("Ranges is " + repr(ranges))
    Debug("+++++++++++++++++++ End compare chunk "
          "++++++++++++++++++++++++++++++")
    return ranges
def hexdump(dest, src, numbytes=-1, startnum=0):
    '''Hex dump utility.  The function call is
        hexdump(dest, src, numbytes, startnum)
    where
        dest       A file object opened for writing; is where the output
                   bytes will be sent.  For convenience, dest can also be
                   a string.
        src        A file object opened for reading.  It contains the bytes
                   that will be dumped.  For convenience, src can also be
                   a string.
        numbytes   How many bytes to dump.  The default of -1 means dump all
                   the bytes from the file object.
        startnum   The offset to start numbering from.  This can be used to
                   start the offset numbering from something other than 0.
    The function does not return anything.  Exceptions will be raised for
    improper parameters.  Exceptions from the underlying operations such
    as file access are not caught.
    '''
    def OutputLine(dest, bytes, offset, bytes_per_line, nonprintable_char):
        '''Print a hex dump line of bytes_per_line bytes.
        '''
        if len(bytes) == 0:
            return
        dest.write("%08x  " % offset)
        # Print the hex values
        for i in range(bytes_per_line):
            if i < len(bytes):
                dest.write("%02x " % bytes[i])
            else:
                dest.write("   ")
            if i == 7:
                dest.write(" ")
        dest.write(" | ")
        # Print the ASCII representation
        for i in range(bytes_per_line):
            if i < len(bytes):
                char = bytes[i]
                if char >= 32:
                    dest.write("%c" % bytes[i])
                else:
                    dest.write("%c" % nonprintable_char)
        dest.write("\n")   # Go to the next line
    bytes_per_line = 16
    nonprintable_char = 250  # Use for DOS
    if "OSTYPE" in os.environ:
        if os.environ["OSTYPE"] == "linux-gnu":
            nonprintable_char = 183  # For Linux xterm
    stringio = StringIO('')
    # If dest is a string, convert it to a StringIO object.
    if isinstance(dest, str):
        Dest = StringIO()
    else:
        Dest = dest
    if isinstance(src, str):
        Src = StringIO(src)
    else:
        Src = src
    done = 0
    if numbytes == -1:
        numbytes = 0x7fffffff
    bytes = Src.read(bytes_per_line)
    count = 0
    offset = startnum
    while len(bytes) != 0:
        if len(bytes) + count >= numbytes:
            bytes = bytes[:numbytes - count]
        OutputLine(Dest, bytes, offset, bytes_per_line, nonprintable_char)
        count = count + len(bytes)
        if count >= numbytes:
            break
        bytes = Src.read(bytes_per_line)
        offset = offset + bytes_per_line
def TestHexDump():
    # Perform some simple tests
    dest = sys.stdout
    s = ("This is a sample string that is definitely longer than "
         "16 characters.")
    src = StringIO(s)
    print("Whole string: %r" % s)
    hexdump(dest, src)

    print("\n0 bytes")
    src.seek(0)
    hexdump(dest, src, numbytes=0)

    print("\n1 byte")
    src.seek(0)
    hexdump(dest, src, numbytes=1)

    print("\n2 bytes")
    src.seek(0)
    hexdump(dest, src, numbytes=2)

    print("\n15 bytes")
    src.seek(0)
    hexdump(dest, src, numbytes=15)

    print("\n16 bytes")
    src.seek(0)
    hexdump(dest, src, numbytes=16)

    print("\n17 bytes")
    src.seek(0)
    hexdump(dest, src, numbytes=17)

    print("\nWith nonzero startnum")
    src.seek(0)
    hexdump(dest, src, startnum=0x1)

    print("\nWith number of bytes larger than string size")
    src.seek(0)
    hexdump(dest, src, numbytes=len(s)+1)

    del src
    src = s
    print("Whole string as a string:\n%r", s)
    hexdump(dest, src)

    del src
    print("Script source as a file; 35 bytes:")
    src = open("hd.py")
    hexdump(dest, src, numbytes=35)
    src.close()
def PrintDifference(ifp1, ifp2, diff):
    '''
    '''
    offset = diff[0]
    numbytes = diff[1] - offset + 1
    print(sepG)
    s = "bytes"
    if numbytes == 1:
        s = "byte"
    print("File %s:  %d (0x%x) %s different" % (file1G, numbytes, numbytes, s))
    ifp1.seek(offset)
    ifp2.seek(offset)
    hexdump(sys.stdout, ifp1, numbytes, offset)
    print("File %s:" % file2G)
    hexdump(sys.stdout, ifp2, numbytes, offset)
def PrintHeader(size1, size2):
    if size1 != size2:
        s = "byte"
        if size1 > 1:
            s = "bytes"
        print("File %s is %d (0x%x) %s" % (file1G, size1, size1, s))
        s = "byte"
        if size2 > 1:
            s = "bytes"
        print("File %s is %d (0x%x) %s" % (file2G, size2, size2, s))
        size = size1
        if size1 > size2:
            size = size2
        if size == 1:
            print("Only the first byte is compared")
        else:
            print("Only the first %d (0x%x) bytes are compared" % (size, size))
    else:
        print("Files are %d (0x%x) bytes in size" % (size1, size1))
if __name__ == "__main__": 
    if len(sys.argv) != 3:
        Usage()
    file1G = sys.argv[1]
    file2G = sys.argv[2]
    ifp1 = open(file1G, "rb")
    ifp2 = open(file2G, "rb")
    filesize, size1, size2 = CheckSizes()
    difflist = CompareBytes(ifp1, ifp2, filesize)
    if len(difflist) == 0:
        exit(0)  # Files are equal, so return 0 status
    PrintHeader(size1, size2)
    ifp1.seek(0)
    ifp2.seek(0)
    if len(difflist) > 0:
        for diff in difflist:
            PrintDifference(ifp1, ifp2, diff)
        print(sepG)
    exit(1)  # Files are not equal, so return 1 status
