import cv2
import numpy as np
import speech_recognition as sr
import threading
import os
import wave
import json
import pyaudio
from vosk import Model, KaldiRecognizer
import time 
import re
from word2number import w2n


game_time_left = 0  # Time left in seconds
game_timer_active = False  # Indicates if the game timer is running
last_time_check = time.time()  # Keeps track of the last time we checked the timer
pause_time_left = 0  # Keeps track of the time left when the timer was paused
paused = 0
paused_time_add = 0

FRAMES_PER_SECOND = 60
passes_count = 0

# Load the background image
bg_image_path = 'C:\eSupport\\frame-text-tiktok-element-decorative-template-design-ornament-banner-design-template_609989-1712.png'
#bg2_image_path = "C:\eSupport\\Untitled design (11).png"

bg_image = cv2.imread(bg_image_path)
#bg_image2 = cv2.imread(bg2_image_path)

# Resize the background image if necessary
# bg_image = cv2.resize(bg_image, (desired_width, desired_height))
bg_image = cv2.resize(bg_image, (200, 75), interpolation=cv2.INTER_AREA)
# bg_image2 = cv2.resize(bg_image2, (200, 70), interpolation=cv2.INTER_AREA)

def overlay_image(background, overlay, x, y):
    """
    Overlay an image onto another image at position (x, y)
    """
    h, w = overlay.shape[:2]
    background[y:y+h, x:x+w] = overlay

# Position where you want to overlay the background image
pos_x = 20
pos_y = 20

def listen_for_commands_vosk():
    global passes_count 
    model_path = "C:\\vosk-model-small-en-us-0.15" # Update this path to your Vosk model
    if not os.path.exists(model_path):
        print("Please check the model path and try again.")
        return
    model = Model(model_path)
    
    mic_index = 3 # Update this to the index of your preferred microphone

    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, input_device_index=mic_index, frames_per_buffer=4000)
    stream.start_stream()

    rec = KaldiRecognizer(model, 16000)
    rec.SetWords(True)  # Enable word-level recognition to easily catch the wake word

    command_start_time = None

    print("Basket Bot is ready (listening for 'Hello basket')...")

    listening_for_command = False
    while True:
        global passes_count, game_time_left, game_timer_active, last_time_check, pause_time_left, paused_time_add
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            results = json.loads(rec.Result())
            text = results.get('text', '').lower()
            print(f"Recognized: {text}")

            if "hello basket" in text and not listening_for_command:
                print("Heard wake word! Waiting for command...")
                listening_for_command = True
                command_start_time = time.time()
            elif listening_for_command:
                # This block processes the command after the wake word is detected
                elapsed_time = time.time() - command_start_time
                print(f"Command received: {text}")  # Implement your command handling logic here

                valid_commands = ["reset score", "research score", "he said score", "recess score", "research school"]
                if any(command in text for command in valid_commands):
                    global passes_count
                    passes_count = 0
                    print("Score reset successfully.")
                    listening_for_command = False  # Resets listening state; remove if you want continuous command listening

                try:
                    if "minute" in text:
                        # Attempt to convert textual numbers to numeric
                        minutes = w2n.word_to_num(text.split("minute")[0])
                    # Pause command
                    elif "pause clock" in text or "pause timer" in text or "pause" in text:
                        if game_timer_active:
                            paused = 1
                            pause_time_left = game_time_left
                            game_timer_active = False
                            print("Timer paused.")
                    # Resume command
                    elif "resume clock" in text or "resume timer" in text or "resume" in text:
                        if not game_timer_active and pause_time_left > 0:
                            game_time_left = pause_time_left + paused_time_add
                            paused = 0
                            paused_time_add = 0
                            game_timer_active = True
                            last_time_check = time.time()
                            print("Timer resumed.")
                    # Reset command
                    elif "reset clock" in text or "reset timer" in text:
                        game_time_left = 0
                        game_timer_active = False
                        pause_time_left = 0
                        print("Timer reset to 0.")
                    else:
                        # Extracting numeric values directly
                        match = re.search(r'(\d+)\s*minutes', text)
                        minutes = int(match.group(1)) if match else 0

                    if 1 <= minutes <= 60:
                        game_time_left = minutes * 60
                        game_timer_active = True
                        print(f"Timer set for {minutes} minutes.")
                        listening_for_command = False
                        minutes = 0
                except ValueError:
                    print("Could not understand the number of minutes.")

                if elapsed_time > 5:  # 3-second time frame
                    print("Time's up. Did not receive any command.")
                    listening_for_command = False  # Stop listening for the command
                    rec = KaldiRecognizer(model, 16000)  # Reset recognizer for the next wake word
                    continue


