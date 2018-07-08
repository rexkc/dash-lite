from functions import populateFloorplan, plotts, requestHeaders
from flask import Flask, render_template, jsonify, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import os, datetime
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
import requests, urllib
import json

app = Flask(__name__)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'locally-debugging'

app.config.from_object(Config)

class resuableForm(FlaskForm):
    dateFrom = StringField('From', validators=[DataRequired()])
    dateTo = StringField('From', validators=[DataRequired()])
    power = StringField('Power', validators=[DataRequired()])
    temperature = StringField('Temperature', validators=[DataRequired()])
    pressure = StringField('Pressure', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def root():
    return render_template("home.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/reports')
def reports():
    return render_template("reports.html")

@app.route('/floorplan')
def floorplan():
    dataArray = populateFloorplan('58c75abe35a24a57a18754170d498f4e','BuildingSecurityAspect','2017-11-30T00:00:00Z','2017-12-07T00:00:00Z')
    return render_template("floorplan.html",dataArray = dataArray)

@app.route('/data')
def data():
    N = 500
    random_x = np.linspace(0, 1, N)
    random_y = np.random.randn(N)
    graph = dict(
        data=[go.Scatter(
            x= random_x,
            y= random_y
        )]
    )
    graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/assets')
def assets():
    url = 'https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/?size=200'
    response = requests.get(url, headers=requestHeaders())
    data = json.loads(response.text)
    # setup for hiding deleted assets
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
    form = resuableForm()
    if form.validate_on_submit():
        dateFrom = form.dateFrom.data
        dateTo = form.dateTo.data
    else:
        currentTime = datetime.datetime.utcnow()
        pastDayTime = currentTime - datetime.timedelta(days = 7)
        dateTo = currentTime.isoformat() + 'Z'
        dateFrom = pastDayTime.isoformat() + 'Z'
    print(dateFrom)
    print(dateTo)
    url="https://gateway.eu1.mindsphere.io/api/iottimeseries/v3/timeseries/{0}/{1}?from={2}&to={3}".format(asset,aspect,dateFrom,dateTo)
    response =requests.get(url, headers=requestHeaders())
    graphJSON = plotts(json.loads(response.text),var)
    return render_template('timeseries.html',graphJSON = graphJSON, form = form, asset = asset, aspect = aspect, var = var)

@app.route("/analytics")
def analytics():
    return render_template('analytics.html')

@app.route("/predict")
def predict():
    body = {}
    body['modelConfiguration'] = {'polynomialDegree' : 1}
    body['metadataConfiguration'] = {
        'outputVariable' : {
            'entityId' : 'Weather',
            'propertySetName': 'tempSensor',
            'propertyName': 'temperature'
            },
        "inputVariables": [{
            "entityId": "Weather",
            "propertySetName": "windDetector",
            "propertyName": "windSpeed"
            }]
        }
    body['trainingData'] = {
        "variable": {
        "entityId": "Weather",
        "propertySetName": "tempSensor"
      },
      "timeSeries": [
        {
          "_time": "2017-10-01T12:00:00.001Z",
          "powerOutputSensor": "20.0"
        },
        {
          "_time": "2017-10-01T12:00:00.002Z",
          "powerOutputSensor": "21.0"
        },
        {
          "_time": "2017-10-01T12:00:00.003Z",
          "powerOutputSensor": "23.0"
        }
      ]
    }
    return render_template('a_trend.html')




#test if env is in cloud foundry by getting VCAP port
try:
    port = int(os.getenv("VCAP_APP_PORT"))
except:
    if __name__ == "__main__":
        app.run(debug='true')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
