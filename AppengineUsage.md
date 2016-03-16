How to use lovely.jsonrpc with appengine

# Introduction #

Here is how you can use JSON-RPC with Googel appengine.

# Details #

Here is the code for an echo server (echo.py) :

```
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson

from lovely.jsonrpc import dispatcher
from lovely.jsonrpc.wsgi import WSGIJSONRPCApplication

class EchoService(object):

    def echo(self, value):
        return value

echoService = dispatcher.JSONRPCDispatcher(
                            EchoService(),
                            json_impl=simplejson,
                            )

application = WSGIJSONRPCApplication({'_jsonrpc/myservice':echoService})

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
```

And in the app.yaml :

```
- url: /_jsonrpc/.*
  script: echo.py
```