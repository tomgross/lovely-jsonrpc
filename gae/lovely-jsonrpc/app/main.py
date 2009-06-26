import environment
from google.appengine.ext.webapp import util
from lovely.jsonrpc import wsgi
import demo
from lovely.jsonrpc import dispatcher

def main():
    app = wsgi.WSGIJSONRPCApplication(
        {'demo':dispatcher.JSONRPCDispatcher(demo.DemoAPI())})
    util.run_wsgi_app(app)

if __name__ == '__main__':
    main()
