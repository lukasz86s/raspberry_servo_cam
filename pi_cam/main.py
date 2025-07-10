from tkinter import *
import cv2
#from picamera2 import Picamera2
import PIL.Image, PIL.ImageTk
import time
from external_devices import MoveCamera, Sprinkler, TogleLight
from threading import Thread
import sys

CV2_BACKEND = 0
PICAMERA2_BACKEND = 1

class Application(Frame):
    def __init__(self, master=None, backend=1,video_source=0):
        super().__init__(master)
        self.master = master
        self.grid()
        self.buttons_name = {"left": [2, 0], "up": [1, 1], "down": [2, 1], "right": [2, 2]}
        self.offset = 1
        self.master.protocol("WM_DELETE_WINDOW", self.Quit)
        
        self.move_cam = MoveCamera()
        self.sprinkler = Sprinkler()
        self.light = TogleLight("http://192.168.100.115")
        #self.move_cam.start_pwm()
        if backend == PICAMERA2_BACKEND:
            self.vid = MyVideoCapRpiCam()
        else:
            self.vid = MyVideoCapture(video_source)
        self.create_widgets()
        self.delay = 20
        self.update()
        self.master.mainloop()
        

    def Quit(self):
        self.move_cam.stop_pwm()
        if PICAMERA2_BACKEND:
            self.vid.vid.stop()
        self.destroy()
        self.master.destroy()
        sys.exit()
        
    def start_spray(self):
        Thread(target=self.sprinkler.spray).start()
        
    def update(self):

        ret, frame = self.vid.get_frame()
        self.photo = None
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=frame)
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)

        self.master.after(self.delay, self.update)

    def create_widgets(self):
        self.buttons_instance = dict()
        for name, position in zip(self.buttons_name, self.buttons_name.values()):
            self.buttons_instance[name] = Button(self, text=name)
            self.buttons_instance[name].grid(column=position[1]+self.offset, row=position[0])
        self.buttons_instance["podlej"] = Button(self, text="podlej")
        self.buttons_instance["podlej"].grid(column=0, row=1)
        self.buttons_instance["podlej"]["command"] = self.start_spray
        # create togle light button
        self.buttons_instance["togle_light"] = Button(self, text='light')
        self.buttons_instance["togle_light"].grid(column=0, row=2)
        self.buttons_instance["togle_light"]["command"] = self.light.togle_light
        # move to the up loop
        self.buttons_instance["left"]["command"] = (lambda : self.move_cam.add_to_pwm(direction="left"))
        self.buttons_instance["right"]["command"] = (lambda : self.move_cam.add_to_pwm(direction="right"))
        
        self.buttons_instance["up"]["command"] = (lambda : self.move_cam.add_to_pwm(direction="up"))
        self.buttons_instance["down"]["command"] = (lambda : self.move_cam.add_to_pwm(direction="down"))
        # Create a canvas that can fit the above video source size
        self.canvas = Canvas(self, width=self.vid.width, height=self.vid.height)
        self.canvas.grid(column=0, row=0, columnspan=5)

    def say_hi(self):
        print("hi and godby")

class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)
        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
                return (ret, frame)
            else:
                return (ret, None)
        else:
            return (None, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

class MyVideoCapRpiCam:
    def __init__(self):
        self.width = 640
        self.height = 480
        self.vid = Picamera2()
        self.vid.create_video_configuration(main={"size": (self.width, self.height)})
        #start camera
        self.vid.start()
        
    def get_frame(self):
        return (True, self.vid.capture_image("main"))

if __name__ == "__main__":
    root = Tk()
    app = Application(root)

