import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2 as cv
from frames import *
from displayTumor import *
from predictTumor import *

class Gui:
    MainWindow = 0
    listOfWinFrame = list()
    FirstFrame = object()
    val = 0
    fileName = 0
    DT = object()

    wHeight = 700
    wWidth = 1180

    def __init__(self):
        global MainWindow
        MainWindow = tk.Tk()
        MainWindow.geometry('1200x720')
        MainWindow.resizable(width=False, height=False)
        MainWindow.title("Brain Tumor Detection")

        # Set background image
        bg_image = Image.open("image_no_background.png")
        bg_image = bg_image.resize((1200, 720), Image.ANTIALIAS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        background_label = tk.Label(MainWindow, image=bg_photo)
        background_label.image = bg_photo
        background_label.place(relwidth=1, relheight=1)

        self.DT = DisplayTumor()

        self.fileName = tk.StringVar()

        self.FirstFrame = Frames(self, MainWindow, self.wWidth, self.wHeight, 0, 0)
        self.FirstFrame.btnView['state'] = 'disable'

        self.listOfWinFrame.append(self.FirstFrame)

        WindowLabel = tk.Label(self.FirstFrame.getFrames(), text="Brain Tumor Detection", height=1, width=40)
        WindowLabel.place(x=320, y=30)
        WindowLabel.configure(background="#000000", foreground="#FFFFFF", font=("Comic Sans MS", 24, "bold"))

        self.val = tk.IntVar()
        RB1 = tk.Radiobutton(self.FirstFrame.getFrames(), text="Detect Tumor", variable=self.val,
                             value=1, command=self.check)
        RB1.place(x=250, y=200)
        RB1.configure(background="#000000", foreground="#FFFFFF", font=("Arial", 14))

        RB2 = tk.Radiobutton(self.FirstFrame.getFrames(), text="View Tumor Region",
                             variable=self.val, value=2, command=self.check)
        RB2.place(x=250, y=250)
        RB2.configure(background="#000000", foreground="#FFFFFF", font=("Arial", 14))

        browseBtn = tk.Button(self.FirstFrame.getFrames(), text="Browse", width=12, command=self.browseWindow)
        browseBtn.place(x=800, y=550)
        browseBtn.configure(background="#FF5733", foreground="#FFFFFF", font=("Arial", 14, "bold"))

        MainWindow.mainloop()

    def getListOfWinFrame(self):
        return self.listOfWinFrame

    def browseWindow(self):
        global mriImage
        FILEOPENOPTIONS = dict(defaultextension='*.*',
                               filetypes=[('jpg', '*.jpg'), ('png', '*.png'), ('jpeg', '*.jpeg'), ('All Files', '*.*')])
        self.fileName = filedialog.askopenfilename(**FILEOPENOPTIONS)
        image = Image.open(self.fileName)
        imageName = str(self.fileName)
        mriImage = cv.imread(imageName, 1)
        self.listOfWinFrame[0].readImage(image)
        self.listOfWinFrame[0].displayImage()
        self.DT.readImage(image)

    def check(self):
        global mriImage
        if self.val.get() == 1:
            self.listOfWinFrame = 0
            self.listOfWinFrame = list()
            self.listOfWinFrame.append(self.FirstFrame)

            self.listOfWinFrame[0].setCallObject(self.DT)

            res = predictTumor(mriImage)
            
            if res > 0.5:
                resLabel = tk.Label(self.FirstFrame.getFrames(), text="Tumor Detected", height=1, width=20)
                resLabel.configure(background="#000000", foreground="red", font=("Comic Sans MS", 16, "bold"))
            else:
                resLabel = tk.Label(self.FirstFrame.getFrames(), text="No Tumor", height=1, width=20)
                resLabel.configure(background="#000000", foreground="green", font=("Comic Sans MS", 16, "bold"))

            resLabel.place(x=700, y=450)

        elif self.val.get() == 2:
            self.listOfWinFrame = 0
            self.listOfWinFrame = list()
            self.listOfWinFrame.append(self.FirstFrame)

            self.listOfWinFrame[0].setCallObject(self.DT)
            self.listOfWinFrame[0].setMethod(self.DT.removeNoise)
            secFrame = Frames(self, MainWindow, self.wWidth, self.wHeight, self.DT.displayTumor, self.DT)

            self.listOfWinFrame.append(secFrame)

            for i in range(len(self.listOfWinFrame)):
                if i != 0:
                    self.listOfWinFrame[i].hide()
            self.listOfWinFrame[0].unhide()

            if len(self.listOfWinFrame) > 1:
                self.listOfWinFrame[0].btnView['state'] = 'active'

        else:
            print("Not Working")

mainObj = Gui()
