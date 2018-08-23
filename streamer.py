import base64
import cv2
import zmq

controler_ip = '10.0.1.114'
stream_port = '5555'

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://' + controler_ip + ':' + stream_port)

img_quality = 80


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, image = video_capture.read()

    if not ret:
        break

    image = image_resize(image, height=300)

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), img_quality]

    encoded, buffer = cv2.imencode('.jpg', image, encode_param)
    jpg_as_text = base64.b64encode(buffer)

    footage_socket.send(jpg_as_text)

    image = cv2.flip(image, 1)

    cv2.imshow("Stream Source ", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
