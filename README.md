# Greenness index calculator
A Python script that takes a folder of images and calculates a greenness index for each image by dividing the sum of all green pixel values by the sum of all green, red and blue pixel values. The output will be saved in an Excel file.

$$\text{Greennes index} = \frac{\sum_{i=1}^n \text{green pixels}}{\sum_{i=1}^n \text{green pixels} + \sum_{i=1}^n \text{red pixels} + \sum_{i=1}^n \text{blue pixels}}$$

Update: the script now also calculates the contrast of each image by computing the standard deviation of pixel values in the red, green, and blue channels, and then averaging these values:

$$\text{Contrast} = \frac{\sigma_\text{red pixels} + \sigma_\text{green pixels} + \sigma_\text{blue pixels}}{3}$$

## How to use this script
### 1. Precondition: color-correcting and cropping images
This script does not edit the pictures it uses in any way. In other words, it is the user's responsibility to make sure the images are ready to be analyzed. Adobe Lightroom can be used to crop and color-correct photographs. The latter is less important for pictures taken in laboratory setting with contant lighting conditions and camera settings.

### 2. Installing Python
If you have never used Python before, you need to install it first (see the [Python website](https://www.python.org/downloads/)). It is also recommended to install a Python editor such as PyCharm (go for the [community edition](https://www.jetbrains.com/pycharm/download/other.html)), but this is not required, as Python comes with a basic editor called IDLE.

### 3. The files in the project folder
After making sure Python is installed; download the project folder from GitHub (click on `code` > `download ZIP`). Unzip it, and put it in a file location where you can find it back. The project contains the script itself, a folder with example images and an output file. The indices from the example images are already calculated: please see if you understand these values.

### 4. Running the script
Next, navigate to the folder `img` and replace the files inside with the images you wish to analyze. Open the project via PyCharm or any other editor, run the code, and the values will be written to the Excel file.

## Editing the script
If you don't restructure/rename anything the project folder, it is not necessary to change the script in order to run it correctly. The file names of the images aren't relevant, as long as they're in the correct folder. But it might be necessary to edit a few things:

### Changing the file locations
The first two variables declared at the script define where the images can be found, where the output file will be created and what name it will have. If you want Python to find the images elsewhere on your computer, or want to save the output somewhere else, you can change these variables. However, I recommend just moving the files.

### Calculating the blueness or redness index instead
By changing the integer that is stored in the variable `indexColor`, you change the index that is calculated. As mentioned in the script, the indices `0`, `1` and `2` stand for the red, green and blue channel respectively. Changing the `1` by a `0` or a `2` will cause the script to calculate the red or blue index.
