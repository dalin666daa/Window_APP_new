import cv2
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
from ultralytics import YOLO
from paddleocr import PaddleOCR
# import add_test
# from add_test import AddTestDialogmeters_latest
from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QMessageBox
import re
from datetime import datetime
import time
# from master import MasterPage
# from running_test_page import RunningTestPage
# from add_test import store_values
# from add_test import get_inputs
class CameraThread(QThread):
    new_frame = pyqtSignal(np.ndarray)
    camera_error = pyqtSignal(str)
    value_updated = pyqtSignal(float, str)
    # from running_test_page import RunningTestPage
    def __init__(self,test):
        super().__init__()
        self.add_test = AddTestDialog()
        # self.running_test_page = running_test_page
        # self.add_test.values_from_add_test.connect(self.get_add_test_values)
        self.value_status = ""
        self.extracted_values = []
        self.stable_value = None
        self.display_start_time = None
        self.display_duration = 3
        self._run_flag = True
        self.test_info = {}
        self.model = YOLO(r"C:\Users\a\yolo13\ultralytics1\ultralytics\best_03_09_24.pt")
        self.ocr = PaddleOCR(use_angle_cls=False, lang='en',show_log=False)
        
    #     try:
    # # Retrieve and validate inputs
    #         value_text = self.add_test.value_input.text().strip()
    #         tolerance_text = self.add_test.tolerance_input.text().strip()

    #         if not value_text or not tolerance_text:
    #              raise ValueError("Empty input")

    # # Convert the inputs to float
    #         value = float(value_text)
    #         tolerance = float(tolerance_text)

    # # Calculate the lower and upper bounds
    #         self.lower_bound = value - (tolerance / 100) * value
    #         self.upper_bound = value + (tolerance / 100) * value
    #     except ValueError:
    #             print("Input Error", "Please enter valid numeric values.")
        # self.lower_bound = float(self.add_test.value_input.text()) - (float(self.add_test.tolerance_input.text()) / 100) * float(self.add_test.value_input.text())
        # self.upper_bound = float(self.add_test.value_input.text()) + (float(self.add_test.tolerance_input.text()) / 100) * float(self.add_test.value_input.text())
        # magnitude = 0.0
        # tolerance = 0.0
        # self.add_test.value_input = 0.0
        self.lower_bound = 0.0
        self.upper_bound = 0.0
        self.stable_v= 0.0
        self.status_label = ""
        # self.value_text = 0.0
        self.value_text = float(test.get('value','N/A'))

        self.tolerance_text =float(test.get('tolerance','N/A'))
        self.unit_text = test.get(test.get('unit','N/A'))
        self.lower_bound = self.value_text - (self.tolerance_text / 100) * self.value_text
        self.upper_bound = self.value_text + (self.tolerance_text / 100) * self.value_text
    # def get_add_test_values(self,value,tolerance,unit):
    #         self.value_text = value
    #         self.tolerance_text = tolerance
    #         self.unit_text = unit
    #         self.lower_bound = float(value - (tolerance / 100) * value)
    #         self.upper_bound = float(value + (tolerance / 100) * value)
    #         print("add test values :: {self.value_text},{self.tolerance_text},{self.unit_text}")
    def detect_display_screen(self, results, frame):
        if results[0].obb.xyxy.shape[0] > 0:
            x1, y1, x2, y2 = map(int, results[0].obb.xyxy[0])
            height, width, _ = frame.shape
            x1 = max(0, min(x1, width))
            y1 = max(0, min(y1, height))
            x2 = max(0, min(x2, width))
            y2 = max(0, min(y2, height))
            roi = (x1, y1, x2, y2)
        else:
            roi = (100, 100, 400, 200)
        return roi
    def extract_text_from_roi(self, frame, roi):
        x1, y1, x2, y2 = roi
        cropped_image = frame[y1:y2, x1:x2]
        gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

        ocr_result = self.ocr.ocr(gray_image)

        extracted_text_lines = []
        if ocr_result and ocr_result[0]:
            for line in ocr_result:
                for word in line:
                    text, confidence = word[1]
                    extracted_text_lines.append(text)

        extracted_text = ' '.join(extracted_text_lines)
        return extracted_text

    def run(self):
        self.capture = cv2.VideoCapture(0)
        # self.value_text= float(test.get('value', 'N/A'))
        print(f"from running page to camera thread value pass {self.value_text} , {self.tolerance_text},{self.unit_text}")
        # print(f'list of values from running test = {self.running_test_page.value},{self.running_test_page.tolerance}')
        # if self.get_add_test_values():
        #     print("values received from signal")
        # if not self.capture.isOpened():
        #     self.camera_error.emit("Error: Could not open camera.")
        #     return
        # if self.add_test.exec_() == QDialog.Accepted:
        #     test_info = self.add_test.get_inputs()
        #     print(test_info)
        # else:
        #     print("didnt went past add test")
        # frame_counter = 0
        while self.capture.isOpened() and self._run_flag:
            ret, frame = self.capture.read()
            
            try:
    # Retrieve and validate inputs

            #  value_text = self.add_test.get_inputs().values()   
            #  print(value_text)
            #  tolerance_text = self.add_test.get_input().values()

            #  value_text = self.add_test.value_input.text().strip() #   input value = preset value
            #  tolerance_text = self.add_test.tolerance_input.text().strip() # tolerance value 
            #  print()
             if not self.value_text or not self.tolerance_text:
                 raise ValueError("Empty input")

    # Convert the inputs to float
             value_new = float(self.value_text)
             tolerance_new = float(self.tolerance_text)

    # Calculate the lower and upper bounds
             
            except ValueError:
                print("Input Error", "Please enter valid numeric values.")
            if ret:
                print("frame entered ")
                result=self.model.predict(frame,conf=0.65)
                if len(result[0].obb.xyxy.tolist()) == 1:
                      roi = self.detect_display_screen(result, frame)
                      cv2.rectangle(frame, (roi[0], roi[1]), (roi[2], roi[3]), (0, 255, 0), 2)
                      extracted_text = self.extract_text_from_roi(frame, roi)
                      cv2.putText(frame, f'OCR Text: {extracted_text}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                      numerical_values = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*", extracted_text)
            
                      if numerical_values and len(numerical_values) != 0:
                         try:
                            strg = numerical_values[0].replace(' ', '')
                            value = float(strg)
                         except IndexError:
                            value = 0.0
                         self.extracted_values.append(value)

                      if len(self.extracted_values) >= 10:
                            last_values = self.extracted_values[-10:]
                            if all(v == last_values[0] and v != 0.0 for v in last_values):
                                    self.stable_value = last_values[0]
                                    self.display_start_time = time.time()
                                    self.extracted_values.clear()
                                    # print("unit values after:",self.add_test.unit_input.text())
                                    # print("unit values before:",self.add_test.unit_input)

                            # if self.unit_text == 'k' or self.unit_text == 'K':
                            if True:
                            #    lower_bound = lower_bound * 1000 
                            #    upper_bound = upper_bound * 1000
                               try:
                                # self.stable_value= self.stable_value 
                                if self.lower_bound <= self.stable_value <= self.upper_bound:
                                # if lower_bound <= self.stable_value <= upper_bound:
                                
                                        self.value_status = "OK"
                                else:
                                        self.value_status = "Not Good"
                               except:
                                print("stable value is none")
                            elif self.unit_text == 'm' or self.unit_text == 'M':
                                    lower_bound = lower_bound * 1000000
                                    upper_bound = upper_bound * 1000000
                                    self.stable_value= self.stable_value *1000000
                                    if lower_bound <= self.stable_value <= upper_bound:
                                        self.value_status = "OK"
                                    else:
                                        self.value_status = "Not Good"
                    #   else :
                    #      self.display_start_time= time.time()
                  
                      if self.stable_value is not None and int(time.time() - self.display_start_time) < self.display_duration:
                                self.stable_v = self.stable_value
                                self.status_label= self.value_status
                                print("status label:",self.status_label)
                                self.value_updated.emit(self.stable_v, self.status_label)
                      elif self.stable_value is not None and int(time.time() - self.display_start_time) >= self.display_duration:
                                self.stable_value = None
                                self.stable_v = 0.0
                                print(" greater than 3 ")
                                
                                self.status_label= ""
                                self.value_updated.emit(self.stable_v, self.status_label) # changed here 
                       
                # if frame_counter % 3 == 0:  # Process every third frame
                self.new_frame.emit(frame)
                # frame_counter += 1
            else:
                print("exit without frame")
                self.camera_error.emit("Error: Could not read frame.")
                break

        self.capture.release()

    def stop(self):
        self._run_flag = False
        self.quit()
        self.wait()

#Class for lux meter 


# import cv2
# from PyQt5.QtCore import QThread, pyqtSignal
# import numpy as np
# from ultralytics import YOLO
# from paddleocr import PaddleOCR
# # import add_test
# from add_test import AddTestDialog
# from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QMessageBox
# import re
# from datetime import datetime
# import time
# # from running_test_page import RunningTestPage
# from add_test import store_values
# from add_test import get_inputs
# class for lux meter readings 
class CameraThreadLux(QThread):
    new_frame = pyqtSignal(np.ndarray)
    camera_error = pyqtSignal(str)
    value_updated = pyqtSignal(float, str)
    # from running_test_page import RunningTestPage
    def __init__(self,test):
        super().__init__()
        self.add_test = AddTestDialog()
        # self.running_test_page = running_test_page
        # self.add_test.values_from_add_test.connect(self.get_add_test_values)
        self.value_status = ""
        self.extracted_values = []
        self.stable_value = None
        self.display_start_time = None
        self.display_duration = 3
        self._run_flag = True
        self.test_info = {}
        self.model = YOLO(r"C:\Users\a\yolo13\ultralytics1\ultralytics\best_03_09_24.pt")
        self.ocr = PaddleOCR(use_angle_cls=False, lang='en',show_log=False)
        
    #     try:
    # # Retrieve and validate inputs
    #         value_text = self.add_test.value_input.text().strip()
    #         tolerance_text = self.add_test.tolerance_input.text().strip()

    #         if not value_text or not tolerance_text:
    #              raise ValueError("Empty input")

    # # Convert the inputs to float
    #         value = float(value_text)
    #         tolerance = float(tolerance_text)

    # # Calculate the lower and upper bounds
    #         self.lower_bound = value - (tolerance / 100) * value
    #         self.upper_bound = value + (tolerance / 100) * value
    #     except ValueError:
    #             print("Input Error", "Please enter valid numeric values.")
        # self.lower_bound = float(self.add_test.value_input.text()) - (float(self.add_test.tolerance_input.text()) / 100) * float(self.add_test.value_input.text())
        # self.upper_bound = float(self.add_test.value_input.text()) + (float(self.add_test.tolerance_input.text()) / 100) * float(self.add_test.value_input.text())
        # magnitude = 0.0
        # tolerance = 0.0
        # self.add_test.value_input = 0.0
        self.lower_bound = 0.0
        self.upper_bound = 0.0
        self.stable_v= 0.0
        self.status_label = ""
        # self.value_text = 0.0
        self.value_text = float(test.get('value','N/A'))

        self.tolerance_text =float(test.get('tolerance','N/A'))
        self.value_text1 = float(test.get('value1','N/A'))

        self.tolerance_text1 =float(test.get('tolerance1','N/A'))
        self.value_text2 = float(test.get('value2','N/A'))

        self.tolerance_text2 =float(test.get('tolerance2','N/A'))
        self.unit_text = test.get(test.get('unit','N/A'))
        self.lower_bound = self.value_text - (self.tolerance_text / 100) * self.value_text
        self.upper_bound = self.value_text + (self.tolerance_text / 100) * self.value_text
        self.lower_bound1 = self.value_text1 - (self.tolerance_text1 / 100) * self.value_text1
        self.upper_bound1 = self.value_text1 + (self.tolerance_text1 / 100) * self.value_text1
        self.lower_bound2 = self.value_text2 - (self.tolerance_text2 / 100) * self.value_text2
        self.upper_bound2 = self.value_text2 + (self.tolerance_text2 / 100) * self.value_text2
    # def get_add_test_values(self,value,tolerance,unit):
    #         self.value_text = value
    #         self.tolerance_text = tolerance
    #         self.unit_text = unit
    #         self.lower_bound = float(value - (tolerance / 100) * value)
    #         self.upper_bound = float(value + (tolerance / 100) * value)
    #         print("add test values :: {self.value_text},{self.tolerance_text},{self.unit_text}")
    def detect_display_screen(self, results, frame):
        if results[0].obb.xyxy.shape[0] > 0:
            x1, y1, x2, y2 = map(int, results[0].obb.xyxy[0])
            height, width, _ = frame.shape
            x1 = max(0, min(x1, width))
            y1 = max(0, min(y1, height))
            x2 = max(0, min(x2, width))
            y2 = max(0, min(y2, height))
            roi = (x1, y1, x2, y2)
        else:
            roi = (100, 100, 400, 200)
        return roi
    def extract_text_from_roi(self, frame, roi):
        x1, y1, x2, y2 = roi
        cropped_image = frame[y1:y2, x1:x2]
        gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

        ocr_result = self.ocr.ocr(gray_image)

        extracted_text_lines = []
        if ocr_result and ocr_result[0]:
            for line in ocr_result:
                for word in line:
                    text, confidence = word[1]
                    extracted_text_lines.append(text)

        extracted_text = ' '.join(extracted_text_lines)
        return extracted_text

    def run(self):
        self.capture = cv2.VideoCapture(0)
        # self.value_text= float(test.get('value', 'N/A'))
        print(f"from running page to camera thread value pass {self.value_text} , {self.tolerance_text},{self.unit_text}")
        # print(f'list of values from running test = {self.running_test_page.value},{self.running_test_page.tolerance}')
        # if self.get_add_test_values():
        #     print("values received from signal")
        # if not self.capture.isOpened():
        #     self.camera_error.emit("Error: Could not open camera.")
        #     return
        # if self.add_test.exec_() == QDialog.Accepted:
        #     test_info = self.add_test.get_inputs()
        #     print(test_info)
        # else:
        #     print("didnt went past add test")
        # frame_counter = 0
        while self.capture.isOpened() and self._run_flag:
            ret, frame = self.capture.read()
            
            try:
    # Retrieve and validate inputs

            #  value_text = self.add_test.get_inputs().values()   
            #  print(value_text)
            #  tolerance_text = self.add_test.get_input().values()

            #  value_text = self.add_test.value_input.text().strip() #   input value = preset value
            #  tolerance_text = self.add_test.tolerance_input.text().strip() # tolerance value 
            #  print()
             if not self.value_text or not self.tolerance_text:
                 raise ValueError("Empty input")

    # Convert the inputs to float
             value_new = float(self.value_text)
             tolerance_new = float(self.tolerance_text)

    # Calculate the lower and upper bounds
             
            except ValueError:
                print("Input Error", "Please enter valid numeric values.")
            if ret:
                print("frame entered ")
                result=self.model.predict(frame,conf=0.65)
                if len(result[0].obb.xyxy.tolist()) == 1:
                      roi = self.detect_display_screen(result, frame)
                      cv2.rectangle(frame, (roi[0], roi[1]), (roi[2], roi[3]), (0, 255, 0), 2)
                      extracted_text = self.extract_text_from_roi(frame, roi)
                      cv2.putText(frame, f'OCR Text: {extracted_text}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                      numerical_values = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", extracted_text)
            
                      if numerical_values and len(numerical_values) != 0:
                         try:
                            strg = numerical_values[0].replace(' ', '')
                            value = float(strg)
                         except IndexError:
                            value = 0.0
                         self.extracted_values.append(value)

                      if len(self.extracted_values) >= 10:
                            last_values = self.extracted_values[-10:]
                            if all(v == last_values[0] and v != 0.0 for v in last_values):
                                    self.stable_value = last_values[0]
                                    self.display_start_time = time.time()
                                    self.extracted_values.clear()
                                    # print("unit values after:",self.add_test.unit_input.text())
                                    # print("unit values before:",self.add_test.unit_input)

                            # if self.unit_text == 'k' or self.unit_text == 'K':
                            if True:
                            #    lower_bound = lower_bound * 1000 
                            #    upper_bound = upper_bound * 1000
                               try:
                                # self.stable_value= self.stable_value 
                                if self.lower_bound <= self.stable_value <= self.upper_bound:
                                # if lower_bound <= self.stable_value <= upper_bound:
                                
                                        self.value_status = "OK"
                                else:
                                        self.value_status = "Not Good"
                               except:
                                print("stable value is none")
                            elif self.unit_text == 'm' or self.unit_text == 'M': # units not yet implemented in the code 
                                    lower_bound = lower_bound * 1000000
                                    upper_bound = upper_bound * 1000000
                                    self.stable_value= self.stable_value *1000000
                                    if lower_bound <= self.stable_value <= upper_bound:
                                        self.value_status = "OK"
                                    else:
                                        self.value_status = "Not Good"
                    #   else :
                    #      self.display_start_time= time.time()
                  
                      if self.stable_value is not None and int(time.time() - self.display_start_time) < self.display_duration:
                                self.stable_v = self.stable_value
                                self.status_label= self.value_status
                                print("status label:",self.status_label)
                                self.value_updated.emit(self.stable_v, self.status_label)
                      elif self.stable_value is not None and int(time.time() - self.display_start_time) >= self.display_duration:
                                self.stable_value = None
                                self.stable_v = 0.0
                                print(" greater than 3 ")
                                
                                self.status_label= ""
                                self.value_updated.emit(self.stable_v, self.status_label) # changed here 
                      self.new_frame.emit(frame)
                else:
                    self.new_frame.emit(frame) #new code here 30-10 18:35
                    self.stable_value = None
                    self.stable_v = 0.0
                    self.status_label= "INVALID"
                    self.value_updated.emit(self.stable_v, self.status_label)

                 # if frame_counter % 3 == 0:  # Process every third frame
                # self.new_frame.emit(frame)
                # else:
                # frame_counter += 1
            else:
                print("exit without frame")
                self.camera_error.emit("Error: Could not read frame.")
                break

        self.capture.release()

    def stop(self):
        self._run_flag = False
        self.quit()
        self.wait()

from concurrent.futures import ThreadPoolExecutor
# case 3 : mutiple meters (still working on it)
class CameraThreadmeters(QThread):
    new_frame = pyqtSignal(np.ndarray)
    camera_error = pyqtSignal(str)
    value_updated = pyqtSignal(float, str)
    value_updated1 = pyqtSignal(float, str)
    value_updated2 = pyqtSignal(float, str)
    value_updated3 = pyqtSignal(str, str)
    # value_updated
    # from running_test_page import RunningTestPage
    def __init__(self,test,model,ocr1,ocr2):
        super().__init__()
        # self.add_test = AddTestDialog()
        # self.running_test_page = running_test_page
        # self.add_test.values_from_add_test.connect(self.get_add_test_values)
        self.value_status = ""
        self.value_status1 = ""
        self.value_status2 = ""
        
        self.extracted_values = []
        self.extracted_values1 = []
        self.extracted_values2 = []
        self.extracted_values_no_nc = []
        self.stable_value = None
        self.stable_value1 = None 
        self.stable_value2 = None 
        
        self.display_start_time = None
        self.display_start_time1 = None
        self.display_start_time2 = None

        self.display_duration = 3
        self._run_flag = True
        self.test_info = {}
        
        # self.model = YOLO(r"C:\Users\a\yolo13\ultralytics1\ultralytics\best_03_09_24.pt")
        # self.model = YOLO(r"D:\best_lux_meter_inc_2_11_24.pt")# newly added on 2_11_24
        # self.ocr1 = PaddleOCR(use_angle_cls=False, lang='en',show_log=False)
        # self.ocr2 = PaddleOCR(use_angle_cls=False, lang='en',show_log=False)
        self.model = model
        self.ocr1 = ocr1

        self.ocr2 = ocr2
    #     try:
    # # Retrieve and validate inputs
    #         value_text = self.add_test.value_input.text().strip()
    #         tolerance_text = self.add_test.tolerance_input.text().strip()

    #         if not value_text or not tolerance_text:
    #              raise ValueError("Empty input")

    # # Convert the inputs to float
    #         value = float(value_text)
    #         tolerance = float(tolerance_text)

    # # Calculate the lower and upper bounds
    #         self.lower_bound = value - (tolerance / 100) * value
    #         self.upper_bound = value + (tolerance / 100) * value
    #     except ValueError:
    #             print("Input Error", "Please enter valid numeric values.")
        # self.lower_bound = float(self.add_test.value_input.text()) - (float(self.add_test.tolerance_input.text()) / 100) * float(self.add_test.value_input.text())
        # self.upper_bound = float(self.add_test.value_input.text()) + (float(self.add_test.tolerance_input.text()) / 100) * float(self.add_test.value_input.text())
        # magnitude = 0.0
        # tolerance = 0.0
        # self.add_test.value_input = 0.0
        self.lower_bound = 0.0
        self.upper_bound = 0.0
        self.lower_bound1 = 0.0
        self.upper_bound1= 0.0
        self.lower_bound2 = 0.0
        self.upper_bound2 = 0.0
        self.stable_v= 0.0
        self.status_label = ""
        # self.value_text = 0.0
        # self.value_text = float(test.get('value1','N/A'))

        # self.tolerance_text =float(test.get('tolerance1','N/A'))
        # self.unit_text = test.get(test.get('unit1','N/A'))
        # self.lower_bound = self.value_text - (self.tolerance_text / 100) * self.value_text
        # self.upper_bound = self.value_text + (self.tolerance_text / 100) * self.value_text
        # self.value_text = float(test.get('value','N/A'))

        # self.tolerance_text =float(test.get('tolerance','N/A'))
        self.model_values = test.get('Model','N/A')
        print("model name :",self.model_values)
        if self.model_values == "DoubleMeters":
            self.value_text1 = float(test.get('value1','N/A'))

            self.tolerance_text1 =float(test.get('tolerance1','N/A'))
            self.floating_text1 = test.get('floatingPoint1','N/A')
            self.value_text2 = float(test.get('value2','N/A'))

            self.tolerance_text2 =float(test.get('tolerance2','N/A'))
            self.floating_text2 = test.get('floatingPoint2','N/A')
        # self.unit_text = test.get(test.get('unit','N/A'))
        # self.lower_bound = self.value_text - (self.tolerance_text / 100) * self.value_text
        # self.upper_bound = self.value_text + (self.tolerance_text / 100) * self.value_text
            self.lower_bound1 = self.value_text1 - (self.tolerance_text1 / 100) * self.value_text1
            self.upper_bound1 = self.value_text1 + (self.tolerance_text1 / 100) * self.value_text1
            self.lower_bound2 = self.value_text2 - (self.tolerance_text2 / 100) * self.value_text2
            self.upper_bound2 = self.value_text2 + (self.tolerance_text2 / 100) * self.value_text2
        elif self.model_values == "NO/NC":
            self.value_text1 = float(test.get('value1','N/A'))

            self.tolerance_text1 =float(test.get('tolerance1','N/A'))
            self.floating_text1 = test.get('floatingPoint1','N/A')
        else:
            self.value_text1 = float(test.get('value1','N/A'))

            self.tolerance_text1 =float(test.get('tolerance1','N/A'))
            self.floating_text1 = test.get('floatingPoint1','N/A')
            self.lower_bound1 = self.value_text1 - (self.tolerance_text1 / 100) * self.value_text1
            self.upper_bound1 = self.value_text1 + (self.tolerance_text1 / 100) * self.value_text1
            
    # def get_add_test_values(self,value,tolerance,unit):
    #         self.value_text = value
    #         self.tolerance_text = tolerance
    #         self.unit_text = unit
    #         self.lower_bound = float(value - (tolerance / 100) * value)
    #         self.upper_bound = float(value + (tolerance / 100) * value)
    #         print("add test values :: {self.value_text},{self.tolerance_text},{self.unit_text}")
    def detect_display_screen(self, results, frame): # for single meter display 
        if results[0].obb.xyxy.shape[0] > 0:
            x1, y1, x2, y2 = map(int, results[0].obb.xyxy[0])
            height, width, _ = frame.shape
            x1 = max(0, min(x1, width))
            y1 = max(0, min(y1, height))
            x2 = max(0, min(x2, width))
            y2 = max(0, min(y2, height))
            roi = (x1, y1, x2, y2)
        else:
            roi = (100, 100, 400, 200)
        return roi
    def detect_display_screen_meters(self, results, frame):#for 2 meter display
        if results[0].obb.xyxy.shape[0] > 0:
            try:

                x11, y11, x21, y21 = map(int, results[0].obb.xyxy[0])
                x12, y12, x22, y22 = map(int, results[0].obb.xyxy[1])
            except ValueError:
                print("Value Error / Empty ")
            height, width, _ = frame.shape
            x11 = max(0, min(x11, width))
            y11 = max(0, min(y11, height))
            x21 = max(0, min(x21, width))
            y21 = max(0, min(y21, height))
            roi1 = (x11, y11, x21, y21) # roi for first BB
            x12 = max(0, min(x12, width))
            y12 = max(0, min(y12, height))
            x22 = max(0, min(x22, width))
            y22 = max(0, min(y22, height))
            roi2 = (x12, y12, x22, y22) # roi for the second BB
        else:
            roi1 = (100, 100, 400, 200) # default random co-ordinates for the detected BB
            roi2 = (100, 100, 400 ,200)
        return roi1,roi2
    def extract_text_from_roi_no_nc(self, frame, roi):
        x1, y1, x2, y2 = roi
        cropped_image = frame[y1:y2, x1:x2]
        gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        try:
         ocr_result = self.ocr1.ocr(gray_image)
        except ValueError:
            print("Ocr text empty for the moment")
        extracted_text_lines = []
        if ocr_result and ocr_result[0]:
            for line in ocr_result:
                for word in line:
                    text, confidence = word[1]
                    extracted_text_lines.append(text)

        extracted_text = ' '.join(extracted_text_lines)
        cv2.putText(frame, f'OCR_NO_NC Text: {extracted_text}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
        # if 'M' in extracted_text or 'Mn' in extracted_text:
        #             self.value_status1 = "Open"
        # else:
        #             self.value_status1 = "Close"
        
        
        if self.floating_text1 == 'y':
            # print(f"floating point text 1 : {self.floating_text1}")
            numerical_values = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*", extracted_text)
        else:
            numerical_values = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", extracted_text)
            
        if numerical_values and len(numerical_values) != 0:
             try:
                            strg = numerical_values[0].replace(' ', '')
                            value = float(strg)
             except IndexError:
                 value = 0.0
             self.extracted_values_no_nc.append(value)

        # value = float(re.findall(r"\d+\.?\d*", text)[0]) if re.findall(r"\d+\.?\d*", text) else 0.0
        # self.extracted_values.append(value)
        self.extracted_values1.append(extracted_text)
        # Check if we have 10 or more readings for stability check
        if len(self.extracted_values1) >= 10:
            last_values = self.extracted_values1[-5:]
            if any('M' in str(v) or 'Mn' in str(v) for v in last_values):
                self.value_status1 = "Open"
                self.stable_value1 = "0.0 M"
                self.value_updated3.emit(self.stable_value1,self.value_status1)
                self.extracted_values1.clear()
            else:
                self.value_status1 = "Close"
                
                if len(self.extracted_values_no_nc) >= 8:
                    last_values = self.extracted_values_no_nc[-8:]
                    if all(v == last_values[0] for v in last_values):
                        self.stable_value1 = last_values[0]
                        self.display_start_time1 = time.time()
                    self.extracted_values_no_nc.clear()
                if self.stable_value1 is not None and int(time.time() - self.display_start_time1) < self.display_duration:
                    # stable_v = self.stable_value1
                    # status_label= self.value_status1
                    # print(f"values1t = {self.stable_value1},{status_label}")
                            self.value_updated3.emit(self.stable_value1,self.value_status1)
                elif self.stable_value1 is not None and int(time.time() - self.display_start_time1) >= self.display_duration:
                            self.stable_value1 = None
                            stable_v = ""
                            # print(" greater than 3 ")
                            status_label= ""
                            # print(f"values1f = {self.stable_value1},{status_label}")
                            self.value_updated3.emit(stable_v, status_label)
                
                # if True:
                #             #    lower_bound = lower_bound * 1000 
                #             #    upper_bound = upper_bound * 1000
                #     try:
                #                 # self.stable_value= self.stable_value 
                #        if self.lower_bound1 <= self.stable_value1 <= self.upper_bound1:
                #                 # if lower_bound <= self.stable_value <= upper_bound:
                                
                #            self.value_status1 = "OK"
                #        else:
                #            self.value_status1 = "Not Good"
                #     except:
                #            print("stable value is none")
                # Convert stable value based on unit text
                # if self.unit_text.lower() == 'k':
                #     stable_value *= 1000
                # elif self.unit_text.lower() == 'm':
                #     stable_value *= 1000000

                # Determine value status based on bounds
                # if self.lower_bound <= stable_value <= self.upper_bound:
                #     value_status = "OK"
                # else:
                #     value_status = "Not Good"
        
    def extract_text_from_roi_1_rev(self, frame, roi):
        x1, y1, x2, y2 = roi
        cropped_image = frame[y1:y2, x1:x2]
        gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        try:
         ocr_result = self.ocr1.ocr(gray_image)
        except ValueError:
            print("Ocr text empty for the moment")
        extracted_text_lines = []
        if ocr_result and ocr_result[0]:
            for line in ocr_result:
                for word in line:
                    text, confidence = word[1]
                    extracted_text_lines.append(text)

        extracted_text = ' '.join(extracted_text_lines)
        cv2.putText(frame, f'OCR1 Text: {extracted_text}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
        if self.floating_text1 == 'y':
            # print(f"floating point text 1 : {self.floating_text1}")
            numerical_values = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*", extracted_text)
        else:
            numerical_values = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", extracted_text)
            
        if numerical_values and len(numerical_values) != 0:
             try:
                            strg = numerical_values[0].replace(' ', '')
                            value = float(strg)
             except IndexError:
                 value = 0.0
             self.extracted_values1.append(value)

        # value = float(re.findall(r"\d+\.?\d*", text)[0]) if re.findall(r"\d+\.?\d*", text) else 0.0
        # self.extracted_values.append(value)

        # Check if we have 10 or more readings for stability check
        if len(self.extracted_values1) >= 10:
            last_values = self.extracted_values1[-10:]
            if all(v == last_values[0] and v != 0.0 for v in last_values):
                self.stable_value1 = last_values[0]
                self.display_start_time1 = time.time()
                self.extracted_values1.clear()
                
                if True:
                            #    lower_bound = lower_bound * 1000 
                            #    upper_bound = upper_bound * 1000
                    try:
                                # self.stable_value= self.stable_value 
                       if self.lower_bound1 <= self.stable_value1 <= self.upper_bound1:
                                # if lower_bound <= self.stable_value <= upper_bound:
                                
                           self.value_status1 = "OK"
                       else:
                           self.value_status1 = "Not Good"
                    except:
                           print("stable value is none")
                # Convert stable value based on unit text
                # if self.unit_text.lower() == 'k':
                #     stable_value *= 1000
                # elif self.unit_text.lower() == 'm':
                #     stable_value *= 1000000

                # Determine value status based on bounds
                # if self.lower_bound <= stable_value <= self.upper_bound:
                #     value_status = "OK"
                # else:
                #     value_status = "Not Good"
        if self.stable_value1 is not None and int(time.time() - self.display_start_time1) < self.display_duration:
                    stable_v = self.stable_value1
                    status_label= self.value_status1
                    # print(f"values1t = {self.stable_value1},{status_label}")
                    self.value_updated1.emit(stable_v,status_label)
        elif self.stable_value1 is not None and int(time.time() - self.display_start_time1) >= self.display_duration:
                    self.stable_value1 = None
                    stable_v = 0.0
                    # print(" greater than 3 ")
                    status_label= ""
                    # print(f"values1f = {self.stable_value1},{status_label}")
                    self.value_updated1.emit(stable_v, status_label)
        #         return stable_value, value_status, display_start_time
        # return None, "", None
        # return extracted_text
    def extract_text_from_roi_2_rev(self, frame, roi):
        x1, y1, x2, y2 = roi
        cropped_image = frame[y1:y2, x1:x2]
        gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        try:
         ocr_result = self.ocr2.ocr(gray_image)
        except ValueError:
            print("Ocr text empty for the moment")
        extracted_text_lines = []
        if ocr_result and ocr_result[0]:
            for line in ocr_result:
                for word in line:
                    text, confidence = word[1]
                    extracted_text_lines.append(text)

        extracted_text = ' '.join(extracted_text_lines)
        cv2.putText(frame, f'OCR2 Text: {extracted_text}', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
        # numerical_values = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", extracted_text)
        if self.floating_text2 == 'y':
            print(f"floating point text 1 : {self.floating_text2}")
            numerical_values = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*", extracted_text)
        else:
            numerical_values = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", extracted_text)
        if numerical_values and len(numerical_values) != 0:
             try:
                            strg = numerical_values[0].replace(' ', '')
                            value = float(strg)
             except IndexError:
                 value = 0.0
             self.extracted_values2.append(value)

        # value = float(re.findall(r"\d+\.?\d*", text)[0]) if re.findall(r"\d+\.?\d*", text) else 0.0
        # self.extracted_values.append(value)

        # Check if we have 10 or more readings for stability check
        if len(self.extracted_values2) >= 10:
            last_values = self.extracted_values2[-10:]
            if all(v == last_values[0] and v != 0.0 for v in last_values):
                self.stable_value2 = last_values[0]
                self.display_start_time2 = time.time()
                self.extracted_values2.clear()
                
                if True:
                            #    lower_bound = lower_bound * 1000 
                            #    upper_bound = upper_bound * 1000
                    try:
                                # self.stable_value= self.stable_value 
                       if self.lower_bound2 <= self.stable_value2 <= self.upper_bound2:
                                # if lower_bound <= self.stable_value <= upper_bound:
                                
                           self.value_status2 = "OK"
                       else:
                           self.value_status2 = "Not Good"
                    except:
                           print("stable value is none")
                # Convert stable value based on unit text
                # if self.unit_text.lower() == 'k':
                #     stable_value *= 1000
                # elif self.unit_text.lower() == 'm':
                #     stable_value *= 1000000

                # Determine value status based on bounds
                # if self.lower_bound <= stable_value <= self.upper_bound:
                #     value_status = "OK"
                # else:
                #     value_status = "Not Good"
        if self.stable_value2 is not None and int(time.time() - self.display_start_time2) < self.display_duration:
                    stable_v = self.stable_value2
                    status_label= self.value_status2
                    # print(f"values1t = {self.stable_value2},{status_label}")
                    self.value_updated2.emit(stable_v,status_label)
        elif self.stable_value2 is not None and int(time.time() - self.display_start_time2) >= self.display_duration:
                    self.stable_value2 = None
                    stable_v = 0.0
                    # print(" greater than 3 ")
                    status_label= ""
                    # print(f"values1f = {self.stable_value2},{status_label}") # for testing 
                    self.value_updated2.emit(stable_v, status_label)
    def extract_text_from_roi_1(self, frame, roi):
        x1, y1, x2, y2 = roi
        cropped_image = frame[y1:y2, x1:x2]
        gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        try:
         ocr_result = self.ocr1.ocr(gray_image)
        except ValueError:
            print("Ocr text empty for the moment")
        extracted_text_lines = []
        if ocr_result and ocr_result[0]:
            for line in ocr_result:
                for word in line:
                    text, confidence = word[1]
                    extracted_text_lines.append(text)

        extracted_text = ' '.join(extracted_text_lines)
        return extracted_text
    def extract_text_from_roi_2(self, frame, roi):
        x1, y1, x2, y2 = roi
        cropped_image = frame[y1:y2, x1:x2]
        gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        try:
         ocr_result = self.ocr2.ocr(gray_image)
        except ValueError:
            print("Ocr text empty for the moment")
        extracted_text_lines = []
        if ocr_result and ocr_result[0]:
            for line in ocr_result:
                for word in line:
                    text, confidence = word[1]
                    extracted_text_lines.append(text)

        extracted_text = ' '.join(extracted_text_lines)
        return extracted_text
    def process_single_text(self, text): #newly added
        """Processes a single extracted text value to determine stability and status."""
        # extracted_values = []
        numerical_values = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", text)
            
        if numerical_values and len(numerical_values) != 0:
             try:
                            strg = numerical_values[0].replace(' ', '')
                            value = float(strg)
             except IndexError:
                 value = 0.0
             self.extracted_values.append(value)

        # value = float(re.findall(r"\d+\.?\d*", text)[0]) if re.findall(r"\d+\.?\d*", text) else 0.0
        # self.extracted_values.append(value)

        # Check if we have 10 or more readings for stability check
        if len(self.extracted_values) >= 10:
            last_values = self.extracted_values[-10:]
            if all(v == last_values[0] and v != 0.0 for v in last_values):
                stable_value = last_values[0]
                display_start_time = time.time()
                self.extracted_values.clear()
                
                if True:
                            #    lower_bound = lower_bound * 1000 
                            #    upper_bound = upper_bound * 1000
                    try:
                                # self.stable_value= self.stable_value 
                       if self.lower_bound <= stable_value <= self.upper_bound:
                                # if lower_bound <= self.stable_value <= upper_bound:
                                
                           value_status = "OK"
                       else:
                           value_status = "Not Good"
                    except:
                           print("stable value is none")
                # Convert stable value based on unit text
                # if self.unit_text.lower() == 'k':
                #     stable_value *= 1000
                # elif self.unit_text.lower() == 'm':
                #     stable_value *= 1000000

                # Determine value status based on bounds
                # if self.lower_bound <= stable_value <= self.upper_bound:
                #     value_status = "OK"
                # else:
                #     value_status = "Not Good"

                return stable_value, value_status, display_start_time
        return None, "", None
    def status_checker1(self,stable_value,status,display_start_time):
        print("reached status checker1")
        if stable_value is not None and int(time.time() - display_start_time) < self.display_duration:
                    stable_v = stable_value
                    status_label= value_status
                    print(f"values1t = {stable_value},{status_label}")
                    self.value_updated1.emit(stable_v,status_label)
        elif stable_value is not None and int(time.time() - self.display_start_time) >= self.display_duration:
                    stable_value = None
                    stable_v = 0.0
                    # print(" greater than 3 ")
                    status_label= ""
                    print(f"values1f = {stable_value},{status_label}")
                    self.value_updated1.emit(stable_v, status_label)
    def status_checker2(self,stable_value,status,display_start_time):
        print("reached status checker2")
        if stable_value is not None and int(time.time() - display_start_time) < self.display_duration:
                    stable_v = stable_value
                    status_label= value_status
                    print(f"values2t = {stable_value},{status_label}")
                    self.value_updated2.emit(stable_v,status_label)
        elif stable_value is not None and int(time.time() - self.display_start_time) >= self.display_duration:
                    stable_value = None
                    stable_v = 0.0
                    # print(" greater than 3 ")
                    status_label= ""
                    print(f"values2f = {stable_value},{status_label}")
                    self.value_updated2.emit(stable_v, status_label)                
    def process_extracted_text(self, text1, text2, frame): #newly added

        # Use ThreadPoolExecutor to process both texts concurrently
        with ThreadPoolExecutor() as executor:
            future1 = executor.submit(self.process_single_text, text1)
            future2 = executor.submit(self.process_single_text, text2)

            # Retrieve results for both texts
            stable_value1, status1, display_start_time1 = future1.result()
            print(f"stable1={stable_value1}/n")
            stable_value2, status2, display_start_time2 = future2.result()
            print(f"stable1={stable_value2}")
        return stable_value1, status1, display_start_time1,stable_value2, status2, display_start_time2
        # with ThreadPoolExecutor() as executor: # newly added 2-11-24
        #     var1 = executor.submit(self.status_checker,stable_value1,status1,display_start_time1)
        #     var2 = executor.submit(self.status_checker,stable_value2,status2,display_start_time2)
    def apply_zoom(self,frame, zoom_scale):
        try:
            height, width = frame.shape[:2]
            center_x, center_y = width // 2, height // 2
        # zoom_scale = 2

        # Calculate the coordinates of the region to crop
            new_width = int(width / zoom_scale)
            new_height = int(height / zoom_scale)
        
            left = center_x - new_width // 2
            right = center_x + new_width // 2
            top = center_y - new_height // 2
            bottom = center_y + new_height // 2
        
        # Crop and resize the frame
            frame_zoomed = frame[top:bottom, left:right]
            frame_zoomed = cv2.resize(frame_zoomed, (width, height))
            return frame_zoomed
        except:
            print("frame not found error")   
    def run(self):
        self.capture = cv2.VideoCapture(0)
        # self.value_text= float(test.get('value', 'N/A'))
        # print(f"from running page to camera thread value pass {self.value_text} , {self.tolerance_text},{self.unit_text}")
        # print(f'list of values from running test = {self.running_test_page.value},{self.running_test_page.tolerance}')
        # if self.get_add_test_values():
        #     print("values received from signal")
        # if not self.capture.isOpened():
        #     self.camera_error.emit("Error: Could not open camera.")
        #     return
        # if self.add_test.exec_() == QDialog.Accepted:
        #     test_info = self.add_test.get_inputs()
        #     print(test_info)
        # else:
        #     print("didnt went past add test")
        # frame_counter = 0

        while self.capture.isOpened() and self._run_flag:
            ret, frame = self.capture.read()
            if self.model_values== "NO/NC":
                frame = self.apply_zoom(frame,1.9)
            # try:
    # Retrieve and validate inputs

            #  value_text = self.add_test.get_inputs().values()   
            #  print(value_text)
            #  tolerance_text = self.add_test.get_input().values()

            #  value_text = self.add_test.value_input.text().strip() #   input value = preset value
            #  tolerance_text = self.add_test.tolerance_input.text().strip() # tolerance value 
            #  print()
            #  if not self.value_text or not self.tolerance_text:
            #      raise ValueError("Empty input")

    # Convert the inputs to float
            #  value_new = float(self.value_text)
            #  tolerance_new = float(self.tolerance_text)

    # Calculate the lower and upper bounds
             
            # except ValueError:
            #     print("Input Error", "Please enter valid numeric values.")
            if ret:
                # print("frame entered ")
                result=self.model.predict(frame,conf=0.65)
                if self.model_values== "DoubleMeters":
                    if len(result[0].obb.xyxy.tolist()) == 2: # for 2 meter display 
                            roi1,roi2= self.detect_display_screen_meters(result, frame)
                            #if roi1 < roi2: # left screen is meter 1 and right screen is meter 2 , logic : checking x co ordinate values of the two roi and choosing text1 corresponding to roi1<roi2 or vice-versa

                            cv2.rectangle(frame, (roi1[0], roi1[1]), (roi1[2], roi1[3]), (0, 255, 0), 2)
                            cv2.rectangle(frame, (roi2[0], roi2[1]), (roi2[2], roi2[3]), (0, 255, 0), 2)
                        
                            # if text is empty  (try and except )
                            if roi1[0] < roi2[0]:
                                with ThreadPoolExecutor() as executor:
                                    future1 = executor.submit(self.extract_text_from_roi_1_rev, frame, roi1)
                                    future2 = executor.submit(self.extract_text_from_roi_2_rev, frame, roi2)
                                    try:
                                        future1.result()
                                        future2.result()
                                    except ValueError:
                                        print("Threading not executed properly :(")
                            else:
                                with ThreadPoolExecutor() as executor:
                                    future1 = executor.submit(self.extract_text_from_roi_1_rev, frame, roi2)
                                    future2 = executor.submit(self.extract_text_from_roi_2_rev, frame, roi1)
                                    try:
                                        future1.result()
                                        future2.result()
                                    except ValueError:
                                        print("Threading not executed properly :(")
                            
                        #   cv2.putText(frame, f'OCR1 Text: {extracted_text1},OCR2 Text: {extracted_text2}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                            #__________________working fine till here__________________________
                        #   stable_value1, status1, display_start_time1,stable_value2, status2, display_start_time2=self.process_extracted_text(extracted_text1, extracted_text2, frame)
                        #   print(f"stable1={stable_value1},stable2= {stable_value2}")
                        #   with ThreadPoolExecutor() as executor:
                        #     executor.submit(self.status_checker1, stable_value1, status1, display_start_time1)
                        #     executor.submit(self.status_checker2, stable_value2, status2, display_start_time2)
                            
                            #after getting the status , need to send it to the 
                        #   extracted_text1 = self.extract_text_from_roi(frame, roi1)
                        #   extracted_text2 = self.extract_text_from_roi(frame, roi2)
                        #   cv2.putText(frame, f'OCR1 Text: {extracted_text1} OCR1 Text: {extracted_text2}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                        #   numerical_values1 = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", extracted_text1)
                
                        #   if numerical_values1 and len(numerical_values1) != 0:
                        #      try:
                        #         strg = numerical_values1[0].replace(' ', '')
                        #         value = float(strg)
                        #      except IndexError:
                        #         value = 0.0
                        #      self.extracted_values1.append(value)
                            
                        #   numerical_values2 = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", extracted_text2)
                
                        #   if numerical_values2 and len(numerical_values2) != 0:
                        #      try:
                        #         strg = numerical_values2[0].replace(' ', '')
                        #         value = float(strg)
                        #      except IndexError:
                        #         value = 0.0
                        #      self.extracted_values2.append(value)

                        #   if len(self.extracted_values) >= 10:
                        #         last_values = self.extracted_values[-10:]
                        #         if all(v == last_values[0] and v != 0.0 for v in last_values):
                        #                 self.stable_value = last_values[0]
                        #                 self.display_start_time = time.time()
                        #                 self.extracted_values.clear()
                        #                 # print("unit values after:",self.add_test.unit_input.text())
                        #                 # print("unit values before:",self.add_test.unit_input)

                        #         # if self.unit_text == 'k' or self.unit_text == 'K':
                        #         if True:
                        #         #    lower_bound = lower_bound * 1000 
                        #         #    upper_bound = upper_bound * 1000
                        #            try:
                        #             # self.stable_value= self.stable_value 
                        #             if self.lower_bound <= self.stable_value <= self.upper_bound:
                        #             # if lower_bound <= self.stable_value <= upper_bound:
                                    
                        #                     self.value_status = "OK"
                        #             else:
                        #                     self.value_status = "Not Good"
                        #            except:
                        #             print("stable value is none")
                        #         elif self.unit_text == 'm' or self.unit_text == 'M': # units not yet implemented in the code 
                        #                 lower_bound = lower_bound * 1000000
                        #                 upper_bound = upper_bound * 1000000
                        #                 self.stable_value= self.stable_value *1000000
                        #                 if lower_bound <= self.stable_value <= upper_bound:
                        #                     self.value_status = "OK"
                        #                 else:
                        #                     self.value_status = "Not Good"
                        # #   else :
                        # #      self.display_start_time= time.time()
                        
                        #   if self.stable_value is not None and int(time.time() - self.display_start_time) < self.display_duration:
                        #             self.stable_v = self.stable_value
                        #             self.status_label= self.value_status
                        #             print("status label:",self.status_label)
                        #             self.value_updated.emit(self.stable_v, self.status_label)
                        #   elif self.stable_value is not None and int(time.time() - self.display_start_time) >= self.display_duration:
                        #             self.stable_value = None
                        #             self.stable_v = 0.0
                        #             print(" greater than 3 ")
                                    
                        #             self.status_label= ""
                        #             self.value_updated.emit(self.stable_v, self.status_label) # changed here 
                            self.new_frame.emit(frame)
                    else:
                        self.new_frame.emit(frame) #new code here 30-10 18:35
                        self.stable_value1 = None
                        self.stable_value2 = None
                        # self.stable_v = 0.0
                        stable_v  = 0.0
                        status_label= "INVALID"
                        # self.value_updated.emit(self.stable_v, self.status_label)
                        self.value_updated1.emit(stable_v, status_label)
                        self.value_updated2.emit(stable_v, status_label)
                 # if frame_counter % 3 == 0:  # Process every third frame
                # self.new_frame.emit(frame)
                # else:
                # frame_counter += 1
                elif self.model_values== "NO/NC":
                    if len(result[0].obb.xyxy.tolist()) == 1: # for 2 meter display 
                            roi1 = self.detect_display_screen(result, frame)
                            #if roi1 < roi2: # left screen is meter 1 and right screen is meter 2 , logic : checking x co ordinate values of the two roi and choosing text1 corresponding to roi1<roi2 or vice-versa

                            cv2.rectangle(frame, (roi1[0], roi1[1]), (roi1[2], roi1[3]), (0, 255, 0), 2)
                            
                        
                            # if text is empty  (try and except )
                            
                            with ThreadPoolExecutor() as executor:
                                future1 = executor.submit(self.extract_text_from_roi_no_nc, frame, roi1)
                                # future2 = executor.submit(self.extract_text_from_roi_2_rev, frame, roi2)
                                try:
                                    future1.result()
                                    
                                except ValueError:
                                    print("Threading not executed properly :(")
                            
                            
                        #   cv2.putText(frame, f'OCR1 Text: {extracted_text1},OCR2 Text: {extracted_text2}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                            #__________________working fine till here__________________________
                        #   stable_value1, status1, display_start_time1,stable_value2, status2, display_start_time2=self.process_extracted_text(extracted_text1, extracted_text2, frame)
                        #   print(f"stable1={stable_value1},stable2= {stable_value2}")
                        #   with ThreadPoolExecutor() as executor:
                        #     executor.submit(self.status_checker1, stable_value1, status1, display_start_time1)
                        #     executor.submit(self.status_checker2, stable_value2, status2, display_start_time2)
                            
                            #after getting the status , need to send it to the 
                        #   extracted_text1 = self.extract_text_from_roi(frame, roi1)
                        #   extracted_text2 = self.extract_text_from_roi(frame, roi2)
                        #   cv2.putText(frame, f'OCR1 Text: {extracted_text1} OCR1 Text: {extracted_text2}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                        #   numerical_values1 = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", extracted_text1)
                
                        #   if numerical_values1 and len(numerical_values1) != 0:
                        #      try:
                        #         strg = numerical_values1[0].replace(' ', '')
                        #         value = float(strg)
                        #      except IndexError:
                        #         value = 0.0
                        #      self.extracted_values1.append(value)
                            
                        #   numerical_values2 = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", extracted_text2)
                
                        #   if numerical_values2 and len(numerical_values2) != 0:
                        #      try:
                        #         strg = numerical_values2[0].replace(' ', '')
                        #         value = float(strg)
                        #      except IndexError:
                        #         value = 0.0
                        #      self.extracted_values2.append(value)

                        #   if len(self.extracted_values) >= 10:
                        #         last_values = self.extracted_values[-10:]
                        #         if all(v == last_values[0] and v != 0.0 for v in last_values):
                        #                 self.stable_value = last_values[0]
                        #                 self.display_start_time = time.time()
                        #                 self.extracted_values.clear()
                        #                 # print("unit values after:",self.add_test.unit_input.text())
                        #                 # print("unit values before:",self.add_test.unit_input)

                        #         # if self.unit_text == 'k' or self.unit_text == 'K':
                        #         if True:
                        #         #    lower_bound = lower_bound * 1000 
                        #         #    upper_bound = upper_bound * 1000
                        #            try:
                        #             # self.stable_value= self.stable_value 
                        #             if self.lower_bound <= self.stable_value <= self.upper_bound:
                        #             # if lower_bound <= self.stable_value <= upper_bound:
                                    
                        #                     self.value_status = "OK"
                        #             else:
                        #                     self.value_status = "Not Good"
                        #            except:
                        #             print("stable value is none")
                        #         elif self.unit_text == 'm' or self.unit_text == 'M': # units not yet implemented in the code 
                        #                 lower_bound = lower_bound * 1000000
                        #                 upper_bound = upper_bound * 1000000
                        #                 self.stable_value= self.stable_value *1000000
                        #                 if lower_bound <= self.stable_value <= upper_bound:
                        #                     self.value_status = "OK"
                        #                 else:
                        #                     self.value_status = "Not Good"
                        # #   else :
                        # #      self.display_start_time= time.time()
                        
                        #   if self.stable_value is not None and int(time.time() - self.display_start_time) < self.display_duration:
                        #             self.stable_v = self.stable_value
                        #             self.status_label= self.value_status
                        #             print("status label:",self.status_label)
                        #             self.value_updated.emit(self.stable_v, self.status_label)
                        #   elif self.stable_value is not None and int(time.time() - self.display_start_time) >= self.display_duration:
                        #             self.stable_value = None
                        #             self.stable_v = 0.0
                        #             print(" greater than 3 ")
                                    
                        #             self.status_label= ""
                        #             self.value_updated.emit(self.stable_v, self.status_label) # changed here 
                            self.new_frame.emit(frame)
                    else:
                        self.new_frame.emit(frame) #new code here 30-10 18:35
                        self.stable_value1 = None
                        self.stable_value2 = None
                        # self.stable_v = 0.0
                        stable_v  = 0.0
                        status_label= "INVALID"
                        # self.value_updated.emit(self.stable_v, self.status_label)
                        self.value_updated1.emit(stable_v, status_label)
                        self.value_updated2.emit(stable_v, status_label)

                else:
                    if len(result[0].obb.xyxy.tolist()) == 1: # for 2 meter display 
                            roi1 = self.detect_display_screen(result, frame)
                            #if roi1 < roi2: # left screen is meter 1 and right screen is meter 2 , logic : checking x co ordinate values of the two roi and choosing text1 corresponding to roi1<roi2 or vice-versa

                            cv2.rectangle(frame, (roi1[0], roi1[1]), (roi1[2], roi1[3]), (0, 255, 0), 2)
                            
                        
                            # if text is empty  (try and except )
                            
                            with ThreadPoolExecutor() as executor:
                                future1 = executor.submit(self.extract_text_from_roi_1_rev, frame, roi1)
                                # future2 = executor.submit(self.extract_text_from_roi_2_rev, frame, roi2)
                                try:
                                    future1.result()
                                    
                                except ValueError:
                                    print("Threading not executed properly :(")
                            
                            
                        #   cv2.putText(frame, f'OCR1 Text: {extracted_text1},OCR2 Text: {extracted_text2}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                            #__________________working fine till here__________________________
                        #   stable_value1, status1, display_start_time1,stable_value2, status2, display_start_time2=self.process_extracted_text(extracted_text1, extracted_text2, frame)
                        #   print(f"stable1={stable_value1},stable2= {stable_value2}")
                        #   with ThreadPoolExecutor() as executor:
                        #     executor.submit(self.status_checker1, stable_value1, status1, display_start_time1)
                        #     executor.submit(self.status_checker2, stable_value2, status2, display_start_time2)
                            
                            #after getting the status , need to send it to the 
                        #   extracted_text1 = self.extract_text_from_roi(frame, roi1)
                        #   extracted_text2 = self.extract_text_from_roi(frame, roi2)
                        #   cv2.putText(frame, f'OCR1 Text: {extracted_text1} OCR1 Text: {extracted_text2}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                        #   numerical_values1 = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", extracted_text1)
                
                        #   if numerical_values1 and len(numerical_values1) != 0:
                        #      try:
                        #         strg = numerical_values1[0].replace(' ', '')
                        #         value = float(strg)
                        #      except IndexError:
                        #         value = 0.0
                        #      self.extracted_values1.append(value)
                            
                        #   numerical_values2 = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", extracted_text2)
                
                        #   if numerical_values2 and len(numerical_values2) != 0:
                        #      try:
                        #         strg = numerical_values2[0].replace(' ', '')
                        #         value = float(strg)
                        #      except IndexError:
                        #         value = 0.0
                        #      self.extracted_values2.append(value)

                        #   if len(self.extracted_values) >= 10:
                        #         last_values = self.extracted_values[-10:]
                        #         if all(v == last_values[0] and v != 0.0 for v in last_values):
                        #                 self.stable_value = last_values[0]
                        #                 self.display_start_time = time.time()
                        #                 self.extracted_values.clear()
                        #                 # print("unit values after:",self.add_test.unit_input.text())
                        #                 # print("unit values before:",self.add_test.unit_input)

                        #         # if self.unit_text == 'k' or self.unit_text == 'K':
                        #         if True:
                        #         #    lower_bound = lower_bound * 1000 
                        #         #    upper_bound = upper_bound * 1000
                        #            try:
                        #             # self.stable_value= self.stable_value 
                        #             if self.lower_bound <= self.stable_value <= self.upper_bound:
                        #             # if lower_bound <= self.stable_value <= upper_bound:
                                    
                        #                     self.value_status = "OK"
                        #             else:
                        #                     self.value_status = "Not Good"
                        #            except:
                        #             print("stable value is none")
                        #         elif self.unit_text == 'm' or self.unit_text == 'M': # units not yet implemented in the code 
                        #                 lower_bound = lower_bound * 1000000
                        #                 upper_bound = upper_bound * 1000000
                        #                 self.stable_value= self.stable_value *1000000
                        #                 if lower_bound <= self.stable_value <= upper_bound:
                        #                     self.value_status = "OK"
                        #                 else:
                        #                     self.value_status = "Not Good"
                        # #   else :
                        # #      self.display_start_time= time.time()
                        
                        #   if self.stable_value is not None and int(time.time() - self.display_start_time) < self.display_duration:
                        #             self.stable_v = self.stable_value
                        #             self.status_label= self.value_status
                        #             print("status label:",self.status_label)
                        #             self.value_updated.emit(self.stable_v, self.status_label)
                        #   elif self.stable_value is not None and int(time.time() - self.display_start_time) >= self.display_duration:
                        #             self.stable_value = None
                        #             self.stable_v = 0.0
                        #             print(" greater than 3 ")
                                    
                        #             self.status_label= ""
                        #             self.value_updated.emit(self.stable_v, self.status_label) # changed here 
                            self.new_frame.emit(frame)
                    else:
                        self.new_frame.emit(frame) #new code here 30-10 18:35
                        self.stable_value1 = None
                        self.stable_value2 = None
                        # self.stable_v = 0.0
                        stable_v  = 0.0
                        status_label= "INVALID"
                        # self.value_updated.emit(self.stable_v, self.status_label)
                        self.value_updated1.emit(stable_v, status_label)
                        self.value_updated2.emit(stable_v, status_label)

            else:
                print("exit without frame")
                self.camera_error.emit("Error: Could not read frame.")
                break

        self.capture.release()

    def stop(self):
        self._run_flag = False
        self.quit()
        self.wait()
class CameraThreadmeters_old(QThread): #changed before no/nc
    new_frame = pyqtSignal(np.ndarray)
    camera_error = pyqtSignal(str)
    value_updated = pyqtSignal(float, str)
    value_updated1 = pyqtSignal(float, str)
    value_updated2 = pyqtSignal(float, str)
    # from running_test_page import RunningTestPage
    def __init__(self,test,model,ocr1,ocr2):
        super().__init__()
        # self.add_test = AddTestDialog()
        # self.running_test_page = running_test_page
        # self.add_test.values_from_add_test.connect(self.get_add_test_values)
        self.value_status = ""
        self.value_status1 = ""
        self.value_status2 = ""
        
        self.extracted_values = []
        self.extracted_values1 = []
        self.extracted_values2 = []
        self.stable_value = None
        self.stable_value1 = None 
        self.stable_value2 = None 
        self.display_start_time = None
        self.display_start_time1 = None
        self.display_start_time2 = None

        self.display_duration = 3
        self._run_flag = True
        self.test_info = {}
        
        # self.model = YOLO(r"C:\Users\a\yolo13\ultralytics1\ultralytics\best_03_09_24.pt")
        # self.model = YOLO(r"D:\best_lux_meter_inc_2_11_24.pt")# newly added on 2_11_24
        # self.ocr1 = PaddleOCR(use_angle_cls=False, lang='en',show_log=False)
        # self.ocr2 = PaddleOCR(use_angle_cls=False, lang='en',show_log=False)
        self.model = model
        self.ocr1 = ocr1

        self.ocr2 = ocr2
    #     try:
    # # Retrieve and validate inputs
    #         value_text = self.add_test.value_input.text().strip()
    #         tolerance_text = self.add_test.tolerance_input.text().strip()

    #         if not value_text or not tolerance_text:
    #              raise ValueError("Empty input")

    # # Convert the inputs to float
    #         value = float(value_text)
    #         tolerance = float(tolerance_text)

    # # Calculate the lower and upper bounds
    #         self.lower_bound = value - (tolerance / 100) * value
    #         self.upper_bound = value + (tolerance / 100) * value
    #     except ValueError:
    #             print("Input Error", "Please enter valid numeric values.")
        # self.lower_bound = float(self.add_test.value_input.text()) - (float(self.add_test.tolerance_input.text()) / 100) * float(self.add_test.value_input.text())
        # self.upper_bound = float(self.add_test.value_input.text()) + (float(self.add_test.tolerance_input.text()) / 100) * float(self.add_test.value_input.text())
        # magnitude = 0.0
        # tolerance = 0.0
        # self.add_test.value_input = 0.0
        self.lower_bound = 0.0
        self.upper_bound = 0.0
        self.lower_bound1 = 0.0
        self.upper_bound1= 0.0
        self.lower_bound2 = 0.0
        self.upper_bound2 = 0.0
        self.stable_v= 0.0
        self.status_label = ""
        # self.value_text = 0.0
        # self.value_text = float(test.get('value1','N/A'))

        # self.tolerance_text =float(test.get('tolerance1','N/A'))
        # self.unit_text = test.get(test.get('unit1','N/A'))
        # self.lower_bound = self.value_text - (self.tolerance_text / 100) * self.value_text
        # self.upper_bound = self.value_text + (self.tolerance_text / 100) * self.value_text
        # self.value_text = float(test.get('value','N/A'))

        # self.tolerance_text =float(test.get('tolerance','N/A'))
        self.model_values = test.get('Model','N/A')
        print("model name :",self.model_values)
        if self.model_values == "DoubleMeters":
            self.value_text1 = float(test.get('value1','N/A'))

            self.tolerance_text1 =float(test.get('tolerance1','N/A'))
            self.floating_text1 = test.get('floatingPoint1','N/A')
            self.value_text2 = float(test.get('value2','N/A'))

            self.tolerance_text2 =float(test.get('tolerance2','N/A'))
            self.floating_text2 = test.get('floatingPoint2','N/A')
        # self.unit_text = test.get(test.get('unit','N/A'))
        # self.lower_bound = self.value_text - (self.tolerance_text / 100) * self.value_text
        # self.upper_bound = self.value_text + (self.tolerance_text / 100) * self.value_text
            self.lower_bound1 = self.value_text1 - (self.tolerance_text1 / 100) * self.value_text1
            self.upper_bound1 = self.value_text1 + (self.tolerance_text1 / 100) * self.value_text1
            self.lower_bound2 = self.value_text2 - (self.tolerance_text2 / 100) * self.value_text2
            self.upper_bound2 = self.value_text2 + (self.tolerance_text2 / 100) * self.value_text2
        else:
            self.value_text1 = float(test.get('value1','N/A'))

            self.tolerance_text1 =float(test.get('tolerance1','N/A'))
            self.floating_text1 = test.get('floatingPoint1','N/A')
            self.lower_bound1 = self.value_text1 - (self.tolerance_text1 / 100) * self.value_text1
            self.upper_bound1 = self.value_text1 + (self.tolerance_text1 / 100) * self.value_text1
            
    # def get_add_test_values(self,value,tolerance,unit):
    #         self.value_text = value
    #         self.tolerance_text = tolerance
    #         self.unit_text = unit
    #         self.lower_bound = float(value - (tolerance / 100) * value)
    #         self.upper_bound = float(value + (tolerance / 100) * value)
    #         print("add test values :: {self.value_text},{self.tolerance_text},{self.unit_text}")
    def detect_display_screen(self, results, frame): # for single meter display 
        if results[0].obb.xyxy.shape[0] > 0:
            x1, y1, x2, y2 = map(int, results[0].obb.xyxy[0])
            height, width, _ = frame.shape
            x1 = max(0, min(x1, width))
            y1 = max(0, min(y1, height))
            x2 = max(0, min(x2, width))
            y2 = max(0, min(y2, height))
            roi = (x1, y1, x2, y2)
        else:
            roi = (100, 100, 400, 200)
        return roi
    def detect_display_screen_meters(self, results, frame):#for 2 meter display
        if results[0].obb.xyxy.shape[0] > 0:
            try:

                x11, y11, x21, y21 = map(int, results[0].obb.xyxy[0])
                x12, y12, x22, y22 = map(int, results[0].obb.xyxy[1])
            except ValueError:
                print("Value Error / Empty ")
            height, width, _ = frame.shape
            x11 = max(0, min(x11, width))
            y11 = max(0, min(y11, height))
            x21 = max(0, min(x21, width))
            y21 = max(0, min(y21, height))
            roi1 = (x11, y11, x21, y21) # roi for first BB
            x12 = max(0, min(x12, width))
            y12 = max(0, min(y12, height))
            x22 = max(0, min(x22, width))
            y22 = max(0, min(y22, height))
            roi2 = (x12, y12, x22, y22) # roi for the second BB
        else:
            roi1 = (100, 100, 400, 200) # default random co-ordinates for the detected BB
            roi2 = (100, 100, 400 ,200)
        return roi1,roi2
    def extract_text_from_roi_1_rev(self, frame, roi):
        x1, y1, x2, y2 = roi
        cropped_image = frame[y1:y2, x1:x2]
        gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        try:
         ocr_result = self.ocr1.ocr(gray_image)
        except ValueError:
            print("Ocr text empty for the moment")
        extracted_text_lines = []
        if ocr_result and ocr_result[0]:
            for line in ocr_result:
                for word in line:
                    text, confidence = word[1]
                    extracted_text_lines.append(text)

        extracted_text = ' '.join(extracted_text_lines)
        cv2.putText(frame, f'OCR1 Text: {extracted_text}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
        if self.floating_text1 == 'y':
            # print(f"floating point text 1 : {self.floating_text1}")
            numerical_values = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*", extracted_text) # |[-+]?\d*\.\d+\s*(?i)(Mn|Kn) finds Mn or Kn
        else:
            numerical_values = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", extracted_text)
            
        if numerical_values and len(numerical_values) != 0:
             try:
                            strg = numerical_values[0].replace(' ', '')
                            value = float(strg)
             except IndexError:
                 value = 0.0
             self.extracted_values1.append(value)

        # value = float(re.findall(r"\d+\.?\d*", text)[0]) if re.findall(r"\d+\.?\d*", text) else 0.0
        # self.extracted_values.append(value)

        # Check if we have 10 or more readings for stability check
        if len(self.extracted_values1) >= 10:
            last_values = self.extracted_values1[-10:]
            if all(v == last_values[0] and v != 0.0 for v in last_values):
                self.stable_value1 = last_values[0]
                self.display_start_time1 = time.time()
                self.extracted_values1.clear()
                
                if True:
                            #    lower_bound = lower_bound * 1000 
                            #    upper_bound = upper_bound * 1000
                    try:
                                # self.stable_value= self.stable_value 
                       if self.lower_bound1 <= self.stable_value1 <= self.upper_bound1:
                                # if lower_bound <= self.stable_value <= upper_bound:
                                
                           self.value_status1 = "OK"
                       else:
                           self.value_status1 = "Not Good"
                    except:
                           print("stable value is none")
                # Convert stable value based on unit text
                # if self.unit_text.lower() == 'k':
                #     stable_value *= 1000
                # elif self.unit_text.lower() == 'm':
                #     stable_value *= 1000000

                # Determine value status based on bounds
                # if self.lower_bound <= stable_value <= self.upper_bound:
                #     value_status = "OK"
                # else:
                #     value_status = "Not Good"
        if self.stable_value1 is not None and int(time.time() - self.display_start_time1) < self.display_duration:
                    stable_v = self.stable_value1
                    status_label= self.value_status1
                    # print(f"values1t = {self.stable_value1},{status_label}")
                    self.value_updated1.emit(stable_v,status_label)
        elif self.stable_value1 is not None and int(time.time() - self.display_start_time1) >= self.display_duration:
                    self.stable_value1 = None
                    stable_v = 0.0
                    # print(" greater than 3 ")
                    status_label= ""
                    # print(f"values1f = {self.stable_value1},{status_label}")
                    self.value_updated1.emit(stable_v, status_label)
        #         return stable_value, value_status, display_start_time
        # return None, "", None
        # return extracted_text
    def extract_text_from_roi_2_rev(self, frame, roi):
        x1, y1, x2, y2 = roi
        cropped_image = frame[y1:y2, x1:x2]
        gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        try:
         ocr_result = self.ocr2.ocr(gray_image)
        except ValueError:
            print("Ocr text empty for the moment")
        extracted_text_lines = []
        if ocr_result and ocr_result[0]:
            for line in ocr_result:
                for word in line:
                    text, confidence = word[1]
                    extracted_text_lines.append(text)

        extracted_text = ' '.join(extracted_text_lines)
        cv2.putText(frame, f'OCR2 Text: {extracted_text}', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
        # numerical_values = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", extracted_text)
        if self.floating_text2 == 'y':
            print(f"floating point text 1 : {self.floating_text2}")
            numerical_values = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*", extracted_text)
        else:
            numerical_values = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", extracted_text)
        if numerical_values and len(numerical_values) != 0:
             try:
                            strg = numerical_values[0].replace(' ', '')
                            value = float(strg)
             except IndexError:
                 value = 0.0
             self.extracted_values2.append(value)

        # value = float(re.findall(r"\d+\.?\d*", text)[0]) if re.findall(r"\d+\.?\d*", text) else 0.0
        # self.extracted_values.append(value)

        # Check if we have 10 or more readings for stability check
        if len(self.extracted_values2) >= 10:
            last_values = self.extracted_values2[-10:]
            if all(v == last_values[0] and v != 0.0 for v in last_values):
                self.stable_value2 = last_values[0]
                self.display_start_time2 = time.time()
                self.extracted_values2.clear()
                
                if True:
                            #    lower_bound = lower_bound * 1000 
                            #    upper_bound = upper_bound * 1000
                    try:
                                # self.stable_value= self.stable_value 
                       if self.lower_bound2 <= self.stable_value2 <= self.upper_bound2:
                                # if lower_bound <= self.stable_value <= upper_bound:
                                
                           self.value_status2 = "OK"
                       else:
                           self.value_status2 = "Not Good"
                    except:
                           print("stable value is none")
                # Convert stable value based on unit text
                # if self.unit_text.lower() == 'k':
                #     stable_value *= 1000
                # elif self.unit_text.lower() == 'm':
                #     stable_value *= 1000000

                # Determine value status based on bounds
                # if self.lower_bound <= stable_value <= self.upper_bound:
                #     value_status = "OK"
                # else:
                #     value_status = "Not Good"
        if self.stable_value2 is not None and int(time.time() - self.display_start_time2) < self.display_duration:
                    stable_v = self.stable_value2
                    status_label= self.value_status2
                    # print(f"values1t = {self.stable_value2},{status_label}")
                    self.value_updated2.emit(stable_v,status_label)
        elif self.stable_value2 is not None and int(time.time() - self.display_start_time2) >= self.display_duration:
                    self.stable_value2 = None
                    stable_v = 0.0
                    # print(" greater than 3 ")
                    status_label= ""
                    # print(f"values1f = {self.stable_value2},{status_label}") # for testing 
                    self.value_updated2.emit(stable_v, status_label)
    def extract_text_from_roi_1(self, frame, roi):
        x1, y1, x2, y2 = roi
        cropped_image = frame[y1:y2, x1:x2]
        gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        try:
         ocr_result = self.ocr1.ocr(gray_image)
        except ValueError:
            print("Ocr text empty for the moment")
        extracted_text_lines = []
        if ocr_result and ocr_result[0]:
            for line in ocr_result:
                for word in line:
                    text, confidence = word[1]
                    extracted_text_lines.append(text)

        extracted_text = ' '.join(extracted_text_lines)
        return extracted_text
    def extract_text_from_roi_2(self, frame, roi):
        x1, y1, x2, y2 = roi
        cropped_image = frame[y1:y2, x1:x2]
        gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        try:
         ocr_result = self.ocr2.ocr(gray_image)
        except ValueError:
            print("Ocr text empty for the moment")
        extracted_text_lines = []
        if ocr_result and ocr_result[0]:
            for line in ocr_result:
                for word in line:
                    text, confidence = word[1]
                    extracted_text_lines.append(text)

        extracted_text = ' '.join(extracted_text_lines)
        return extracted_text
    def process_single_text(self, text): #newly added
        """Processes a single extracted text value to determine stability and status."""
        # extracted_values = []
        numerical_values = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", text)
            
        if numerical_values and len(numerical_values) != 0:
             try:
                            strg = numerical_values[0].replace(' ', '')
                            value = float(strg)
             except IndexError:
                 value = 0.0
             self.extracted_values.append(value)

        # value = float(re.findall(r"\d+\.?\d*", text)[0]) if re.findall(r"\d+\.?\d*", text) else 0.0
        # self.extracted_values.append(value)

        # Check if we have 10 or more readings for stability check
        if len(self.extracted_values) >= 10:
            last_values = self.extracted_values[-10:]
            if all(v == last_values[0] and v != 0.0 for v in last_values):
                stable_value = last_values[0]
                display_start_time = time.time()
                self.extracted_values.clear()
                
                if True:
                            #    lower_bound = lower_bound * 1000 
                            #    upper_bound = upper_bound * 1000
                    try:
                                # self.stable_value= self.stable_value 
                       if self.lower_bound <= stable_value <= self.upper_bound:
                                # if lower_bound <= self.stable_value <= upper_bound:
                                
                           value_status = "OK"
                       else:
                           value_status = "Not Good"
                    except:
                           print("stable value is none")
                # Convert stable value based on unit text
                # if self.unit_text.lower() == 'k':
                #     stable_value *= 1000
                # elif self.unit_text.lower() == 'm':
                #     stable_value *= 1000000

                # Determine value status based on bounds
                # if self.lower_bound <= stable_value <= self.upper_bound:
                #     value_status = "OK"
                # else:
                #     value_status = "Not Good"

                return stable_value, value_status, display_start_time
        return None, "", None
    def status_checker1(self,stable_value,status,display_start_time):
        print("reached status checker1")
        if stable_value is not None and int(time.time() - display_start_time) < self.display_duration:
                    stable_v = stable_value
                    status_label= value_status
                    print(f"values1t = {stable_value},{status_label}")
                    self.value_updated1.emit(stable_v,status_label)
        elif stable_value is not None and int(time.time() - self.display_start_time) >= self.display_duration:
                    stable_value = None
                    stable_v = 0.0
                    # print(" greater than 3 ")
                    status_label= ""
                    print(f"values1f = {stable_value},{status_label}")
                    self.value_updated1.emit(stable_v, status_label)
    def status_checker2(self,stable_value,status,display_start_time):
        print("reached status checker2")
        if stable_value is not None and int(time.time() - display_start_time) < self.display_duration:
                    stable_v = stable_value
                    status_label= value_status
                    print(f"values2t = {stable_value},{status_label}")
                    self.value_updated2.emit(stable_v,status_label)
        elif stable_value is not None and int(time.time() - self.display_start_time) >= self.display_duration:
                    stable_value = None
                    stable_v = 0.0
                    # print(" greater than 3 ")
                    status_label= ""
                    print(f"values2f = {stable_value},{status_label}")
                    self.value_updated2.emit(stable_v, status_label)                
    def process_extracted_text(self, text1, text2, frame): #newly added

        # Use ThreadPoolExecutor to process both texts concurrently
        with ThreadPoolExecutor() as executor:
            future1 = executor.submit(self.process_single_text, text1)
            future2 = executor.submit(self.process_single_text, text2)

            # Retrieve results for both texts
            stable_value1, status1, display_start_time1 = future1.result()
            print(f"stable1={stable_value1}/n")
            stable_value2, status2, display_start_time2 = future2.result()
            print(f"stable1={stable_value2}")
        return stable_value1, status1, display_start_time1,stable_value2, status2, display_start_time2
        # with ThreadPoolExecutor() as executor: # newly added 2-11-24
        #     var1 = executor.submit(self.status_checker,stable_value1,status1,display_start_time1)
        #     var2 = executor.submit(self.status_checker,stable_value2,status2,display_start_time2)
        
    def run(self):
        self.capture = cv2.VideoCapture(0)
        # self.value_text= float(test.get('value', 'N/A'))
        # print(f"from running page to camera thread value pass {self.value_text} , {self.tolerance_text},{self.unit_text}")
        # print(f'list of values from running test = {self.running_test_page.value},{self.running_test_page.tolerance}')
        # if self.get_add_test_values():
        #     print("values received from signal")
        # if not self.capture.isOpened():
        #     self.camera_error.emit("Error: Could not open camera.")
        #     return
        # if self.add_test.exec_() == QDialog.Accepted:
        #     test_info = self.add_test.get_inputs()
        #     print(test_info)
        # else:
        #     print("didnt went past add test")
        # frame_counter = 0
        while self.capture.isOpened() and self._run_flag:
            ret, frame = self.capture.read()
            
            # try:
    # Retrieve and validate inputs

            #  value_text = self.add_test.get_inputs().values()   
            #  print(value_text)
            #  tolerance_text = self.add_test.get_input().values()

            #  value_text = self.add_test.value_input.text().strip() #   input value = preset value
            #  tolerance_text = self.add_test.tolerance_input.text().strip() # tolerance value 
            #  print()
            #  if not self.value_text or not self.tolerance_text:
            #      raise ValueError("Empty input")

    # Convert the inputs to float
            #  value_new = float(self.value_text)
            #  tolerance_new = float(self.tolerance_text)

    # Calculate the lower and upper bounds
             
            # except ValueError:
            #     print("Input Error", "Please enter valid numeric values.")
            if ret:
                # print("frame entered ")
                result=self.model.predict(frame,conf=0.65)
                if self.model_values== "DoubleMeters":
                    if len(result[0].obb.xyxy.tolist()) == 2: # for 2 meter display 
                            roi1,roi2= self.detect_display_screen_meters(result, frame)
                            #if roi1 < roi2: # left screen is meter 1 and right screen is meter 2 , logic : checking x co ordinate values of the two roi and choosing text1 corresponding to roi1<roi2 or vice-versa

                            cv2.rectangle(frame, (roi1[0], roi1[1]), (roi1[2], roi1[3]), (0, 255, 0), 2)
                            cv2.rectangle(frame, (roi2[0], roi2[1]), (roi2[2], roi2[3]), (0, 255, 0), 2)
                        
                            # if text is empty  (try and except )
                            if roi1[0] < roi2[0]:
                                with ThreadPoolExecutor() as executor:
                                    future1 = executor.submit(self.extract_text_from_roi_1_rev, frame, roi1)
                                    future2 = executor.submit(self.extract_text_from_roi_2_rev, frame, roi2)
                                    try:
                                        future1.result()
                                        future2.result()
                                    except ValueError:
                                        print("Threading not executed properly :(")
                            else:
                                with ThreadPoolExecutor() as executor:
                                    future1 = executor.submit(self.extract_text_from_roi_1_rev, frame, roi2)
                                    future2 = executor.submit(self.extract_text_from_roi_2_rev, frame, roi1)
                                    try:
                                        future1.result()
                                        future2.result()
                                    except ValueError:
                                        print("Threading not executed properly :(")
                            
                        #   cv2.putText(frame, f'OCR1 Text: {extracted_text1},OCR2 Text: {extracted_text2}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                            #__________________working fine till here__________________________
                        #   stable_value1, status1, display_start_time1,stable_value2, status2, display_start_time2=self.process_extracted_text(extracted_text1, extracted_text2, frame)
                        #   print(f"stable1={stable_value1},stable2= {stable_value2}")
                        #   with ThreadPoolExecutor() as executor:
                        #     executor.submit(self.status_checker1, stable_value1, status1, display_start_time1)
                        #     executor.submit(self.status_checker2, stable_value2, status2, display_start_time2)
                            
                            #after getting the status , need to send it to the 
                        #   extracted_text1 = self.extract_text_from_roi(frame, roi1)
                        #   extracted_text2 = self.extract_text_from_roi(frame, roi2)
                        #   cv2.putText(frame, f'OCR1 Text: {extracted_text1} OCR1 Text: {extracted_text2}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                        #   numerical_values1 = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", extracted_text1)
                
                        #   if numerical_values1 and len(numerical_values1) != 0:
                        #      try:
                        #         strg = numerical_values1[0].replace(' ', '')
                        #         value = float(strg)
                        #      except IndexError:
                        #         value = 0.0
                        #      self.extracted_values1.append(value)
                            
                        #   numerical_values2 = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", extracted_text2)
                
                        #   if numerical_values2 and len(numerical_values2) != 0:
                        #      try:
                        #         strg = numerical_values2[0].replace(' ', '')
                        #         value = float(strg)
                        #      except IndexError:
                        #         value = 0.0
                        #      self.extracted_values2.append(value)

                        #   if len(self.extracted_values) >= 10:
                        #         last_values = self.extracted_values[-10:]
                        #         if all(v == last_values[0] and v != 0.0 for v in last_values):
                        #                 self.stable_value = last_values[0]
                        #                 self.display_start_time = time.time()
                        #                 self.extracted_values.clear()
                        #                 # print("unit values after:",self.add_test.unit_input.text())
                        #                 # print("unit values before:",self.add_test.unit_input)

                        #         # if self.unit_text == 'k' or self.unit_text == 'K':
                        #         if True:
                        #         #    lower_bound = lower_bound * 1000 
                        #         #    upper_bound = upper_bound * 1000
                        #            try:
                        #             # self.stable_value= self.stable_value 
                        #             if self.lower_bound <= self.stable_value <= self.upper_bound:
                        #             # if lower_bound <= self.stable_value <= upper_bound:
                                    
                        #                     self.value_status = "OK"
                        #             else:
                        #                     self.value_status = "Not Good"
                        #            except:
                        #             print("stable value is none")
                        #         elif self.unit_text == 'm' or self.unit_text == 'M': # units not yet implemented in the code 
                        #                 lower_bound = lower_bound * 1000000
                        #                 upper_bound = upper_bound * 1000000
                        #                 self.stable_value= self.stable_value *1000000
                        #                 if lower_bound <= self.stable_value <= upper_bound:
                        #                     self.value_status = "OK"
                        #                 else:
                        #                     self.value_status = "Not Good"
                        # #   else :
                        # #      self.display_start_time= time.time()
                        
                        #   if self.stable_value is not None and int(time.time() - self.display_start_time) < self.display_duration:
                        #             self.stable_v = self.stable_value
                        #             self.status_label= self.value_status
                        #             print("status label:",self.status_label)
                        #             self.value_updated.emit(self.stable_v, self.status_label)
                        #   elif self.stable_value is not None and int(time.time() - self.display_start_time) >= self.display_duration:
                        #             self.stable_value = None
                        #             self.stable_v = 0.0
                        #             print(" greater than 3 ")
                                    
                        #             self.status_label= ""
                        #             self.value_updated.emit(self.stable_v, self.status_label) # changed here 
                            self.new_frame.emit(frame)
                    else:
                        self.new_frame.emit(frame) #new code here 30-10 18:35
                        self.stable_value1 = None
                        self.stable_value2 = None
                        # self.stable_v = 0.0
                        stable_v  = 0.0
                        status_label= "INVALID"
                        # self.value_updated.emit(self.stable_v, self.status_label)
                        self.value_updated1.emit(stable_v, status_label)
                        self.value_updated2.emit(stable_v, status_label)
                 # if frame_counter % 3 == 0:  # Process every third frame
                # self.new_frame.emit(frame)
                # else:
                # frame_counter += 1
                else:
                    if len(result[0].obb.xyxy.tolist()) == 1: # for 2 meter display 
                            roi1 = self.detect_display_screen(result, frame)
                            #if roi1 < roi2: # left screen is meter 1 and right screen is meter 2 , logic : checking x co ordinate values of the two roi and choosing text1 corresponding to roi1<roi2 or vice-versa

                            cv2.rectangle(frame, (roi1[0], roi1[1]), (roi1[2], roi1[3]), (0, 255, 0), 2)
                            
                        
                            # if text is empty  (try and except )
                            
                            with ThreadPoolExecutor() as executor:
                                future1 = executor.submit(self.extract_text_from_roi_1_rev, frame, roi1)
                                # future2 = executor.submit(self.extract_text_from_roi_2_rev, frame, roi2)
                                try:
                                    future1.result()
                                    
                                except ValueError:
                                    print("Threading not executed properly :(")
                            
                            
                        #   cv2.putText(frame, f'OCR1 Text: {extracted_text1},OCR2 Text: {extracted_text2}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                            #__________________working fine till here__________________________
                        #   stable_value1, status1, display_start_time1,stable_value2, status2, display_start_time2=self.process_extracted_text(extracted_text1, extracted_text2, frame)
                        #   print(f"stable1={stable_value1},stable2= {stable_value2}")
                        #   with ThreadPoolExecutor() as executor:
                        #     executor.submit(self.status_checker1, stable_value1, status1, display_start_time1)
                        #     executor.submit(self.status_checker2, stable_value2, status2, display_start_time2)
                            
                            #after getting the status , need to send it to the 
                        #   extracted_text1 = self.extract_text_from_roi(frame, roi1)
                        #   extracted_text2 = self.extract_text_from_roi(frame, roi2)
                        #   cv2.putText(frame, f'OCR1 Text: {extracted_text1} OCR1 Text: {extracted_text2}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                        #   numerical_values1 = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", extracted_text1)
                
                        #   if numerical_values1 and len(numerical_values1) != 0:
                        #      try:
                        #         strg = numerical_values1[0].replace(' ', '')
                        #         value = float(strg)
                        #      except IndexError:
                        #         value = 0.0
                        #      self.extracted_values1.append(value)
                            
                        #   numerical_values2 = re.findall(r"[-+]?\d*\.\d+|\d+\s*\.\s*\d+|\d+\s+\d*\.\d+\s*\d*|[-+]?\d+", extracted_text2)
                
                        #   if numerical_values2 and len(numerical_values2) != 0:
                        #      try:
                        #         strg = numerical_values2[0].replace(' ', '')
                        #         value = float(strg)
                        #      except IndexError:
                        #         value = 0.0
                        #      self.extracted_values2.append(value)

                        #   if len(self.extracted_values) >= 10:
                        #         last_values = self.extracted_values[-10:]
                        #         if all(v == last_values[0] and v != 0.0 for v in last_values):
                        #                 self.stable_value = last_values[0]
                        #                 self.display_start_time = time.time()
                        #                 self.extracted_values.clear()
                        #                 # print("unit values after:",self.add_test.unit_input.text())
                        #                 # print("unit values before:",self.add_test.unit_input)

                        #         # if self.unit_text == 'k' or self.unit_text == 'K':
                        #         if True:
                        #         #    lower_bound = lower_bound * 1000 
                        #         #    upper_bound = upper_bound * 1000
                        #            try:
                        #             # self.stable_value= self.stable_value 
                        #             if self.lower_bound <= self.stable_value <= self.upper_bound:
                        #             # if lower_bound <= self.stable_value <= upper_bound:
                                    
                        #                     self.value_status = "OK"
                        #             else:
                        #                     self.value_status = "Not Good"
                        #            except:
                        #             print("stable value is none")
                        #         elif self.unit_text == 'm' or self.unit_text == 'M': # units not yet implemented in the code 
                        #                 lower_bound = lower_bound * 1000000
                        #                 upper_bound = upper_bound * 1000000
                        #                 self.stable_value= self.stable_value *1000000
                        #                 if lower_bound <= self.stable_value <= upper_bound:
                        #                     self.value_status = "OK"
                        #                 else:
                        #                     self.value_status = "Not Good"
                        # #   else :
                        # #      self.display_start_time= time.time()
                        
                        #   if self.stable_value is not None and int(time.time() - self.display_start_time) < self.display_duration:
                        #             self.stable_v = self.stable_value
                        #             self.status_label= self.value_status
                        #             print("status label:",self.status_label)
                        #             self.value_updated.emit(self.stable_v, self.status_label)
                        #   elif self.stable_value is not None and int(time.time() - self.display_start_time) >= self.display_duration:
                        #             self.stable_value = None
                        #             self.stable_v = 0.0
                        #             print(" greater than 3 ")
                                    
                        #             self.status_label= ""
                        #             self.value_updated.emit(self.stable_v, self.status_label) # changed here 
                            self.new_frame.emit(frame)
                    else:
                        self.new_frame.emit(frame) #new code here 30-10 18:35
                        self.stable_value1 = None
                        self.stable_value2 = None
                        # self.stable_v = 0.0
                        stable_v  = 0.0
                        status_label= "INVALID"
                        # self.value_updated.emit(self.stable_v, self.status_label)
                        self.value_updated1.emit(stable_v, status_label)
                        self.value_updated2.emit(stable_v, status_label)

            else:
                print("exit without frame")
                self.camera_error.emit("Error: Could not read frame.")
                break

        self.capture.release()

    def stop(self):
        self._run_flag = False
        self.quit()
        self.wait()