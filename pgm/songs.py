from get import GetTextLines
import sys
import time
import iso
from pdb import set_trace as xx 
if 1:
    import debug
    debug.SetDebugger()
 
favorites = '''

Beethoven's 7th, 2nd movement|sv2QnrCJNk0|
Beethoven's 9th, 2nd movement (1824)|iwIvS4yIThU|Genius
Bad Romance|VCTOpdlZJ8U|PMJ & tap dancing (Sarah Reich) (singer is Telly Savalas' daughter)
Catharsis (2013)|h3hlFAVV6aI|My beloved Sa-Sa|  Sally went to a fiddle camp in WA and learned this song.  When she returned, she said she knew I'd like it.  She was right, as it's my favorite fiddle song.
Crazy (1961)|MbnrdCS57d0||Nobody sings it like Patsy Cline.
Diamonds and Rust (1975)|2MSwBM_CbyY|Baez's best
Don't Cry For Me Argentina (1977)|_n8mq7sedP4|A masterpiece
I'll Never Find Another You (1963)|KmactMIhrRM|How I feel about Glenda
Midnight In Moscow (1961)|o744d4mwOgQ|Dixieland from England
Potato Head Blues (1927)|EfGZB78R7uw|Famous trumpet solo
Scheherezade (1st movement, written 1888)|6dDk6aft4JU|von Karajan on Deutsche Grammophone
Stairway to Heaven (1971)|QkF3oxziUI4|
Vltava (The Moldau) (1875)|l6kqu2mk-Kw|Smetana (he was deaf when he wrote this)

'''

