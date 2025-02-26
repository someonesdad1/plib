"""
Print the time to hash a bunch of data for the different python hash library
algorithms.  Pass the files to hash on the command line.

Results for /pylib/pgm using -r (Wed 23 Dec 2020 11:06:28 AM):

    Number of bytes from files = 458.0 Mbytes

                   Relative
    Speed, MB/s    speed, %     Algorithm         12-byte hash
    -----------    --------     ---------         ------------
       1030          100          sha1            5c339e152a26
        754           73           md5            8b103a8ebb38
        433           42         sha224           42b65c8f315a
        432           42         sha256           52f652752418
        404           39         blake2s          21050b2d35ca
        314           30         sha384           ced6647144e2
        314           30         sha512           79ebdebeee16
        238           23         blake2b          788d1086268f
        142           13        shake_128         04767f2eedf5
        123           12        sha3_224          29e6c22ad911
        117           11        sha3_256          d6bea1945aaa
        117           11        shake_256         3904d8a4f598
        91             8        sha3_384          2d3c28e2a16a
        64             6        sha3_512          1a2f98bfd314
    Total processing time = 35.882 seconds

Repeat Tue 06 Jul 2021 08:30:21 AM

    Number of bytes from files = 442.9 Mbytes

                   Relative
    Speed, MB/s    speed, %     Algorithm         12-byte hash
    -----------    --------     ---------         ------------
       1026          100          sha1            8cf218ca0e39
        756           73           md5            b200e96a04d2
        435           42         sha224           dd3d35eefdb0
        434           42         sha256           90ee86edb1dd
        425           41         blake2s          916649295a58
        313           30         sha512           3c003f7890f2
        313           30         sha384           662ec7df227f
        241           23         blake2b          6389bff1a260
        141           13        shake_128         c32599131678
        123           11        sha3_224          2c97f27017ee
        117           11        sha3_256          9fd6c491a5c8
        116           11        shake_256         81b51bdf46c2
        91             8        sha3_384          83e1c70ee31a
        64             6        sha3_512          cb305c04410b
    Total processing time = 34.803 seconds

Note that all the files would have been cached in the RAM disk.  A
second run took 34.846 s.
"""

from time import time
import getopt
import hashlib
import os
import pathlib
import sys
import textwrap


def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)


def Usage(d, status=1):
    name = sys.argv[0]
    s = f"""
Usage:  {name} [options] [file1 [file2 ...]]
  Calculate the hash for the set of files with the different algorithms 
  in python's hashlib.  Print a report sorted by algorithm speed.
  Only files are processed.

Options:
  -r    Recursively process all files at and below the current directory
"""[1:-1]
    print(s)
    exit(status)


def ParseCommandLine(d):
    d["-r"] = False  # Process all files recursively
    try:
        opts, args = getopt.getopt(sys.argv[1:], "r")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o == "-r":
            d["-r"] = not d["-r"]
    if not args and not d["-r"]:
        Usage(d)
    return args


def Test(algorithm_name):
    "Time how long it takes to hash the data and return the time in s"
    h = hashlib.new(algorithm_name)
    start = time()
    h.update(data)
    end = time()
    s = end - start
    numbytes = 12
    try:
        return h.hexdigest()[:numbytes], s
    except TypeError:  # Shake methods are variable length digests
        return h.hexdigest(128)[:numbytes], s


def GetData(files):
    """Return a string containing the bytes of the files on the command
    line.  If d["-r"] is True, process all files at and below the
    current directory.
    """
    data = []
    if d["-r"]:
        p = pathlib.Path(".")
        for file in p.glob("**/*"):
            if not file.is_file():
                continue
            data.append(open(file, "rb").read())
    else:
        for file in files:
            p = pathlib.Path(file)
            if not p.is_file():
                continue
            data.append(open(file, "rb").read())
    return b"".join(data)


def Report(files, data, results):
    size_MB = len(data) / 1e6
    if files:
        print(f"Command line arguments:")
        s = " ".join(files)
        for line in textwrap.wrap(" ".join(files)):
            print(" ", line)
    else:
        print(f"All files under {os.getcwd()}")
    print(f"Number of bytes from files = {round(size_MB, 1)} Mbytes")
    print("""
               Relative
Speed, MB/s    speed, %     Algorithm         12-byte hash
-----------    --------     ---------         ------------""")
    total_time = 0
    results = sorted(results)
    max_speed = size_MB / results[0][0]  # Used to calculated relative speed
    for time_in_s, name, digest in sorted(results):
        speed_MB_per_s = size_MB / time_in_s
        rel_speed_pct = 100 * speed_MB_per_s / max_speed
        total_time += time_in_s
        print(
            f"{int(speed_MB_per_s):^11d}   "
            f"{int(rel_speed_pct):6d}        "
            f"{name:^9s}         {digest:10s}"
        )
    print(f"Total processing time = {round(total_time, 3)} seconds")


if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    data, results = GetData(files), []
    for name in sorted(hashlib.algorithms_available):
        digest, time_in_s = Test(name)
        results.append((time_in_s, name, digest))
    Report(files, data, results)
