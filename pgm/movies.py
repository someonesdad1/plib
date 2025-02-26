"""
Index of movies on VCR tapes
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2005 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Index of movies on VCR tapes
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import os
    import getopt
    import re
    from collections import defaultdict
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
if 1:  # Global variables
    # Data are (tape number ; Title)
    data = """
        1 ; American Graffiti
        1 ; Beverly Hills Cop
        1 ; High Anxiety
        2 ; Bugs Bunny/Road Runner Movie, The
        2 ; Christmas Carol, A
        2 ; Down & Out in Beverly Hills
        3 ; Emerald Forest, The
        3 ; Natural, The
        3 ; Raiders of the Lost Ark
        4 ; 2001
        4 ; Star Wars
        5 ; Blazing Saddles
        5 ; Top Secret
        5 ; Young Frankenstein
        6 ; Airplane
        6 ; Buckaroo Bonzai
        6 ; Ensign Pulver (remake)
        7 ; Baby
        7 ; Last Starfighter, The
        7 ; Romancing the Stone
        8 ; Star Trek
        8 ; Star Trek2:  Wrath of Khan
        8 ; Star Trek3:  Search For Spock
        9 ; Elephant Man
        9 ; Koyaanisqatsi
        9 ; Like Father Like Son
        10 ; Kramer vs. Kramer
        10 ; Spartacus
        11 ; Donald
        11 ; Ladyhawke
        11 ; Never Cry Wolf
        12 ; Blade Runner
        12 ; Spring Break
        12 ; Whitewater Sam
        13 ; Donald's Bee Pictures
        13 ; Explorers
        13 ; Swiss Family Robinson
        14 ; Brewster's Millions
        14 ; Just the Way You Are
        14 ; Terms of Endearment
        15 ; From the Hip
        15 ; Jagged Edge
        15 ; Legal Eagles
        16 ; Bonnie and Clyde
        16 ; Godfather, The
        17 ; Empire Strikes Back
        17 ; Gone With the Wind
        18 ; Cocoon
        18 ; Lost in America
        18 ; Save the Tiger
        19 ; Superman 2
        19 ; Uncommon Valor
        19 ; Windwalker
        20 ; Cotton Club, The
        20 ; Deer Hunter, The
        21 ; Bill Cosby -- Himself
        21 ; Chariots of Fire
        21 ; Superman 3
        22 ; Murder by Death
        22 ; Russians Are Coming, The
        22 ; Tootsie
        23 ; Butch Cassidy
        23 ; Fireball Forward
        23 ; Support Your Local Sheriff
        24 ; Breakfast at Tiffany's
        24 ; Flim Flam Man, The
        24 ; My Bodyguard
        25 ; China Syndrome
        25 ; Summer Rental
        25 ; Witness for the Prosecution
        26 ; Casablanca
        26 ; First Blood
        26 ; Mask
        27 ; Falcon & the Snowman
        27 ; On Golden Pond
        28 ; Gambler, The
        28 ; Rear Window, The
        29 ; Marathon Man
        29 ; Octopussy
        30 ; Mad Max
        30 ; My Summer Vacation
        30 ; Star Chamber
        31 ; Masada
        31 ; Mr. Roberts
        31 ; Prizzi's Honor
        32 ; Sleuth
        33 ; Inv of Body Snatchers
        34 ; Plan 9 From Outer Space
        35 ; Thing, The (original)
        36 ; NFL Crunch Course
        37 ; Best of Football Follies
        38 ; Das Boot
        38 ; Perils of Gwendolyn, The
        38 ; Sixteen Candles (uncensored)
        39 ; Karate Kid, The
        39 ; Never Ending Story, The
        39 ; Oh God, You Devil!
        40 ; Creator
        40 ; Return of the Jedi
        40 ; Weird Science
        41 ; Bullitt
        41 ; DARYL
        41 ; Real Genius
        42 ; Better off Dead
        42 ; Grace Quigley
        42 ; Sting, The
        43 ; Compromising Positions
        43 ; Finnegan Begin Again
        43 ; Johnny Dangerously
        44 ; Missing in Action
        44 ; Slap Shot
        44 ; Witness
        45 ; Citizen Kane
        45 ; Magnificent Seven, The
        45 ; Slapshot
        46 ; Arthur
        46 ; Dog Day Afternoon
        46 ; Victor/Victoria
        47 ; Sam's Son
        47 ; Three Musketeers, The
        47 ; Wargames
        48 ; They Call Me Trinity
        48 ; What's Up, Doc?
        48 ; Wild Bunch, The
        49 ; WC Fields: Golf Specialist
        49 ; WC Fields: The Dentist
        49 ; WC Fields: The Fatal Glass of Beer
        50 ; Airplane 2
        50 ; Greystoke: Tarzan
        50 ; Passage to India, A
        51 ; Burglar
        51 ; Dragnet
        51 ; Twins
        52 ; Billy Jack
        52 ; Goodbye Girl, The
        52 ; Yankee Doodle Dandy
        53 ; All of Me
        53 ; Pee Wee's Big Adventure
        53 ; Sound of Music, The
        54 ; Brian's Song
        54 ; French Lt's Woman
        54 ; Murphy's Romance
        55 ; Ain't That Ducky?
        56 ; Nuttiness Continues, The
        57 ; Breakfast Club, The
        57 ; Clue Movie, The
        57 ; Gunga Din
        58 ; Jewel of the Nile
        58 ; Out of Africa
        58 ; Transylvania 6-5000
        59 ; Ghandi
        59 ; Truly Tasteless Jokes
        60 ; Back to the Future
        60 ; Nevada Smith
        60 ; Outland
        61 ; Donovan's Reef
        61 ; Gremlins
        61 ; Thomasina
        62 ; Longest Yard, The
        62 ; National Lampoon's Vacation
        62 ; Strange Brew
        63 ; Holcroft Covenant, The
        63 ; Money Pit, The
        63 ; Rambo
        64 ; Indiana Jones: Temple of Doom
        64 ; Space Camp
        64 ; Young Sherlock Holmes
        65 ; Daffy Duck
        66 ; Victory at Sea, Vol. 1
        67 ; Victory at Sea, Vol. 2
        68 ; Victory at Sea, Vol. 3
        69 ; Victory at Sea, Vol. 4
        70 ; Victory at Sea, Vol. 5
        71 ; Victory at Sea, Vol. 6
        72 ; Lucas
        72 ; Short Circuit
        72 ; Wildcats
        73 ; Ocean's Eleven
        73 ; Pretty in Pink
        73 ; Sword in the Stone
        74 ; A Piece of the Action
        74 ; Howard the Duck
        74 ; My Little Chickadee
        74 ; Trouble With Tribbles, The
        75 ; Battle of Britain
        75 ; Heartbreak Kid, The
        75 ; Old Gringo
        75 ; Rocky
        76 ; Papillon
        76 ; Quiet Man, The
        76 ; Sunshine Boys, The
        77 ; My Chauffeur
        77 ; Stand By Me
        77 ; Top Gun
        78 ; Ferris Bueller's Day Off
        78 ; Silent Night, Deadly Night
        78 ; Thing, The (second version)
        79 ; April Fool's Day
        79 ; Cujo
        79 ; Three Days of the Condor
        80 ; Half Moon Street
        80 ; Highlander
        80 ; Jeremiah Johnson
        81 ; Bill Cosby:  49
        81 ; Check is in the Mail
        81 ; Jumpin' Jack Flash
        82 ; Armed and Dangerous
        82 ; Class Reunion
        82 ; Haunted Honeymoon
        83 ; Great Expectations
        83 ; Red Dawn
        83 ; Throw Momma From Train
        84 ; Drywall Home Improvement
        84 ; Interior Wall Finishing
        84 ; Plumbing
        84 ; Preparation & Painting
        85 ; Man Who Knew Too Much
        85 ; Rope
        85 ; Vertigo
        86 ; Dirty Dozen, The
        86 ; Nightmare on Elm Street 3
        87 ; Cool Hand Luke
        87 ; King and I, The
        87 ; Tale of Two Chipmunks
        88 ; Birds, The
        88 ; Dark Crystal, The
        88 ; Now and Forever
        89 ; Dr. Detroit
        89 ; Remo Williams
        89 ; Sixteen Candles (censored)
        90 ; Nova Math Mystery Tour
        91 ; Family Plot
        91 ; Gray Lady Down
        91 ; When Wolves Cry
        92 ; Disney
        93 ; A  Christmas Story
        93 ; Desperately Seeking Susan
        93 ; Killing Hour, The
        94 ; Rio Lobo
        94 ; Rooster Cogburn
        94 ; War Wagon
        95 ; Red River
        95 ; Rio Grande
        96 ; Fighting SeaBees
        96 ; Sons of Katie Elder
        97 ; Cobra
        97 ; Platoon
        97 ; Running Man
        98 ; Heartbreak Ridge
        98 ; PePe La Pew's Skunk Tales
        98 ; Raw Deal
        99 ; Adventures in Babysitting
        99 ; Colors
        99 ; Real Men
        100 ; Christine
        100 ; Nightmare on Elm Street
        100 ; Terminator
        101 ; Black Widow
        101 ; How to Marry a Millionaire
        101 ; River, The
        102 ; Private Resort
        102 ; Return of the Living Dead
        102 ; Star Trk4:  Voyage Home
        103 ; Buddy Holly Story, The
        103 ; Principal, The
        103 ; Suspect
        104 ; Birth of the Blues
        104 ; Terror in the Aisles
        104 ; Three Men and a Baby
        105 ; Die Hard
        105 ; Elvira - Mistress of Dark
        105 ; Short Circuit 2
        106 ; Blind Date
        106 ; Count Dracula
        106 ; Superman 4
        107 ; Nuts
        107 ; Question of Guilt, A
        107 ; Trains, Planes & Automobiles
        108 ; Last Emperor
        108 ; Willow
        109 ; Beverly Hills Cop 2
        109 ; Frantic
        109 ; Outrageous Fortune
        110 ; Blood Sport
        110 ; Halloween 4
        110 ; Seventh Sign, The
        111 ; Adam's Rib
        111 ; Crocodile Dundee 2
        111 ; Night Court
        111 ; Predator
        112 ; Nova
        113 ; Charley Lonesome Cougar
        113 ; Coming to America
        113 ; ET
        114 ; La Bamba
        114 ; Moonstruck
        114 ; Stand Alone
        115 ; Big Business
        115 ; Cocktail
        115 ; Whitewater Summer
        116 ; Enemy Mine
        116 ; Married to the Mob
        116 ; Moving
        117 ; Cocoon II The Return
        117 ; Dirty Rotten Scoundrels
        117 ; Fish Called Wanda,
        118 ; Inner Space
        118 ; Mississippi Burning
        118 ; Revenge of the Nerds II
        119 ; Big
        119 ; Obsession
        119 ; Satchmo
        120 ; Captain's Courageous
        120 ; My Stepmother is an Alien
        120 ; Punchline
        121 ; Burbs, The
        121 ; Stranger, The
        121 ; Who Is Harry Crumb
        122 ; Bill & Ted's Excellent Adventure
        122 ; True Believer
        122 ; Woman in Red, The
        123 ; Naked Gun, The
        123 ; Scrooged
        123 ; Working Girl
        124 ; Dangerous Liaisons
        124 ; Indiana Jones Last Crusade
        124 ; Space Balls
        125 ; Patton
        125 ; Second Sight
        125 ; Tucker
        126 ; Lethal Weapon 1
        126 ; Lethal Weapon 2
        126 ; See No Evil, Hear No Evil
        127 ; For Keeps
        127 ; Peter Pan
        127 ; Wait Until Dark
        128 ; Cartoon Classics
        129 ; 747 Pilots Eye View
        130 ; Cinderella
        131 ; Daffy Duck
        132 ; Casper
        133 ; Abyss, The
        133 ; Dead Poets Society
        134 ; An Innocent Man
        134 ; Conan the Destroyer
        134 ; Harlem Nights
        135 ; Day the Earth Stood Still
        135 ; Fabulous Baker Boys
        135 ; Turner & Hooch
        136 ; Don & Glenda's Wedding
        137 ; Civil War:  Fiery Trial
        138 ; Shirley Temple Festival
        139 ; Daffy Duck
        140 ; Daffy Duck
        141 ; Escape from Sobibor
        141 ; How Life Begins
        141 ; Psycho
        142 ; Voyager I Encounters
        143 ; DOA
        143 ; Moon Over Parador
        143 ; Sledge Hammer
        144 ; 3 Chumps and a Baby
        144 ; A  Cry In the Dark
        144 ; Cat Ballou
        144 ; Dead Calm
        145 ; Dead Pool
        145 ; Family Business
        145 ; Steel Magnolias
        146 ; Peterson's Movies
        147 ; Fields of Dream
        147 ; Leviathan
        147 ; Secret Garden
        148 ; Exercise to the 50's
        150 ; Color Purple, The
        150 ; Parenthood
        151 ; Fat Man, Little Boy
        151 ; Fletch
        151 ; The Accused
        152 ; Code Name:  Emerald
        152 ; Final Countdown
        153 ; Feds
        153 ; Hunt for Red October
        153 ; LA Story
        154 ; 48 Hours
        154 ; Another 48 Hours
        154 ; Sara, Plain and Tall
        155 ; Brighton Beach Memoirs
        155 ; Package, The
        155 ; Stake Out
        156 ; Blue Steel
        156 ; Chances Are
        156 ; Cousins
        157 ; Let it Ride
        157 ; Pretty Woman
        157 ; Sweet Dreams
        158 ; Driving Miss Daisy
        158 ; Lock Up
        158 ; Tequila Sunrise
        159 ; Happy Together
        159 ; She Devil
        159 ; Uncle Buck
        160 ; Above the Law
        160 ; Criminal Law
        160 ; Internal Affairs
        161 ; Flashback
        161 ; Stella
        161 ; Why Me
        162 ; Cadillac Man
        162 ; Deceivers, The
        162 ; Great Balls of Fire
        163 ; Once Around
        163 ; Russia House, The
        163 ; Switch
        164 ; Arachnophobia
        164 ; Ghost
        164 ; Narrow Margin
        165 ; Flatliners
        165 ; One Night Stand
        165 ; Pacific Heights
        165 ; Presumed Innocent
        166 ; Boost, The
        166 ; European Vacation
        166 ; Mosquito Coast, The
        167 ; Clara's Heart
        167 ; Opportunity Knocks
        167 ; Seven Hours to Judgment
        168 ; I Love You To Death
        168 ; Problem Child
        168 ; Short Time
        169 ; Sibling Rivalry
        169 ; Two Jakes, The
        169 ; Witches
        170 ; Promised Land
        170 ; Running Scared
        170 ; Stepfather, The
        171 ; Edward Scissorhands
        171 ; Kindergarten Cop
        171 ; Shipwrecked
        172 ; Best Seller
        172 ; Physical Evidence
        172 ; Without a Clue
        173 ; Bird on a Wire
        173 ; Desperate Hours
        173 ; White Palace
        174 ; Misery
        174 ; Overboard
        174 ; Sleeping With the Enemy
        175 ; Bonfires of the Vanities
        175 ; Five Heartbeats, The
        175 ; Mr. & Mrs. Bridge
        176 ; Almost An Angel
        176 ; Awakenings
        176 ; Good Fellas
        177 ; David
        177 ; Green Card
        177 ; Lean on Me
        178 ; Class Action
        178 ; Nothing But Trouble
        178 ; Whistle Blower
        179 ; All About Eve
        179 ; Harvey
        179 ; White Christmas
        180 ; Annie Hall
        180 ; New Jack City
        180 ; Terminator 2
        181 ; Back to the Future III
        181 ; Home Alone
        181 ; King Ralph
        182 ; Doors, The
        182 ; Quiqley Down Under
        183 ; Naked Gun 2 1/2
        183 ; Robin Hd - Prince of Thieves
        183 ; Silence of the Lambs
        184 ; Betsy's Wedding
        184 ; Bringing Up Baby
        185 ; Crocodile Dundee
        185 ; Die Hard 2
        185 ; Shock to the System
        186 ; Backdraft
        186 ; Cyrano de Bergerac
        186 ; Ghost Dad
        187 ; Jerk, The
        187 ; Playmates
        187 ; Shadow of a Doubt
        188 ; City Slickers
        188 ; Grifters, The
        188 ; She Woke Up
        189 ; Lawnmower Man
        189 ; Memoirs of An Invisible Man
        189 ; Roger Rabbit
        189 ; Who Framed Roger Rabbit?
        190 ; Dorf Olympics
        190 ; It's a Mad, Mad,World
        190 ; Sneakers
        191 ; For the Boys
        191 ; Grease
        191 ; Ricochet
        192 ; Deceived
        192 ; Patriot Games
        192 ; Shining Through
        193 ; Bible, The
        193 ; Dark Crystal
        194 ; FX2
        194 ; Hellbound Hellraiser II
        194 ; Hidden, The
        195 ; Far and Away
        195 ; Housesitter
        195 ; Indecent Proposal
        196 ; Coneheads, The
        196 ; Shining, The
        197 ; Hot Shots Part Dieux
        197 ; Singles
        197 ; Under Siege
        198 ; Against All Flags
        198 ; Sea Hawk, The
        198 ; Sea Wolf, The
        199 ; Subs:  Sharks of Steel
        200 ; Ten Commandments, The
        201 ; Dances With Wolves
        201 ; Thelma and Louise
        202 ; Scent of a Woman
        202 ; True Romance
        203 ; Emergency Preparedness
        203 ; Lorenzo's Oil
        204 ; Dirty Harry
        204 ; Little Man Tate
        205 ; SNL Christmas Past Special
        205 ; SNL Dorf Special
        206 ; Captain Ron
        206 ; House Warming
        206 ; Intersection
        207 ; Crash Landing
        207 ; Remember the Day
        207 ; Stella Dallas
        208 ; Fried Green Tomatoes
        208 ; JFK
        209 ; Defenseless
        209 ; Drop Dead Fred
        209 ; Hatari
        210 ; Bugsy
        210 ; Last Boy Scout, The
        210 ; Point Break
        211 ; Carlito's Way
        211 ; Fugitive, The
        212 ; Ace Ventura
        212 ; Perfect World, A
        212 ; Sometimes a Great Notion
        213 ; Basic Instinct
        213 ; Rocketeer, The
        213 ; Sister Act
        214 ; Alive
        214 ; Free Willy
        214 ; Sleepless in Seattle
        215 ; Babe (Ruth), The
        215 ; Hoffa
        216 ; Fleet's In
        216 ; Glenn Miller Story
        216 ; If I'm Lucky
        217 ; Cape Fear
        217 ; Doctor, The
        217 ; Garth Brooks Concert
        218 ; Benny Goodman Story
        218 ; Great Dictator, The
        218 ; Song is Born, A
        219 ; Dracula
        219 ; Foreign Affair, A
        220 ; Tombstone
        221 ; Schindler's List
        222 ; Little Colonel, The
        222 ; Shirley Temple
        223 ; Three Faces of Eve
        223 ; Wuthering Heights
        224 ; Cutting Edge, The
        224 ; Radio Flyer
        224 ; Roxanne
    """


def Usage(d, status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] regexp
      Print movie titles containing regexp.
    Options:
      -h    Print a manpage
      -i    Make the search case-sensitive
      -n    Print titles by tape number
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-i"] = False
    d["-n"] = False
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, regex = getopt.getopt(sys.argv[1:], "hin")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-h",):
            Usage(d, status=0)
        elif o in ("-n",):
            d["-n"] = not d["-n"]
        elif o in ("-i",):
            d["-i"] = not d["-i"]
    if not d["-n"] and len(regex) != 1:
        Usage(d)
    return None if d["-n"] else regex[0]


def GetMovies(d):
    movies = []
    by_number = defaultdict(list)
    for i in data.split("\n"):
        i = i.strip()
        if not i or i[0] == "#":
            continue
        tape, title = i.split(";")
        tape = int(tape)
        m = (title.strip(), tape)
        by_number[tape].append(title)
        movies.append(m)
    movies.sort()
    d["movies"] = movies
    d["by_number"] = by_number


def Search(regex, d):
    """Return (movies, max_width) where movies is a list of tuples
    (title, tape_number) and max_width is the widest title.
    """
    if d["-i"]:
        r = re.compile(regex)
    else:
        r = re.compile(regex, re.I)
    movies, max_width = [], 0
    for title, tape in d["movies"]:
        if r.search(title):
            movies.append((title, tape))
            max_width = max(max_width, len(title))
    movies.sort()
    return (movies, max_width + 2)


def PrintByNumber(d):
    n = d["by_number"]
    numbers = list(n.keys())
    numbers.sort()
    for i in numbers:
        print("{0:5d}".format(i), end=" ")
        first = True
        for j in n[i]:
            if first:
                print(j)
                first = False
            else:
                print("{0:5s}".format(""), j)
    exit(0)


if __name__ == "__main__":
    d = {}  # Options dictionary
    regex = ParseCommandLine(d)
    GetMovies(d)
    if d["-n"]:
        PrintByNumber(d)
    movies, max_width = Search(regex, d)
    for title, tape in movies:
        f = "{0:%ds} {1}" % max_width
        print(f.format(title, tape))
