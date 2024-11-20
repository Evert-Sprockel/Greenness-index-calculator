import os
import pandas as pd
from PIL import Image
import numpy as np


# Precondition: the images have to be color corrected and cropped to the right size


# Define the path to the directory containing the images
imagesDirectory = 'img'
# Define name of output file
outputFileName = 'GreennessDataOutput'
# Calculate index of
#  red:   0
#  green: 1
#  blue:  2
indexColor = 1


# Retrieve all images in a folder
# Returns list of paths to the images
def getImageList(folderDirectory):
    files = os.listdir(folderDirectory)
    imagePaths = []
    for filename in files:
        # Construct the full path to the file
        filePath = os.path.join(folderDirectory, filename)
        if isValidImage(filePath):
            imagePaths.append(filePath)
            # print(f'{filePath}: valid image')
        else:
            print(f'{filePath}: NOT VALID IMAGE')
    return imagePaths


# Checks if image is suitable
# Returns true if image is suitable, returns false if not
def isValidImage(imagePath):
    return isValidFile(imagePath) and isRGB(imagePath)


# Checks if file is a suitable format
# Returns true if file is image, returns false if not
def isValidFile(imagePath):
    return imagePath.lower().endswith(('.png', '.jpg', '.jpeg'))


# Checks if image is in RGB format
# Returns true if image is in RGB, returns false if not
def isRGB(imagePath):
    with Image.open(imagePath) as image:
        return image.mode == 'RGB' or image.mode == 'RGBA'


# Takes one image path and calculates the greenness index and contrast
# Returns a list with eight floats: 3x channel mean, 3x channel std. dev., 1x greenness index, 1x total contrast
def calculateIndexAndContrast(image_path):
    channelMaC = extractChannelMeansAndContrastFromImage(image_path)
    channelMaC.insert(3, channelMaC[indexColor] / (channelMaC[0] + channelMaC[1] + channelMaC[2]))
    channelMaC.append(np.mean([channelMaC[4], channelMaC[5], channelMaC[6]]))
    return channelMaC


# Takes one image path and calculates the average of each channel
# Returns a list with six floats: two for each channel
def extractChannelMeansAndContrastFromImage(imagePath):
    with Image.open(imagePath) as image:
        print(f'Started calculating {imagePath}')
        imgArray = np.array(image)
        channelMeans = []
        channelContrast = []
        for channelIndex in range(3):
            channel = imgArray[:, :, channelIndex]
            channelMeans.append(calculateChannelMean(channel))
            channelContrast.append(np.std(channel))
        return channelMeans + channelContrast


# Calculates the mean of all the pixel values of a given channel
# Returns one float representing the channel average
def calculateChannelMean(channel):
    if not isinstance(channel, np.ndarray):
        raise TypeError(f"Not a numpy array")
    return np.mean(channel)


# Calculates the standard deviations of all the pixel values of a given channel: a measure of contrast
# Returns one float representing the channel standard deviation/contrast
def calculateChannelContrast(channel):
    if not isinstance(channel, np.ndarray):
        raise TypeError(f"Not a numpy array")
    return np.std(channel)


# Creates an empty dataframe
# Returns the empty dataframe
def createDataframe():
    if indexColor == 0:
        headers = ['Filename', 'RedChannelAverage', 'GreenChannelAverage', 'BlueChannelAverage',
                   'RednessIndex(R/(R+G+B))', 'RedChannelStd.dev.', 'GreenChannelStd.dev.', 'BlueChannelStd.dev.',
                   'Contrast((Rstdev+Gstdev+Bstdev)/3)']
    elif indexColor == 1:
        headers = ['Filename', 'RedChannelAverage', 'GreenChannelAverage', 'BlueChannelAverage',
                   'GreennessIndex(G/(R+G+B))', 'RedChannelStd.dev.', 'GreenChannelStd.dev.', 'BlueChannelStd.dev.',
                   'Contrast((Rstdev+Gstdev+Bstdev)/3)']
    else:
        headers = ['Filename', 'RedChannelAverage', 'GreenChannelAverage', 'BlueChannelAverage',
                   'BluenessIndex(B/(R+G+B))', 'RedChannelStd.dev.', 'GreenChannelStd.dev.', 'BlueChannelStd.dev.',
                   'Contrast((Rstdev+Gstdev+Bstdev)/3)']
    return pd.DataFrame(columns=headers)


# Creates an Excel file and writes data in it
# Returns nothing
def openAndWriteToExcel(df, fileName):
    df.to_excel(fileName + '.xlsx', index=False)





##### main program ######
print("\nStart of calculation")
listOfImages = getImageList(imagesDirectory)
df = createDataframe()
for path in listOfImages:
    newRow = [path] + calculateIndexAndContrast(path)
    df.loc[len(df)] = newRow
openAndWriteToExcel(df, outputFileName)
