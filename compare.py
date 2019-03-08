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
dist = np.load('distance_syllables_combine.npy')
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
maximum = np.int_(np.rint(dist_temp.max()+25))
minimum = np.int_(np.rint(dist_temp.min()-25))

step = 1
function_array = np.zeros((len(dist), len(range(minimum, maximum, step))))
fig = plt.figure()
for i in range(len(dist)):
    for j in range(len(range(minimum, maximum, step))):
        array = dist[:,i]
        temp = array < (minimum + j * step)
        array = array[temp]
        temp = 0 < array
        function_array[i,j] = len(array[temp])
    plt.title("Number of alternative artists that are located within \n a certain distance from other alternative artists based on common words Markovs matrix")
    plt.xlabel('Distance, Standard Unit')
    plt.ylabel('Number of Artists within current Distance') 
    plt.plot(range(minimum, maximum, step), function_array[i,:], label=artists[i])
    plt.legend() 

#Use this for syl.
dist_temp = dist[~np.eye(dist.shape[0],dtype=bool)].reshape(dist.shape[0],-1)
maximum = dist_temp.max() + 0.30
minimum = dist_temp.min() - 0.30
t = np.linspace(minimum,maximum,100)
dt = t[1]-t[0]
function_array = np.zeros((len(dist), len(t)))
fig = plt.figure()
for i in range(len(dist)):
    for j in range(len(t)):
        array = dist[:,i]
        temp = array < (minimum + j * dt)
        function_array[i,j] = len(array[temp])
    plt.title("Number of rap artists that are located within \n a certain distance from other rap artists based on syllables Markovs matrix")
    plt.xlabel('Distance, Standard Unit')
    plt.ylabel('Number of Artists within current Distance')    
    plt.plot(t, function_array[i,:], label=artists[i])
    plt.legend()    

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
        dist[i,j] = one.compare_to(two,'words')
        dist[j,i] = dist[i,j]
        del(two)
    del(one)
   
np.save('distance_words_combine',dist)

# Analys of combined data
    
#Use this for word/word length
dist_temp = dist[~np.eye(dist.shape[0],dtype=bool)].reshape(dist.shape[0],-1)
mean = dist_temp.mean()
maximum = np.int_(np.rint(dist_temp.max())) + 5000
minimum = np.int_(np.rint(dist_temp.min())) - 1000

step = 1
function_array = np.zeros((len(dist), len(range(minimum, maximum, step)),3))
for i in range(len(dist)):
    for j in range(len(range(minimum, maximum, step))):
        array = dist[:,i]
        array = np.delete(array, i)
        temp = array < (minimum + j * step)
        rap = dist[0:21,i]
        alt = dist[21:40,i]
        if (i<=20):
            rap = np.delete(rap, i)
        else:
            alt = np.delete(alt, i - 21)
        temp1 = rap < (minimum + j * step)        
        temp2 = alt < (minimum + j * step)
        function_array[i,j,0] = array[temp].size
        function_array[i,j,1] = rap[temp1].size
        function_array[i,j,2] = alt[temp2].size

fig = plt.figure()
for i in range(21):
    plt.subplot(1, 2, 1)
    plt.subplot(1, 2, 1).set_title("Number of rap artists that are located within \n a certain distance from other rap artists based on words length Markovs matrix")
    plt.xlabel('Distance, Standard Unit')
    plt.ylabel('Number of Artists within current Distance')
    plt.plot(range(minimum, maximum, step), function_array[i,:,1], label=artists[i])
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.subplot(1, 2, 2).set_title("Number of alternative artists that are located within a \n certain distance from other rap artists based on words length Markovs matrix")
    plt.xlabel('Distance, Standard Unit')
    plt.ylabel('Number of Artists within current Distance')
    plt.plot(range(minimum, maximum, step), function_array[i,:,2], label=artists[i])
    plt.legend()   


fig = plt.figure()
for i in range(21,40):
    plt.subplot(1, 2, 1)
    plt.subplot(1, 2, 1).set_title("Number of rap artists that are located within a \n certain distance from alternative artists based on words length Markovs matrix")
    plt.xlabel('Distance, Standard Unit')
    plt.ylabel('Number of Artists within current Distance')
    plt.plot(range(minimum, maximum, step), function_array[i,:,1], label=artists[i])
    plt.legend()   
    plt.subplot(1, 2, 2)
    plt.subplot(1, 2, 2).set_title("Number of alternative artists that are located within a \n certain distance from other alternative artists based on words length Markovs matrix")
    plt.xlabel('Distance, Standard Unit')
    plt.ylabel('Number of Artists within current Distance')
    plt.plot(range(minimum, maximum, step), function_array[i,:,2], label=artists[i])
    plt.legend()    
    
#Use this for word syl.
dist_temp = dist[~np.eye(dist.shape[0],dtype=bool)].reshape(dist.shape[0],-1)
maximum = dist_temp.max() + 0.5
minimum = dist_temp.min() - 0.5
t = np.linspace(minimum,maximum,100)
dt = t[1]-t[0]
function_array = np.zeros((len(dist), len(t), 3))
for i in range(len(dist)):
    for j in range(len(t)):
        array = dist[:,i]
        array = np.delete(array, i)
        temp = array < (minimum + j * dt)
        rap = dist[0:21,i]
        alt = dist[21:40,i]
        if (i<=20):
            rap = np.delete(rap, i)
        else:
            alt = np.delete(alt, i - 21)
        temp1 = rap < (minimum + j * dt)        
        temp2 = alt < (minimum + j * dt)
        function_array[i,j,0] = array[temp].size
        function_array[i,j,1] = rap[temp1].size
        function_array[i,j,2] = alt[temp2].size

fig = plt.figure()
for i in range(21):
    plt.subplot(1, 2, 1)
    plt.subplot(1, 2, 1).set_title("Number of rap artists that are located within a \n certain distance from other rap artists based on syllables Markovs matrix")
    plt.xlabel('Distance, Standard Unit')
    plt.ylabel('Number of Artists within current Distance')
    plt.plot(t, function_array[i,:,1], label=artists[i])
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.subplot(1, 2, 2).set_title("Number of alternative artists that are located within a \n certain distance from rap artists based on syllables Markovs matrix")
    plt.xlabel('Distance, Standard Unit')
    plt.ylabel('Number of Artists within current Distance')
    plt.plot(t, function_array[i,:,2], label=artists[i])
    plt.legend()   


fig = plt.figure()
for i in range(21,40):
    plt.subplot(1, 2, 1)
    plt.subplot(1, 2, 1).set_title("Number of rap artists that are located within a \n certain distance from alternative artists based on syllables Markovs matrix")
    plt.xlabel('Distance, Standard Unit')
    plt.ylabel('Number of Artists within current Distance')
    plt.plot(t, function_array[i,:,1], label=artists[i])
    plt.legend()   
    plt.subplot(1, 2, 2)
    plt.subplot(1, 2, 2).set_title("Number of alternative artists that are located within a \n certain distance from other alternative artists based on syllables Markovs matrix")
    plt.xlabel('Distance, Standard Unit')
    plt.ylabel('Number of Artists within current Distance')
    plt.plot(t, function_array[i,:,2], label=artists[i])
    plt.legend()        
    
   

        
        
    
    