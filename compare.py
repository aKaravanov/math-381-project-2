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
        dist[i,j] = one.compare_to(two,'common')
        dist[j,i] = dist[i,j]
        del(two)
    del(one)
   
np.save('distance_common_words_{}'.format(GENRE),dist)   

from sklearn import manifold
dist = np.load('distance_syllables_hip hop.npy')
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

#New Plots

#Use this for word/word length
dist_temp = dist[~np.eye(dist.shape[0],dtype=bool)].reshape(dist.shape[0],-1)
mean = dist_temp.mean()
maximum = np.int_(np.rint(dist_temp.max()))
minimum = np.int_(np.rint(dist_temp.min()))

step = 1
function_array = np.zeros((len(dist), len(range(minimum, maximum, step))))
for i in range(len(dist)):
    for j in range(len(range(minimum, maximum, step))):
        array = dist[:,i]
        temp = array < (minimum + j * step)
        function_array[i,j] = len(array[temp])
    plt.plot(range(minimum, maximum, step), function_array[i,:])
plt.show()

#Use this for syl.
dist_temp = dist[~np.eye(dist.shape[0],dtype=bool)].reshape(dist.shape[0],-1)
maximum = dist_temp.max()
minimum = dist_temp.min()  
t = np.linspace(minimum,maximum,100)
dt = t[1]-t[0]
function_array = np.zeros((len(dist), len(t)))
for i in range(len(dist)):
    for j in range(len(t)):
        array = dist[:,i]
        temp = array < (minimum + j * dt)
        function_array[i,j] = len(array[temp])
    plt.plot(t, function_array[i,:])    

plt.show()    

# Comp between genres
PATH = 'combine/'
artists = []
for GENRE in os.listdir(PATH):
    PATH = 'combine/{}/song lyrics/'.format(GENRE)
    for artist in os.listdir(PATH):
        artists.append(artist)
        
dist = np.zeros((len(artists),len(artists)))
songs = []
words = []
for i in range(len(artists)):
    genre_one = int((i-1)/20)
    if (genre_one==0):
        GENRE = "hip hop"
    elif (genre_one==1):
        GENRE = "rock and alt"    
    one = AM(GENRE,artists[i])
    songs.append(one.songs)
    words.append(one.size)
    for j in range(i+1,len(artists)):
        genre_two = int((j-1)/20)
        if (genre_two==0):
            GENRE = "hip hop"
        elif (genre_two==1):
            GENRE = "rock and alt"  
        two = AM(GENRE,artists[j])
        dist[i,j] = one.compare_to(two,'syllables')
        dist[j,i] = dist[i,j]
        del(two)
    del(one)
   
np.save('distance_syllables_combine',dist)

# Analys of combined data
    
#Use this for word/word length
dist_temp = dist[~np.eye(dist.shape[0],dtype=bool)].reshape(dist.shape[0],-1)
mean = dist_temp.mean()
maximum = np.int_(np.rint(dist_temp.max()))
minimum = np.int_(np.rint(dist_temp.min()))

step = 1
function_array = np.zeros((len(dist), len(range(minimum, maximum, step)),3))
for i in range(len(dist)):
    for j in range(len(range(minimum, maximum, step))):
        array = dist[:,i]
        temp = array < (minimum + j * step)
        array = array[temp]
        temp = 0 < array
        rap = dist[0:20,i]
        temp1 = rap < (minimum + j * step)
        rap = rap[temp1]
        temp1 = 0 < rap
        alt = dist[21:39,i]
        temp2 = alt < (minimum + j * step)
        alt = alt[temp2]
        temp2 = 0 < alt
        function_array[i,j,0] = len(array[temp])
        function_array[i,j,1] = len(rap[temp1])
        function_array[i,j,2] = len(alt[temp2])

fig = plt.figure()
for i in range(21):
    plt.subplot(1, 2, 1)
    plt.subplot(1, 2, 1).set_title("Distances between rap artists and other rap artists")
    plt.xlabel('Distance, Standard Unit')
    plt.ylabel('Number of Artists within current Distance')
    plt.plot(range(minimum, maximum, step), function_array[i,:,1])
    plt.subplot(1, 2, 2)
    plt.subplot(1, 2, 2).set_title("Distances between rap artists and alternative artists")
    plt.xlabel('Distance, Standard Unit')
    plt.ylabel('Number of Artists within current Distance')
    plt.plot(range(minimum, maximum, step), function_array[i,:,2])   


fig = plt.figure()
for i in range(21,40):
    plt.subplot(1, 2, 1)
    plt.subplot(1, 2, 1).set_title("Distances between alternative artists and rap artists")
    plt.xlabel('Distance, Standard Unit')
    plt.ylabel('Number of Artists within current Distance')
    plt.plot(range(minimum, maximum, step), function_array[i,:,1])
    plt.subplot(1, 2, 2)
    plt.subplot(1, 2, 2).set_title("Distances between alternative artists and other alternative artists")
    plt.xlabel('Distance, Standard Unit')
    plt.ylabel('Number of Artists within current Distance')
    plt.plot(range(minimum, maximum, step), function_array[i,:,2]) 
   

        
        
    
    