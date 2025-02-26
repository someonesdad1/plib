from g import *

output_stream = open("out/helloworld.ps", "w")
ginitialize(output_stream)
setOrientation(portrait, inches)
move(1, 1)
rectangle(5, 4)
move(3, 3)
text("Hello, world")
