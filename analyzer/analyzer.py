import sys
import os
import cv2
import numpy
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
    first_frame = capture_buffer[0]
    middle_frame = capture_buffer[len(capture_buffer) // 2]
    last_frame = capture_buffer[len(capture_buffer) - 1]

    # night_vision = utils.is_greyscale(first_frame)
    new_movements, movement_mask = utils.get_matches(capture_buffer, working_dir)

    red_img = numpy.zeros((*movement_mask.shape, 3), numpy.uint8)
    red_img[:,:,2] = movement_mask
    middle_frame = cv2.addWeighted(middle_frame, 0.75, red_img, 0.25, 0)

    for f in new_movements:
        x, y, w, h = f["bounding_rect"]
        cv2.rectangle(middle_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        slice = cv2.addWeighted(middle_frame[y:y+h, x:x+w], 0.7, first_frame[y:y+h, x:x+w], 0.3, 0)
        slice = cv2.addWeighted(middle_frame[y:y+h, x:x+w], 0.7, last_frame[y:y+h, x:x+w], 0.3, 0)
        middle_frame[y:y+h, x:x+w] = slice

    utils.write(working_dir, middle_frame)

    if len(new_movements) > 0:
        sys.exit(Movements.FOUND)
    else:
        sys.exit(Movements.NOT_FOUND)


if __name__ == "__main__":
    main()
