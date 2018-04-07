from text2vid import *
from preprocessing import *
from summarize import *

v = Video()
b = BingImage()

search_queries, sentences = fetch_search_queries(corpus)

print(len(search_queries))
print(len(sentences))

# text_sentences = ["Tipu Sultan", "Lenin from Russia."]
img_url = []

for query in search_queries:
    img_url.append(b.fetch_image(query))

for i in range(len(img_url)):
    v.add_part(os.path.join('img', img_url[i]), sentences[i])

v.generate_video()

summary = summarize_text(corpus)
for summary_ in summary:
	print(summary_)