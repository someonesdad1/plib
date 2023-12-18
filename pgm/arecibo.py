# Sun 17 Dec 2023 04:08:12 PM
# From https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/cryptologic-spectrum/communications_with_extraterrestrial.pdf

# Page 6 states Barney Oliver made this message in 1961 and it has 1271
# binary digits.

from wrap import dedent
from lwtest import Assert
 
# From Word interpreting the PDF
data1 = '''
1 o o o o o o o o o o o o o O O o o O o o   o o o  o o o o o o o o o O O O o  1 o o o o 1 1 1 o o o O O o 0 o 1 o o O O o 1 o o O o o o 1 O O o O o 1  o o o  o o 1 o o o 1 O o o O O o o o O 0 o o O o o O o o O o O o o o o O o o  o o o o 1 0 0 0   0 O o o 1 O o O o O o 1 O   o 0   O O o O o o o 1 o o  o o o o o o o 1 o o o 1 o o o o o 1 O o o O o o 1 o o O O o o o o 1 o o o 1  o 1 o o o O o o o 1 1 I O O O o o O O o O O o o o o 1 o o O o O o o o o o O 0 1 o o o o o O o o o o o O   o 0 O 0 o O O O o O o o o o o O O O O o O  o o o o o 0 o o 0 0 0 0 0 O o o o o O o 1 O O o O o 1 O o o o O o 1  
O O o 1 o o O o 1 1 O O o 1 O o o O O o o O O o 1 1 O o o O o o O o O O o o  
O O O O O O   O O O o O O O O o O O o 1   o O O o 1 1 O O O o 1 I O O O o 
1 1 o 1 1 o 1 1 o 1 o o 1 1 o O O o 1 1 o o 1 o 1   o o I o 1 1 o o 1 O o 1  1 o o 1 o o 1 o o 1 o I o 1 o o 1 o o 1 0 O O o 1 o O O o 1 1 o o o o 1 1  O o 1 1 o O O o 1 1 O O O   o o O O o 1 O o O O O O O O O O o 1   1 1 I o 1  
O 0   o o o 0 0 0 O O 0 O O o O O o o 1 o o O o O o o 0 O o o 1 o O O o o 1  
O o o O 0 o O O o 1 o 1 1 o 1 1 1 O o 1 O O o O o o O O O O o o o 1 1 1 1 1 0 1 O O 0 0 0 O o O O O 0 O 0 o O O o O o O O O O o O O O o 1 O O O O O O O o O  o o o O o o 1 o o o 1 O o 1 1 1 o o O O o 0 0 o O o o o 1 o 1 o O o O O O O  o o o o O o   o 1 O o 1 O O O o 1 1 o o I o 1 o 1 1 1 o o I o 1 O o O O O O  O 0 o O o o o 1 o 1 O o 1 O o 0 o 1 O O o o o O O O o o I o o   O o O O O O  O 0 o o o o o 0 o 1 o o 1 O 0 o O o 1 o O o O O O O o o O o 1 1 1 1 1 O O 0    O o o o o o o 1 1 1 1 1 O O o O O o 1 1 1 o 1 o I o o O o O o 1 o 1 o 1 O  o O O o 0 0 o o 1 o 1 o I O o O o o O o 1 O o O o O o O O o 1 O o o 1 o  o 0 o o O O o o 1 o 1 O O o 1 O O o O O o O o o O O O o o O o 1 O O   1  1 O o o 1 O O o I O o 1 1 o 1 1 0 o 1 1 1 o 1 1 o 1 1 o 1 O O o O o 1 0 O o  o o 1 o 1 o 1 o I 0 o o 1 o O o 1 O O O O O o o O O O o O o o O o O o 1 O O 0 1 o o o 1 O o I 0 o 1 0 0 o 1 o O o 1 O o o O o o 1 o O O O O o O O o  O O o 1 1 1 o o o O o 1 1 1 1 1 O o 0 o o 1 1 1 O O O o   0 o 1 1 1 1 I o 1 0 O O O o 1 0 1 o 1 o 0 O o o I o 1 O 0 0 O o 1 O O o 1 O O 0 o o o 1 O O O O O O O O O o  1  o o o 1 0 o o o 1 1 1 O o o o 1 o o o o o 1 O o o 1 o O   O O O O O O o 1 O O o O o   o 1 o   o I   O o 1 O o o O o 1 O O O O o 1 1 o 1 I O O 0 0 1 0 o o O o 1 0 0 o 1 o o o 1 o O o 1 O o o o o 1 o O O O o 1 1 O O O O O o O 
1 O o o O o 1 1 o 1 1 o o o 1 1 o 1 1 O O o o o 1 1 O o 1 1 1
'''
# By selecting the text in Chrome's PDF viewer
data2 = '''
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0
0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0
0 1 0 0 0 0 0 0 0 1 1 1 Q 0 0 0 0 0 0 o.o 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 ~ 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 1 0 0
0 0 0 1 0 0 0 0 1 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1 0
1 1 0 1 1 0 1 1 0 1 0 0 1 1 0 0 0 0 1 1 0 0 1 0 1 1 0 0 1 0 1 1 0 0 1 0 0 1 0 0
1 0 0 1 0 0 1 0 0 1 0 1 0 1 0 0 1 0 0 1 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1 0 0
0 0 1 1 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 1 0 1 1 0 1 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 1 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 1 0 0 1 0 0 0 0 1 1 0 0 1 0 1 0 1 1 1 0 0 1 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 1 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 1 1 1 0 1 0 1 0 0 0 0 0 0 1 0 1 0 1 0 0 0
0 0 0 0 0 0 0 0 1 0 1 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 1 0
0 0 0 0 0 0 0 0 1 0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0
1 0 0 0 1 0 0 0 1 0 0 1 1 0 1 1 0 0 1 1 1 0 1 1 0 1 1 0 1 0 0 0 0 0 1 0 0 0 1 0
0 0 1 0 1 0 1 0 1 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1
0 0 0 1 0 0 1 0 0 1 0 0 0 1 0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1
0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 1 l l 0 0 0 0 0 0 0 l l l l l 0 1 0 0 0 0 0 l 0 1
0 1 0 0 0 0 0 1 0 1 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 1 0 0 0 0 1 1 1 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 1 0 0 0 l 0 0 0 l 0 0 0 1 0 0 0 0 0 l 0 0 0 0 0 1 l 0 0 0 1 1 0 0 0 0 l
0 0 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 1 1 0 1 1 0 0 0 1 1 0 1 1 0 0 0 0 0 1 1 0 0 1 1 1 
'''[1:-1]

