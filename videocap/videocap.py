import time
import argparse
import cv2
import numpy


def gray_blur(frame):
    width_4 = int(len(frame[0]) / 4)
    height_4 = int(len(frame) / 4)
    frame = cv2.resize(frame, (width_4, height_4))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (15, 15), 0)
    cv2.imshow("GRAY", gray)
    return gray


def detect_movement(frame1, frame2, movement_limit):
    frame1 = gray_blur(frame1)
    frame2 = gray_blur(frame2)
    frame_delta = cv2.absdiff(frame1, frame2)
    threshold = cv2.threshold(frame_delta, movement_limit, 255, cv2.THRESH_BINARY)[1]
    (contours, _) = cv2.findContours(
        threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    return (len(contours) > 0, contours)


def main(args):
    trigger_movement_level = args.trigger_movement
    movement_limit = args.movement_limit
    increase_movement_value = 1.0
    decrease_movement_value = 0.1
    movement_level = 0
    frame_number = 0

    vcap = cv2.VideoCapture(args.camera)
    width = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width_4 = int(width / 4)
    height_4 = int(height / 4)
    fps = int(vcap.get(cv2.CAP_PROP_FPS))
    fps_8 = int(fps / 8)

    fourcc = cv2.VideoWriter_fourcc("M", "J", "P", "G")
    out_full = cv2.VideoWriter(f"{args.output}-full.avi", fourcc, fps, (width, height))
    out_low = cv2.VideoWriter(
        f"{args.output}-low.avi", fourcc, fps_8, (width_4, height_4)
    )

    # A buffer of the last 20 frames
    frame_buffer = []
    for i in range(0, 20):
        frame_buffer.append(numpy.full((height, width, 3), 0, numpy.uint8))

    while True:
        ret, frame = vcap.read()
        if ret:
            frame_buffer.append(frame.copy())
            frame_buffer.pop(0)

            ret, contours = detect_movement(frame_buffer[9], frame_buffer[19], movement_limit)
            cv2.putText(frame, str(int(movement_level)), (width-100, height-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            if ret:
                movement_level += increase_movement_value

                if movement_level > trigger_movement_level:
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)


                for c in contours:
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(
                        frame, (x * 4, y * 4), (x * 4 + w * 4, y * 4 + h * 4), color, 2
                    )

            if movement_level > trigger_movement_level:
                out_full.write(frame)
                if frame_number % 8 == 0:
                    frame_4 = cv2.resize(frame, (int(width / 4), int(height / 4)))
                    out_low.write(frame_4)

            if movement_level > 0:
                movement_level -= decrease_movement_value
            elif movement_level < 0:
                movement_level = 0

            cv2.imshow("VIDEO", frame)
        cv2.waitKey(1)
        frame_number += 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--trigger-movement", type=float, default=50, help="Trigger movement level"
    )
    ap.add_argument(
        "--movement-limit", type=float, default=25, help="Movement lower"
    )
    ap.add_argument(
        "--output",
        type=str,
        default="output",
        help="Name of output file with movements",
    )
    ap.add_argument("--camera", type=str, required=True, help="Video Source")
    main(ap.parse_args())
