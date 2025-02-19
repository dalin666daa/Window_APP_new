from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QMessageBox, QComboBox, QTimeEdit, QGraphicsDropShadowEffect, QApplication
from PyQt5.QtGui import QPalette, QColor, QFont, QPainter, QPen, QRegExpValidator
from PyQt5.QtCore import pyqtSignal, Qt, QRegExp
import re
from datetime import datetime


class AddTestDialog(QDialog):
    values_from_add_test = pyqtSignal(float, float, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Test")
        self.setWindowFlag(Qt.FramelessWindowHint)  # Remove title bar for modern look
        self.setAttribute(Qt.WA_TranslucentBackground)  # Transparent background
        self.setWindowOpacity(0.95)  # Slight transparency effect

        # Set up the form layout
        self.layout = QFormLayout(self)

        # Dropdown combo box for model selection
        self.model_combo = QComboBox()
        self.model_combo.addItems(["SingleMultiMeter", "LuxMeter", "DoubleMeters"])
        self.model_combo.setCurrentIndex(0)
        self.model_combo.currentTextChanged.connect(self.update_form_once)
        # Update the combobox styling
        self.model_combo.setStyleSheet("""
            QComboBox {
                color: green;  # Text color in the combobox
                background-color: #fff;  # Dark background
                border: 2px solid #666;
                border-radius: 10px;
                padding: 6px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: 2px solid #fff;
                border-radius: 10px;
                background-color: #fff;
            }
            QComboBox::down-arrow {
                image: url(data:image/png;base64,...);  # Optional: custom down-arrow image
            }
            QComboBox QAbstractItemView {
                background-color: #fff;  # Dark background for the dropdown list
                color: #176e3c;  # Light cyan text color for the dropdown items
                selection-background-color: #fff;  # Darker background when an item is selected
                selection-color: #FFFFFF;  # White text when an item is selected
            }
        """)

        # Input fields for test details
        self.tester_input = self.create_input_field("Tester")
        self.value_input = self.create_input_field("Value", True)
        self.tolerance_input = self.create_input_field("Tolerance", True)
        self.unit_input = self.create_input_field("Unit")
        # self.stabilization_time_input = QTimeEdit(self)
        # self.stabilization_time_input.setDisplayFormat("HH:mm:ss")
        # self.stabilization_time_input.setTime(datetime.now().time())

        # Add form fields to the layout
        self.layout.addRow("Model:", self.model_combo)
        # self.tester_input = None
        # self.value_input = None
        # self.tolerance_input = None
        # self.unit_input = None
        self.layout.addRow("Tester:", self.tester_input)
        self.layout.addRow("Value:", self.value_input)
        self.layout.addRow("Tolerance:", self.tolerance_input)
        self.layout.addRow("Unit:", self.unit_input)
        # self.update_form()
# 
        
                 
        # self.layout.addRow("Stabilization Time:", self.stabilization_time_input)

        # Button box for dialog actions
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.on_accept)
        buttons.rejected.connect(self.reject)
        self.add_shadow_effect(buttons)
        self.layout.addRow(buttons)

        # Set the initial size of the dialog
        self.resize(600, 400)

        # Apply the futuristic UI and enhanced visuals
        self.set_futuristic_ui()

        # Set font for all widgets
        self.set_font(QFont("Orbitron", 12))
    def update_form_once(self):
        # while self.layout.rowCount() > 1:
        #         self.layout.removeRow(1)
        # Check if model_combo is set to "DoubleMeters"
        # self.layout.addRow("Tester:", self.tester_input)
        # # self.layout.addRow("Value:", self.value_input)
        # # self.layout.addRow("Tolerance:", self.tolerance_input)
        # # self.layout.addRow("Unit:", self.unit_input)
        
        if self.model_combo.currentText() == "DoubleMeters":
            # Clear current rows (except model selector)
            

            # Add rows for "DoubleMeters" configuration
            self.layout.addRow("Tester1:", self.tester_input)
            self.layout.addRow("Value2:", self.value_input)
            self.layout.addRow("Tolerance2:", self.tolerance_input)
            self.layout.addRow("Unit2:", self.unit_input)
        else:
            # Reset to single meter labels
            self.layout.addRow("Tester:", self.tester_input)
            self.layout.addRow("Value:", self.value_input)
            self.layout.addRow("Tolerance:", self.tolerance_input)
            self.layout.addRow("Unit:", self.unit_input)

        # Disconnect to prevent further changes after the first update
        self.model_combo.currentTextChanged.disconnect(self.update_form_once)
    def create_input_field(self, placeholder, is_numeric=False):
        input_field = QLineEdit()
        input_field.setPlaceholderText(f"Enter {placeholder}")
        input_field.setStyleSheet("""
            QLineEdit {
                background-color: #fff;
                color: #176e3cs;
                border: 2px solid #666;
                border-radius: 8px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #176e3c;
            }
        """)
        if is_numeric:
            # Apply numeric validation
            validator = QRegExpValidator(QRegExp(r'^\d+(\.\d+)?$'))
            input_field.setValidator(validator)
        return input_field

    def add_shadow_effect(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(23,110,60))  # Neon cyan shadow
        shadow.setOffset(0, 0)
        widget.setGraphicsEffect(shadow)

    def set_futuristic_ui(self):
        # Apply a dark theme with neon accents and shadows
        app_palette = QPalette()
        app_palette.setColor(QPalette.Window, QColor(24, 24, 24))
        app_palette.setColor(QPalette.Base, QColor(23, 110, 60))
        app_palette.setColor(QPalette.Button, QColor(23,110,60))
        app_palette.setColor(QPalette.WindowText, QColor(23,110,60))
        app_palette.setColor(QPalette.ButtonText, QColor(23,110,60))
        app_palette.setColor(QPalette.Highlight, QColor(23,110,60))
        app_palette.setColor(QPalette.HighlightedText, QColor(0,0,0))

        QApplication.instance().setPalette(app_palette)

    def set_font(self, font):
        self.setFont(font)
        self.tester_input.setFont(font)
        self.value_input.setFont(font)
        self.tolerance_input.setFont(font)
        self.unit_input.setFont(font)
        # self.stabilization_time_input.setFont(font)
        self.model_combo.setFont(font)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor(23,110,60), 2)
        painter.setPen(pen)
        painter.setBrush(QColor(24, 24, 24))
        painter.drawRoundedRect(self.rect(), 15, 15)
        super().paintEvent(event)

    def on_accept(self):
        print(f"model :: {self.model_combo}")
        if self.validate_inputs():
            self.values_from_add_test.emit(
                float(self.value_input.text()),
                float(self.tolerance_input.text()),
                self.unit_input.text()
            )
            self.accept()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter valid data.")

    def validate_inputs(self):
        tester = self.tester_input.text().strip()
        if not tester:
            QMessageBox.warning(self, "Input Error", "Tester cannot be empty.")
            return False

        if not self.is_numeric(self.value_input.text()) or not self.is_numeric(self.tolerance_input.text()):
            QMessageBox.warning(self, "Input Error", "Value and Tolerance must be numbers.")
            return False

        if not self.is_time_format(self.stabilization_time_input.text()):
            QMessageBox.warning(self, "Input Error", "Stabilization Time must be in HH:mm:ss format.")
            return False

        return True

    @staticmethod
    def is_numeric(value):
        return re.match(r'^\d+(\.\d+)?$', value) is not None

    @staticmethod
    # def is_time_format(value):
    #     try:
    #         datetime.strptime(value, "%H:%M:%S")
    #         return True
    #     except ValueError:
    #         return False

    def get_inputs(self):
        return {
            "model": self.model_combo.currentText(),
            "tester": self.tester_input.text(),
            "value": self.value_input.text(),
            "tolerance": self.tolerance_input.text(),
            "unit": self.unit_input.text(),
            # "stabilization_time": self.stabilization_time_input.text()
        }


# Sample code to run the dialog
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    add_test_dialog = AddTestDialog()
    if add_test_dialog.exec_() == QDialog.Accepted:
        test_info = add_test_dialog.get_inputs()
        print(test_info)  # Handle the added test data here