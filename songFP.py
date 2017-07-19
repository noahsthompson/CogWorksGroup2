import librosa
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from IPython.display import Audio
import collections
import numpy as np


#%matplotlib notebook

''' ------------- Sample Song ----------- remember to replace filepath 
fig, ax = plt.subplots()
samples, fs = librosa.load(r"/Users/ji-macbook15/Desktop/moo/1.mp3", sr=44100, mono=True) #song number 1
S, freqs, times, im = ax.specgram(samples[::100], NFFT=4096, Fs=fs,
                                                      window=mlab.window_hanning,
                                                      noverlap=(4096 // 2))
'''
class songFP:
    """ Allows the user to identify, or "fingerprint" a song
    --------------------------------------------------------

    
    """

    def __init__(self):
        '''initiates songFP class
        each song in database is in the form, '''
        self.songDatabase = {}

        database = []#rewrite add
        #database = {}
        
        '''daniel rewrote own version
        def __init__(self, load = None):
        self.songDatabase = {} # "Song Title" : (Duration(int), Song(np.array))
        self.peakDatabase = {}
        self.recordings = 0
        pass
        '''
    
    def record(self, seconds, title = "Recording"):
        """Add a recording to the database.


        Keyword arguments:
        seconds -- the duration of the recording
        title -- the name of the recording (default "Recording 1,2,3...")
        """
        #Records audio and converts from Hex to Dec
        byte_encoded_signal, sampling_rate = record_audio(seconds)   
        for e in range(len(byte_encoded_signal)):
            byte_encoded_signal[e] = np.fromstring(byte_encoded_signal[e], dtype=np.int16)
        #Saves full recording for playback
        if title == "Recording":
            self.songDatabase[title + " " + str(self.recordings + 1)] = np.hstack(byte_encoded_signal)
            self.recordings += 1
        else:
            self.songDatabase[title] = np.hstack(byte_encoded_signal)
        play_audio(byte_encoded_signal, seconds)
        #Saves recording's fingerprints
        #  self.peak datbaase = below
        # self._findPeaks(np.hstack(byte_encoded_signal))
        return None

        
    def f(array, order):
        '''
        going from analog to digital signal is incoding, basic is 16 bit encoding


        USE np.linspace(start,stop,N)
        ###returns an array that starts at the start point, stops at the stop point inclusive, and divides it so that there are N elements in array total
        also can use np.sin on all of them at once

        taking analog signal and getting our digital signal, don't need to worry about 16 bit encoding



        ##cast as 16 int numpy array cuz no need to waste space
        '''
        slic = (slice(None), slice(None), slice(None,None,-1), slice(None,None,-1), slice(None,None,-1))
        if order == "th":
            return np.copy(array[slic[2::-1]])
        if order == "tf":
            return np.copy(array[slic[:-2:-1]])
        return np.copy(array)
    
    
    def addSong(self, name, spec, frequencies, thetimes):
        ''' WARNING this funtion may not have been fully integrated into a class yet. 
        
        need to write a docstring for this function including inputs and outputs
        
        
        
        ''' 
        
        ys, xs = np.histogram(spec.flatten(), bins=len(freqs)//2, normed=True)
        dx = xs[-1] - xs[-2]
        cdf = np.cumsum(ys)*dx  # this gives you the cumulative distribution of amplitudes
        cutoff = xs[np.searchsorted(cdf, 0.77)]

        foreground = (spec >= cutoff)

        a = np.where(foreground, spec, 0)
        bins = np.argwhere(a)


        for i in range(bins.shape[0] - 1):
            for j in range(20):
                if (i + 1 + j) < bins.shape[0]:
                    t1 = np.round(thetimes[bins[i + j][1]],2)
                    f1 = np.round(frequencies[bins[i + j][0]],2)
                    t2 = np.round(thetimes[bins[i + 1 + j][1]], 2)
                    f2 = np.round(frequencies[bins[i + 1 + j][0]], 2)
                    x = (f1, f2, t2 - t1)
                    if x in database:
                        database[x].append((name,t1)) #this will increase the runtime by A LOT. We need to convert to dict
                    else:
                        database[x] = [(name, t1)]  
#     return database

        pass

    def deleteSong(self, song):
        """
        Deletes a song from the database  
        """

        pass

    def listSongs(self):
        """Lists all the songs in the database"""
        pass

    def listArtists(self):
        """Lists all the artists in the database w/o repeats"""

    def findPeaks():#Roger write this
        """ """
        
        pass

    def match_song(db, excerpt): #note to self: excerpt = [(f1,f2,deltaT),(),]
        templist = []
        for notes in excerpt:
            if (notes in database):
                templist.append(tuple(database[notes]))
        counts = collections.Counter(templist)
        return counts.most_common()[0][0][0]








