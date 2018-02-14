from pylab import *
from PIL import Image
import tools as tools
from DRalgorithm import *

def facialRecognition(imagePath,databasePath):
    # find the size of image in databse
    databaseImgPath = tools.findImg(databasePath,1)
    databaseImg = Image.open(databaseImgPath).convert('L')
    print 'databaseImg.shape:'+str(databaseImg.size)

    # resize the target picture 
    targetImg = Image.open(imagePath).convert('L').resize(databaseImg.size)
    newImgPath = './targetImg.jpg'
    targetImg.save(newImgPath)

    # sample training
    sampleClass,sampleEigenvectors,sampleMean,sampleProjections =sampleTraining(databasePath)
    
    # match picture
    result = matchImg(newImgPath,sampleClass,sampleEigenvectors,sampleMean,sampleProjections)
    print 'the new image is in subject'+str(result)

    # plot pca eigenface
    #meanImgPath = plotPCA(result,databasePath)
    meanImgPath = ""
    return result, meanImgPath

def sampleTraining(databasePath):
    path = databasePath
    ImgArray,classes = tools.readImages(path)
    print '    recognitionTest->sampleTraining->len(ImgArray):'+str(len(ImgArray))
    ImgMatrix = tools.asRowMatrix(ImgArray)
    eigenvalues, eigenvectors, mean = fisherfaces(ImgMatrix,classes)

    sampleClass = classes
    sampleEigenvectors = eigenvectors
    sampleMean = mean
    sampleProjections = []
    for Imgi in ImgArray:
        sampleProjections.append(project(sampleEigenvectors, Imgi.reshape(1,-1), sampleMean))

    return sampleClass,sampleEigenvectors,sampleMean,sampleProjections


def matchImg(imagePath,sampleclass,sampleEigenvectors,sampleMean,sampleProjections):
    newImagePath = imagePath
    newImage = array(Image.open(newImagePath).convert('L'))

    minDistance = float('inf')
    targetClass = -1
    newProjection = project(sampleEigenvectors, newImage.reshape(1,-1), sampleMean)

    for i in xrange(len(sampleProjections)):
        distance = tools.euclideanDistance(sampleProjections[i], newProjection)
        if distance < minDistance:
            minDistance = distance
            targetClass = sampleclass[i]

    # because the class start with index 0, so we add 1 to convert it into real subject index
    targetClass = targetClass + 1
    return targetClass

def plotPCA(targetClass,databasePath):
    path = databasePath
    ImgArray,classes = tools.readImages(path)
    ImgMatrix = tools.asRowMatrix(ImgArray)
    numberOfVectors = len(ImgArray)*2/3
    eigenvalues, eigenvectors, mean = pca(ImgMatrix,numberOfVectors)

    """
    print 'plotPCA length:'+str(len(ImgArray))
    print 'plotPCA eigenvectors shape:'+str(eigenvectors.shape)
    for i in range(0,15):
        print 'plotPCA i:'+str(i)
        e = eigenvectors[:,(5+i*11)].reshape(ImgArray[0].shape)
        subplot(4,4,i+1,title="subject %r"%(i+1))
        gray()
        axis('off')
        imshow(tools.normalize(e,0,255))

    show()
    """

    imgPath = tools.findImg(path,targetClass)
    if( imgPath == None ):
        print 'cannot find image'
        return None
    
    print 'imgPath:'+str(imgPath)
    meanImage = array(Image.open(imgPath).convert('L'))

    projection = project(eigenvectors, meanImage.reshape(1,-1), mean)
    plotImg = reconstruct(eigenvectors, projection, mean) 
    plotImg = plotImg.reshape(ImgArray[0].shape)

    meanImg = Image.fromarray(plotImg).convert('RGB')
    meanImgPath = './plotPcaMeanImg.jpg'
    meanImg.save(meanImgPath)
    return meanImgPath
    
'''
#==============================================================================
# input to target picture and facial database path
#==============================================================================

#newImagePath = '../att_faces/s11/1.pgm' # AT&T face database target
#path = '../att_faces'# AT&T face database

ImagePath = '../yaleA/s07/subject07.leftlight.jpg' # Yale A face database target
path = '../yaleA'# Yale A face database

#newImage = array(Image.open(newImagePath).convert('L'), dtype=np.uint8)
newImage = array(Image.open(newImagePath).convert('L'))
print 'newImage:'+str(newImage.shape)

ImgArray,classes = tools.readImages(path)
print 'main-> ImgArray len:'+str(len(ImgArray))

#==============================================================================
# fisherfaces to the facial database
#==============================================================================

ImgMatrix = tools.asRowMatrix(ImgArray)
print 'main-> ImgMatrix shape:'+str(ImgMatrix.shape)
eigenvalues, eigenvectors, mean = fisherfaces(ImgMatrix,classes)

#==============================================================================
# get sample information
#==============================================================================

sampleClass = classes
sampleEigenvectors = eigenvectors
sampleMean = mean
sampleProjections = []
for Imgi in ImgArray:
    sampleProjections.append(project(sampleEigenvectors, Imgi.reshape(1,-1), sampleMean))

print 'sample projection:'+str(len(sampleProjections))
print 'sample class:'+str(len(np.unique(sampleClass)))
print 'sample Eigenvectors:'+str(sampleEigenvectors.shape)

print 'sample projection[20]:'+str(sampleProjections[20].shape)
#==============================================================================
# calculate the distance between the new Image and every single Image in sample
#==============================================================================

minDistance = float('inf')
targetClass = -1
newProjection = project(sampleEigenvectors, newImage.reshape(1,-1), sampleMean)

for i in xrange(len(sampleProjections)):
    distance = tools.euclideanDistance(sampleProjections[i], newProjection)
    if distance < minDistance:
        minDistance = distance
        targetClass = classes[i]

# because the class start with index 0, so we add 1 to convert it into real subject index
targetClass = targetClass + 1
print 'the new image is in subject'+str(targetClass)

"""
E = []
for i in xrange(min(len(ImgArray), 16)):
    e = W[:,i].reshape(ImgArray[0].shape)
    E.append(tools.normalize(e,0,255))
# plot them and store the plot to "python_eigenfaces.pdf"
tools.subplot(title="Eigenfaces AT&T Facedatabase", images=E, rows=4, cols=4, sptitle="Eigenface", colormap=cm.jet, filename="python_pca_eigenfaces.png")

E = []
steps=[i for i in xrange(10, min(len(ImgArray), 320), 20)]
for i in xrange(min(len(steps), 16)):
    numEvs = steps[i]
    P = project(W[:,0:numEvs], ImgArray[0].reshape(1,-1), mu)
    #print 'eigenfaces: W[:,0:numEvs] shape:'+str(W[:,0:numEvs].shape) # 10304,310
    #print 'eigenfaces:   P shape:'+str(P.shape) # 1,310
    R = reconstruct(W[:,0:numEvs], P, mu) 
    #print 'eigenfaces:   R shape:'+str(R.shape) # 1,10304
    # reshape and append to plots
    R = R.reshape(ImgArray[0].shape)
    E.append(tools.normalize(R,0,255))

# plot them and store the plot to "python_reconstruction.pdf"
tools.subplot(title="Reconstruction AT&T Facedatabase", images=E, rows=4, cols=4, sptitle="Eigenvectors", sptitles=steps, colormap=cm.gray, filename="python_pca_reconstruction.png")
"""
print 'end'
'''
