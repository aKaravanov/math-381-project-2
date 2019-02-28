from azlyrics import Azlyrics
import os
import time
import random
import sys
from http.client import RemoteDisconnected
def pull_lyrics(GENRE):
	SONG_NAMES = GENRE + '/song names/'
	LYRICS = GENRE + '/song lyrics/'
	if not os.path.exists(LYRICS):
		os.makedirs(LYRICS)
	flag = True
	resume = False
	while(flag):
		r = input('resume? (y/n) ')
		if r == 'y':
			resume = True
			wa = 'r+'
			flag = False
		elif r == 'n':
			wa = 'w'
			print('overwriting')
			flag = False

	completed = open(GENRE + '/completed.txt',wa)
	failed = open(GENRE + '/failed.txt',wa)
	if resume:
		comp = completed.read().split('\n')
		fail = failed.read().split('\n')
		
	for path in os.listdir(SONG_NAMES):
		artist = path[:-4]
		if artist.lower()[0:2] == 'a ':
			artist = artist[2:]
		elif artist.lower()[0:4] == 'the ':
			artist = artist[4:]

		f = open(SONG_NAMES + path)
		if not os.path.exists(LYRICS + artist):
			os.makedirs(LYRICS + artist)
		for song in f:
			# strip special characters from song name
			song = song.rstrip()
			song_strip = ''.join(e for e in song if e.isalnum())
			s = artist + ':' + song
			if (not resume) or (s not in comp and s not in fail):
				print('fetching',artist,song)
				az = Azlyrics(artist,song)
				try:
					lyrics = az.format_lyrics(az.get_lyrics())
					out = open(LYRICS + artist + '/' + song_strip + '.txt','w')
					out.write(lyrics)
					out.close()
					completed.write(s + '\n')
				except(ValueError):
					failed.write(s + '\n')
					print('FAILED')
					print()
				except(Exception) as e:
					print(e)
					import ctypes 
					ctypes.windll.user32.MessageBoxW(0, "something fucked up", "we done", 1)
					f.close()
					completed.close()
					failed.close()
					sys.exit(1)

				time.sleep(10 + 5*random.random())
			
		f.close()

	completed.close()
	failed.close()

gen = input('genre folder?\n')
pull_lyrics(gen)
print('whats up')
