import os
import json
import datetime
import requests
import plotly
import plotly.graph_objs as go
from flask import request
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from vars import tokenURL,credentials

## If using bearer token, replace requestHeaders() function with below function
# def requestHeaders():
#     headers = {'Authorization': 'Bearer ' + '<paste bearer token here>'}
#     return headers

def getToken():
    # Function to create a backend client and retrieve a token
    oauthclient = BackendApplicationClient(client_id=credentials['client_id'])
    oauthsession = OAuth2Session(client=oauthclient)
    token = oauthsession.fetch_token(token_url=tokenURL, client_id=credentials['client_id'],
            client_secret=credentials['client_secret'])
    return token

tokenTime = ''
currentToken = ''
def requestHeaders():
    # Function for constructing request headers
    global tokenTime
    global currentToken
    try:
        int(os.getenv("VCAP_APPLICATION")) #app is running in cloud foundry
        headers =  {'Authorization': request.headers["Authorization"]}
    except:
        if (tokenTime == '') or (datetime.datetime.now() > tokenTime + datetime.timedelta(minutes = 25)): #check expiry
            currentToken = getToken()
            tokenTime = datetime.datetime.fromtimestamp(currentToken['expires_at'])
            headers = {'Authorization': 'Bearer ' + currentToken['access_token']}
        else:
            headers = {'Authorization': 'Bearer ' + currentToken['access_token']}
    return headers

def getTimeSeries(asset,aspect,variable,dateFrom,dateTo):
    url="https://gateway.eu1.mindsphere.io/api/iottimeseries/v3/timeseries/{0}/{1}?from={2}&to={3}&select={4}".format(asset,aspect,dateFrom,dateTo,variable)
    response =requests.get(url, headers=requestHeaders())
    graphJSON = plotTS(json.loads(response.text),variable)
    return graphJSON

def plotTS(data,variable):
    plotData = []
    plotTime = []
    for i in range(len(data)):
        try:
            plotData.append(data[i][variable])
            plotTime.append(str(data[i]['_time']))
        except:
            pass # ignore datapoints without the variable

    graph = dict(
        data=[go.Scatter(
            x= plotTime,
            y= plotData
        )],
        layout=dict(
            title=variable,
            yaxis=dict(
                title="value"
            ),
            xaxis=dict(
                title="time",
                rangeslider={}
            )
        )
    )
    graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
