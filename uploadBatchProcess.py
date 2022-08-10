import time
import requests
import pyrebase

firebaseConfig = {
  "databaseURL": "https://project1-f8315-default-rtdb.firebaseio.com",
  "apiKey": "AIzaSyDB9SF_UZ2_7Ki-GfWdnXBXK_D-x_WR_rA",
  "authDomain": "project1-f8315.firebaseapp.com",
  "projectId": "project1-f8315",
  "storageBucket": "project1-f8315.appspot.com",
  "messagingSenderId": "679127440004",
  "appId": "1:679127440004:web:033e7a6acdcf14c72b00d1",
  "measurementId": "G-NCBJWESB90"}

r = requests.get("http://api.marketstack.com/v1/eod?access_key=724933db1dd416011718aeb8992372be&symbols=AAPL")

while True:
    if r.status_code == 200:
        data = r.json()
        firebase = pyrebase.initialize_app(firebaseConfig)
        database = firebase.database()
        database.child("Stocks").set(data)
        time.sleep(86400)
    else:
        exit()




