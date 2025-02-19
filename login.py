from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QApplication
)
from PyQt5 import QtGui

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(200, 200, 400, 300)
        self.setStyleSheet("background-color: black; color: white; border: none;")

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title Label
        title_label = QLabel("Login", self)
        title_label.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #76B900;")  # Green color
        layout.addWidget(title_label)

        # Username Input
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("background-color: #2B2B2B; color: white; padding: 10px; border: none; border-radius: 5px;")
        layout.addWidget(self.username_input)

        # Password Input
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("background-color: #2B2B2B; color: white; padding: 10px; border: none; border-radius: 5px;")
        layout.addWidget(self.password_input)

        # Login Button
        login_button = QPushButton("Login")
        login_button.setStyleSheet("background-color: #76B900; color: white; padding: 10px; border: none; border-radius: 5px; font-size: 16px;")
        login_button.clicked.connect(self.on_login)
        layout.addWidget(login_button)

        # Cancel Button
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("background-color: #76B900; color: white; padding: 10px; border: none; border-radius: 5px; font-size: 16px;")
        cancel_button.clicked.connect(self.reject)  # Close the dialog without logging in
        layout.addWidget(cancel_button) #D32F2F

        self.setLayout(layout)

    def on_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Simple authentication logic (replace with your actual logic)
        if (username == "enpro" and password == "enpro") or (username == "" and password == ""):  # Example credentials
            print("Logging in...")
            self.accept()  # Close the dialog and return Accepted
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect username or password.", QMessageBox.Ok)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.exec_()
