# Basic Python app on MindSphere

For this app to run locally the it needs to be authenticated to communicate with the MindSphere APIs. To get client credentials, follow [these steps](https://developer.mindsphere.io/howto/howto-selfhosted/index.html#step-1-create-service-credentials).

Afterwards create a new "vars.py" file and add to root folder with below code:

```py
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

def getToken():
    tenantID = '<tenant name>'
    tokenURL = 'https://'+tenantID+'.piam.eu1.mindsphere.io/oauth/token'
    credentials = {
        'client_id': '<client id>',
        'client_secret': r'<client secret>',
    }
    

    oauthclient = BackendApplicationClient(client_id=credentials['client_id'])
    oauthsession = OAuth2Session(client=oauthclient)
    token = oauthsession.fetch_token(token_url=tokenURL, client_id=credentials['client_id'],
            client_secret=credentials['client_secret'])
    return token
```

Alternatively, hard code the token with a temporary bearer token, which you can reterieve using ([this app](https://github.com/rexkc/mdsp-token-vendor)):

```py
def getToken():
    token = 'bearer ' + '<bearer token>'
    return token
```

### Running on Mindsphere
Ensure that you have Cloud Foundry installed on your computer and are correctly logged in ([more info here](https://developer.mindsphere.io/howto/howto-cloud-foundry/index.html)).
Change the name of your app within manifest.yml
```yaml
#manifest.yml
applications:
 - name: <YourAppNameHere>
  instances: 1
  memory: 64MB
  disk_quota: 512MB
  buildpack: python_buildpack
  command: python server.py
```
Push the app to your MindSphere instance with
```sh
$ cf push
```
Then follow the ([steps on the developer site](https://developer.mindsphere.io/howto/howto-cf-running-app.html#deploy-the-application-to-cloud-foundry-via-cf-cli)) to register the application on MindSphere.

### Test locally
This script requires [Python2](https://www.python.org/download/releases/2.0/) to run, ensure vars.py in previous step is prepared.

Install the required python packages run:
```sh
$ pip install -r requirements.txt
```
To run locally you need to authenticate your app to communicate with MindSphere api. I used a technical user, you can get one following  [these steps](https://developer.mindsphere.io/howto/howto-selfhosted/index.html#step-1-create-service-credentials).  Afterwards you need to add those details to vars.py
Alternatively, you may want to use a bearer token, which will need to be added to vars.py
```sh
$ python server.py
```
