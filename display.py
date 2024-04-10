import cv2
import socket
import pickle
import struct

# Initialize socket connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection
connection = server_socket.accept()[0]

data = b''
payload_size = struct.calcsize("<L")

while True:
    # Retrieve frame size and frame data from socket
    while len(data) < payload_size:
        data += connection.recv(4096)
    
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    
    msg_size = struct.unpack("<L", packed_msg_size)[0]
    
    while len(data) < msg_size:
        data += connection.recv(4096)
    
    frame_data = data[:msg_size]
    data = data[msg_size:]
    
    # Deserialize frame data
    frame = pickle.loads(frame_data)
    
    # Display the received frame
    cv2.imshow('Video Stream', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()
connection.close()
server_socket.close()
