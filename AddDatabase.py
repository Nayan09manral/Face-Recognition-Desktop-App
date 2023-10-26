import firebase_admin
from firebase_admin import credentials
from firebase_admin import  db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendancerealtime-d2c47-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "1234":
        {
            "Name": "Emili Blunt",
            "Major": "computer science",
            "Starting_year": 2020,
            "Total_attendance": 16,
            "Standing": "G",
            "Year": "4",
            "Last_attendance_time": "2023-10-05 00:54:22"

        },
"1235":
        {
            "Name": "Elon Musk",
            "Major": "computer science",
            "Starting_year": 2020,
            "Total_attendance": 17,
            "Standing": "G",
            "Year": "4",
            "Last_attendance_time": "2023-10-05 00:50:22"

        },
"1236":
        {
            "Name": "Nayan Manral",
            "Major": "computer science",
            "Starting_year": 2020,
            "Total_attendance": 46,
            "Standing": "G",
            "Year": "4",
            "Last_attendance_time": "2023-10-05 00:44:22"

        }

}

for key, value in data.items():
    ref.child(key).set(value)