def detect_basketball(video_path):
    global passes_count, game_time_left, game_timer_active, paused_time_add
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Unable to open video.")
        return
    
    passed_first_area = False

    count_frame = 0
    
    area1_top_left = (150, 100)
    area1_bottom_right = (350, 300)
    area2_top_left = (100, 310)
    area2_bottom_right = (400, 500)

     # Initialize last_time_check with the current time at the start
    last_time_check = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        #overlay_image(frame, bg_image2, 540, 650)

        # Timer countdown
        if game_timer_active:
            current_time = time.time()
            elapsed = current_time - last_time_check
            if elapsed >= 1:
                game_time_left -= int(elapsed)
                last_time_check = current_time

                # Handle when the timer reaches 0
                if game_time_left <= 0:
                    game_timer_active = False
                    print("Time's up!")
                    game_time_left = 0  # Ensure the time doesn't go negative
        elif paused == 1:
            paused_time_add += 1

         # Show timer on frame
        minutes, seconds = divmod(game_time_left, 60)
        timer_text = f"{minutes:02d}:{seconds:02d}"

        # Calculate the position and size of the rectangle based on the text size
        rect_top_left = (555, 665)  # Adjust as needed
        rect_bottom_right = (720, 770)  # Adjust as needed
        rect_color = (0, 0, 0)  # Black color for the rectangle
        rect_thickness = -1  # Fill the rectangle

        # Draw the rectangle for the background
        cv2.rectangle(frame, rect_top_left, rect_bottom_right, rect_color, rect_thickness)

        cv2.putText(frame, timer_text, (570, 710), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 5)

        #new stuff
        overlay_image(frame, bg_image, pos_x, pos_y)
        # Draw the text over the background image
        text = f"SCORE: {passes_count}"
        text_color = (0, 0, 0)  # White text
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        thickness = 3

        # Calculate text size to optionally adjust text position for better alignment
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)

        # Adjust text position based on the background image size and position
        text_x = pos_x + 16  # For example, start 10 pixels from the left edge of the bg image
        text_y = pos_y + text_height + 24  # For example, 20 pixels from the top edge of the bg image

        cv2.putText(frame, text, (text_x, text_y), font, font_scale, text_color, thickness)
                
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
                if 0.5 <= circularity <= 1.0:  # Adjust thresholds as necessary
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
                        count_frame += 1
                        if (count_frame >= FRAMES_PER_SECOND/4):
                            passes_count += 1
                            print(f"Basketball passed through both areas in sequence! Total passes: {passes_count}")
                            passed_first_area = False
                            count_frame = 0

        # UI updates, including drawing areas of interest and displaying the pass count
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.rectangle(frame, area1_top_left, area1_bottom_right, (0, 0, 255), 2)
        cv2.rectangle(frame, area2_top_left, area2_bottom_right, (0, 0, 255), 2)
        cv2.imshow('Basketball Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Start the voice command listener in a separate thread
if __name__ == "__main__":
    # Start the voice command listener
    listen_for_commands_thread = threading.Thread(target=listen_for_commands_vosk, daemon=True)
    listen_for_commands_thread.start()

    # Start the basketball detection
    detect_basketball(1)  # Assuming your webcam is indexed as 1

# Example usage
#detect_basketball(1)  # For webcam, assuming it's indexed as 0


