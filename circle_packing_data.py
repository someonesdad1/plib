_pgminfo = '''
    <oo desc
        Download the circle packing data from
        http://hydra.nat.uni-magdeburg.de/packing/cci/cci.html and construct a CSV file
        from it.
    oo>
    <oo cr Copyright © 2026 Don Peterson oo>
    <oo license
        Licensed under the Open Software License version 3.0.
        See http://opensource.org/licenses/OSL-3.0.
    oo>
    <oo cat Put_category_here oo>
    <oo test none oo>
    <oo todo

        - List of todo items here

    oo>
'''
if 1:  # Header
    if 1:   # Standard imports
        from pathlib import Path as P
        import csv
        import sys
    if 1:   # Custom imports
        import requests
        from color import t
        from wrap import dedent
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        t.dbg = t.lill
        # Hold the downloaded data
        g.radius = []
        g.distance = []
        g.ratio = []
        g.density = []
        g.contacts = []
        g.loose = []
        g.boundary = []
        g.symmetry = []
        g.author = []
        g.hdr = "http://hydra.nat.uni-magdeburg.de/packing/cci/txt"
        g.tmp = P("/tmp/circle_packing_data")   # Cache files here
        g.minlength = 2734  # Each downloaded file must have >= this number of lines
        # Name of the files we'll use to store data
        g.files = "radius distance ratio density contacts loose boundary symmetry author".split()
        # Keep track of number of lines in CSV file written
        g.lines = 0
if 1:   # Utility
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.n}", end="")
if 1:   # Core functionality
    def DownloadFiles():
        "Download the website's files and cache them in g.tmp"
        for file in g.files:
            url = f"{g.hdr}/{file}.txt"
            r = requests.get(url)
            s = r.content.decode()  # Convert to UTF8 string
            with P(f"{g.tmp}/{file}.txt").open("w") as f: # Cache the file
                f.write(s)
            Dbg(f"Downloaded {file}.txt")
    def ProcessFile(file):
        'Return file as a list of (a, b) where a is an integer and b is a string'
        myfile = f"{g.tmp}/{file}"
        Dbg(f"  Processing {myfile}")
        s = open(myfile).read()
        o = []
        for line in s.split("\n"):
            line = line.strip()
            if not line:
                continue
            f = line.split()
            if len(f) == 1:
                # This only happens in symmetry.txt for no group; make it C1
                n = f[0]
                item = "C1"
            elif len(f) == 2:
                n, item = line.split()
            else:
                n = f[0]
                item = ' '.join(f[1:])
            n = int(n)
            o.append((n, item))
        Dbg(f"    {file}: {len(o)} lines")
        return o
    def MakeCSVFile(file):
        # Read in data from the cached files
        Dbg("Reading in cached file data")
        radius   = ProcessFile("radius.txt")
        distance = ProcessFile("distance.txt")
        ratio    = ProcessFile("ratio.txt")
        density  = ProcessFile("density.txt")
        contacts = ProcessFile("contacts.txt")
        loose    = ProcessFile("loose.txt")
        boundary = ProcessFile("boundary.txt")
        symmetry = ProcessFile("symmetry.txt")
        author   = ProcessFile("author.txt")
        # Fix the distance array
        distance.insert(0, (1, '0.000000000000000000000000000000'))
        Dbg("Fixed distance array (missing first line)")
        # Check the lengths of the arrays
        n = len(radius)
        s = (radius, distance, ratio, density, contacts, loose, boundary, symmetry, author)
        assert (len(i) == n for i in s)
        Dbg("All array lengths OK")
        # Verify first element in every file is correct integer
        N = []
        for i in range(n):
            value = radius[i][0]
            for k in s:
                assert k[i][0] == value
            N.append(value)
        Dbg("First element integer matches in each file")
        # Construct the CSV file
        cfile = P("circle_packing.csv")
        with open(str(cfile), "w", newline='') as csvfile:
            w = csv.writer(csvfile)
            for i in range(n):
                row = [N[i]]
                for j in s:
                    row.append(j[i][1])
                w.writerow(row)
                g.lines += 1    # Count number of lines written
        print(f"Wrote CSV file {t.sky}{cfile} ({g.lines} lines)")
    def ReadCSVFile(cfile):
        'Read in the file to verify it reads correctly'
        data = {}
        with open(cfile, newline='') as csvfile:
            reader = csv.reader(csvfile)
            count = 0
            for row in reader:
                N = int(row[0])
                radius = float(row[1])
                distance = float(row[2])
                ratio = float(row[3])
                density = float(row[4])
                contacts = int(row[5])
                loose = int(row[6])
                boundary = int(row[7])
                symmetry = row[8]
                reference = row[9]
                count += 1
        # Make sure we read in the same number of lines we wrote
        if count != g.lines:
            print(f"{t.redl}Error:  number of lines read != number of lines written")
            print(f"  Number read    = {count}")
            print(f"  Number written = {g.lines}")
            exit(1)
    def UpdateMessage():
        print(dedent("""
        This script shouldn't be run until you know the web page 
        http://hydra.nat.uni-magdeburg.de/packing/cci/cci.html has been updated (the
        last update date is given as e.g. 'Last update: 25-Dec-2024' at the top of the
        page).  When you want to update the data, you must:

            - Delete the directory /tmp/circle_packing_data
            - Run this script with any command line argument
        """))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        UpdateMessage()
        exit(0)
    # Make a temporary directory in /tmp
    if not g.tmp.exists():
        g.tmp.mkdir()
        DownloadFiles()
    else:
        t.print(f"{t.ornl}Files cached in {g.tmp}.  Remove directory for fresh download.")
    csvfile = "circle_packing.csv"
    MakeCSVFile(csvfile)
    ReadCSVFile(csvfile)
