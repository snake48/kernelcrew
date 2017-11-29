

import face_recognition
import picamera
import numpy as np
from bluetooth import *
import sys
import time

if sys.version < '3':
    input = raw_input

addr = None

if len(sys.argv) < 2:
    print("no device specified.  Searching all nearby bluetooth devices for")
    print("the SampleServer service")
else:
    addr = sys.argv[1]
    print("Searching for SampleServer on %s" % addr)

# search for the SampleServer service
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
service_matches = find_service( uuid = uuid, address = addr )

if len(service_matches) == 0:
    print("couldn't find the SampleServer service =(")
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("connecting to \"%s\" on %s" % (name, host))

# Create the client socket
sock=BluetoothSocket( RFCOMM )
sock.connect((host, port))
# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

# Load a sample picture and learn how to recognize it.
print("Loading known face image(s)")
#obama_image = face_recognition.load_image_file("obama_small.jpg")
obama_image = face_recognition.load_image_file("jasper.png")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
o_image = face_recognition.load_image_file("harry.png")
o_face_encoding = face_recognition.face_encodings(o_image)[0]
# Initialize some variables
face_locations = []
face_encodings = []

while True:
    print("Capturing image.")
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(output)
    print("Found {} faces in image.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(output, face_locations)

    # Loop over each face found in the frame to see if it's someone we know.
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces([obama_face_encoding], face_encoding)
        match2 = face_recognition.compare_faces([o_face_encoding], face_encoding)
 
        name = "<Unknown Person>"

        if match[0]:
            name="Jasper"
            data = "qwertyuiop"
            if len(data) == 0: break
            sock.send(data)
            time.sleep(10)
            data = "qwertyuiop"
            sock.send(data)
        elif match2[0]:
            name="Harry"

                   
        

        print("I see someone named {}!".format(name))
sock.close()
