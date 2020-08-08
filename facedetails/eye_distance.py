import cv2
import math

xmlPath = os.path.abspath("static")
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def eye_distance_calculate(imgg):
    image = cv2.resize(imgg, (500, 500))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ex, ey, ew, eh = 0.0, 0.0, 0.0, 0.0
    centers = []
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = image[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            centers.append((x + int(ex + 0.5 * ew), y + int(ey + 0.5 * eh)))
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (15, 1, 235), 5)

    distance = math.sqrt((centers[0][0] - centers[1][0]) ** 2 + (centers[0][1] - centers[1][1]) ** 2)
    return  (round(distance))
