import cv2
import numpy as np
import pyrealsense2 as rs
import serial
import time
from ultralytics import YOLO
from threading import Thread

# Arduino 
arduino_port = 'COM3' # or com9 windows
baud_rate = 9600
arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)  

# RealSense config
pipe = rs.pipeline()
cfg = rs.config()
cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipe.start(cfg)


model = YOLO("yolov8s-seg.pt")  # Replace with your model
current_command = None 
previous_depth_value = None

def send_command(command):
    global current_command
    if command != current_command:  
        arduino.write(command.encode())
        current_command = command
        print(f"Command sent: {command}")


def draw_obb(image, x, y, class_id, depth_value):
    global previous_depth_value
    depth_threshold = 0.05 
    if depth_value == 0:
        send_command('S')  
    else:
        if previous_depth_value is None or abs(depth_value - previous_depth_value) > depth_threshold:
            send_command('F')  # Move motor forward
            previous_depth_value = depth_value
        # send_command('F')  # Move motor forward

    
    cv2.putText(image, f"Depth: {depth_value:.2f}m", (x - 50, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    cv2.circle(image, (x, y), 5, (0, 0, 255), -1)
def process_mask(image, mask, depth_frame):
    # Find contours
    mask = (mask > 0.5).astype(np.uint8)  # Binary mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Ignore small areas
            # Calculate the center of the contour
            M = cv2.moments(contour)
            if M["m00"] != 0:
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])
            else:
                center_x, center_y = 0, 0
            
            # Get depth value
            try:
                depth_value = depth_frame.get_distance(center_x, center_y)
            except Exception as e:
                print(f"Error retrieving depth: {e}")
                depth_value = 0.0

            # Draw the center and depth
            # draw_obb(image, center_x, center_y, depth_value)
    global previous_depth_value
    depth_threshold = 0.05 
    if depth_value == 0:
            send_command('S')  
    else:
            if previous_depth_value is None or abs(depth_value - previous_depth_value) > depth_threshold:
                send_command('F')  # Move motor forward
                previous_depth_value = depth_value
        # send_command('F')  # Move motor forward

    
    cv2.putText(image, f"Depth: {depth_value:.2f}m", (x - 50, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    cv2.circle(image, (x, y), 5, (0, 0, 255), -1)

def process_frames():
    while True:
       
        frames = pipe.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        
        if not color_frame or not depth_frame:
            continue
        
        
        color_image = np.asanyarray(color_frame.get_data())
        
       
        results = model.predict(color_image, conf=0.3)
        
        
        detections = results[0].plot()
        try:
            for mask in results[0].masks:
                process_mask(detections, mask, depth_frame)
        except:
            # send_command('F')
            print("No maskes detected")
        # for box in results[0].boxes:
        #     x_min, y_min, x_max, y_max = map(int, box.xyxy[0])  # Bounding box coordinates
        #     center_x = (x_min + x_max) // 2
        #     center_y = (y_min + y_max) // 2
        #     class_id = int(box.cls[0])
            
            
        #     try:
        #         depth_value = depth_frame.get_distance(center_x, center_y)
        #     except Exception as e:
        #         print(f"Error retrieving depth: {e}")
        #         # depth_value = 0.0
            
            
        #     draw_obb(detections, center_x, center_y, class_id, depth_value)
        
        # Display 
        cv2.imshow("Video Detection", detections)
        
       
        if cv2.waitKey(1) & 0xFF == ord('q'):
            send_command('S')
            break

# Run the frame processing in a separate thread
frame_thread = Thread(target=process_frames)
frame_thread.start()
frame_thread.join()

# Release resources
arduino.close()
pipe.stop()
cv2.destroyAllWindows()
