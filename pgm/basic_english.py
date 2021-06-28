'''
Script that will parse words from stdin and print out those that do not
belong to the included words below.

See http://simple.wikipedia.org/wiki/Wikipedia:Basic_English_ordered_wordlist.
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
    # Print words from stdin that don't belong to Ogden's basic English
    # word set
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    from pdb import set_trace as xx
if 1:   # Global variables
    all_words = set()
    punct = ".,;:?![](){}='\"@#$%^&*-_=+|\\<>`~"
    wordlist = '''
    # Basic 100

        i a about across after again against all almost among and any as
        at be because before between but by come do down east enough
        even ever every far for forward from get give go have he here
        how if in keep let little make may much near no north not now of
        off on only or other out over please put quite say see seem send
        so some south still such take than that the then there this
        though through till to together tomorrow under up very well west
        when where while who why will with yes yesterday you

    # General 400

        account act addition adjustment advertisement agreement air
        amount amusement animal answer apparatus approval argument art
        attack attempt attention attraction authority back balance base
        behavior belief birth bit bite blood blow body brass bread
        breath brother building burn burst business butter canvas care
        cause chalk chance change cloth coal color comfort committee
        company comparison competition condition connection control cook
        copper copy cork cotton cough country cover crack credit crime
        crush cry current curve damage danger daughter day death debt
        decision degree design desire destruction detail development
        digestion direction discovery discussion disease disgust
        distance distribution division doubt drink driving dust earth
        edge education effect end error event example exchange existence
        expansion experience expert fact fall family father fear feeling
        fiction field fight fire flame flight flower fold food force
        form friend front fruit glass gold government grain grass grip
        group growth guide harbor harmony hate hearing heat help history
        hole hope hour humor ice idea impulse increase industry ink
        insect instrument insurance interest invention iron jelly join
        journey judge jump kick kiss knowledge land language laugh law
        lead learning leather letter level lift light limit linen liquid
        list look loss love machine man manager mark market mass meal
        measure meat meeting memory metal middle milk mind mine minute
        mist money month morning mother motion mountain move music name
        nation need news night noise note number observation offer oil
        operation opinion order organization ornament owner page pain
        paint paper part paste payment peace person place plant play
        pleasure point poison polish porter position powder power price
        print process produce profit property prose protest pull
        punishment purpose push quality question rain range rate ray
        reaction reading reason record regret relation religion
        representative request respect rest reward rhythm rice river
        road roll room rub rule run salt sand scale science sea seat
        secretary selection self sense servant sex shade shake shame
        shock side sign silk silver sister size sky sleep slip slope
        smash smell smile smoke sneeze snow soap society son song sort
        sound soup space stage start statement steam steel step stitch
        stone stop story stretch structure substance sugar suggestion
        summer support surprise swim system talk taste tax teaching
        tendency test theory thing thought thunder time tin top touch
        trade transport trick trouble turn twist unit use value verse
        vessel view voice walk war wash waste water wave wax way weather
        week weight wind wine winter woman wood wool word work wound
        writing year yearaccount

    # 100 picturable words

        angle ant apple arch arm army baby bag ball band basin basket
        bath bed bee bell berry bird blade board boat bone book boot
        bottle box boy brain brake branch brick bridge brush bucket bulb
        button cake camera card carriage cart cat chain cheese chest
        chin church circle clock cloud coat collar comb cord cow cup
        curtain cushion dog door drain drawer dress drop ear egg engine
        eye face farm feather finger fish flag floor fly foot fork fowl
        frame garden girl glove goat gun hair hammer hand hat head heart
        hook horn horse hospital house island jewel kettle key knee
        knife knot leaf leg library line lip lock map match monkey moon
        mouth muscle nail neck needle nerve net nose nut office orange
        oven parcel pen pencil picture pig pin pipe plane plate
        plough/plow pocket pot potato prison pump rail rat receipt ring
        rod roof root sail school scissors screw seed sheep shelf ship
        shirt shoe skin skirt snake sock spade sponge spoon spring
        square stamp star station stem stick stocking stomach store
        street sun table tail thread throat thumb ticket toe tongue
        tooth town train tray tree trousers umbrella wall watch wheel
        whip whistle window wing wire worm

    # 100 general qualities

        able acid angry automatic beautiful black boiling bright broken
        brown cheap chemical chief clean clear common complex conscious
        cut deep dependent early elastic electric equal fat fertile
        first fixed flat free frequent full general good great grey/gray
        hanging happy hard healthy high hollow important kind like
        living long male married material medical military natural
        necessary new normal open parallel past physical political poor
        possible present private probable quick quiet ready red regular
        responsible right round same second separate serious sharp
        smooth sticky stiff straight strong sudden sweet tall thick
        tight tired true violent waiting warm wet wide wise yellow young

    # 50 opposites

        awake bad bent bitter blue certain cold complete cruel dark dead
        dear delicate different dirty dry false feeble female foolish
        future green ill last late left loose loud low mixed narrow old
        opposite public rough sad safe secret short shut simple slow
        small soft solid special strange thin white wrong

    # Don's additions

        add an are is it its should unless above added aid aim allow
        already also although always am another anything anytime appear
        aren't ask avoid avoided avoiding aware awareness away awful
        become been begin being best better born both break buy caee can
        cannot car caused center chair check chew choose chosen close
        coming contain contents copies correct correctly could course
        create creating data desk difference doing don't each easier
        easily easy eat eaten eats edit editing ehar enter essential
        everyone everything fail feel few file finish five follow found
        four fresh fuel function further giving goal going greater
        greatest happen has having he'll her highest himself his hit
        home however i'd i'll i'm into is it it's item its know leading
        least leave leaving life load log lot lower lunch made main
        maintain maintaining makes making many maximise maximum me mean
        meaning medicine minimize minimum mistake modified moment more
        most multiple must my naming needed never next nine obvious
        often ok once one opposed option our particular particularly
        pause people perfectly phone piece plain pointing positive press
        prevent problem producing product provide putting quickly rather
        read reader real rear require returned said save search seeing
        seven she should show since six sixth somewhere soon sooner
        speak speaker split stay sure takes task tell term text their
        them theselves they they're those three told too tool try trying
        twice two type upon us used useful useless using want was we
        we're were what whether which whole whom without won't worry
        worst would write writer written wrote you'll within
        
        i came come cried fine girl boy him her large mr mrs oh own
        taken wife husband visit view park perhaps monday tuesday
        wednesday thursday friday saturday sunday lady man men woman
        women had case just known affect agree agreed certain certainly
        enter entering heard grow grown likely party share single think
        thinking truth families acted acting adding address age ago
        afraid ah alike alive alone along apply january february march
        april may june july august september october november december
        assume asked ate aunt uncle bear became beg began below bold bow
        busy bye call cared child city cool cost date did die died
        dinner dirt dish does done drive due dying one two three four
        five six seven eight nine ten eleven twelve thirteen fourteen
        fifteen sixteen seventeen eighteen nineteen twenty thirty forty
        fifty sixty seventy eighty ninety hundred else ended except fair
        fast feet fell fill find fit fix fool fun game gave given glad
        goes gone grew guest half hall harm hear hide hidden hold hot
        hurt itself joy kept kill knew ladies lane lay laying learn led
        less lie liked listen live lived lose lost mamma papa mom dad
        matter meet met mild mile miss mud none nothing object occur odd
        owe paid pair path pass pay paying per plan post pour poured
        proud pure quit race ran result return ride rise rock sat saw
        sell sent set shop sick sit slowly tea tear teeth thank these
        throw threw took tried unhappy until upper wait waited walked
        wanted wear went wish wonder yet your yourself

    '''
def GetAllWords():
    global all_words
    words = []
    for line in wordlist.split("\n"):
        line = line.strip()
        if not line or line[0] == "#":
            continue
        all_words.update(set(line.split()))
def RemovePunctuation(word):
    if word[0] in punct:
        word = word[1:]
    try:
        if word[-1] in punct:
            return word[:-1]
    except Exception:
        pass
    return word
def ProcessLine(linenum, line, wordsdict):
    '''Split the line into words and put each word into the dictionary
    wordsdict (key = word, value = linenumber).
    '''
    table = ''.maketrans(punct, " "*len(punct))
    words = line.lower().translate(table).split()
    for word in words:
        if word not in wordsdict:
            wordsdict[word] = linenum
def GetWords():
    '''Read the lines from stdin and return a dictionary of the words
    from these lines.  The word is the key; the value is the line
    number.
    '''
    words = {}
    if 0:
        print("xx, Reading from file instead of stdin")
        for i, line in enumerate(open("aa").readlines()):
            ProcessLine(i + 1, line, words)
        return words
    for i, line in enumerate(sys.stdin.readlines()):
        ProcessLine(i + 1, line, words)
    return words
def NotElementaryWord(word):
    '''Return True if word is not an elementary word.
    '''
    if word in all_words:
        return False
    # Check for plurals
    if word.endswith("s"):
        if word[:-1] in all_words:
            return False
    elif word.endswith("es"):
        if word[:-2] in all_words:
            return False
    return True
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-h":
        print(dedent(f'''
        Usage:  {sys.argv[0]}
          Parses stdin into words and print those that don't belong to basic
          English usage.
        '''))
        exit(0)
    GetAllWords()
    # Put all the words from stdin in a dictionary (word : linenum)
    words = GetWords()
    # Now check each word
    bad = []
    for word in words:
        if NotElementaryWord(word):
            linenum = words[word]
            bad.append(f"{word} [{linenum:d}]")
    bad.sort()
    print("Non-elementary words:  (line number in brackets)")
    for s in bad:
        print("  ", s)
