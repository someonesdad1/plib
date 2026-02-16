'''
Utilities to deal with color

'''
if 1:   # Header
    if 1:  # Standard imports
        from collections import defaultdict, deque
        from pprint import pprint as pp
        import string
    if 1:  # Custom imports
        from columnize import Columnize
    if 1:  # Global variables
        pass
if 1:   # Core functionality
    def NormalizeColorName(s):
        '''Return the string s normalized to my naming convention, which is lowercase
        snake-case with one underscore between words.
        '''
        if not s.strip():
            raise ValueError("Empty or whitespace-only string not allowed")
        if 1:   # Find a sentinel character to put at the end of the sequence
            sentinels = deque("🟦🟫🟪🟩🟨🟧🟥")
            sentinel = None
            while sentinels:
                c = sentinels.popleft()
                if c not in s:
                    sentinel = c
                    break
            if sentinel is None:
                raise ValueError("Couldn't find sentinel character")
        if 1:   # Process the string
            u = deque(s + sentinel)
            uc = set(string.ascii_uppercase)
            while u[0] != sentinel:
                c = u.popleft()
                u.append(" " + c.lower() if c in uc else c)
            assert u[0] == sentinel
            c = u.popleft()     # Remove sentinel
        # Final processing:  split, reassemble, substitute underscores
        v = ' '.join(''.join(u).split()).replace(" ", "_")
        return v
    def GetColornameDict(color_data):
        '''color_data should be a sequence with entries like
        (9, "cloudy blue", Color(172, 194, 217), 'cynblu')
        '''
        di = defaultdict(list)
        w = 0
        lst = []
        for item in color_data:
            attr, name, clr, hue = item
            name = NormalizeColorName(name)
            w = max(w, len(name))
            di[hue].append([name, clr])
            lst.append(f"'{name:{w}s}': '{clr.xrgb} {clr.xhsv} {clr.xhls}'")

        for i in lst:
            print(i)
        exit()

        o, names = [], []
        for hue in di:
            #t.print(f"{t('whtl', 'redl')}{hue}")
            for name, clr in di[hue]:
                s = NormalizeColorName(name)
                names.append((len(s), s))
                o.append(f"{t(clr)}{s}{t.n}")
        for i in Columnize(o, indent=" "*4):
            print(i)
        big = sorted(names)[-1][1]
        print(f"{len(o)} color names, maximum length = {w} ({big})")
