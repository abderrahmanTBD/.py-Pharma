from PIL import Image, ImageTk
import tkinter as tk
import sys
import os


class BkgrFrame(tk.Frame):
    def __init__(self, parent, file_path, width, height):
        super(BkgrFrame, self).__init__(parent, borderwidth=0, highlightthickness=0)

        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack()

        pil_img = Image.open(file_path)
        self.img = ImageTk.PhotoImage(pil_img.resize((width, height), Image.ANTIALIAS))
        self.bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def add(self, widget, x, y):
        canvas_window = self.canvas.create_window(x, y, anchor=tk.NW, window=widget)
        return widget
    
def runAR():
    root.destroy()
    os.system('python pharmapyAR.py')
    
def runFR():
    root.destroy()
    os.system('python pharmapyFR.py')


if __name__ == '__main__':

    IMAGE_PATH = 'img/background.jpg'
    WIDTH, HEIGTH = 350, 200

    root = tk.Tk()
    root.geometry('{}x{}'.format(WIDTH, HEIGTH))

    bkrgframe = BkgrFrame(root, IMAGE_PATH, WIDTH, HEIGTH)
    bkrgframe.pack()

    button1 = bkrgframe.add(tk.Button(root, text="Francais",command=runFR), 40, 170)
    button2 = bkrgframe.add(tk.Button(root, text="العربية",command=runAR), 250, 170)

    root.mainloop()
