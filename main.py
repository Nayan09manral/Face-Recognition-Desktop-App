
import pickle

import cv2
import os

import face_recognition

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []

for path in modePathList:
    mode_image = cv2.imread(os.path.join(folderModePath, path))
    # Resize the mode image to match the desired region size
    mode_image = cv2.resize(mode_image, (414, 633))
    imgModeList.append(mode_image)

# Load the encoding
print("Loading Encoded File ...")
file = open('EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentsIds = encodeListKnownWithIds
print(studentsIds)
print("Encode File Loaded")

while True:
    success, img = cap.read()

    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)

    if not success:
        print("Error: Could not read a frame from the webcam.")
        break

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[2]

    for encodeFace , faceLoc in  zip(encodeCurFrame,faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        print("matches",matches)
        print("faceDis",faceDis)

    cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()