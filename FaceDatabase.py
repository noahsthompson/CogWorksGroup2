#%matplotlib notebook Uncomment to run in jupyter
import matplotlib.pyplot as plt
import skimage.io as io
import numpy as np

from camera import save_camera_config, take_picture
from dlib_models import load_dlib_models

class faceDatabase():
    """faceDatabase:
        fields:
        faceData- Tuple of (name(str), discriptorArray(np.array),weight(int)). Discriptor array has shape (128,). Weight
        is the number of images that have gone into the current average, and determines how much to weight the incoming
        averages.
        Methods:
        __init__
        
        params:
        loadFile: the directory of a comma seperated value file to be read in to faceData
        """
    
    def __init__(self,loadFile == None):
        if(loadFile=None):
            self.faceData=np.array([])
            
        else:
            pass
        
    def camera(self, port=0, exposure=0.2):
        save_camera_config(port, exposure)
        img_array = take_picture()
        return img_array
        
    def get_name(self,index):
        return self.faceData[index,0]
    
    def get_descrip(self,index):
        return self.faceData[index,1]
    
    def get_weight(self,index):
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
        
    def camera(self, port=0, exposure=0.2):
        save_camera_config(port, exposure)
        img_array = take_picture()
        self.database.append(img_array)
        
    def camera(self, port=0, exposure=0.2):
        save_camera_config(port, exposure)
        img_array = take_picture()
        self.database.append(img_array)
        
    @load_dlib_models
    def detect(self, img, upscale = 1):
        '''
        takes in:
            -img: an array
            -upscale: an integer that represents the
            amount of times to upscale the img to detect
            smaller faces

        returns: a numpy array of dimensions, w, 128 with w being the number of faces
        present in the image each one having a corresponding 128 size vector.

        '''
        from dlib_models import models

        face_detect = models["face detect"]
        face_rec_model = models["face rec"]
        shape_predictor = models["shape predict"]

        detections = face_detect(img, upscale)
        detections = list(detections)

        faceArr = np.zeros((len(detections), 128))


        for it in range(len(detections)):
            det = detections[it]
            shape = shape_predictor(img, det)
            descriptor = np.array(face_rec_model.compute_face_descriptor(img, shape))
            faceArr[it] = descriptor

        return faceArr
    
    
    def loadcamera(self, name, upscale=1):
        # Takes picture
        img_array = take_picture()[:,:,:3]
        detections = list(face_detect(img_array, upscale))
        
        #Loads and displays face if a SINGLE one is detected
        if len(detections) == 1:
            det = detections[0]
            l, r, t, b = det.left(), det.right(), det.top(), det.bottom()
            shape = shape_predictor(img_array, det)
            descriptor = np.array(face_rec_model.compute_face_descriptor(img_array, shape))
            assert descriptor.size == 128, "Descriptor is not of shape (128, 1)!"
            self.database.append(("{}".format(name), descriptor))
            self.ax.clear()
            self.ax.imshow(img_array)
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.ax.add_patch(patches.Rectangle((l,b), r-l, t-b, linewidth=2, edgecolor='m', facecolor='none'))
            plt.xlabel("{} has been successfully loaded!".format(name))
            plt.show()
        else:
            print("Error: Unable to detect {}'s face!".format(name))
    
    
