from PIL import Image
from pylab import *
import os, sys

def readImages(path):
    '''
    This function is used to read images from face database file.
    Because of the specific structure in face database file, 
    we have to read images in certain orders.
    
    Input
        path: address of the face database file

    Output
        ImgArray: array of all images, each element is image's array form
        ImgClasses: array of class of each imageS
    '''

    subjectClass = 0
    ImgArray,ImgClasses = [], []
    # dirName: current file path
    # dirNames: sub file path under current path
    # fileNames: files in the current path
    for dirName , dirNames , fileNames in os.walk(path):
        for subDirName in dirNames:
            subjectPath = os.path.join(dirName , subDirName)
            for fileName in os.listdir(subjectPath):
                # In Mac OS when the whole file is copied, some unseen file named by '.DS_Store' would be created
                # we need to ingore such file
                if fileName == '.DS_Store':
                    continue
                img = array(Image.open(os.path.join(subjectPath , fileName)).convert('L'))
                ImgArray.append(img)
                ImgClasses.append(subjectClass)
            subjectClass = subjectClass+1
            #print 'toos: subjectPath'+str(subjectPath)


    return [ImgArray,ImgClasses]


def asRowMatrix(ImgArray):
    '''
    This function is used to transform the array X to matrix,
    every row of the new matrix represents the original array element

    Input
        ImgArray: the array needs to transform

    Output
        matrix: the new matrix transformed from the array
    '''

    if len(ImgArray) == 0:
        return array([])
    matrix = empty((0, ImgArray[0].size), dtype=ImgArray[0].dtype)

    for row in ImgArray:
        matrix = vstack((matrix, array(row).reshape(1,-1)))
    return matrix


def normalize(matrix, low, high):
    '''
    This function is used to normalize a matrix with low and high scales

    Input
        matrix: the target matrix
        low,high: range of normalize scale

    Output
        matrix: matrix after being normalized
    '''

    matrix = array(matrix)

    # normalize the matrix from 0 to 1. 
    minX = np.min(matrix)
    maxX = np.max(matrix)
    matrix = matrix - float(minX)
    matrix = matrix / float((maxX - minX))

    # scale to [low...high].
    matrix = (high-low) * matrix
    matrix = matrix + low
    
    matrix = array(matrix)
    return matrix


def euclideanDistance(x,y):
    '''
    The function is used to calculate the euclidean distance between projection x and projection y
    
    Input
        x: matrix x 
        y: matrix y

    Output
        distance: euclidean distance between x and y

    '''
    x = array(x).flatten()
    y = array(y).flatten()

    sum = 0;
    for i in range(0,len(x)):
        sum = sum + np.power((x[i]-y[i]),2)

    distance = sqrt(sum)

    #distance = np.sqrt(np.sum(np.power((x-y),2)))
    return distance

def findImg(path,index):
    for dirName , dirNames , fileNames in os.walk(path):
        for i in range(0,len(dirNames)):
            if( i == index-1 ):
                subjectPath = os.path.join(dirName , dirNames[i])
                for fileName in os.listdir(subjectPath):
                    if fileName == '.DS_Store':
                        continue
                    #pil_im = Image.open(os.path.join(subjectPath , fileName)).convert('L')
                    #img = array(Image.open(os.path.join(subjectPath , fileName)).convert('L'))
                    imgPath = os.path.join(subjectPath , fileName)
                    return imgPath
    return None

def subplot(title, images, rows, cols, sptitle="subplot", sptitles=[], colormap=cm.gray, ticks_visible=True, filename=None):
    fig = plt.figure()
    '''
    The function is used to draw plot from image array

    Input

    '''
    # main title
    fig.text(.5, .95, title, horizontalalignment='center') 
    for i in xrange(len(images)):
        ax0 = fig.add_subplot(rows,cols,(i+1))
        plt.setp(ax0.get_xticklabels(), visible=False)
        plt.setp(ax0.get_yticklabels(), visible=False)
        if len(sptitles) == len(images):
            plt.title("%s #%s" % (sptitle, str(sptitles[i])), create_font('Tahoma',10))
        else:
            plt.title("%s #%d" % (sptitle, (i+1)), create_font('Tahoma',10))
        plt.imshow(array(images[i]), cmap=colormap)
    if filename is None:
        plt.show()
    else:
        fig.savefig(filename)

def create_font(fontname='Tahoma', fontsize=10):
    return { 'fontname': fontname, 'fontsize':fontsize }



