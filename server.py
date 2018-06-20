from flask import Flask, render_template, jsonify, url_for, flash, request
from random import sample
import os
import datetime
import numpy as np
import requests
import urllib
import json

app = Flask(__name__)

jwt = 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImtleS1pZC0xIiwidHlwIjoiSldUIn0.eyJqdGkiOiJlNzAyZjlmYzM5ODk0ZGNiOTAxYTJiMzhiZTc4MjMwYiIsInN1YiI6ImRkMzA4ZDIyLTQ0ZjktNDAwOS1hYzdmLTRlMTk2YTNlMjQ5YSIsInNjb3BlIjpbIm1kc3A6Y29yZTp0c20uZnVsbC1hY2Nlc3MiLCJtZHNwOmNvcmU6YWdtLmZ1bGxhY2Nlc3MiLCJtZHNwOmNvcmU6YXNzZXRtYW5hZ2VtZW50LmFkbWluIiwibWRzcDpjb3JlOmlvdC5maWxBZG1pbiJdLCJjbGllbnRfaWQiOiJ0b2tlbi1zaWxkZXZtcyIsImNpZCI6InRva2VuLXNpbGRldm1zIiwiYXpwIjoidG9rZW4tc2lsZGV2bXMiLCJncmFudF90eXBlIjoiYXV0aG9yaXphdGlvbl9jb2RlIiwidXNlcl9pZCI6ImRkMzA4ZDIyLTQ0ZjktNDAwOS1hYzdmLTRlMTk2YTNlMjQ5YSIsIm9yaWdpbiI6InNpbGRldm1zIiwidXNlcl9uYW1lIjoicmV4LmNoZW5Ac2llbWVucy5jb20iLCJlbWFpbCI6InJleC5jaGVuQHNpZW1lbnMuY29tIiwiYXV0aF90aW1lIjoxNTI5NTA0MDU1LCJyZXZfc2lnIjoiYWZjYzM3YmEiLCJpYXQiOjE1Mjk1MDQwNTYsImV4cCI6MTUyOTUwNTg1NiwiaXNzIjoiaHR0cHM6Ly9zaWxkZXZtcy5waWFtLmV1MS5taW5kc3BoZXJlLmlvL29hdXRoL3Rva2VuIiwiemlkIjoic2lsZGV2bXMiLCJhdWQiOlsibWRzcDpjb3JlOmlvdCIsIm1kc3A6Y29yZTp0c20iLCJtZHNwOmNvcmU6YXNzZXRtYW5hZ2VtZW50IiwidG9rZW4tc2lsZGV2bXMiLCJtZHNwOmNvcmU6YWdtIl0sInRlbiI6InNpbGRldm1zIiwic2NoZW1hcyI6WyJ1cm46c2llbWVuczptaW5kc3BoZXJlOmlhbTp2MSJdLCJjYXQiOiJ1c2VyLXRva2VuOnYxIn0.rGIDXa0CRjJgScfxyIwaWVcT-_ja9Gcu7bJmAyMuPwwoYT3AOobH-U7kH0_B-DfKDxXjEO8lazOOK4AjDjeFxcqDxYkTyhsUJCh6sDSPC0_We7sOgALrGgJAhzj_nWte2asX875xz58Jxi1ZwIxrYqteaSKktLOYC1vDAXUB-y6eBlZREwljOg4xZfBi2a363QXIBAX0jfSpwtznhPze16DUXG6JQjgyo9dEONU04HThwT0xhx_TTZh0UwohE5qtasxw0ecNtaDzBF7SN18sBAWze0CJeJzyZ6Ioh1mc_HVIJeaGnCaClfPl9KvpPxlinMta8tyv9qjit16XPuI7-Q'

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

@app.route('/data')
def data():
    return jsonify({'data' : sample(range(10000,20000),100)})

