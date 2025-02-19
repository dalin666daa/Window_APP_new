from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox, QHBoxLayout
from running_test_page import RunningTestPage

class TestDetailDialog(QDialog):
    def __init__(self, test, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Test Details")
        self.setFixedSize(300, 200)
        self.setStyleSheet("background-color: #333333; color: white;")

        layout = QVBoxLayout()

        # Display test details
        test_details = (
            f"Model: {test.get('Model', 'N/A')}\n"
            f"Tester: {test.get('tester1', 'N/A')}\n"
            f"Value: {test.get('value1', 'N/A')}\n"
            f"Tolerance: {test.get('tolerance1', 'N/A')}\n"
            # f"Stabilizing Time: {test.get('stabilization_time', 'N/A')}"
        )
        detail_label = QLabel(test_details)
        detail_label.setStyleSheet("color: white;")
        layout.addWidget(detail_label)

        # Create buttons
        button_layout = QHBoxLayout()
        
        run_button = QPushButton("Run Test")
        self.style_button(run_button)
        run_button.clicked.connect(lambda: self.confirm_run(test))
        button_layout.addWidget(run_button)

        close_button = QPushButton("Close")
        self.style_button(close_button)
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.adjustSize()  # Resize to fit contents
        self.setFixedSize(self.size())  # Ensure the dialog size doesn't change after showing

    def style_button(self, button):
        button.setStyleSheet("color: white; background-color: #76B900;")

    def confirm_run(self, test):
        reply = QMessageBox.question(
            self,
            'Confirm Run',
            f'Are you sure you want to run the test: {test.get("tester", "N/A")}?', 
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            running_test_page = RunningTestPage(test, self.parent().show_test_selection)
            self.parent().clear_layout()  # Ensure this method is defined in the parent
            self.parent().layout().addWidget(running_test_page)
            self.close()

# Example usage (for testing)
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Dummy test data for demonstration
    test_data = {
        'tester': 'John Doe',
        'value': 42,
        'tolerance': 5,
        'stabilization_time': '12:00:00'
    }

    dialog = TestDetailDialog(test_data)
    dialog.exec_()

    sys.exit(app.exec_())
