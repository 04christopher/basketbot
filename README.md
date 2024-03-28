# BasketBot - The All In One Basketball Game Helper

# ProduHacks 2024 Winner 

Team 25: Troy Wu, Jason Hsu, Christopher Chen, Khai Phan

# Revolutionizing Basketball Scorekeeping

BasketBot is a sophisticated and user-friendly basketball scorekeeping application that revolutionizes the way scores are tracked in basketball games. Using cutting-edge computer vision and voice recognition technologies, BasketBot offers a seamless and efficient solution to manual scorekeeping, which can be laborious and error-prone. It features object recognition and tracking, built-in game clock, as well as voice command recognition for manual score and timer controls.

###Features
Automated Score Counting: Leveraging the power of OpenCV, BasketBot detects and counts scores accurately, ensuring that players can focus on the game without the hassle of manual scorekeeping.

Voice-Controlled Interface: With integrated voice recognition powered by PyAudio and the VOSK API model, users can interact with BasketBot using simple voice commands to control scores and timer features.

Machine Learning-Enhanced Net Recognition: Employing machine learning algorithms via the TensorFlow framework, BasketBot can recognize basketball nets to facilitate accurate score detection.

Convenient and User-Friendly: Designed to be straightforward and easy to use, BasketBot is perfect for users of all ages and can be set up in any environment, requiring no specialized equipment.

###Tech Stack
Python: The core programming language for developing the BasketBot's functionality.

OpenCV: For capturing video streams and processing image data to detect scores.

PyAudio: To capture audio streams from the microphone for voice recognition.

VOSK: An open-source speech recognition toolkit that provides models for voice command recognition.

TensorFlow: An open-source machine learning library used to build the neural network for enhanced net detection.

###How It Works
Detection: BasketBot uses OpenCV to process the video feed from the basketball court, detecting the ball and net through color and shape recognition algorithms.

Voice Control: The system listens for specific voice commands using PyAudio and VOSK. When a wake word such as "Hello Basket" is recognized, BasketBot awaits further commands to control the score or set up a game timer.

Scorekeeping: Once a score is detected through the net, BasketBot updates the score count automatically. Users can also adjust the score through voice commands like "add point" or "subtract point."

Timer: The user can set a game timer by saying a command like "set timer for 20 minutes," which BasketBot will acknowledge and start counting down, displaying the time left on the screen.

### Tech Stack

- OpenCV
- Python
- PyAudio
- VOSK Offline Speech Recognition API

<video controls width="500">
    <source src="/path/to/video.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>

![Alt text](https://github.com/04christopher/team25/blob/main/demoshot.jpg)
