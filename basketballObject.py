import math
import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import numpy as np
# Create the color Finder object
# True : debug mode
myColorFinder = ColorFinder(True)
hsvVals = {'hmin': 8, 'smin': 138, 'vmin': 0, 'hmax': 142, 'smax': 255, 'vmax': 255}

# Variables
posListX, posListY = [], []
xList = [item for item in range(0, 1300)]
prediction = False

while True:
    # Grab the image
    img = cv2.imread("ball.png")
    img = img[0:900, :] # crop the image

    # Display
    img = cv2.resize(img, (0, 0), None, 0.7, 0.7)
    
    # Process the image using the ColorFinder update method
    imgColor, mask = myColorFinder.update(img, hsvVals)
    
    cv2.imshow("Image with Color", imgColor)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()