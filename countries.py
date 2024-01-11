'''
Data on area of countries

    Two global tuples are wp_area_data and cia_area_data from GetWPData()
    and GetCIAData().

    wp_area_data contains (name, total, land, water) where the last three
    are areas in m².

    cia_area_data contains (name, region, area) where area is in m².
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # <data> Land and water area of countries
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from f import flt
        from f import flt
        from io import StringIO
        from pathlib import Path as P
        import csv
    if 1:   # Custom imports
        pass
    if 1:   # Global variables
        __all__ = "GetWPData GetCIAData wp_area_data cia_area_data".split()
if 1:   # Core functionality
    def GetWPData():
        '''Return a tuple of tuples of the area in m² of earth and the countries
        of the world.  Each entry is (name, total_area, land_area, water_area).
    
        Originally screen-scraped from
        https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_area
        Thu 11 Jan 2024 09:11:45 AM.  This web page has many errors, so I put
        the data into a spreadsheet and corrected them by getting the total
        area from the CIA Word Factbook (see below) and assumed the water area
        number was correct.  Then the invariant total = land + water was
        used to correct the land value if necessary.  These data were put into
        the file countries.csv.
        '''
        o = []
        for i in csv.reader(open("wp_countries.csv")):
            name = i[0]
            total, land, water = [flt(j) for j in i[1:]]
            assert total == land + water
            # Change the areas to square meters
            total, land, water = [flt(i)*1e6 for i in (total, land, water)]
            o.append((name, total, land, water))
        return tuple(o)
    def GetCIAData():
        '''Return a tuple of tuples of CIA World Factbook information on the
        areas of countries.  If show is True, print the data to stdout.
        Each tuple is (name, region, area) where area is a flt in square
        meters.
    
        World Factbook https://www.cia.gov/the-world-factbook/ dated 11 Jan
        2024.  The page used was
        https://www.cia.gov/the-world-factbook/field/area/country-comparison/
        (this page has a download button for a CSV file).
        '''
        w = 60
        o = []
        for i in csv.reader(P("cia_countries.csv").open()):
            if not i:
                continue
            name, slug, area_sqkm, date, rank, region = [j.strip() for j in i]
            if name == "name":
                continue
            if name.startswith("Holy See"):
                area_sqkm = "0.49"
            area = flt(area_sqkm.replace(",", ""))*1e6
            s = f"{name} ({region})"
            o.append((name, region, area))
        return tuple(o)
    wp_area_data = GetWPData()
    cia_area_data = GetCIAData()

if __name__ == "__main__": 
    import sys
    if len(sys.argv) > 1:
        import debug
        debug.SetDebugger()
    # Print out the data
    v, w = 8, max(len(i[0]) for i in wp_area_data)
    a = "Area of countries of the world in m² (T = 10¹², G = 10⁹, M = 10⁶, k = 10³)"
    # Wikipedia stuff
    print("\nWikipedia data")
    print(f"{a:{w}s} {'Total':^{v}s} {'Land':^{v}s} {'Water':^{v}s}")
    for i in wp_area_data:
        name, total_area, land_area, water_area = i
        a, b, c, d = i
        e = "m²"
        b, c, d = b.engsi + e, c.engsi + e, d.engsi + e
        print(f"{a:{w}s} {b:^{v}s} {c:^{v}s} {d:^{v}s}")
    # CIA stuff
    print("\nCIA data")
    v, w = 44, 18
    # Shorten region names
    reg = {
        "Central America and the Caribbean": "C. Amer. & Carib.",
        "East and Southeast Asia": "E & SE Asia",
        "Australia and Oceania": "Aust. & Oceania",
        "": "",
    }
    for name, region, area in sorted(cia_area_data):
        if region in reg:
            region = reg[region]
        print(f"{name:{v}s} {region:{w}s} {area.engsi:s}m²")
