import os

import numpy as np
from bs4 import BeautifulSoup
import requests
import json
import time

agent = 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) \
        Gecko/20100101 Firefox/24.0'
headers = {'User-Agent': agent}
base = "https://www.azlyrics.com/"


def artists(letter):
    if letter.isalpha() and len(letter) is 1:
        letter = letter.lower()
        url = base+letter+".html"
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.content, "html.parser")
        data = []

        for div in soup.find_all("div", {"class": "container main-page"}):
            links = div.findAll('a')
            for a in links:
                data.append(a.text.strip())
        return json.dumps(data)
    else:
        raise Exception("Unexpected Input")


def songs(artist):
    artist = artist.lower().replace(" ", "")
    first_char = artist[0]
    url = base+first_char+"/"+artist+".html"
    req = requests.get(url, headers=headers)

    artist = {
        'artist': artist,
        'albums': {}
    }

    soup = BeautifulSoup(req.content, 'html.parser')

    all_albums = soup.find('div', id='listAlbum')
    first_album = all_albums.find('div', class_='album')
    album_name = first_album.b.text
    songs = []

    for tag in first_album.find_next_siblings(['a', 'div']):
        if tag.name == 'div':
            artist['albums'][album_name] = songs
            songs = []
            if tag.b is None:
                pass
            elif tag.b:
                album_name = tag.b.text

        else:
            if tag.text is "":
                pass
            elif tag.text:
                songs.append(tag.text)

    artist['albums'][album_name] = songs

    return (json.dumps(artist))


def lyrics(artist, song):
    artist = artist.lower().replace(" ", "")
    song = song.lower().replace(" ", "")
    url = base+"lyrics/"+artist+"/"+song+".html"

    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")
    lyrics = soup.find_all("div", attrs={"class": None, "id": None})
    if not lyrics:
        return {'Error': 'Unable to find '+song+' by '+artist}
    elif lyrics:
        lyrics = [x.getText() for x in lyrics]
        return lyrics


def make_pairs(corpus):
    for i in range(len(corpus)-1):
        yield (corpus[i], corpus[i+1])


def update_dict(pairs):
    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]
        if word_1[0].isupper():
            starting_words.append(word_1)


SPEECH_PATH = './hip hop/song lyrics/'
word_dict = {}
starting_words = []

song_number = 0

# for artist in os.listdir(SPEECH_PATH):
#     for song in os.listdir(SPEECH_PATH + artist + '/'):
#         song_number = song_number + 1
#         song_path = SPEECH_PATH + artist + '/'
#         with open(f'{song_path}{song}', encoding='latin-1') as speech:
#             contents = speech.read()
#             corpus = contents.split()
#             pairs = make_pairs(corpus)
#             update_dict(pairs)

for song in os.listdir(SPEECH_PATH + "Eminem" + '/'):
        song_number = song_number + 1
        song_path = SPEECH_PATH + "Eminem" + '/'
        with open(f'{song_path}{song}', encoding='latin-1') as speech:
            contents = speech.read()
            corpus = contents.split()
            pairs = make_pairs(corpus)
            update_dict(pairs)

print(song_number)
first_word = np.random.choice(starting_words)
chain = [first_word]
n_words = 60
for i in range(n_words):
    chain.append(np.random.choice(word_dict[chain[-1]]))
print(' '.join(chain))
