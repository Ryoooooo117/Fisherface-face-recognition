from PIL import Image
from pylab import *
import os
import cv2

def histeq(im,nbr_bins=256):

	imhist,bins = histogram(im.flatten(),nbr_bins,normed=True)
	cdf = imhist.cumsum()
	cdf = 255 * cdf / cdf[-1]
  	
	im2 = interp(im.flatten(),bins[:-1],cdf) 
	im2 = im2.reshape(im.shape)
	return im2

def faceDetect(imagePath):
	face_cascade = cv2.CascadeClassifier('/usr/local/Cellar/opencv/2.4.13.2/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
	
	img_detected = cv2.imread(imagePath)
	gray = cv2.cvtColor(img_detected,cv2.COLOR_BGRA2GRAY)

	faces = face_cascade.detectMultiScale(
		gray,
		scaleFactor = 1.3,
		minNeighbors = 6,
		minSize=(4,4)
	)

	# drwa rectangle to highlight the face detected
	for(x,y,w,h) in faces:
		cv2.rectangle(img_detected,(x,y),(x+w,y+h),(0,255,0),2)

	print 'found %d faces in original picture'%(len(faces))

	cv2.imwrite("detected.jpg",img_detected)
	path = "detected.jpg"
	corpImg = img_detected[y:y+h,x:x+w]
	cv2.imwrite("cropedImg.jpg",corpImg)
	#path = "cropedImg.jpg"
	return img_detected,path
