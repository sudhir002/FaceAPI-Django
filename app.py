from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
from flask_cors import CORS
#====================================
import eye_distance
from eye_distance import eye_distance_calculate
from face_shape import FaceApp


app = Flask(__name__)
CORS(app)


@app.route('/upload', methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        try:
            base64_string = request.form["imgstring"]
            base64_decode = np.frombuffer(base64.b64decode(base64_string), np.uint8)
            image = cv2.imdecode(base64_decode, cv2.IMREAD_COLOR)
        except Exception as e:
            return ({"status": "problem into read image"})

        try:
            eye_distance = eye_distance_calculate(image)
        except Exception as e:
            eye_distance = "Distance is not found"

        try:
            face_shape_info = FaceApp(image)
        except Exception as e:
            face_shape_info = FaceApp(image)
        recomended_by = face_shape_info["faceShape"]
        if recomended_by == "Rectangular":
            recomended = ["Round", "Oval", "Aviator"]
        elif recomended_by == "Diamond":
            recomended = ["Oval", "Cat", "Eye"]
        elif recomended_by == "Oval Shape":
            recomended = ["Round", "Squar", "Rectangular", "Aviator"]
        elif recomended_by == "Triangle":
            recomended = ["Oval", "Cat", "Eye"]
        elif recomended_by == "Square":
            recomended = ["Round", "Oval", "Cat Eye"]
        elif recomended_by == "Round":
            recomended = ["Cat Eye", "Rectangular"]
        else:
            recomended = ["Shape not found"]

        return jsonify(
            {
                "eye_distance": eye_distance,
                "face_info": face_shape_info,
                "recomendation": recomended
            })
    else:
        return ({"status": "please use post method only"})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
