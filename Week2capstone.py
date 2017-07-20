%matplotlib notebook
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
    
    def __init__(self,loadFile=None):
        if(loadFile==None):
            self.faceData=[]
            
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
    def add(self,name,descriptor):
        """ add: adds new face to database, or averages new descriptor with name already in database
            params:
            name(str)- Name of new face
            descriptor(np.array)- (128,) array of descriptors"""
        # gets the array of names
        for face in self.faceData:
            if face[0] == name:

                face[1] = (face[1]*face[2] + descriptor)/(face[2]+1)
                face[2] += 1
        self.faceData.append([name, descriptor, 1])
        pass
            
            
    def saveFile():
        pass
    #database shape: np.array((name1, vector1), (name2, vector2), etc.)
    def match(self, imgvector):
        #vector.shape: (128,)
        closest_person = "" #most similar person
        minDist =109. #distance w/ most similar person
        
        for face in self.faceData: #look thru every face in db
            l2 = np.sqrt(np.sum((face[1] - imgvector)**2))#distance between db face and the given face
            if (l2 < minDist): #if l2 is smaller
                minDist = l2
                closest_person = face[0]
        if (minDist > 0.5):
            return "unknown"
        else:
            print('probably, ')
            print('l2, ', l2)
            return closest_person
 
        
    def addCamera(self, name, port=0, exposure=0.2):
        save_camera_config(port, exposure)
        img_array = take_picture()
        self.add(name,img_array)
        

        
    @load_dlib_models
    def img_to_array(self, img, upscale = 1):
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
    
    def detectFromImg(self, img, upscale = 1):
        faces = self.img_to_array(img)
        print(faces.shape)
        people = []
        for face in faces:
            people.append(self.match(face))
        return people
'''   
test = faceDatabase()
#print(test.img_to_array(io.imread("obama.jpg")))
test.add('obama', test.img_to_array(io.imread("obama.jpg")))
test.add('obama', test.img_to_array(io.imread("obama2.jpg")))
test.add('noah', test.img_to_array(io.imread("noah_thompson1.jpg")))
test.add('noah', test.img_to_array(io.imread("noah_thompson2.jpg")))
test.add('noah', test.img_to_array(io.imread("noah_thompson3.jpg")))
#test.addCamera('roger')
#test.add('noah', test.img_to_array(io.imread("noah_thompson4.png")))
#test.add('noah', test.img_to_array(io.imread("noah_thompson5.png")))
test.detectFromImg(test.camera())

'''
