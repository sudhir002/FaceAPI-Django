import numpy as np
import cv2
import dlib
from sklearn.cluster import KMeans
import math
from math import degrees
import glob, os

xmlPath = os.path.abspath("static")

face_cascade_path = xmlPath + "/xml" + "/haarcascade_frontalface_default.xml"
predictor_path = xmlPath + "/xml" + "/shape_predictor_68_face_landmarks.dat"
faceCascade = cv2.CascadeClassifier(face_cascade_path)
predictor = dlib.shape_predictor(predictor_path)

fitment_length = 0

def faceMultiScale(gauss):
    faces = faceCascade.detectMultiScale(
        gauss,
        scaleFactor=1.05,
        minNeighbors=5,
        minSize=(100, 100),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    return faces

def FaceApp(imagepath):
    image = cv2.resize(imagepath, (500, 500))
    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gauss = cv2.GaussianBlur(gray, (3, 3), 0)
    faces = faceMultiScale(gauss)
    for (x, y, w, h) in faces:
        dlib_rect = dlib.rectangle(int(x), int(y), int(x+w), int(y+h))
        detected_landmarks = predictor(image, dlib_rect).parts()
        landmarks = np.matrix([[p.x,p.y] for p in detected_landmarks])
        landmark = image.copy()
        mypoint = []
        for idx, point in enumerate(landmarks):
                pos = (point[0, 0], point[0, 1])
                mypoint.append(point)
        forpoint18 = mypoint[17].tolist()
        forpoint27 = mypoint[26].tolist()
        fitment_length = math.sqrt((forpoint18[0][0] - forpoint27[0][0]) ** 2 + (forpoint18[0][1] - forpoint27[0][1]) ** 2)
        fitment_length = fitment_length + 10

    results = original.copy()
    for (x,y,w,h) in faces:
        cv2.rectangle(results, (x, y), (x+w, y+h), (0, 255, 0), 2)
        temp = original.copy()
        forehead = temp[y:y+int(0.25*h), x:x+w]
        rows, cols, bands = forehead.shape
        X = forehead.reshape(rows*cols, bands)
        """
        Applying kmeans clustering algorithm for forehead with 2 clusters 
        this clustering differentiates between hair and skin (thats why 2 clusters)
        """
        kmeans = KMeans(n_clusters=2, init='k-means++', max_iter=300, n_init=10, random_state=None)
        y_kmeans = kmeans.fit_predict(X)
        for i in range(0,rows):
            for j in range(0,cols):
                if y_kmeans[i*cols+j]==True:
                    forehead[i][j]=[255,255,255]
                if y_kmeans[i*cols+j]==False:
                    forehead[i][j]=[0,0,0]

        forehead_mid = [int(cols/2), int(rows/2) ] #midpoint of forehead
        lef=0
        pixel_value = forehead[forehead_mid[1], forehead_mid[0]]
        for i in range(0, cols):
            if forehead[forehead_mid[1], forehead_mid[0]-i].all() != pixel_value.all():
                lef = forehead_mid[0]-i
                break
        left = [lef, forehead_mid[1]]
        rig=0
        for i in range(0, cols):
            if forehead[forehead_mid[1], forehead_mid[0]+i].all() != pixel_value.all():
                rig = forehead_mid[0]+i
                break
        right = [rig, forehead_mid[1]]

    line1 = np.subtract(right+y, left+x)[0]

    linepointleft = (landmarks[1, 0], landmarks[1, 1])
    linepointright = (landmarks[15, 0], landmarks[15, 1])
    line2 = np.subtract(linepointright, linepointleft)[0]

    linepointleft = (landmarks[3, 0], landmarks[3, 1])
    linepointright = (landmarks[13, 0], landmarks[13, 1])
    line3 = np.subtract(linepointright, linepointleft)[0]

    linepointbottom = (landmarks[8, 0], landmarks[8, 1])
    linepointtop = (landmarks[8, 0], y)
    line4 = np.subtract(linepointbottom, linepointtop)[1]

    similarity = np.std([line1, line2, line3])
    ovalsimilarity = np.std([line2, line4])

    ax, ay = landmarks[3, 0], landmarks[3, 1]
    bx, by = landmarks[4, 0], landmarks[4, 1]
    cx, cy = landmarks[5, 0], landmarks[5, 1]
    dx, dy = landmarks[6, 0], landmarks[6, 1]

    alpha0 = math.atan2(cy-ay, cx-ax)
    alpha1 = math.atan2(dy-by, dx-bx)
    alpha = alpha1-alpha0
    angle = abs(degrees(alpha))
    angle = 180-angle

    try:
        for i in range(1):

            if similarity < 10:
                if angle < 162:
                    # print('Face Shape is: Square. Jawlines are more angular')
                    faceShape = "Square"
                    break
                else:
                    # print('Face Shape is: Round. Jawlines are not that angular')
                    faceShape = "Round"
                    break

            if ovalsimilarity < 10:
                # print( 'Face Shape is: Diamond. Face Width and Face Length are similar and Face Length is more than Face Width')
                faceShape = "Diamond"
                break
            if line4 > line2:
                if angle < 170:
                    # print('Face Shape is: Rectangular. Face length is largest and jawline are angular ')
                    faceShape = "Rectangular"
                    break
                else:
                    # print('Face Shape is: Oblong. Face length is largest and jawlines are not angular')
                    faceShape = "Oval Shape"
                    break

            if line3 > line1:
                if angle < 165:
                    # print('Face Shape is: Triangle. Forehead is more wider')
                    faceShape = "Triangle"
                    break
    except Exception as e:
        faceShape = "Not Found"

    faceShape_info = {
        "forehead_length": str(line1),
        "face_width": str(line2),
        "jaw_line_length": str(line3),
        "face_length": str(line4),
        "similarity": round(similarity),
        "ovalsimilarity": round(ovalsimilarity),
        "angle_of_the_jaw": round(angle),
        "faceShape": faceShape,
        "fitment_length" : str(round(fitment_length))
    }
    return faceShape_info