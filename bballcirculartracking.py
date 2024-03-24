import cv2
import numpy as np

def detect_basketball(video_path):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Unable to open video.")
        return
    
    passes_count = 0
    passed_first_area = False
    
    area1_top_left = (150, 100)
    area1_bottom_right = (350, 300)
    area2_top_left = (100, 310)
    area2_bottom_right = (400, 500)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_lime_green = np.array([30, 50, 50])
        upper_lime_green = np.array([90, 255, 255])
        mask = cv2.inRange(hsv_frame, lower_lime_green, upper_lime_green)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            ((x, y), radius) = cv2.minEnclosingCircle(contour)
            circle_area = np.pi * (radius ** 2)
            
            if area > 0:  # Avoid division by zero
                circularity = area / circle_area
                if 0.7 <= circularity <= 1.0:  # Adjust thresholds as necessary
                    M = cv2.moments(contour)
                    center = (int(M['m10']/M['m00']), int(M['m01']/M['m00']))
                    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
                    
                    # Check if it passes through areas
                    if (area1_top_left[0] < x < area1_bottom_right[0]) and \
                       (area1_top_left[1] < y < area1_bottom_right[1]):
                        passed_first_area = True
                    
                    if passed_first_area and \
                       (area2_top_left[0] < x < area2_bottom_right[0]) and \
                       (area2_top_left[1] < y < area2_bottom_right[1]):
                        passes_count += 1
                        print(f"Basketball passed through both areas in sequence! Total passes: {passes_count}")
                        passed_first_area = False

        # UI updates, including drawing areas of interest and displaying the pass count
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, f"Passes: {passes_count}", (50, 50), font, 1, (255, 255, 255), 2)
        cv2.rectangle(frame, area1_top_left, area1_bottom_right, (0, 0, 255), 2)
        cv2.rectangle(frame, area2_top_left, area2_bottom_right, (0, 0, 255), 2)
        cv2.imshow('Basketball Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Example usage
detect_basketball(1)  # For webcam, assuming it's indexed as 0
