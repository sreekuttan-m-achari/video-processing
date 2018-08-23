import cv2
import zmq
import base64
import numpy as np

cascPath = "haarcascade_frontalface_default.xml"

# Create the haar cascade
face_cascade = cv2.CascadeClassifier(cascPath)

context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.bind('tcp://*:5555')
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

while True:
    try:
        frame = footage_socket.recv_string()
        img = base64.b64decode(frame)
        npimg = np.fromstring(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        source = cv2.flip(source, 1)

        gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))

        # print("The number of faces found = ", len(faces))

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(source, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Faces found", source)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        break