songs = '''

#Flight of the Condor|66KVAhNE_rQ|1982| This was a BBC TV show and had great pan pipe music from South America.
#Hot Rod Lincoln|3R7l7nDuj1o|
#Jefferson Airplane: White Rabbit|EUY2kJE0AZE|
#Journey to Kilimanjaro|e0DpZ3WVowY|1994 Nova show.  Melodically simple but haunting music:  1:20, 4:15, 8:10, 12:03, 19:40, 22:08, 36:50, 38:46, *39:34, 44:58, 51:57, 54:15 (credits)

The Dead South:  In Hell I'll be in Good Company|B9FzVhw8_bY|
The Dead South:  People Are Strange|4YQJ6KuWvQ|
The Dead South:  You Are My Sunshine|4YQJ6KuWvQ|
The Dead South:  House of the Rising Sun|4YQJ6KuWvQ|
5th Dimension:  Aquarius|oPK7ZF6jfJE&t=8|
A Horse With No Name|mSZXWdKSQNM|
Abbott and Costello: Who's on First|kTcRRaXV-fg|Genius comedy
Air Supply:  All Out of Love|https://www.youtube.com/watch?v=tH2w6Oxx0kQ|
Air Supply:  Even the Nights Are Better|https://www.youtube.com/watch?v=BRx58DgOxeg|
Air Supply:  Making Love Out of Nothing at All|https://www.youtube.com/watch?v=JMKi9qVrGWM|
Andrew Sisters:  Boogie Woogie Bugle Boy|8of3uhG1tCI|
Angel of the Morning|https://www.youtube.com/watch?v=HTzGMEfbnAw|
Animals: House Of The Rising Sun|MJkr0DWbhTk||I loved this song in high school.
B.B. King: How Blue Can You Get?|LWLAAzOBoBI|A masterpiece
B.B. King: The Thrill is Gone|Nu4tjTyqbho|
Bad Bad Leroy Brown|CIiVindRSTA|
Beatles:  Drive My Car|kfSQkZuIx84|
Beatles:  Paperback Writer|yYvkICbTZIQ|
Beatles:  Penny Lane|S-rB0pHI9fU|
Beatles: Hey Jude|mQER0A0ej0M|
Big John|KnnHprUGKF0|
Blowin' in the Wind|Ld6fAO4idaI|
Bobby Darin:  Dream Lover|wVHAQX5sSaU|
Bobby Darin:  Mack the Knife|SEllHMWkXEU|
Bond: Victory|j3nBuwOPu8A&list=RDE5NByiEIbD8|
Brook Benton: Rainy Night in Georgia|bDRbF80NKDU|
Bucket drummer|FqJdzYY_Fas|
Buffalo Springfield:  For What It's Worth|gp5JCrSXkJY|
Carly Simon: You're So Vain|cleCtBP0o5Y|
Carpenters:  Rainy Days and Monday|PjFoQxjgbrs|
Carpenters: Superstar|SJmmaIGiGBg|
Chicago:  25 Or 6 To 4|iUAYeN3Rp2E|Great horns and guitar|This reminds me of visiting a friend in Chicago in the early 1970's and he took me to a place where this band played, although they weren't there.
Christy Minstrels: Today (1964)|3cELsUMcQdc|
Connie Francis:  Everybody's Somebody's Fool|ECOthzFvUXY|
Country Roads:  John Denver|1vrEljMfXYo|
Country Roads:  Petersens|qap9Qm-Q894|Petersens
Cowsills: Hair|BFy-yzj02FE|
Cowsills: I love the flower girl|dZMc0-ZAUeY|
Cowsills: Indian Lake|3Xup3HSZLIQ|Bubble rock
Creedence Clearwater: Run Through The Jungle|EbI0cMyyw_M|
Creedence Clearwater: Suzy Q|7x60p7UNLnQ|
Crosby, Stills, and Nash: Judy Blue Eyes (1969)|cMJug2iz3NA|1969
Crosby, Stills, and Nash: Judy Blue Eyes (2012)|XWvw_uZPGDA|
Dalida:  Hava Nagila|https://www.youtube.com/watch?v=YBj2PZ1IeIc|
Dave Clark Five:  Take Five|vmDDOFXSgAs|
Dave Clark Five:  Unsquare Dance|lbdEzRfbeH4|
Doc Severinsen and Arturo Sandoval|s53B0PyAEOE|Great trumpets & guitar, but the violin is best
Don Maclean:  American Pie|iX_TFkut1PM|
Don Rondo: White Silver Sands|mOqbjENGN7s|
Doors:  Light My Fire|LY1l8T2Lcl0|
Doors:  The Crystal Ship|bU1sLx1tjPY|
Dueling Banjos|myhnAZFR1po|
Dusty Springfield: Silver Threads and Golden Needles|uz6HB9HYQz4|
Eagles: Hotel California|https://www.youtube.com/watch?v=BciS5krYL80|
El Condor Pasa|pey29CLID3I|
Ella Fitzgerald scat singing|9CbVy1NnB4g|
Elton John:  Crocodile Rock|75r0nQu-hMs|
Elton John: I'm Still Standing|Ye9hGotPPVk|
Elton John: Rocket Man|BdEe5SpdIuo|
Eurythmics: Sweet Dreams|qeMFqkcPYcg|
Fast Freight:  Eliza Gilkyson|Sin3FeAQAws| Eliza Gilkyson (song writer's daughter)
Fast Freight:  Kingston Trio|Oy_NkJOwRqE||This has always been a favorite Kingston Trio song of mine.  I used to mentally sing it in my mind many times when driving back from fiddle contests when Sally was young.
Ferrante & Teicher:  Exodus|xhXZ3eXJIFc|
Flatt & Scruggs:  Foggy Mountain Breakdown|z_Y3mnj-8lA|
Fleetwood Mac:  Dreams|O5ugW4-BstE|
Fleetwood Mac: Gypsy|mwgg1Pu6cNg|
Frank Sinatra:  It Was A Very Good Year|CJARjwzmceg|
George Harrison: My Sweet Lord|AR4lpQWcT5g|
Ghost Riders In the Sky: Burl Ives (1949)|j2klh2cTa_Q|
Ghost Riders In the Sky: Frankie Laine|ZwAPa0qHmLo|
Ghost Riders In the Sky: Highwaymen (1990)|nOWjX4BpC24|
Ghost Riders In the Sky: Marty Robbins|fD5kS3G1Jkk|
Girl drummer|L-So4DLDvGc|
Gordon Lightfoot:  The Wreck of the Edmund Fitzgerald|9vST6hVRj2A|
Hang 'Em High Movie Theme|0gscut1p4kY|
Harve Presnell: They Call the Wind Mariah|ByqYEzugleE|
Hawaii 50 Theme|AepyGm9Me6w|
Heart:  Barracuda|PeMvMNpvB5M|
Hit the Road Jack: Becca Krueger|OfUDsHtSv88|(skip first 20 seconds)
Hit the Road Jack: Ray Charles|SrnWp5O0DEs|
Hollies:  Long Cool Woman|X3sU_q1GH-4|
Hollies: Bus Stop|It75wQ0JypA|
I Am A Man Of Constant Sorrow|OdYGnAFaeHU|
I Will Survive|ARt9HV9T0w8|
Ievan Polkka|4om1rQKPijI|A masterpiece of a capella
It's a Heartache|https://www.youtube.com/watch?v=bEOl38y8Nj8|
Jimmy Rodgers:  Kisses Sweeter Than Wine|iulmZAz8XfY|
Jimmy Smith:  Walk On the Wild Side|5O82y59h7MI|
Joan Baez: The Night They Drove Old Dixie Down|wanJQC5KAfo|
Johnny Horton: North to Alaska (1960)|RO6IU9RpjS8|
Judy Collins:  Both Sides Now|8L1UngfqojI|
Kansas:  Dust in the Wind|tH2w6Oxx0kQ|
Kenny Rogers:  The Gambler|https://www.youtube.com/watch?v=7hx4gdlfamo|
Kingston Trio:  Bay Of Mexico|-16OczraVi4|
Kingston Trio: MTA|MbtkL5_f6-4|
Korobushka: Bond Live at Albert Hall|E5NByiEIbD8|
Korobushka: Bond Live at Albert Hall|vvC2vjtmUX8|
Korobushka: Mikhail Smirnov|Pr3ZgN8onRA|Mikhail Smirnov
Lee Marvin: I was Born Under a Wandering Star|NTymtAbaG08|
Listen To Your Heart|yCC_b5WHLX0|
Lou Christie:  Two Faces Have I|w05w1XbZTG8|
Louis Armstrong: Struttin' With Some Barbecue|yl-2R_Pb7dk|
MacArthur Park|iplpKwxFH2I|
Maggie May|EOl7dh7a-6g|
Magnificent Seven (1960)|8XDB7GMnbUQ|
Marty Robbins:  El Paso|-zBzZJd-nfw|
Mary Hopkins: Those Were The Days|y3KEhWTnWvE|
Mary MacGregor: Torn Between Two Lovers|TzGbvTl4mpg|
Mason Williams:  Classical Gas|PRZkc88uNXo|
Me & Bobby McGee|WXV_QjenbDw|
Memories (from Cats): Betty Buckley|5mlllRdIfqw|
Memories (from Cats): Elaine Paige|mdBVJbzkoqo|
Memories (from Cats): Streisand|MWoQW-b6Ph8|
Men At Work:  Land Down Under|8jHXu86O01w|
Michael Jackson:  Beat It|oRdxUFDoQe0|
Midnight In Moscow|FY3Zr5Tj5zw|2011
Moody Blues:  Blue World|8a9bfvNuTw0|With lyrics
Moody Blues:  Blue World|oosjl8wNLJU|
Moody Blues:  I'm Just A Singer in a Rock And Roll Band|5UZWXE76ELU|Album
Moody Blues:  I'm Just a Singer in a Rock and Roll Band|s5tb25TqXYU|Concert
Moody Blues:  Isn't Life Strange|9WZZjXgJ4W8|
Moody Blues:  Question|tmOZFAYeurY|
Moody Blues:  Ride My See-saw|GXHMTuoK060|
Moody Blues:  Your Wildest Dreams|kmmPFrkuPq0|
Moody Blues: The Voice|-umqM9R8cnI|
Nancy Sinatra and Lee Hazelwood: Lady Bird|FIPQVpw-zkk|
Nancy Sinatra and Lee Hazelwood: Summer Wine|Ib_eW9VSUwM|
Nancy Sinatra: These Boots Are Made for Walkin'|rypT2qMO1RY|
Nancy Sinatra: You Only Live Twice|XgFtQPgHyek|
Neil Young:  Old Man|rAtDrFdomN4|
Neil Young: Heart of Gold|X3IA6pIVank|
Nothing Else Matters: Banjo & Mandolin|3JFb_aOn6rc|
Nothing Else Matters: Guitar & cello|pxoW-00Zyho|
Nothing Else Matters: Hammered dulcimer|8KK0-9Moz5Q|
Nothing Else Matters: Hardpan|32v8ARqaBas|
Nothing Else Matters: Harp|KMX2bmtS_TE|
Nothing Else Matters: Metallica|tAGnKpE4NCI|
Nothing Else Matters: PMJ:  15 year old girl singer|KSSa0-oAnIo|
Nothing Else Matters: Piano|DmL12NRE4hQ|
Papillon: Movie theme|Js69DkyaDVQ|
Papillon: Waltz arrangement|https://www.youtube.com/watch?v=FKrmozFh5ww|
Patricia: Perez Prado|rTXIXkeWnEo|
Paul McCartney carpool karaoke|QjvzCTqkBDQ|
Paul Muriat: Love is Blue|YYf_hb-jsGo|
Paul Simon:  Kodachrome|8rlDTK6QI-w|
Peggy Lee: Fever|JGb5IweiYG8|
Petersens: She's Got You|7nXPQbKZBbw|
Petula Clark:  Downtown|Zx06XNfDvk0|
Phil Collins:  Easy Lover|2aJ2Vh_e2dQ|
Pirates of the Caribbean|27mB8verLK8|
Pirates of the Caribbean|6zTc2hD2npA|Auckland Symphony
Popcorn Song|DBYjZTdrJlA|
Purple People Eater|Rx47qrH1GRs|
Push It To The Limit|9D-QD_HIfjA|
Queen of Hearts|https://www.youtube.com/watch?v=P0DK-0fIKCw|
Rawhide|_EjbzCX3enA|
Ray Charles Singers:  Love Me With All Your Heart|k3nfqH4YDDM|
Ray Charles:  Cincinnati Kid|rfn1YrwG2Oc|
Ray Charles:  Georgia On My Mind|QL3EZwSJAh0|
Rolling Stones:  Angie|S7sigwbqEj8|
Rolling Stones:  Jumpin' Jack Flash|-rIG2POqtV8|
Rolling Stones:  Paint It Black|O4irXQhgMqg|
Rosemary Clooney: Mambo Italiano|9prJXEhNhPA|
Roy Clark: Yesterday when I was young|GQIAcztYjbc|
Sally:  Gypsy Waltz|eDGE6ah-e4Y|
Sally:  Orange Blossom Special|6-5xPixiCkI|
Sally:  Sally Goodin|nbYBBeylfGk||My second-favorite fiddle song
Sally:  Unknown song|ob44BR1Hurg|
Seekers:  A World of our Own|PSxwqBJLU8A|
Seekers: Morningtown Ride|M-RkC6MYT2E|1964
Seekers: Morningtown Ride|wqdaCOt51Dk|2014
She Works Hard for the Money|09ZSKE38lTU|
Simon & Garfunkel:  Scarborough Fair|-BakWVXHSug|
Simon & Garfunkel: Mrs. Robinson|_C2vqI9FVwg|
Simon & Garfunkel: Sounds of Silence|4zLfCnGVeL4|
Simon & Garfunkel: The Boxer|C1VUWDcp5Sg|
Skeeter Davis:  End of the World|sonLd-32ns4|
Stairway to Heaven: Heart|2cZ_EFAmj08|
Stairway to Heaven: Led Zeppelin (concert)|https://www.youtube.com/watch?v=BciS5krYL80e|
Stone Ponies:  Different Drum|w9qsDgA1q8Y|
Streisand: People|fPlQ6EtArSc|
Streisand: Woman in Love|hQLGCX8D-1Y|
Styx:  Mr. Roboto|51ybp_YFo7I|
Sunrise, Sunset|lRsciuPOWW4|
Survivor:  Eye Of The Tiger|btPJPFnesV4|
Temptations:  Papa Was a Rollin' Stone|71l85z2bXAs|
Tennessee Ernie Ford:  16 Tons|jIfu2A0ezq0|
The Ballad Of Cat Ballou|Sw16X_9XtuE|
The Little Nash Rambler|enqNl7tdLR4|
The Night the Lights Went Out in Georgia|wMD5nBcPrCk|
Theme From Shaft|Q429AOpL_ds|
This is a Man's World: James Brown|wd1-HM234DE|
This is a Man's World: PMJ|mPimt0Zu_To|
Three Dog Night:  Eli's coming|1A2eet1bttY|Also look up writer's Laura Nyro's version.
Three Dog Night:  One|UiKcd7yPLdU|
Time Won't Let Me|3yQERVphWhY|
Tony Bennett: I Left My Heart in San Francisco|SC73kdOL5hk|
Total Eclipse of the Heart|lcOxhH8N3Bo|
Toto: Africa|qDLJ3pUZm9A|
Tuxedo Junction|iBTYcqtaOjg|
Unchained Melody|zrK5u5W8afc|
Unforgettable|Fy_JRGjc1To|
Vanity Fare:  Early In The Morning|9hN9YRo7y1s||I played this a lot on a stereo/phono/8-track thingy I bought from my Dad's store in the 1960's.
Village Stompers: Washington Square|ihenbyTzQ2A|
Volga Boatmen (1866)|qsovBF4N27Q|
Volga Boatmen|0tw3g88JtWA|Baritone L. Kharitonov 1965 
We Five: You Were On My Mind|c7YSANg8vgw|
Yardbirds:  Heart Full of Soul|pM1qZBFiOLU|
Zager and Evans:  In The Year 2525|yesyhQkYrQM|

Rimsky-Korsakov:  Scheherezade|1i6TsIVKByM|Excellent youth orchestra
Barber of Seville (1821)|OloXRhesab0||Most of us probably heard this first by watching Saturday morning cartoons.
Ravel: Bolero|8KsXPq3nedY|
Beethoven: Moonlight Sonata (3rd)|o6rBK0BqL2w|17 year old girl (Tina S)
Beethoven: Moonlight Sonata (3rd)|zucBfXpCA6s|Valentina Lisitsa
Beethoven:  2nd movement 9th|p5favl2Qtx0|Player-piano type visual
Beethoven: Für Elise|_mVW8tgGY_w|
Beethoven: Moonlight Sonata|4Tr0otuiQuU|
Beethoven's 9th|fRZaX6-dsn8|
Beethoven's 5th|1lHOYvIhLxo|
Beethoven's 7th|W5NsPOgyALI|
Dvorak:  New World Symphony (Dvorak's 9th 1893)|VuaTY3zHO8Q|London Symphony Orchestra
New World Symphony and The Moldau|Qut5e3OfCvg|Slovak Philharmonic
Tchaikovsky:  1812 Overture (1888)|QUpuAvQQrC0|
Bach: Toccata and Fugue in D Minor|JL0PCLMSQms|Violin
Bach: Toccata and Fugue in D Minor|_Cst9lV5PPg|Brass
Bach: Toccata and Fugue in D Minor|eDFFUIGoBUc|Accordion
Bach: Toccata and Fugue in D Minor|ho9rZjlsyYY|Organ
Bach: Toccata and Fugue in D Minor|i9UQ61EbdO0|Orchestra
Bach: Toccata and Fugue in D Minor|ipzR9bhei_o|Organ with bar graph score
Bach: Toccata and Fugue in D Minor|oPmKRtWta4E|Harp (a masterpiece)
Bach: Toccata and Fugue in D Minor|ojBYW3ycVTE|Guitar
Bach: Toccata and Fugue in D Minor|zhH53UODLEM|Piano with visual score

'''

