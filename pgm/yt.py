'''
Make an HTML file of URLs to youtube videos
'''
if 1:   # Header
    from color import t
    from wrap import dedent
    import iso
    import requests
    import sys
    if 0:
        import debug
        debug.SetDebugger()
    from dpprint import PP
    pp = PP()
if 1:   # Classes
    class G:
        pass
    g = G()
    # If the command line has an argument, validate the URLs
    g.validate = len(sys.argv) > 1
    class Item:
        def __init__(self, title, url, comment=""):
            self.title = title
            self.url = f"https://www.youtube.com/watch?v={url}"
            self.comment = comment
            self.validate()
        def validate(self):
            '''Validate the URL.  This is a heuristic that looks for the string
            "This video isn't available anymore", indicating the url is no
            longer valid.
            '''
            if not g.validate:
                return
            r = requests.get(self.url)
            s = "This video isn't available anymore"
            if s in r.text:
                t.print(f"{t.ornl}{self.url!r} not available")
        def __str__(self):
            return f'    {self.title} <a href="{self.url}">click</a><br>'
if 1:   # Data
    data = {
        "Construction": [
            Item("Bulldozer making a road in Turkey", "D7db_5tXg8Q", '''At 3 minutes, he comes to a steep
                area and you naturally wonder how he's going to make a road through this area.  He makes
                it look simple. Note the use of the uphill blade edge, as that's how he gets the fill for
                the road bed.'''),
            Item("Bulldozer making a different road", "YRq7DZHt5y4"),
            Item("Bulldozer digging road through rocks", "ECc0wzH5OQQ"),
            Item("Land clearing with two bulldozers and an anchor chain", "2TL7fuVYyRg"),
        ],
}
if __name__ == "__main__":
    now = iso.ISO()
    print(dedent('''
        <!DOCTYPE html>
        <body>
    '''))
    for category in data:
        print(f"<h2>{category}</h2>")
        for item in data[category]:
            print(item)
    if 1:
        print(f"<br><p>Updated {now.date}</p>")
    print("</body>")
# vim: tw=0 wm=0
