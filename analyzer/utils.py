import os.path
import numpy
import cv2


def capture_video(file_path):
    """ Returns a list of all frames in a video segment """
    capture_buffer = []
    cap = cv2.VideoCapture(file_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        capture_buffer.append(frame)

    cap.release()
    return capture_buffer


def avg_color(frame):
    """
    Returns the averange color of a frame

    Each color component is returned separately. The first average will averange
    on one axis, the second merges them to just a single value per color channel.
    """
    avgcol_f = numpy.average(frame, axis=0)
    return numpy.average(avgcol_f, axis=0)


def is_greyscale(frame):
    """
    Compare the color channels to see if the picture is greyscale
    
    This is used to detect of the night mode is enabled
    """

    avgcol = avg_color(frame)
    if int(avgcol[0]) == int(avgcol[1]) and int(avgcol[0]) == int(avgcol[2]):
        return True
    return False


def get_norm_frame(frame, size=(480, 270), blur=(5, 5)):
    """
    Returns a smaller, grayscale and blurry version of a frame
    
    This is used mainly for movement matching, the blur will filter out
    noise. Colors are not needed for movements so they are removed.
    Finally the image is resized to make processing faster.
    
    """
    frame = cv2.resize(frame, size)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, blur, 0)
    return frame


def write(path, frame, name="match"):
    """ Write file to disk """
    cv2.imwrite(f"{path}/{name}.jpg", frame)


def read(path, name="match", flag=cv2.IMREAD_UNCHANGED, default_content=None):
    """ Read file to disk """
    if os.path.exists(f"{path}/{name}.jpg"):
        return cv2.imread(f"{path}/{name}.jpg", flag)
    else:
        return default_content


def get_movement_mask(frame1, frame2):
    """
    Detect movements between two frames

    Return a movement mask
    """

    frame1 = get_norm_frame(frame1)
    frame2 = get_norm_frame(frame2)

    frame_delta = cv2.absdiff(frame1, frame2)
    threshold = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations=2)
    frame = cv2.bitwise_and(frame_delta, frame_delta, mask=threshold)

    return frame


def get_movements_mask(frame_sequence: list, size=(480, 270)):
    """
    Detect movements in a sequence of frames

    Return a marged movement mask
    """

    movement_mask = numpy.zeros(size, dtype="uint8")

    for frame_number in range(0, len(frame_sequence) - 1):
        frame1 = frame_sequence[frame_number]
        frame2 = frame_sequence[frame_number + 1]
        mask = get_movement_mask(frame1, frame2)
        movement_mask = cv2.add(movement_mask, mask)

    return movement_mask


def get_new_movements(
    frame_sequence: list, path, size=(270, 480), full_size=(1920, 1080)
):
    """
    Detect movements in a sequence of frames, return frame slices

    This function detect movements in a frame and returns these sections of
    the frame in a datastructure. These frames are later sent to extensions
    to classify if these are something to care about or not.
    """

    black_img = numpy.full(size, 0, numpy.uint8)
    old_movement_mask = read(path, "mask", default_content=black_img)
    movement_mask = get_movements_mask(frame_sequence, size)
    store_movement_mask = cv2.addWeighted(old_movement_mask, 0.99, black_img, 0.01, 0)
    movement_threshold = cv2.threshold(movement_mask, 5, 255, cv2.THRESH_BINARY)[1]
    store_movement_mask = cv2.add(store_movement_mask, movement_threshold)

    # threshold = cv2.dilate(old_movement_mask, None, iterations=32)
    neg_old_movement_mask = cv2.bitwise_not(old_movement_mask)
    neg_old_movement_mask = cv2.bitwise_or(
        movement_mask, movement_mask, mask=neg_old_movement_mask
    )

    neg_old_movement_mask = cv2.resize(neg_old_movement_mask, full_size)

    (contours, _) = cv2.findContours(
        neg_old_movement_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    movement_matches = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        crop_frame = frame_sequence[0][y : y + h, x : x + w]

        if y > 40:  # Ignore the timestamp
            movement_matches.append(
                {"bounding_rect": (x, y, w, h), "frame_slice": crop_frame}
            )

    write(path, store_movement_mask, "mask")

    return (movement_matches, cv2.resize(store_movement_mask, full_size))
