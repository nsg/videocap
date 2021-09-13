#!/usr/bin/env python3

import sys
import cv2

PATH=sys.argv[1]
FILE=sys.argv[2]
FILEPATH = f"{PATH}/{FILE}"

cap = cv2.VideoCapture(FILEPATH)

CAPTURE_BUFFER=[]

while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break

    CAPTURE_BUFFER.append(frame)

cap.release()

print(f"Found {len(CAPTURE_BUFFER)} frames in {FILEPATH}")

SIZE = (480, 270)

frame = CAPTURE_BUFFER[0]

first_frame = CAPTURE_BUFFER[0]
first_frame = cv2.resize(first_frame, SIZE)
first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
first_frame = cv2.GaussianBlur(first_frame, (5, 5), 0)

middle_frame = CAPTURE_BUFFER[len(CAPTURE_BUFFER)//2]
middle_frame = cv2.resize(middle_frame, SIZE)
middle_frame = cv2.cvtColor(middle_frame, cv2.COLOR_BGR2GRAY)
middle_frame = cv2.GaussianBlur(middle_frame, (5, 5), 0)

frame_delta = cv2.absdiff(first_frame, middle_frame)
thresholded = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
thresholded = cv2.dilate(thresholded, None, iterations=2)
(contours, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

movement = False

for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(frame, (x*4, y*4), (x*4+w*4, y*4+h*4), (0, 255, 0), 2)
    movement = True

if movement:
    cv2.imwrite(f"{PATH}/match.jpg", frame)
    sys.exit(0)

sys.exit(1)
