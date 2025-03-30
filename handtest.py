import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import time

# Initialize camera and modules
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("C:\\python\\Handrecognition\\Model\\keras_model.h5", 
                        "C:\\python\\Handrecognition\\Model\\labels.txt")

offset = 20
imgSize = 300
labels = ["F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
          "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "A", "B", "C", "D", "E"]

# Open a text file to store the predictions
output_file = open("out.txt", "a")  # Open in append mode

while True:
    success, img = cap.read()
    if not success:
        print("Failed to access the camera.")
        break

    imgOutput = img.copy()
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

        # Ensure cropping is within image boundaries
        try:
            imgCrop = img[y-offset:y+h+offset, x-offset:x+w+offset]
            aspectRatio = h / w

            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal+wGap] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal+hGap, :] = imgResize

            prediction, index = classifier.getPrediction(imgWhite, draw=False)
            print(prediction, index)

            # Write the prediction to the text file
            output_file.write(f"{labels[index]}\n")
            output_file.flush()  # Ensure data is written to the file immediately

            cv2.putText(imgOutput, labels[index], (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 0, 255), 2)
            cv2.rectangle(imgOutput, (x-offset, y-offset), (x+w, y+h), (255, 0, 255), 4)

        except Exception as e:
            print(f"Error during processing: {e}")

        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhite)

    cv2.imshow("Image", imgOutput)

    # Add a key press to turn off the camera
    key = cv2.waitKey(1)
    if key == ord('q'):  # Press 'q' to exit
        print("Turning off the camera...")
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Close the text file
output_file.close()