# XML Remote Procedure Call (XML-RPC)

# TỔNG QUAN

## GIỚI THIỆU VỀ XML-RPC

Tài liệu này là hướng dẫn về các xử dụng XML-RPC. Chương trình được viết bằng python và chạy thử bằng UR robot trên URsim

<aside>
❗ Có thể thời điểm bạn làm theo hướng dẫn, phiên bản python và các thư viện đã thay đổi. Vì vậy nếu có thể thì cài các thư viện đúng theo bài hướng dẫn này.

</aside>

### 1. XML-RPC là gì? Ý tưởng cốt lõi

Hãy tưởng tượng bạn có 2 chương trình chạy trên 2 máy tính khác nhau (thậm chí là cùng 1 máy tính nhưng 2 tiếng trình riêng biệt). Một chương trình (Client) muốn thực thi 1 hàm (function) tồn tại trong chương trinhg kia (server) và nhận lại kết quả.

**⇒ XML-RPC (XML Remote Procedure Call) chính là một giao thức giúp thực hiện điều đó.**

- **Remote Procedure Call (RPC):** “Gọi hàm từ xa”. Client có thể gọi một hàm trên server như thể nó là một hàm cục bộ.
- **XML:** Dữ liệu được trao đổi (tên hàm, các tham số, giá trị trả về) được định dạng bằng ngôn ngũ XML.
- **Giao thức truyền tải:** XML-RPC thường sử dụng giao thức HTTP để gửi/nhận các thông điệp XML này.

### 2. Luồng hoạt động cơ bản

**Client**

- Muốn gọi hàm sum(a,b) trên Server.
- Đóng gói yêu cầu này thành 1 thông điệp XML. Nội dung XML sẽ trông giống như: “Tôi muốn gọi hàm tên là ‘sum’ với hai tham số là ‘a ‘ và ‘b’”.
- Gửi thông điệp XML này đến Server thông qua một yêu cầu HTTP POST.

**Server**

