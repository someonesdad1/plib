'''

Construct the python module /plib/eevblog_data.py that lets the EEVblog episodes from
https://www.eevblog.com/episodes/ be searched.  The /plib/pgm/eev.py script can be used to do
regular expression searches and open the links that are found in the browser.

Instructions to create the needed data for this script:
    - Go to the EEVblog episodes page and open it in Chrome
    - Press ctrl-U to view the page source
    - Select all the text and go to /home/don/dp and save it in a file using vi in 'eevblog.data'
    - Run this script and it will create /plib/eevblog_data.py

Import this module and the eevblog global variable will be a dictionary with the episode's title
as the key and the value will be the relevant URL.  Note that as of 1 Jan 2025 not all the early
titles load pages with a video link.

'''
if 1:   # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from pathlib import Path as P
        import re
        import sys
        import time
        from pprint import pprint as pp
    if 1:   # Custom imports
        import requests
        from dptime import dpdatetime
        from color import t
        if 0:
            import debug
            debug.SetDebugger() 
if 1:   # Core functionality
    class Title:
        '''Class to regularize the title.  Note there are a number of things needing fixes, as
        the website was written by a human, not a script.
        '''
        def __init__(self, title):
            '''We'll standardize on the following properties
            n           EEVblog number (most are numbered in sequence).  None if no number.
            title       Basic title with no 'EEVblog dddd -'.
            part        Part number (<= numparts), None if not a multipart
            numparts    Number of parts, None if not a multipart
            
            The __str__ form is what should be used to print the title to the screen.
            '''
            # Remove leading and trailing " characters
            if title[0] == '"':
                title = title[1:]
            if title[-1] == '"':
                title = title[:-1]
            # title can have double and single quotes in them, so escape them
            title1 = title.replace('"', '\\"').replace("'", "\\'")
            # Standardize on 'EEVblog'
            title = title.replace("EEVBlog", "EEVblog")
            # Standardize the numbering
            if title.startswith("EEVblog #"):
                title = title.replace("EEVblog #", "EEVblog ")
            if title.startswith("EEVblog#"):
                title = title.replace("EEVblog#", "EEVblog ")
            # Some are missing space characters
            if title.startswith("EEVblog") and title[7] != " ":
                title = "EEVblog " + title[7:]
            # These are the standard forms that are fine
            r = re.compile(r"^EEVblog \d+ -")
            mo = r.search(title)
            if mo:
                self.title = title
                if "1388" in title:
                    title = "Dumpster Diving 4K TV Murphy's \"Repair\""
                return
            # Find the not quite standard forms
            r = re.compile(r"^EEVblog \d+")
            mo = r.search(title)
            if not mo:
                self.title = title
                return
            # These  have things like "Part x", a cuddled '-' or ':'
            r = re.compile(r"^EEVblog \d+:")
            mo = r.search(title)
            if mo:
                title = title.replace(":", " -", 1)
                self.title = title
                return
            r = re.compile(r"^EEVblog \d+-")
            mo = r.search(title)
            if mo:
                title = title.replace("-", " -", 1)
                self.title = title
                return
            # Set our title
            self.title = title
        def __str__(self):
            return self.title
    def CreateModule():
        '''Create the /plib/eevblog_data.py module file that has a dict of titles and the relevant
        URL to the web page.
    
        To create this, load the url in the browser, view the source, copy it to the clipboard, then
        pasted it to /home/don/dp/eevblog.data.  This function will open it and create the module from
        it.
        '''
        url = "https://www.eevblog.com/"
        module = P("/plib/eevblog_data.py")
        datafile = P("/home/don/dp/eevblog.data")
        # regex to get relevant lines with URL
        r_url = re.compile(f'^<a href="({url}.*?)"')
        # regex to get title
        r_title = re.compile(r'title="(.*?)"')
        # Get the datafile's lines
        lines = datafile.read_text().split("\n")
        o = []
        for line in datafile.read_text().split("\n"):
            line = line.strip()
            mo = r_url.search(line)
            if not line or not mo:
                continue
            page_url = mo.groups()[0]
            mo = r_title.search(line)
            if not mo:
                continue
            title = mo.groups()[0]
            o.append((title.strip(), page_url.strip()))
            if 0:
                t.print(f"{t.purl}{page_url} {t.ornl}{title}")
        # Write the module
        with open(module, "w") as fp:
            f = fp
            if 0:   # Debug by printing to stdout
                f = sys.stdout
            print(f"# Created by a script on {dpdatetime()}", file=f)
            print("", file=f)
            print("eevblog = {", file=f)
            for i, x in enumerate(o):
                title, page_url = x
                if not title:
                    continue
                # Regularize the title
                title = Title(title)
                print(f'{" "*4}"{title!s}": "{page_url}",', file=f)
            print("}", file=f)

if __name__ == "__main__":  
    CreateModule()
