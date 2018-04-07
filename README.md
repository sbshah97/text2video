# text2video

## About

Text is boring — this system auto generates engaging narrated films from PDF textbook excerpts as follows:
1. PDF to text conversion, and text cleaning / pre-processing (Not Sure of this is Necessary)
2. Topic identification and extraction using NLP 
3. Search images by topic and download from Bing API images 
4. Create Audio for sentence using a Python text to speech library
5. Create MP4 video from images + text + audio using some Python Library 

## Installation 

The Project has been written in Python 2.7 using Flask as a basic and simple server to run the code.

### Installing Dependencies

* Clone the project in a directory on your local system.
```
git clone https://github.com/salman-bhai/text2video
cd text2video/
```

* Create a new Virtual Environment using the Python Package `virtualenv` and activate the virtual environment in it.
```
virtualenv venv
source venv/bin/activate
```

* Install the Python Dependencies in the same Python Virtual Environment by running the following command:
```
pip install -r requirements.txt
```

* You can start the server by running the following command:
```
python server.py
```

### Note:
You will need to install certain NLTK Dependencies as well to get the code to run. Kindly look open an issue in case you miss anything.

## Project Documentation

* All Project Documentation is on the Wiki and in case anything is missing kindly feel free to open up a new Issue on the Github Issue Tracker for the same.

## Project Members

* [Mohit Reddy](https://github.com/mohitreddy1996)
* [Salman Shah](https://github.com/salman-bhai)
* [Hrishi Hiraskar](https://github.com/hrily)