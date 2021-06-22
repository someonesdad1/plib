'''
TODO

* Need two spaces after '.' and ':'.

Comments:  the algorithm works, but I think I'd rather see random
location of the extra spaces rather than starting at the beginning of
the line.  Justify PNP to 79 spaces and you'll see why.

'''
from pdb import set_trace as xx 

def Justify1(words, maxWidth):
    # From https://medium.com/@dimko1/text-justification-63f4cda29375
    res, curr, num_of_letters = [], [], 0
    for w in words:
        if num_of_letters + len(w) + len(curr) > maxWidth:
            num_of_spaces = maxWidth - num_of_letters
            words_amout = len(curr) - 1 or 1
            for i in range(num_of_spaces):
                curr[i % words_amout] += ' '
            res.append(''.join(curr))
            curr, num_of_letters = [], 0
        curr += [w]
        num_of_letters += len(w)
    return res + [' '.join(curr).ljust(maxWidth)]

def Justify(words, L):
    # From https://medium.com/@dimko1/text-justification-63f4cda29375
    out, line, num_of_letters = [], [], 0
    for word in words:
        if num_of_letters + len(word) + len(line) > L:
            num_of_spaces = L - num_of_letters
            words_amount = len(line) - 1 
            for i in range(num_of_spaces):
                line[i % words_amount] += ' '
            out.append(''.join(line))
            #print(f"{word}:  {line}")
            line, num_of_letters = [], 0
        line.append(word)
        num_of_letters += len(word)
    out.append(' '.join(line).ljust(L))
    return out

s = open("pnp").read()
for line in Justify(s.split(), 79):
    print(line)
