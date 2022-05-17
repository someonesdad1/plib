import sys
import time
from pdb import set_trace as xx 
 
favorites = '''

2nd movement Beethoven's 9th (written 1824)|iwIvS4yIThU|Genius
Bad Romance|VCTOpdlZJ8U|PMJ & tap dancing (Sarah Reich) (singer is Telly Savalas' daughter)
Catharsis (2013)|h3hlFAVV6aI|My beloved Sa-Sa|  Sally went to a fiddle camp in WA and learned this song.  When she returned, she said she knew I'd like it.  She was right, as it's my favorite fiddle song.
Crazy (1961)|MbnrdCS57d0||Nobody sings it like Patsy Cline.
Diamonds and Rust (1975)|2MSwBM_CbyY|Baez's best
Don't Cry For Me Argentina (1977)|_n8mq7sedP4|A masterpiece
I'll Never Find Another You (1963)|KmactMIhrRM|How I feel about Glenda
Midnight In Moscow (1961)|o744d4mwOgQ|Dixieland from England
Potato Head Blues (1927)|EfGZB78R7uw|Famous trumpet solo
Scheherezade (1st movement, written 1888)|6dDk6aft4JU|von Karajan on Deutsche Grammophone (I bought this record in about 1970 and was mesmerized by it)
Stairway to Heaven (1971)|QkF3oxziUI4|
The Moldau (written 1875)|l6kqu2mk-Kw|Such accomplished young musicians

'''

