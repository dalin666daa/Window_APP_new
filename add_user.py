from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QFormLayout

class AddUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add User")

        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        # Input fields
        self.username_input = QLineEdit(self)
        self.fullname_input = QLineEdit(self)
        self.email_input = QLineEdit(self)
        self.contact_input = QLineEdit(self)
        self.country_input = QLineEdit(self)
        self.industry_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        # Add fields to the form layout
        self.form_layout.addRow(QLabel("Username:"), self.username_input)
        self.form_layout.addRow(QLabel("Full Name:"), self.fullname_input)
        self.form_layout.addRow(QLabel("Email:"), self.email_input)
        self.form_layout.addRow(QLabel("Contact Number:"), self.contact_input)
        self.form_layout.addRow(QLabel("Country:"), self.country_input)
        self.form_layout.addRow(QLabel("Industry:"), self.industry_input)
        self.form_layout.addRow(QLabel("Password:"), self.password_input)
        self.form_layout.addRow(QLabel("Confirm Password:"), self.confirm_password_input)

        self.layout.addLayout(self.form_layout)

        # Buttons
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_user)
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.reject)

        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def save_user(self):
        if self.password_input.text() != self.confirm_password_input.text():
            QMessageBox.warning(self, "Input Error", "Passwords do not match!", QMessageBox.Ok)
            return

        if not self.username_input.text():
            QMessageBox.warning(self, "Input Error", "Username cannot be empty!", QMessageBox.Ok)
            return

        user_info = {
            'username': self.username_input.text(),
            'fullname': self.fullname_input.text(),
            'email': self.email_input.text(),
            'contact': self.contact_input.text(),
            'country': self.country_input.text(),
            'industry': self.industry_input.text(),
            'password': self.password_input.text()
        }

        self.user_info = user_info  # Store user info
        self.accept()  # Accept the dialog

    def get_user_info(self):
        return self.user_info
