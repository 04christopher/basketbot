import cv2
import numpy as np

def detect_basketball(video_path):
    # Open video capture
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Unable to open video.")
        return
    
    # Counter to track the number of times basketball passes through the right side
    passes_count = 0
    passed_first_area = False
    
    # Define areas of interest
    area1_top_left = (150, 100)
    area1_bottom_right = (350, 300)
    area2_top_left = (100, 310)
    area2_bottom_right = (400, 500)
    
    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        
        # If frame read successful
        if ret:

            # Inside your while loop, after updating passes_count
            # Define font, size, color, and thickness
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            color = (255, 255, 255)  # White color
            thickness = 2
            location = (50, 50)  # Top left corner of the window

            # Convert the counter to a string to display
            counter_text = f"Passes: {passes_count}"

            # Draw the counter on the frame
            cv2.putText(frame, counter_text, location, font, font_scale, color, thickness)
            # Now display the frame as you already do
            cv2.imshow('Basketball Detection', frame)

            # Convert frame to HSV color space
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Define lower and upper bounds for the color orange (common color of a basketball)
            lower_orange = np.array([30, 50, 50])
            upper_orange = np.array([90, 255, 255])
            
            # Threshold the frame to get only orange colors
            mask_orange = cv2.inRange(hsv_frame, lower_orange, upper_orange)
            
            # Find contours in the orange mask
            contours, _ = cv2.findContours(mask_orange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Check if any contour was found
            if contours:
                # Get the contour with the largest area (presumably the basketball)
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Get the bounding rectangle of the contour
                #x, y, w, h = cv2.boundingRect(largest_contour)

                #circle detection
                ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
                M = cv2.moments(largest_contour)

                if M["m00"] > 0:
                    center = (int(M['m10']/M['m00']), int(M['m01']/M['m00']))
                    if radius > 10:
                        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                        cv2.circle(frame, center, 5, (0, 0, 255), -1)
                
                # Draw a rectangle around the detected basketball
                #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Check if the basketball is passing through area 1
                if (area1_top_left[0] < x < area1_bottom_right[0]) and \
                   (area1_top_left[1] < y < area1_bottom_right[1]):
                    passed_first_area = True
                
                # Check if the basketball has passed through the second area after passing through the first area
                if passed_first_area and \
                   (area2_top_left[0] < x < area2_bottom_right[0]) and \
                   (area2_top_left[1] < y < area2_bottom_right[1]):
                    passes_count += 1
                    print(f"Basketball passed through both areas in sequence! Total passes: {passes_count}")
                    passed_first_area = False  # Reset for the next pass
            
            # Draw areas of interest on the frame
            cv2.rectangle(frame, area1_top_left, area1_bottom_right, (0, 0, 255), 2)
            cv2.rectangle(frame, area2_top_left, area2_bottom_right, (0, 0, 255), 2)
            
            # Display the frame
            cv2.imshow('Basketball Detection', frame)
            
            # Check for key press to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    
    # Release video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Example usage with webcam (change to 0 for default webcam)
detect_basketball(1)