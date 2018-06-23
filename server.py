from flask import Flask, render_template, jsonify, url_for, flash, request
from random import sample
import os
import datetime
import numpy as np
import plotly
import pandas as pd
import requests
import urllib
import json

app = Flask(__name__)

jwt = 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImtleS1pZC0xIiwidHlwIjoiSldUIn0.eyJqdGkiOiI5YmNjYjEzNzAzODM0MzIxYjMxYWY1ZWFkNTEzOTc5NiIsInN1YiI6InRlY2h1c3IiLCJzY29wZSI6WyJtZHNwOmNvcmU6QWRtaW4zcmRQYXJ0eVRlY2hVc2VyIl0sImNsaWVudF9pZCI6InRlY2h1c3IiLCJjaWQiOiJ0ZWNodXNyIiwiYXpwIjoidGVjaHVzciIsImdyYW50X3R5cGUiOiJjbGllbnRfY3JlZGVudGlhbHMiLCJyZXZfc2lnIjoiZmYwMjU3NTAiLCJpYXQiOjE1Mjk1OTA0NDksImV4cCI6MTUyOTU5MjI0OSwiaXNzIjoiaHR0cHM6Ly9zaWxkZXZtcy5waWFtLmV1MS5taW5kc3BoZXJlLmlvL29hdXRoL3Rva2VuIiwiemlkIjoic2lsZGV2bXMiLCJhdWQiOlsidGVjaHVzciJdLCJ0ZW4iOiJzaWxkZXZtcyIsInNjaGVtYXMiOlsidXJuOnNpZW1lbnM6bWluZHNwaGVyZTppYW06djEiXSwiY2F0IjoiY2xpZW50LXRva2VuOnYxIn0.a2CDi3ge9vliDYie-H1Pw8XJVJ-mqwS6lkr3eaGh5YEfGZkbSeqTPaZ7l9ks7DUji4-nesbO4hmn9d3-owSA6izgwRXuelOmsXX5ErHI0YgmHlWR8-Z16wAsrmXW_HvrpRXIM2Qhdj2xQFrzP0S_u9Io9Qu-5mF5UKsQcB8qHjCvM65SkCbC50d2szSWsT84NZRv0ruHv1V89Y-r9ibKCdpKoQjTi6uH3gJGykW_cO4hm_q_x3tsCxe1ViRPq3z7iQ9DkSnM6V9uQ6GBmYD8_watajX2f2nbEtfXD32Y3LI8wfNkx5wVWixu_W2MYwi7jpYPN0ABrBeiCy_xVM4xxg'

@app.route('/')
def root():
    return render_template("home.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/reports')
def reports():
    print(os.getenv("VCAP_APP_PORT"))
    return render_template("reports.html")

@app.route('/floorplan')
def floorplan():
    dataArray = [{'x': 0, 'y': 0.4, 'v': 900},{'x': -0.9, 'y': 0.4, 'v': 900}]
    return render_template("floorplan.html",dataArray = dataArray)

@app.route('/data')
def data():
    return jsonify({'data' : sample(range(10000,20000),100)})

@app.route('/assets')
def assets():
    url = 'https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/?size=200'
    headers = {'Authorization': request.headers["Authorization"]}
    # headers = {'Authorization': jwt}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    for i in range(len(data['_embedded']['assets'])):
        if '152' in data['_embedded']['assets'][i]['name']:
            data['_embedded']['assets'][i]['name'] = '(DELETED)'
    return render_template('assets.html', assets_data = data)

@app.route('/assets/<id>/aspects')
def assets_aspects(id):
    url = 'https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/{0}/aspects'.format(id)
    headers = {'Authorization': request.headers["Authorization"]}
    # headers = {'Authorization': jwt}
    response =requests.get(url, headers=headers)
    return render_template('aspects.html', aspects_data = json.loads(response.text))

@app.route("/timeseries/<asset>/<aspect>/<var>", methods=['GET','POST'])
def timeseries(asset,aspect,var):
    # params_string = ""
    # url="https://gateway.eu1.mindsphere.io/api/iottimeseries/v3/timeseries/{0}/{1}{2}".format(asset,aspect,params_string)
    url="https://gateway.eu1.mindsphere.io/api/iottimeseries/v3/timeseries/{0}/{1}?from=2018-06-18T00:00:00Z&to=2018-06-19T23:50:00Z".format(asset,aspect)
    # headers = {'Authorization': jwt}
    headers = {'Authorization': request.headers["Authorization"]}
    response =requests.get(url, headers=headers)
    (plotdata,plottime) = plotts(json.loads(response.text),var)
    return render_template('timeseries.html',plotdata=plotdata,plottime=plottime)

def plotts(data,var):
    plotdata = []
    plottime = []
    for i in range(len(data)):
        plotdata.append(data[i][var])
        plottime.append(str(data[i]['_time']))
    print(plottime)
    return plotdata, plottime

#test if env is in cloud foundry by getting VCAP port
try:
    port = int(os.getenv("VCAP_APP_PORT"))
except:
    if __name__ == "__main__":
        app.run(debug='true')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
