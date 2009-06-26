=============
JSON-RPC Demo
=============

We create a testing app.

    >>> from webtest import TestApp
    >>> from lovely.jsonrpc import wsgi
    >>> from lovely.jsonrpc import dispatcher
    >>> import demo

    >>> app = wsgi.WSGIJSONRPCApplication(
    ...     {'demo':
    ...      dispatcher.JSONRPCDispatcher(demo.DemoAPI())})
    >>> app = TestApp(app)

Let us create a client proxy.

    >>> from lovely.jsonrpc.testing import TestJSONRPCProxy
    >>> client = TestJSONRPCProxy('/demo', app)

    >>> client.echo(1)
    1
    >>> client.echo_args(1, x=2)
    [[1], {'x': 2}]


