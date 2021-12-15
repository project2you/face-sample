import json
import os
import face_recognition
import time
import sys
import base64

import numpy as np
from flask_cors import CORS

from flask import Flask, request, jsonify , make_response

import random
import string

import random

import urllib
import cv2
from skimage import io


def get_random_string(length):
    # put your letters in the following string
    sample_letters = 'abcdefghi'
    result_str = ''.join((random.choice(sample_letters) for i in range(length)))
    return  result_str


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Flask app should start in global layout
app = Flask(__name__)
CORS(app)

sys.stdout.flush()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST') # Put any other methods you need here
    return response

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello go!</h1>"

@app.route("/api", methods=['POST'])
def api():
    if request.method == 'POST':
       content = request.json
       url_image = content['url_image']

       imgdata = base64.b64decode(content['faceid'])
       gen = get_random_string(4)
       face1 = 'upload/face1_'+gen+'.jpg'

       with open(face1, 'wb') as fh:
          fh.write(imgdata)

       start = time.time()
       # Load face 1
       load_file1 = face_recognition.load_image_file(face1)
       face1_encoding = face_recognition.face_encodings(load_file1)[0]

       known_encodings = [
          face1_encoding,
       ]
      
       # Load face 2
       #image_to_test = face_recognition.load_image_file("kim.jpg")
       image_to_test  = io.imread(url_image+'.jpg')

       face2_encoding = face_recognition.face_encodings(image_to_test)[0]

       # See how far apart the test image is from the known faces
       face_distances = face_recognition.face_distance(known_encodings, face2_encoding)

       for i, face_distance in enumerate(face_distances):
          print("distance of {:.2} from known image #{}".format((1-face_distance), i))
          value = round(1-face_distance,2) * 100

       end = time.time() 
       finish = end - start

       return jsonify({"confidence": value})
       #return jsonify({"data1":content['faceid']})


def verify(file1,file2):
    #file1 = request.files['file1']1111111111111
    #file2 = request.files['file2']

    #if file1 and allowed_file(file1.filename):
    #    file1.save(file1.filename)

    #if file2 and allowed_file(file2.filename):
    #    file2.save(file2.filename)

    start = time.time()
    face1 = face_recognition.load_image_file(file1)

    # Get the face encodings for the known images
    face1_encoding = face_recognition.face_encodings(face1)[0]

    known_encodings = [
        face1_encoding,
    ]

    # Load a test image and get encondings for it
    image_to_test = face_recognition.load_image_file('test1.jpg')
    image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]

    # See how far apart the test image is from the known faces
    face_distances = face_recognition.face_distance(known_encodings, image_to_test_encoding)

    #print(face_distances)

    for i, face_distance in enumerate(face_distances):
       print("distance of {:.2} from known image #{}".format((1-face_distance), i))
       value = 1-face_distance
       value = '%.2f' %value

    end = time.time() 
    finish = end - start
    #return  str(value)
    return str(value)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0', threaded=True)
