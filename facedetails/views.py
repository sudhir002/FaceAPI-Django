# date - 29-07-2020
# author - Sudhir kumar

import os
import math
import base64
import cv2
import numpy as np
import socketio
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from facedetails.face import faceMultiScale, FaceApp
from engineio.payload import Payload

Payload.max_decode_packets = 500
sio = socketio.Server(cors_allowed_origins='*')

xmlPath = os.path.abspath("static")
eye_cascade = cv2.CascadeClassifier(xmlPath + "/xml" + '/haarcascade_eye.xml')

def eye_distance_calculate(imgg):
    image = cv2.resize(imgg, (500, 500))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ex, ey, ew, eh = 0.0, 0.0, 0.0, 0.0
    centers = []
    faces = faceMultiScale(gray)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = image[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            centers.append((x + int(ex + 0.5 * ew), y + int(ey + 0.5 * eh)))
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (15, 1, 235), 5)
    distance = math.sqrt((centers[0][0] - centers[1][0]) ** 2 + (centers[0][1] - centers[1][1]) ** 2)
    return  (round(distance))


def imgBase64decode(data):
    nparr = np.fromstring(base64.b64decode(data), np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image

def welcome(request):
    data = {
        "My Name": "Suhir Kumar Singh",
        "Occupation": "AI Engineer",
        "FaceDetails_API": "/faceDetails"
    }
    return render(request, "index.html")


def faceApp(request):
    data = {
        "My Name": "Suhir Kumar Singh",
        "Occupation": "AI Engineer",
        "FaceDetails_API": "/faceDetails"
    }
    return render(request, "welcome.html")


@sio.on('input')
def input(sid, data):
    try:
        data = data.split("image/jpeg;base64,")[1]
    except:
        sio.emit("result", "no image")

    image = imgBase64decode(data)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceMultiScale(gray)
    count_faces = len(faces)
    if count_faces >= 1:
        for x, y, w, h in faces:
            x = x
            y = y
            w = w
            h = h
        try:
            eye_distance = eye_distance_calculate(image)
            print("eyed===", eye_distance)
        except Exception as e:
            eye_distance = "Distance is not found"

        try:
            face_shape_info = FaceApp(image)
        except Exception as e:
            face_shape_info = FaceApp(image)
            print("-=-=-=-=here-=-=")
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
            
        print("-=-=-=-=", face_shape_info)

        resultData = {
            "faceDetect": {"x":x.tolist(), "y":y.tolist(), "w":w.tolist(), "h": h.tolist(), "NoOfFaces" :count_faces},
            "eye_distance": eye_distance,
            "face_info": face_shape_info,
            "recomendation": recomended
        }
        sio.emit("result", [{"NumberOfFaces": resultData}])
    else:
        sio.emit("result", { "NumberOfFaces" :count_faces})


