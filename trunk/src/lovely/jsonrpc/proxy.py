##############################################################################
#
# Copyright 2008 Lovely Systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
##############################################################################

from urlparse import urlparse
from lovely.jsonrpc import dispatcher
import Cookie
import base64

class RemoteException(Exception):
    """An error occured on the server side"""

class HTTPException(Exception):
    """A http exception occured"""

class JSONDeserializeException(Exception):
    """A json deserialization error occured"""

class Session(object):

    _auth = None

    def __init__(self, username=None, password=None):
        self.cookies = Cookie.SmartCookie()
        if username and password:
            self._auth = {"AUTHORIZATION": "Basic %s" %
                          base64.encodestring("%s:%s" % ('Vorschau', 'Iswwdnsudi10')
                                              ).strip()}

    def save_headers(self, headers):
        if self._auth:
            headers.update(self._auth)
        headers['Cookie'] = self.cookies.output(header="")
        return headers

    def load_headers(self, headers):
        ch = headers.get('set-cookie')
        if ch:
            self.cookies.load(ch)

class JSONRPCTransport(object):

    """the default httplib transport implementation"""

    headers = {'User-Agent':'lovey.jsonpc.proxy (httplib)',
               'Content-Type':'application/json',
               'Accept':'application/json'}

    def __init__(self, uri, session=None, headers={}):
        import httplib
        self.session = session
        self.url = urlparse(uri)
        self.headers = self.headers.copy()
        self.headers.update(headers)
        if self.url.scheme == 'http':
            conn_impl = httplib.HTTPConnection
        elif self.url.scheme == 'https':
            conn_impl = httplib.HTTPSConnection
        else:
            raise Exception, 'Unsupported scheme %r' % self.url.scheme
        if self.url.port:
            loc = ':'.join((self.url.hostname,
                            str(self.url.port)))
        else:
            loc = self.url.hostname
        self.conn = conn_impl(loc)

    def request(self, request_body):
        if self.session:
            headers = self.session.save_headers(self.headers.copy())
        else:
            headers = self.headers
        self.conn.request('POST', self.url.path,
                          body=request_body, headers=headers)
        resp = self.conn.getresponse()
        if self.session:
            self.session.load_headers(dict(resp.getheaders()))

        return resp.status, resp.read()

class ServerProxy(object):

    def __init__(self, uri, transport_impl=JSONRPCTransport,
                 json_impl=None, **kwargs):
        """Initialization"""
        self._transport = transport_impl(uri, **kwargs)
        if json_impl is None:
            import simplejson
            self._json_impl = simplejson
        else:
            self._json_impl = json_impl

    def _request(self, payload):
        status, body = self._transport.request(payload)
        if status > 299:
            raise HTTPException, '%s\n%r' % (status, body)
        try:
            res = self._json_impl.loads(body)
        except ValueError:
            raise JSONDeserializeException, "Cannot deserialize json: %r" % body
        if res.get('error'):
            raise RemoteException, res.get('error')
        return res.get('result')

    def __repr__(self):
        return (
            "<ServerProxy for %s%s>" %
            (self.__host, self.__handler)
            )

    __str__ = __repr__

    def __getattr__(self, name):
        return dispatcher._Method(self._request, name, self._json_impl)

