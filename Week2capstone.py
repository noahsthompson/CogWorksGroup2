import matplotlib.pyplot as plt
import matplotlib.patches as patches
import skimage.io as io
import numpy as np
import time
import os
from dlib_models import load_dlib_models
from camera import save_camera_config, take_picture



class faceDatabase():
    """faceDatabase:
        fields:
        faceData- Tuple of (name(str), descriptorArray(np.array),weight(int)):
           -Name is a string corresponding to a person's face in the database
           -Descriptor array has shape (128,). 
           -Weight is the number of images that have gone into the current average, and determines how much to weight the incoming
        averages.
        Methods:
        __init__
        
        add
        
        
        
        params:
        loadFile: the directory of a comma seperated value file to be read in to faceData
        """
    
    def __init__(self,loadFile=None):
        self.faceData = []
        
        
    def loadfile(self, name, path, upscale=4, folder=False):
        if(folder == True):
            for fn in os.listdir(path):
                print(fn)
                filename = fn[:-4]
                if filename[-1] in ['0','1','2','3','4','5','6','7', '8', '9']:
                    
                    filename = filename[:-1]
                print(filename)
                self.loadfile(filename, path + "/" + fn)
            
        else:        
            img_array = io.imread("{}".format(path))[:,:,:3]
            detections = list(face_detect(img_array, upscale))

            # Loads and displays face if a SINGLE one is detected
            if len(detections) == 1:
                det = detections[0]
                l, r, t, b = det.left(), det.right(), det.top(), det.bottom()
                shape = shape_predictor(img_array, det)
                descriptor = np.array(face_rec_model.compute_face_descriptor(img_array, shape))
                assert descriptor.size == 128, "Descriptor is not of shape (128, 1)!"
                
                self.add(name, descriptor)
                fig,ax = plt.subplots()
                ax.clear()
                ax.imshow(img_array)
                ax.set_xticks([])
                ax.set_yticks([])
                ax.add_patch(patches.Rectangle((l,b), r-l, t-b, linewidth=2, edgecolor='m', facecolor='none'))
                plt.xlabel("{} has been successfully loaded!".format(name))
                
                plt.ion()
                plt.draw()
                try:
                    plt.pause(0.5)
                except Exception:
                    pass
            elif len(detections) >= 1:
                print("Error: More than 1 face detected in file given!")
            else:
                print("Error: No faces detected in file given!")
        
    def avgVectorIn(self, vtotal, vadd, weight):
        return ((vtotal * weight) + vadd)/(weight + 1)    
        
    def add(self,name,descriptor):
        """ add: adds new face to database, or averages new descriptor with name already in database
            params:
            name(str)- Name of new face
            descriptor(np.array)- (128,) array of descriptors"""
        # gets the array of names
        for face in self.faceData:
            if face[0] == name:
                face[1] = self.avgVectorIn(face[1], descriptor, face[2])
                face[2] += 1
                
                return None
        self.faceData.append([name, descriptor, 1])
        return None
            
            
    def saveFile():
        pass

    
    
    def match(self, imgvector, db = self.faceData):
        #vector.shape: (128,)
        closest_person = "?" #most similar person
        minDist = .5 #distance w/ most similar person
        confidence = 'low'
        #print(self.faceData)
        for face in db: #look through every face in db
            l2 = np.sqrt(np.sum((face[1] - imgvector)**2))#distance between db face and the given face
            if (l2 < minDist): #if l2 is smaller
                minDist = l2
                closest_person = face[0]
        if (minDist < .5):
            confidence = 'med'
        if (minDist < .35):
            confidence = 'high'
        
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
        people = []
        for face in faces:
            people.append(self.match(face)[0])####
            conf.append(self.match(face)[1])

                        
    
    def detectFromCamera(self ,wait = 0):
        time.sleep(wait)
        y = self.camera()
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
            ax.set_xticks([])
            ax.set_yticks([])
            ax.text(border[0]+2, border[3]+20, people[e], bbox={'facecolor':color, 'alpha':1, 'pad':1}, fontsize = 8)
        
        print('The people in this picture are(in order):', ', '.join(people))
        
    def addCamera(self, name, port=0, exposure=0.2, wait = 0 ):
        time.sleep(wait)
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
        
        border = test.detectFromImg(img_array)[1][0]
        fig,ax = plt.subplots()
        ax.imshow(img_array)
        ax.add_patch(patches.Rectangle((border[1], border[3]),border[0]-border[1],border[2]-border[3],edgecolor = 'pink', fill=False))
        ax.set_xticks([])
        ax.set_yticks([])
        self.add(name,face)
        
    def camera(self, port=0, exposure=0.2):
        save_camera_config(port, exposure)
        img_array = take_picture()
        if img_array == []:
            raise ValueError("No face detected") 
        return img_array
    
    def listNames(self):
        res = []
        for face in self.faceDatabase:
            res.append(face[0])
        return res
    
    def dbHave(self, name):
        return name in listNames
    
    def removeName(self, name):
        for e, face in enumerate(self.faceDatabase):
            if face[0] == name:
                del self.faceDatabase[e]
        pass

