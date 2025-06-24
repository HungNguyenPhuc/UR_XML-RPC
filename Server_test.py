from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer


# Định nghĩa một class để giới hạn các đường dẫn RPC (tùy chọn nhưng an toàn hơn)
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)  # Chỉ chấp nhận yêu cầu đến đường dẫn /RPC2


# --- Đây là nơi bạn định nghĩa các hàm mà Client có thể gọi ---
def add(x, y):
    """Hàm cộng hai số."""
    print(f"Server: Nhận yêu cầu cộng {x} và {y}")
    return x + y


def subtract(x, y):
    """Hàm trừ hai số."""
    print(f"Server: Nhận yêu cầu trừ {x} và {y}")
    return x - y


def get_server_info():
    """Hàm trả về một dictionary (struct trong XML-RPC)."""
    print("Server: Nhận yêu cầu lấy thông tin.")
    return {
        "server_name": "MySimpleServer",
        "version": "1.0",
        "supported_functions": ["add", "subtract", "get_server_info"],
    }


# --- Thiết lập và chạy Server ---
# Lắng nghe trên localhost (127.0.0.1) tại cổng 8000
HOST = "localhost"
PORT = 8000

print(f"Đang khởi tạo XML-RPC server tại http://{HOST}:{PORT}")

# Tạo server
with SimpleXMLRPCServer(
    (HOST, PORT), requestHandler=RequestHandler, logRequests=True, allow_none=True
) as server:
    # `allow_none=True` cho phép trả về giá trị None
    # `logRequests=True` sẽ in ra thông tin về các yêu cầu HTTP nhận được

    # Đăng ký các hàm để Client có thể gọi chúng
    # server.register_function(tên_hàm_trong_python, 'tên_hàm_mà_client_sẽ_gọi')
    server.register_function(add, "add")
    server.register_function(subtract, "subtract")
    server.register_function(get_server_info, "info")  # Client sẽ gọi hàm 'info'

    # (Tùy chọn) Đăng ký các hàm introspection, cho phép client tự khám phá các hàm có sẵn
    server.register_introspection_functions()

    # Chạy server mãi mãi để lắng nghe yêu cầu
    print("Server đã sẵn sàng. Nhấn Ctrl+C để thoát.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã nhận lệnh thoát. Tắt server.")