songs = '''

16 Tons|jIfu2A0ezq0|
1812 Overture (1888)|QUpuAvQQrC0|Real cannons & church bells|  I used to listen to this on an 8-track tape I got from my parents.  I'd lay on the floor of my apartment between the small stereo speakers and enjoy it.
25 Or 6 To 4|iUAYeN3Rp2E|Great horns and guitar|This reminds me of visiting a friend in Chicago in the early 1970's and he took me to a place where this band played, although they weren't there.
2nd movement Beethoven's 9th|p5favl2Qtx0|Player-piano type visual
A Horse With No Name|mSZXWdKSQNM|
A World of our Own|PSxwqBJLU8A|
Africa|qDLJ3pUZm9A|
American Pie|iX_TFkut1PM|
Angie|S7sigwbqEj8||Always one of my favorite songs from the Stones along with Jumpin' Jack Flash.
Aquarius|oPK7ZF6jfJE&t=8|
Bad Bad Leroy Brown|CIiVindRSTA|
Barber of Seville (1821)|OloXRhesab0||Most of us probably heard this first by watching Saturday morning cartoons.
Barracuda|PeMvMNpvB5M|
Bay Of Mexico|-16OczraVi4|
Beat It|oRdxUFDoQe0||When this song came out, I bought the record and loved playing it loud on my stereo.
Big John|KnnHprUGKF0|
Blowin' in the Wind|Ld6fAO4idaI|
Bolero|8KsXPq3nedY||My thesis adviser's wife always laughed when I pronounced the composer's name with the accent on the first syllable (I didn't know any better).
Boogie Woogie Bugle Boy|8of3uhG1tCI|
Both Sides Now|8L1UngfqojI|
Bucket drummer|FqJdzYY_Fas|
Bus Stop|It75wQ0JypA|
Cincinnati Kid|rfn1YrwG2Oc||My roommate in freshman year from college had a 1965 Chevelle SS we'd ride around in and he'd play the album from this movie.  I've always liked this song.
Classical Gas|PRZkc88uNXo||This guitar song was quite a hit when it came out.
Country Roads|1vrEljMfXYo|John Denver|  Every time I hear this, it saddens me that John Denver was killed in the crash of a plane he was piloting.  He was a wonderful talent.
Country Roads|qap9Qm-Q894|Petersens
Crocodile Rock|75r0nQu-hMs|
Different Drum|w9qsDgA1q8Y||This was by the Stone Ponies in the 1960's and everyone knew what a fox Linda Rondstat was.
Doc Severinsen and Arturo Sandoval|s53B0PyAEOE|Great trumpets & guitar, but the violin is best
Downtown|Zx06XNfDvk0|
Dream Lover|wVHAQX5sSaU||Bobby Darin -- always makes me think of 'Mack the Knife'.
Dreams|O5ugW4-BstE|
Drive My Car|kfSQkZuIx84|
Dueling Banjos|myhnAZFR1po||In the dorm in freshman year in college.  A guy down the hall (we called him Penguin) had this on a 45 record and he was forced to play it hundreds of times, as everyone loved it.
Dust in the Wind|tH2w6Oxx0kQ||Good song by Kansas.
Early In The Morning|9hN9YRo7y1s||I played this a lot on a stereo/phono/8-track thingy I bought from my Dad's store in the 1960's.
Easy Lover|2aJ2Vh_e2dQ||This always reminds me of a winter camping trip cross-country skiing into the Steens mountains.  We hear this song on the radio in my Land Cruiser a few times while driving over there.
El Condor Pasa|pey29CLID3I|
El Paso|-zBzZJd-nfw|
Eli's coming|1A2eet1bttY|Also look up writer's Laura Nyro's version.
Ella Fitzgerald scat singing|9CbVy1NnB4g||She was a master at scat singing.  Debbie and I got to see her once at a theater in Oakland, CA.
End of the World|sonLd-32ns4|
Everybody's Somebody's Fool|ECOthzFvUXY|
Exodus|xhXZ3eXJIFc|
Eye Of The Tiger|btPJPFnesV4|
Fast Freight|Oy_NkJOwRqE||This has always been a favorite Kingston Trio song of mine.  I used to mentally sing it in my mind many times when driving back from fiddle contests when Sally was young.
Fast Freight|Sin3FeAQAws| Eliza Gilkyson (song writer's daughter)
Fever|JGb5IweiYG8|
Flight of the Condor|66KVAhNE_rQ|1982| This was a BBC TV show and had great pan pipe music from South America.
Foggy Mountain Breakdown|z_Y3mnj-8lA|| College friends used to rave about Flatt & Scruggs.
For What It's Worth|gp5JCrSXkJY|
Georgia On My Mind|QL3EZwSJAh0|
Ghost Riders In the Sky|ZwAPa0qHmLo|Frankie Laine|I first heard this in a nightclub in Santa Barbara when visiting my sister while in college.  
Ghost Riders In the Sky|fD5kS3G1Jkk|Marty Robbins
Ghost Riders In the Sky|j2klh2cTa_Q|Burl Ives (1949)
Ghost Riders In the Sky|nOWjX4BpC24|Highwaymen (1990)
Girl drummer|L-So4DLDvGc||How can you watch this and not mentally smile at this girl's joy?
Gypsy|mwgg1Pu6cNg|
Hair|BFy-yzj02FE|
Hang 'Em High Theme|0gscut1p4kY|
Hawaii 50 Theme|AepyGm9Me6w||In the 1960's, we always watched Hawaii 50.  My roommate and I would always remember the producer's name as Reza S. Badiyi.  How can I remember that and not remember where I set my glasses down?
Heart Full of Soul|pM1qZBFiOLU||The Yardbirds played at our high school once.
Heart of Gold|X3IA6pIVank|
Hey Jude|mQER0A0ej0M|
Hit the Road Jack|OfUDsHtSv88|Becca Krueger (skip first 20 seconds) | This is Ray Charles' song, but Becca and the group do an amazing job at it.
Hit the Road Jack|SrnWp5O0DEs|
Hot Rod Lincoln|3R7l7nDuj1o|
Hotel California|811QZGDysx0|
House Of The Rising Sun|MJkr0DWbhTk||I loved this song in high school.
How Blue Can You Get?|LWLAAzOBoBI|A masterpiece
I Am A Man Of Constant Sorrow|OdYGnAFaeHU|
I Left My Heart in San Francisco|SC73kdOL5hk
I Will Survive|ARt9HV9T0w8|
I love the flower girl|dZMc0-ZAUeY|
I was Born Under a Wandering Star|NTymtAbaG08
I'm Still Standing|Ye9hGotPPVk|
Ievan Polkka|4om1rQKPijI|A masterpiece of a capella -- I love the scat singing of the girl in the red dress around 1:30
In The Year 2525|yesyhQkYrQM|
Indian Lake|3Xup3HSZLIQ|Bubble rock
It Was A Very Good Year|CJARjwzmceg||This always reminds me of a particular girlfriend in college and being at a drive-in theater with her, when I somehow went in and used the girl's bathroom -- she laughed and teased me about it afterwords, as she was in another stall.  I remember wondering why there were no urinals.
Journey to Kilimanjaro|e0DpZ3WVowY|1994 Nova show.  Melodically simple but haunting music:  1:20, 4:15, 8:10, 12:03, 19:40, 22:08, 36:50, 38:46, *39:34, 44:58, 51:57, 54:15 (credits)
Judy Blue Eyes|XWvw_uZPGDA|2012
Judy Blue Eyes|cMJug2iz3NA|1969
Jumpin' Jack Flash|-rIG2POqtV8|
Kisses Sweeter Than Wine|iulmZAz8XfY|
Kodachrome|8rlDTK6QI-w|
Korobushka|E5NByiEIbD8|Bond live at Albert Hall
Korobushka|Pr3ZgN8onRA|Mikhail Smirnov
Korobushka|vvC2vjtmUX8|Bond live at Albert Hall
Lady Bird|FIPQVpw-zkk|
Land Down Under|8jHXu86O01w|
Light My Fire|LY1l8T2Lcl0||This always reminds me of a friend's apartment in 1967 in college, as this record was always playing there.
Listen To Your Heart|yCC_b5WHLX0|
Long Cool Woman|X3sU_q1GH-4|
Love Me With All Your Heart|k3nfqH4YDDM||My sister remembers this at our high school dances.
Love is Blue|YYf_hb-jsGo|
MTA|MbtkL5_f6-4|
MacArthur Park|iplpKwxFH2I|
Mack the Knife|SEllHMWkXEU|
Maggie May|EOl7dh7a-6g|
Magnificent Seven (1960)|8XDB7GMnbUQ|
Mambo Italiano|9prJXEhNhPA|
Me & Bobby McGee|WXV_QjenbDw|
Memories (from Cats)|5mlllRdIfqw|Betty Buckley
Memories (from Cats)|MWoQW-b6Ph8|Streisand
Memories (from Cats)|mdBVJbzkoqo|Elaine Paige
Midnight In Moscow|FY3Zr5Tj5zw|2011
Moody Blues:  Blue World|8a9bfvNuTw0|With lyrics
Moody Blues:  Blue World|oosjl8wNLJU|
Moody Blues:  I'm Just A Singer in a Rock And Roll Band|5UZWXE76ELU|Album
Moody Blues:  I'm Just a Singer in a Rock and Roll Band|s5tb25TqXYU|Concert
Moody Blues:  Isn't Life Strange|9WZZjXgJ4W8|
Moody Blues:  Ride My See-saw|GXHMTuoK060|
Moody Blues:  Your Wildest Dreams|kmmPFrkuPq0|
Moonlight Sonata (3rd)|o6rBK0BqL2w|17 year old girl (Tina S)
Moonlight Sonata (3rd)|zucBfXpCA6s|Valentina Lisitsa|  Incredible piano player
Morningtown Ride|M-RkC6MYT2E|1964
Morningtown Ride|wqdaCOt51Dk|2014
Mr. Roboto|51ybp_YFo7I|
Mrs. Robinson|_C2vqI9FVwg|
My Sweet Lord|AR4lpQWcT5g|
New World Symphony (Dvorak's 9th 1893)|VuaTY3zHO8Q|London Symphony Orchestra
New World Symphony and The Moldau|Qut5e3OfCvg|Slovak Philharmonic
North to Alaska (1960)|RO6IU9RpjS8|
Nothing Else Matters|8KK0-9Moz5Q| Hammered dulcimer
Nothing Else Matters|KSSa0-oAnIo| PMJ:  15 year old girl singer
Nothing Else Matters|tAGnKpE4NCI|
Old Man|rAtDrFdomN4|
One|UiKcd7yPLdU|
Paint It Black|O4irXQhgMqg|
Papa Was a Rollin' Stone|71l85z2bXAs||That bass beat gets to you...
Paperback Writer|yYvkICbTZIQ|
Papillon|Js69DkyaDVQ|
Patricia|rTXIXkeWnEo|
Paul McCartney carpool karaoke|QjvzCTqkBDQ|
Penny Lane|S-rB0pHI9fU|
People|fPlQ6EtArSc||Streisand's first big hit in the early 1960's
Pirates of the Caribbean|27mB8verLK8|
Pirates of the Caribbean|6zTc2hD2npA|Auckland Symphony
Popcorn Song|DBYjZTdrJlA|
Purple People Eater|Rx47qrH1GRs||I remember hearing this in my mom's car in the 1950's
Push It To The Limit|9D-QD_HIfjA|
Question|tmOZFAYeurY|
Rainy Days and Monday|PjFoQxjgbrs|
Rainy Night in Georgia|bDRbF80NKDU|
Rawhide|_EjbzCX3enA|
Rocket Man|BdEe5SpdIuo|
Run Through The Jungle|EbI0cMyyw_M|
Sally:  Gypsy Waltz|eDGE6ah-e4Y|
Sally:  Orange Blossom Special|6-5xPixiCkI|
Sally:  Sally Goodin|nbYBBeylfGk||My second-favorite fiddle song
Sally:  Unknown song|ob44BR1Hurg|
Scarborough Fair|-BakWVXHSug||I listened to this many times in my dorm room in college
Scheherezade|1i6TsIVKByM|Excellent youth orchestra
She Works Hard for the Money|09ZSKE38lTU|
She's Got You|7nXPQbKZBbw|Petersens
Silver Threads and Golden Needles|uz6HB9HYQz4|Dusty Springfield
Sounds of Silence|4zLfCnGVeL4|
Stairway to Heaven|2cZ_EFAmj08| Heart at Kennedy Center; great production
Struttin' With Some Barbecue|yl-2R_Pb7dk|
Summer Wine|Ib_eW9VSUwM|
Sunrise, Sunset (Mantovani)|EzEHI1alPZ8|
Sunrise, Sunset|lRsciuPOWW4||I remember hearing this playing in my parents' house in the 1960's; it made much more sense to me decades later after seeing Sally grow up.
Superstar|SJmmaIGiGBg|
Suzy Q|7x60p7UNLnQ|
Sweet Dreams|qeMFqkcPYcg|
Take Five|vmDDOFXSgAs||Great; also listen to 'Unsquare Dance' on this album.
The Ballad Of Cat Ballou|Sw16X_9XtuE|
The Boxer|C1VUWDcp5Sg|
The Crystal Ship|bU1sLx1tjPY||This was on the flip side of the "Light My Fire" 45.
The Little Nash Rambler|enqNl7tdLR4|
The Night They Drove Old Dixie Down|wanJQC5KAfo|
The Night the Lights Went Out in Georgia|wMD5nBcPrCk|
The Thrill is Gone|Nu4tjTyqbho|
The Voice|-umqM9R8cnI|
The Wreck of the Edmund Fitzgerald|9vST6hVRj2A|
Theme From Shaft|Q429AOpL_ds|
These Boots Are Made for Walkin'|rypT2qMO1RY|
They Call the Wind Mariah|ByqYEzugleE|Harve Presnell|From the movie 'Paint Your Wagon'.
This is a Man's World|mPimt0Zu_To|PMJ with woman singer
This is a Man's World|wd1-HM234DE|James Brown 1960's
Those Were The Days|y3KEhWTnWvE|
Time Won't Let Me|3yQERVphWhY|
Toccata and Fugue in D Minor|JL0PCLMSQms|Violin
Toccata and Fugue in D Minor|_Cst9lV5PPg|Brass
Toccata and Fugue in D Minor|eDFFUIGoBUc|Accordion
Toccata and Fugue in D Minor|ho9rZjlsyYY|Organ
Toccata and Fugue in D Minor|i9UQ61EbdO0|Orchestra
Toccata and Fugue in D Minor|ipzR9bhei_o|Organ with bar graph score
Toccata and Fugue in D Minor|oPmKRtWta4E|Harp (a masterpiece)
Toccata and Fugue in D Minor|ojBYW3ycVTE|Guitar
Toccata and Fugue in D Minor|zhH53UODLEM|Piano with visual score
Today (1964)|3cELsUMcQdc||I listened to this many, many times
Torn Between Two Lovers|TzGbvTl4mpg||This always reminds me driving back to college in my 6 cylinder Mustang late at night.  I had removed the dash and replaced the bulbs with some painted with red nail polish, so my dash lights were red.
Total Eclipse of the Heart|lcOxhH8N3Bo|
Tuxedo Junction|iBTYcqtaOjg|
Two Faces Have I|w05w1XbZTG8|
Unchained Melody|zrK5u5W8afc|
Unforgettable|Fy_JRGjc1To|
Unsquare Dance|lbdEzRfbeH4||Try to keep the beat with this.
Victory|j3nBuwOPu8A&list=RDE5NByiEIbD8| Bond
Volga Boatmen (1866)|qsovBF4N27Q|
Volga Boatmen|0tw3g88JtWA|Leonid Kharitonov 1965 | He was an incredible baritone.
Walk On the Wild Side|5O82y59h7MI||I bought this album in the 1960's and always wait for a particular 2 second phrase near the end.
Washington Square|ihenbyTzQ2A|
White Rabbit|EUY2kJE0AZE||In 1966, I bought a $5 transistor radio from a friend in high school and remember hearing this song on it numerous times.
White Silver Sands|mOqbjENGN7s|First 45 rpm record I ever bought in 1957
Who's on First|kTcRRaXV-fg|Genius comedy
Woman in Love|hQLGCX8D-1Y|
Yesterday when I was young|GQIAcztYjbc||Great song
You Only Live Twice|XgFtQPgHyek||This was a theme from one of the James Bond movies
You Were On My Mind|c7YSANg8vgw|
You're So Vain|cleCtBP0o5Y||A long mystery is who was this song referring to.

'''

def Print(s):
    link = "https://www.youtube.com/watch?v="
    song_list = []
    # Process each line
    for line in s.split("\n"):
        line = line.strip()
        if not line or line[0] == "#":
            continue
        f = [i.strip() for i in line.split("|")]
        f[1] = link + f[1]
        song_list.append(f)
    # Output the HTML data
    for f in sorted(song_list):
        descr, link = f[0], f[1]
        extra = ' '.join(f[2:]) if long else f[2]
        #print(f"[{f[0]}]({f[1]}) {s} <br>")
        print(f"<a href=\"{link}\">{descr}</a> {extra} <br>")

if __name__ == "__main__": 
    long = len(sys.argv) > 1
    print(f"<p>{time.asctime()}</p><p>Favorites:</p>")
    Print(favorites)
    print(f"<p>Others:</p>")
    Print(songs)
 
# vim: tw=0 wm=0
