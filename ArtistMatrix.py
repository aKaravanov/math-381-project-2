import numpy as np
import os
import re 
import pyphen
rand = np.random

class ArtistMatrix:
    def __init__(self,genre,artist,size=15000):
        '''initializes the artist matrix'''
        
        self.M = np.zeros((size,size))
        # this dictionary maps words in an artists vocab to the index
        # in the transition matrix
        self.M_syl = np.zeros((20,20))
        self.pyp = pyphen.Pyphen(lang='en')
        self.ind_dict = {}
        self.syl_dict = {}
        self.artist = artist
        self.genre = genre
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
                    words1 = ['_start_'] + words
                    words2 = words + ['_end_']
                    w1_syls = ['_start_'] + \
                    [len(self.pyp.positions(w1))+1 for w1 in words]
                    w2_syls = [len(self.pyp.positions(w2))+1 for w2 in words] \
                    + ['_end_']
                    for w1,w2,w1_syl,w2_syl in zip(words1,words2,w1_syls,w2_syls):
                        w1 = w1.lower()
                        w2 = w2.lower()
                        if w1 not in self.ind_dict.keys():
                            self.__add_word(w1,self.ind_dict)
                        if w2 not in self.ind_dict.keys():
                            self.__add_word(w2,self.ind_dict)
                        if w1_syl not in self.syl_dict.keys():
                            self.__add_word(w1_syl,self.syl_dict)
                        if w2_syl not in self.syl_dict.keys():
                            self.__add_word(w2_syl,self.syl_dict)
                        self.__update_entry(w1,w2,self.ind_dict,self.M)
                        self.__update_entry(w1_syl,w2_syl,self.syl_dict,self.M_syl)
            f.close()
        self.M = self.__normalize(self.M,self.ind_dict)
        self.M_syl = self.__normalize(self.M_syl,self.syl_dict)
        print(self.artist,self.size)
            
    def __add_word(self,word,d):
        '''adds a word to the vocabulary of the artist'''
        d.update({word:len(d)})
        if len(d) >= self.size:
            self.__enlarge()
    
    def __update_entry(self,w1,w2,d,M):
        '''adds an occurance of of w1 following w2'''
        c = d[w1]
        r = d[w2]
        M[r,c] += 1
        
    def __normalize(self,M,d):
        '''finishes initialization by making all columns sum to one, and 
        trimming the extra rows and columns off the matrix'''
        M1 = M[0:len(d),0:len(d)]
        # end always goes to start
        M[d['_start_'],d['_end_']] = 1
        s = M1.sum(axis=0)
        M1 /= s
        self.size = len(self.ind_dict)
        return M1
        
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
        print('comparing',self.artist,'and',other.artist)
        if method == 'common':
            dis,common = self.__dist(self.M,self.ind_dict,
                                       other.M,other.ind_dict)
            return dis * self.size * other.size / common**2
        elif method == 'syllables':
            dis,common = self.__dist(self.M_syl,self.syl_dict,
                                       other.M_syl,other.syl_dict)
            return dis
        else:
            print('not a valid distance')
    
    def __dist(self,M,d,otherM,otherd):
        '''compares two artists matrices, returning the euclidean distance 
        only between columns/rows found in both matrices, also returns the number
        of columns/rows they have in common'''
        my_inds = []
        your_inds = []
        for word in d.keys():
            if word in otherd.keys():
                my_inds.append(d[word])
                your_inds.append(otherd[word])
        print('common words',len(my_inds))      
        my_cols = M[:,my_inds]
        me = my_cols[my_inds,:]
        your_cols = otherM[:,your_inds]
        you = your_cols[your_inds,:]
        dis = np.sqrt(np.sum((me-you)**2))
        return dis, len(my_inds)
    
    def __syllable_dist(self,other):
        '''compares artists based on how words of a certain number of syllables
        transition from one to another'''
        
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
                
              