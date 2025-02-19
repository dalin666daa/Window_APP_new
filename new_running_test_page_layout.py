# from PyQt5.QtGui import QPixmap

# class HomePage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("AI-PROBE")
#         self.setGeometry(100, 100, 1280, 800)
#         self.setStyleSheet("background-color: #121212;")
        
#         # Initialize text-to-speech engine
#         self.engine = pyttsx3.init()
#         self.init_tts()

#         self.stacked_widget = QStackedWidget(self)
#         self.home_page = QWidget()
#         self.reports_page = ReportsPage()

#         self.init_home_page()

#         self.stacked_widget.addWidget(self.home_page)
#         self.stacked_widget.addWidget(self.reports_page)

#         layout = QVBoxLayout()
#         layout.addWidget(self.stacked_widget)
#         self.setLayout(layout)

#     def init_tts(self):
#         voices = self.engine.getProperty('voices')
#         if voices:
#             self.engine.setProperty('voice', voices[1].id)  # Change index as needed
#         else:
#             print("No voices available.")

#     def showEvent(self, event):
#         super().showEvent(event)
#         self.announce_welcome()

#     def announce_welcome(self):
#         self.text_to_audio("Hai, I am Eva. Welcome to AI Probe by En Products. Please log in.")

#     def text_to_audio(self, text):
#         try:
#             self.engine.say(text)
#             self.engine.runAndWait()
#         except Exception as e:
#             print(f"Error during TTS: {e}")

#     def init_home_page(self):
#         layout = QVBoxLayout()
#         layout.addWidget(self.create_title_card())
#         layout.addLayout(self.create_second_card_layout())
#         self.home_page.setLayout(layout)

#     def create_title_card(self):
#         title_card = QFrame()
#         title_card.setStyleSheet("background-color: #1E1E1E; border-radius: 10px; padding: 20px;")

#         title_label = QLabel("AI-PROBE", title_card)
#         title_label.setFont(QtGui.QFont("Roboto", 36, QtGui.QFont.Bold))
#         title_label.setAlignment(Qt.AlignCenter)
#         title_label.setStyleSheet("color: #E0E0E0;")

#         # Load and add logo 
#         logo_label = QLabel(title_card)
#         pixmap = QPixmap(r"D:\Window_APP_4\Window_APP\source\logo_enpro.png")  
#         scaled_pixmap = pixmap.scaled(300, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Adjust size as needed
#         logo_label.setPixmap(scaled_pixmap)
#         logo_label.setAlignment(Qt.AlignCenter)

#         title_layout = QVBoxLayout()
#         title_layout.addWidget(title_label)
#         title_layout.addWidget(logo_label)

#         title_card.setLayout(title_layout)
#         return title_card

    # ... rest of your code remains the same ...
import torch
print(torch.cuda.is_available())
import paddle
print(paddle.is_compiled_with_cuda())
# print(python.__version__)
import sys
print("Current Python version:", sys.version)
print("Python executable path:", sys.executable)
