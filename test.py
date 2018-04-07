from text2vid import *

v = Video()
v.add_part("space.png", "Give me some space.")
v.add_part("code.png", "Hello World! Let's Code.")
v.generate_video()
