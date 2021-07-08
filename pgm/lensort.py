'''
Sort by line length.  Take input from stdin if there's no parameter
on the command line.
'''

import sys

if __name__ == "__main__": 
    lines, decorate = [], lambda x: (len(x), x)
    if len(sys.argv) == 1:
        for i in sys.stdin:
            lines.append(decorate(i))
    else:
        for file in sys.argv[1:]:
            for i in open(file):
                lines.append(decorate(i))
    for line in sorted(lines):
        print(line[1], end="")
