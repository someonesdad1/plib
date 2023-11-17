from get import GetTextLines
import sys
import time
import iso
from pdb import set_trace as xx 
if 1:
    import debug
    debug.SetDebugger()
 
favorites = '''

Angie (Rolling Stones)|S7sigwbqEj8|
Beethoven's 7th|Rw-KtQLdRT4|2nd movement 14:33 is best
Beethoven's 9th, 2nd movement (1824)|iwIvS4yIThU|Genius
Bad Romance|VCTOpdlZJ8U|PMJ & Sarah Reich tap dancing (singer is Telly Savalas' daughter)
Catharsis (Sa Sa 2013)|h3hlFAVV6aI|My favorite fiddle song
Crazy (Patsy Cline 1961)|MbnrdCS57d0||Nobody sings it like Patsy Cline.
Diamonds and Rust (Joan Baez 1975)|IrVD0bP_ybg|Baez's best
Don't Cry For Me Argentina (Karen Carpenter 1977)|_n8mq7sedP4|A masterpiece
Fast Freight:  Eliza Gilkyson|Sin3FeAQAws| Haunting, singer is song writer's daughter
Hit the Road Jack (Becca Krueger)|OfUDsHtSv88|(skip first 20 seconds)
Ievan Polkka|4om1rQKPijI|A masterpiece of a capella, 2008
Ievan Polkka|Zcg66Qcwjw8|13 years later, 2021
I'll Never Find Another You (Seekers 1963)|KmactMIhrRM|How I feel about Glenda
Korobushka|Pr3ZgN8onRA|
Bond: Korobushka|E5NByiEIbD8|
Midnight In Moscow (Kenny Ball 1961)|o744d4mwOgQ|Dixieland from England
Papillon: Waltz arrangement|FKrmozFh5ww|
Potato Head Blues (Louis Armstrong 1927)|EfGZB78R7uw|Famous trumpet solo
Scheherazade (1st movement, Rimsky-Korsakov 1888)|6dDk6aft4JU|von Karajan on Deutsche Grammophone
Stairway to Heaven (Led Zeppelin 1971)|QkF3oxziUI4|
This is a Man's World (PMJ, Morgan James)|mPimt0Zu_To|
Vltava (The Moldau) (Smetana, 1875)|l6kqu2mk-Kw|
Volga Boatmen (1866)|qsovBF4N27Q|This has nothing to do with the movie, but I also like music of this scene from the movie.

'''

dead_urls = '''
Hot Rod Lincoln|3R7l7nDuj1o|
White Rabbit|EUY2kJE0AZE|
Bobby Darin:  Mack the Knife|SEllHMWkXEU|
Ray Charles:  Georgia On My Mind|QL3EZwSJAh0|
The Night the Lights Went Out in Georgia|wMD5nBcPrCk|
'''

