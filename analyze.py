#!/usr/bin/env python3

import sys
import cv2
import numpy
import datetime

PATH = sys.argv[1]
FILE = sys.argv[2]
FILEPATH = f"{PATH}/{FILE}"


def capture_video(file_path):
    capture_buffer = []
    cap = cv2.VideoCapture(file_path)

    while cap.isOpened():
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


def avg_color(frame):
    avgcol_f = numpy.average(frame, axis=0)
    return numpy.average(avgcol_f, axis=0)


def diff_frames(f1, f2, out_frame):

    norm_frame1 = get_norm_frame(CAPTURE_BUFFER, f1)
    norm_frame2 = get_norm_frame(CAPTURE_BUFFER, f2)

    frame1 = CAPTURE_BUFFER[f1]
    frame2 = CAPTURE_BUFFER[f2]

    frame_delta = cv2.absdiff(norm_frame1, norm_frame2)
    thresholded = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresholded = cv2.dilate(thresholded, None, iterations=2)
    (contours, _) = cv2.findContours(
        thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    movement = False
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        crop_frame1 = frame1[y * 4 : y * 4 + h * 4, x * 4 : x * 4 + w * 4]
        crop_frame2 = frame2[y * 4 : y * 4 + h * 4, x * 4 : x * 4 + w * 4]

        if not NIGHT_VISION:
            avg_color1 = avg_color(crop_frame1)
            avg_color2 = avg_color(crop_frame2)

            color_channel_1 = avg_color1[0] - avg_color2[0]
            color_channel_2 = avg_color1[1] - avg_color2[1]
            color_channel_3 = avg_color1[2] - avg_color2[2]
        else:
            color_channel_1 = 255
            color_channel_2 = 255
            color_channel_3 = 255

        color_channel_diff_tr = 25
        if (
            color_channel_1 > color_channel_diff_tr
            or color_channel_2 > color_channel_diff_tr
            or color_channel_3 > color_channel_diff_tr
        ):
            cv2.rectangle(
                out_frame,
                (x * 4, y * 4),
                (x * 4 + w * 4, y * 4 + h * 4),
                (0, 255, 0),
                2,
            )
            if y > 12:
                movement = True
                # debug
                # im_v = cv2.vconcat([crop_frame1, crop_frame2])
                # cv2.imwrite(f"{PATH}/debug.jpg", im_v)
        else:
            cv2.rectangle(
                out_frame,
                (x * 4, y * 4),
                (x * 4 + w * 4, y * 4 + h * 4),
                (0, 0, 255),
                2,
            )

    return movement


CAPTURE_BUFFER = capture_video(FILEPATH)
CAPTURE_BUFFER_SIZE = len(CAPTURE_BUFFER)

frame = CAPTURE_BUFFER[0]

avgcol = avg_color(frame)
if int(avgcol[0]) == int(avgcol[1]) and int(avgcol[0]) == int(avgcol[2]):
    NIGHT_VISION = True
else:
    NIGHT_VISION = False

now = datetime.datetime.now()
if now.hour < 8 or now.hour > 19:
    IS_EVENING_OR_NIGHT = True
else:
    IS_EVENING_OR_NIGHT = False

diffed_segments = 0
for f1 in range(0, CAPTURE_BUFFER_SIZE, 30):
    f2 = f1 + 14
    if f2 >= CAPTURE_BUFFER_SIZE:
        f2 = CAPTURE_BUFFER_SIZE - 1

    frame_diff = diff_frames(f1, f2, frame)

    if frame_diff:
        diffed_segments += 1

print(
    f"{FILEPATH}: {CAPTURE_BUFFER_SIZE} frames, {diffed_segments} move, night:{NIGHT_VISION},{IS_EVENING_OR_NIGHT}"
)

if NIGHT_VISION and diffed_segments > 0 and IS_EVENING_OR_NIGHT:
    cv2.imwrite(f"{PATH}/match.jpg", frame)
    sys.exit(0)
elif diffed_segments > 3:
    cv2.imwrite(f"{PATH}/match.jpg", frame)
    sys.exit(0)

sys.exit(1)
