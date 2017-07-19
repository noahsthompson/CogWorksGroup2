
import librosa
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from IPython.display import Audio
import collections
import numpy as np
import itertools
#%matplotlib notebook

class FPDatabase:
    """"Database of song fingerprints: 
            dictionary songDatabase:
                Key:  note transition over a certain time as expressed by a tuple (frequency1,frequency2,time) 
                Value: the set of all songs expressed in a tuple (Name, Artist) that contain that note transition
            method __init__(self,readFile=None):
                params:readFile: the filepath to a CSV file of a song dataBase to be read in
                sets dictionary to none, if readFile not None. If readFile is not None, it should specify a file to read dictionary
                values in from.
            method addSong(self,songFP,Name,Artist):
                params: songFP: numpy array of note transitions,Name: string of song name, Artist: string of artist name
                returns: none
                Adds the Name Artist tuple to the list under each  note transition in song FP
            method MatchSong(self, sampleFP):
                params: sample FP: Numpy array of note transitions in sample
                returns: name/artist tuple of best guess
                goes through each note transition in sample FP and looks up the list of name/artist values. Finds the most common name/artist pair across each note transition in sample FP.
            """
    def __init__(self,readFile=none):
        if(readFile==None):
            self.songDatabase={}
        else:
            pass
    def getNoteTransitions(self,Key):
        return self.songDatabase(Key)
    def addSong(self, songFP,Name,Artist):
        for i in songFP:
            if(self.songDatabase.has_key(i)):
                    self.songDatabase[i].add((Name,Artist))
            else:
                self.songDatabase[i]=Set([(Name,Artist)])
    def matchSong(self, sampleFP):
        songCount=[]
        for i in sampleFP:
            if(self.Database.has_key(i)):
                songCount.extend(self.Database[i])
        counts = collections.Counter(songCount)
        return counts.most_common()
        

def getForeground(Spec,frac_cut=.77,):
    ys, xs = np.histogram(S.flatten(), bins=S.size//2, normed=True)
    dx = xs[-1] - xs[-2]
    cdf = np.cumsum(ys)*dx
    cutoff = xs[np.searchsorted(cdf, frac_cut)]
    return (S >= cutoff)
def getPeaks(foreground, fp=(generate_binary_structure(rank=2,connectivity=2))):
    
    return data&peaks(data == maximum_filter(data, footprint=fp))

def getFP(Spec,freq,times,name,artist,verificationLength=20):
    foreground=getForeground(Spec)
    peaks=getPeaks(foreground)
    peakIndexs=np.argwhere(peaks)# should cast peaks from a boolean array to a int array and keep true
    FP=np.array()
    #returns array of tuples(frequency1,frequency2,time)
    for i in np.arange(len(peakIndexs)):
        for j in range(1,verificationLength+1)
            if(j<len(peakIndexs))
                f1=np.round(freq[peakIndexs[i][0]],2)
                f2=np.round(freq[peakIndexs[j][0]],2)
                dt=np.round(times[peakIndexs[j][1]]-times[peakIndexs[i][1]])
                FP=np.append(FP,np.array[(f1,f2,dt)])
    return FP

                                                        
    
