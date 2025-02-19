# New UI using call library and open cv dll 
import cv2 

cap = cv2.VideoCapture(0)
import cv2
import numpy as np

def send_frame_to_labview(frame):
    _, encoded_frame = cv2.imencode('.bmp', frame) 
    print("TYPE:",(encoded_frame.size))  
    array_flattened_string = " ".join(map(str, encoded_frame.flatten()))
    # print(f"{array_flattened_string}")
    return array_flattened_string

while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
        send_frame_to_labview(frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()