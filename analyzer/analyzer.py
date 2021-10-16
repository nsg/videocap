import sys
import os
import cv2
import utils


class Movements:
    FOUND = 0
    NOT_FOUND = 1


def main():
    path = os.environ["VIDEOCAP_DATA"]
    file = sys.argv[1]
    video_source = f"{path}/{file}"

    capture_buffer = utils.capture_video(video_source)
    middle_frame = capture_buffer[len(capture_buffer)//2]

    # night_vision = utils.is_greyscale(first_frame)
    new_movements = utils.get_new_movements(capture_buffer, path)

    for f in new_movements:
        x, y, w, h = f["bounding_rect"]
        cv2.rectangle(middle_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    utils.write(path, middle_frame)

    if len(new_movements) > 0:
        print(f"Found movement in {video_source}")
        sys.exit(Movements.FOUND)
    else:
        sys.exit(Movements.NOT_FOUND)


if __name__ == "__main__":
    main()
