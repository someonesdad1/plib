'''
PBS list of 100 great read books in the US.  
    https://www.pbs.org/the-great-american-read/books/#/
'''
from color import t
data = '''
    1 | To Kill a Mockingbird | Harper Lee 
    2 | Outlander (Series) | Diana Gabaldon 
    3 | Harry Potter (Series) | J.K. Rowling 
    4 | Pride and Prejudice | Jane Austen 
    5 | The Lord of the Rings (Series) | J.R.R. Tolkien 
    6 | Gone with the Wind | Margaret Mitchell 
    7 | Charlotte's Web | E. B. White 
    8 | Little Women | Louisa May Alcott 
    9 | The Chronicles of Narnia (Series) | C.S. Lewis 
    10 | Jane Eyre | Charlotte Brontë 
    11 | Anne of Green Gables | Lucy Maud Montgomery 
    12 | The Grapes of Wrath | John Steinbeck 
    13 | A Tree Grows in Brooklyn | Betty Smith 
    14 | The Book Thief | Markus Zusak 
    15 | The Great Gatsby | F. Scott Fitzgerald 
    16 | The Help | Kathryn Stockett 
    17 | The Adventures of Tom Sawyer | Mark Twain 
    18 | 1984 | George Orwell 
    19 | And Then There Were None | Agatha Christie 
    20 | Atlas Shrugged | Ayn Rand 
    21 | Wuthering Heights | Emily Brontë 
    22 | Lonesome Dove | Larry McMurtry 
    23 | The Pillars of the Earth | Ken Follett 
    24 | The Stand | Stephen King 
    25 | Rebecca | Daphne du Maurier 
    26 | A Prayer for Owen Meany | John Irving 
    27 | The Color Purple | Alice Walker 
    28 | Alice's Adventures in Wonderland | Lewis Carroll 
    29 | Great Expectations | Charles Dickens 
    30 | The Catcher in the Rye | J.D. Salinger 
    31 | Where the Red Fern Grows | Wilson Rawls 
    32 | The Outsiders | S. E. Hinton 
    33 | The Da Vinci Code | Dan Brown 
    34 | The Handmaid's Tale | Margaret Atwood 
    35 | Dune | Frank Herbert 
    36 | The Little Prince | Antoine de Saint-Exupéry 
    37 | The Call of the Wild | Jack London 
    38 | The Clan of the Cave Bear | Jean M. Auel 
    39 | The Hitchhiker's Guide to The Galaxy | Douglas Adams 
    40 | The Hunger Games (Series) | Suzanne Collins 
    41 | The Count of Monte Cristo | Alexandre Dumas 
    42 | The Joy Luck Club | Amy Tan 
    43 | Frankenstein | Mary Shelley 
    44 | The Giver | Lois Lowry 
    45 | Memoirs of a Geisha | Arthur Golden 
    46 | Moby Dick | Herman Melville 
    47 | Catch-22 | Joseph Heller 
    48 | Game of Thrones (Series) | George R. R. Martin 
    49 | Foundation (Series) | Isaac Asimov 
    50 | War and Peace | Leo Tolstoy 
    51 | Their Eyes Were Watching God | Zora Neale Hurston 
    52 | Jurassic Park | Michael Crichton 
    53 | The Godfather | Mario Puzo 
    54 | One Hundred Years of Solitude | Gabriel García Márquez 
    55 | The Picture of Dorian Gray | Oscar Wilde 
    56 | The Notebook | Nicholas Sparks 
    57 | The Shack | William P. Young 
    58 | A Confederacy of Dunces | John Kennedy Toole 
    59 | The Hunt for Red October | Tom Clancy 
    60 | Beloved | Toni Morrison 
    61 | The Martian | Andy Weir 
    62 | The Wheel of Time (Series) | Robert Jordan, Brandon Sanderson 
    63 | Siddhartha | Hermann Hesse 
    64 | Crime and Punishment | Fyodor Dostoyevsky 
    65 | The Sun Also Rises | Ernest Hemingway 
    66 | The Curious Incident of the Dog in the Night-Time | Mark Haddon 
    67 | A Separate Peace | John Knowles 
    68 | Don Quixote | Miguel de Cervantes 
    69 | The Lovely Bones | Alice Sebold 
    70 | The Alchemist | Paulo Coelho 
    71 | Hatchet (Series) | Gary Paulsen 
    72 | Invisible Man | Ralph Ellison 
    73 | The Twilight Saga (Series) | Stephenie Meyer 
    74 | Tales of the City (Series) | Armistead Maupin 
    75 | Gulliver's Travels | Jonathan Swift 
    76 | Ready Player One | Ernest Cline 
    77 | Left Behind (Series) | Tim LaHaye, Jerry B. Jenkins 
    78 | Gone Girl | Gillian Flynn 
    79 | Watchers | Dean Koontz 
    80 | The Pilgrim's Progress | John Bunyan 
    81 | Alex Cross Mysteries (Series) | James Patterson 
    82 | Things Fall Apart | Chinua Achebe 
    83 | Heart of Darkness | Joseph Conrad 
    84 | Gilead | Marilynne Robinson 
    85 | Flowers in the Attic | V.C. Andrews 
    86 | Fifty Shades of Grey (Series) | E.L. James 
    87 | The Sirens of Titan | Kurt Vonnegut 
    88 | This Present Darkness | Frank E. Peretti 
    89 | Americanah | Chimamanda Ngozi Adichie 
    90 | Another Country | James Baldwin 
    91 | Bless Me, Ultima | Rudolfo Anaya 
    92 | Looking for Alaska | John Green 
    93 | The Brief Wondrous Life of Oscar Wao | Junot Díaz 
    94 | Swan Song | Robert R. McCammon 
    95 | Mind Invaders | Dave Hunt 
    96 | White Teeth | Zadie Smith 
    97 | Ghost | Jason Reynolds 
    98 | The Coldest Winter Ever | Sister Souljah 
    99 | The Intuitionist | Colson Whitehead 
    100 | Doña Bárbára | Rómulo Gallegos 
'''[1:-1]
def GetData():
    'Return list of (num, title, author)'
    o = []
    for line in data.split("\n"):
        o.append([i.strip() for i in line.split("|")])
    return o
def PrintData():
    # Set up colors
    t.num = t("gryl")
    t.title = t("wht", attr="it")
    t.author = t("gryl")
    o = GetData()
    # Get column sizes
    wn = max(len(str(i[0])) for i in o) + 2
    wti = max(len(str(i[1])) for i in o) + 2
    wa = max(len(str(i[2])) for i in o) + 2
    # Print in color
    for n, ti, au in o:
        t.print(f"{t.num}{str(n):{wn}s} {t.title}{ti:{wti}s}{t.n} {t.author}{au:{wa}s}")
if __name__ == "__main__":  
    PrintData()
