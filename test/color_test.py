import subprocess
import os
import sys
import color as c
from lwtest import run
from pdb import set_trace as xx

pyver = sys.version_info[0]
nl = "\n"

expected_lines = '''
[1;36;40mBackground -->  black   blue    green   cyan    red    magenta  brown   white
[0;37;40mblack (0)      [0;30;40mwxyz 00[0;37;40m [0;30;44mwxyz 10[0;37;40m [0;30;42mwxyz 20[0;37;40m [0;30;46mwxyz 30[0;37;40m [0;30;41mwxyz 40[0;37;40m [0;30;45mwxyz 50[0;37;40m [0;30;43mwxyz 60[0;37;40m [0;30;47mwxyz 70[0;37;40m [0;37;40m
[0;37;40mblue (1)       [0;34;40mwxyz 01[0;37;40m [0;34;44mwxyz 11[0;37;40m [0;34;42mwxyz 21[0;37;40m [0;34;46mwxyz 31[0;37;40m [0;34;41mwxyz 41[0;37;40m [0;34;45mwxyz 51[0;37;40m [0;34;43mwxyz 61[0;37;40m [0;34;47mwxyz 71[0;37;40m [0;37;40m
[0;37;40mgreen (2)      [0;32;40mwxyz 02[0;37;40m [0;32;44mwxyz 12[0;37;40m [0;32;42mwxyz 22[0;37;40m [0;32;46mwxyz 32[0;37;40m [0;32;41mwxyz 42[0;37;40m [0;32;45mwxyz 52[0;37;40m [0;32;43mwxyz 62[0;37;40m [0;32;47mwxyz 72[0;37;40m [0;37;40m
[0;37;40mcyan (3)       [0;36;40mwxyz 03[0;37;40m [0;36;44mwxyz 13[0;37;40m [0;36;42mwxyz 23[0;37;40m [0;36;46mwxyz 33[0;37;40m [0;36;41mwxyz 43[0;37;40m [0;36;45mwxyz 53[0;37;40m [0;36;43mwxyz 63[0;37;40m [0;36;47mwxyz 73[0;37;40m [0;37;40m
[0;37;40mred (4)        [0;31;40mwxyz 04[0;37;40m [0;31;44mwxyz 14[0;37;40m [0;31;42mwxyz 24[0;37;40m [0;31;46mwxyz 34[0;37;40m [0;31;41mwxyz 44[0;37;40m [0;31;45mwxyz 54[0;37;40m [0;31;43mwxyz 64[0;37;40m [0;31;47mwxyz 74[0;37;40m [0;37;40m
[0;37;40mmagenta (5)    [0;35;40mwxyz 05[0;37;40m [0;35;44mwxyz 15[0;37;40m [0;35;42mwxyz 25[0;37;40m [0;35;46mwxyz 35[0;37;40m [0;35;41mwxyz 45[0;37;40m [0;35;45mwxyz 55[0;37;40m [0;35;43mwxyz 65[0;37;40m [0;35;47mwxyz 75[0;37;40m [0;37;40m
[0;37;40mbrown (6)      [0;33;40mwxyz 06[0;37;40m [0;33;44mwxyz 16[0;37;40m [0;33;42mwxyz 26[0;37;40m [0;33;46mwxyz 36[0;37;40m [0;33;41mwxyz 46[0;37;40m [0;33;45mwxyz 56[0;37;40m [0;33;43mwxyz 66[0;37;40m [0;33;47mwxyz 76[0;37;40m [0;37;40m
[0;37;40mwhite (7)      [0;37;40mwxyz 07[0;37;40m [0;37;44mwxyz 17[0;37;40m [0;37;42mwxyz 27[0;37;40m [0;37;46mwxyz 37[0;37;40m [0;37;41mwxyz 47[0;37;40m [0;37;45mwxyz 57[0;37;40m [0;37;43mwxyz 67[0;37;40m [0;37;47mwxyz 77[0;37;40m [0;37;40m
[0;37;40mgray (8)       [1;30;40mwxyz 08[0;37;40m [1;30;44mwxyz 18[0;37;40m [1;30;42mwxyz 28[0;37;40m [1;30;46mwxyz 38[0;37;40m [1;30;41mwxyz 48[0;37;40m [1;30;45mwxyz 58[0;37;40m [1;30;43mwxyz 68[0;37;40m [1;30;47mwxyz 78[0;37;40m [0;37;40m
[0;37;40mlblue (9)      [1;34;40mwxyz 09[0;37;40m [1;34;44mwxyz 19[0;37;40m [1;34;42mwxyz 29[0;37;40m [1;34;46mwxyz 39[0;37;40m [1;34;41mwxyz 49[0;37;40m [1;34;45mwxyz 59[0;37;40m [1;34;43mwxyz 69[0;37;40m [1;34;47mwxyz 79[0;37;40m [0;37;40m
[0;37;40mlgreen (10)    [1;32;40mwxyz 0a[0;37;40m [1;32;44mwxyz 1a[0;37;40m [1;32;42mwxyz 2a[0;37;40m [1;32;46mwxyz 3a[0;37;40m [1;32;41mwxyz 4a[0;37;40m [1;32;45mwxyz 5a[0;37;40m [1;32;43mwxyz 6a[0;37;40m [1;32;47mwxyz 7a[0;37;40m [0;37;40m
[0;37;40mlcyan (11)     [1;36;40mwxyz 0b[0;37;40m [1;36;44mwxyz 1b[0;37;40m [1;36;42mwxyz 2b[0;37;40m [1;36;46mwxyz 3b[0;37;40m [1;36;41mwxyz 4b[0;37;40m [1;36;45mwxyz 5b[0;37;40m [1;36;43mwxyz 6b[0;37;40m [1;36;47mwxyz 7b[0;37;40m [0;37;40m
[0;37;40mlred (12)      [1;31;40mwxyz 0c[0;37;40m [1;31;44mwxyz 1c[0;37;40m [1;31;42mwxyz 2c[0;37;40m [1;31;46mwxyz 3c[0;37;40m [1;31;41mwxyz 4c[0;37;40m [1;31;45mwxyz 5c[0;37;40m [1;31;43mwxyz 6c[0;37;40m [1;31;47mwxyz 7c[0;37;40m [0;37;40m
[0;37;40mlmagenta (13)  [1;35;40mwxyz 0d[0;37;40m [1;35;44mwxyz 1d[0;37;40m [1;35;42mwxyz 2d[0;37;40m [1;35;46mwxyz 3d[0;37;40m [1;35;41mwxyz 4d[0;37;40m [1;35;45mwxyz 5d[0;37;40m [1;35;43mwxyz 6d[0;37;40m [1;35;47mwxyz 7d[0;37;40m [0;37;40m
[0;37;40myellow (14)    [1;33;40mwxyz 0e[0;37;40m [1;33;44mwxyz 1e[0;37;40m [1;33;42mwxyz 2e[0;37;40m [1;33;46mwxyz 3e[0;37;40m [1;33;41mwxyz 4e[0;37;40m [1;33;45mwxyz 5e[0;37;40m [1;33;43mwxyz 6e[0;37;40m [1;33;47mwxyz 7e[0;37;40m [0;37;40m
[0;37;40mlwhite (15)    [1;37;40mwxyz 0f[0;37;40m [1;37;44mwxyz 1f[0;37;40m [1;37;42mwxyz 2f[0;37;40m [1;37;46mwxyz 3f[0;37;40m [1;37;41mwxyz 4f[0;37;40m [1;37;45mwxyz 5f[0;37;40m [1;37;43mwxyz 6f[0;37;40m [1;37;47mwxyz 7f[0;37;40m [0;37;40m
[1;36;40m
Background -->  gray    lblue   lgreen  lcyan   lred  lmagenta yellow  lWhite
[0;37;40mblack (0)      [0;30;40mwxyz 80[0;37;40m [0;30;44mwxyz 90[0;37;40m [0;30;42mwxyz a0[0;37;40m [0;30;46mwxyz b0[0;37;40m [0;30;41mwxyz c0[0;37;40m [0;30;45mwxyz d0[0;37;40m [0;30;43mwxyz e0[0;37;40m [0;30;47mwxyz f0[0;37;40m [0;37;40m
[0;37;40mblue (1)       [0;34;40mwxyz 81[0;37;40m [0;34;44mwxyz 91[0;37;40m [0;34;42mwxyz a1[0;37;40m [0;34;46mwxyz b1[0;37;40m [0;34;41mwxyz c1[0;37;40m [0;34;45mwxyz d1[0;37;40m [0;34;43mwxyz e1[0;37;40m [0;34;47mwxyz f1[0;37;40m [0;37;40m
[0;37;40mgreen (2)      [0;32;40mwxyz 82[0;37;40m [0;32;44mwxyz 92[0;37;40m [0;32;42mwxyz a2[0;37;40m [0;32;46mwxyz b2[0;37;40m [0;32;41mwxyz c2[0;37;40m [0;32;45mwxyz d2[0;37;40m [0;32;43mwxyz e2[0;37;40m [0;32;47mwxyz f2[0;37;40m [0;37;40m
[0;37;40mcyan (3)       [0;36;40mwxyz 83[0;37;40m [0;36;44mwxyz 93[0;37;40m [0;36;42mwxyz a3[0;37;40m [0;36;46mwxyz b3[0;37;40m [0;36;41mwxyz c3[0;37;40m [0;36;45mwxyz d3[0;37;40m [0;36;43mwxyz e3[0;37;40m [0;36;47mwxyz f3[0;37;40m [0;37;40m
[0;37;40mred (4)        [0;31;40mwxyz 84[0;37;40m [0;31;44mwxyz 94[0;37;40m [0;31;42mwxyz a4[0;37;40m [0;31;46mwxyz b4[0;37;40m [0;31;41mwxyz c4[0;37;40m [0;31;45mwxyz d4[0;37;40m [0;31;43mwxyz e4[0;37;40m [0;31;47mwxyz f4[0;37;40m [0;37;40m
[0;37;40mmagenta (5)    [0;35;40mwxyz 85[0;37;40m [0;35;44mwxyz 95[0;37;40m [0;35;42mwxyz a5[0;37;40m [0;35;46mwxyz b5[0;37;40m [0;35;41mwxyz c5[0;37;40m [0;35;45mwxyz d5[0;37;40m [0;35;43mwxyz e5[0;37;40m [0;35;47mwxyz f5[0;37;40m [0;37;40m
[0;37;40mbrown (6)      [0;33;40mwxyz 86[0;37;40m [0;33;44mwxyz 96[0;37;40m [0;33;42mwxyz a6[0;37;40m [0;33;46mwxyz b6[0;37;40m [0;33;41mwxyz c6[0;37;40m [0;33;45mwxyz d6[0;37;40m [0;33;43mwxyz e6[0;37;40m [0;33;47mwxyz f6[0;37;40m [0;37;40m
[0;37;40mwhite (7)      [0;37;40mwxyz 87[0;37;40m [0;37;44mwxyz 97[0;37;40m [0;37;42mwxyz a7[0;37;40m [0;37;46mwxyz b7[0;37;40m [0;37;41mwxyz c7[0;37;40m [0;37;45mwxyz d7[0;37;40m [0;37;43mwxyz e7[0;37;40m [0;37;47mwxyz f7[0;37;40m [0;37;40m
[0;37;40mgray (8)       [1;30;40mwxyz 88[0;37;40m [1;30;44mwxyz 98[0;37;40m [1;30;42mwxyz a8[0;37;40m [1;30;46mwxyz b8[0;37;40m [1;30;41mwxyz c8[0;37;40m [1;30;45mwxyz d8[0;37;40m [1;30;43mwxyz e8[0;37;40m [1;30;47mwxyz f8[0;37;40m [0;37;40m
[0;37;40mlblue (9)      [1;34;40mwxyz 89[0;37;40m [1;34;44mwxyz 99[0;37;40m [1;34;42mwxyz a9[0;37;40m [1;34;46mwxyz b9[0;37;40m [1;34;41mwxyz c9[0;37;40m [1;34;45mwxyz d9[0;37;40m [1;34;43mwxyz e9[0;37;40m [1;34;47mwxyz f9[0;37;40m [0;37;40m
[0;37;40mlgreen (10)    [1;32;40mwxyz 8a[0;37;40m [1;32;44mwxyz 9a[0;37;40m [1;32;42mwxyz aa[0;37;40m [1;32;46mwxyz ba[0;37;40m [1;32;41mwxyz ca[0;37;40m [1;32;45mwxyz da[0;37;40m [1;32;43mwxyz ea[0;37;40m [1;32;47mwxyz fa[0;37;40m [0;37;40m
[0;37;40mlcyan (11)     [1;36;40mwxyz 8b[0;37;40m [1;36;44mwxyz 9b[0;37;40m [1;36;42mwxyz ab[0;37;40m [1;36;46mwxyz bb[0;37;40m [1;36;41mwxyz cb[0;37;40m [1;36;45mwxyz db[0;37;40m [1;36;43mwxyz eb[0;37;40m [1;36;47mwxyz fb[0;37;40m [0;37;40m
[0;37;40mlred (12)      [1;31;40mwxyz 8c[0;37;40m [1;31;44mwxyz 9c[0;37;40m [1;31;42mwxyz ac[0;37;40m [1;31;46mwxyz bc[0;37;40m [1;31;41mwxyz cc[0;37;40m [1;31;45mwxyz dc[0;37;40m [1;31;43mwxyz ec[0;37;40m [1;31;47mwxyz fc[0;37;40m [0;37;40m
[0;37;40mlmagenta (13)  [1;35;40mwxyz 8d[0;37;40m [1;35;44mwxyz 9d[0;37;40m [1;35;42mwxyz ad[0;37;40m [1;35;46mwxyz bd[0;37;40m [1;35;41mwxyz cd[0;37;40m [1;35;45mwxyz dd[0;37;40m [1;35;43mwxyz ed[0;37;40m [1;35;47mwxyz fd[0;37;40m [0;37;40m
[0;37;40myellow (14)    [1;33;40mwxyz 8e[0;37;40m [1;33;44mwxyz 9e[0;37;40m [1;33;42mwxyz ae[0;37;40m [1;33;46mwxyz be[0;37;40m [1;33;41mwxyz ce[0;37;40m [1;33;45mwxyz de[0;37;40m [1;33;43mwxyz ee[0;37;40m [1;33;47mwxyz fe[0;37;40m [0;37;40m
[0;37;40mlwhite (15)    [1;37;40mwxyz 8f[0;37;40m [1;37;44mwxyz 9f[0;37;40m [1;37;42mwxyz af[0;37;40m [1;37;46mwxyz bf[0;37;40m [1;37;41mwxyz cf[0;37;40m [1;37;45mwxyz df[0;37;40m [1;37;43mwxyz ef[0;37;40m [1;37;47mwxyz ff[0;37;40m [0;37;40m
Styles:  [0;37;40m[0mnormal[0m [0;37;40m[1mbold[0m [0;37;40m[3mitalic[0m [0;37;40m[4munderline[0m [0;37;40m[5mblink[0m [0;37;40m[7mreverse[0m [0;37;40m
'''[1:-1].split(nl)

