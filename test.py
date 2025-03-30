import cv2
import mediapipe as mp
import serial
import time
import signal
import sys
import requests

# Initialize serial communication with Arduino
arduino = serial.Serial(port='COM13', baudrate=9600, timeout=1)
time.sleep(2)  # Wait for the serial connection to initialize

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Flask server URL to send serial output
FLASK_SERVER_URL = "http://127.0.0.1:5000/serial-output"

# Function to detect individual fingers (1 for up, 0 for down)
def detect_fingers(image, hand_landmarks):
    finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
    thumb_tip = 4
    finger_states = [0, 0, 0, 0, 0]  # Thumb, Index, Middle, Ring, Pinky

    # Check thumb
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        finger_states[0] = 1  # Thumb is up

    # Check the other fingers
    for idx, tip in enumerate(finger_tips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            finger_states[idx + 1] = 1  # Other fingers are up

    return finger_states

# Signal handler to clean up resources
def signal_handler(sig, frame):
    print("Terminating process...")
    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()
    arduino.close()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Start capturing video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers_state = detect_fingers(image, hand_landmarks)
            arduino.write(bytes(fingers_state))  # Send list of fingers as bytes
            print(f"Fingers State: {fingers_state}")

            # Send the serial output to the Flask server
            try:
                requests.post(FLASK_SERVER_URL, json={"fingers_state": fingers_state})
            except Exception as e:
                print(f"Error sending data to Flask server: {e}")

    cv2.imshow('Hand Tracking', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Cleanup resources when the loop ends
cap.release()
cv2.destroyAllWindows()
arduino.close()