import math
import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import numpy as np

# Initialize the Video
cap = cv2.VideoCapture('./Videos/vid (4).mp4')

# Create the color Finder object
myColorFinder = ColorFinder(False)
hsvVals = {'hmin': 8, 'smin': 138, 'vmin': 0, 'hmax': 142, 'smax': 255, 'vmax': 255}

# Variables
posListX, posListY = [], []
xList = [item for item in range(0, 1300)] # image shpae of x -> 1300x1080
prediction = False

while True:
    
    success, img = cap.read()
    img = img[0:900, :]
    
    # Display
    img = cv2.resize(img, (0, 0), None, 0.7, 0.7)
    
    # Process the image using the ColorFinder update method
    imgColor, mask = myColorFinder.update(img, hsvVals)
    
    imgContours, contours = cvzone.findContours(img, mask, minArea=500)
    
    if contours:
        posListX.append(contours[0]['center'][0])
        posListY.append(contours[0]['center'][1])
        
    if posListX and posListY: 
        # polunomial regression y = Ax ^ 2 + Bx + C
        A, B, C = np.polyfit(posListX, posListY, 2)
        
        
        for i, (posX, posY) in enumerate(zip(posListX, posListY)):
            pos = (posX, posY)
            cv2.circle(imgContours, pos, 5, (0, 255, 0), cv2.FILLED)
            if i >= 1:
                cv2.line(imgContours, pos, (posListX[i - 1], posListY[i - 1]), (0, 255, 0), 2)
        
        for x in xList:
            y = int(A * x**2 + B * x + C)
            cv2.circle(imgContours, (x, y), 2, (255, 0, 255), cv2.FILLED)
            
        print(posListX)
        if len(posListX) < 10 :
            # Prediction
            a = A
            b = B
            c = C - 590

            x = int((-b - math.sqrt(b ** 2 - (4 * a * c))) / (2 * a))
            # print(x)
            prediction = 100 < x < 150

        if prediction:
            cvzone.putTextRect(imgContours, "Basket", (50, 100),
                               scale=3, thickness=3, colorR=(0, 200, 0), offset=20)
        else:
            cvzone.putTextRect(imgContours, "No Basket", (50, 100),
                               scale=3, thickness=3, colorR=(0, 0, 200), offset=20)
            
    cv2.imshow("Image with countours", imgContours)
    
    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(85) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()