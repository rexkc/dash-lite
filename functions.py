import os
import json
import datetime
import plotly
import plotly.graph_objs as go
from flask import request
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from vars import tokenURL,credentials

def getToken():
    # create a backend client and retrieve a token
    oauthclient = BackendApplicationClient(client_id=credentials['client_id'])
    oauthsession = OAuth2Session(client=oauthclient)
    token = oauthsession.fetch_token(token_url=tokenURL, client_id=credentials['client_id'],
            client_secret=credentials['client_secret'])
    return token

tokenTime = ''
currentToken = ''
def requestHeaders():
    global tokenTime
    global currentToken
    try:
        int(os.getenv("VCAP_APP_PORT"))!= 5000 #app is running in cloud foundry
        headers =  {'Authorization': request.headers["Authorization"]}
    except:
        if (tokenTime == '') or (datetime.datetime.now() > tokenTime + datetime.timedelta(minutes = 25)): #check expiry
            currentToken = getToken()
            tokenTime = datetime.datetime.fromtimestamp(currentToken['expires_at'])
            headers = {'Authorization': 'Bearer ' + currentToken['access_token']}
        else:
            headers = {'Authorization': 'Bearer ' + currentToken['access_token']}
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
        )],
        layout=dict(
            title=var,
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