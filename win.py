'''
Module's on_windows variable when True indicates we should use
Windows-style path names.
'''

import sys
from pdb import set_trace as xx 

#xx()

systems = {
'3.6.1 (default, Mar 24 2017, 12:50:34) \n[GCC 5.4.0]': False,
'2.7.13 (default, Mar 14 2017, 23:27:55) \n[GCC 5.4.0]': False,
'2.7.16 (default, Mar 20 2019, 12:29:04) \n[GCC 7.4.0]': False,
'3.6.8 (default, Feb 15 2019, 01:54:23) \n[GCC 7.4.0]': False,
'2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]': True,
'3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 07:18:10) [MSC v.1900 32 bit (Intel)]': True,
'3.6.1 (v3.6.1:69c0db5, Mar 21 2017, 18:41:36) [MSC v.1900 64 bit (AMD64)]': True,
'3.7.4 (default, Jul 21 2019, 15:59:45) \n[GCC 7.4.0]': False,
'3.7.7 (default, Apr 10 2020, 13:49:17) \n[GCC 9.3.0]': False,
}
on_windows = systems[sys.version]
