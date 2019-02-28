import numpy as np
import os
import re 
rand = np.random

class ArtistMatrix:
    def __init__(self,genre,artist,size=15000):
        '''initializes the artist matrix'''
        
        self.M = np.zeros((size,size))
        self.ind_dict = {}
        self.artist = artist
        self.genre = genre
        self.next_ind = 0
        self.size = size
        self.songs = 0
        self.ARTIST_PATH = '{}/song lyrics/{}/'.format(genre,artist)
        for song in os.listdir(self.ARTIST_PATH):
            self.songs += 1
            f = open(os.path.join(self.ARTIST_PATH,song))
            for line in f:
                # remove special characters
                line = re.sub(r',|\(|\)|\!|\?|\.|(\[.*\])|\"', '', line)
                words = line.split()
                if len(words) > 0: # case of empty lines
                    for w1,w2 in zip(['_start_'] + words,words + ['_end_']):
                        w1 = w1.lower()
                        w2 = w2.lower()
                        if w1 not in self.ind_dict.keys():
                            self.__add_word(w1)
                        if w2 not in self.ind_dict.keys():
                            self.__add_word(w2)
                        self.__update_entry(w1,w2)
            f.close()
        self.__normalize()
        print(self.artist,self.size)
            
    def __add_word(self,word):
        '''adds a word to the vocabulary of the artist'''
        self.ind_dict.update({word:self.next_ind})
        self.next_ind += 1
        if self.next_ind >= self.size:
            self.__enlarge()
    
    def __update_entry(self,w1,w2):
        '''adds an occurance of of w1 following w2'''
        c = self.ind_dict[w1]
        r = self.ind_dict[w2]
        self.M[r,c] += 1
        
    def __normalize(self):
        '''finishes initialization by making all columns sum to one, and 
        trimming the extra rows and columns off the matrix'''
        self.M = self.M[0:self.next_ind,0:self.next_ind]
        # end always goes to start
        self.M[self.ind_dict['_start_'],self.ind_dict['_end_']] = 1
        s = self.M.sum(axis=0)
        self.M /= s
        self.size = len(self.ind_dict)
        
    def get_entry(self,w1,w2):
        '''returns probability of w2 following w1'''
        if w1 in self.ind_dict.keys() and w2 in self.ind_dict.keys():
            c = self.ind_dict[w1]
            r = self.ind_dict[w2]
            return self.M[r,c]
        else:
            return -1
        
    def compare_to(self,other,method='common'):
        '''compares this artists matrix to other's matrix'''
        if method == 'common':
            return self.__common_dist(other)
        else:
            print('not a valid distance')
    
    def __common_dist(self,other):
        '''compares two artists based on the words in their shared vocabulary'''
        print('comparing',self.artist,'and',other.artist)
        my_inds = []
        your_inds = []
        for word in self.ind_dict.keys():
            if word in other.ind_dict.keys():
                my_inds.append(self.ind_dict[word])
                your_inds.append(other.ind_dict[word])
        print('common words',len(my_inds))      
        my_cols = self.M[:,my_inds]
        me = my_cols[my_inds,:]
        your_cols = other.M[:,your_inds]
        you = your_cols[your_inds,:]
        return np.sum((me-you)**2)
    
    def __enlarge(self):
        '''makes the matrix bigger during initialization, if more 
        space is needed'''
        print('making it bigger')
        self.size += 200
        m = np.zeros((self.size,self.size))
        m[0:self.size-200,0:self.size-200] = self.M
        self.M = m
        del(m)
        
    def generate(self,n=5,start='_start_'):
        '''generate a string of lyrics, n lines long'''
        if type(start) == str:
            start = [start]*n
        lines = []
        words = list(self.ind_dict.keys())
        inds = list(self.ind_dict.values())
        for i in range(n):
            line = ''
            if start[i] not in self.ind_dict.keys():
                raise ValueError(start[i],'not in vocabulary of',self.artist)
            prev = start[i]
            while prev != '_end_':
                line += (prev != '_start_') * (prev + ' ')
                curr_ind = self.ind_dict[prev]
                nxt_ind = rand.choice(np.arange(self.size),p=self.M[:,curr_ind])
                prev = words[inds.index(nxt_ind)]
            lines.append(line)
        return lines
                
              