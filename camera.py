import cv2
import socket
import pickle
import struct

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)

# Initialize socket connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.79.204', 8000))  # Replace with Laptop B's IP address

while True:
    ret, frame = cap.read()
    
    # Serialize frame to send over network
    data = pickle.dumps(frame)
    
    # Send frame size and frame data over socket
    client_socket.sendall(struct.pack("<L", len(data)) + data)
    
    # Display the frame locally (optional)
    cv2.imshow('Camera Feed', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Cleanup
cap.release()
cv2.destroyAllWindows()
client_socket.close()