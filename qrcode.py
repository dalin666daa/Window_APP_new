import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QGridLayout
from PyQt5.QtGui import QImage, QPalette, QColor, QPixmap
from PyQt5.QtCore import QTimer
from pyzbar.pyzbar import decode
import numpy as np

class QRCodeReader(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the UI
        self.setWindowTitle("Multiple QR Code Reader")
        self.setGeometry(100, 100, 800, 600)

        # Set dark theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

        # Main layout
        self.layout = QVBoxLayout()
        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        self.result_container = QWidget(self)
        self.result_layout = QGridLayout(self.result_container)
        self.result_container.setLayout(self.result_layout)
        self.layout.addWidget(self.result_container)

        self.start_button = QPushButton("Start Scanning", self)
        self.start_button.clicked.connect(self.start_scanning)
        self.layout.addWidget(self.start_button)

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(self.layout)

        self.cap = None

    def start_scanning(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(1)
            self.update_frame()

    def update_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Decode QR codes
                decoded_objects = decode(frame)

                # Display video feed
                self.display_video(frame)

                # Update results based on detected QR codes
                self.display_results(decoded_objects, frame)

            # Update frame every 30 ms
            QTimer.singleShot(30, self.update_frame)

    def display_video(self, frame):
        # Convert frame to QImage
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Set the video frame to the label
        self.video_label.setPixmap(QPixmap.fromImage(q_img))

    def display_results(self, decoded_objects, frame):
        # Clear previous results
        for i in reversed(range(self.result_layout.count())):
            widget = self.result_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create a grid layout for displaying QR codes and their data
        for i, obj in enumerate(decoded_objects):
            qr_data = obj.data.decode('utf-8')

            # Draw a rectangle around the QR code (optional)
            pts = obj.polygon
            if len(pts) == 4:
                cv2.polylines(frame, [np.array(pts)], isClosed=True, color=(255, 0, 0), thickness=2)

            # Convert the QR code to an image
            qr_image = self.extract_qr_code(frame, obj)

            # Create labels to show QR code image and data
            if qr_image is not None:
                qr_pixmap = QPixmap.fromImage(qr_image)
                qr_label = QLabel()
                qr_label.setPixmap(qr_pixmap)
                self.result_layout.addWidget(qr_label, i, 0)

            result_label = QLabel(f"Detected: {qr_data}")
            result_label.setStyleSheet("color: white;")
            self.result_layout.addWidget(result_label, i, 1)

    def extract_qr_code(self, frame, obj):
        """Extracts the QR code from the frame."""
        (x, y, w, h) = cv2.boundingRect(np.array(obj.polygon))
        qr_code_image = frame[y:y+h, x:x+w]
        qr_code_image_rgb = cv2.cvtColor(qr_code_image, cv2.COLOR_BGR2RGB)
        h, w, ch = qr_code_image_rgb.shape
        bytes_per_line = ch * w
        return QImage(qr_code_image_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)

    def closeEvent(self, event):
        if self.cap:
            self.cap.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeReader()
    window.show()
    sys.exit(app.exec_())
