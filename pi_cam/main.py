from tkinter import *
import cv2
import PIL.Image, PIL.ImageTk
import time
from servo_pwm import MoveCamera
import sys

class Application(Frame):
    def __init__(self, master=None, video_source=0):
        super().__init__(master)
        self.master = master
        self.grid()
        self.buttons_name = {"left": [2, 0], "up": [1, 1], "down": [2, 1], "right": [2, 2]}
        self.offset = 1
        self.master.protocol("WM_DELETE_WINDOW", self.Quit)
        
        self.move_cam = MoveCamera()
        #self.move_cam.start_pwm()

        self.vid = MyVideoCapture(video_source)
        self.create_widgets()
        self.delay = 20
        self.update()
        self.master.mainloop()
        

    def Quit(self):
        self.move_cam.stop_pwm()
        self.destroy()
        self.master.destroy()
        sys.exit()
        
    def update(self):
        # Get a frame from the video source
        #print(self.move_cam.dc_horizontal)
        #print(self.move_cam.dc_vertical)
 
        if(self.move_cam.counter >0):
            self.move_cam.counter -= 1 
        if(self.move_cam.counter == 0):
            self.move_cam.stop_servo()
            
        ret, frame = self.vid.get_frame()
        self.photo = None
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)

        self.master.after(self.delay, self.update)

    def create_widgets(self):
        self.buttons_instance = dict()
        for name, position in zip(self.buttons_name, self.buttons_name.values()):
            self.buttons_instance[name] = Button(self, text=name)
            self.buttons_instance[name].grid(column=position[1]+self.offset, row=position[0])
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
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (None, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()



if __name__ == "__main__":
    root = Tk()
    app = Application(root)

