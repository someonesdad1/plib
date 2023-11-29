'''

Searches for URLs in text files given on the command line and lists the
ones that are defunct or return a non-200 status.
    - If the request returns a status that is not 200, then the file, URL,
      and status are printed.
    - URLs that cause an exception message to be printed are probably sites
      that cannot be reached or are ill-formed/incomplete URLs.
If there is no output, then either there were no URLs in the file(s) or all 
the URL were successfully loaded.

To use this, install select with 'pip install select'.
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
        import requests
        import sys
        from textwrap import dedent
    if 1:   # Global variables
        class G:
            pass
        g = G()
        # This regex came from https://gist.github.com/gruber/8891611 on 29
        # Nov 2023 and purports to find valid URLs in text strings.
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
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} file1 [file2 ...]
          Search for URLs in the given files and tries to load them.  Any
          that cannot be loaded are printed to stdout.  Use '-' to get text
          from stdin.
        '''[1:].rstrip()))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Describe this option
        d["-d"] = 3         # Number of significant digits
        d["-s"] = False     # Just show the URLs encountered
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "s") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("s"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o == "-h":
                Usage(status=0)
        return args
if 1:   # Core functionality
    def URL_is_unreadable(url, file):
        '''Return (True, status_code) if URL cannot be read, (False,
        status_code) otherwise.  -1 is returned for an exception.
        '''
        try:
            r = requests.get(url)
        except Exception as e:
            print(f"Exception: {file}: {url!r}")
            return (False, -1)
        st = r.status_code
        return (False, st) if st == 200 else (True, st)
    def GetURLs(s):
        'Return a list of the URLs in the string s'
        urls = []
        mo = g.r.search(s)
        while mo:
            for i in mo.groups():
                urls.append(i)
            start, end = mo.span()
            s = s[end + 1:]
            mo = g.r.search(s)
        return urls

if __name__ == "__main__":
    def CheckFile(file):
        'Find URLs in the file and print any that cannot be read'
        if file == "-":
            s = sys.stdin.read()
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
        for url in urls:
            if d["-s"]:
                print(f"{file}:  {url!r}")
            else:
                not_ok, status = URL_is_unreadable(url, file)
                if not_ok:
                    print(f"{file}:  {url!r}, status = {status}")
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        CheckFile(file)
