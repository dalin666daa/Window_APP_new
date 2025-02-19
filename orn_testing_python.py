from ultralytics import YOLO
import cv2
from tinydb import TinyDB
# from collections import Counter
import torch
# db = TinyDB(r"D:\Window_APP_4\Window_APP\tinydb1.json")
# model = YOLO(r"D:\ornament_weights.pt")
model = YOLO("yolov8n-obb.pt")
cap = cv2.VideoCapture(0)
zoom_factor = 1.0
min_zoom = 1.0
max_zoom = 4.0
zoom_step = 0.1
i=40
# Callback function to handle mouse events
def handle_mouse(event, x, y, flags, param):
    global zoom_factor

    if event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:  # Scroll up to zoom in
            zoom_factor = min(zoom_factor + zoom_step, max_zoom)
        else:  # Scroll down to zoom out
            zoom_factor = max(zoom_factor - zoom_step, min_zoom)

while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
        h, w, _ = frame.shape
        zoom_factor = 2.4
    # Calculate the crop area based on the zoom factor
        center_x, center_y = w // 2, h // 2
        new_w = int(w / zoom_factor)
        new_h = int(h / zoom_factor)
        start_x = max(center_x - new_w // 2, 0)
        start_y = max(center_y - new_h // 2, 0)
        end_x = min(center_x + new_w // 2, w)
        end_y = min(center_y + new_h // 2, h)

        # Crop and resize the frame
        # cropped_frame = frame[start_y:end_y, start_x:end_x]
        # zoomed_frame = cv2.resize(cropped_frame, (w, h), interpolation=cv2.INTER_LINEAR)
        results=model.predict(frame,conf = 0.65)
        db = TinyDB(r"D:\Window_APP_4\Window_APP\tinydb1.json")
        new_frame = results[0].plot()
        class_counts = [torch.sum(results[0].obb.cls == 0).item()]
        class_counts1 = [torch.sum(results[0].obb.cls == 1).item()]
        class_counts2 = [torch.sum(results[0].obb.cls == 2).item()]
        table = db.table('Counter :')
        db_count=table.get(cond=None,doc_id=table._get_next_id() - 1)
        earing_counts = [int(value) for key, value in db_count.items() if key.startswith('earing1_cnt')]
        earing_counts1 = [int(value) for key, value in db_count.items() if key.startswith('earing2_cnt')]
        earing_counts2 = [int(value) for key, value in db_count.items() if key.startswith('earing3_cnt')]
        
        print(earing_counts)
        # print("class count",class_counts)
        # print("db_count val :",earing_counts)
        var= [(f"{int(''.join(map(str,earing_counts))) - int(''.join(map(str,class_counts)))} earring1 missing","")[earing_counts == class_counts],(f"{int(''.join(map(str,earing_counts1))) - int(''.join(map(str,class_counts1)))} earring2 missing","")[earing_counts1 == class_counts1],(f"{int(''.join(map(str,earing_counts2))) - int(''.join(map(str,class_counts2)))} earring3 missing","")[earing_counts2 == class_counts2]]
        # new_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
        new_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2HSV)
        # img = cv.medianBlur(img,5)
 
        # ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
        # th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
        #             cv.THRESH_BINARY,11,2)
        # th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
        #             cv.THRESH_BINARY,11,2)
        # _,new_frame = cv2.threshold(new_frame,127,255,cv2.THRESH_BINARY)
        # new_frame= cv2.adaptiveThreshold(new_frame,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
        #             cv2.THRESH_BINARY,11,2)

        # thresholding added here
        # new_frame= cv2.adaptiveThreshold(new_frame,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        #             cv2.THRESH_BINARY,11,2)                    
        print("Detection Status :",var)
        cv2.imshow('ornament det',new_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('i'):
            print("ok \n")
            cv2.imwrite(f'Vertex{i}.jpg',new_frame)
            i=i+1
    # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything is done, release the capture and close the window
cap.release()
cv2.destroyAllWindows()