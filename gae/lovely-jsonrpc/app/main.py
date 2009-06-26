import environment
from google.appengine.ext.webapp import util
from lovely.jsonrpc import wsgi
import demo

def main():
    app = wsgi.WSGIJSONRPCApplication({'demo':demo.DemoAPI()})
    util.run_wsgi_app(app)

if __name__ == '__main__':
    main()
