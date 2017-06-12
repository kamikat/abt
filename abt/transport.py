from xmlrpclib import SafeTransport as XMLSafeTransport
from jsonrpclib.jsonrpc import TransportMixIn

class SafeTransport(TransportMixIn, XMLSafeTransport):
    def __init__(self, context=None):
        TransportMixIn.__init__(self)
        XMLSafeTransport.__init__(self, context)

