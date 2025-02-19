import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QStackedWidget,
    QPushButton, QFrame, QLabel, QHBoxLayout, QDialog
)
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie, QColor, QFont , QPixmap ,QPainter ,QBrush
import pyttsx3
from login import LoginWindow
from reports import ReportsPage
from report_selection_dialog import ReportSelectionDialog
from master import MasterPage 

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-PROBE")
        self.setGeometry(100, 100, 1280, 800)
        self.setStyleSheet("background-color: #121212;")
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.init_tts()

        self.stacked_widget = QStackedWidget(self)
        self.home_page = QWidget()
        self.reports_page = ReportsPage()

        self.init_home_page()

        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.reports_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def init_tts(self):
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[1].id)  # Change index as needed
        else:
            print("No voices available.")

    def showEvent(self, event):
        super().showEvent(event)
        self.announce_welcome()

    def announce_welcome(self):
        self.text_to_audio("Hai, I am Eva. Welcome to AI Probe by En Products. Please log in.")

    def text_to_audio(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error during TTS: {e}")

    def init_home_page(self):
        layout = QVBoxLayout()
        layout.addWidget(self.create_title_card())
        layout.addLayout(self.create_second_card_layout())
        self.home_page.setLayout(layout)

    def create_title_card(self):
        title_card = QFrame()
        title_card.setStyleSheet("background-color: #1E1E1E; border-radius: 10px; padding: 20px;")

        
        title_label = QLabel("AI-PROBE", title_card)
        title_label.setFont(QtGui.QFont("Roboto", 43, QtGui.QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #76B900;") #E0E0E0 ,76B900 , 0BDA51

        # Load and add logo 
        logo_label = QLabel(title_card)
        pixmap = QPixmap(r"D:\output-onlinepngtools (3).png")  
        scaled_pixmap = pixmap.scaled(450, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Adjust size as needed
        scaled_pixmap = self.apply_rounded_corners(scaled_pixmap, 30) 
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        title_layout = QVBoxLayout()
        title_layout.addWidget(title_label)
        title_layout.addWidget(logo_label)

        title_card.setLayout(title_layout)
        return title_card

    def create_second_card_layout(self):
        second_card_layout = QHBoxLayout()
        graph_card = self.create_graph_card()
        button_card = self.create_button_card()
        second_card_layout.addWidget(graph_card)
        second_card_layout.addWidget(button_card)
        return second_card_layout

    def create_graph_card(self):
        graph_card = QFrame()
        graph_card.setStyleSheet("background-color: #1E1E1E; border-radius: 10px; padding: 20px;")

        gif_label = QLabel(graph_card)
        gif_label.setAlignment(Qt.AlignCenter)

        movie = QMovie(r"D:\Window_APP_4\Window_APP\source\nvidia.gif")
        gif_label.setMovie(movie)
        movie.start()
        
        graph_layout = QVBoxLayout()
        graph_layout.addWidget(gif_label)
        graph_card.setLayout(graph_layout)
        return graph_card
    def apply_rounded_corners(self, pixmap, radius):
        # Create a new pixmap with transparent background
        rounded = QPixmap(pixmap.size())
        rounded.fill(Qt.transparent)

        # Paint the rounded corners
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(pixmap))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rounded.rect(), radius, radius)
        painter.end()

        return rounded
    def create_button_card(self):
        button_card = QFrame()
        button_card.setStyleSheet("background-color: #1E1E1E; border-radius: 10px; padding: 20px;")
        button_layout = QVBoxLayout()

        login_button = self.create_button("Login", '#76B900', self.on_login) #76B900 ,#FF6F61
        reports_button = self.create_button("Report", '#76B900', self.on_select_report)
        quit_button = self.create_button("Quit", '#76B900', self.on_quit)

        button_layout.addWidget(login_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(reports_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(quit_button, alignment=Qt.AlignCenter)

        button_card.setLayout(button_layout)
        return button_card

    def create_button(self, text, color, callback):
        button = QPushButton(text)
        button.setStyleSheet(f"""
            background-color: {color}; color: #302e2e; padding: 10px; border: none; border-radius: 5px;
        """)
        button.setFont(QtGui.QFont("Roboto", 24))
        button.setMinimumSize(200, 60)
        button.clicked.connect(callback)

        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color}; color: #302e2e; padding: 10px; border: none; border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color, 20)};
            }}
        """)
        
        return button

    def darken_color(self, color, amount):
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r = max(0, r - amount)
        g = max(0, g - amount)
        b = max(0, b - amount)
        return f'#{r:02x}{g:02x}{b:02x}'

    def on_login(self):
        login_window = LoginWindow()
        if login_window.exec_() == QDialog.Accepted:
            master_page = MasterPage()
            master_page.show()
            self.close()

    def on_select_report(self):
        dialog = ReportSelectionDialog(reports_folder='reports/', parent=self)
        dialog.report_selected.connect(self.on_report_selected)
        dialog.exec_()

    def on_report_selected(self, file_path):
        try:
            self.text_to_audio("Here are the reports for the batch.")
            self.reports_page.load_reports(file_path)
            self.stacked_widget.setCurrentWidget(self.reports_page)
        except Exception as e:
            print(f"Error loading report: {e}")

    def on_quit(self):
        self.text_to_audio("See you soon.")
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())