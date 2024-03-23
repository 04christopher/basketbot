import time
import cv2,pandas
from datetime import datetime
import numpy as np
#from flask import Flask, render_template

# app = Flask(__name__, static_folder='static')

# Your boolean data
boolean_data = True  # Replace this with your boolean data

# @app.route('/')
# def index():
#   return render_template('index.html', boolean_data=boolean_data)

# if __name__ == '__main__':
#    app.run(debug=True)

def detect_basketball(video_path):
    # Open video capture
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Unable to open video.")
        return
    
    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        
        # If frame read successful
        if ret:
            # Convert frame to HSV color space
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Define lower and upper bounds for the color orange (common color of a basketball)
            lower_orange = np.array([5, 50, 50])
            upper_orange = np.array([15, 255, 255])
            
            # Threshold the frame to get only orange colors
            mask = cv2.inRange(hsv_frame, lower_orange, upper_orange)
            
            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Check if any contour was found
            if contours:
                # Get the contour with the largest area (presumably the basketball)
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Get the bounding rectangle of the contour
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Draw a rectangle around the detected basketball
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Display the frame
            cv2.imshow('Basketball Detection', frame)
            
            # Check for key press to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

first_frame = None
status_list = [None,None]
time_stamp=[]
df = pandas.DataFrame(columns=["Start", "End"])
video = cv2.VideoCapture(0) #0  is the first port for camera, try 1 to choose a different cam
motion_threshold = 12000  #chooses size of object that is detected in pixels (contour area) 



amount_of_movement = 0 #counter for reps and stuff


delay_seconds = 3                        #loop for delaying the cam so i can run in front of it and stuff
for i in range(delay_seconds, 0, -1):
    print(f"{i} seconds remaining, Get In Position!")
    time.sleep(1)  # Pause for 1 second
print("Start")

while True:

    
    check,color_frame=video.read()
    status=0
    gray=cv2.cvtColor(color_frame,cv2.COLOR_BGR2GRAY) #converting color frame to gray frame
    gray=cv2.GaussianBlur(gray,(21,21),0)             #gaussian blur don't really understand but it works
    
    detect_basketball(0)
    if first_frame is None:
        first_frame = gray
        continue
    
    delta_frame=cv2.absdiff(first_frame, gray) #creating delta frame
    thresh_frame=cv2.threshold(delta_frame, 135, 255, cv2.THRESH_BINARY)[1] #creating threshold frame, also barely understand. (only need 2nd tuple?)
    
    
    thresh_frame=cv2.dilate(thresh_frame,None,iterations=3) #dilating threshold frame
    (cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #finding edge contours (complicated math) (Simple Chain Approximation Rule)
    
    for contour in cnts:
        if cv2.contourArea(contour) < motion_threshold:  #skips objects smaller than threshold
            continue
        status=1                                  #means that object is detected
        (x,y,w,h)=cv2.boundingRect(contour) 
        cv2.rectangle(color_frame,(x,y),(x+w,y+h),(0,0,255),2) #red rectangle bounding object
    
    status_list.append(status)                    
    
    if status_list[-1]==1 and status_list[-2]==0:     #object entering frame
        time_stamp.append(datetime.now())
        print("Motion Detected")
        amount_of_movement+=1
        print(amount_of_movement)
        boolean_data = True
    if status_list[-1]==0 and status_list[-2]==1:      #object leaving frame
        time_stamp.append(datetime.now())
        boolean_data = False
        
    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Colour Frame", color_frame)
    
    key=cv2.waitKey(1)                           #getting continuous livestream
    if key==ord('q'):                            #end camera with q
        if status==1:
            time_stamp.append(datetime.now())
        break
    

print(status_list)
for i in range(0, len(time_stamp),2):
    df=df.append({"Start":time_stamp[i],"End":time_stamp[i+1]},ignore_index=True)
    
df.to_csv("All_Time_Stamp.csv")
video.release()
cv2.destroyAllWindows()