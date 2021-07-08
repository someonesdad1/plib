'''

This example code requires the following one-line text files:
    t0.txt:  it is what it is
    t1.txt:  what is it
    t2.txt:  it is a banana

The output shows how an inverted index can be built.  The second half of
the demo shows how a full inverted index can be built that lets you search
for a phrase.

This came from http://rosettacode.org/wiki/Inverted_index#Python
'''
 
import os
from pprint import pprint as pp
from glob import glob
from collections import Counter
from pdb import set_trace as xx 

try: reduce
except: from functools import reduce
try:    raw_input
except: raw_input = input

def parsetexts(fileglob='t*.txt'):
    '''Returns (texts, words) where texts is a dictionary with filename
    keys and lists of words in the file.  words is a list of all the words
    in the files.
    '''
    texts, words = {}, set()
    for txtfile in glob(fileglob):
        with open(txtfile, 'r') as f:
            txt = f.read().split()
            words |= set(txt)
            texts[txtfile.split('\\')[-1]] = txt
    return texts, words

def termsearch(terms): # Searches simple inverted index

    '''reduce(func, iterable, [initializer]) applies a function of two
    arguments cumulatively to items of the sequence.  If initializer is
    present, it precedes the items of the sequence and serves as a default
    when the sequence is empty.

    '''
    return reduce(set.intersection,
                  (invindex[term] for term in terms),
                  set(texts.keys()))

def fulltermsearch(terms): # Searches full inverted index
    if not set(terms).issubset(words):
        return set()
    return reduce(set.intersection,
                  (set(x[0] for x in txtindx)
                   for term, txtindx in finvindex.items()
                   if term in terms),
                  set(texts.keys()) )

def phrasesearch(phrase):
    wordsinphrase = phrase.strip().strip('"').split()
    if not set(wordsinphrase).issubset(words):
        return set()
    #firstword, *otherwords = wordsinphrase # Only Python 3
    firstword, otherwords = wordsinphrase[0], wordsinphrase[1:]
    found = []
    for txt in termsearch(wordsinphrase):
        # Possible text files
        for firstindx in (indx for t,indx in finvindex[firstword]
                          if t == txt):
            # Over all positions of the first word of the phrase in this txt
            if all( (txt, firstindx+1 + otherindx) in finvindex[otherword]
                    for otherindx, otherword in enumerate(otherwords) ):
                found.append(txt)
    return found

if __name__ == "__main__": 
    # The example is put into a try block so the created text files are erased
    # after running.
    try:
        text_files = {
            "t0.txt": "it is what it is\n",
            "t1.txt": "what is it\n",
            "t2.txt": "it is a banana\n",
        }
        # Create the text files
        for filename, line in text_files.items():
            open(filename, "w").write(line)

        # Inverted index example
        texts, words = parsetexts()
        print('Texts')
        pp(texts)
        print('\nWords')
        pp(sorted(words))
        invindex = {word:set(txt for txt, wrds in texts.items() if word in wrds)
                    for word in words}
        print('\nInverted Index')
        pp({k:sorted(v) for k,v in invindex.items()})
        terms = ["what", "is", "it"]
        print('\nTerm Search for: ' + repr(terms))
        pp(sorted(termsearch(terms)))
        print("-"*70)

        # Full inverted index example
        finvindex = {word:set((txt, wrdindx)
                            for txt, wrds in texts.items()
                            for wrdindx in (i for i,w in enumerate(wrds) if word==w)
                            if word in wrds)
                    for word in words}
        print('\nFull Inverted Index')
        pp({k:sorted(v) for k,v in finvindex.items()})

        print('\nTerm Search on full inverted index for: ' + repr(terms))
        pp(sorted(fulltermsearch(terms)))

        phrase = '"what is it"'
        print('\nPhrase Search for: ' + phrase)
        print(phrasesearch(phrase))

        # Show multiple match capability
        phrase = '"it is"'
        print('\nPhrase Search for: ' + phrase)
        ans = phrasesearch(phrase)
        print(ans)
        ans = Counter(ans)
        print('  The phrase is found most commonly in text: ' + repr(ans.most_common(1)[0][0]))
    finally:
        for filename in text_files:
            if os.path.exists(filename):
                os.remove(filename)
