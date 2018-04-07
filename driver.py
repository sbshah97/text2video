from text2vid import *

v = Video()
b = BingImage()

text_sentences = ["Tipu Sultan", "Lenin from Russia."]
img_url = []

for text in text_sentences:
    img_url.append(b.fetch_image(text))

for i in range(len(img_url)):
    v.add_part(os.path.join('img', img_url[i]), text_sentences[i])

v.generate_video()

# v.add_part("/home/salman-bhai/All-Projects/text2video/lenin-660113_960_720.jpg",
#            "Lenin stud banda tha")
# v.generate_video()
