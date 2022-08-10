from flask import Flask, jsonify, request, render_template
import pandas as pd
import json
import pyrebase
from plotly import graph_objects as go
import plotly

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

@app.route("/")
def index():
    stocks = db.child("Stocks").child("data").get().val()
    df = pd.json_normalize(stocks)
    fig = go.Figure(data= [go.Candlestick(x=df['date'], open= df['open'], high= df['high'], low= df['low'], close= df['close'])])
    fig.update_layout(xaxis_rangeslider_visible=False, template = "plotly_dark")
    fig.update_layout(yaxis_title="AALP price USD", xaxis_title = 'Date')
    fig.update_yaxes(type="log")
    graph1json = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', graph1json = graph1json )

@app.route("/scatterchart.html")
def scatterchart():
    stocks = db.child("Stocks").child("data").get().val()
    df = pd.json_normalize(stocks)
    df['date'] = pd.to_datetime(df['date'])
    df['date_new'] = df['date'].dt.date
    linechart = {"Date":"Volume"}
    linechart.update(dict(df[['date_new', 'volume']].values))
    return render_template('scatterchart.html', data = linechart)

@app.route("/histogram.html")
def histogram():
    stocks = db.child("Stocks").child("data").get().val()
    df = pd.json_normalize(stocks)
    df['date'] = pd.to_datetime(df['date'])
    df['date_new'] = df['date'].dt.date
    linechart = {"Date":"High"}
    linechart.update(dict(df[['date_new', 'high']].values))
    return render_template('histogram.html', data = linechart)

@app.route("/combochart.html")
def combochart():
    stocks = db.child("Stocks").child("data").get().val()
    df = pd.json_normalize(stocks)
    df['date'] = pd.to_datetime(df['date'])
    df['date_new'] = df['date'].dt.date
    df['variation_closeopen'] = df['close'] - df['open']
    linechart = {"Date":"profit"}
    linechart.update(dict(df[['date_new', 'variation_closeopen']].values))
    return render_template('combochart.html', data = linechart)

if __name__ == "__main__":
    app.run(debug=True)