songs = '''

16 Tons|jIfu2A0ezq0|
25 Or 6 To 4|iUAYeN3Rp2E|Great horns and guitar
A Horse With No Name|mSZXWdKSQNM|
Africa|qDLJ3pUZm9A|
Air Supply:  All Out of Love|https://www.youtube.com/watch?v=tH2w6Oxx0kQ|
Air Supply:  Even the Nights Are Better|https://www.youtube.com/watch?v=BRx58DgOxeg|
Air Supply:  Making Love Out of Nothing at All|https://www.youtube.com/watch?v=JMKi9qVrGWM|
American Pie|iX_TFkut1PM|
Angel of the Morning|https://www.youtube.com/watch?v=HTzGMEfbnAw|
Aquarius|oPK7ZF6jfJE&t=8|
B.B. King: How Blue Can You Get?|LWLAAzOBoBI|A masterpiece
B.B. King: The Thrill is Gone|Nu4tjTyqbho|
Bad Bad Leroy Brown|CIiVindRSTA|
Ballad Of Cat Ballou|-ghnpUNTR1I|
Barracuda|PeMvMNpvB5M|
Beat It|oRdxUFDoQe0|
Beatles:  Drive My Car|kfSQkZuIx84|
Beatles:  Paperback Writer|yYvkICbTZIQ|
Beatles:  Penny Lane|S-rB0pHI9fU|
Beatles: Hey Jude|mQER0A0ej0M|
Big John|KnnHprUGKF0|
Blowin' in the Wind|Ld6fAO4idaI|
Bobby Darin:  Dream Lover|wVHAQX5sSaU|
Bond: Korobushka|vvC2vjtmUX8|
Bond: Victory|j3nBuwOPu8A&list=RDE5NByiEIbD8|
Boogie Woogie Bugle Boy|8of3uhG1tCI|
Both Sides Now|8L1UngfqojI|
Bucket drummer|FqJdzYY_Fas|
Buffalo Springfield:  For What It's Worth|gp5JCrSXkJY|
Carpenters:  Rainy Days and Monday|PjFoQxjgbrs|
Carpenters: Superstar|SJmmaIGiGBg|
Classical Gas|PRZkc88uNXo|
Country Roads:  John Denver|1vrEljMfXYo|
Country Roads:  Petersens|qap9Qm-Q894|Petersens
Cowsills: Hair|BFy-yzj02FE|
Cowsills: I love the flower girl|dZMc0-ZAUeY|
Cowsills: Indian Lake|3Xup3HSZLIQ|Bubble rock
Creedence Clearwater: Run Through The Jungle|EbI0cMyyw_M|
Creedence Clearwater: Suzy Q|7x60p7UNLnQ|
Crosby, Stills, and Nash: Judy Blue Eyes (1969)|cMJug2iz3NA|1969
Crosby, Stills, and Nash: Judy Blue Eyes (2012)|XWvw_uZPGDA|
Dave Clark Five:  Take Five|vmDDOFXSgAs|
Dave Clark Five:  Unsquare Dance|lbdEzRfbeH4|
Different Drum|w9qsDgA1q8Y|
Doc Severinsen and Arturo Sandoval|s53B0PyAEOE|Great trumpets & guitar, but the violin is best
Doors:  Light My Fire|LY1l8T2Lcl0|
Doors:  The Crystal Ship|bU1sLx1tjPY|
Downtown|Zx06XNfDvk0|
Dueling Banjos|myhnAZFR1po|
Dust in the Wind|tH2w6Oxx0kQ|
Early In The Morning|9hN9YRo7y1s||I played this a lot on a stereo/phono/8-track thingy I bought from my Dad's store in the 1960's.
Easy Lover|2aJ2Vh_e2dQ|
El Condor Pasa|pey29CLID3I|
El Paso|-zBzZJd-nfw|
Ella Fitzgerald scat singing|9CbVy1NnB4g|
Elton John: Crocodile Rock|75r0nQu-hMs|
Elton John: I'm Still Standing|Ye9hGotPPVk|
Elton John: Rocket Man|BdEe5SpdIuo|
End of the World|sonLd-32ns4|
Everybody's Somebody's Fool|ECOthzFvUXY|
Exodus|xhXZ3eXJIFc|
Eye Of The Tiger|btPJPFnesV4|
Fever|JGb5IweiYG8|
Fleetwood Mac:  Dreams|O5ugW4-BstE|
Fleetwood Mac: Gypsy|mwgg1Pu6cNg|
Flight of the Condor|66KVAhNE_rQ|1982| This was a BBC TV show and had great pan pipe music from South America.
Für Elise|2fcX2dWmR6g|
Foggy Mountain Breakdown|z_Y3mnj-8lA|
Ghost Riders In the Sky: Roy Clark|8o2w1zhBKzk|
Ghost Riders In the Sky: Burl Ives (1949)|j2klh2cTa_Q|
Ghost Riders In the Sky: Frankie Laine|ZwAPa0qHmLo|
Ghost Riders In the Sky: Highwaymen (1990)|nOWjX4BpC24|
Ghost Riders In the Sky: Marty Robbins|fD5kS3G1Jkk|
Girl drummer|L-So4DLDvGc|
Hang 'Em High Movie Theme|0gscut1p4kY|
Hava Nagila|https://www.youtube.com/watch?v=YBj2PZ1IeIc|
Hawaii 50 Theme|AepyGm9Me6w|
Heart Full of Soul|pM1qZBFiOLU|
Hit the Road Jack|SrnWp5O0DEs| Ray Charles
Hollies:  Long Cool Woman|g8XiNKsKyVk|
Hollies: Bus Stop|It75wQ0JypA|
Hotel California|https://www.youtube.com/watch?v=BciS5krYL80|
House Of The Rising Sun|MJkr0DWbhTk||I loved this song in high school.
I Am A Man Of Constant Sorrow|OdYGnAFaeHU|
I Left My Heart in San Francisco|SC73kdOL5hk|
I Will Survive|ARt9HV9T0w8|
I was Born Under a Wandering Star|NTymtAbaG08|
In Hell I'll be in Good Company|B9FzVhw8_bY|
In The Year 2525|yesyhQkYrQM|
It Was A Very Good Year|CJARjwzmceg|
It's a Heartache|https://www.youtube.com/watch?v=bEOl38y8Nj8|
Jailhouse Rock|A99sV18J0mk|
Johnny B. Goode|Uf4rxCB4lys|
Journey to Kilimanjaro|5ZFJWIGN9zQ|1994 Nova show.  Melodically simple but haunting music:  0:48, 6:43, 9:28, 10:44, 30:07, 35:27, 37:33, 38:14*, 43:45, 50:42, 53:00(credits),
Kingston Trio: Bay Of Mexico|-16OczraVi4|
Kingston Trio: Fast Freight|Oy_NkJOwRqE||
Kingston Trio: MTA|MbtkL5_f6-4|
Kisses Sweeter Than Wine|iulmZAz8XfY|
Kodachrome|8rlDTK6QI-w|
Land Down Under|8jHXu86O01w|
Les Bicyclettes De Belsize|Qe_1B1P9Bw4|
Listen To Your Heart|yCC_b5WHLX0|
Love Me With All Your Heart|k3nfqH4YDDM|
Love is Blue|YYf_hb-jsGo|
MacArthur Park|iplpKwxFH2I|
Maggie May|EOl7dh7a-6g|
Magnificent Seven (1960)|8XDB7GMnbUQ|
Mambo Italiano|9prJXEhNhPA|
Me & Bobby McGee|WXV_QjenbDw|
Memories (from Cats): Betty Buckley|5mlllRdIfqw|
Memories (from Cats): Elaine Paige|mdBVJbzkoqo|
Memories (from Cats): Streisand|MWoQW-b6Ph8|
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
Mr. Roboto|51ybp_YFo7I|
My Sweet Lord|AR4lpQWcT5g|
Nancy Sinatra and Lee Hazelwood: Lady Bird|FIPQVpw-zkk|
Nancy Sinatra and Lee Hazelwood: Summer Wine|Ib_eW9VSUwM|
Nancy Sinatra: These Boots Are Made for Walkin'|rypT2qMO1RY|
Nancy Sinatra: You Only Live Twice|XgFtQPgHyek|
Neil Young:  Old Man|rAtDrFdomN4|
Neil Young: Heart of Gold|X3IA6pIVank|
North to Alaska (1960)|RO6IU9RpjS8|
Nothing Else Matters: Banjo & Mandolin|3JFb_aOn6rc|
Nothing Else Matters: Guitar & cello|pxoW-00Zyho|
Nothing Else Matters: Guitar|WlGiOiRQNhI|
Nothing Else Matters: Hammered dulcimer|8KK0-9Moz5Q|
Nothing Else Matters: Hardpan|32v8ARqaBas|She makes it look easy
Nothing Else Matters: Harp|KMX2bmtS_TE|
Nothing Else Matters: Metallica|tAGnKpE4NCI|
Nothing Else Matters: PMJ:  15 year old girl singer|KSSa0-oAnIo|
Nothing Else Matters: Piano|DmL12NRE4hQ|
Papa Was a Rollin' Stone|71l85z2bXAs|
Papillon|Js69DkyaDVQ|
Patricia|rTXIXkeWnEo|
Paul McCartney carpool karaoke|QjvzCTqkBDQ|
People|fPlQ6EtArSc|
Pirates of the Caribbean|27mB8verLK8|
Pirates of the Caribbean|6zTc2hD2npA|Auckland Symphony
Popcorn Song|DBYjZTdrJlA|
Purple People Eater|Rx47qrH1GRs|
Push It To The Limit|9D-QD_HIfjA|
Que Sera Sera|xZbKHDPPrrc|
Queen of Hearts|P0DK-0fIKCw|
Rainy Night in Georgia|bDRbF80NKDU|
Rawhide|_EjbzCX3enA|
Ray Charles:  Cincinnati Kid|rfn1YrwG2Oc|
Rolling Stones:  Jumpin' Jack Flash|-rIG2POqtV8|
Rolling Stones:  Paint It Black|O4irXQhgMqg|
Sally:  Gypsy Waltz|eDGE6ah-e4Y|
Sally:  Orange Blossom Special|6-5xPixiCkI|
Sally:  Sally Goodin|nbYBBeylfGk||My second-favorite fiddle song
Sally:  Unknown song|ob44BR1Hurg|
Seekers:  A World of our Own|PSxwqBJLU8A|
Seekers: Morningtown Ride|M-RkC6MYT2E|1964
Seekers: Morningtown Ride|wqdaCOt51Dk|2014
She Works Hard for the Money|09ZSKE38lTU|
She's Got You|7nXPQbKZBbw|
Shrek Hallelujah|EbO6P-_Zx0Y|
Silver Threads and Golden Needles|uz6HB9HYQz4|Dusty Springfield
Simon & Garfunkel:  Scarborough Fair|-BakWVXHSug|
Simon & Garfunkel: Mrs. Robinson|_C2vqI9FVwg|
Simon & Garfunkel: Sounds of Silence|4zLfCnGVeL4|
Simon & Garfunkel: The Boxer|C1VUWDcp5Sg|
Stairway to Heaven: Heart|2cZ_EFAmj08|
Stairway to Heaven: Led Zeppelin (concert)|BciS5krYL80e|
Stairway to Heaven: Harp|wLiH6F82t_U|
Struttin' With Some Barbecue|yl-2R_Pb7dk|
Sunrise, Sunset|03rzUoyq9K0|Fiddler On the Roof movie
Sunrise, Sunset|QD8u-fjQnFs|Bette Midler
Sweet Dreams|qeMFqkcPYcg|
The Gambler|7hx4gdlfamo|
The Little Nash Rambler|enqNl7tdLR4|
The Night They Drove Old Dixie Down|wanJQC5KAfo|
The Wreck of the Edmund Fitzgerald|9vST6hVRj2A|
Theme From Shaft|Q429AOpL_ds|
They Call the Wind Mariah|ByqYEzugleE|
This is a Man's World: James Brown|wd1-HM234DE|
Those Were The Days|y3KEhWTnWvE|
Three Dog Night:  Eli's coming|1A2eet1bttY|Also look up writer's Laura Nyro's version.
Three Dog Night:  One|UiKcd7yPLdU|
Time Won't Let Me|3yQERVphWhY|
Today (1964)|3cELsUMcQdc|
Torn Between Two Lovers|TzGbvTl4mpg|
Total Eclipse of the Heart|lcOxhH8N3Bo|
Tuxedo Junction|iBTYcqtaOjg|
Two Faces Have I|w05w1XbZTG8|
Unchained Melody|zrK5u5W8afc|
Unforgettable|Fy_JRGjc1To|
Volga Boatmen|0tw3g88JtWA|Baritone L. Kharitonov 1965 
Volga Boatmen |yfO0ADduEr8|Better than Kharitonov
Walk On the Wild Side|5O82y59h7MI|
Walking in the Air|upH1QZU4Z0Y|Movie theme sung by a 13 year old choirboy
Washington Square|ihenbyTzQ2A|
White Silver Sands|mOqbjENGN7s|
Who's on First|kTcRRaXV-fg|Genius comedy
Woman in Love (Barbra Streisand)|hQLGCX8D-1Y|
Yesterday when I was young|GQIAcztYjbc|
You Were On My Mind|c7YSANg8vgw|
You'll Never Know|4HU8I9BY1H0|
You're So Vain|cleCtBP0o5Y|

Rimsky-Korsakov:  Scheherazade|1i6TsIVKByM|Excellent youth orchestra
Barber of Seville (1821)|OloXRhesab0||Most of us probably heard this first by watching Saturday morning cartoons.
Ravel: Bolero|8KsXPq3nedY|
Beethoven: Moonlight Sonata (3rd)|o6rBK0BqL2w|17 year old girl (Tina S)
Beethoven: Moonlight Sonata (3rd)|zucBfXpCA6s|Valentina Lisitsa
Beethoven:  2nd movement 9th|p5favl2Qtx0|Player-piano type visual
Beethoven: Für Elise|_mVW8tgGY_w|
Beethoven: Moonlight Sonata|4Tr0otuiQuU|
Beethoven's 9th|fRZaX6-dsn8|
Beethoven's 5th|1lHOYvIhLxo|
Beethoven's 5th|Zev0ran0iuU|NY Philharmonic
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
            if not line or line.strip()[0] == "#":
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
    print(f"<p>Updated {now.date}<p>")
 
# vim: tw=0 wm=0
