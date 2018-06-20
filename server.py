from flask import Flask, render_template, jsonify
from random import sample
import os

app = Flask(__name__)

@app.route('/')
def root():
    return render_template("home.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/reports')
def reports():
    return render_template("reports.html")

@app.route('/chart')
def chart():
    return render_template("chart.html")

@app.route('/data')
def data():
    return jsonify({'results' : sample(range(1,10),5)})

@app.route('/assets')
def assets():
    url = 'https://gateway.eu1.mindsphere.io/api/assetmanagement/v3/assets/?size=200'
    jwt= request.headers["Authorization"]
    headers = {'Authorization': jwt}
    response =requests.get(url, headers=headers)
    data=json.loads(response.text)
    return render_template('assets.html', assets_data = data)

#test if env is in cloud foundry by getting VCAP port
try:
    port = int(os.getenv("VCAP_APP_PORT"))
except:
    if __name__ == "__main__":
        app.run(debug='true')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
