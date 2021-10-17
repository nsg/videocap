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
    camera = file.split("/")[0]
    video_source = f"{path}/{file}"

    if "mp4" in camera:
        working_dir = f"{path}"
    else:
        working_dir = f"{path}/{camera}"

    capture_buffer = utils.capture_video(video_source)
    middle_frame = capture_buffer[len(capture_buffer) // 2]

    # night_vision = utils.is_greyscale(first_frame)
    new_movements = utils.get_new_movements(capture_buffer, working_dir)

    for f in new_movements:
        x, y, w, h = f["bounding_rect"]
        cv2.rectangle(middle_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    utils.write(working_dir, middle_frame)

    if len(new_movements) > 0:
        sys.exit(Movements.FOUND)
    else:
        sys.exit(Movements.NOT_FOUND)


if __name__ == "__main__":
    main()
