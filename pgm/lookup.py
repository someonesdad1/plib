'''
TODO:
    * -v doesn't limit to verbs and seems to take a long time:
        'dict -cv black'.  'dict -cn black' doesn't show just nouns.
    * 'dict -a black' fails.
    * Figure out how to add in the information from
      words_syllables.py.

Script to look up words in various dictionaries.  For a demo of
capabilities, try

    python lookup.py "heav"
        Find all words with the string "heav" in them
    python lookup.py -dc "^mother$|^motherless$|^motherly$"
        Show all words/definitions/synonyms/type for the indicated
        regexps.  Note this produces colored output on a DOS/cygwin
        shell.  You can make it colored on e.g. a UNIX box if you're
        willing to write suitable escape-code stuff analogous to
        what's in the color module.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Lookup words in dictionaries
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import re
    import os
    import getopt
    import subprocess
    import string
    from textwrap import TextWrapper
    from pprint import pprint as pp
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from get import GetTokens
    # The following is a non-standard python module that can be gotten from
    # https://someonesdad1.github.io/hobbyutil/project_list.html
    import color as color
if 1:   # Global variables
    dbg = False   # Turn on for debug printing, which helps to debug the code
    # This script uses a grep-like tool to perform the searches.  The grep
    # variable must point to a grep executable.  Use the grep_options to
    # customize behavior.
    grep = "/bin/egrep"
    grep_options = [
        "-i",
        "--color=auto",   # GNU grep option
    ]
    # You need to make the following variables point to the needed WordNet
    # ASCII database files.  See the words.pdf file for details.
    dir, W = "/pylib/", "types_of_words/WordNet/"
    Join = os.path.join
    wordnet_files = {
        "index": Join(dir, W, "index.sense"),
        "adj": Join(dir, W, "data.adj"),
        "adv": Join(dir, W, "data.adv"),
        "noun": Join(dir, W, "data.noun"),
        "verb": Join(dir, W, "data.verb"),
        "dict": Join(dir, "pgm", "words.wordnet"),
    }
    # Make the following dictionary point to the dictionary files you wish
    # to use.
    dir = "/pylib/pgm"  # Directory where dictionaries are
    dictionary_files = {
        0: Join(dir, "words.ogden"),          # Ogden's 851 word list
        1: Join(dir, "words.2of12"),          # 42 kwords
        2: Join(dir, "words"),                # 93 kwords
        3: Join(dir, "words.2005.wayne"),     # Big dictionary 274 kwords
        4: Join(dir, "words.x.universal"),    # Very large dictionary 511 kwords
        # Tenhundred from
        # http://splasho.com/upgoer5/phpspellcheck/dictionaries/1000.dicin
    #5: Join(dir, "words.tenhundred"),     # 1000 words
        "-w": wordnet_files["dict"],          # WordNet words, 155 kwords
    }
    del dir, Join, W
    # The following dictionary contains the open streams to the WordNet
    # data files.
    streams = {
        "a": open(wordnet_files["adj"]),
        "r": open(wordnet_files["adv"]),
        "n": open(wordnet_files["noun"]),
        "v": open(wordnet_files["verb"]),
    }
    streams["s"] = streams["a"]
    # Get the number of screen columns
    columns = int(os.environ["COLUMNS"]) - 1 if "COLUMNS" in os.environ else 79
    # Color-related stuff.  Note:  the color module is a python module
    # that uses escape sequences to set colors.  I use it under a modern bash
    # based on mintty under cygwin and bash under Linux.
    black = color.black
    blue = color.blue
    green = color.green
    cyan = color.cyan
    red = color.red
    magenta = color.magenta
    brown = color.brown
    white = color.white
    gray = color.gray
    lblue = color.lblue
    lgreen = color.lgreen
    lcyan = color.lcyan
    lred = color.lred
    lmagenta = color.lmagenta
    yellow = color.yellow
    lwhite = color.lwhite
    fg = color.fg
    normal = color.normal
    # WordNet uses letters to identify the types of words; we'll use more
    # conventional abbreviations.  This also allows us to set the color
    # for these types of words.
    abbr = {
        "a": ("adj.", yellow),
        "s": ("adj.", yellow),
        "n": ("n.", lwhite),
        "v": ("v.", lgreen),
        "r": ("adv.", lmagenta),
    }
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def ParseIndexLine(line):
    '''A typical index line is:
        airheaded%5:00:00:frivolous:00 02120828 1 0
    '''
    f = line.split()
    key, offset = f[0], int(f[1])
    f = key.split(":")
    p = f[0].split("%")
    head_word = f[3]
    word, sense = p[0], int(p[1])
    # Translate sense number to a letter
    letter = " nvars"[sense]
    # Note that head_word is only non-empty if letter is "s"
    return word, letter, head_word, offset
def ParseDataLine(line):
    '''The five typical lines' contents (shown wrapped):

    adjective:

        00001740 00 a 01 able 0 005 = 05200169 n 0000 = 05616246 n
        0000 + 05616246 n 0101 + 05200169 n 0101 ! 00002098 a 0101 |
        (usually followed by `to') having the necessary means or skill
        or know-how or authority to do something; "able to swim"; "she
        was able to program her computer"; "we were at last able to
        buy a car"; "able to get a grant for the project"

    adjective satellite:

        02120828 00 s 08 airheaded 0 dizzy 0 empty-headed 0
        featherbrained 0 giddy 0 light-headed 0 lightheaded 0 silly 0
        004 & 02120458 a 0000 + 04648440 n 0802 + 04894444 n 0701 +
        04648440 n 0501 | lacking seriousness; given to frivolity; "a
        dizzy blonde"; "light-headed teenagers"; "silly giggles"

    adverb:

        00002436 02 r 03 horseback 0 ahorse 0 ahorseback 0 000 | on
        the back of a horse; "he rode horseback to town"; "managed to
        escape ahorse"; "policeman patrolled the streets ahorseback"

    noun:

        00001740 03 n 01 entity 0 003 ~ 00001930 n 0000 ~ 00002137 n
        0000 ~ 04424418 n 0000 | that which is perceived or known or
        inferred to have its own distinct existence (living or
        nonliving)

    verb:

        00001740 29 v 04 breathe 0 take_a_breath 0 respire 0 suspire 3
        021 * 00005041 v 0000 * 00004227 v 0000 + 03110322 a 0301 +
        00831191 n 0303 + 04080833 n 0301 + 04250850 n 0105 + 00831191
        n 0101 ^ 00004227 v 0103 ^ 00005041 v 0103 $ 00002325 v 0000 $
        00002573 v 0000 ~ 00002573 v 0000 ~ 00002724 v 0000 ~ 00002942
        v 0000 ~ 00003826 v 0000 ~ 00004032 v 0000 ~ 00004227 v 0000 ~
        00005041 v 0000 ~ 00006697 v 0000 ~ 00007328 v 0000 ~ 00017031
        v 0000 02 + 02 00 + 08 00 | draw air into, and expel out of,
        the lungs; "I can breathe better when the air is clean"; "The
        patient is respiring"

    Note the definition ("gloss") is after the vertical bar, so that's
    parsed out first.  Then the remainder is parsed; the description
    is in the wndb.5.pdf file.  Note we only keep the word type letter
    and the synonyms.
    '''
    head, definition = line.split("|")
    definition = definition.strip()
    if definition[0] in string.ascii_lowercase:
        definition = definition[0].upper() + definition[1:]
    f = head.split()
    letter, syn_cnt = f[2], int("0x" + f[3], 16)
    synonyms = f[4:4 + 2*syn_cnt:2]
    word = synonyms[0]
    synonyms = synonyms[1:] if len(synonyms) > 1 else []
    return word, letter, synonyms, definition
def PrintWord(word, letter, head_word, offset, d):
    '''word is the word as found in the index.sense file but
    displayable (the underscores are removed).  letter is one of
    "nvars".  head_word is not empty if letter is "s".  offset is an
    integer to read the relevant line from the stream after performing
    a seek to that offset.
    '''
    stream = streams[letter]
    stream.seek(offset)
    line = stream.readline()
    main_word, letter, synonyms, definition = ParseDataLine(line)
    key = word + "%" + letter
    indent = " "*2
    w = TextWrapper()
    w.fix_sentence_endings = True
    w.initial_indent = indent
    w.subsequent_indent = indent
    Wrap = w.fill
    if d["-d"] or d["-" + letter]:
        if d["-c"] and ("_" in word or "-" in word or " " in word):
            return
        fg(lred)
        print(word)
        normal()
        fg(abbr[letter][1])
        print(indent, abbr[letter][0], end="", sep="")
        if synonyms:
            t = Wrap(', '.join(synonyms))
            print(t)
        else:
            print()
        w.subsequent_indent = indent*3 + " "
        t = Wrap(definition)
        print(indent*2, t)
        normal()
def PrintWordNet(word, d):
    '''word is a word in the WordNet index, so find its line(s) in the
    index.sense file.  Then dereference each synset reference and
    send the data to stdout.
    '''
    Word = word.strip().replace("_", " ")
    # Note:  it's important to use double quotes around the regexp;
    # otherwise the command will hang when word contains an
    # apostrophe.
    cmd = (grep + ' "^' + word.strip() + '%" ' +
           wordnet_files["index"].replace("\\", "/"))
    p = subprocess.PIPE
    s = subprocess.Popen(cmd, bufsize=0, stdout=p, stderr=p,
                         universal_newlines=True, shell=True)
    # Get results of grep
    lines = s.stdout.readlines()
    if dbg:
        print("xx2 cmd =", cmd)
        print("xx3 lines =", lines)
    error = s.stderr.readlines()
    if error:
        print("PrintWordNet() grep error:", file=sys.stderr)
        for e in error:
            print(e, file=sys.stderr)
        normal()
        exit(1)
    # lines now contains those words in the WordNet index.sense file
    # that matched the word passed in.
    for line in lines:
        found_word, letter, head_word, offset = ParseIndexLine(line)
        if dbg:
            print("xx4 word from index line =", found_word, letter)
        if d["-d"] or d["-" + letter]:
            # Note we use Word instead of word or found_word!
            PrintWord(Word, letter, head_word, offset, d)
def WordNet(regexp, d):
    'Given the regexp, search the Wordnet files'
    # If none of the WordNet-related options are True, just do a
    # regular lookup.
    no_wn = (
        not d["-a"] and
        not d["-d"] and
        not d["-n"] and
        not d["-r"] and
        not d["-s"] and
        not d["-v"]
    )
    if no_wn:
        LookUp(regexp, d)
    # Get the word matches from the dictionary file
    cmd = grep + " " + d["-i"] + " --color=auto "
    cmd += "'" + regexp + "' "
    wd = wordnet_files["dict"].replace("\\", "/")
    cmd += wd
    if dbg:
        print("Wordnet search cmd =", cmd)
    p = subprocess.PIPE
    s = subprocess.Popen(cmd, bufsize=0, stdout=p, stderr=p, shell=True)
    # Get results of grep
    results = [i.strip() for i in s.stdout.readlines()]
    error = [i.strip() for i in s.stderr.readlines()]
    if error:
        print("WordNet() grep error:", file=sys.stderr)
        for e in error:
            print(e, file=sys.stderr)
        normal()
        exit(1)
    # Under python 3, the results contents are byte strings, so convert
    # them to text using UTF-8 decoding.
    results = [i.decode("UTF-8") for i in results]
    # We have the full words that matched in results, so print out
    # what the user has requested.
    if dbg:
        print("xx1 results =", results)
    for word in results:
        PrintWordNet(word, d)
    normal()
    exit(0)
def LookUp(regexp, d):
    # Build the grep command string
    cmd = grep + " " + d["-i"] + " --color=auto "
    if "'" in regexp:
        cmd += '"' + regexp + '" '
    else:
        cmd += "'" + regexp + "' "
    wd = d["dict"][d["which_dict"]].replace("\\", "/")
    cmd += wd
    if dbg:
        print("xx grep command =", repr(cmd))
    rc = subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr,
                         bufsize=0, shell=True)
    #normal()
    exit(rc)
def ParseCommandLine(d):
    # Define the dictionaries we'll use.  1 is the default.
    d["dict"] = dictionary_files
    d["-@"] = False     # Get command line words from stdin
    d["-a"] = False     # Limit to adjectives
    d["-c"] = False     # Do not show compound or hyphenated words
    d["-d"] = False     # Show definitions/synonyms
    d["-H"] = False     # 
    d["-h"] = False     # Describe the dictionaries
    d["-i"] = "-i"      # Don't ignore case
    d["-n"] = False     # Limit to nouns
    d["-r"] = False     # Limit to adverbs
    d["-s"] = False     # Look up all words on command line
    d["-S"] = False     # Used for satellite adjectives
    d["-v"] = False     # Limit to verbs
    d["-w"] = False     # Use WordNet dictionary
    d["which_dict"] = 2
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "@012345acdHhinrsvw")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for o, a in optlist:
        if o[1] in set("@acdHnrsvw"):
            d[o] = not d[o]
            if o[1] in set("acdnrv"):
                d["-w"] = True
        elif o[1] in set("012345"):
            d["which_dict"] = int(o[1])
        if o == "-i":
            d[o] = ""
        elif o == "-h":
            Usage(d, status=0)
    if d["-@"]:
        d["-s"] = True
    if d["-w"]:
        d["which_dict"] = "-w"
    if d["-w"] and d["-a"]:
        # We also set -S to True because of the special case of
        # satellite adjectives.
        d["-S"] = True
    if d["-H"]:
        Error("-H not implemented yet")
    if d["-s"]:
        return args
    if not args:
        Usage(d)
    else:
        if len(args) > 1:
            # Combine the words with underscores and use the -d option to
            # look things up in Wordnet.
            d["-d"] = True
            d["-w"] = True
            return '_'.join(args)
        else:
            return args[0]
def Usage(d, status=1):
    which = d["which_dict"]
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] regexp
      Look up a regular expression in a dictionary of words (case-
      insensitive search by default).  If you search the WordNet dictionary,
      use an underscore for the space character (use -c to exclude them).
      The -w option provides the ability to search the list of words from
      WordNet and see synonyms and definitions.  
    
      The -s option is used to look up all the words on the command line
      (they are plain text, not regular expressions).  Any words not (-s) or
      are (-S) in the indicated dictionary are printed out.  Use -@ to read
      stdin for words one line at a time.
    Options:  ({which} is the default dictionary)
      -@      Read words from stdin; implies -s or -S were used
      -0      Use a short English dictionary  (850 words)
      -1      Use a simple dictionary         (42 kwords)
      -2      Use a larger ubuntu dictionary  (98 kwords)
      -3      Use a large dictionary         (274 kwords)
      -4      Use a massive dictionary       (511 kwords)
      -5      Use the ten-hundred dictionary   (1 kwords)
      -H      Describe the dictionaries
      -i      Make search case-sensitive
      -S      Show command line words in dict
      -s      Show command line words not in dict
      -w      Use a dictionary from WordNet  (155 kwords)
    WordNet search options (causes -w option to be set):
        -a      Limit to adjectives
        -c      Do not show compound or hyphenated words
        -d      Show definitions/synonyms for all words that match
        -n      Limit to nouns
        -r      Limit to adverbs
        -v      Limit to verbs
    Acknowledgements for some great tools:
      1.  Thanks to Alan Beale for his 12dicts.
          http://wordlist.aspell.net/12dicts/
      2.  Thanks to the folks at Princeton who provide WordNet:
          http://wordnet.princeton.edu/.
    '''))
    exit(status)
def DictionaryLookup(words, d):
    '''Print words in the list of words that aren't (d["-s"] or are
    (d["-S"]) in the indicated dictionary.
    '''
    # Get dictionary
    def convert(x):
        return x if d["-i"] else lambda x: x.lower()
    tokens = set(GetTokens(d["dict"][d["which_dict"]], convert=convert))
    if d["-@"]:
        # Read lines of words from stdin
        line = sys.stdin.readline()
        while line:
            for word in line.split():
                if convert(word) not in tokens:
                    print(word)
            line = sys.stdin.readline()
    else:
        for word in words:
            if convert(word) not in tokens:
                print(word)
if __name__ == "__main__": 
    d = {}  # Options dictionary
    regexp = ParseCommandLine(d)
    if d["-s"] or d["-S"]:
        DictionaryLookup(regexp, d)
    elif d["-w"]:
        WordNet(regexp, d)
    else:
        LookUp(regexp, d)
