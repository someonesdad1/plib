'''
ToDo
    - Refine the error messages by trapping requests' exceptions.  See
      https://requests.readthedocs.io/en/latest/api/#exceptions.
      The supported exceptions would make the exception messages more
      explicit without having to figure things out from the detailed text
      in the str(e) form.
    - Note it finds URLs like 'trigger.py' in wl2rgb.py, so the code should
      probably eliminate things that don't start with "http", "https",
      "ftp", etc.  Those three might be all that are needed in a practical
      sense.
    - Adapt to other documents
        - OO
        - Word
        - PDF
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
    def GetURLs(s, unique=True):
        '''Return a list of the URLs in the string s.  If unique is True,
        then only return the unique URLs.  The order of the URLs in the
        list is the same as they are encountered in the string.
        '''
        urls = []
        mo = g.r.search(s)
        while mo:
            for i in mo.groups():
                if unique and i not in urls:
                    urls.append(i)
            start, end = mo.span()
            s = s[end + 1:]
            mo = g.r.search(s)
        return urls

if __name__ == "__main__":
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} file1 [file2 ...]
          Search for URLs in the given files and tries to load them.  Any
          that cannot be loaded are printed to stdout.  Use '-' to get text
          from stdin.
        Warning:
          This script requests and loads the data from every web page to
          ensure that the URL is valid.  This can take a long time to
          execute for a set of files with a lot of URLs in them.
        Options:
          -c        Turn off color in output
          -f        Don't include the file name in the output
          -s        Print the URLs in the file(s) (don't load them)
          -t        Run some simple tests
          -u        Same as -s, but sort the URLs and only show unique ones
        '''[1:].rstrip()))
        exit(status)
    def RunTests():
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
    def ParseCommandLine(d):
        d["-c"] = True      # Turn off color in output
        d["-f"] = False     # Don't include file name
        d["-s"] = False     # Just show the URLs encountered without any checking
        d["-t"] = False     # Run simple tests
        d["-u"] = False     # Same as -s but sorted and uniqued
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "cfstu") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("cfstu"):
                d[o] = not d[o]
            elif o == "-h":
                Usage(status=0)
        if d["-t"]:
            RunTests()
        return args
    def CheckFile(file):
        'Find URLs in the file and print any that cannot be read'
        filename = file
        if file == "-":
            s = sys.stdin.read()
            filename = "sys.stdin"
        else:
            p = P(file)
            if not p.exists():
                print(f"{file!r} doesn't exist", file=sys.stderr)
                return
            try:
                s = open(file).read()
            except Exception as e:
                print(f"Cannot read {file!r}: {e!r}", file=sys.stderr)
                return
        urls = GetURLs(s)
        if d["-s"]:
            for url in urls:
                if d["-f"]:
                    print(f"{url}")
                else:
                    print(f"{filename}:  {url}")
        elif d["-u"]:
            urls_ = list(sorted(set(urls)))
            for url in urls_:
                if d["-f"]:
                    print(f"{url}")
                else:
                    print(f"{filename}:  {url}")
        else:
            for url in urls:
                if d["-s"] or d["-u"]:
                    if d["-f"]:
                        print(f"{url}")
                    else:
                        print(f"{filename}:  {url}")
                else:
                    loaded = set()  # Only load a URL once
                    if file not in loaded:
                        not_ok, status, exception = URL_is_unreadable(url)
                        loaded.add(file)
                        if not_ok:
                            if exception is not None:
                                if d["-f"]:
                                    print(f"{t.exc}Exception:{t.n}  {url}")
                                else:
                                    print(f"{t.exc}Exception:{t.n}  {filename}:  {url}")
                            else:
                                if d["-f"]:
                                    print(f"{url}    status = {t.st}{status}{t.n}")
                                else:
                                    print(f"{filename}:  {url}    status = {t.st}{status}{t.n}")
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    if d["-c"]:
        t.exc = t("ornl")
        t.st = t("yell")
    else:
        t.exc = ""
        t.st = ""
    if len(files) == 1:
        d["-f"] = True
    for file in files:
        CheckFile(file)
