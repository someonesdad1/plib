'''
xx Move stuff to get.py

Provides functions to tokenize files and streams:

GetTokens
    Use on a group of files or streams; keywords let you filter
    lines and tokens and control splitting into tokens.
GetWords
    Similar to GetTokens but is intended to parse words in a file or
    string.
Tokenize
    Will tokenize a string, file, or stream and turn it into a list of
    these tokens.  Intended for tokenizing text.
Asciify
    Will "ASCIIfy" a string, which means to turn letters like 'Å' to the
    ASCII 'A' and punctuation like '—' (em dash) to an ASCII '-'
    (hyphen).

Note:  You may want to read more about tokenizing at
http://www.nltk.org/book/ch03.html (see section 3.7).
'''

# Copyright (C) 2018 Don Peterson
# Contact:  gmail.com@someonesdad1
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

import re
import string
import sys
from asciify import Asciify
from pdb import set_trace as xx

def GetTokens(*files, **kw):
    '''Generator that returns a sequence of tokens gotten from the
    indicated input source(s).  files can be either file names or stream
    objects.
    
    Keywords [default value]:
        convert     Univariate function(s) to apply to each token.  [identity]
        sep         Split each line on this string.  [" "]
        fltr        Univariate function(s) to filter each input line.
                    [identity]
 
    The filtering functions convert and fltr can be a sequence of functions to
    apply if the toolz module is available.
    '''
    if not files:
        return
    remove_nl = lambda line: line[:-1] if line and line[-1] == "\n" else line
    identity = lambda x: x
    # If the toolz module is available, the compose object (in functoolz)
    # allows a sequence of univariate functions to be used to transform
    # lines and tokens: if the sequence of functions is [f, g, h], then the
    # transformed line or token object will be f(g(h(object))).  If you
    # wish to get toolz (a nice functional programming module), use 'pip
    # install toolz'.
    try:
        from toolz import compose
    except ImportError:
        compose = identity
    # Keyword options
    convert = compose(kw.setdefault("convert", identity))
    sep     = kw.setdefault("sep", " ")
    fltr    = compose(kw.setdefault("fltr", identity))
    # Process each file/stream
    for file in files:
        if hasattr(file, "write"):      # It's a stream
            line = file.readline()
            while line:
                line = fltr(line)
                tokens = remove_nl(line).split(sep)
                for token in tokens:
                    yield convert(token)
                line = file.readline()
        else:                           # It's a file
            for line in open(file):
                line = fltr(line)
                tokens = remove_nl(line).split(sep)
                for token in tokens:
                    yield convert(token)

def GetWords(file, comment_char="#", case=None, existing_set=None,
             sepchar=" ", isstring=False):
    '''Tokenize the file, ignoring comments.  A set of words is
    returned; if existing_set is not None, then the set of words is 
    added to it.

    If isstring is True, then file is a string to be read and parsed
    for words.  Otherwise, it's a file name to open or a stream to be
    read from.
 
    If comment_char is not None, then it's a string that denotes the
    beginning of a comment line after leading whitespace is stripped;
    comment lines are ignored.
 
    If case is None, the words are left alone.  If it's
    'upper', they are converted to uppercase; if it's 'lower', they're
    converted to lower case.
    '''
    strings = []
    if isstring:
        lines = file.split("\n")
    else:
        try:
            lines = file.readlines()
        except Exception:
            lines = open(file).readlines()
    for l in lines:
        ln = l.strip() 
        if case == "upper":
            ln = ln.upper() 
        elif case == "lower":
            ln = ln.lower() 
        elif case is not None:
            m = "case must be 'upper', 'lower', or None"
            raise ValueError(m)
        if not ln or (comment_char and ln.startswith(comment_char)):
            continue
        strings.append(ln)
    words = set((sepchar.join(strings)).split(sepchar))
    words.discard("")
    if existing_set is not None:
        existing_set.update(words)
        return
    return words

