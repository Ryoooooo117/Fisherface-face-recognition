from Tkinter import *
from PIL import Image,ImageTk
import tkFileDialog
import tkMessageBox
import time
from recognitionTest import facialRecognition


def loadTargetPic(p):
    filename = tkFileDialog.askopenfilename(initialdir = '/Users/jinglianghe/Documents/faceDatabase')
    if len(filename) != 0:
        im = Image.open(filename).resize((300,300))
        tkim = ImageTk.PhotoImage(im)
        leftCanvas.itemconfigure(leftCanvasImg,image = tkim)
        leftCanvas.image = tkim
        targetImgPath.set(filename)
        picLabel['text'] = 'Image: %r'%(filename.split('/')[-2:])

def loadDatabase():
    filename = tkFileDialog.askdirectory(initialdir = '/Users/jinglianghe/Documents/faceDatabase')
    databasePath.set(filename)
    if len(filename) != 0:
        databaseLabel['text'] = 'Database: %r'%(filename.split('/')[-1])


def match():
    imgPath = targetImgPath.get()
    database = databasePath.get()
    if len(imgPath) == 0 or len(database) == 0:
        print 'path is empty'
    else:
        print 'targetImgPath:'+str(imgPath)
        print 'databasePath:'+str(database)

        startTime = time.clock()
        targetIndex, meanImgPath = facialRecognition(imgPath,database)
        stopTime = time.clock()
        print '    match time:'+str(stopTime-startTime)
        #loadMeanPic(meanImgPath)
        tkMessageBox.showinfo(title = "result", message = 'match subject '+str(targetIndex))
        resLabel['text'] = 'Result: subject %r'%(targetIndex)


def loadMeanPic(meanImgPath):
    im = Image.open(meanImgPath).resize((300,300))
    tkim = ImageTk.PhotoImage(im)
    rightCanvas.itemconfigure(rightCanvasImg,image = tkim)
    rightCanvas.image = tkim


imgSize = 300 

root = Tk()
root.title('Facial Recognition')

targetImgPath = StringVar()
databasePath = StringVar()

leftInitialImg = Image.open('leftBackground.jpg').resize((imgSize,imgSize))
leftTkIm = ImageTk.PhotoImage(leftInitialImg)
rightInitialImg = Image.open('rightBackground.jpg').resize((imgSize,imgSize))
rightTkIm = ImageTk.PhotoImage(rightInitialImg)

bTarget = Button(root,text='Target Image',command = lambda p=None: loadTargetPic(p))
bTarget.grid(row = 0,column = 0,sticky = W)

bDatabase = Button(root,text='Face Database',command = loadDatabase )
bDatabase.grid(row = 0,column = 0,sticky = E)

databaseLabel = Label(root,text='Database')
databaseLabel.grid(row = 0, column = 1, sticky = W)

bMatch = Button(root,text='Match',command = match )
bMatch.grid(row = 0,column=1,sticky = E)



leftCanvas = Canvas(root,width = imgSize, height = imgSize, bg = 'white')
leftCanvasImg = leftCanvas.create_image(imgSize/2,imgSize/2,image = leftTkIm)
leftCanvas.grid(row = 1,column = 0)

rightCanvas = Canvas(root,width = imgSize, height = imgSize, bg = 'white')
rightCanvasImg = rightCanvas.create_image(imgSize/2,imgSize/2,image = rightTkIm)
rightCanvas.grid(row = 1,column = 1)

picLabel = Label(root,text='Image Information')
picLabel.grid(row = 2, column = 0, sticky = W)

resLabel = Label(root,text='Result')
resLabel.grid(row = 2, column = 1, sticky = E)
root.mainloop()
