import os

import cv2
import face_recognition
import pickle

# Importing student images
folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentsIds = []

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    # print(path)
    studentsIds.append(os.path.splitext(path)[0])
    print(studentsIds)


def findEncodings(imagesList):

    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding Started...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentsIds]
print("Encodinig Completed")

file = open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()

