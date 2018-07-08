import requests
import os
import json
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
from flask import request
from collections import Counter
from vars import token

def requestHeaders():
    try:
        int(os.getenv("VCAP_APP_PORT"))!= 5000 #app is running in cloud foundry
        headers =  {'Authorization': request.headers["Authorization"]}
    except:
        headers = {'Authorization': 'Bearer ' + token['access_token']}
    return headers

def plotts(data,var):
    plotdata = []
    plottime = []
    for i in range(len(data)):
        try:
            plotdata.append(data[i][var])
            plottime.append(str(data[i]['_time']))
        except:
            pass # ignore datapoints without the variable

    graph = dict(
        data=[go.Scatter(
            x= plottime,
            y= plotdata
        )]
    )
    graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def populateFloorplan(Asset,Aspect,dateFrom,dateTo):
    # create request url
    url="https://gateway.eu1.mindsphere.io/api/iottimeseries/v3/timeseries/{0}/{1}?from={2}&to={3}".format(Asset,Aspect,dateFrom,dateTo)
    response =requests.get(url, headers=requestHeaders())
    # load response in dict
    raw_dict = json.loads(response.text)
    # initialize array for returning data
    dataArray = []

    #TODO make all location codes into array so this can run on a for loop (same for message codes) 
    bwNth = [x for x in raw_dict if x['locationCode'] == 30102] # filter for B3 Nth Entry Dr Ea
    counts = Counter(c['messageCode'] for c in bwNth) # get counts of message occurances
    dataArray.append({'label' : 'B3 Nth Entry Dr Ea', 'x': -0.023, 'y': 0.36, 'PB': counts[17300], 'CR' : counts[17200]}) # add data to array

    bwGnd = [x for x in raw_dict if x['locationCode'] == 30206] # filter for B3 Gnd To Link
    counts = Counter(c['messageCode'] for c in bwGnd) # get counts of message occurances
    dataArray.append({'label' : 'B3 Gnd To Link', 'x': 0.76, 'y': -0.2, 'PB': counts[17300], 'CR' : counts[17200]}) # add data to array
    return dataArray