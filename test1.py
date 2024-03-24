import cv2

# Capture video from the first camera
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()
    
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Detect basketball and hoop in the frame
    # This is highly simplified; actual implementation will vary based on your model
    # basketball_detected, hoop_detected = detect_objects(frame, model)
    
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

    # Check if the basketball goes through the hoop
    # This step will require tracking the basketball's trajectory and checking its relation to the hoop
    # made_it = check_basketball_hoop_relation(basketball_detected, hoop_detected)

    # Display the resulting frame (optional, for testing)
    # cv2.imshow('Frame', frame)

    # Break the loop with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()