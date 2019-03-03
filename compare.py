import numpy as np
from ArtistMatrix import ArtistMatrix as AM
import os
import matplotlib.pyplot as plt
GENRE = 'rock and alt'
PATH = '{}/song lyrics/'.format(GENRE)
artists = []
for artist in os.listdir(PATH):
    artists.append(artist)


dist = np.zeros((len(artists),len(artists)))
songs = []
words = []
for i in range(len(artists)):
    one = AM(GENRE,artists[i])
    songs.append(one.songs)
    words.append(one.size)
    for j in range(i+1,len(artists)):
        two = AM(GENRE,artists[j])
        dist[i,j] = one.compare_to(two)
        dist[j,i] = dist[i,j]
        del(two)
    del(one)

np.save('words_per_song_{}'.format(GENRE),np.array([songs,words]))   
np.save('distance_common_words_{}'.format(GENRE),dist)   

from sklearn import manifold

mds = manifold.MDS(n_components=2,dissimilarity='precomputed')
pos = mds.fit(dist).embedding_

from ActiveYears import ActiveYears
ay = ActiveYears()
y = [ay.active(art) for art in artists]
size = np.array(words) / np.array(songs)
plt.scatter(pos[:,0],pos[:,1],c=y,s=size**1.5)
for i in range(len(artists)):
    plt.text(pos[i,0]+50,pos[i,1]+20,artists[i])
plt.xticks([])
plt.yticks([])   
plt.colorbar()  
plt.show()