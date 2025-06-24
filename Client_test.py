import xmlrpc.client
from time import sleep

# Địa chỉ và cổng của server
HOST = "localhost"
PORT = 8000
SERVER_URL = (
    f"http://{HOST}:{PORT}/RPC2"  # Đường dẫn phải khớp với rpc_paths trên server
)

# Tạo một đối tượng proxy để kết nối đến server
# Proxy này hoạt động như một đối tượng cục bộ, nhưng các cuộc gọi hàm của nó
# thực chất được gửi đến server.
try:
    with xmlrpc.client.ServerProxy(SERVER_URL, allow_none=True) as proxy:
        print(f"Đã kết nối đến server tại {SERVER_URL}")
        sleep(1)
        # --- Gọi các hàm từ xa ---

        # 1. Gọi hàm add(5, 3)
        print("\nGọi hàm 'add(5, 3)'...")
        result_add = proxy.add(5, 3)
        print(f"Kết quả từ server: 5 + 3 = {result_add}")
        sleep(1)
        print(f"Kiểu dữ liệu của kết quả: {type(result_add)}")
        sleep(1)
        # 2. Gọi hàm subtract(10, 4)
        print("\nGọi hàm 'subtract(10, 4)'...")
        result_subtract = proxy.subtract(10, 4)
        print(f"Kết quả từ server: 10 - 4 = {result_subtract}")
        sleep(1)
        # 3. Gọi hàm info()
        print("\nGọi hàm 'info()'...")
        server_info = proxy.info()
        print(f"Thông tin từ server: {server_info}")
        sleep(1)
        print(f"Kiểu dữ liệu của kết quả: {type(server_info)}")  # Sẽ là dict
        sleep(1)
        # 4. Sử dụng introspection để xem các hàm có sẵn
        # (Chỉ hoạt động nếu server.register_introspection_functions() được gọi)
        print("\nSử dụng introspection để liệt kê các hàm trên server:")
        available_methods = proxy.system.listMethods()
        sleep(1)
        print("Các hàm có sẵn:", available_methods)
        sleep(1)

        # 5. Thử gọi một hàm không tồn tại để xem lỗi
        try:
            print("\nThử gọi hàm không tồn tại 'multiply(2, 3)'...")
            proxy.multiply(2, 3)
        except xmlrpc.client.Fault as err:
            print("Đã xảy ra lỗi như mong đợi!")
            print(f"  Mã lỗi: {err.faultCode}")
            print(f"  Thông điệp lỗi: {err.faultString}")


except ConnectionRefusedError:
    print(
        f"\nLỖI: Không thể kết nối đến server tại {SERVER_URL}. Bạn đã chạy server.py chưa?"
    )
except Exception as e:
    print(f"\nĐã xảy ra lỗi không mong muốn: {e}")
