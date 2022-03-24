from tkinter import *
from tkinter import ttk

import rotatix

import threading

import time

class Rotatix_Canvas(Canvas):
    @staticmethod
    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % rgb

    def run(self):
        self.iteration = self.iteration + 1 % self.rotatix_sketch.sides

        self.delete("all")
        self.render_arm_rotation(self.iteration)

    def render_arm_rotation(self, iteration=0):
        point = self.width() / 2, self.height() / 2
        coordinates = self.rotatix_sketch.rasterize(x=point[0],y=point[1],iteration=iteration)
        for color_in, color_out, x, y in coordinates:
            color = Rotatix_Canvas.rgb_to_hex(tuple(color_in))
            self.create_line(point[0], point[1], x, y, width=3, fill=color)
            point = x,y
    def __init__(self, parent, rotatix_sketch=None, **kwargs):
        Canvas.__init__(self, parent, kwargs)
        self.init(rotatix_sketch)
        self.iteration = 0
    def __str__(self):
        return "Rotatix Sketch (" + str(self.rotatix_sketch) + ")"

    def init(self, rotatix_sketch):
        self.rotatix_sketch = None

        self.set_rotatix_sketch(rotatix_sketch)

        self.iteration = 0
        self.configure(width=self.width(), height=self.height())

    def set_rotatix_sketch(self, rotatix_sketch=None):
        self.event_generate("<<Clear>>")

        if self.rotatix_sketch:
            del self.rotatix_sketch
        self.rotatix_sketch = rotatix_sketch

        total_length = self.rotatix_sketch.rasterize_size()[0] + 20
    def width(self):
        if self.rotatix_sketch:
            return self.rotatix_sketch.rasterize_size()[0] + 20
        return 0

    def height(self):
        if self.rotatix_sketch:
            return self.rotatix_sketch.rasterize_size()[1] + 20
        return 0
class Rotatix_Frame(Frame):

    def __init__(self, parent, rotatix_sketch = None):
        super().__init__(parent)
        self.canvas = Rotatix_Canvas(parent=self, rotatix_sketch=rotatix_sketch)
        self.master.title(str(self.canvas))
        self.configure(width=self.canvas.width(), height=self.canvas.height())

    def run(self):
        self.canvas.run()
        self.canvas.pack()

class Render_Thread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Render_Thread, self).__init__(*args, **kwargs)
        self._stop = threading.Event()

    # function using _stop function
    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
    def run(self):
        print("Render Thread Started!")
        app = Application.application
        while True:
            if self.stopped():
                print("Render Thread Stopped!")
                return
            else:
                print("ITERATION: " + str(app.rotatix_frame.canvas.iteration))
            time.sleep(0)
            app.rotatix_frame.run()
class Application(Tk):
    application = None

    def GetApplication(rotatix_sketch=None):
        if not Application.application:
            Application(rotatix_sketch)
        return Application.application

    def __init__(self, rotatix_sketch=None):
        super().__init__()

        Application.application = self

        self.geometry("1024x768")

        self.rotatix_frame = Rotatix_Frame(self, rotatix_sketch)
        self.rotatix_frame.grid(column=0, row=0)

        self.exit_button = ttk.Button(text="Exit", command=self.stop)
        self.exit_button.grid(column=0, row=1)

        self.render_thread = Render_Thread()

    def start(self):
        self.render_thread.start()
        self.mainloop()

        print("Main Loop Exited!")
        self.render_thread.stop()
        print("Program terminated!")

    def stop(self):
        self.render_thread.stop()