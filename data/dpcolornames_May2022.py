# Name strings to Color instance mapping 3 May 2022
#
#    This file is my basic set of colors for use in terminal programs with the color.py
#    module.
#
#    The first set of 12 colors were motivated by the resistor color code: blk brn red
#    orn yel grn blu vio gry wht.  I added cyn and mag because these two colors are used
#    a lot.  Suffixes of "d" for "dark", "l" for "light" and "b" for "background" were
#    added.  Most of these are gotten by changing the L parameter in the hue, lightness,
#    saturation coordinates.  Small inconsistencies exist in the hex strings for these
#    HLS definitions because of float rounding characteristics of the python colorsys
#    module's functions.
#
#    The second set of color names added the following names, trying to stick with a
#    3-letter naming scheme:
#
#        - pnk   Pink
#        - lip   Lipstick
#        - lav   Lavender
#        - lil   Lilac
#        - pur   Purple
#        - roy   Royal blue
#        - den   Denim
#        - sky   Sky blue
#        - trq   Turquoise
#        - sea   Sea green
#        - lwn   Lawn
#        - olv   Olive
#
#    A naming goal was that the name should evoke that color in my mind.  This, of
#    course, is subjective, so feel free to define things to your needs.
#
#    Note these definitions rely on a 24-bit color environment.  'python color.py l'
#    will print these out, along with the closest ANSI 8-bit color that matches each
#    definition.
#
# Assessment 17 May 2025 
#
#   I have been using these 96 color names for about 3 years and they have served my
#   needs well.  Probably their most important feature is the short names are easily
#   remembered.  This lets me get a color I want quickly in a python script, as I just
#   use e.g.
#
#       from color import t
#       t.print(f"{t.redl}Error message")
#
#   to get an error message in red (an update was to add these names as attributes to
#   the t instance of class TRM).  I use a wht on blk terminal window and the most
#   visible colors to my eyes (and hence the ones I use the most) are ornl, yell, grnl,
#   royl, and lavl/purl.
#
# Copyright © 2022 Don Peterson
# MIT License:  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 

{
    "blk" : "$000000",
    "blkd": "$001e00",
    "blkl": "$003c00",
    "blkb": "$00b400",
    "gry" : "$006400",
    "gryd": "$005000",
    "gryl": "$009600",
    "gryb": "$00d200",
    "wht" : "$00b400",
    "whtd": "$008200",
    "whtl": "$00ff00",
    "whtb": "$00e600",
    "blu" : "$aa80ff",
    "blud": "$aa40ff",
    "blul": "$aaa0ff",
    "blub": "$aae0ff",
    "brn" : "$154bff",
    "brnd": "$1434ff",
    "brnl": "$15b0ff",
    "brnb": "$14e0ff",
    "cyn" : "$7e4cff",
    "cynd": "$7e35ff",
    "cynl": "$7f80ff",
    "cynb": "$7ed9ff",
    "grn" : "$555aff",
    "grnd": "$5540ff",
    "grnl": "$5580ff",
    "grnb": "$55e0ff",
    "mag" : "$d450ff",
    "magd": "$d33eff",
    "magl": "$d480ff",
    "magb": "$d3e0ff",
    "orn" : "$0f60ff",
    "ornd": "$0f40ff",
    "ornl": "$0f90ff",
    "ornb": "$0fe0ff",
    "red" : "$0050ff",
    "redd": "$0034ff",
    "redl": "$0080ff",
    "redb": "$00e0ff",
    "vio" : "$c080ff",
    "viod": "$c040ff",
    "viol": "$c0a0ff",
    "viob": "$c0e0ff",
    "yel" : "$2960ff",
    "yeld": "$2940ff",
    "yell": "$2a80ff",
    "yelb": "$29e0ff",
    "pnk" : "$f79885",
    "pnkd": "$f75f71",
    "pnkl": "$f7d0ff",
    "pnkb": "$f7db63",
    "lip" : "$ef6bf3",
    "lipd": "$ef40ff",
    "lipl": "$efc0ff",
    "lipb": "$efe0ff",
    "lav" : "$c29f91",
    "lavd": "$c24794",
    "lavl": "$c2c790",
    "lavb": "$c2df8d",
    "lil" : "$babfae",
    "lild": "$ba5fb1",
    "lill": "$bacfae",
    "lilb": "$b9dfae",
    "pur" : "$c65fc1",
    "purd": "$c63fc2",
    "purl": "$c5afbe",
    "purb": "$c6dfbe",
    "roy" : "$9f9fbe",
    "royd": "$9f4fc2",
    "royl": "$9fb0be",
    "royb": "$9fdfbe",
    "den" : "$966fc1",
    "dend": "$973fc2",
    "denl": "$97b0be",
    "denb": "$97dfbe",
    "sky" : "$90c3ff",
    "skyd": "$9040ff",
    "skyl": "$90d7ff",
    "skyb": "$90e0ff",
    "trq" : "$7370ff",
    "trqd": "$7240ff",
    "trql": "$72b0ff",
    "trqb": "$72e0ff",
    "sea" : "$677f7f",
    "sead": "$673f7e",
    "seal": "$67af7e",
    "seab": "$66df7d",
    "lwn" : "$425fe4",
    "lwnd": "$423fe6",
    "lwnl": "$42a1e3",
    "lwnb": "$41dfde",
    "olv" : "$38609a",
    "olvd": "$373f9a",
    "olvl": "$37af98",
    "olvb": "$38df95",
}
