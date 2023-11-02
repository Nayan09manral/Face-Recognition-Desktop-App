
import pickle
import cvzone
import numpy as np
import cv2
import os
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import  db
from firebase_admin import storage
import numpy as np

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendancerealtime-d2c47-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancerealtime-d2c47.appspot.com"
})

bucket = storage.bucket()


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

modeType = 0
counter = 0
id = -1
imgStudent = []

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
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    for encodeFace , faceLoc in  zip(encodeCurFrame,faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        # print("matches",matches)
        # print("faceDis",faceDis)

        matchIndex = np.argmin(faceDis)
        # print("Match Index",matchIndex)

        if matches[matchIndex]:
           # print("Known Face Detected")
           # print(studentsIds[matchIndex])
           y1, x2, y2, x1 = faceLoc
           y1, x2, y2, x1 = y1 * 4, x2 * 4 , y2 * 4, x1 * 4
           bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
           imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
           id = studentsIds[matchIndex]

           if counter == 0:
              counter = 1
              modeType = 1

    if counter!= 0:

          if counter ==1:
              # Get the data
              studentsInfo = db.reference(f'Students/{id}').get()
              print(studentsInfo)
              #Get the Image from the storage
              blob = bucket.get_blob(f'Images/{id}.png')
              array = np.frombuffer(blob.download_as_string(), np.uint8)
              imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
              #Update data of attendance
              ref = db.reference(f'Students/{id}')
              studentsInfo['Total_attendance'] +=1
              ref.child('Total_attendance').set(studentsInfo['Total_attendance'])

          if 10<counter<20:
              modeType = 2

          imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

          if counter<=10:
            cv2.putText(imgBackground,str(studentsInfo['Total_attendance']),(861,125),
                        cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
            cv2.putText(imgBackground, str(studentsInfo['Major']), (1006, 550),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(imgBackground, str(id), (1006, 493),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(imgBackground, str(studentsInfo['Standing']), (910, 625),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
            cv2.putText(imgBackground, str(studentsInfo['Year']), (1025, 625),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
            cv2.putText(imgBackground, str(studentsInfo['Starting_year']), (1125, 625),

                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

            (w, h), _ = cv2.getTextSize(studentsInfo['Name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
            offset = (414-w)//2
            cv2.putText(imgBackground, str(studentsInfo['Name']), (800+offset, 445),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)


            imgStudent = cv2.resize(imgStudent, (216, 216))
            imgBackground[175:175 + 216, 909:909 + 216] = imgStudent



          counter+= 1

          if counter>=20:
             counter = 0
             modeType = 0
             studentsInfo = []
             imgStudent = []
             imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


    cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()