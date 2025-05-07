import socket
import threading
import time

# Gửi kết nối giả đến server Minecraft
def connect_to_minecraft_server(ip, port, thread_id, stop_event):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)  # Đặt timeout để tránh treo
            s.connect((ip, port))

            # Fake handshake theo định dạng đơn giản của Minecraft
            # Không phải handshake thực sự, nhưng server có thể phản hồi
            fake_handshake = b"\x00" * 10  # Dữ liệu giả, bạn có thể tùy chỉnh
            s.sendall(fake_handshake)

            print(f"✅ Luồng {thread_id} đã kết nối tới {ip}:{port}")
            time.sleep(0.5)  # Dừng một chút rồi đóng
    except Exception as e:
        print(f"❌ Luồng {thread_id} lỗi: {e}")

# Dừng chương trình sau một khoảng thời gian
def stop_after_timeout(seconds, stop_event):
    time.sleep(seconds)
    stop_event.set()
    print(f"⏰ Dừng tất cả luồng sau {seconds} giây!")

# ======= THIẾT LẬP =======
server = input("Nhập IP và port server Minecraft (ví dụ: play.example.com:25565): ")
ip, port = server.strip().split(":")
port = int(port)

thread_count = int(input("Nhập số lượng luồng kết nối: "))
timeout = int(input("Chạy trong bao nhiêu giây: "))

# Sự kiện dừng toàn bộ
stop_event = threading.Event()

threads = []

# Tạo và khởi chạy các luồng
for i in range(thread_count):
    t = threading.Thread(
        target=connect_to_minecraft_server,
        args=(ip, port, i, stop_event),
        name=f"Thread-{i}"
    )
    threads.append(t)
    t.start()
    time.sleep(0.05)  # Giãn cách nhẹ để tránh nghẽn socket

# Luồng dừng
stopper = threading.Thread(target=stop_after_timeout, args=(timeout, stop_event))
stopper.start()

# Chờ tất cả luồng hoàn tất
for t in threads:
    t.join()

print("✅ Tất cả luồng đã hoàn thành.")
