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


def get_norm_frame(buffer, offset):
    """
    Returns a smaller, grayscale and blurry version of a frame
    
    This is used mainly for movement matching, the blur will filter out
    noise. Colors are not needed for movements so they are removed.
    Finally the image is resized to make processing faster.
    
    """
    size = (480, 270)
    frame = buffer[offset]
    frame = cv2.resize(frame, size)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    return frame
