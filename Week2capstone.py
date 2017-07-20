
%matplotlib notebook
from camera import save_camera_config, take_picture
import matplotlib.pyplot as plt

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