@app.route('/assets')
def assets():
    # response = requests.get("http://pokeapi.co/api/v2/pokemon/1/")
    # print('------------------------success-----------------------')
    # return response.content
    url = 'https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/?size=200'
    # headers = {'Authorization': request.headers["Authorization"]}
    headers = {'Authorization': jwt}
    response = requests.get(url, headers=headers)
    return render_template('assets.html', assets_data = json.loads(response.text))

@app.route('/assets/<id>/aspects')
def assets_aspects(id):
    url = 'https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/{0}/aspects'.format(id)
    # headers = {'Authorization': request.headers["Authorization"]}
    headers = {'Authorization': jwt}
    response =requests.get(url, headers=headers)
    data=json.loads(response.text)
    return render_template('aspects.html', aspects_data = data)

@app.route("/timeseries/<asset>/<aspect>", methods=['GET','POST'])
def timeseries(asset,aspect):
    from_param=request.args.get('from')
    to_param=request.args.get('to')
    preset_param = request.args.get('preset')
    limit_param=request.args.get('limit')
    select_param=request.args.get('select')
    params_string = ""

    if preset_param == "Last Hour":
	    to_param = iso8601datetime(datetime.datetime.utcnow())
	    from_param = iso8601datetime(datetime.datetime.utcnow()-datetime.timedelta(hours=1))
    elif preset_param == "Last 24 Hours":
	    to_param = iso8601datetime(datetime.datetime.utcnow())
	    from_param = iso8601datetime(datetime.datetime.utcnow()-datetime.timedelta(days=1))
    elif preset_param == "Last 7 Days":
	    to_param = iso8601datetime(datetime.datetime.utcnow())
	    from_param = iso8601datetime(datetime.datetime.utcnow()-datetime.timedelta(days=7))
    elif preset_param == "Last 30 Days":
	    to_param = iso8601datetime(datetime.datetime.utcnow())
	    from_param = iso8601datetime(datetime.datetime.utcnow()-datetime.timedelta(days=30))
    elif preset_param == "Custom":
	    pass
    else:
	    pass
    if from_param != None:
	    params_string = params_string + "&from=" + from_param
    if to_param != None:
	    params_string = params_string + "&to=" + to_param
    if limit_param != None:
        params_string = params_string + "&limit=" + limit_param
    if select_param != None or "":
	    params_string = params_string + "&select=" + select_param
    if params_string != "":
	    params_string = "?" + params_string
    url="https://gateway.eu1.mindsphere.io/api/iottimeseries/v3/timeseries/{0}/{1}{2}".format(asset,aspect,params_string)
    headers = {'Authorization': request.headers["Authorization"]}
    response =requests.get(url, headers=headers)
    data=json.loads(response.text)

    plot_data = data_arrays(data)
    #x_data = plot_data[0][0]
    #time_data = plot_data[1]
    #localisetime(time_data)
    
    trace=[]
    for key in plot_data[2]:
        trace.append(go.Scatter(x = plot_data[1][plot_data[2].index(key)],y = plot_data[0][plot_data[2].index(key)],name=key))
        
    graph_data =trace
    graph = plotly.offline.plot(graph_data, include_plotlyjs=False, output_type='div')
    layout = go.Layout(
    dict(title=asset + ' ' + aspect,titlefont=dict(family='Arial',size=22,color='#000000')),
    xaxis=dict(title='Time',titlefont=dict(family='Arial',size=18,color='#000000'))
    )
    
    fig = go.Figure(data=graph_data, layout=layout)
    #temp_graph = plotly.offline.plot(graph_data, include_plotlyjs=False, output_type='div')
    graph = plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')
    params = { 'from': from_param, 'to': to_param, 'limit': limit_param, 'selected': select_param}
    return render_template('timeseries.html', params=params, url=url,asset=asset,aspect=aspect, data=data, graph=Markup(graph),x_data=plot_data[0], time_data=plot_data[1])

#test if env is in cloud foundry by getting VCAP port
try:
    port = int(os.getenv("VCAP_APP_PORT"))
except:
    if __name__ == "__main__":
        app.run(debug='true')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
