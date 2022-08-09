from sklearn.svm import LinearSVC 
import numpy as np
import cv2 as cv
import PIL 
import os

# Global Variable for Camera.
# reshape_value = width * height (of the saved picture)
reshape_value = 16800

class Model:

    

    def __init__(self):
        self.model = LinearSVC()
    
    def train_model(self, counters):
        img_list = np.array([])
        class_list = np.array([])

        counters[0] = len([f for f in os.listdir("1")
                if os.path.isfile(os.path.join("1", f))])

        counters[1] = len([f for f in os.listdir("2")
                if os.path.isfile(os.path.join("2", f))])
        

        for i in range(1, counters[0]):
            img = cv.imread(f'1/frame{i}.jpg')[:,:,0]
            img = img.reshape(reshape_value) # 640x480 RES. Check yours
            img_list = np.append(img_list,[img])
            class_list = np.append(class_list,1)

        for i in range(1, counters[1]):
            img = cv.imread(f'2/frame{i}.jpg')[:,:,0]
            img = img.reshape(reshape_value) # 150x112 RES. Check yours
            img_list = np.append(img_list,[img])
            class_list = np.append(class_list,2)

        img_list = img_list.reshape(counters[0] - 1 + counters[1] - 1, reshape_value)
        self.model.fit(img_list,class_list)
        print("Model Successfully Trained!")

    def predict(self,frame):
        frame = frame[1]
        cv.imwrite("frame.jpg", cv.cvtColor(frame, cv.COLOR_RGB2GRAY))

        img = PIL.Image.open("frame.jpg")
        img.thumbnail((150, 150), PIL.Image.ANTIALIAS)
        img.save("frame.jpg")

        #Reshape
        img = cv.imread('frame.jpg')[:, :, 0]
        img = img.reshape(reshape_value)

        #Do the prediction
        prediction = self.model.predict([img])

        return prediction[0]