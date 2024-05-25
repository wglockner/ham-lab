import socket
import select

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s

def connect_to_plc(socket, plc_ip, plc_port):
    socket.connect((plc_ip, plc_port))
    print("Connected to PLC")

def send_data(socket, data):
    socket.sendall(data.encode())

def receive_data(socket):
    received_data = ''
    socket.setblocking(0)  # Set the socket to non-blocking mode

    while True:
        ready = select.select([socket], [], [], 1.0)  # Wait for 1 second
        if ready[0]:
            chunk = socket.recv(1024).decode()
            if not chunk:
                break
            received_data += chunk
        else:
            # No data available within 1 second
            break

    socket.setblocking(1)  # Set the socket back to blocking mode
    return received_data

# Usage
plc_ip = '192.168.1.2'  # PLC's static IP address
plc_port = 10000        # Port that the PLC is listening on
s = create_socket()
connect_to_plc(s, plc_ip, plc_port)
send_data(s, "Hello PLC")
print(receive_data(s))
s.close()
