from ultralytics import YOLO
import cv2
import numpy as np
import pyrealsense2 as rs
import serial
import time

# arduino_port = 'COM3' # COM9
# baud_rate = 9600
pipe = rs.pipeline()
cfg = rs.config()
cfg.enable_stream(rs.stream.depth , 640 , 480, rs.format.z16 , 30)
cfg.enable_stream(rs.stream.color , 640 , 480, rs.format.bgr8 , 30)
pipe.start(cfg)
# Load YOLOv8 model
model = YOLO("yolov8s.pt")  # Replace with your OBB-trained YOLOv8 model

# Open video capture (replace 'video.mp4' with 0 for webcam)
# video_path = "video.mp4"
# cap = cv2.VideoCapture(0)

# if not cap.isOpened():
    # print("Error: Could not open video.")
    # exit()

# Define a function to draw OBB and center point
def draw_obb(image,x,y,class_id,depth_value):
    # try:
    #     if depth_value   == 0:
    #            try:
    #                 # Initialize serial connection
    #                 arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
    #                 time.sleep(2)  # Wait for Arduino to reset
    #                 command = 'S'
    #                 # print("Connection to Arduino established.")

                    
                        
    #                     # print("F: Move motor forward")
    #                     # print("R: Move motor in reverse")
    #                     # print("S: Stop the motor")
    #                     # print("Q: Quit the program")
    #                     # command = input("Enter your command: ").strip().upper()

    #                     # if command == 'Q':
    #                     #     print("Exiting program.")
    #                     #     break

    #                     # if command not in ['F', 'R', 'S']:
    #                     #     print("Invalid command. Try again.")
    #                     #     continue

    #                 arduino.write(command.encode())  # Send command to Arduino
    #                 time.sleep(0.1)  # Give Arduino time to process
    #                 response = arduino.readline().decode('utf-8').strip()  # Read response
    #                     # print("Arduino response:", response)

    #            except serial.SerialException as e:
    #                 print(f"Error connecting to Arduino: {e}")

    #         #    finally:
    #         #         if 'arduino' in locals() and arduino.is_open:
    #         #             arduino.close()
    #         #             print("Serial connection closed.")
    #     else :
    #         try:
    #                 # Initialize serial connection
    #                 arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
    #                 time.sleep(2)  # Wait for Arduino to reset
    #                 command = 'F'
    #                 # print("Connection to Arduino established.")

                    
                        
    #                     # print("F: Move motor forward")
    #                     # print("R: Move motor in reverse")
    #                     # print("S: Stop the motor")
    #                     # print("Q: Quit the program")
    #                     # command = input("Enter your command: ").strip().upper()

    #                     # if command == 'Q':
    #                     #     print("Exiting program.")
    #                     #     break

    #                     # if command not in ['F', 'R', 'S']:
    #                     #     print("Invalid command. Try again.")
    #                     #     continue

    #                 arduino.write(command.encode())  # Send command to Arduino
    #                 time.sleep(0.1)  # Give Arduino time to process
    #                 response = arduino.readline().decode('utf-8').strip()
    #         except serial.SerialException as e:
    #                 print(f"Error connecting to Arduino: {e}")
    # except :
    #         print("Depth value not calculated")            
    # Convert rotation (radians) to degrees
    # angle = np.degrees(r)

    # # Create a rotated rectangle
    # rect = ((x, y), (w, h), angle)
    # box = cv2.boxPoints(rect)
    # box = np.int0(box)  # Convert to integer coordinates

    # Draw the OBB on the image
    # cv2.drawContours(image, [box], 0, (0, 255, 0), 2)  # Green bounding box
    cv2.putText(image, str(depth_value),(int(center_x) - 50, int(center_y) - 10) , cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1) # need to be placed above the dot of corresponding classes
    # Draw the center point
    cv2.circle(image, (int(x), int(y)), 5, (0, 0, 255), -1)  # Red center point
    
    # Display class label and confidence above the bounding box
    # label = f"{class_name} {confidence:.2f}"
    # text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
    # text_x = int(x - text_size[0] / 2)
    # text_y = int(y - h / 2 - 10)  # Slightly above the bounding box
    # cv2.putText(image, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

# Read class names if available
# class_names = model.names  # YOLOv8 class names

while True:
    frame = pipe.wait_for_frames()
    frames = frame.get_color_frame()
    depth_frame = frame.get_depth_frame()
    # Perform inference
    frames1 = np.asanyarray(frames.get_data())
    # frames2 = np.asanyarray(depth_frame.get_data())
    # cap = cv2.imread(frames1)
    # cvframe = cv2.imread(frames)``
    results = model.predict(frames1)

    # Extract OBB detections (xywhr format)
    detections = results[0].plot()  
    for box in results[0].boxes:
            x_min, y_min, x_max, y_max = map(int, box.xyxy[0])  # Bounding box coordinates
            # confidence = box.conf[0]  # Confidence score
            class_id = int(box.cls[0])
            center_x = int((x_min + x_max) / 2)
            center_y = int((y_min + y_max) / 2)
            try:
                distance = depth_frame.get_distance(center_x, center_y)
            except Exception as e:
                print(f"Error retrieving distance: {e}")
                # distance = 0.0   # doubt whether to make distance zero by default 
            # depth_value = depth_frame.get_distance(center_x,center_y)   
            
            draw_obb(detections, center_x, center_y, class_id , distance)
            
    # xywhr = detections.xywhr.cpu().numpy()  # OBB format: center_x, center_y, width, height, rotation
    # class_ids = results[0].xyxy.cls.cpu().numpy().astype(int)  # Class IDs
    # confidences = detections.conf.cpu().numpy()  # Confidence scores

    # Draw detections on the frame
    # for i, bbox in enumerate(xywhr):
    #     # x, y, w, h, r = bbox  # OBB parameters
    #     class_id = class_ids[i]
    #     confidence = confidences[i]

    #     # Get class name
    #     class_name = class_names[class_id] if class_names else f"Class {class_id}"

    #     # Draw OBB and center point
    #     draw_obb(frames1, x, y, w, h, r, class_id, confidence, class_name)

    # Display the frame
    cv2.imshow("Video Detection", frames1)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# # Release resources
# cap.release()
# cv2.destroyAllWindows()
####### transmitting to arduino 
# import serial
# import time

# arduino_port = 'COM3' # COM9
# baud_rate = 9600

# try:
#     # Initialize serial connection
#     arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
#     time.sleep(2)  # Wait for Arduino to reset

#     print("Connection to Arduino established.")

#     while True:
        
#         print("F: Move motor forward")
#         print("R: Move motor in reverse")
#         print("S: Stop the motor")
#         print("Q: Quit the program")
#         command = input("Enter your command: ").strip().upper()

#         if command == 'Q':
#             print("Exiting program.")
#             break

#         if command not in ['F', 'R', 'S']:
#             print("Invalid command. Try again.")
#             continue

#         arduino.write(command.encode())  # Send command to Arduino
#         time.sleep(0.1)  # Give Arduino time to process
#         response = arduino.readline().decode('utf-8').strip()  # Read response
#         print("Arduino response:", response)

# except serial.SerialException as e:
#     print(f"Error connecting to Arduino: {e}")

# finally:
#     if 'arduino' in locals() and arduino.is_open:
#         arduino.close()
#         print("Serial connection closed.")
