'''
Print words that are not in Ogden's 850 basic English words
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
    # Print words that are not in Ogden's 850 basic English words
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    import re
    from collections import deque
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from columnize import Columnize
if 1:   # Global variables
    ogdens_words = set('''
        i a able about account acid across act addition adjustment
        advertisement after again against agreement air all almost among
        amount amusement and angle angry animal answer ant any apparatus
        apple approval arch argument arm army art as at attack attempt
        attention attraction authority automatic awake baby back bad bag
        balance ball band base basin basket bath be beautiful because bed
        bee before behavior belief bell bent berry between bird birth bit
        bite bitter black blade blood blow blue board boat body boiling
        bone book boot bottle box boy brain brake branch brass bread breath
        brick bridge bright broken brother brown brush bucket building bulb
        burn burst business but butter button by cake camera canvas card
        care carriage cart cat cause certain chain chalk chance change
        cheap cheese chemical chest chief chin church circle clean clear
        clock cloth cloud coal coat cold collar color comb come comfort
        committee common company comparison competition complete complex
        condition connection conscious control cook copper copy cord cork
        cotton cough country cover cow crack credit crime cruel crush cry
        cup current curtain curve cushion cut damage danger dark daughter
        day dead dear death debt decision deep degree delicate dependent
        design desire destruction detail development different digestion
        direction dirty discovery discussion disease disgust distance
        distribution division do dog door doubt down drain drawer dress
        drink driving drop dry dust ear early earth east edge education
        effect egg elastic electric end engine enough equal error even
        event ever every example exchange existence expansion experience
        expert eye face fact fall false family far farm fat father fear
        feather feeble feeling female fertile fiction field fight finger
        fire first fish fixed flag flame flat flight floor flower fly fold
        food foolish foot for force fork form forward fowl frame free
        frequent friend from front fruit full future garden general get
        girl give glass glove go goat gold good government grain grass
        great green grey gray grip group growth guide gun hair hammer hand
        hanging happy harbor hard harmony hat hate have he head healthy
        hearing heart heat help here high history hole hollow hook hope
        horn horse hospital hour house how humor ice idea if ill important
        impulse in increase industry ink insect instrument insurance
        interest invention iron island jelly jewel join journey judge jump
        keep kettle key kick kind kiss knee knife knot knowledge land
        language last late laugh law lead leaf learning leather left leg
        let letter level library lift light like limit line linen lip
        liquid list little living lock long look loose loss loud love low
        machine make male man manager map mark market married mass match
        material may meal measure meat medical meeting memory metal middle
        military milk mind mine minute mist mixed money monkey month moon
        morning mother motion mountain mouth move much muscle music nail
        name narrow nation natural near necessary neck need needle nerve
        net new news night no noise normal north nose not note now number
        nut observation of off offer office oil old on only open operation
        opinion opposite or orange order organization ornament other out
        oven over owner page pain paint paper parallel parcel part past
        paste payment peace pen pencil person physical picture pig pin pipe
        place plane plant plate play please pleasure plow pocket point
        poison polish political poor porter position possible pot potato
        powder power present price print prison private probable process
        produce profit property prose protest public pull pump punishment
        purpose push put quality question quick quiet quite rail rain range
        rat rate ray reaction reading ready reason receipt record red
        regret regular relation religion representative request respect
        responsible rest reward rhythm rice right ring river road rod roll
        roof room root rough round rub rule run sad safe sail salt same
        sand say scale school science scissors screw sea seat second secret
        secretary see seed seem selection self send sense separate serious
        servant sex shade shake shame sharp sheep shelf ship shirt shock
        shoe short shut side sign silk silver simple sister size skin skirt
        sky sleep slip slope slow small smash smell smile smoke smooth
        snake sneeze snow so soap society sock soft solid some son song
        sort sound soup south space spade special sponge spoon spring
        square stage stamp star start statement station steam steel stem
        step stick sticky stiff still stitch stocking stomach stone stop
        store story straight strange street stretch strong structure
        substance such sudden sugar suggestion summer sun support surprise
        sweet swim system table tail take talk tall taste tax teaching
        tendency test than that the then theory there thick thin thing this
        though thought thread throat through thumb thunder ticket tight
        till time tin tired to toe together tomorrow tongue tooth top touch
        town trade train transport tray tree trick trouble trousers true
        turn twist umbrella under unit up use value verse very vessel view
        violent voice waiting walk wall war warm wash waste watch water
        wave wax way weather week weight well west wet wheel when where
        while whip whistle white who why wide will wind window wine wing
        winter wire wise with woman wood wool word work worm wound writing
        wrong year yellow yes yesterday you young
        '''.split())
def Usage(status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [file1 [file2 ...]]
      Split the text files into words by substituting space characters for all
      punctuation and splitting on whitespace.  After converting to lowercase,
      print out any words that are not in Ogden's "Basic English" list of 850
      words.  Use '-' to take input from stdin.

      Ogden's word list was created in 1930 with the intent of finding the
      basic list of words that can express 90% of the concepts in the Oxford
      Pocket English Dictionary.  Unfortunately, words and meanings change over
      time, so it's uncertain how useful a list nearly a century old is.  For
      example, the word spam didn't exist when Ogden made his list, yet it has
      two important meanings today in the 2020's.  

      Still, if you use this script to assess how large the set of words you
      use in your writing is, it may cause you to revise your writing.  The
      first job of writing is to communicate, so to first order, it's less
      important to be grammatically correct than to get the correct ideas
      across.  For example, you might say "He don't understand the book" and
      though it's grammatically incorrect, most everyone will understand it.
      Clearly, what you allow in your writing is dependent on the audience.
    Options:
      -h    Print a manpage
      -n    Ignore words with numbers
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-n"] = False     # Ignore words with numbers
    try:
        optlist, files = getopt.getopt(sys.argv[1:], "hn")
    except getopt.GetoptError as str:
        msg, option = str
        out(msg)
        sys.exit(1)
    for o, a in optlist:
        if o[1] in "n":
            d[o] = not d[o]
        if o == "-h":
            Usage(status=0)
    if not files:
        Usage()
    return files
def GetLines(files):
    s = []
    for file in files:
        if file == "-":
            s += sys.stdin.readlines()
        else:
            s += open(file).readlines()
    return s
def GetTranslationTable():
    '''Returns a dictionary indexed by integers 0 to 255 that map a Unicode
    ordinal to an equivalent ordinal.  Here, characters that are not letters
    or digits are converted to space characters.
    '''
    td = {}
    for key in range(256):
        if (0x41 <= key <= 0x5a or      # Upper case letters
            0x61 <= key <= 0x7a or      # Lower case letters
            0x30 <= key <= 0x39):       # Digits
            td[key] = key
        else:
            td[key] = 0x20               # Space character's ordinal
    return td
def GetWords(lines):
    '''Convert all the text to a single string, make it lowercase,
    then return it as a set of words.
    '''
    s = ' '.join(lines).lower()
    table = GetTranslationTable()
    tt = str.maketrans(table)
    words = set(s.translate(tt).split())
    if d["-n"]:     # Ignore words with number digits
        r = re.compile(r"\d+")
        out, words = deque(), deque(words)
        while words:
            word = words.popleft()
            if not r.search(word):
                out.append(word)
        words = set(out)
    return words
if __name__ == "__main__": 
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    lines = GetLines(files)
    words = GetWords(lines)
    big_words = sorted(list(words - ogdens_words))
    if big_words:
        print("The following words are not in Ogden's list of 850 simple English words:")
        for line in Columnize(big_words):
            print(line)
