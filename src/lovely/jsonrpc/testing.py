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

from lovely.jsonrpc import wsgi
import threading
from wsgiref.simple_server import make_server

class TestingAPI(object):

    def echo(self, *args, **kwargs):
        return args, kwargs

def get_server(port=12345):
    api = TestingAPI()
    app = wsgi.WSGIJSONRPCApplication(api)
    return  make_server('localhost', 12345, app)

class OneRequest(threading.Thread):

    def __init__(self, server):
        super(OneRequest, self).__init__()
        self.server = server

    def run(self):
        self.server.handle_request()

def one_request(server):
    OneRequest(server).start()
