from collections import namedtuple
from color import t
from dpprint import PP
from get import GetTextLines
import iso
import requests
import sys
if 0:
    import debug
    debug.SetDebugger()
pp = PP()
# Fields are
#   0   Title
#   1   Artist
#   2   URL
#   3   Comment
Entry = namedtuple("Entry", "title artist url comment")
favorites = '''

    Angie ; Rolling Stones ; oWRr03VcA-0 ;
    Bach: Toccata and Fugue in D Minor ; Amy Turk ; oPmKRtWta4E ;
    Bach: Toccata and Fugue in D Minor ; Canadian Brass ; _Cst9lV5PPg ;
    Beethoven's 7th ; Bernstein ; Rw-KtQLdRT4 ; 2nd movement at 14:33 is my favorite
    Beethoven's 9th, 2nd movement (1824) ; ; iwIvS4yIThU ; 
    Beethoven: Moonlight Sonata (3rd) ;Tina S ; o6rBK0BqL2w ; 
    Bad Romance ; PMJ, Sarah Reich, Ariana Savalas ; VCTOpdlZJ8U ; Percussion by Sarah Reich :^)
    Catharsis ; Sally ; h3hlFAVV6aI ; My favorite fiddle song
    Crazy ; Patsy Cline ; MbnrdCS57d0 ; 
    Diamonds and Rust ; Joan Baez ; IrVD0bP_ybg ; 
    Don't Cry For Me Argentina ; Karen Carpenter ; _n8mq7sedP4 ; 
    Fast Freight ; Eliza Gilkyson ; Sin3FeAQAws ;  Singer is song writer's daughter
    Hit the Road Jack ; Becca Krueger ; OfUDsHtSv88 ; (skip first 20 seconds)
    Ievan Polkka ; Loituma ; 4om1rQKPijI ; 2008
    I'll Never Find Another You ; Seekers ; KmactMIhrRM ; How I feel about Glenda
    Korobushka ; ; Pr3ZgN8onRA ; (vocal)
    Korobushka ; Bond ; E5NByiEIbD8 ; (strings)
    Midnight In Moscow ; Kenny Ball ; o744d4mwOgQ ; 
    Papillon (waltz arrangement) ; ; FKrmozFh5ww ; 
    Potato Head Blues ; Louis Armstrong ; EfGZB78R7uw ; Famous trumpet solo
    Scheherazade (1st movement) ; Rimsky-Korsakov ; 6dDk6aft4JU ;
    Stairway to Heaven ; Led Zeppelin ; QkF3oxziUI4 ; 
    The Good, The Bad, and the Ugly ; Danish National Symphony ; enuOArEfqGo ; 
    This is a Man's World ; PMJ, Morgan James ; mPimt0Zu_To ; 
    Vltava (The Moldau) ; Smetana ; l6kqu2mk-Kw ; 
    Volga Boatmen ; ; qsovBF4N27Q ;

'''
dead_urls = '''

    Bad Bad Leroy Brown ; Jim Croce ; CIiVindRSTA ; 
    Beethoven: Für Elise ; ; _mVW8tgGY_w ; 
    Dueling Banjos ; Deliverance movie ; myhnAZFR1po ; 
    Fever ; Peggy Lee ; JGb5IweiYG8 ; 
    Georgia On My Mind ; Ray Charles ; QL3EZwSJAh0 ; 
    Hot Rod Lincoln ; ; 3R7l7nDuj1o ; 
    I Will Survive ; ; ARt9HV9T0w8 ; 
    Jumpin' Jack Flash ; Rolling Stones ; -rIG2POqtV8 ; 
    Mack the Knife ; Bobby Darin ; SEllHMWkXEU ; 
    The Night the Lights Went Out in Georgia ; Vicki Lawrence ; wMD5nBcPrCk ; 
    White Rabbit ; Jefferson Airplane ; EUY2kJE0AZE ; 

'''
songs = '''

    100 lbs of Clay ; Gene McDaniels ; rUGonj90b5I ;
    16 Tons ; Tennessee Ernie Ford ; jIfu2A0ezq0 ; 
    25 Or 6 To 4 ; Chicago ; iUAYeN3Rp2E ; Great horns and guitar
    A Horse With No Name ; America ; mSZXWdKSQNM ; 
    A World of our Own ; Seekers ; PSxwqBJLU8A ; 
    Africa ; Toto ; qDLJ3pUZm9A ; 
    All Out of Love ; Air Supply ; https://www.youtube.com/watch?v=tH2w6Oxx0kQ ; 
    American Pie ; Don Maclean ; iX_TFkut1PM ; 
    Angel of the Morning ; ; https://www.youtube.com/watch?v=HTzGMEfbnAw ; 
    Aquarius ; Fifth Dimension ; oPK7ZF6jfJE&t=8 ; 
    Ballad Of Cat Ballou ; Nat King Cole and Stubby Kaye; -ghnpUNTR1I ; 
    Barracuda ; Heart ; PeMvMNpvB5M ; 
    Bay Of Mexico ; Kingston Trio ; -16OczraVi4 ; 
    Beat It ; Michael Jackson ; oRdxUFDoQe0 ; 
    Big John ; ; KnnHprUGKF0 ; 
    Blowin' in the Wind ; Peter, Paul, and Mary ; Ld6fAO4idaI ; 
    Blue World ; Moody Blues ; 8a9bfvNuTw0 ; With lyrics
    Blue World ; Moody Blues ; oosjl8wNLJU ; 
    Bolero; Danish National Symphony; 3T92rCMQOMI ; 
    Boogie Woogie Bugle Boy ; Andrew Sisters ; 8of3uhG1tCI ; 
    Both Sides Now ; Judy Collins ; 8L1UngfqojI ; 
    Brandy ; Looking Glass ; CFhFyvk0yS8 ;
    Bucket drummer ; ? ; FqJdzYY_Fas ; 
    Build Me Up Buttercup ; The Foundations ; w0kLkDCoRXc ;
    Bus Stop ; Hollies ; It75wQ0JypA ; 
    Carpool karaoke ; Paul McCartney ; QjvzCTqkBDQ ; 
    Classical Gas ; Mason Williams ; PRZkc88uNXo ; 
    Country Roads ; John Denver ; 1vrEljMfXYo ; 
    Country Roads ; Petersens ; qap9Qm-Q894 ; Petersens
    Crocodile Rock ; Elton John ; 75r0nQu-hMs ; 
    Different Drum ; Stone Pony ; w9qsDgA1q8Y ; 
    Doc & San Miguel 5 ; Doc Severinsen and Arturo Sandoval ; s53B0PyAEOE ; Great trumpets & guitar, but the violin is best
    Downtown ; Petula Clark ; Zx06XNfDvk0 ; 
    Dream Lover ; Bobby Darin ; wVHAQX5sSaU ; 
    Dreams ; Fleetwood Mac ; O5ugW4-BstE ; 
    Drive My Car ; Beatles ; kfSQkZuIx84 ; 
    Dust in the Wind ; Kansas ; tH2w6Oxx0kQ ; 
    Early In The Morning ; Vanity Fare ; 9hN9YRo7y1s ;
    Easy Lover ; Phil Collins ; 2aJ2Vh_e2dQ ; 
    El Condor Pasa ; Simon & Garfunkel ; pey29CLID3I ; 
    El Paso ; Marty Robbins ; -zBzZJd-nfw ; 
    Eli's coming ; Three Dog Night ; 1A2eet1bttY ; Also look up writer's Laura Nyro's version.
    End of the World ; Skeeter Davis ; sonLd-32ns4 ; 
    Even the Nights Are Better ; Air Supply ; https://www.youtube.com/watch?v=BRx58DgOxeg ; 
    Everybody's Somebody's Fool ; Connie Francis ; ECOthzFvUXY ; 
    Exodus ; Ferranti & Teicher ; xhXZ3eXJIFc ; 
    Eye Of The Tiger ; Survivor ; btPJPFnesV4 ; 
    Eye in the Sky ; Alan Parsons Project ; 56hqrlQxMMI ; 
    Fast Freight ; Kingston Trio ; Oy_NkJOwRqE ; 
    Flight of the Condor ; BBC TV show ; 66KVAhNE_rQ ; This was a 1982 BBC TV show and had great pan pipe music from South America.
    Foggy Mountain Breakdown ; Flatt & Scruggs ; z_Y3mnj-8lA ; 
    For What It's Worth ; Buffalo Springfield ; gp5JCrSXkJY ; 
    Für Elise ; ; 2fcX2dWmR6g ; 
    Games People Play ; Alan Parsons Project ; SLi7Ljcy6n8 ; 
    Ghost Riders In the Sky ; Burl Ives ; j2klh2cTa_Q ; 
    Ghost Riders In the Sky ; Frankie Laine ; ZwAPa0qHmLo ; 
    Ghost Riders In the Sky ; Highwaymen ; nOWjX4BpC24 ; 
    Ghost Riders In the Sky ; Marty Robbins ; fD5kS3G1Jkk ; 
    Ghost Riders In the Sky ; Roy Clark & Glen Campbell ; v_kbgjsuCec ; 
    Ghost Riders In the Sky ; Roy Clark ; 8o2w1zhBKzk ; 
    Girl drummer ; ; L-So4DLDvGc ; 
    Gypsy ; Fleetwood Mac ; mwgg1Pu6cNg ; 
    Gypsy Waltz ; Sally ; eDGE6ah-e4Y ; 
    Hair ; Cowsills ; BFy-yzj02FE ; 
    Hallelujah ; Lucy Thomas ; dLk9pzmaFHY ;
    Hang 'Em High ; Movie theme ; 0gscut1p4kY ; 
    Hava Nagila ; Dalida ; YBj2PZ1IeIc ; 
    Hawaii 50 ; TV show theme ; AepyGm9Me6w ; 
    Heart Full of Soul ; Yardbirds ; pM1qZBFiOLU ; 
    Heart of Gold ; Neil Young ; X3IA6pIVank ; 
    Hey Jude ; Beatles ; mQER0A0ej0M ; 
    Hit the Road Jack ; Ray Charles ; SrnWp5O0DEs ;
    Hotel California ; Eagles ; BciS5krYL80 ; 
    House Of The Rising Sun ; Animals ; MJkr0DWbhTk ; 
    How Blue Can You Get? ; B.B. King ; LWLAAzOBoBI ; A masterpiece
    I Am A Man Of Constant Sorrow ; Movie song ; OdYGnAFaeHU ; 
    I Left My Heart in San Francisco ; Tony Bennett ; SC73kdOL5hk ; 
    I love the flower girl ; Cowsills ; dZMc0-ZAUeY ; 
    I was Born Under a Wandering Star ; Lee Marvin ; NTymtAbaG08 ; 
    I'm Just A Singer in a Rock And Roll Band ; Moody Blues ; 5UZWXE76ELU ; Album
    I'm Just a Singer in a Rock and Roll Band ; Moody Blues ; s5tb25TqXYU ; Concert
    I'm Still Standing ; Elton John ; Ye9hGotPPVk ; 
    Ievan Polkka ; Loituma ; Zcg66Qcwjw8 ; 2021
    In Hell I'll be in Good Company ; Dead South ; B9FzVhw8_bY ; 
    In The Year 2525 ; Zager &  Evans ; yesyhQkYrQM ; 
    Indian Lake ; Cowsills ; 3Xup3HSZLIQ ; Bubble rock
    Isn't Life Strange ; Moody Blues ; 9WZZjXgJ4W8 ; 
    It Was A Very Good Year ; Frank Sinatra ; CJARjwzmceg ; 
    It's a Heartache ; Bonnie Tyler ; bEOl38y8Nj8 ; 
    Jailhouse Rock ; Elvis Presley ; A99sV18J0mk ; 
    Johnny B. Goode ; Chuck Berry ; Uf4rxCB4lys ; 
    Journey to Kilimanjaro ; Nova TV show ; 5ZFJWIGN9zQ ; 1994 Melodically simple but haunting music:  0:48, 6:43, 9:28, 10:44, 30:07, 35:27, 37:33, 38:14*, 43:45, 50:42, 53:00(credits),
    Judy Blue Eyes (1969) ; Crosby, Stills, and Nash ; cMJug2iz3NA ; 1969
    Judy Blue Eyes (2012) ; Crosby, Stills, and Nash ; XWvw_uZPGDA ; 
    Kisses Sweeter Than Wine ; Marty Robbins ; iulmZAz8XfY ; 
    Kodachrome ; Paul Simon ; 8rlDTK6QI-w ; 
    Korobushka ; Bond ; vvC2vjtmUX8 ; 
    Land Down Under ; Men at Work ; 8jHXu86O01w ; 
    Les Bicyclettes De Belsize ; Englebert Humperdinck ; Qe_1B1P9Bw4 ; 
    Light My Fire ; Doors ; LY1l8T2Lcl0 ; 
    Listen To Your Heart ; Roxette ; yCC_b5WHLX0 ; 
    Long Cool Woman ; Hollies ; g8XiNKsKyVk ; 
    Love Me With All Your Heart ; Ray Charles Singers ; k3nfqH4YDDM ; 
    Love is Blue ; Paul Muriat ; YYf_hb-jsGo ; 
    MTA ; Kingston Trio ; MbtkL5_f6-4 ; 
    MacArthur Park ; Richard Harris ; iplpKwxFH2I ; 
    Maggie May ; Rod Steward ; EOl7dh7a-6g ; 
    Magnificent Seven ; Movie theme ; 8XDB7GMnbUQ ; 
    Making Love Out of Nothing at All ; Air Supply ; https://www.youtube.com/watch?v=JMKi9qVrGWM ; 
    Mambo Italiano ; Rosemary Clooney ; 9prJXEhNhPA ; 
    Me & Bobby McGee ; Janis Joplin ; WXV_QjenbDw ; 
    Memories (from Cats); Barbra Streisand ; MWoQW-b6Ph8 ; 
    Memories (from Cats); Betty Buckley ; 5mlllRdIfqw ; 
    Memories (from Cats); Elaine Paige ; mdBVJbzkoqo ; 
    Midnight In Moscow ; Sweet & Hot 2011 ; FY3Zr5Tj5zw ; 2011
    Morningtown Ride ; Seekers ; M-RkC6MYT2E ; 1964
    Morningtown Ride ; Seekers ; wqdaCOt51Dk ; 2014
    Mr. Roboto ; Styx ; 51ybp_YFo7I ; 
    Mrs. Robinson ; Simon & Garfunkel ; _C2vqI9FVwg ; 
    My Sweet Lord ; George Harrison ; AR4lpQWcT5g ; 
    Nancy Sinatra and Lee Hazelwood: Lady Bird ; Nancy Sinatra and Lee Hazelwood ; FIPQVpw-zkk ; 
    Nancy Sinatra and Lee Hazelwood: Summer Wine ; Nancy Sinatra and Lee Hazelwood ; Ib_eW9VSUwM ; 
    North to Alaska (1960) ; Johnny Horton ; RO6IU9RpjS8 ; 
    Nothing Else Matters ; Metallica ; tAGnKpE4NCI ; 
    Nothing Else Matters ; PMJ, 15 year old girl singer ; KSSa0-oAnIo ; 
    Nothing Else Matters: Banjo & Mandolin ; ; 3JFb_aOn6rc ; 
    Nothing Else Matters: Guitar & cello ; ; pxoW-00Zyho ; 
    Nothing Else Matters: Guitar ; ; WlGiOiRQNhI ; 
    Nothing Else Matters: Hammered dulcimer ; ; 8KK0-9Moz5Q ; 
    Nothing Else Matters: Hardpan ; ; 32v8ARqaBas ;
    Nothing Else Matters: Harp ; ; KMX2bmtS_TE ; 
    Nothing Else Matters: Piano ; ; DmL12NRE4hQ ; 
    Old Man ; Neil Young ; rAtDrFdomN4 ; 
    Old and Wise ; Alan Parsons Project ; ZmzqqdVFw8g ; 
    One ; Three Dog Night ; UiKcd7yPLdU ; 
    Orange Blossom Special ; Sally ; 6-5xPixiCkI ; 
    Paint It Black ; Rolling Stones ; O4irXQhgMqg ; 
    Papa Was a Rollin' Stone ; Temptations ; 71l85z2bXAs ; 
    Paperback Writer ; Beatles ; yYvkICbTZIQ ; 
    Papillon ; Movie theme ; Js69DkyaDVQ ; 
    Patricia ; ; rTXIXkeWnEo ; 
    Penny Lane ; Beatles ; S-rB0pHI9fU ; 
    People ; Barbra Streisand ; fPlQ6EtArSc ; 
    Pirates of the Caribbean ; Movie theme ; 27mB8verLK8 ; 
    Popcorn Song ; ; DBYjZTdrJlA ; 
    Purple People Eater ; Sheb Wooley ; Rx47qrH1GRs ; 
    Push It To The Limit ; Movie theme ; 9D-QD_HIfjA ; 
    Puttin' on the Ritz ; Berlin Brass Quintet ; oQVR-fnyM3o ;
    Que Sera Sera ; Doris Day ; xZbKHDPPrrc ; 
    Queen of Hearts ; Juice Newton ; P0DK-0fIKCw ; 
    Question ; Moody Blues ; tmOZFAYeurY ; 
    Rainy Days and Monday ; Carpenters ; PjFoQxjgbrs ; 
    Rainy Night in Georgia ; Brook Benton ; bDRbF80NKDU ; 
    Rawhide ; Frankie Laine ; _EjbzCX3enA ; 
    Ray Charles:  Cincinnati Kid ; Ray Charles ; rfn1YrwG2Oc ; 
    Ride My See-saw ; Moody Blues ; GXHMTuoK060 ; 
    Rocket Man ; Elton John ; BdEe5SpdIuo ; 
    Run Through The Jungle ; Creedence Clearwater ; EbI0cMyyw_M ; 
    Runaround Sue ; Dion ; nFch8vH81ks ;
    Sally Goodin ; Sally ; nbYBBeylfGk ; My second-favorite fiddle song
    Scarborough Fair ; Simon & Garfunkel ; -BakWVXHSug ; 
    Scat singing ; Ella Fitzgerald & Mel Torme ; 9CbVy1NnB4g ; 
    She Works Hard for the Money ; Donna Summers ; 09ZSKE38lTU ; 
    She's Got You ; Petersens ; 7nXPQbKZBbw ; 
    Shrek Hallelujah ; Rufus Wainright ; EbO6P-_Zx0Y ; 
    Silver Threads and Golden Needles ; Dusty Springfield ; uz6HB9HYQz4 ; Dusty Springfield
    Sounds of Silence ; Simon & Garfunkel ; 4zLfCnGVeL4 ; 
    Stairway to Heaven (concert) ; Led Zeppelin ; BciS5krYL80e ; 
    Stairway to Heaven ; Heart ; 2cZ_EFAmj08 ; 
    Stairway to Heaven: Harp ; ; wLiH6F82t_U ; 
    Struttin' With Some Barbecue ; Louis Armstrong ; yl-2R_Pb7dk ; 
    Sunrise, Sunset ;  ; 03rzUoyq9K0 ;
    Sunrise, Sunset ; Bette Midler ; QD8u-fjQnFs ;
    Superstar ; Carpenters ; SJmmaIGiGBg ; 
    Suzy Q ; Creedence Clearwater ; 7x60p7UNLnQ ; 
    Sweet Dreams ; Eurythmics ; qeMFqkcPYcg ; 
    Take Five ; Dave Clark Five ; vmDDOFXSgAs ; 
    The Boxer ; Simon & Garfunkel ; C1VUWDcp5Sg ; 
    The Crystal Ship ; Doors ; bU1sLx1tjPY ; 
    The Gambler ; Kenny Rogers ; 7hx4gdlfamo ; 
    The Little Nash Rambler ; Playmates ; enqNl7tdLR4 ; 
    The Night They Drove Old Dixie Down ; Joan Baez ; wanJQC5KAfo ; 
    The Thrill is Gone ; B.B. King ; Nu4tjTyqbho ; 
    The Voice ; Moody Blues ; -umqM9R8cnI ; 
    The Wreck of the Edmund Fitzgerald ; Gordon Lightfoot ; 9vST6hVRj2A ; 
    Theme From Shaft ; Isaac Hayes ; Q429AOpL_ds ; 
    These Boots Are Made for Walkin' ; Nancy Sinatra ; rypT2qMO1RY ; 
    They Call the Wind Mariah ; Harv Presnel ; ByqYEzugleE ;
    They Call the Wind Mariah ; Smothers Brothers ; wFHh0Rs34v0 ;
    This is a Man's World ; James Brown ; wd1-HM234DE ; 
    Those Were The Days ; Mary Hopkins ; y3KEhWTnWvE ; 
    Time Won't Let Me ; Outsiders ; 3yQERVphWhY ; 
    Today (1964) ; Christy Minstrels ; 3cELsUMcQdc ; 
    Torn Between Two Lovers ; ; TzGbvTl4mpg ; 
    Total Eclipse of the Heart ; Bonnie Tyler ; lcOxhH8N3Bo ; 
    Tuxedo Junction ; Mary MacGregor ; iBTYcqtaOjg ; 
    Two Faces Have I ; Lou Christie ; w05w1XbZTG8 ; 
    The Good, the Bad and the Ugly ; The Ukelele Orchestra of Great Britain ; pLgJ7pk0X-s ;
    Unchained Melody ; Righteous Brothers ; m0EBs6uRgtw ; 
    Unforgettable ; Nat King Cole ; Fy_JRGjc1To ; 
    Unknown song ; Sally ; ob44BR1Hurg ; 
    Unsquare Dance ; Dave Clark Five ; lbdEzRfbeH4 ; 
    Victory ; Bond ; j3nBuwOPu8A&list=RDE5NByiEIbD8 ; 
    Volga Boatmen  ; Red Army Choir & Band ; yfO0ADduEr8 ; 1996
    Volga Boatmen ; L. Kharitonov ; 0tw3g88JtWA ; 1965 
    Walk On the Wild Side ; Walk on the Wild Side ; 5O82y59h7MI ; 
    Walking in the Air ; Malakai Bayoh & Aled Jones ; Lq8kqsI3hCo ; Movie theme sung by a 13 year old choirboy
    Walking in the Air ; Walking In the Air movie ; upH1QZU4Z0Y ; Movie theme sung by a 13 year old choirboy Aled Jones
    Wanderer ; Dion ; SbYa7NBYyRc ;
    Washington Square ; Village Stompers ; ihenbyTzQ2A ; 
    White Silver Sands ; Don Rondo ; mOqbjENGN7s ; 
    Who's on First ; Abbott & Costello ; jIGRgmxRfiE ; Genius comedy
    Woman in Love ; Barbra Streisand ; hQLGCX8D-1Y ; 
    Yesterday When I was Young ; Roy Clark ; GQIAcztYjbc ; 
    You Only Live Twice ; Nancy Sinatra ; XgFtQPgHyek ; 
    You Were On My Mind ; We Five ; c7YSANg8vgw ; 
    You'll Never Know ; Ralna English ; 4HU8I9BY1H0 ; 
    You're So Vain ; Carly Simon ; cleCtBP0o5Y ; 
    Your Wildest Dreams ; Moody Blues ; kmmPFrkuPq0 ; 

    Rimsky-Korsakov:  Scheherazade ; ; 1i6TsIVKByM ; Excellent youth orchestra
    Barber of Seville (1821) ; ; OloXRhesab0 ; Most of us probably heard this first by watching Saturday morning cartoons.
    Ravel: Bolero ; ; 8KsXPq3nedY ; 
    Beethoven: Moonlight Sonata (3rd) ; ; zucBfXpCA6s ; Valentina Lisitsa
    Beethoven:  2nd movement 9th ; ; p5favl2Qtx0 ; Player-piano type visual
    Beethoven: Moonlight Sonata ; ; 4Tr0otuiQuU ; 
    Beethoven's 9th ; ; fRZaX6-dsn8 ; 
    Beethoven's 5th ; ; 1lHOYvIhLxo ; 
    Beethoven's 5th ; ; Zev0ran0iuU ; NY Philharmonic
    Beethoven's 7th ; ; W5NsPOgyALI ; 
    Dvorak:  New World Symphony (Dvorak's 9th 1893) ; ; O_tPb4JFgmw ; 
    New World Symphony and The Moldau ; ; Qut5e3OfCvg ; Slovak Philharmonic
    Tchaikovsky:  1812 Overture (1888) ; ; QUpuAvQQrC0 ; 

    Bach: Toccata and Fugue in D Minor: Violin ; ; JL0PCLMSQms ; Violin
    Bach: Toccata and Fugue in D Minor ; ; eDFFUIGoBUc ; Accordion
    Bach: Toccata and Fugue in D Minor ; ; ho9rZjlsyYY ; Organ
    Bach: Toccata and Fugue in D Minor ; ; i9UQ61EbdO0 ; Orchestra
    Bach: Toccata and Fugue in D Minor ; ; ipzR9bhei_o ; Organ with bar graph score
    Bach: Toccata and Fugue in D Minor ; ; ojBYW3ycVTE ; Guitar
    Bach: Toccata and Fugue in D Minor ; ; zhH53UODLEM ; Piano with visual score

'''
if 1:   # Functions
    def Check(line):
        '''Split on the field separator and check the that line has the requisite fields.'''
        f = line.split(";")
        if len(f) != 4:
            t.print(f"{t.ornl}Bad line (missing 4 fields, separator is ';'):\n    {t.lil}{line!r}")
            exit(1)
    def Validate():
        "Check that all the lines have the proper form"
        for item in (favorites, songs):
            for line in GetTextLines(item):
                if not line or line.strip()[0] == "#":
                    continue
                Check(line)
    def CheckLinks(url):
        pass
    def Print(entries):
        # namedtuple("Entry", "title artist url comment")
        for i in sorted(entries):
            if i.artist:
                print(f'<a href="{i.url}">{i.title}</a> [{i.artist}] {i.comment} <br>')
            else:
                print(f'<a href="{i.url}">{i.title}</a> {i.comment} <br>')
    def ValidateURL(entry):
        if not validate:
            return
        global validated_OK
        r = requests.get(entry.url)
        # This is a heuristic that looks for the string "This video isn't available
        # anymore", indicating the url is no longer valid.
        s = "This video isn't available anymore"
        if s in r.text:
            url = entry.url.replace("https://www.youtube.com/watch?v=", "")
            print(f"\n{entry.title!r} {url!r} not available")
            validated_OK = False
        else:
            # Just print a "." to indicate we're still working
            print(end=".")
    def Get(container):
        '''Return a list of Entry instances:  each item is a named tuple with
        components title, artist, url, comment.
        '''
        o = []
        for line in container.split("\n"):
            line = line.strip()
            if not line or line[0] == "#":
                continue
            # Split the line on ';' as the field separator
            title, artist, url, comment = [i.strip() for i in line.split(";")]
            # If the URL doesn't start with "https://", construct it
            if not url.startswith("https://"):
                url = "https://www.youtube.com/watch?v=" + url
            entry = Entry(title, artist, url, comment)
            o.append(entry)
            ValidateURL(entry)
        return o

if __name__ == "__main__":
    # If the command line has an argument, validate the URLs
    validate = len(sys.argv) > 1
    if 1:   # Get the song URLs and validate them
        validated_OK = True
        favorites_list = Get(favorites)
        song_list = Get(songs)
        if not validated_OK:
            exit(1)
        now = iso.ISO()
    print("Favorites:</p>")
    Print(favorites_list)
    print("<p>Others:</p>")
    Print(song_list)
    if 0:
        print(f"<p>Updated {now.date}<p>")
# vim: tw=0 wm=0