- Nhận yêu cầu HTTP POST.
- Phân tích (parse) thông điệp XML để biết Client muốn làm gì (gọi hàm ‘sum’ với biến ‘a’ và ‘b’.
- Tìm và thực thi hàm ‘sum(a,b)’ của chính nó.
- Nhận được kết quả (ví dụ c= a+b).
- Đóng gói kết quả c này thành một thông điệp XML khác.
- Gửi lại thông điệp XML chứa kết quả cho Client thông qua phản hồi HTTP.

**Client**

- Nhận phản hồi từ Server.
- Phân tích thông điệp XML để lấy ra kết quả c.
- Tiếp tục xử lý với kết quả nhận được

### 3. Ưu điểm và nhược điểm

- **Ưu điểm**
    - **Siêu đơn giản:** rất dễ hiểu và triển khai.
    - **Ngôn ngữ chéo:** Vì dự trên XML và HTTP (các tiêu chuẩn mở), một client viết bằng Python có thể dễ dàng gọi một server viết bằng Java,C++,Ruby,… và ngược lại.
    - **Dễ debug:** Vì các thông điểm à XML (văn bản thuần túy), bạn có thể dễ dàng đọc và hiểu chúng để gỡ lỗi.
    - **Vượt qua tường lửa:** Vì xử dụng HTTP (thường là 80) hoặc HTTPS(443), nó có thể dễ dàng đi qua các tường lửa mà không cần cấu hình đặc biệt.
- **Ngược điểm:**
    - **Dài dòng (Verbose):** XML khá dài dòng, ;àm cho các thông điệp lớn hơn các định dạng nhị phân hoặc JSON.
    - **Tốc độ:** Việc phân tích XML có thể làm chậm thời gian hơn so với các định dạng khác như JSON (của REST API) hoặc giao thức nhị phân (gRPC)
    - **Kiểu dữ liệu hạn chế:** XML-RPC chỉ hỗ trợ một tập hợp các kiểu dữ liệu cơ bản (int, float, string, boolean, array, struct/dictionary). Không hỗ trợ các đối tượng phức tạp một cách tự nhiên.

## CÀI ĐẶT

Python đã tích hợp sẵn 2 thư viện xmlrpc.server và xmlrpc.client giúp việc tạo Server và Client trở lên cực kì dễ dàng. 

Ngoài ra có thể tham khảo link sau để biết thêm chi tiết: [https://docs.python.org/3/library/xmlrpc.html](https://docs.python.org/3/library/xmlrpc.html)

### Cài đặt URsim trên docker

LƯU Ý: Hướng dẫn này thực hiện trên Ubuntu 25.04. Với phiên bản window sẽ bổ sung sau.

- Cài đặt docker: [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)
- Pull docker Image của URsim về:

```bash
docker pull universalrobots/ursim_e-series
```

- Chạy URsim:

```bash
docker run --rm -it -p 5900:5900 -p 6080:6080 -p 29999:29999 -p 502:502 -p 2222:2222 -p 30001-30004:30001-30004--cpus=1 --privileged universalrobots/ursim_e-series
```

- Dán link sau vào trình duyệt để truy cập URsim: [http://localhost:6080/vnc.html?host=localhost&port=6080](http://localhost:6080/vnc.html?host=localhost&port=6080) hoặc [http://172.17.0.3:6080/vnc.html?host=172.17.0.3&port=6080](http://172.17.0.3:6080/vnc.html?host=172.17.0.3&port=6080)

## CHƯƠNG TRÌNH MẪU

Sau đây là một số ví dụ về giao thức XML-RPC

### 1. Chạy thử giao thức XML-RPC

Chương trình mẫu:

- Server.py

```python
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Định nghĩa một class để giới hạn các đường dẫn RPC (tùy chọn nhưng an toàn hơn)
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',) # Chỉ chấp nhận yêu cầu đến đường dẫn /RPC2

# Định nghĩa các hàm mà Client có thể gọi 
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
        "server_name": "SimpleExmapleServer"
        "version": "0.0",
        "supported_functions": ["add", "subtract", "get_server_info"]
    }

# --- Thiết lập và chạy Server ---
# Lắng nghe trên localhost (127.0.0.1) tại cổng 8000
HOST = 'localhost'
PORT = 8000

print(f"Đang khởi tạo XML-RPC server tại http://{HOST}:{PORT}")

# Tạo server
with SimpleXMLRPCServer((HOST, PORT), requestHandler=RequestHandler, logRequests=True, allow_none=True) as server:
    # `allow_none=True` cho phép trả về giá trị None
    # `logRequests=True` sẽ in ra thông tin về các yêu cầu HTTP nhận được

    # Đăng ký các hàm để Client có thể gọi chúng
    # server.register_function(tên_hàm_trong_python, 'tên_hàm_mà_client_sẽ_gọi')
    server.register_function(add, 'add')
    server.register_function(subtract, 'subtract')
    server.register_function(get_server_info, 'info') # Client sẽ gọi hàm 'info'

    # Đăng ký các hàm introspection, cho phép client tự khám phá các hàm có sẵn
    server.register_introspection_functions()

    # Chạy server mãi mãi để lắng nghe yêu cầu
    print("Server đã sẵn sàng. Nhấn Ctrl+C để thoát.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã nhận lệnh thoát. Tắt server.")
```

- Client.py

```python
import xmlrpc.client

# Địa chỉ và cổng của server
HOST = 'localhost'
PORT = 8000
SERVER_URL = f"http://{HOST}:{PORT}/RPC2" # Đường dẫn phải khớp với rpc_paths trên server

# Tạo một đối tượng proxy để kết nối đến server
# Proxy này hoạt động như một đối tượng cục bộ, nhưng các cuộc gọi hàm của nó thực chất được gửi đến server.
try:
    with xmlrpc.client.ServerProxy(SERVER_URL, allow_none=True) as proxy:
        print(f"Đã kết nối đến server tại {SERVER_URL}")

        # --- Gọi các hàm từ xa ---

        # 1. Gọi hàm add(5, 3)
        print("\nGọi hàm 'add(5, 3)'...")
        result_add = proxy.add(5, 3)
        print(f"Kết quả từ server: 5 + 3 = {result_add}")
        print(f"Kiểu dữ liệu của kết quả: {type(result_add)}")

        # 2. Gọi hàm subtract(10, 4)
        print("\nGọi hàm 'subtract(10, 4)'...")
        result_subtract = proxy.subtract(10, 4)
        print(f"Kết quả từ server: 10 - 4 = {result_subtract}")

        # 3. Gọi hàm info()
        print("\nGọi hàm 'info()'...")
        server_info = proxy.info()
        print(f"Thông tin từ server: {server_info}")
        print(f"Kiểu dữ liệu của kết quả: {type(server_info)}") # Sẽ là dict

        # 4. Sử dụng introspection để xem các hàm có sẵn
        # (Chỉ hoạt động nếu server.register_introspection_functions() được gọi)
        print("\nSử dụng introspection để liệt kê các hàm trên server:")
        available_methods = proxy.system.listMethods()
        print("Các hàm có sẵn:", available_methods)

        # 5. Thử gọi một hàm không tồn tại để xem lỗi
        try:
            print("\nThử gọi hàm không tồn tại 'multiply(2, 3)'...")
            proxy.multiply(2, 3)
        except xmlrpc.client.Fault as err:
            print("Đã xảy ra lỗi như mong đợi!")
            print(f"  Mã lỗi: {err.faultCode}")
            print(f"  Thông điệp lỗi: {err.faultString}")

except ConnectionRefusedError:
    print(f"\nLỖI: Không thể kết nối đến server tại {SERVER_URL}. Bạn đã chạy server.py chưa?")
except Exception as e:
    print(f"\nĐã xảy ra lỗi không mong muốn: {e}")
```

- Kết quả:

[Test XML-RPC.mp4](XML%20Remote%20Procedure%20Call%20(XML-RPC)%202118b22d5735807784cffd68ff18be54/Test_XML-RPC.mp4)

<aside>
❗

> Lưu ý: ‘SimpleXMLRPCServer’ chỉ chấp nhận đường dẫn đến ‘/RPC2’
> 
</aside>

### 2. Chạy qua URsim ở docker

B1: Chạy URsim ở docker:

```bash
docker run --rm -it -p 5900:5900 -p 6080:6080 -p 29999:29999 -p 502:502 -p 2222:2222 -p 30001-30004:30001-30004 --cpus=1 --privileged universalrobots/ursim_e-series
```

![image.png](XML%20Remote%20Procedure%20Call%20(XML-RPC)%202118b22d5735807784cffd68ff18be54/a6c19af2-b92e-45f1-a777-7d68592b8b74.png)

B2: Viết chương trình trên robot:

- Ở đây chúng ta sẽ làm 1 trình di chuyển ngẫu nhiên vị trí. Các waypoint được gửi ngẫu nhiên từ máy tính
- Logic chương trình:

![Untitled Diagram.drawio.svg](XML%20Remote%20Procedure%20Call%20(XML-RPC)%202118b22d5735807784cffd68ff18be54/Untitled_Diagram.drawio.svg)

- Chương trình trên robot:

![Screenshot From 2025-06-14 14-04-52.png](XML%20Remote%20Procedure%20Call%20(XML-RPC)%202118b22d5735807784cffd68ff18be54/Screenshot_From_2025-06-14_14-04-52.png)

B3: Viết chương trình trên PC

- Thư viện xử dụng: ramdom (theo bài toán) và xmlrpc.server(bắt buộc)

```python
import random
from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer
```

- Tạo 1 class để giới hạn các đường dẫn RPC

```python
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_path = {"/RPC2"}
```

- Khai báo HOST và PORT
    - Với HOST là biến string địa chỉ IP của PC
    - PORT là cổng sẽ mở ra để thực hiện giao tiếp

```python
HOST = "172.17.0.1"
PORT = 49211
print(f"Khởi tạo XML_RPC server tại http://{HOST}:{PORT}")
```

- Tạo hàm get_pose để cho robot gọi hàm và gửi vị trí cho robot

```python
def get_pose():
    X = random.randint(-180, 180)
    Y = random.randint(-500, -200)
    Z = random.randint(0, 300)
    return {"X": X / 1000, "Y": Y / 1000, "Z": Z / 1000}
```

- Khởi tạo sever cho XML-RPC

```python
with SimpleXMLRPCServer(
    (HOST, PORT), requestHandler=RequestHandler, logRequests=True, allow_none=True
) as server:
    server.RequestHandlerClass.protocol_version = "HTTP/1.1"
    server.register_function(get_pose, name="get_pose") # Đăng kí function để cho các client có thể gọi và sử dụng 
    print("server đã sẵn sàng. Nhấn Ctrl+C để thoát.")
    try:
        server.serve_forever() # Giữ cho server hoạt động mãi mãi
    except KeyboardInterrupt:
        print("\nExit")
```

- Code đầy đủ

```python
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

```

Video demo:

[Demo XML-RPC URSim.mp4](XML%20Remote%20Procedure%20Call%20(XML-RPC)%202118b22d5735807784cffd68ff18be54/Demo_XML-RPC_URSim.mp4)

# Lịch sử phiên bản

V0.0: Tạo tài liệu hướng dẫn trên ubuntu 25.04

---

V0.1: Tạo hướng dẫn trên Window

- [ ]  Docker
- [ ]  Demo video