def Inspect():
    'Check that all the lines have the proper form'
    def Check(line):
        f = line.split("|")
        if len(f) not in (3, 4):
            print(f"Bad line:\n{line!r}")
            exit(1)
    for item in (favorites, songs):
        for line in GetTextLines(item):
            if not line or line[0] == "#":
                continue
            Check(line)
def Print(s):
    link = "https://www.youtube.com/watch?v="
    song_list = []
    # Process each line
    for line in s.split("\n"):
        line = line.strip()
        if not line or line[0] == "#":
            continue
        f = [i.strip() for i in line.split("|")]
        if not f[1].startswith("https://"):
            f[1] = link + f[1]
        song_list.append(f)
    # Output the HTML data
    for f in sorted(song_list):
        descr, link = f[0], f[1]
        extra = ' '.join(f[2:]) if long else f[2]
        print(f"<a href=\"{link}\">{descr}</a> {extra} <br>")
def Notation():
    print(dedent('''
    '''))

if __name__ == "__main__": 
    now = iso.ISO()
    Inspect()
    long = len(sys.argv) > 1
    print(f"Favorites:</p>")
    Print(favorites)
    print(f"<p>Others:</p>")
    Print(songs)
    print(f"<p>{now.date}<p>")
 
# vim: tw=0 wm=0
