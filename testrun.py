import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window title
        self.setWindowTitle('AIprob Login')
        self.setGeometry(0, 0, 800, 600)  # Initial size, will go full screen

        # Create a frame to act as a card
        self.card = QFrame(self)
        self.card.setStyleSheet("""
            QFrame {
                background-color: #3c3f41;
                border-radius: 15px;
                padding: 20px;
            }
        """)

        # Create labels
        self.company_label = QLabel('Company Name: Your Company', self.card)
        self.product_label = QLabel('Product Name: AIprob', self.card)

        # Create buttons
        self.login_button = QPushButton('Login', self.card)
        self.quit_button = QPushButton('Quit', self.card)

        # Connect buttons to functions
        self.quit_button.clicked.connect(self.close)
        self.login_button.clicked.connect(self.login)

        # Set layout for the card
        layout = QVBoxLayout(self.card)
        layout.addWidget(self.company_label)
        layout.addWidget(self.product_label)
        layout.addWidget(self.login_button)
        layout.addWidget(self.quit_button)

        # Set the layout for the main window
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.card, alignment=Qt.AlignCenter)  # Correct alignment

        self.setLayout(main_layout)

        # Apply styles
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b; 
                color: #ffffff; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                font-size: 14px;
            }
            QLabel {
                font-size: 16px;
                margin-bottom: 10px;
            }
            QPushButton {
                background-color: #1a73e8; 
                color: white; 
                border: none; 
                border-radius: 5px; 
                padding: 10px; 
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
            QPushButton:pressed {
                background-color: #003d7a;
            }
        """)

    def login(self):
        print("Login button clicked!")  # Replace with actual login logic

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.showFullScreen()  # Set the application to full-screen
    sys.exit(app.exec_())
