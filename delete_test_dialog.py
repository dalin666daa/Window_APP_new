from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
from PyQt5.QtCore import Qt

class DeleteTestDialog(QDialog):
    def __init__(self, tests):
        super().__init__()
        self.setWindowTitle("Delete Test")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #2B2B2B; color: white; border-radius: 10px;")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.label = QLabel("Select a test to delete:")
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(self.label)

        # Create a scroll area for buttons
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.button_container = QFrame()
        self.button_layout = QVBoxLayout(self.button_container)

        # Create buttons for each test to delete
        for i, test in enumerate(tests):
            button = QPushButton(f"Delete Test {i + 1}: {test['value']}")
            button.setStyleSheet("""
                background-color: #D9534F; 
                color: white; 
                padding: 10px; 
                border: none; 
                border-radius: 5px;
                margin: 5px 0;
            """)
            button.clicked.connect(lambda _, index=i: self.delete_test(index))
            self.button_layout.addWidget(button)

        self.button_container.setLayout(self.button_layout)
        self.scroll_area.setWidget(self.button_container)

        self.layout.addWidget(self.scroll_area)

        # Add Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet("""
            background-color: #5bc0de; 
            color: white; 
            padding: 10px; 
            border: none; 
            border-radius: 5px;
        """)
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)
        self.test_to_delete = None  # Store the index of the test to delete

    def delete_test(self, index):
        self.test_to_delete = index  # Store the index
        self.accept()  # Close the dialog

    def get_test_to_delete(self):
        return self.test_to_delete  # Return the index of the test to delete

# Example usage
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Dummy test data for demonstration
    tests = [{'value': 'Test A'}, {'value': 'Test B'}, {'value': 'Test C'}]

    dialog = DeleteTestDialog(tests)
    if dialog.exec_() == QDialog.Accepted:
        print(f"Test to delete: {dialog.get_test_to_delete() + 1}")  # Output the index of the deleted test
    else:
        print("Deletion canceled.")

    sys.exit(app.exec_())
