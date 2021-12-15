import json
import os
import face_recognition
import time
import sys


from flask import Flask
from flask import request
from flask import make_response
import numpy as np

# Flask app should start in global layout
app = Flask(__name__)
sys.stdout.flush()


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/api", methods=['GET', 'POST'])
def webhook():
    content = request.json
    print (content)
    return jsonify(request.json)

@app.route("/face")
def face():
    start = time.time()
    known_obama_image = face_recognition.load_image_file("test1.jpg")
    #known_biden_image = face_recognition.load_image_file("biden.jpg")

    # Get the face encodings for the known images
    obama_face_encoding = face_recognition.face_encodings(known_obama_image)[0]
    #biden_face_encoding = face_recognition.face_encodings(known_biden_image)[0]

    known_encodings = [
        obama_face_encoding,
        #biden_face_encoding
    ]

    # Load a test image and get encondings for it
    image_to_test = face_recognition.load_image_file("test2.jpg")
    image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]

    # See how far apart the test image is from the known faces
    face_distances = face_recognition.face_distance(known_encodings, image_to_test_encoding)

    print(face_distances)

    for i, face_distance in enumerate(face_distances):
        print("distance of {:.2} from known image #{}".format((1-face_distance), i), flush=True)
        #print("- With a normal cutoff of 0.6, would the test image match the known image? {}".format(face_distance < 0.6))
        #print("- With a very strict cutoff of 0.5, would the test image match the known image? {}".format(face_distance < 0.5))
        print()

    end = time.time() 
    print(end - start)
    return 'ok'


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0', threaded=True)
