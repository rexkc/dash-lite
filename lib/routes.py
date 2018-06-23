from functions import *
from flask import Flask, render_template, jsonify, url_for, request
from random import sample
import requests
import json
import os

webServer = Flask(__name__)

@webServer.route('/home')
def home():
    return render_template("home.html")

@webServer.route('/reports')
def reports():
    print(os.getenv("VCAP_APP_PORT"))
    return render_template("reports.html")

@webServer.route('/data')
def data():
    return jsonify({'data' : sample(range(10000,20000),100)})

@webServer.route('/assets')
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

@webServer.route('/assets/<id>/aspects')
def assets_aspects(id):
    url = 'https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/{0}/aspects'.format(id)
    headers = {'Authorization': request.headers["Authorization"]}
    # headers = {'Authorization': jwt}
    response =requests.get(url, headers=headers)
    return render_template('aspects.html', aspects_data = json.loads(response.text))

@webServer.route("/timeseries/<asset>/<aspect>/<var>", methods=['GET','POST'])
def timeseries(asset,aspect,var):
    url="https://gateway.eu1.mindsphere.io/api/iottimeseries/v3/timeseries/{0}/{1}?from=2018-06-18T00:00:00Z&to=2018-06-19T23:50:00Z".format(asset,aspect)
    # headers = {'Authorization': jwt}
    headers = {'Authorization': request.headers["Authorization"]}
    response =requests.get(url, headers=headers)
    (plotdata,plottime) = plotts(json.loads(response.text),var)
    return render_template('timeseries.html',plotdata=plotdata,plottime=plottime)