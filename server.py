from functions import populateFloorplan, plotts, requestHeaders
from flask import Flask, render_template, jsonify, url_for, flash, request
from random import sample
import os, datetime
import numpy as np
import plotly
import requests, urllib
import json

app = Flask(__name__)

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
    dataArray = populateFloorplan('58c75abe35a24a57a18754170d498f4e','BuildingSecurityAspect','2017-11-30T00:00:00Z','2017-12-07T00:00:00Z')
    return render_template("floorplan.html",dataArray = dataArray)

@app.route('/data')
def data():
    return jsonify({'data' : sample(range(10000,20000),100)})

@app.route('/assets')
def assets():
    url = 'https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/?size=200'
    response = requests.get(url, headers=requestHeaders())
    data = json.loads(response.text)
    for i in range(len(data['_embedded']['assets'])):
        if '152' in data['_embedded']['assets'][i]['name']:
            data['_embedded']['assets'][i]['name'] = '(DELETED)'
    return render_template('assets.html', assets_data = data)

@app.route('/assets/<id>/aspects')
def assets_aspects(id):
    url = 'https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/{0}/aspects'.format(id)
    response =requests.get(url, headers=requestHeaders())
    return render_template('aspects.html', aspects_data = json.loads(response.text))

@app.route("/timeseries/<asset>/<aspect>/<var>", methods=['GET','POST'])
def timeseries(asset,aspect,var):   
    url="https://gateway.eu1.mindsphere.io/api/iottimeseries/v3/timeseries/{0}/{1}?from=2018-06-18T00:00:00Z&to=2018-06-19T23:50:00Z".format(asset,aspect)
    response =requests.get(url, headers=requestHeaders())
    (plotdata,plottime) = plotts(json.loads(response.text),var)
    return render_template('timeseries.html',plotdata=plotdata,plottime=plottime)

#test if env is in cloud foundry by getting VCAP port
try:
    port = int(os.getenv("VCAP_APP_PORT"))
except:
    if __name__ == "__main__":
        app.run(debug='true')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
