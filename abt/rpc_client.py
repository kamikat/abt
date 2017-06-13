import ssl
import jsonrpclib
import transport

def connect(url="http://localhost:6800/jsonrpc", ca_file=None, no_verify=False):
    if ca_file or no_verify:
        if no_verify:
            ssl_context = ssl._create_unverified_context()
        elif ca_file:
            ssl_context = ssl.create_default_context()
            ssl_context.load_verify_locations(cafile=ca_file)
        transp= transport.SafeTransport(context=ssl_context)
        server = jsonrpclib.Server(url, transport=transp)
    else:
        server = jsonrpclib.Server(url)
    return (server.aria2, server)