def IsAbbreviation(w):
    '''Returns True if w is an abbreviation.
    '''
    if not hasattr(IsAbbreviation, "abbrev"):
        IsAbbreviation.abbrev = set('''
        a.c. a.d. a.k.a. abr. abstr. acad. acc. acct. addr. adj. adm.
        adv. advb. anon. app. appl. assoc. attrib. auth. ave. b. b.c.
        b.c.e. b.o. b.t.u. betw. bk. bur. c. c.e. c.o.d. c.p.u. cent.
        cert. cf. ch. chas. co. colloq. conf. conv. corresp. ct. d.a.
        d.c. d.o.a. dat. def. dep. dept. descr. e. e.s.p. ed. edw.
        emph. eng. equip. esp. etym. etymol. euphem. exc. f. fr. fut.
        geo. gov. govt. h.p. handbk. hist. i.d. i.u.d. illustr. inc.
        intro. jr. jrnl. jurisd. jurispr. lat. lbf. lett. ltd. ln. m.
        masc. mass. meas. med. mil. misc. mt. n. n.b. n.e. n.s.w. n.w.
        n.y. n.z. nom. nucl. o.d. o.e.d. o.k. obj. orig. oz. p. p.a.
        p.e. p.m. p.o. ph.d. phil. phys. pl. publ. q. q.v. r.a.f.
        r.c. r.n. ref. rep. rev. s. s.e. st. s.t.p. s.u.v. s.w. sat.
        sci. soc. sp. sr. st. subj. subord. t.b. techn. technol. tr.
        trans. u.k. u.s. u.s.s.r. univ. unkn. unoffic. usu. v. v.p.
        var. vet. vic. viz. vol. vols. vulg. w. w.c. w.m.d. wk. yr.
        yrs.
 
        u.s.a. u.s.n. u.s.a.f. u.s.c.g.
        g.i. pvt. cpl. corp. sgt. lt. capt. maj. cmdr. col. gen.
        e.g. et.al. etc. q.e.d. i.e. ibid. ib.
        a.m. p.m.
        mr. mrs. ms. mss. messrs. mssrs. dr. prof.
        jan. feb. mar. apr. jun. jul. aug. sep. oct. nov. dec.
        mon. tue. wed. thu. fri. 
        '''.split())
        if 1:
            # The following abbreviations can also be words that end
            # a sentence; you can exclude them if you wish.
            IsAbbreviation.abbrev.update(set('''
                add. admin. ann. bull. conn. dim. fig. math. mod.
                no. pa. pop. sept. sing. west. wed. sat. sun.
            '''.split()))
    return w.strip().lower() in IsAbbreviation.abbrev

def Tokenize(source, remove_punct=False, no_possessives=False,
             asciify=False):
    """Returns a list of tokens from from source, which can be a
    stream, file name to open, or a string, utilized in that order.  
    This function is intended to be used with text to return the 
    words in a source.  Here, 'words' means both textual words
    and punctuation characters.  An abbreviation like 'Mr.' will 
    stay an abbreviation, unlike 'rabbit,' which will be separated from
    the comma.

    The behavior is similar to the nltk.tokenize.word_tokenize function,
    but Tokenize doesn't return any characters that weren't in the
    original text.
 
    The text is split on whitespace and punctuation characters are
    considered separate tokens.  Set remove_punct to True to have
    punctuation removed, in which case the tokens will be words.
 
    Example:  If s = '"Hello", said the rabbit\'s sister.', then
    Tokenize(s) will return the list
 
        ['"', 'Hello', '"', ',', 'said', 'the', "rabbit's", 
         'sister', '.']
 
    The apostrophe is left in if it's internal to a word.  If you don't
    want this behavior, set no_possessives to true.  A number of Unicode
    characters are considered equivalent to the apostrophe and they are
    removed too (see ProcessWord).
    
    If remove_punct is True, then the function returns the list
 
        ['Hello', 'said', 'the', "rabbit's", 'sister']
 
    If both remove_punct and no_possessives are True, then the function
    returns the list
 
        ['Hello', 'said', 'the', "rabbits", 'sister']
 
    If asciify is True, then a number of Unicode punctuation characters
    are changed to their rough ASCII equivalents.  For example, the left
    double quotation mark “ (codepoint U+201c) is changed to the ASCII
    character " (codepoint U+0022).
    """
    if isinstance(source, str):
        try:
            s = open(source).read()
        except FileNotFoundError:
            s = source
    else:
        s = source.read()   # It must be a stream
    tokens = []
    for word in s.split():
        tokens.extend(ProcessWord(word, no_possessives=no_possessives, 
                                  asciify=asciify))
    if remove_punct:
        tokens = [i for i in tokens if not IsPunctuation(i)]
    return tokens

