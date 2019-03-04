import numpy as np
from ArtistMatrix import ArtistMatrix as AM
import os
import matplotlib.pyplot as plt
GENRE = 'hip hop'
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
        dist[i,j] = one.compare_to(two,'syllables')
        dist[j,i] = dist[i,j]
        del(two)
    del(one)
   
np.save('distance_syllables_{}'.format(GENRE),dist)   

from sklearn import manifold
dist = np.load('distance_common_words_hiphop.npy')
mds = manifold.MDS(n_components=2,dissimilarity='precomputed')
pos = mds.fit(dist).embedding_

from ActiveYears import ActiveYears
ay = ActiveYears()
y = [ay.active(art) for art in artists]
#size = np.array(words) / np.array(songs)
plt.scatter(pos[:,0],pos[:,1],c=y,cmap='hot')
for i in range(len(artists)):
    plt.text(pos[i,0]+5,pos[i,1]+2,artists[i])
plt.xticks([])
plt.yticks([])   
plt.colorbar()  
plt.show()