def RecoverData(s):
    '''The set of non-whitespace characters in the screen-scraped message
    is '.01Qlo~'.  I would make the following substitutions:
                    Row Col
        .   ' '      6   21  Length of line indicates it's spurious
        0   None    
        1   None    
        Q   '0'      6   13
        l   '1'     various  Easy to see why confused with 1
        o   '0'      6   20
        ~   '0'      8   13  Gotten by counting in figure 2  
    It's supposed to be 41 columns and 31 rows.  However, return the string
    of 1271 characters.
    '''
    if 0:   # Show characters in raw data
        print(''.join(sorted(set(s))))
    if 0:   # Print with ruler and numbered rows
        print(dedent('''
        1-based line number starts each line
                    1         2         3         4    
           ····+····|····+····|····+····|····+····|····+
        '''))
    
        for i, line in enumerate(data2.split("\n")):
            print(f"{i+1:2d} {line.strip().replace(' ', '')}")
    if 1:   # Fix the data
        # Remove spaces and newlines
        s = data2.replace(" ", "").replace("\n", "")
        # Remove the '.'
        s = s.replace(".", "")
        Assert(len(s) == 1271)
        # Other fixes
        s = s.replace("l", "1")
        s = s.replace("Q", "0")
        s = s.replace("o", "0")
        s = s.replace("~", "0")
        # Should be only 0 and 1
        Assert(set(s) == set("01"))
    return s
def PrintRows(s, nrows, one="1", zero="0", double=False):
    ncols = 1271//nrows
    # Print a header to get column number
    if double:
        print("  ", end="")
        for i in range(1, 5):
            print(f"{i:20d}", end="")
        print()
        print("   ", end="")
        for i in range(ncols):
            print(f"{(i + 1) % 10} ", end="")
    else:
        print("  ", end="")
        for i in range(1, 5):
            print(f"{i:10d}", end="")
        print()
        print("   ", end="")
        for i in range(ncols):
            print(f"{(i + 1) % 10}", end="")
    # Print the data rows
    for i, c in enumerate(s):
        if i % ncols == 0:
            print(f"\n{i//ncols + 1:2d} ", end="")
        char = one + one if double else one
        if c == "0":
            char = zero + zero if double else zero
        print(char, end="")
    print()
    
s = RecoverData(data2)
if 1:
    # Print 31 rows
    one = "█"
    one = "●"
    zero = "‥"
    zero = " "
    PrintRows(s, nrows=31, one=one, zero=zero)
else:
    # Print 41 rows
    PrintRows(s, nrows=41, one="█", zero="‥")
