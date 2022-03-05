#pip install opencv-python
import cv2 as cv


class Camera:

    def __init__(self):
        self.camera = cv.VideoCapture(0) 
        #Number is to select the Webcam

        if not self.camera.isOpened():
            raise ValueError("Can't open camera")

        #Height and Width of the camera
        self.width = self.camera.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.camera.get(cv.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        if self.camera.isOpened():
            self.camera.release()

    def get_frame(self):
        if self.camera.isOpened():
            ret, frame = self.camera.read()

            if ret: 
                return (ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB))
                #Change the colors for processing
            else:
                return(ret, None)
        else:
            return None