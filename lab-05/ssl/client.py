import socket
import threading
import ssl

# --- PHẦN 1 & 3: THIẾT LẬP BAN ĐẦU VÀ HÀM NHẬN DỮ LIỆU ---

# Thông tin server
server_address = ('localhost', 12345)

# Hàm này sẽ chạy trên một luồng riêng để lắng nghe dữ liệu từ server
def receive_data(ssl_sock):
    """
    Liên tục nhận dữ liệu từ server và in ra màn hình.
    """
    try:
        while True:
            # Nhận dữ liệu (tối đa 1024 bytes)
            data = ssl_sock.recv(1024)
            if not data:
                # Nếu không có dữ liệu, có nghĩa là server đã đóng kết nối
                print("\nServer đã đóng kết nối.")
                break
            # In dữ liệu đã được giải mã
            print(f"NHẬN: {data.decode('utf-8')}")
    except Exception as e:
        # Xử lý các lỗi có thể xảy ra khi nhận dữ liệu
        print(f"\nLỗi khi nhận dữ liệu: {e}")
    finally:
        # Đóng socket khi kết thúc
        print("Đóng luồng nhận.")
        ssl_sock.close()

# --- PHẦN 2 & 3: TẠO SOCKET, KẾT NỐI VÀ KHỞI ĐỘNG LUỒNG ---

# Tạo socket client chuẩn
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tạo SSL context để cấu hình các tùy chọn SSL/TLS
# ssl.PROTOCOL_TLS_CLIENT yêu cầu phiên bản TLS 1.2 trở lên, an toàn hơn
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE  # Tắt xác minh chứng chỉ (chỉ dùng cho mục đích thử nghiệm)

# Bọc socket thông thường bằng SSL context để tạo kết nối an toàn
# server_hostname là cần thiết cho Server Name Indication (SNI)
ssl_socket = context.wrap_socket(client_socket, server_hostname=server_address[0])

try:
    # Kết nối đến server
    print(f"Đang kết nối đến {server_address[0]}:{server_address[1]}...")
    ssl_socket.connect(server_address)
    print("Kết nối thành công!")

    # Bắt đầu một luồng để chạy hàm receive_data
    # Điều này cho phép client vừa gửi vừa nhận dữ liệu đồng thời
    receive_thread = threading.Thread(target=receive_data, args=(ssl_socket,))
    receive_thread.daemon = True  # Luồng sẽ tự động tắt khi chương trình chính kết thúc
    receive_thread.start()

    # --- PHẦN 4: GỬI DỮ LIỆU LÊN SERVER (LUỒNG CHÍNH) ---
    print("Nhập tin nhắn để gửi. Nhấn Ctrl+C để thoát.")
    while True:
        message = input()
        if message:
            # Gửi tin nhắn đã được mã hóa utf-8
            ssl_socket.send(message.encode('utf-8'))

except KeyboardInterrupt:
    # Người dùng nhấn Ctrl+C để thoát chương trình
    print("\nBạn đã yêu cầu thoát. Đang đóng kết nối...")
except ConnectionRefusedError:
    print("Kết nối bị từ chối. Hãy chắc chắn rằng server đang chạy.")
except Exception as e:
    # Bắt các lỗi kết nối khác
    print(f"Đã xảy ra lỗi: {e}")
finally:
    # Đảm bảo socket luôn được đóng khi chương trình kết thúc
    ssl_socket.close()
    print("Đã đóng kết nối chính.")