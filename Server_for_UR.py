import random
from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_path = {"/RPC2"}


HOST = "172.17.0.1"
PORT = 49211
print(f"Khởi tạo XML_RPC server tại http://{HOST}:{PORT}")


def get_pose():
    X = random.randint(-180, 180)
    Y = random.randint(-500, -200)
    Z = random.randint(0, 300)
    return {"X": X / 1000, "Y": Y / 1000, "Z": Z / 1000}


with SimpleXMLRPCServer(
    (HOST, PORT), requestHandler=RequestHandler, logRequests=True, allow_none=True
) as server:
    server.RequestHandlerClass.protocol_version = "HTTP/1.1"
    server.register_function(get_pose, name="get_pose")
    print("server đã sẵn sàng. Nhấn Ctrl+C để thoát.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nExit")
