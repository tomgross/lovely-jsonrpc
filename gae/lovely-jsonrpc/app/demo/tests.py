##############################################################################
#
# Copyright 2009 Lovely Systems GmbH
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

import unittest, doctest
from zope.testing.doctestunit import DocFileSuite, DocTestSuite
from lovely.jsonrpc.testing import TestJSONRPCProxy
from lovely.jsonrpc.proxy import ServerProxy

def get_test_proxy(ep):
    from webtest import TestApp
    from lovely.jsonrpc import wsgi
    from lovely.jsonrpc import dispatcher
    import demo
    app = wsgi.WSGIJSONRPCApplication(
    {'demo':
     dispatcher.JSONRPCDispatcher(demo.DemoAPI())})
    app = TestApp(app)
    proxy = TestJSONRPCProxy('/demo', app)
    return proxy

def get_gae_proxy(ep):
    url = 'http://lovely-jsonrpc.appspot.com/' + ep
    return ServerProxy(url)

def setUpLocal(test):
    test.globs['get_proxy'] = get_test_proxy

def setUpGAE(test):
    test.globs['get_proxy'] = get_gae_proxy

def test_suite():
    readme_local = DocFileSuite(
        'README.txt', setUp=setUpLocal,
        optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
        )
    readme_gae = DocFileSuite(
        'README.txt', setUp=setUpGAE,
        optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
        )
    readme_gae.level=2
    s = unittest.TestSuite((
        readme_local,
        readme_gae
        ))
    return s
