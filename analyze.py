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


def diff_frames(frame1, frame2, out_frame):
    frame_delta = cv2.absdiff(frame1, frame2)
    thresholded = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresholded = cv2.dilate(thresholded, None, iterations=2)
    (contours, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    movement = False

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(out_frame, (x*4, y*4), (x*4+w*4, y*4+h*4), (0, 255, 0), 2)
        if y > 10:
            movement = True

    return movement

CAPTURE_BUFFER = capture_video(FILEPATH)
CAPTURE_BUFFER_SIZE = len(CAPTURE_BUFFER)

frame = CAPTURE_BUFFER[0]

diffed_segments = 0
for f1 in range(0, CAPTURE_BUFFER_SIZE, 30):
    f2 = f1 + 14
    if f2 >= CAPTURE_BUFFER_SIZE:
        f2 = CAPTURE_BUFFER_SIZE - 1

    frame1 = get_norm_frame(CAPTURE_BUFFER, f1)
    frame2 = get_norm_frame(CAPTURE_BUFFER, f2)

    frame_diff = diff_frames(frame1, frame2, frame)

    if frame_diff:
        diffed_segments += 1

if diffed_segments > 3:
    cv2.imwrite(f"{PATH}/match.jpg", frame)
    sys.exit(0)

print(f"I found {CAPTURE_BUFFER_SIZE} frames in {FILEPATH}, with {diffed_segments} segments with movements.")

sys.exit(1)
