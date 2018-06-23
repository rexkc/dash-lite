from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from server import server
from routes import webServer
import sys,os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

myApp = DispatcherMiddleware(server,{'/home': webServer})

if __name__ == '__main__':
   run_simple('127.0.0.1', 3000, myApp, use_reloader=True, use_debugger=True)

#test if env is in cloud foundry by getting VCAP port
try:
    port = int(os.getenv("VCAP_APP_PORT"))
except:
    if __name__ == "__main__":
        server.run(debug='true')

if __name__ == "__main__":
    server.run(host='0.0.0.0', port=port)
