=============
JSON-RPC Demo
=============

Let us get a client proxy.

    >>> client = get_proxy('/demo')
    >>> client.echo(1)
    1
    >>> client.echo_args(1, x=2)
    [[1], {'x': 2}]