expected_lines = '''
[1;36;40mBackground -->  black   blue    green   cyan    red    magenta  brown   white
[0;37;40mblack (0)      [0;30;40mwxyz 00[0;37;40m [0;30;44mwxyz 10[0;37;40m [0;30;42mwxyz 20[0;37;40m [0;30;46mwxyz 30[0;37;40m [0;30;41mwxyz 40[0;37;40m [0;30;45mwxyz 50[0;37;40m [0;30;43mwxyz 60[0;37;40m [0;30;47mwxyz 70[0;37;40m [0;37;40m
[0;37;40mblue (1)       [0;34;40mwxyz 01[0;37;40m [0;34;44mwxyz 11[0;37;40m [0;34;42mwxyz 21[0;37;40m [0;34;46mwxyz 31[0;37;40m [0;34;41mwxyz 41[0;37;40m [0;34;45mwxyz 51[0;37;40m [0;34;43mwxyz 61[0;37;40m [0;34;47mwxyz 71[0;37;40m [0;37;40m
[0;37;40mgreen (2)      [0;32;40mwxyz 02[0;37;40m [0;32;44mwxyz 12[0;37;40m [0;32;42mwxyz 22[0;37;40m [0;32;46mwxyz 32[0;37;40m [0;32;41mwxyz 42[0;37;40m [0;32;45mwxyz 52[0;37;40m [0;32;43mwxyz 62[0;37;40m [0;32;47mwxyz 72[0;37;40m [0;37;40m
[0;37;40mcyan (3)       [0;36;40mwxyz 03[0;37;40m [0;36;44mwxyz 13[0;37;40m [0;36;42mwxyz 23[0;37;40m [0;36;46mwxyz 33[0;37;40m [0;36;41mwxyz 43[0;37;40m [0;36;45mwxyz 53[0;37;40m [0;36;43mwxyz 63[0;37;40m [0;36;47mwxyz 73[0;37;40m [0;37;40m
[0;37;40mred (4)        [0;31;40mwxyz 04[0;37;40m [0;31;44mwxyz 14[0;37;40m [0;31;42mwxyz 24[0;37;40m [0;31;46mwxyz 34[0;37;40m [0;31;41mwxyz 44[0;37;40m [0;31;45mwxyz 54[0;37;40m [0;31;43mwxyz 64[0;37;40m [0;31;47mwxyz 74[0;37;40m [0;37;40m
[0;37;40mmagenta (5)    [0;35;40mwxyz 05[0;37;40m [0;35;44mwxyz 15[0;37;40m [0;35;42mwxyz 25[0;37;40m [0;35;46mwxyz 35[0;37;40m [0;35;41mwxyz 45[0;37;40m [0;35;45mwxyz 55[0;37;40m [0;35;43mwxyz 65[0;37;40m [0;35;47mwxyz 75[0;37;40m [0;37;40m
[0;37;40mbrown (6)      [0;33;40mwxyz 06[0;37;40m [0;33;44mwxyz 16[0;37;40m [0;33;42mwxyz 26[0;37;40m [0;33;46mwxyz 36[0;37;40m [0;33;41mwxyz 46[0;37;40m [0;33;45mwxyz 56[0;37;40m [0;33;43mwxyz 66[0;37;40m [0;33;47mwxyz 76[0;37;40m [0;37;40m
[0;37;40mwhite (7)      [0;37;40mwxyz 07[0;37;40m [0;37;44mwxyz 17[0;37;40m [0;37;42mwxyz 27[0;37;40m [0;37;46mwxyz 37[0;37;40m [0;37;41mwxyz 47[0;37;40m [0;37;45mwxyz 57[0;37;40m [0;37;43mwxyz 67[0;37;40m [0;37;47mwxyz 77[0;37;40m [0;37;40m
[0;37;40mgray (8)       [1;30;40mwxyz 08[0;37;40m [1;30;44mwxyz 18[0;37;40m [1;30;42mwxyz 28[0;37;40m [1;30;46mwxyz 38[0;37;40m [1;30;41mwxyz 48[0;37;40m [1;30;45mwxyz 58[0;37;40m [1;30;43mwxyz 68[0;37;40m [1;30;47mwxyz 78[0;37;40m [0;37;40m
[0;37;40mlblue (9)      [1;34;40mwxyz 09[0;37;40m [1;34;44mwxyz 19[0;37;40m [1;34;42mwxyz 29[0;37;40m [1;34;46mwxyz 39[0;37;40m [1;34;41mwxyz 49[0;37;40m [1;34;45mwxyz 59[0;37;40m [1;34;43mwxyz 69[0;37;40m [1;34;47mwxyz 79[0;37;40m [0;37;40m
[0;37;40mlgreen (10)    [1;32;40mwxyz 0a[0;37;40m [1;32;44mwxyz 1a[0;37;40m [1;32;42mwxyz 2a[0;37;40m [1;32;46mwxyz 3a[0;37;40m [1;32;41mwxyz 4a[0;37;40m [1;32;45mwxyz 5a[0;37;40m [1;32;43mwxyz 6a[0;37;40m [1;32;47mwxyz 7a[0;37;40m [0;37;40m
[0;37;40mlcyan (11)     [1;36;40mwxyz 0b[0;37;40m [1;36;44mwxyz 1b[0;37;40m [1;36;42mwxyz 2b[0;37;40m [1;36;46mwxyz 3b[0;37;40m [1;36;41mwxyz 4b[0;37;40m [1;36;45mwxyz 5b[0;37;40m [1;36;43mwxyz 6b[0;37;40m [1;36;47mwxyz 7b[0;37;40m [0;37;40m
[0;37;40mlred (12)      [1;31;40mwxyz 0c[0;37;40m [1;31;44mwxyz 1c[0;37;40m [1;31;42mwxyz 2c[0;37;40m [1;31;46mwxyz 3c[0;37;40m [1;31;41mwxyz 4c[0;37;40m [1;31;45mwxyz 5c[0;37;40m [1;31;43mwxyz 6c[0;37;40m [1;31;47mwxyz 7c[0;37;40m [0;37;40m
[0;37;40mlmagenta (13)  [1;35;40mwxyz 0d[0;37;40m [1;35;44mwxyz 1d[0;37;40m [1;35;42mwxyz 2d[0;37;40m [1;35;46mwxyz 3d[0;37;40m [1;35;41mwxyz 4d[0;37;40m [1;35;45mwxyz 5d[0;37;40m [1;35;43mwxyz 6d[0;37;40m [1;35;47mwxyz 7d[0;37;40m [0;37;40m
[0;37;40myellow (14)    [1;33;40mwxyz 0e[0;37;40m [1;33;44mwxyz 1e[0;37;40m [1;33;42mwxyz 2e[0;37;40m [1;33;46mwxyz 3e[0;37;40m [1;33;41mwxyz 4e[0;37;40m [1;33;45mwxyz 5e[0;37;40m [1;33;43mwxyz 6e[0;37;40m [1;33;47mwxyz 7e[0;37;40m [0;37;40m
[0;37;40mlwhite (15)    [1;37;40mwxyz 0f[0;37;40m [1;37;44mwxyz 1f[0;37;40m [1;37;42mwxyz 2f[0;37;40m [1;37;46mwxyz 3f[0;37;40m [1;37;41mwxyz 4f[0;37;40m [1;37;45mwxyz 5f[0;37;40m [1;37;43mwxyz 6f[0;37;40m [1;37;47mwxyz 7f[0;37;40m [0;37;40m
[1;36;40m
Background -->  gray    lblue   lgreen  lcyan   lred  lmagenta yellow  lWhite
[0;37;40mblack (0)      [0;30;40mwxyz 80[0;37;40m [0;30;44mwxyz 90[0;37;40m [0;30;42mwxyz a0[0;37;40m [0;30;46mwxyz b0[0;37;40m [0;30;41mwxyz c0[0;37;40m [0;30;45mwxyz d0[0;37;40m [0;30;43mwxyz e0[0;37;40m [0;30;47mwxyz f0[0;37;40m [0;37;40m
[0;37;40mblue (1)       [0;34;40mwxyz 81[0;37;40m [0;34;44mwxyz 91[0;37;40m [0;34;42mwxyz a1[0;37;40m [0;34;46mwxyz b1[0;37;40m [0;34;41mwxyz c1[0;37;40m [0;34;45mwxyz d1[0;37;40m [0;34;43mwxyz e1[0;37;40m [0;34;47mwxyz f1[0;37;40m [0;37;40m
[0;37;40mgreen (2)      [0;32;40mwxyz 82[0;37;40m [0;32;44mwxyz 92[0;37;40m [0;32;42mwxyz a2[0;37;40m [0;32;46mwxyz b2[0;37;40m [0;32;41mwxyz c2[0;37;40m [0;32;45mwxyz d2[0;37;40m [0;32;43mwxyz e2[0;37;40m [0;32;47mwxyz f2[0;37;40m [0;37;40m
[0;37;40mcyan (3)       [0;36;40mwxyz 83[0;37;40m [0;36;44mwxyz 93[0;37;40m [0;36;42mwxyz a3[0;37;40m [0;36;46mwxyz b3[0;37;40m [0;36;41mwxyz c3[0;37;40m [0;36;45mwxyz d3[0;37;40m [0;36;43mwxyz e3[0;37;40m [0;36;47mwxyz f3[0;37;40m [0;37;40m
[0;37;40mred (4)        [0;31;40mwxyz 84[0;37;40m [0;31;44mwxyz 94[0;37;40m [0;31;42mwxyz a4[0;37;40m [0;31;46mwxyz b4[0;37;40m [0;31;41mwxyz c4[0;37;40m [0;31;45mwxyz d4[0;37;40m [0;31;43mwxyz e4[0;37;40m [0;31;47mwxyz f4[0;37;40m [0;37;40m
[0;37;40mmagenta (5)    [0;35;40mwxyz 85[0;37;40m [0;35;44mwxyz 95[0;37;40m [0;35;42mwxyz a5[0;37;40m [0;35;46mwxyz b5[0;37;40m [0;35;41mwxyz c5[0;37;40m [0;35;45mwxyz d5[0;37;40m [0;35;43mwxyz e5[0;37;40m [0;35;47mwxyz f5[0;37;40m [0;37;40m
[0;37;40mbrown (6)      [0;33;40mwxyz 86[0;37;40m [0;33;44mwxyz 96[0;37;40m [0;33;42mwxyz a6[0;37;40m [0;33;46mwxyz b6[0;37;40m [0;33;41mwxyz c6[0;37;40m [0;33;45mwxyz d6[0;37;40m [0;33;43mwxyz e6[0;37;40m [0;33;47mwxyz f6[0;37;40m [0;37;40m
[0;37;40mwhite (7)      [0;37;40mwxyz 87[0;37;40m [0;37;44mwxyz 97[0;37;40m [0;37;42mwxyz a7[0;37;40m [0;37;46mwxyz b7[0;37;40m [0;37;41mwxyz c7[0;37;40m [0;37;45mwxyz d7[0;37;40m [0;37;43mwxyz e7[0;37;40m [0;37;47mwxyz f7[0;37;40m [0;37;40m
[0;37;40mgray (8)       [1;30;40mwxyz 88[0;37;40m [1;30;44mwxyz 98[0;37;40m [1;30;42mwxyz a8[0;37;40m [1;30;46mwxyz b8[0;37;40m [1;30;41mwxyz c8[0;37;40m [1;30;45mwxyz d8[0;37;40m [1;30;43mwxyz e8[0;37;40m [1;30;47mwxyz f8[0;37;40m [0;37;40m
[0;37;40mlblue (9)      [1;34;40mwxyz 89[0;37;40m [1;34;44mwxyz 99[0;37;40m [1;34;42mwxyz a9[0;37;40m [1;34;46mwxyz b9[0;37;40m [1;34;41mwxyz c9[0;37;40m [1;34;45mwxyz d9[0;37;40m [1;34;43mwxyz e9[0;37;40m [1;34;47mwxyz f9[0;37;40m [0;37;40m
[0;37;40mlgreen (10)    [1;32;40mwxyz 8a[0;37;40m [1;32;44mwxyz 9a[0;37;40m [1;32;42mwxyz aa[0;37;40m [1;32;46mwxyz ba[0;37;40m [1;32;41mwxyz ca[0;37;40m [1;32;45mwxyz da[0;37;40m [1;32;43mwxyz ea[0;37;40m [1;32;47mwxyz fa[0;37;40m [0;37;40m
[0;37;40mlcyan (11)     [1;36;40mwxyz 8b[0;37;40m [1;36;44mwxyz 9b[0;37;40m [1;36;42mwxyz ab[0;37;40m [1;36;46mwxyz bb[0;37;40m [1;36;41mwxyz cb[0;37;40m [1;36;45mwxyz db[0;37;40m [1;36;43mwxyz eb[0;37;40m [1;36;47mwxyz fb[0;37;40m [0;37;40m
[0;37;40mlred (12)      [1;31;40mwxyz 8c[0;37;40m [1;31;44mwxyz 9c[0;37;40m [1;31;42mwxyz ac[0;37;40m [1;31;46mwxyz bc[0;37;40m [1;31;41mwxyz cc[0;37;40m [1;31;45mwxyz dc[0;37;40m [1;31;43mwxyz ec[0;37;40m [1;31;47mwxyz fc[0;37;40m [0;37;40m
[0;37;40mlmagenta (13)  [1;35;40mwxyz 8d[0;37;40m [1;35;44mwxyz 9d[0;37;40m [1;35;42mwxyz ad[0;37;40m [1;35;46mwxyz bd[0;37;40m [1;35;41mwxyz cd[0;37;40m [1;35;45mwxyz dd[0;37;40m [1;35;43mwxyz ed[0;37;40m [1;35;47mwxyz fd[0;37;40m [0;37;40m
[0;37;40myellow (14)    [1;33;40mwxyz 8e[0;37;40m [1;33;44mwxyz 9e[0;37;40m [1;33;42mwxyz ae[0;37;40m [1;33;46mwxyz be[0;37;40m [1;33;41mwxyz ce[0;37;40m [1;33;45mwxyz de[0;37;40m [1;33;43mwxyz ee[0;37;40m [1;33;47mwxyz fe[0;37;40m [0;37;40m
[0;37;40mlwhite (15)    [1;37;40mwxyz 8f[0;37;40m [1;37;44mwxyz 9f[0;37;40m [1;37;42mwxyz af[0;37;40m [1;37;46mwxyz bf[0;37;40m [1;37;41mwxyz cf[0;37;40m [1;37;45mwxyz df[0;37;40m [1;37;43mwxyz ef[0;37;40m [1;37;47mwxyz ff[0;37;40m [0;37;40m
Styles:  [0mnormal[0m [1mbold[0m [3mitalic[0m [4munderline[0m [5mblink[0m [7mreverse[0m [0;37;40m
Demo of ColorContext object:
[1;33;40m[3m  In yellow italics
  [1;34;40m[4mIn blue underlined
[0;37;40m  [1;31;40m[7mIn red reverse
[0;37;40m[0;37;40m  Back to normal
Demo of yellow(1) call to get background yellow if f-string: [0;30;43mHi there[0;37;40m
'''[1:].split(nl)

def TestAsScript():
    # Run the color.py module as a script and capture its output.  Compare
    # the results to the above string (remove the first line).
    cmd = os.environ["PYTHON"].split() + [os.environ["PYTHONLIB"] + "/color.py"]
    s = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    if pyver == 3:
        lines = [i.decode("utf8") for i in s.stdout.readlines()]
    else:
        lines = s.stdout.readlines()
    del lines[0]
    lines = [i.rstrip("\n") for i in lines]         # Remove newlines
    # Need to get rid of last line 
    del expected_lines[-1]
    assert(lines == expected_lines)

def TestCanReturnAsString():
    # fg
    got = c.fg(c.lred, s=True)
    expected = "[1;31;40m"
    assert(got == expected)
    # normal
    got = c.normal(s=True)
    expected = "[0;37;40m"
    assert(got == expected)
    # SetStyle
    got = c.SetStyle("underline", s=True)
    expected = "[4m"
    assert(got == expected)

if __name__ == "__main__":
    exit(run(globals())[0])
