'''
Ping routine for the local network:  Show the IP addresses on 192.168.0.0
that respond.

Typical results
    1       CenturyLink ZyXEL PK5001Z cable modem
    36      Don's Windows machine
    49      LaserJet 4050 printer
    55      ?
    154     Glenda's Windows machine (doesn't shown on scan)

Code idea from here:
https://www.tutorialspoint.com/python_penetration_testing/python_penetration_testing_network_scanner.htm
'''

import os
from time import time
from color import TRM as t

ip = "192.168.0."
ping = "ping -c 1 "
trigger = "ttl="
end = " "*2
start = time()

for i in range(1, 255):
    addr = ip + str(i)
    s = os.popen(ping + addr).read()
    if "ttl=" in s:
        print(f"{t('grn')}{addr}{t.n}", end=end)
    else:
        print(addr, end=end)
    if i % 5 == 0:
        print()
print()
t = (time() - start)/60
print(f"Scan took {t:.1d} minutes")
