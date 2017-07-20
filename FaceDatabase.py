import numpy as np

class faceDatabase():
    """faceDatabase:
        feilds:
        faceData- Tuple of (name(str), discriptorArray(np.array),weight(int)). Discriptor array has shape (128,). Weight
        is the number of images that have gone into the current average, and determines how much to weight the incoming
        averages.
        Methods:
        __init__
        
        params:
        loadFile: the directory of a comma seperated value file to be read in to faceData
        """
    
    def __init__(self,loadFile=None):
        if(loadFile=None):
            self.faceData=np.array([])
        else:
            pass
    def get_name(self,index)
    return self.faceData[index,0]
    def get_descrip(self,index)
    return self.faceData[index,1]
    def get_weight(self,index)
    return self.faceData[index,2]
    def add(self,name,discriptor):
        """ add: adds new face to database, or averages new discriptor with name already in database
            params:
            name(str)- Name of new face
            discriptor(np.array)- (128,) array of discriptors"""
        # gets the array of names
        names=self.get_name(slice(None,None,None))
        #Check if name already exists in database
        if (name in names):
            #gets index of face
            index=np.where(names == name)
                #Updates face data with new image
                self.faceData[index]= (name,(get_descrip(index)+discriptor)/(get_weight(index)+1),get_weight(index)+1)
        else:
            #Adds new face to database
            self.faceData=np.append(self.faceData,[(name,discriptor,1)])
    def saveFile():
        pass
    #database shape: np.array((name1, vector1), (name2, vector2), etc.)
    def match(self, imgvector):
        #vector.shape: (128,)
        closest_person = "" #most similar person
        closest_l2 = np.iinfo(np.int16).max #distance w/ most similar person
        
        for face in database: #look thru every face in db
            l2 = np.sqrt(np.sum((face[1] - imgvector)**2)) #distance between db face and the given face
            if (l2 < closest_l2): #if l2 is smaller
                closest_l2 = l2
                closest_person = face[0]
        if (l2 > 10):
            return "cant find anyone close"
        else:
            return closest_person
