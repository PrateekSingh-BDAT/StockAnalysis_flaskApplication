import os
from flask import Flask, request, jsonify
import pyrebase



app = Flask(__name__)

firebaseConfig = {
  "apiKey": "AIzaSyD-RVdcxd_6dskD1W6DdFA0KrMEnxcJVd4",
  "authDomain": "fir-frompython.firebaseapp.com",
  "databaseURL": "https://fir-frompython-default-rtdb.firebaseio.com",
  "projectId": "fir-frompython",
  "storageBucket": "fir-frompython.appspot.com",
  "messagingSenderId": "529313000758",
  "appId": "1:529313000758:web:ec25dcd2311c359fa61797",
  "measurementId": "G-N4VQM7B0M6"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

@app.route("/", methods = ['GET'])
def get_unfilteredview():
    """View all"""
    data = db.child("Stocks").child("data").get()
    return jsonify(data.val())

@app.route('/range/<int:xnasstock_first>/<int:xnasstock_last>', methods = ['GET'])
def get_range(xnasstock_first,xnasstock_last):
    """View Range"""
    stock_list = []
    index = 0
    for index in range(xnasstock_first, xnasstock_last, 1):
        stocks = db.child("Stocks").child("data").child(index).get()
        stock_list.append(dict(stocks.val()))
    return jsonify(stock_list)

@app.route('/specific/<int:stock_id>', methods = ['GET'])
def get_stockid(stock_id):
    """View Specific"""
    found_stock = db.child("Stocks").child("data").child(stock_id).get()
    return jsonify(dict(found_stock.val()))

port = int(os.environ.get('PORT', 3000))
if __name__ == "__main__":
    """Run Flask App"""
    app.run(threaded=True, host = '0.0.0.0', port = port)