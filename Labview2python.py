#to labview comm for ornament detection UI 
import socket
import cv2
import base64

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Set up a TCP server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 65432)
server_socket.bind(server_address)
server_socket.listen(1)
print("Waiting for LabVIEW to connect...")

conn, addr = server_socket.accept()
print(f"Connected to LabVIEW at {addr}")

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.png', frame)
        array_flattened_string = " ".join(map(str, buffer.flatten()))
        # frame_data = base64.b64encode(buffer).decode('utf-8')
        # print("encoded data : \n",(frame_data + "\n").encode('utf-8'))
        # Send frame data to LabVIEW
        # conn.sendall((frame_data + "\n").encode('utf-8'))
        print("array",array_flattened_string)
        conn.sendall(array_flattened_string.encode('utf-8'))
        # Display the video locally for verification (optional)
        cv2.imshow('Python Video Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    conn.close()
    server_socket.close()
    cv2.destroyAllWindows()
