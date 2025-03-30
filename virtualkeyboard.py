import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize Mediapipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Define a full keyboard layout
keyboard_layout = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/'],
    ['Space']
]

# Keyboard dimensions
key_width = 80
key_height = 80
keyboard_start_x = 50
keyboard_start_y = 50

# Open text files to write
output_file = open("output.txt", "a")
typed_words_file = open("typed_words.txt", "a")

# Variable to store the current word
current_word = ""

# Function to draw the keyboard
def draw_keyboard(frame):
    for row_idx, row in enumerate(keyboard_layout):
        for col_idx, key in enumerate(row):
            x = keyboard_start_x + col_idx * key_width
            y = keyboard_start_y + row_idx * key_height

            # Draw keys
            cv2.rectangle(frame, (x, y), (x + key_width, y + key_height), (238, 130, 238), -1)
            cv2.rectangle(frame, (x, y), (x + key_width, y + key_height), (255, 255, 255), 2)

            # Draw key labels
            if key == "Space":
                cv2.putText(frame, key, (x + 10, y + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            else:
                cv2.putText(frame, key, (x + 25, y + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

# Function to detect which key is pressed
def detect_key(x, y):
    for row_idx, row in enumerate(keyboard_layout):
        for col_idx, key in enumerate(row):
            key_x = keyboard_start_x + col_idx * key_width
            key_y = keyboard_start_y + row_idx * key_height
            if key_x < x < key_x + key_width and key_y < y < key_y + key_height:
                return key
    return None

# Function to count the number of fingers up
def count_fingers(hand_landmarks):
    fingers_up = 0
    finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
    thumb_tip = 4

    # Check thumb
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        fingers_up += 1

    # Check other fingers
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers_up += 1

    return fingers_up

# Start video capture
cap = cv2.VideoCapture(0)

frame_width = 1280
frame_height = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

last_pressed_time = 0
debounce_delay = 0.5

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    draw_keyboard(frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the tip of the index finger (landmark 8)
            x = int(hand_landmarks.landmark[8].x * frame.shape[1])
            y = int(hand_landmarks.landmark[8].y * frame.shape[0])

            # Highlight the fingertip
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

            # Count fingers
            fingers_up = count_fingers(hand_landmarks)
            cv2.putText(frame, f"Fingers Up: {fingers_up}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Detect key press only if one finger is up
            if fingers_up == 1:
                key = detect_key(x, y)
                current_time = time.time()
                if key and current_time - last_pressed_time > debounce_delay:
                    last_pressed_time = current_time
                    cv2.putText(frame, f"Pressed: {key}", (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    if key == "Space":
                        if current_word.strip():
                            typed_words_file.write(current_word.strip() + "\n")
                            typed_words_file.flush()
                        output_file.write(" ")
                        current_word += " "
                    elif key in [';', ',', '.', '/']:
                        output_file.write(key)
                        current_word += key
                    else:
                        output_file.write(key)
                        current_word += key

                    output_file.flush()

                    # Write the current word to the typed_words file when a space is pressed
                    if key == "Space":
                        typed_words_file.write(current_word.strip() + "\n")
                        typed_words_file.flush()
                        current_word = ""

    cv2.imshow("Virtual Keyboard", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
output_file.close()
typed_words_file.close()