def IsPunctuation(c):
    if not hasattr(IsPunctuation, "punc"):
        # Get punctuation characters
        others = ''.join([chr(i) for i in 
            (0x00ab, 0x00bb, 0x2012, 0x2013, 0x2014, 0x2015, 0x2018,
             0x2019, 0x201a, 0x201b, 0x201c, 0x201d, 0x201e, 0x201f,
             0x2039, 0x203a, 0x2053, 0x229d, 0x2448, 0x2449, 0x2504,
             0x2505, 0x2508, 0x2509, 0x254c, 0x254d, 0x275b, 0x275c,
             0x275d, 0x275e, 0x275f, 0x2760, 0x276e, 0x276f, 0x2e3a,
             0x2e3b, 0x301c, 0x301d, 0x301e, 0x301f, 0x3030, 0xff02)])
        IsPunctuation.punc = set(string.punctuation + others)
    for i in c:
        if i not in IsPunctuation.punc:
            return False
    return True

IsPunctuation(";")
print(''.join(IsPunctuation.punc))
exit()

def ProcessWord(w, no_possessives=False, asciify=False):
    '''The word w may have punctuation preceding or following it.
    The punctuation characters need to be separated from the word's
    characters and the group need to be returned as a separate list.
 
    Example:  If w is '[(the', then ['[', '(', 'the'] will be returned.
 
    If no_possessives is true, apostrophes internal to the word are
    removed.
 
    If asciify is True, a number of Unicode punctuation characters are 
    converted to their rough ASCII equivalents.  For example, the left
    double quotation mark “ (codepoint U+201c) is changed to the ASCII
    character " (codepoint U+0022).
    '''
    if not hasattr(ProcessWord, "trans"):
        ProcessWord.trans = {}
        for i in (0x0027, 0x2018, 0x1019, 0x201a, 0x201b,
                  0x275b, 0x275c, 0x275f):
            ProcessWord.trans[i] = None
    def RemovePunct(s, w):
        while w and IsPunctuation(w[0]):
            s.append(w[0])
            w = w[1:]
        return w
    if IsAbbreviation(w) or len(w) == 1:
        return [w]
    s = []
    # Remove front punctuation
    w = RemovePunct(s, w)
    # Remove back punctuation
    w, t = ''.join(reversed(w)), []
    w = RemovePunct(t, w)
    w = ''.join(reversed(w))
    if w:
        if no_possessives:
            w = w.translate(ProcessWord.trans)
        s.append(w)
    if t:
        s.extend(list(reversed(t)))     # Add trailing punctuation
    if asciify:
        for i, item in enumerate(s):
            s[i] = Asciify(item)
    return s

def ReadWordlist(file, case=None):
    '''file can be a stream, filename, or a string to parse.  This
    function is aimed at reading wordlists I use on my computer.  These
    will have comment lines beginning with '#' after stripping
    whitespace.  Then all words are separated by whitespace and can be
    gotten at once on the whole file's string with strip().

    If case is None, do nothing with the words.  If it is "lower",
    change them to lower case; upper with "upper".  If you're interested
    in turning the list into an ASCII file, look at the Asciify function
    in the asciify module.
    '''
    try:
        s = file.read()
    except Exception:
        try:
            s = open(file).read()
        except FileNotFound:
            s = file
    lines = []
    for line in s.split("\n"):
        line = line.strip()
        if not line or line[0] == "#":
            continue
        lines.append(line)
    s = ' '.join(lines)
    if case == "upper":
        s = s.upper()
    elif case == "lower":
        s = s.lower()
    return set(s.split())

if __name__ == "__main__": 
    # Tokenize the files on the command line and print them one per line
    if len(sys.argv) == 1:
        # Process stdin
        tokens = Tokenize(sys.stdin, asciify=True)
    else:
        tokens = []
        for file in sys.argv[1:]:
            t = Tokenize(file, asciify=True)
            tokens.extend(t)
    for token in tokens:
        print(token)
            
