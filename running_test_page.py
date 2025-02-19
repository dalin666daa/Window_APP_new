import sys
import pyttsx3
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QProgressBar, QMessageBox, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from camera_thread import CameraThreadmeters
import cv2
import numpy as np
from ultralytics import YOLO
from paddleocr import PaddleOCR
class RunningTestPage(QFrame):
    def __init__(self, test, back_callback):
        super().__init__()
        self.model = YOLO(r"D:\best_lux_meter_inc_2_11_24.pt")# newly added on 2_11_24
        self.result=self.model.predict(r"C:\Users\a\yolo13\ultralytics1\image78.jpg",conf=0.65) # executing the model using a test image to load faster in camera 
        self.ocr1 = PaddleOCR(use_angle_cls=False, lang='en',show_log=False)
        self.ocr2 = PaddleOCR(use_angle_cls=False, lang='en',show_log=False)
        self.setStyleSheet("background-color: #2E2E2E; border-radius: 10px; color: #FFFFFF;")
        self.setGeometry(100, 100, 1200, 600)

        # self.stabilization_time = test.get('stabilization_time', 'N/A')
        self.status = test.get('status', 'N/A')  #need to update the status 

        self.engine = pyttsx3.init()

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 10, 0)
        self.main_layout.setSpacing(10)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 5px solid #00BFFF; border-radius: 10px;")
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setMinimumSize(800, 400)
        self.image_label.setScaledContents(True)
        self.main_layout.addWidget(self.image_label, stretch=6)
        self.value = 0.0 
        self.tolerance = 0.0 
        self.unit = ""
        self.camera_running = False
        
        self.camera_thread = CameraThreadmeters(test,self.model,self.ocr1,self.ocr2) #CameraThread before , CameraThreadLux ,
        self.camera_thread.new_frame.connect(self.update_image)
        self.camera_thread.camera_error.connect(self.handle_camera_error)
        # self.camera_thread.value_updated.connect(self.update_value_status)
        self.camera_thread.value_updated1.connect(self.update_value_status1)
        self.camera_thread.value_updated2.connect(self.update_value_status2)
        self.camera_thread.value_updated3.connect(self.update_value_status_no_nc)
        self.card = self.create_card_layout_meteres(test, back_callback) #changed here 
        self.main_layout.addWidget(self.card, alignment=Qt.AlignRight, stretch=3)
        
        
        
        
        
        
        
        
        self.showMaximized()
    
    
    def create_card_layout(self, test, back_callback):
        card = QFrame()
        card.setStyleSheet("background-color: #3B3B3B; border-radius: 10px; padding: 20px; color: #FFFFFF;")
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(0, 0, 0, 0)
        
        tester = test.get('tester', 'N/A')
        value = float(test.get('value', 'N/A'))
        unit = test.get('unit', 'N/A')
        tolerance = float(test.get('tolerance', 'N/A'))
        # print(f'current test values : {value},{tolerance},{unit}')
        # self.status = test.get('status', self.camera_thread.status_label)
        # status = test.camera_thread.stable_value
        tester_label = QLabel(f"<h1 style='color: #00BFFF;'>{tester}</h1>")
        tester_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(tester_label)

        # Create a box for values
        value_box = QFrame()
        value_box.setStyleSheet("background-color: #4A4A4A; border-radius: 10px; padding: 10px;")
        value_box_layout = QVBoxLayout()

        # info_labels = [
        #     f"<b>Preset Value:</b> {value}", # here 
        #     f"<b>Actual Value:</b> {self.camera_thread.stable_v}",
        #     f"<b>Stabilization Time:</b> {status}",
        # ]

        # for info in info_labels:
        #     label = QLabel(info)
        #     label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
        #     value_box_layout.addWidget(label)
        info_labels = [
                    f"<b>Preset Value:</b> {value}",
                    f"<b>Actual Value:</b> {self.camera_thread.stable_v}",
                    f"<b>Tolerance Value(%):</b> {tolerance}",
                        
                        ]

        for i, info in enumerate(info_labels):
             label = QLabel(info)
             label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
             if i == 1:  # This is the "Actual Value" label
                 label.setObjectName("actual_value_label")  # Set object name for actual value
             value_box_layout.addWidget(label)

        value_box.setLayout(value_box_layout)
        card_layout.addWidget(value_box)

        # Create a separate box for Status
        status_box = QFrame()
        status_box.setObjectName("status_box") # obj name for status_box 1 
        # Set the background color based on the status
        if self.status.lower() == 'OK':
            status_box.setStyleSheet("background-color: #28A745; border-radius: 10px; padding: 10px;")
        elif self.status.lower() == 'Not Good':
            status_box.setStyleSheet("background-color: #DC3545; border-radius: 10px; padding: 10px;")
        else:
            status_box.setStyleSheet("background-color: #FFC107; border-radius: 10px; padding: 10px;")  # Yellow for undefined status
        
        status_layout = QVBoxLayout()
        # status_label = QLabel(f"<h1><b>Status:</b> {status}</h1>")
        # status_label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
        # status_layout.addWidget(status_label)
        status_label = QLabel(f"<h1><b>Status:</b> {self.status}</h1>")
        status_label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
        status_label.setObjectName("status_label")  # Set object name for the status label
        status_layout.addWidget(status_label)

        status_box.setLayout(status_layout)
        
        card_layout.addWidget(status_box)

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setStyleSheet("QProgressBar { border: 2px solid #00BFFF; border-radius: 10px; }")
        card_layout.addWidget(self.progress_bar)

        # Camera Button
        self.camera_button = QPushButton("Camera Enable")
        self.camera_button.setStyleSheet(""" 
            QPushButton {
                background-color: #00BFFF; 
                color: white; 
                border-radius: 10px; 
                padding: 10px; 
                font-size: 16px; 
            } 
            QPushButton:hover { 
                background-color: #008FBF; 
            } 
        """)
        self.camera_button.clicked.connect(self.toggle_camera)
        card_layout.addWidget(self.camera_button, alignment=Qt.AlignBottom)

        # Back Button
        back_button = QPushButton("Back to Tests")
        back_button.setStyleSheet(""" 
            QPushButton { 
                background-color: #FF6F61; 
                color: white; 
                border-radius: 10px; 
                padding: 10px; 
                font-size: 16px; 
            } 
            QPushButton:hover { 
                background-color: #BF5B4C; 
            } 
        """)
        back_button.clicked.connect(back_callback)  # Connect to the back callback
        card_layout.addWidget(back_button, alignment=Qt.AlignBottom)

        card.setLayout(card_layout)
        card.setMinimumWidth(400)
        return card

    def create_card_layout_meteres(self, test, back_callback):
        card = QFrame()
        card.setStyleSheet("background-color: #3B3B3B; border-radius: 10px; padding: 20px; color: #FFFFFF;")
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(0, 0, 0, 0)
        modelcombo = test.get('Model','N/A')
        # print("model name :",modelcombo)
        if modelcombo == "DoubleMeters":

            tester = test.get('tester1', 'N/A')
            value1 = float(test.get('value1', 'N/A'))
            unit1 = test.get('unit1', 'N/A')
            tolerance1 = float(test.get('tolerance1', 'N/A'))
            value2 = float(test.get('value2', 'N/A'))
            unit2 = test.get('unit2', 'N/A')
            tolerance2 = float(test.get('tolerance2', 'N/A'))
            # print(f"Recived values at running test page from add_test : {value1},{tolerance1},{value2},{tolerance2}")
        else : 
            tester = test.get('tester1', 'N/A')
            value1 = float(test.get('value1', 'N/A'))
            unit1 = test.get('unit1', 'N/A')
            tolerance1 = float(test.get('tolerance1', 'N/A'))
        # print(f'current test values : {value},{tolerance},{unit}')
        # self.status = test.get('status', self.camera_thread.status_label)
        # status = test.camera_thread.stable_value
        tester_label = QLabel(f"<h1 style='color: #00BFFF;'>{tester}</h1>")
        tester_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(tester_label)
        if modelcombo == "DoubleMeters":

        # Create a box for values
                value_box1 = QFrame()
                value_box1.setStyleSheet("background-color: #4A4A4A; border-radius: 10px; padding: 10px;")
                value_box_layout1 = QVBoxLayout()

                # info_labels = [
                #     f"<b>Preset Value:</b> {value}", # here 
                #     f"<b>Actual Value:</b> {self.camera_thread.stable_v}",
                #     f"<b>Stabilization Time:</b> {status}",
                # ]

                # for info in info_labels:
                #     label = QLabel(info)
                #     label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
                #     value_box_layout.addWidget(label)
                info_labels_1 = [
                            f"<b>Preset Value (1):</b> {value1}",
                            f"<b>Actual Value (1):</b> {self.camera_thread.stable_v}", #need to change here 
                            f"<b>Tolerance Value(%) (1):</b> {tolerance1}",
                                
                                ]
                info_labels_2= [
                            f"<b>Preset Value (2):</b> {value2}",
                            f"<b>Actual Value (2):</b> {self.camera_thread.stable_v}",  #need to change here
                            f"<b>Tolerance Value(%) (2):</b> {tolerance2}",
                                
                                ]
                for i, info in enumerate(info_labels_1):
                    label = QLabel(info)
                    label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
                    if i == 1:  # This is the "Actual Value" label
                        label.setObjectName("actual_value_label1")  # actual_value_label_here
                    value_box_layout1.addWidget(label)
                value_box1.setLayout(value_box_layout1)
                card_layout.addWidget(value_box1)
                # Create a separate box for Status
                status_box = QFrame()
                status_box.setObjectName("status_box1")
                # Set the background color based on the status
                if self.status.lower() == 'OK':
                    status_box.setStyleSheet("background-color: #28A745; border-radius: 10px; padding: 10px;")
                elif self.status.lower() == 'Not Good':
                    status_box.setStyleSheet("background-color: #DC3545; border-radius: 10px; padding: 10px;")
                else:
                    status_box.setStyleSheet("background-color: #FFC107; border-radius: 10px; padding: 10px;")  # Yellow for undefined status
                
                status_layout = QVBoxLayout()
                # status_label = QLabel(f"<h1><b>Status:</b> {status}</h1>")
                # status_label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
                # status_layout.addWidget(status_label)
                status_label = QLabel(f"<h1><b>Status:</b> {self.status}</h1>")
                status_label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
                status_label.setObjectName("status_label1")  # Set object name for the status label
                status_layout.addWidget(status_label)

                status_box.setLayout(status_layout)
                
                card_layout.addWidget(status_box)
                # progress bar in between the statuses
                self.progress_bar = QProgressBar(self)
                self.progress_bar.setRange(0, 0)
                self.progress_bar.setStyleSheet("QProgressBar { border: 2px solid #00BFFF; border-radius: 10px; }")
                card_layout.addWidget(self.progress_bar)
                value_box2 = QFrame()
                value_box2.setStyleSheet("background-color: #4A4A4A; border-radius: 10px; padding: 10px;")
                value_box_layout2 = QVBoxLayout()
                for i, info in enumerate(info_labels_2):
                    label = QLabel(info)
                    label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
                    if i == 1:  # This is the "Actual Value" label
                        label.setObjectName("actual_value_label2")  # Set object name for actual value
                    value_box_layout2.addWidget(label)
                value_box2.setLayout(value_box_layout2)
                card_layout.addWidget(value_box2)

                # Create a separate box for Status
                status_box = QFrame()
                status_box.setObjectName("status_box2") # object name should be changed to access the second screen variables 
                # Set the background color based on the status
                if self.status.lower() == 'OK':
                    status_box.setStyleSheet("background-color: #28A745; border-radius: 10px; padding: 10px;")
                elif self.status.lower() == 'Not Good':
                    status_box.setStyleSheet("background-color: #DC3545; border-radius: 10px; padding: 10px;")
                else:
                    status_box.setStyleSheet("background-color: #FFC107; border-radius: 10px; padding: 10px;")  # Yellow for undefined status
                
                status_layout = QVBoxLayout()
                # status_label = QLabel(f"<h1><b>Status:</b> {status}</h1>")
                # status_label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
                # status_layout.addWidget(status_label)
                status_label = QLabel(f"<h1><b>Status:</b> {self.status}</h1>")
                status_label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
                status_label.setObjectName("status_label2")  # Set object name for the status label
                status_layout.addWidget(status_label)

                status_box.setLayout(status_layout)
                
                card_layout.addWidget(status_box)

        else:
                value_box1 = QFrame()
                value_box1.setStyleSheet("background-color: #4A4A4A; border-radius: 10px; padding: 10px;")
                value_box_layout1 = QVBoxLayout()

                # info_labels = [
                #     f"<b>Preset Value:</b> {value}", # here 
                #     f"<b>Actual Value:</b> {self.camera_thread.stable_v}",
                #     f"<b>Stabilization Time:</b> {status}",
                # ]

                # for info in info_labels:
                #     label = QLabel(info)
                #     label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
                #     value_box_layout.addWidget(label)
                info_labels_1 = [
                            f"<b>Preset Value (1):</b> {value1}",
                            f"<b>Actual Value (1):</b> {self.camera_thread.stable_v}", #need to change here 
                            f"<b>Tolerance Value(%) (1):</b> {tolerance1}",
                                
                                ]
                for i, info in enumerate(info_labels_1):
                    label = QLabel(info)
                    label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
                    if i == 1:  # This is the "Actual Value" label
                        label.setObjectName("actual_value_label1")  # actual_value_label_here
                    value_box_layout1.addWidget(label)
                value_box1.setLayout(value_box_layout1)
                card_layout.addWidget(value_box1)
                # Create a separate box for Status
                status_box = QFrame()
                status_box.setObjectName("status_box1")
                # Set the background color based on the status
                if self.status.lower() == 'OK':
                    status_box.setStyleSheet("background-color: #28A745; border-radius: 10px; padding: 10px;")
                elif self.status.lower() == 'Not Good':
                    status_box.setStyleSheet("background-color: #DC3545; border-radius: 10px; padding: 10px;")
                else:
                    status_box.setStyleSheet("background-color: #FFC107; border-radius: 10px; padding: 10px;")  # Yellow for undefined status
                
                status_layout = QVBoxLayout()
                # status_label = QLabel(f"<h1><b>Status:</b> {status}</h1>")
                # status_label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
                # status_layout.addWidget(status_label)
                status_label = QLabel(f"<h1><b>Status:</b> {self.status}</h1>")
                status_label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
                status_label.setObjectName("status_label1")  # Set object name for the status label
                status_layout.addWidget(status_label)

                status_box.setLayout(status_layout)
                
                card_layout.addWidget(status_box)
                # progress bar in between the statuses
                self.progress_bar = QProgressBar(self)
                self.progress_bar.setRange(0, 0)
                self.progress_bar.setStyleSheet("QProgressBar { border: 2px solid #00BFFF; border-radius: 10px; }")
                card_layout.addWidget(self.progress_bar)

        

        # Camera Button
        self.camera_button = QPushButton("Camera Enable")
        self.camera_button.setStyleSheet(""" 
            QPushButton {
                background-color: #00BFFF; 
                color: white; 
                border-radius: 10px; 
                padding: 10px; 
                font-size: 16px; 
            } 
            QPushButton:hover { 
                background-color: #008FBF; 
            } 
        """)
        self.camera_button.clicked.connect(self.toggle_camera)
        card_layout.addWidget(self.camera_button, alignment=Qt.AlignBottom)

        # Back Button
        self.back_button = QPushButton("Back to Tests")
        self.back_button.setStyleSheet(""" 
            QPushButton { 
                background-color: #FF6F61; 
                color: white; 
                border-radius: 10px; 
                padding: 10px; 
                font-size: 16px; 
            } 
            QPushButton:hover { 
                background-color: #BF5B4C; 
            } 
        """)
        
        self.back_button.clicked.connect(back_callback)  # Connect to the back callback
        # back_button.clicked.connect(self.disable_camera_auto)
        self.back_button.setVisible(True)
        card_layout.addWidget(self.back_button, alignment=Qt.AlignBottom)

        card.setLayout(card_layout)
        card.setMinimumWidth(400)
        return card
    def disable_camera_auto(self):
        if self.camera_running:
            self.camera_thread.stop()
            self.camera_running = False
            
    def toggle_camera(self):
        if not self.camera_running:
            self.enable_camera()
        else:
            self.disable_camera()
    # def store():
    #     print()
    #     return [self.value,self.tolerance,self.unit]
    def enable_camera(self):
        self.camera_thread.start()
        # tester = test.get('tester', 'N/A')
        # value = test.get('value', 'N/A')
        # stable_value = test.get('stable_value', 'N/A')
        # print(f'current test values (enable camera) : {tester},{value},{stable_value}')
        self.update_value_status(0.0, "Initializing...")

        self.camera_running = True
        self.camera_button.setText("Camera Disable")
        self.back_button.setVisible(False)
        self.engine.say(self.status)
        self.engine.runAndWait()

    def disable_camera(self):
        if self.camera_running:
            self.camera_thread.stop()
            self.camera_running = False
            self.camera_button.setText("Camera Enable")
            self.back_button.setVisible(True)
    def update_image(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        h, w, ch = rgb_frame.shape
        qt_image = QImage(rgb_frame.data, w, h, ch * w, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qt_image))

    def handle_camera_error(self, message):
        QMessageBox.warning(self, "Camera Error", message)

    def closeEvent(self, event):
        self.disable_camera()
        event.accept()
    def update_value_status(self, stable_v, status_label):
    # Update the "Actual Value" label
        self.status = status_label # changed here 
        actual_value_label = self.card.findChild(QLabel, "actual_value_label")
        if actual_value_label:
             actual_value_label.setText(f"<b>Actual Value:</b> {stable_v}")
    
    # Update the "Status" label
        status_label_widget = self.card.findChild(QLabel, "status_label")
        if status_label_widget:
             status_label_widget.setText(f"<h1><b>Status:</b> {status_label}</h1>")
    
    # Update the status box background color based on the status
        status_box = self.card.findChild(QFrame, "status_box")
        if status_box:
         if status_label.lower() == 'ok':
            status_box.setStyleSheet("background-color: #28A745; border-radius: 10px; padding: 10px;")
         elif status_label.lower() == 'not good':
            status_box.setStyleSheet("background-color: #DC3545; border-radius: 10px; padding: 10px;")
         else:
            status_box.setStyleSheet("background-color: #FFC107; border-radius: 10px; padding: 10px;")
    def update_value_status_no_nc(self, stable_v, status_label):
    # Update the "Actual Value" label
        self.status = status_label # changed here 
        actual_value_label = self.card.findChild(QLabel, "actual_value_label1")
        if actual_value_label:
             actual_value_label.setText(f"<b>Actual Value:</b> {stable_v}")
    
    # Update the "Status" label
        status_label_widget = self.card.findChild(QLabel, "status_label1")
        if status_label_widget:
             status_label_widget.setText(f"<h1><b>Status:</b> {status_label}</h1>")
    
    # Update the status box background color based on the status
        status_box = self.card.findChild(QFrame, "status_box1")
        if status_box:
         if status_label.lower() == 'close':
            status_box.setStyleSheet("background-color: #28A745; border-radius: 10px; padding: 10px;")
         elif status_label.lower() == 'open':
            status_box.setStyleSheet("background-color: #DC3545; border-radius: 10px; padding: 10px;")
         else:
            status_box.setStyleSheet("background-color: #FFC107; border-radius: 10px; padding: 10px;")
    def update_value_status1(self, stable_v, status_label):
    # Update the "Actual Value" label
        self.status = status_label # changed here 
        actual_value_label = self.card.findChild(QLabel, "actual_value_label1")
        if actual_value_label:
             actual_value_label.setText(f"<b>Actual Value:</b> {stable_v}")
    
    # Update the "Status" label
        status_label_widget = self.card.findChild(QLabel, "status_label1")
        if status_label_widget:
             status_label_widget.setText(f"<h1><b>Status:</b> {status_label}</h1>")
    
    # Update the status box background color based on the status
        status_box = self.card.findChild(QFrame, "status_box1")
        if status_box:
         if status_label.lower() == 'ok':
            status_box.setStyleSheet("background-color: #28A745; border-radius: 10px; padding: 10px;")
         elif status_label.lower() == 'not good':
            status_box.setStyleSheet("background-color: #DC3545; border-radius: 10px; padding: 10px;")
         else:
            status_box.setStyleSheet("background-color: #FFC107; border-radius: 10px; padding: 10px;")
    def update_value_status2(self, stable_v, status_label):
    # Update the "Actual Value" label
        self.status = status_label # changed here 
        actual_value_label = self.card.findChild(QLabel, "actual_value_label2")
        if actual_value_label:
             actual_value_label.setText(f"<b>Actual Value:</b> {stable_v}")
    
    # Update the "Status" label
        status_label_widget = self.card.findChild(QLabel, "status_label2")
        if status_label_widget:
             status_label_widget.setText(f"<h1><b>Status:</b> {status_label}</h1>")
    
    # Update the status box background color based on the status
        status_box = self.card.findChild(QFrame, "status_box2")
        if status_box:
         if status_label.lower() == 'ok':
            status_box.setStyleSheet("background-color: #28A745; border-radius: 10px; padding: 10px;")
         elif status_label.lower() == 'not good':
            status_box.setStyleSheet("background-color: #DC3545; border-radius: 10px; padding: 10px;")
         else:
            status_box.setStyleSheet("background-color: #FFC107; border-radius: 10px; padding: 10px;")

    # def update_value_status(self, stable_v, status_label):
    # # Update the labels with the new values
    #     self.card.findChild(QLabel, "Actual Value:").setText(f"<b>Actual Value:</b> {stable_v}")
    #     self.card.findChild(QLabel, "Status:").setText(f"<h1><b>Status:</b> {status_label}</h1>")

    # # Update the status box background color based on the status
    #     status_box = self.card.findChild(QFrame, "Status Box")
    #     if status_label.lower() == 'ok':
    #         status_box.setStyleSheet("background-color: #28A745; border-radius: 10px; padding: 10px;")
    #     elif status_label.lower() == 'not good':
    #         status_box.setStyleSheet("background-color: #DC3545; border-radius: 10px; padding: 10px;")
    #     else:
    #         status_box.setStyleSheet("background-color: #FFC107; border-radius: 10px; padding: 10px;")