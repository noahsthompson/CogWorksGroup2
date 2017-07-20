
#%matplotlib notebook Uncomment to run in jupyter
import matplotlib.pyplot as plt
import skimage.io as io
import numpy as np

from camera import save_camera_config, take_picture
from dlib_models import load_dlib_models

class facial:
    
    def __init__(self):
        self.database = []
        pass
    
    def camera(self, port=0, exposure=0.2):
        save_camera_config(port, exposure)
        img_array = take_picture()
        self.database.append(img_array)
        
ok = facial()
ok.camera()



 
@load_dlib_models
def detect(img, upscale = 1):
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
    
    faceList = np.zeros((len(detections), 128))
    
    
    for it in range(len(detections)):
        det = detections[it]
        shape = shape_predictor(img, det)
        descriptor = np.array(face_rec_model.compute_face_descriptor(img, shape))
        faceList[it] = descriptor
    
    return faceList


