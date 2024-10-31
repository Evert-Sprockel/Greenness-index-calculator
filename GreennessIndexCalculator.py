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


# Takes one image path and calculates the greenness index
# Returns a list with four floats: one for each channel and one for the average
def calculateChromaticAverages(image_path):
    channelMeans = extractChannelMeansFromImage(image_path)
    channelMeans.append(channelMeans[indexColor] / (channelMeans[0] + channelMeans[1] + channelMeans[2]))
    return channelMeans


# Takes one image path and calculates the average of each channel
# Returns a list with three floats: one for each channel
def extractChannelMeansFromImage(imagePath):
    with Image.open(imagePath) as image:
        print(f'Started calculating {imagePath}')
        imgArray = np.array(image)
        channelMeans = []
        for channelIndex in range(3):
            channel = imgArray[:, :, channelIndex]
            channelMeans.append(calculateChannelMean(channel))
        return channelMeans


# Calculates the mean of all the pixel values of a given channel
# Returns one float representing the channel average
def calculateChannelMean(channel):
    if not isinstance(channel, np.ndarray):
        raise TypeError(f"Not a numpy array")
    return np.mean(channel)


# Creates an empty dataframe
# Returns the empty dataframe
def createDataframe():
    if indexColor == 0:
        headers = ['Filename', 'RedChannelAverage', 'GreenChannelAverage', 'BlueChannelAverage',
                   'RednessIndex(R/R+G+B)']
    elif indexColor == 1:
        headers = ['Filename', 'RedChannelAverage', 'GreenChannelAverage', 'BlueChannelAverage',
                   'GreennessIndex(G/R+G+B)']
    else:
        headers = ['Filename', 'RedChannelAverage', 'GreenChannelAverage', 'BlueChannelAverage',
                   'BluenessIndex(B/R+G+B)']
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
    newRow = [path] + calculateChromaticAverages(path)
    df.loc[len(df)] = newRow
openAndWriteToExcel(df, outputFileName)
