'''
TODO:
    * Change sorting method on revision numbers so they sort into
      numerical order.

Python release dates
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2018 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Python release dates
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    from datetime import date
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
    from bidict import bidict
    from columnize import Columnize
if 1:   # Global variables
    # From https://www.python.org/downloads
    # Downloaded 22 Jul 2021
    data = dedent('''
        3.9.6 Jun 28 2021
        3.8.11 Jun 28 2021
        3.7.11 Jun 28 2021
        3.6.14 Jun 28 2021
        3.9.5 May 3 2021
        3.8.10 May 3 2021
        3.9.4 Apr 4 2021
        3.8.9 Apr 2 2021
        3.9.2 Feb 19 2021
        3.8.8 Feb 19 2021
        3.6.13 Feb 15 2021
        3.7.10 Feb 15 2021
        3.8.7 Dec 21 2020
        3.9.1 Dec 7 2020
        3.9.0 Oct 5 2020
        3.8.6 Sep 24 2020
        3.5.10 Sep 5 2020
        3.7.9 Aug 17 2020
        3.6.12 Aug 17 2020
        3.8.5 Jul 20 2020
        3.8.4 Jul 13 2020
        3.7.8 Jun 27 2020
        3.6.11 Jun 27 2020
        3.8.3 May 13 2020
        2.7.18 Apr 20 2020
        3.7.7 Mar 10 2020
        3.8.2 Feb 24 2020
        3.8.1 Dec 18 2019
        3.7.6 Dec 18 2019
        3.6.10 Dec 18 2019
        3.5.9 Nov 2 2019
        3.5.8 Oct 29 2019
        2.7.17 Oct 19 2019
        3.7.5 Oct 15 2019
        3.8.0 Oct 14 2019
        3.7.4 Jul 8 2019
        3.6.9 Jul 2 2019
        3.7.3 Mar 25 2019
        3.4.10 Mar 18 2019
        3.5.7 Mar 18 2019
        2.7.16 Mar 4 2019
        3.7.2 Dec 24 2018
        3.6.8 Dec 24 2018
        3.7.1 Oct 20 2018
        3.6.7 Oct 20 2018
        3.5.6 Aug 2 2018
        3.4.9 Aug 2 2018
        3.7.0 Jun 27 2018
        3.6.6 Jun 27 2018
        2.7.15 May 1 2018
        3.6.5 Mar 28 2018
        3.4.8 Feb 5 2018
        3.5.5 Feb 5 2018
        3.6.4 Dec 19 2017
        3.6.3 Oct 3 2017
        3.3.7 Sep 19 2017
        2.7.14 Sep 16 2017
        3.4.7 Aug 9 2017
        3.5.4 Aug 8 2017
        3.6.2 Jul 17 2017
        3.6.1 Mar 21 2017
        3.4.6 Jan 17 2017
        3.5.3 Jan 17 2017
        3.6.0 Dec 23 2016
        2.7.13 Dec 17 2016
        3.4.5 Jun 27 2016
        3.5.2 Jun 27 2016
        2.7.12 Jun 25 2016
        3.4.4 Dec 21 2015
        3.5.1 Dec 7 2015
        2.7.11 Dec 5 2015
        3.5.0 Sep 13 2015
        2.7.10 May 23 2015
        3.4.3 Feb 25 2015
        2.7.9 Dec 10 2014
        3.4.2 Oct 13 2014
        3.3.6 Oct 12 2014
        3.2.6 Oct 12 2014
        2.7.8 Jul 2 2014
        2.7.7 Jun 1 2014
        3.4.1 May 19 2014
        3.4.0 Mar 17 2014
        3.3.5 Mar 9 2014
        3.3.4 Feb 9 2014
        3.3.3 Nov 17 2013
        2.7.6 Nov 10 2013
        2.6.9 Oct 29 2013
        3.3.2 May 15 2013
        3.2.5 May 15 2013
        2.7.5 May 12 2013
        2.7.4 Apr 6 2013
        3.3.1 Apr 6 2013
        3.2.4 Apr 6 2013
        3.3.0 Sep 29 2012
        3.2.3 Apr 10 2012
        2.6.8 Apr 10 2012
        3.1.5 Apr 9 2012
        2.7.3 Apr 9 2012
        3.2.2 Sep 3 2011
        3.2.1 Jul 9 2011
        3.1.4 Jun 11 2011
        2.7.2 Jun 11 2011
        2.6.7 Jun 3 2011
        2.5.6 May 26 2011
        3.2.0 Feb 20 2011
        2.7.1 Nov 27 2010
        3.1.3 Nov 27 2010
        2.6.6 Aug 24 2010
        2.7.0 Jul 3 2010
        3.1.2 Mar 20 2010
        2.6.5 Mar 18 2010
        2.5.5 Jan 31 2010
        2.6.4 Oct 26 2009
        2.6.3 Oct 2 2009
        3.1.1 Aug 17 2009
        3.1.0 Jun 26 2009
        2.6.2 Apr 14 2009
        3.0.1 Feb 13 2009
        2.5.4 Dec 23 2008
        2.4.6 Dec 19 2008
        2.5.3 Dec 19 2008
        2.6.1 Dec 4 2008
        3.0.0 Dec 3 2008
        2.6.0 Oct 2 2008
        2.4.5 Mar 11 2008
        2.3.7 Mar 11 2008
        2.5.2 Feb 21 2008
        2.5.1 Apr 19 2007
        2.3.6 Nov 1 2006
        2.4.4 Oct 18 2006
        2.5.0 Sep 19 2006
        2.4.3 Apr 15 2006
        2.4.2 Sep 27 2005
        2.4.1 Mar 30 2005
        2.3.5 Feb 8 2005
        2.4.0 Nov 30 2004
        2.3.4 May 27 2004
        2.3.3 Dec 19 2003
        2.3.2 Oct 3 2003
        2.3.1 Sep 23 2003
        2.3.0 Jul 29 2003
        2.2.3 May 30 2003
        2.2.2 Oct 14 2002
        2.2.1 Apr 10 2002
        2.1.3 Apr 9 2002
        2.2.0 Dec 21 2001
        2.0.1 Jun 22 2001
        ''')
    months = bidict({
        1 : "Jan", 2 : "Feb", 3 : "Mar", 4 : "Apr", 5 : "May", 6 : "Jun",
        7 : "Jul", 8 : "Aug", 9 : "Sep", 10 : "Oct", 11 : "Nov", 12 : "Dec"})
if __name__ == "__main__": 
    byrev, bydate = [], []
    for i, item in enumerate(data.split("\n")):
        rev, month, day, year = item.split()
        dt = date(int(year), months(month), int(day))
        byrev.append((rev, dt))
        bydate.append((dt, rev))
    # Print by revision
    o = []
    print("Python revisions sorted by revision:")
    for rev, dt in sorted(byrev):
        o.append(f"{rev:7s} {dt.day}{months[dt.month]}{dt.year}")
    for line in Columnize(o, indent=" "*2):
        print(line)
    print()
    # Print by date
    o = []
    print("Python revisions sorted by date:")
    for dt, rev in sorted(bydate):
        o.append(f"{rev:7s} {dt.day}{months[dt.month]}{dt.year}")
    for line in Columnize(o, indent=" "*2):
        print(line)
