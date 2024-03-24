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

FRAMES_PER_SECOND = 60
passes_count = 0

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

                valid_commands = ["reset score", "research score", "he said score", "recess score"]
                if any(command in text for command in valid_commands):
                    global passes_count
                    passes_count = 0
                    print("Score reset successfully.")
                    listening_for_command = False  # Resets listening state; remove if you want continuous command listening

                if elapsed_time > 5:  # 3-second time frame
                    print("Time's up. Did not receive any command.")
                    listening_for_command = False  # Stop listening for the command
                    rec = KaldiRecognizer(model, 16000)  # Reset recognizer for the next wake word
                    continue


def detect_basketball(video_path):
    global passes_count 
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
                        if (count_frame >= FRAMES_PER_SECOND/2):
                            passes_count += 1
                            print(f"Basketball passed through both areas in sequence! Total passes: {passes_count}")
                            passed_first_area = False
                            count_frame = 0

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

# Start the voice command listener in a separate thread
if __name__ == "__main__":
    # Start the voice command listener
    listen_for_commands_thread = threading.Thread(target=listen_for_commands_vosk, daemon=True)
    listen_for_commands_thread.start()

    # Start the basketball detection
    detect_basketball(1)  # Assuming your webcam is indexed as 1

# Example usage
#detect_basketball(1)  # For webcam, assuming it's indexed as 0


