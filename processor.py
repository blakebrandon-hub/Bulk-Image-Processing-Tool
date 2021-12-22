import tkinter as tk
from tkinter.ttk import Frame
from tkinter import filedialog, messagebox
import cv2 as cv
import numpy as np
import os
import time


class MainApplication(Frame):
    def __init__(self):
        super().__init__()
        self.configure_gui()
        self.addVariablesToFrame()
        self.addLabelsToFrame()
        self.addButtonsToFrame()
        self.addCheckbuttonsToFrame()
        self.addRadiobuttonsToFrame()
        self.addInputsToFrame()

    def configure_gui(self):
        self.winfo_toplevel().title("Bulk Image Processor")
        self.master.geometry("395x185")
        self.master.resizable(False, False)
        self.icon = tk.PhotoImage(file="icon.png")
        self.master.iconphoto(False, self.icon)

    def addVariablesToFrame(self):
        self.var_resize = tk.StringVar(self.master, 'False')
        self.var_flip = tk.StringVar(self.master, 'False')
        self.var_rotate = tk.StringVar(self.master, 'False')
        self.var_degrees = tk.StringVar(self.master, '1')
        self.var_format = tk.StringVar(self.master, '1')
        self.var_scale = tk.StringVar(self.master, '1.0')
        self.var_sharpen = tk.StringVar(self.master, 'False')
        self.var_blur = tk.StringVar(self.master, 'False')
        self.var_gray = tk.StringVar(self.master, 'False')
        self.var_orient = tk.StringVar(self.master, '1')
        self.var_thresh = tk.StringVar(self.master, 'False')
        self.var_edges = tk.StringVar(self.master, 'False')
        self.count = 1
        self.image = ''
        self.source = ''
        self.dest = ''

    def addLabelsToFrame(self):
        self.lbl_scale = tk.Label(root, text='Scale: ', state='disabled')
        self.lbl_format = tk.Label(root, text='Choose Format: ')
        self.lbl_src = tk.Label(root, text='SOURCE: ')
        self.lbl_dest = tk.Label(root, text='DESTINATION: ')
        self.lbl_scale.place(x=5, y=30)
        self.lbl_format.place(x=265, y=5)
        self.lbl_src.place(x=5, y=135)
        self.lbl_dest.place(x=5, y=160)

    def addButtonsToFrame(self):
        self.btn_source = tk.Button(root, text='Source',
                                    command=self.ifSourceClicked)

        self.btn_dest = tk.Button(root, text='Destination',
                                  command=self.ifDestClicked)

        self.btn_create = tk.Button(root, text='      Create Images      ',
                                    command=self.ifCreateClicked)

        self.btn_source.place(x=265, y=75)
        self.btn_dest.place(x=315, y=75)
        self.btn_create.place(x=265, y=105)

    def addCheckbuttonsToFrame(self):
        self.chk_resize = tk.Checkbutton(root, text='Resize', variable=self.var_resize,
                                         command=self.ifResizeChecked)

        self.chk_flip = tk.Checkbutton(root, text='Flip', variable=self.var_flip,
                                       command=self.ifFlipChecked)

        self.chk_rotate = tk.Checkbutton(root, text='Rotate Clockwise', variable=self.var_rotate,
                                         command=self.ifRotateChecked)

        self.chk_sharpen = tk.Checkbutton(
            root, text='Sharpen', variable=self.var_sharpen)
        self.chk_blur = tk.Checkbutton(
            root, text='Gaussian Blur', variable=self.var_blur)
        self.chk_gray = tk.Checkbutton(
            root, text='Grayscale', variable=self.var_gray)
        self.chk_thresh = tk.Checkbutton(
            root, text='Thresholding', variable=self.var_thresh)
        self.chk_edge = tk.Checkbutton(
            root, text='Edge Detection', variable=self.var_edges)

        self.chk_resize.place(x=5, y=5)
        self.chk_flip.place(x=5, y=50)
        self.chk_rotate.place(x=5, y=90)
        self.chk_sharpen.place(x=155, y=5)
        self.chk_blur.place(x=155, y=30)
        self.chk_gray.place(x=155, y=55)
        self.chk_thresh.place(x=155, y=80)
        self.chk_edge.place(x=155, y=105)

    def addRadiobuttonsToFrame(self):
        self.rb_vertical = tk.Radiobutton(root, text='Vertical',
                                          variable=self.var_orient, value='1', state='disabled')

        self.rb_horizontal = tk.Radiobutton(root, text='Horizontal',
                                            variable=self.var_orient, value='2', state='disabled')

        self.rb_90 = tk.Radiobutton(root, text='90°', variable=self.var_degrees,
                                    value='1', state='disabled')

        self.rb_180 = tk.Radiobutton(root, text='180°', variable=self.var_degrees,
                                     value='2', state='disabled')

        self.rb_270 = tk.Radiobutton(root, text='270°', variable=self.var_degrees,
                                     value='3', state='disabled')

        self.rb_png = tk.Radiobutton(root, text='PNG', variable=self.var_format,
                                     value='1')

        self.rb_jpg = tk.Radiobutton(root, text='JPG', variable=self.var_format,
                                     value='2')

        self.rb_vertical.place(x=5, y=70)
        self.rb_horizontal.place(x=70, y=70)
        self.rb_90.place(x=5, y=110)
        self.rb_180.place(x=50, y=110)
        self.rb_270.place(x=95, y=110)
        self.rb_png.place(x=270, y=25)
        self.rb_jpg.place(x=270, y=45)

    def addInputsToFrame(self):
        self.inp_scale = tk.Entry(
            root, width=5, textvariable=self.var_scale, state='disabled')
        self.inp_scale.place(x=43, y=30)

    def ifResizeChecked(self):

        if self.lbl_scale['state'] == 'disabled':
            self.lbl_scale['state'] = 'normal'
            self.inp_scale['state'] = 'normal'
        else:
            self.var_scale.set('1.0')
            self.lbl_scale['state'] = 'disabled'
            self.inp_scale['state'] = 'disabled'

    def ifFlipChecked(self):

        if self.rb_vertical['state'] == 'disabled':
            self.rb_vertical['state'] = 'normal'
            self.rb_horizontal['state'] = 'normal'
        else:
            self.rb_vertical['state'] = 'disabled'
            self.rb_horizontal['state'] = 'disabled'

    def ifRotateChecked(self):

        if self.rb_90['state'] == 'disabled':
            self.rb_90['state'] = 'normal'
            self.rb_180['state'] = 'normal'
            self.rb_270['state'] = 'normal'
        else:
            self.rb_90['state'] = 'disabled'
            self.rb_180['state'] = 'disabled'
            self.rb_270['state'] = 'disabled'

    def resize(self):
        width = int(self.image.shape[1] * float(self.var_scale.get()))
        height = int(self.image.shape[0] * float(self.var_scale.get()))
        dimensions = (width, height)
        self.image = cv.resize(self.image, dimensions,
                               interpolation=cv.INTER_AREA)

    def flip(self, image):
        self.image = cv.flip(image, int(self.var_orient.get()))

    def rotate(self, image):

        if self.var_degrees.get() == '1':
            self.image = cv.rotate(image, cv.cv2.ROTATE_90_CLOCKWISE)

        if self.var_degrees.get() == '2':
            self.image = cv.rotate(image, cv.ROTATE_180)

        if self.var_degrees.get() == '3':
            self.image = cv.rotate(image, cv.ROTATE_90_COUNTERCLOCKWISE)

    def sharpen(self, image):
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        self.image = cv.filter2D(image, -1, kernel)

    def blur(self, image):
        self.image = cv.GaussianBlur(image, (7, 7), cv.BORDER_DEFAULT)

    def gray(self, image):
        self.image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    def thresh(self, image):
        self.image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        ret, self.image = cv.threshold(self.image, 120, 255, cv.THRESH_BINARY)

    def detect_edges(self, image):
        self.image = cv.Canny(image, threshold1=100, threshold2=200)

    def ifSourceClicked(self):
        self.source = filedialog.askdirectory()

        if len(self.source) != 0:
            self.lbl_src.config(text="SOURCE: " + self.source)
            self.lbl_src.place(x=5, y=135)

    def ifDestClicked(self):
        self.dest = filedialog.askdirectory()

        if len(self.dest) != 0:
            self.lbl_dest.config(text="DESTINATION: " + self.dest)
            self.lbl_dest.place(x=5, y=160)

    def ifCreateClicked(self):

        if bool(eval(self.var_resize.get())) == True:
            scale = self.var_scale.get()
            try:
                scale = float(scale)
                print(scale)
            except:
                messagebox.showinfo(
                    'Bulk Image Processor', 'Scale value must be floating point or integer.')
                return

        if self.source == '':
            messagebox.showinfo('Bulk Image Processor',
                                'Please enter source location.')
            return

        if self.dest == '':
            messagebox.showinfo('Bulk Image Processor',
                                'Please enter destination.')
            return

        self.process()

    def process(self):
        start = time.perf_counter()

        os.chdir(self.source)

        resize = bool(eval(self.var_resize.get()))
        flip = bool(eval(self.var_flip.get()))
        rotate = bool(eval(self.var_rotate.get()))
        sharpen = bool(eval(self.var_sharpen.get()))
        blur = bool(eval(self.var_blur.get()))
        gray = bool(eval(self.var_gray.get()))
        thresholding = bool(eval(self.var_thresh.get()))
        edges = bool(eval(self.var_edges.get()))

        img_format = ''

        if self.var_format.get() == '1':
            img_format = '.png'
        else:
            img_format = '.jpg'

        for file in os.listdir('.'):
            os.chdir(self.source)
            if file.endswith('.png') or file.endswith('.jpg'):
                self.image = cv.imread(file)

                count = 0

                if resize:
                    self.resize()
                    count += 1

                if flip:
                    self.flip(self.image)
                    count += 1

                if rotate:
                    self.rotate(self.image)
                    count += 1

                if sharpen:
                    self.sharpen(self.image)
                    count += 1

                if blur:
                    self.blur(self.image)
                    count += 1

                if gray:
                    self.gray(self.image)
                    count += 1

                if thresholding:
                    self.thresh(self.image)
                    count += 1

                if edges:
                    self.detect_edges(self.image)
                    count += 1

                if count == 0:
                    messagebox.showinfo(
                        'Bulk Image Processor', 'No changes selected.')
                    self.master.after_cancel(process)

                os.chdir(self.dest)
                filename = str(self.count) + img_format
                cv.imwrite(filename, self.image)
                self.count += 1

        finish = time.perf_counter()

        status = f'{self.count-1} image(s) processed in {round(finish-start, 2)} second(s)'
        messagebox.showinfo('Bulk Image Processor', status)
        self.count = 1


if __name__ == '__main__':
    root = tk.Tk()
    main_app = MainApplication()
    root.mainloop()
