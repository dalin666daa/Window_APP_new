from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

class ConfirmUserDialog(QDialog):
    def __init__(self, user_info):
        super().__init__()
        self.setWindowTitle("Confirm User Details")

        self.layout = QVBoxLayout()

        # Show user details
        self.layout.addWidget(QLabel(f"Username: {user_info['username']}"))
        self.layout.addWidget(QLabel(f"Full Name: {user_info['fullname']}"))
        self.layout.addWidget(QLabel(f"Email: {user_info['email']}"))

        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Buttons for confirmation
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.accept)
        button_layout.addWidget(self.confirm_button)

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.reject)
        button_layout.addWidget(self.edit_button)

        # Add button layout to the main layout
        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)
