'''

ToDo
    - Change the default behavior to what -s does now.  The loading
      behavior should be gotten with -l.
    - Refine the error messages by trapping requests' exceptions.  See
      https://requests.readthedocs.io/en/latest/api/#exceptions.  The
      supported exceptions would make the exception messages more explicit
      without having to figure things out from the detailed text in the
      str(e) form.
    - Note it finds URLs like 'trigger.py' in wl2rgb.py, so the code should
      probably eliminate things that don't start with "http", "https",
      "ftp", etc.  Those three might be all that are needed in a practical
      sense.
    - Adapt to other documents
        - OO
        - Word
        - PDF
            - Crude but works:  use pdftohtml to convert to html (puts the
              files in a new directory), then scan the resulting html files
            - PDFMiner:  https://github.com/euske/pdfminer
                - https://github.com/pdfminer/pdfminer.six is a fork.  It
                  looks like it could be useful, especially the pdf2txt.py
                  and dumppdf.py script (the latter is probably what I
                  need).
            - PDFQuery: 'pip install pdfquery', https://pypi.org/project/pdfquery/
                - Search down the https://pypi.org/project/pdfquery/ page
                  to 'your best bet is to dump the xml using', which shows
                  how easy it is to get XML.  Also read about caching to
                  speed things up.
                - https://www.freecodecamp.org/news/extract-data-from-pdf-files-with-python/
                Shows an example of converting a PDF to XML:
                    - #read the PDF
                    - pdf = pdfquery.PDFQuery('customers.pdf')
                    - pdf.load()
                    - #
                    - #convert the pdf to XML
                    - pdf.tree.write('customers.xml', pretty_print = True)
    - Add '-x file' option, which gives URLs that are to be ignored

Provides two functions to help with getting and validating URLs from text
strings.

    GetURLs(s) returns a list of the URLs in the string s.

    URL_is_unreadable(url, file) tells you when a URL is not readable.

You can also run this file as a script to search file(s) for URLs and check
that they can be loaded.

To use this module, install select with 'pip install select'.
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Search text files for defunct URLs.
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        from pathlib import Path as P
        import re
        import sys
        from pprint import pprint as pp
        from textwrap import dedent
    if 1:   # Custom imports
        import requests
        from color import t
        from lwtest import Assert
    if 1:   # Global variables
        class G:
            pass
        g = G()
        # This regex came from https://gist.github.com/gruber/8891611 on 29
        # Nov 2023 and aims to find valid URLs in text strings.
        #
        # Comment:  it's the only regex I was able to find after trying
        # many different ones (mostly from stackoverflow, which has a large
        # number of poor suggestions).
        regex = r'''
            (?xi)
            \b
            (							# Capture 1: entire matched URL
              (?:
                https?:				# URL protocol and colon
                (?:
                  /{1,3}						# 1-3 slashes
                  |								#   or
                  [a-z0-9%]						# Single letter or digit or '%'
                  								# (Trying not to match e.g. "URI::Escape")
                )
                |							#   or
                							# looks like domain name followed by a slash:
                [a-z0-9.\-]+[.]
                (?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj| Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)
                /
              )
              (?:							# One or more:
                [^\s()<>{}\[\]]+						# Run of non-space, non-()<>{}[]
                |								#   or
                \([^\s()]*?\([^\s()]+\)[^\s()]*?\)  # balanced parens, one level deep: (…(…)…)
                |
                \([^\s]+?\)							# balanced parens, non-recursive: (…)
              )+
              (?:							# End with:
                \([^\s()]*?\([^\s()]+\)[^\s()]*?\)  # balanced parens, one level deep: (…(…)…)
                |
                \([^\s]+?\)							# balanced parens, non-recursive: (…)
                |									#   or
                [^\s`!()\[\]{};:'".,<>?«»“”‘’]		# not a space or one of these punct chars
              )
              |					# OR, the following to match naked domains:
              (?:
              	(?<!@)			# not preceded by a @, avoid matching foo@_gmail.com_
                [a-z0-9]+
                (?:[.\-][a-z0-9]+)*
                [.]
                (?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj| Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)
                \b
                /?
                (?!@)			# not succeeded by a @, avoid matching "foo.na" in "foo.na@example.com"
              )
            )
        '''

        g.r = re.compile(regex.strip())
        dbg = None
if 1:   # Core functionality
    def URL_is_unreadable(url):
        '''Return (True, status_code, e) if URL cannot be read, (False,
        status_code, None) otherwise.  status_code is the number returned
        by the get request.  If an exception occurred, e is set to the
        Exception object and status_code will be None.
 
        The URL is considered readable if a get request returns 200 to 299.
        If an exception occurs, it's often because the URL is poorly formed 
        or the website no longer exists.
        '''
        try:
            r = requests.get(url)
        except Exception as e:
            return (True, None, e)
        st = r.status_code
        # Note:  the status code is 200-299 for a successful response (see
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status).  
        success = 200 <= st < 300
        return (False, st, None) if success else (True, st, None)
    def GetURLs(s, unique=True, filter=False, schemes="http https ftp".split()):
        '''Return a list of the URLs in the string s.  If unique is True,
        then only return the unique URLs.  The order of the URLs in the
        list is the same as they are encountered in the string.
 
        filter
            If filter is True, then only URLs with the indicated schemes
            are returned.  Thus "https://developer.mozilla.org" would be
            returned, but "developer.mozilla.org" would not.
 
        schemes
            The URL is kept only if filter is True and the URL starts with
            one of these scheme strings.
 
        https://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml is
        the official list of schemes, last updated 28 Nov 2023 with 358
        schemes.
        '''
        urls, found = [], set()
        mo = g.r.search(s)
        while mo:
            for i in mo.groups():
                if unique and i not in found:
                    urls.append(i)
                    found.add(i)
                else:
                    urls.append(i)
            start, end = mo.span()
            s = s[end + 1:]
            mo = g.r.search(s)
        del found
        # Filter the URLs
        if filter:
            filtered = []
            for url in urls:
                for scheme in schemes:
                    if url.startswith(scheme):
                        filtered.append(url)
                        break
            urls = filtered
        return urls

if __name__ == "__main__":
    def SetUpDbg(debug):
        global dbg
        if debug:
            dbg = True
        t.dbg = t("lill") if dbg else ""
        t.N = t.n if dbg else ""
        Dbg("Debug printing turned on")
    def SetUpColor():
        if d["-c"]:
            t.on = True
            t.exc = t("redl")
            t.st = t("ornl")
            t.sts = t("trql")
        else:
            t.exc = ""
            t.st = ""
    def RunTests():
        Dbg("Running tests")
        # Check a known good URL
        url = "https://en.wikipedia.org/wiki/Main_Page"
        status, sc, exc =  URL_is_unreadable(url)
        Assert(not status and sc == 200 and not exc)
        # Get an exception on an unreachable url
        url = "https://kdfjopeurte.3095uoleorj.eorijeor/kdjfdkfj.html"
        status, sc, exc =  URL_is_unreadable(url)
        Assert(status and sc == None and exc)
        # Get a non-200 status
        url = "http://www.ndt-ed.org/GeneralResources/IACS/IACS.htm"
        status, sc, exc =  URL_is_unreadable(url)
        Assert(status and sc == 404 and not exc)
    def Dbg(*p, **kw):
        if dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        Dbg("Showing manpage")
        print(dedent(f'''
        
        This script evolved as a tool to validate the URLs used in a file.
        The first functionality was to find URLs in text files, such as a
        python script.  This is done by using a regex (regular expresssion)
        to find a URL in a string.  I also intend to develop the following
        abilities:
 
            - Find URLs in Open Office format files.  These are zipped
              groups of XML files, so this should be straightforward.
            - Find URLs in PDF files.  This is not so trivial because
              converting a PDF to a text-like file is very nontrivial.
              My tactic will be to use a library tool to convert the PDF
              content to text, then use the regex to find the URLs.
 
        Finding a suitable regex is not a trivial task as there are many
        flawed ones on the web.  The one I chose to use is from
        https://gist.github.com/gruber/8891611.  By default, it will also
        find things like 'www.abc.com' and 'myscript.py' as URLs.  These
        may in your context be a suitable URL, but the majority of the time
        I'm only interested in URLs that use the URI schemes of http,
        https, or ftp.  This filtering is enforced when the -a option is
        not used.
 
        This file is primarily a python module to find URLs.  The two
        functions are GetURLs() to generate a list of URLs found in a
        string and URL_is_unreadable() to determine URLs that are not
        readable, usually for things like a flawed URL, website that has
        gone defunct, or a URL from a valid website that returns a 404 from
        a get() (a 404 error is where the website could be reached but the
        HTTP server could not find what was asked for).
 
        My major use of this file, however, is as a script to examine the
        thousands of python scripts and documents on my system for broken
        URLs.  Maintenance of URLs in a file is complicated because URLs
        can break at any time, so the only defense is periodic validation.
        It's often a lot of work to fix broken URLs in documents, either
        because you have to find the updated or new URL or you have to
        rewrite the document to remove the defunct URL reference.  I
        sometimes take the pragmatic approach of putting the defunct URLs
        in a file and using the -x option to ignore these URLs when they
        are found after making a note in a document that the URL was found
        to be defunct on a particular date.
 
        '''))
        exit(0)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} file1 [file2 ...]
          Print the URLs in the given text files.  The URLs are listed in
          the order they are found.  Use '-' to get text from stdin.
        File types:
          The default file type is UTF-8 encoded text.  I plan for this
          script to support other file types too:
            - Open Office documents
            - PDF files
          These file types will be determined by their extension.
        Loading the URL to validate it:
          The -l option is used to load the URL's contents by a get()
          command.  This can take a long time for file(s) with lots of
          URLs.  Color is used to highlight URLs that had an exception or
          returned a get() status that wasn't in the range 200-299.
        Options:
          -a        Show all URLs that match the regex (normal behavior is
                    to only show URLs with schemes http, https, or ftp)
          -c        Turn off color in output
          -d        Turn on debug printing
          -f        Don't include the file name in the output
          -h        Print a manpage
          -l        Load the URLs, which verifies the URL is not defunct
          -s        Sort the URLs in each file
          -t        Run basic tests
          -U        Coalesce all unique URLs from the files into a sorted list
          -u        Only show the unique URLs in a file
          -u        Show a list of the statuses found to stderr
          -v        Include get() 400 status code explanations
          -x file   Ignore URLs in the file (can have more than one -x option)
        '''[1:].rstrip()))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Show all URLs, not just http/https/ftp
        d["-c"] = True      # Color in output
        d["-d"] = False     # Show debugging output
        d["-f"] = False     # Don't include file name in output
        d["-h"] = False     # Manpage
        d["-l"] = False     # Load URLs found
        d["-s"] = False     # Sort URLs in each file
        d["-t"] = False     # Run basic tests
        d["-U"] = False     # Coalesce all URLs into sorted unique list
        d["-u"] = False     # Same as -s but sorted and uniqued
        d["-v"] = False     # Show the 400 status explanations that are found
        d["-x"] = []        # Ignore URLs in these files
        try:
            opts, files = getopt.getopt(sys.argv[1:], "acdfhlstUuvx:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("acdfhlstUuv"):
                d[o] = not d[o]
            elif o == "-x":
                d[o].append(a)
        SetUpDbg(d["-d"])
        # Dump the d dict
        if dbg:
            Dbg("Options dictionary:")
            for i in d:
                if i == "-d":
                    continue
                if i.startswith("-"):
                    Dbg(f"  d[{i}] = {d[i]}")
        if d["-t"]:
            RunTests()
        elif d["-h"]:
            Manpage()
        if not files:
            Usage()
        SetUpColor()
        return files
    def GetIgnored():
        '''Get the set of URLs to ignore by virtue of the files saved by -x
        option(s).
        '''
        for file in d["-x"]:
            try:
                s = open(file).read()
            except Exception as e:
                msg = f"Can't read URLs from {file!r}\n  {e}"
                Error(msg)
            urls = GetURLs(s, unique=True, filter=not d["-a"])
            d["ignored"].update(urls)
    def GetFileString(file):
        '''Return (s, filename), where s is the string contents of the file
        and filename is the printable name of the file.  Return None for s if
        file cannot be read.  Print error messages to stderr.
        '''
        if file == "-":
            s = sys.stdin.read()
            return (s, "stdin")
        else:
            p = P(file)
            if not p.exists():
                print(f"{file!r} doesn't exist", file=sys.stderr)
                return (None, file)
            try:
                return (open(file).read(), file)
            except Exception as e:
                print(f"Cannot read {file!r}: {e!r}", file=sys.stderr)
                return (None, file)
    def CheckFile(file):
        'Find URLs in the file and print any that cannot be read'
        s, filename = GetFileString(file)
        urls = GetURLs(s)
        loaded = set()  # Only load a URL once
        for url in urls:
            if url in loaded or url in d["ignored"]:
                continue
            not_ok, status, exception = URL_is_unreadable(url)
            loaded.add(url)
            if not_ok:
                if exception is not None:
                    if d["-f"]:
                        print(f"{t.exc}{url}    Exception{t.n}")
                    else:
                        print(f"{t.exc}{filename}:  {url}    Exception{t.n}")
                else:
                    d["status"].add(status)
                    if d["-f"]:
                        print(f"{url}    {t.st}get() status = {status}{t.n}")
                    else:
                        print(f"{filename}:  {url}    {t.st}get() status = {status}{t.n}")
    def URLsInFile(file):
        'Save the results in the dict d["urls"]'
        Dbg(f"In URLsInFile({file!r})")
        # Only process a file once
        if file in d["files"]:
            Dbg(f"  This file already processed")
            return
        else:
            d["files"].add(file)
        s, filename = GetFileString(file)
        Dbg(f"  Read in string of length {len(s)}")
        if d["-a"]:
            urls = GetURLs(s, unique=False)
        else:
            urls = GetURLs(s, unique=False, filter=True)
        Dbg(f"  Found {len(urls)} URLs")
        # If -U is not True, we can report the files from here
        if d["-u"]:
            # Save only unique URLs
            u, found = [], set()
            for i in urls:
                if i not in found:
                    u.append(i)
                    found.add(i)
            urls = u
        if d["-s"]:
            # Sort by name
            urls = list(sorted(urls))
        # Remove ignored URLs
        urls = [i for i in urls if i not in d["ignored"]]
        if not d["-U"] and urls:
            print(f"{filename}:")
            for url in urls:
                print(f"  {url}")
        d["urls"][file] = urls
    def Report():
        '''The urls are in the dict d["urls"] keyed by filename.  Since the
        -U option was used, collapse this set of URLs into a unique sorted
        list.
        '''
        found = set()
        for file in d["urls"]:
            for url in d["urls"][file]:
                found.add(url)
        for url in sorted(list(found)):
            print(url)
    def StatusName(status):
        '''Convert integer status to string.  Taken from
        https://en.wikipedia.org/wiki/List_of_HTTP_status_codes.
        '''
        names = {
            400: "Bad Request",
            401: "Unauthorized",
            402: "Payment Required",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            406: "Not Acceptable",
            407: "Proxy Authentication Required",
            408: "Request Timeout",
            409: "Conflict",
            410: "Gone",
            411: "Length Required",
            412: "Precondition Failed",
            413: "Payload Too Large",
            414: "URI Too Long",
            415: "Unsupported Media Type",
            416: "Range Not Satisfiable",
            417: "Expectation Failed",
            418: "I'm a teapot (RFC 2324, RFC 7168)",
            421: "Misdirected Request",
            422: "Unprocessable Content",
            423: "Locked (WebDAV; RFC 4918)",
            424: "Failed Dependency (WebDAV; RFC 4918)",
            425: "Too Early (RFC 8470)",
            426: "Upgrade Required",
            428: "Precondition Required (RFC 6585)",
            429: "Too Many Requests (RFC 6585)",
            431: "Request Header Fields Too Large (RFC 6585)",
            451: "Unavailable For Legal Reasons (RFC 7725)",
        }
        return names.get(status, "?")
    def PrintStatuses():
        'Show statuses found to stderr'
        if d["status"] and d["-v"]:
            print(f"\n{t.sts}get() status items found in search:", file=sys.stderr)
            for i in sorted(d["status"]):
                print(f"  {i}:  {StatusName(i)}", file=sys.stderr)
            print(f"{t.N}", end="", file=sys.stderr)
    d = {       # Options dictionary
        "urls": {},         # Container for -U option
        "files": set(),     # Keep track of files processed
        "status": set(),    # Keep track of returned statuses
        "ignored": set(),   # URLs to ignore 
    }
    files = ParseCommandLine(d)
    GetIgnored()
    # Remove duplicate files
    unique = []
    for file in files:
        if file not in unique:
            unique.append(file)
    files = unique
    if len(files) == 1:
        d["-f"] = True
    for file in files:
        if d["-l"]:
            d["-u"] = d["-s"] = True
            CheckFile(file)
            PrintStatuses()
        else:
            URLsInFile(file)
            if d["-U"]:
                Report()
