%matplotlib notebook
import matplotlib.pyplot as plt
import matplotlib.patches as patches
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
                face[1] = avgVectorIn(face[1], descriptor, face[2])
                face[2] += 1
                
                return None
        self.faceData.append([name, descriptor, 1])
        return None
            
            
    def saveFile():
        pass
    #database shape: np.array((name1, vector1, weight1), (name2, vector2, weight2), etc.)
    def match(self, imgvector):
        #vector.shape: (128,)
        closest_person = "unknown" #most similar person
        minDist = .55 #distance w/ most similar person
        confidence = 'low'
        #print(self.faceData)
        for face in self.faceData: #look through every face in db
            l2 = np.sqrt(np.sum((face[1] - imgvector)**2))#distance between db face and the given face
            if (l2 < minDist): #if l2 is smaller
                minDist = l2
                closest_person = face[0]
        if (minDist < .55):
            confidence = 'med'
        if (minDist < .4):
            confidence = 'high'
        print(minDist)
        return closest_person, confidence
 
        
        

        
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
        
        boxes = []

        for it in range(len(detections)):
            det = detections[it]
            shape = shape_predictor(img, det)
            descriptor = np.array(face_rec_model.compute_face_descriptor(img, shape))
            faceArr[it] = descriptor
            l, r, t, b = det.left(), det.right(), det.top(), det.bottom()
            boxes.append((l,r,t,b))
        return faceArr, boxes
    
    def detectFromImg(self, img, upscale = 4):
        faces = self.img_to_array(img)[0]
        conf = []
        #print(faces.shape)
        people = []
        for face in faces:
            people.append(self.match(face)[0])####
            conf.append(self.match(face)[1])
        return people, self.img_to_array(img)[1], conf
    
    def abracadabra(self):
        y = test.camera()
        people, borders, confidences = test.detectFromImg(y)
        fig,ax = plt.subplots()
        ax.imshow(y)
        color = 'red'
        for e, border in enumerate(borders):
            if confidences[e] == 'low':
                color = 'red'
            if confidences[e] == 'med':
                color = 'yellow'
            if confidences[e] == 'high':
                color = 'green'
            ax.add_patch(patches.Rectangle((border[1], border[3]),border[0]-border[1],border[2]-border[3],edgecolor = color, fill=False))
            ax.text(border[0]+2, border[3]-10, people[e], bbox={'facecolor':color, 'alpha':0.6, 'pad':1})
        print('The people in this picture are(in order):', ', '.join(people))
        
    def addCamera(self, name, port=0, exposure=0.2):
        save_camera_config(port, exposure)
        img_array = take_picture()
        face = self.img_to_array(img_array)[0]
        print('There are this many faces: ', len(face))
        if len(face) == 0:
            print(name, ' was not detected. Please try again!')
            return None
        print(img_array.shape)
        if len(face) > 1:
            print('Too many faces were detected. Please try again!')
            return None
        print(name, ' was successfully added to the database.')
        fig,ax = plt.subplots()
        ax.imshow(img_array)
        self.add(name,face)
        
    

        
        
    
test = faceDatabase()
'''
test.add('obama', test.img_to_array(io.imread("obama.jpg"))[0])
test.add('obama', test.img_to_array(io.imread("obama2.jpg"))[0])
test.add('noah', test.img_to_array(io.imread("Noah_Thompson1.jpg"))[0])
test.add('noah', test.img_to_array(io.imread("Noah_Thompson3.jpg"))[0])
'''



