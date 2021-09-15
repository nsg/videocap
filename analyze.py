#!/usr/bin/env python3

import sys
import cv2

PATH=sys.argv[1]
FILE=sys.argv[2]
FILEPATH = f"{PATH}/{FILE}"


def capture_video(file_path):
    capture_buffer = []
    cap = cv2.VideoCapture(file_path)

    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break

        capture_buffer.append(frame)

    cap.release()
    return capture_buffer


def get_norm_frame(buffer, offset):
    size = (480, 270)
    frame = buffer[offset]
    frame = cv2.resize(frame, size)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    return frame

CAPTURE_BUFFER = capture_video(FILEPATH)
print(f"Found {len(CAPTURE_BUFFER)} frames in {FILEPATH}")

frame = CAPTURE_BUFFER[0]

first_frame = get_norm_frame(CAPTURE_BUFFER, 0)
middle_frame = get_norm_frame(CAPTURE_BUFFER, len(CAPTURE_BUFFER)//2)

frame_delta = cv2.absdiff(first_frame, middle_frame)
thresholded = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
thresholded = cv2.dilate(thresholded, None, iterations=2)
(contours, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

movement = False

for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(frame, (x*4, y*4), (x*4+w*4, y*4+h*4), (0, 255, 0), 2)
    if y > 10:
        movement = True

if movement:
    cv2.imwrite(f"{PATH}/match.jpg", frame)
    sys.exit(0)

sys.exit(1)
