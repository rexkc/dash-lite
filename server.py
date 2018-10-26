from functions import plotts, requestHeaders
from flask import Flask, render_template, jsonify, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import os, datetime
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

@app.route('/assets')
def assets():
    url = 'https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets?filter={"and":{"deleted": {"eq": null}}}&size=100'
    response = requests.get(url, headers=requestHeaders())
    data = json.loads(response.text)
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
    url="https://gateway.eu1.mindsphere.io/api/iottimeseries/v3/timeseries/{0}/{1}?from={2}&to={3}".format(asset,aspect,dateFrom,dateTo)
    response =requests.get(url, headers=requestHeaders())
    graphJSON = plotts(json.loads(response.text),var)
    return render_template('timeseries.html',graphJSON = graphJSON, form = form, asset = asset, aspect = aspect, var = var)

#test if env is in cloud foundry by getting VCAP port
try:
    port = int(os.getenv("VCAP_APP_PORT"))
except:
    if __name__ == "__main__":
        app.run(debug='true')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
