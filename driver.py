from imports import *
from text2vid import *
from preprocessing import *
from summarize import *
import sys

if len(sys.argv) != 3:
    exit(0)

v = Video(sys.argv[1])
b = BingImage()

file = open(sys.argv[2], "r")
corpus = file.read()
# os.system('rm {0}'.format(sys.argv[2]))

search_queries, sentences = fetch_search_queries(corpus)

print search_queries, sentences

print(len(search_queries))
print(len(sentences))

img_url = []

for query in search_queries:
    print query
    if len(query) == 0:
        continue
    img_url.append(b.fetch_image(query))

for i in range(len(img_url)):
    v.add_part(os.path.join('img', img_url[i]), sentences[i])

v.generate_video()


file = open("webapp/sum/sum{0}.txt".format(sys.argv[1]), "w")
summary = summarize_text(corpus)
for summary_ in summary:
    print(summary_)
    file.write(summary_)
    file.write('\n')

file.close()