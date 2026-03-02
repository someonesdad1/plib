_pgminfo = '''
<oo desc ∞
    Look for python files in /pylib that don't contain double letters/punctuation
oo>
<oo cr ∞ Copyright © 2026 Don Peterson oo>
<oo license ∞
    Licensed under the Open Software License version 3.0.
    See http://opensource.org/licenses/OSL-3.0.
oo>
<oo cat ∞ util oo>
<oo test ∞ none oo>
<oo todo ∞ oo>
'''
if 1:  # Header
    if 1:   # Standard imports
        from pathlib import Path as P
    if 1:   # Custom imports
        from columnize import Columnize
        import trm
        t = trm.Trm()
if 1:   # Core functionality
    def GetFiles():
        'Recursivly find all python files at and below /plib'
        files = []
        for file in P("/plib").glob("**/*.py"):
            files.append(file)
        return files
if __name__ == "__main__":
    files = GetFiles()
    notfound = []
    ltr = "abcdefghijklmnopqrstuvwxyz!#$%&()*+,-./:;<=>?@[]^_`{|}~"
    ltr = list(sorted(set(ltr + ltr.upper())))
    letters2 = [i + j for i, j in zip(ltr, ltr)]
    letters3 = [i + j + k for i, j, k in zip(ltr, ltr, ltr)]
    print("Letter combinations searched for:")
    for i in Columnize(letters2):
        print(i)
    for pair in letters2 + letters3:
        found = False
        for i, file in enumerate(GetFiles()):
            s = open(file).read()
            if pair in s:
                found = True
                break
        if not found:
            notfound.append(pair)
    print(f"{t.ornl}\n2 & 3 letter combinations in none of the files:{t.grn}")
    for i in Columnize(notfound):
        print(i)
    t.print(end="")
