import pandas as pd #pip install pandas opencv-python
import cv2
import pyttsx3 #pip install pyttsx3==2.7
from tkinter import Tk #pip install tk
from tkinter.filedialog import askopenfilename

# Manually uploading file by User
Tk().withdraw()
imagePath = askopenfilename()
# End 

dataPath = 'colorsDataset.csv'

colNames = ['color', 'colorName', 'hexValue', 'R', 'G', 'B']
dataset = pd.read_csv(dataPath, names=colNames, header=None)

onClick = False
red = blue = green = xPos = yPos = 0

# Retrieving color name
def getColorName(red, blue, green):
    minValue = 10000
    for i in range(len(dataset)):
        minDifference = abs(red - dataset.loc[i, 'R']) + abs(blue - dataset.loc[i, 'B']) + abs(green - dataset.loc[i, 'G'])
        if minDifference <= minValue:
            minValue = minDifference
            colorName = dataset.loc[i, 'colorName']
    return colorName
# End

# Getting R,G,B values corresponding to x,y co-ordinates
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global red, blue, green, onClick, xPos, yPos
        onClick = True
        blue, green, red = image[y, x]
        xPos = x
        yPos = y
        blue = int(blue)
        green = int(green)
        red = int(red)
# End   


image = cv2.imread(imagePath)
image = cv2.resize(image, (800, 600))
cv2.namedWindow("Uploaded")
cv2.setMouseCallback("Uploaded", draw_function)

# Initializing voice engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# End

# Repeated Actions of Mouse clicking
p = 1
while p == 1:
    cv2.imshow("Uploaded", image)
    if onClick:
        engine = pyttsx3.init()
        # Getting Text
        cv2.rectangle(image, (20, 20), (700, 60), (blue, green, red), -1)
        name = getColorName(red, blue, green) + " R=" + str(red) + " B=" + str(blue) + " G=" + str(green)
        cv2.putText(image, name, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        # End
        k = 1
        engine.stop()
        if red + blue + green >= 600:
            cv2.putText(image, name, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        if k == 1:
            # Text to Speech
            engine.setProperty('voice',voices[1].id)
            engine.say(getColorName(red, blue, green))
            engine.runAndWait()
            # End
            onClick = False
    if cv2.waitKey(30) & 0xFF == 27:
        p = 0
        break


cv2.destroyAllWindows()
# End
