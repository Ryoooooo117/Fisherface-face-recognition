from Tkinter import *
import tkMessageBox
import tkFileDialog
from PIL import Image,ImageTk

def loadPic():
    #path = e.get()
    #tkMessageBox.showinfo(title = "path", message = path)
    filename = tkFileDialog.askopenfilename(initialdir = '/Users/jinglianghe/Documents/pythonworkspace')
    e.insert(0,filename)
    im = Image.open(filename)
    tkim = ImageTk.PhotoImage(im)
    #root.update_idletasks()

def changePic():
    l.configure(image = im2)
"""
root = Tk()
root.geometry('200x300')

p = Label(root,text='Path: ')
p.grid(row = 0, column = 0, sticky = W)
e = Entry(root)
e.grid(row = 0, column = 1, sticky = W)

bLoad = Button(root,text='Load',command = loadPic)
bLoad.grid(row = 0, column= 2, sticky = W)

im = ImageTk.PhotoImage(Image.open('../img/gb.jpg'))
im2 = ImageTk.PhotoImage(Image.open('../img/cph1.jpg'))
l = Label(root,image = im)
l.grid(row = 1,column = 0)

bShow = Button(root,text='Show',command = changePic)
bShow.grid(row = 3,column = 0,sticky = E)

root.mainloop()
"""
filename = '/Users/jinglianghe/Documents/faceDatabase/CroppedYale/yaleB01/yaleB01_P00A-005E-10.pgm'
im = Image.open(filename)
im.show()