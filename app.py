from email.mime import image
import tkinter as tk #Graphical interface
from tkinter import simpledialog
from xml.etree.ElementTree import PI
import cv2 as cv
import os #for file handling
import PIL.Image, PIL.ImageTk
import camera
import model
import random

class App:

    def __init__(self, window = tk.Tk(), window_title = "Camera Classifier" ):
        
        self.window = window
        self.window_title = window_title

        window.title(window_title)


        self.counters = [1, 1]   #Two counters starting at 1 for images

        self.model = model.Model()
    

        self.auto_predict = False #Predict when I press button

        self.camera = camera.Camera()

        self.init_gui()

        self.delay = 15

        self.update()

        self.window.attributes('-topmost', True)
        self.window.mainloop()


    #Create GUI for the Model
    def init_gui(self):

        #Create Canvas
        self.canvas = tk.Canvas(self.window, width = self.camera.width, height = self.camera.height)
        self.canvas.pack()

        #Some Buttons

        #Auto Predict Button
        self.btn_toggleauto = tk.Button(self.window, text="Auto Prediction", width=50, command=self.auto_predict_toggle)
        #Pack it and align it to the center.
        self.btn_toggleauto.pack(anchor=tk.CENTER, expand=True)

        #Receive the two objects names to test the Model
        self.classname_one = simpledialog.askstring("Classname One", "Enter the name of the first class:", parent = self.window)
        self.classname_two = simpledialog.askstring("Classname Two", "Enter the name of the second class:", parent = self.window)

        #Save for Class 1 Button
        self.btn_class_one = tk.Button(self.window, text = self.classname_one, width=50, command=lambda: self.save_for_class(1))
        self.btn_class_one.pack(anchor=tk.CENTER, expand=True)

        #Save for Class 2 Button
        self.btn_class_two = tk.Button(self.window, text = self.classname_two, width=50, command=lambda: self.save_for_class(2))
        self.btn_class_two.pack(anchor=tk.CENTER, expand=True)

        #Train Model Button
        self.btn_train = tk.Button(self.window, text = "Train Model", width=50, command=lambda: self.model.train_model(self.counters))
        self.btn_train.pack(anchor=tk.CENTER, expand=True)

        #Predict Button
        self.btn_predict = tk.Button(self.window, text = "Predict picture", width=50, command=self.predict)
        self.btn_predict.pack(anchor=tk.CENTER, expand=True)

        #Reset Button
        self.btn_reset = tk.Button(self.window, text = "Reset", width=50, command=self.reset)
        self.btn_reset.pack(anchor=tk.CENTER, expand=True)

        #Predicted TEXT
        self.class_label = tk.Label(self.window, text = "No Class")
        self.class_label.config(font=("Arial", 20))
        self.class_label.pack(anchor=tk.CENTER, expand=True)

    def auto_predict_toggle(self):
        self.auto_predict = not self.auto_predict
        if self.auto_predict:
            print("AutoPredict is ON!")
        else:
            print("AutoPredict is OFF!")

    def save_for_class(self, class_num):
        ret, frame = self.camera.get_frame()
        if not os.path.exists("1"):
            os.mkdir("1")
        if not os.path.exists("2"):
            os.mkdir("2")
        
        #Index 0 for Class 1. Index 1 for Class 2.
        #Convert it to Grayscale for faster training. No need for colour in simple Models.

        # Generate Random Hash to save the pictures
        frame_hash = self.counters[class_num-1]

        cv.imwrite(f'{class_num}/frame{frame_hash}.jpg', cv.cvtColor(frame, cv.COLOR_RGB2GRAY))
        print("Saved " + f'{class_num}/frame{frame_hash}.jpg')

        img = PIL.Image.open(f'{class_num}/frame{frame_hash}.jpg')
        img.thumbnail((150, 150), PIL.Image.ANTIALIAS)
        img.save(f'{class_num}/frame{frame_hash}.jpg')

        self.counters[class_num - 1] += 1

    #Resets everything
    def reset(self):
        for directory in ['1','2']:
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)   #Deletes file

        self.counters = [1,1]
        self.model = model.Model()
        self.class_label.config(text='NoClass')
        print("Predictions were Reseted!")


    def update(self):
        if self.auto_predict:
            self.predict()
        ret, frame = self.camera.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0,image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def predict(self):
        frame = self.camera.get_frame()
        prediction = self.model.predict(frame)

        if prediction == 1:
            self.class_label.config(text=self.classname_one)
            return self.classname_one
        if prediction == 2:
            self.class_label.config(text=self.classname_two)
            return self.classname_two
        
        