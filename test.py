from PIL import Image, ImageTk
from tkinter import PhotoImage
import multiprocessing as mp
from local_libs.openvibe_tool import *
from local_libs.private_tool import *
import tkinter as tk
import numpy as np
import itertools
import random
import os

def random_sequence():
    seq = [0, 1, 2, 3] # 상하좌우
    arr1 = list(itertools.permutations(seq, 4))
    arr2 = arr1.copy()
    random.shuffle(arr1)
    random.shuffle(arr2)
    print(arr1+arr2[:6])
    np.save(f"{currDir}/src/data/arr.npy", np.array(arr1+arr2[:6]))



class ArrowDisplayApp:
    def __init__(self, root, arr, signal_ls):
        self.p1 = mp.Process(target=self.process_receive, name="receiver", args=[signal_ls])
        self.p1.start()
        self.root = root
        self.root.title("Arrow Display App")
        self.root.attributes('-fullscreen', True)
        self.currDir = os.getcwd()
        self.arrow_images = [
            self.currDir+"/src/images/arrow_up.png",
            self.currDir+"/src/images/arrow_down.png",
            self.currDir+"/src/images/arrow_left.png",
            self.currDir+"/src/images/arrow_right.png"
        ]
        self.session = 0
        self.arr = arr
        self.current_arrow_index = 0
        self.arrow_label = None
        self.a = None
        self.dot_label = None
        self.btnStart = None
        self.root.configure(bg='white')
        self.update_arrow_image()
        self.root.after(0, self.initial_window)

    def process_receive(self, signal_ls):
        lsl = LSL()
        lsl.connect()
        lsl.inlet.flush()
        while True:
            signal = lsl.receiveData()
            signal_ls.append(signal)
        
    def clear_window(self):
        if self.arrow_label:
            self.arrow_label.destroy()
        if self.a:
            self.a.destroy()
        if self.dot_label:
            self.dot_label.destroy()
        if self.btnStart:
            self.btnStart.destroy()

    def btnStartCmd(self):
        # if self.isConnected:
        self.display_none(5000, 1)

    def initial_window(self):
        self.clear_window()
        self.a = tk.Label(self.root, width=200, height=20, background="white")
        self.a.pack()
        self.btnStart = tk.Button(self.root, width=12, height=4,text="Start", command=self.btnStartCmd)
        self.btnStart.pack()


    def update_arrow_image(self):
        image_path = self.arrow_images[self.arr[self.session][self.current_arrow_index]]
        arrow_image = Image.open(image_path)
        ratio = 0.5
        arrow_image = arrow_image.resize((round(arrow_image.size[0]*ratio), round(arrow_image.size[1]*ratio)), Image.ANTIALIAS)
        self.arrow_photo = ImageTk.PhotoImage(arrow_image)
        dot_image = Image.open(self.currDir+"/src/images/dot.png")
        dot_image = dot_image.resize((766, 766), Image.ANTIALIAS)
        self.dot_photo = ImageTk.PhotoImage(dot_image)

    def display_next_arrow(self):
        self.update_arrow_image()
        self.a = tk.Label(self.root, width=200, height=12, background="white")
        self.a.pack()
        self.arrow_label = tk.Label(self.root, image=self.arrow_photo, background="white")
        self.arrow_label.pack()
        self.current_arrow_index += 1
        if self.current_arrow_index == 4:
            self.root.after(4000, self.display_none, 15000, 1)
            self.current_arrow_index = 0
            self.session += 1
            print(self.session)
            if self.session==2:
                # signal_array = np.array([np.array(i) for i in list(signal_ls)])
                # print(signal_array)
                # np.save(f"{self.currDir}/signal.npy", signal_array)
                saveJson(f"{self.currDir}/src/data/signal.json", list(signal_ls))
                self.p1.kill()
                self.root.quit()
            
        else:
            self.root.after(4000, self.display_none, 3000, 2)

    def display_none(self, ms, flag):
        self.clear_window()
        if flag==1:
            """세션 종료"""
            self.root.after(ms, self.display_dot)
        else:
            """Trial 종료"""
            self.root.after(ms, self.display_next_arrow)
        

    def display_dot(self):
        self.clear_window()
        self.dot_label = tk.Label(self.root, image=self.dot_photo, background="white")
        self.dot_label.pack()
        self.root.after(7000, self.display_next_arrow)


if __name__ == "__main__":
    currDir = os.getcwd()
    manager = mp.Manager()
    signal_ls = manager.list()
    arr = np.load(f"{currDir}/src/data/arr.npy")
    print(arr)
    root = tk.Tk()
    app = ArrowDisplayApp(root, arr, signal_ls)
    root.mainloop()