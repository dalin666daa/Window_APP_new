# from ultralytics import YOLO
# import cv2 
# import pyrealsense2 as rs
# # from tinydb import TinyDB
# # from collections import Counter

# # import torch
# # db = TinyDB(r"D:\Window_APP_4\Window_APP\tinydb1.json")
# # model = YOLO(r"D:\ornament_weights.pt")
# # cap = cv2.VideoCapture(1)
# pipe=rs.pipeline()
# cfg = rs.config
# pipe.start(cfg)
# while cap.isOpened():
#         pipe.wait_for_frames()
#         depth_frame = pipe.
#         ret, frame = cap.read()
#         if not ret:
#             print("Error: Failed to capture frame.")
#             break
#         # results=model.predict(frame,conf = 0.65)
#         # db = TinyDB(r"D:\Window_APP_4\Window_APP\tinydb1.json")
#         # new_frame = results[0].plot()
#         # class_counts = [torch.sum(results[0].obb.cls == 0).item()]
#         # class_counts1 = [torch.sum(results[0].obb.cls == 1).item()]
#         # class_counts2 = [torch.sum(results[0].obb.cls == 2).item()]
#         # table = db.table('Counter :')
#         # db_count=table.get(cond=None,doc_id=table._get_next_id() - 1)
#         # earing_counts = [int(value) for key, value in db_count.items() if key.startswith('earing1_cnt')]
#         # earing_counts1 = [int(value) for key, value in db_count.items() if key.startswith('earing2_cnt')]
#         # earing_counts2 = [int(value) for key, value in db_count.items() if key.startswith('earing3_cnt')]
        
#         # print(earing_counts)
#         # print("class count",class_counts)
#         # print("db_count val :",earing_counts)
#         # var= [(f"{int(''.join(map(str,earing_counts))) - int(''.join(map(str,class_counts)))} earring1 missing","")[earing_counts == class_counts],(f"{int(''.join(map(str,earing_counts1))) - int(''.join(map(str,class_counts1)))} earring2 missing","")[earing_counts1 == class_counts1],(f"{int(''.join(map(str,earing_counts2))) - int(''.join(map(str,class_counts2)))} earring3 missing","")[earing_counts2 == class_counts2]]

#         # print("Detection Status :",var)
#         cv2.imshow('ornament det',frame)
        
#         # if cv2.waitKey(1) & 0xFF == ord('i'):
#         #     print("ok \n")
#         #     cv2.imwrite(f'ornament_images{i}.jpg',frame_zoomed)
#         #     i=i+1
#     # Break the loop on 'q' key press
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

# # When everything is done, release the capture and close the window
# cap.release()
# cv2.destroyAllWindows()
import Jetson.GPIO as GPIO 
GPIO.setmode(GPIO.BOARD) # mode = GPIO
channel = 29 # gpio pins 
channel2 = 31
channel3 = 33
# changing pin mode
GPIO.setup(channel, GPIO.OUT)
GPIO.setup(channel2, GPIO.OUT)
GPIO.setup(channel3, GPIO.OUT)


