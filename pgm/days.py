'''
Print number of days from a given date
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Print number of days from a given date
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import time
    import getopt
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
    import julian
def Usage(status=1):
    name = sys.argv[0]
    print(dedent(f'''
    Usage:  {name} [options] [date]
      Prints the number of days since a reference date.  Use 'today' for
      the current moment.  Otherwise, the date must be of the form
      DDMMMYYYY, such as 1Jan2000.
    Options:
      -r ref    Specify the reference date in the form DDMMMYYYY.
                The default is {d["-r"]}.
    '''))
    exit(status)
def ParseDate(s):
    '''Assumes s is of the form DDMMMYYYY and returns a tuple of (year,
    month, day).
    '''
    # Get the day; can be one or two digits.
    day, i = "", 0
    while s[i] in "1234567890":
        day += s[i]
        i += 1
    s = s[i:]
    day = int(day)
    # Next three letters must be month
    d = {
        "jan" : 1, "feb" : 2, "mar" : 3, "apr" : 4, "may" : 5, "jun" : 6,
        "jul" : 7, "aug" : 8, "sep" : 9, "oct" : 10, "nov" : 11, "dec" : 12}
    month = d[s[:3].lower()]
    # Year is last four digits
    year = int(s[3:])
    return year, month, day
def NormalizeDate(s):
    '''Returns a string of the form YYYYMMDD where the characters represent
    digits.  This is the form needed by the julian module.  s is the
    output of ParseDate().
    '''
    year, month, day = s
    return f"{year:04d}{month:02d}{day:02d}"
def ParseCommandLine(d):
    d["-r"] = "1Jan2020"
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "hr:")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for opt in optlist:
        if opt[0] == "-h":
            Usage(0)
        if opt[0] == "-r":
            d["-r"] = opt[1]
    if not args:
        Usage(1)
    return args
def Now():
    s = time.strftime("%d%b%Y")
    if s[0] == "0":
        s = s[1:]
    return s
def Today():
    'Return a normalized string for this moment'
    s = Now()
    return NormalizeDate(ParseDate(s))
if __name__ == "__main__": 
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if args[0] == "today":
        print(f"today = {Now()}")
        t = Today()
    else:
        t = NormalizeDate(ParseDate(args[0]))
    ref = d["-r"]
    j = julian.Julian1
    dt = j(t) - j(NormalizeDate(ParseDate(ref)))
    print(f"Days from reference date {ref} = {dt}")
