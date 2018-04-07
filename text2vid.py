import os, time, math
from gtts import gTTS
from moviepy.editor import *
from mutagen.mp3 import MP3
import requests

_FPS = 24
LANGUAGE = 'en'

class BingImage:
    def __init__(self):
        self.subscription_key = "5ecd1122df704d5080f7a4639f1aad98"
        self.search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
        self.headers = {"Ocp-Apim-Subscription-Key": self.subscription_key, "BingAPIs-Market": "IN"}

    def fetch_image(self,search_term):
        params = {"q": search_term, "imageType": "photo"}
        response = requests.get(self.search_url, headers=self.headers, params=params)

        response.raise_for_status()
        search_results = response.json()

        content_urls = [img["contentUrl"] for img in search_results["value"][:1]]

        for content in content_urls:
            print(content)
            file_type = content.split('/')[-1].split('.')[-1]
            filename = "img{0}.{1}".format(get_timestamp(), file_type)
            command = "wget " + content + " -O img/" + filename
            os.system(command)
            return filename


def get_timestamp():
    return int(time.time() * 1000000)


def generate_audio(text):
    audio_file = 'tmp/aud{0}.mp3'.format(get_timestamp())
    audio = gTTS(text=text, lang=LANGUAGE)
    audio.save(audio_file)
    audio = MP3(audio_file)
    duration = math.ceil(audio.info.length)
    return (audio_file, duration)


def generate_video(image, text, duration):
    video_file = 'tmp/vid{0}.mp4'.format(get_timestamp())
    os.system('ffmpeg -f image2 -r 1/{0} -i {1} -vf "fps=25,scale=w=1280:h=720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" -vcodec mpeg4 -y {2}'.format(
            duration,
            image,
            video_file
        ))
    return video_file


def format_text(string):  # break in to lines to fit the screen
    words = string.split()
    output = ''
    buffer_string = ''
    for w in words:
        if(len(buffer_string) < 50):
            buffer_string += w + ' '
        else:
            output += buffer_string + '\n'
            buffer_string = w + ' '
    output += buffer_string
    return output


class Part:

    def __init__(self, image, text):
        self.image = image
        self.text = text

    def generate_video(self):
        audio_file, duration = generate_audio(self.text)
        video_file = generate_video(self.image, self.text, duration)
        audio_clip = AudioFileClip(audio_file)
        video_clip = VideoFileClip(video_file).set_duration(
            audio_clip.duration).set_position('center').set_fps(_FPS).crossfadein(0.5)
        text_clip = TextClip(format_text(self.text), font='Arial', fontsize=200, color='white',
            bg_color='black', stroke_width=30).set_pos('bottom').set_duration(audio_clip.duration).resize(width=1000)
        result = CompositeVideoClip([video_clip, text_clip])
        result_with_audio = result.set_audio(audio_clip)
        return result_with_audio


class Video:

    def __init__(self):
        self.part_list = []

    def add_part(self, image, text):
        self.part_list.append(Part(image, text))

    def generate_video(self):
        output = 'out{0}.mp4'.format(get_timestamp())
        os.system("rm ./*.mp4")
        clips = []
        for part in self.part_list:
            clips.append(part.generate_video())
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(output)
        os.system("rm tmp/*")
        os.system("rm img/*")
        return output
        
