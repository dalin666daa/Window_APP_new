from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QMessageBox,  QGraphicsDropShadowEffect ,QComboBox ,QApplication
import re
from datetime import datetime
from PyQt5.QtCore import pyqtSignal,QThread,Qt, QRegExp
from PyQt5.QtGui import QPalette, QColor, QFont, QPainter, QPen, QRegExpValidator
import numpy as np
from ultralytics import YOLO
from paddleocr import PaddleOCR
class AddTestDialog(QDialog):
    values_from_add_test = pyqtSignal(float,float,str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Test")
        self.layout = QFormLayout(self)

        # Input fields for test details
        self.tester_input = QLineEdit()
        self.value_input = QLineEdit()
        self.tolerance_input = QLineEdit()
        self.unit_input = QLineEdit()
        self.stabilization_time_input = QLineEdit()

        current_time = datetime.now().strftime("%H%M%S")
        self.stabilization_time_input.setText(current_time)

        self.layout.addRow("Tester:", self.tester_input)
        self.layout.addRow("Value:", self.value_input)
        self.layout.addRow("Tolerance:", self.tolerance_input)
        self.layout.addRow("Unit:", self.unit_input)
        self.layout.addRow("Stabilization Time (HHMMSS):", self.stabilization_time_input)

        # Button box for dialog actions
        buttons = QDialogButtonBox()
        buttons.addButton("Add", QDialogButtonBox.AcceptRole)
        buttons.addButton("Cancel", QDialogButtonBox.RejectRole)
        buttons.accepted.connect(self.on_accept)
        buttons.rejected.connect(self.reject)

        self.layout.addRow(buttons)

    def keyPressEvent(self, event):
        # Get the currently focused widget
        focus_widget = self.focusWidget()

        if isinstance(focus_widget, QLineEdit):
            key = event.key()
            if key == 16777219:  # Backspace
                focus_widget.backspace()
            elif key == 16777220:  # Enter
                self.on_accept()
            elif key == 16777221:  # Escape
                self.reject()
            elif key == 46:  # Decimal point (.)
                focus_widget.insert('.')
            elif 48 <= key <= 57:  # Number keys 0-9
                focus_widget.insert(chr(key))

    def on_accept(self):
        if self.validate_inputs():
            # global value_input = self.value_input.text() , tolerance_input = self.tolerance_input.text() , unit_input = self.unit_input.text()
            # print(f'add test values are {value_input} , {tolerance_input}, {unit_input}')
            self.accept()
            # add_test_dialog = AddTestDialog()
            # if add_test_dialog.exec_() == QDialog.Accepted:
            #      value_input = self.value_input.text()
            #      tolerance_input = self.tolerance_input.text()
            #      unit_input = self.unit_input.text() 

                 
        
        else:
            QMessageBox.warning(self, "Input Error", "Please enter valid data.")
    
    # def store_values():
    #     print(f'store values are {self.value_input.text()}, {self.tolerance_input.text()} , {self.unit_input.text()}')
    #     return [self.value_input.text(), self.tolerance_input.text() , self.unit_input.text()]
    def validate_inputs(self):
        tester = self.tester_input.text().strip()
        if not tester:
            QMessageBox.warning(self, "Input Error", "Tester cannot be empty.")
            return False

        if not self.is_numeric(self.value_input.text()) or not self.is_numeric(self.tolerance_input.text()):
            QMessageBox.warning(self, "Input Error", "Value and Tolerance must be numbers.")
            return False

        if not self.is_time_format(self.stabilization_time_input.text()):
            QMessageBox.warning(self, "Input Error", "Stabilization Time must be in HHMMSS format.")
            return False

        return True

    @staticmethod
    def is_numeric(value):
        return re.match(r'^-?\d+(\.\d+)?$', value) is not None

    @staticmethod
    def is_time_format(value):
        return re.match(r'^\d{6}$', value) is not None

    def get_inputs(self):
        return {
            "tester": self.tester_input.text(),
            "value": self.value_input.text(),
            "tolerance": self.tolerance_input.text(),
            "unit": self.unit_input.text(),
            "stabilization_time": self.stabilization_time_input.text()
        }
# def store_values():
#     ob = AddTestDialog()
# if __name__ == "__main__":
#     import sys
#     from PyQt5.QtWidgets import QApplication

#     app = QApplication(sys.argv)
#     add_test_dialog = AddTestDialog()
#     if add_test_dialog.exec_() == QDialog.Accepted:
#         test_info = add_test_dialog.get_inputs()
#         print(test_info)  # Here you would handle the added test data
#Updating add_testpage 
class AddTestDialogmeters1(QDialog):
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
        self.layout.addRow("Tester:", self.tester_input)
        self.layout.addRow("Value:", self.value_input)
        self.layout.addRow("Tolerance:", self.tolerance_input)
        self.layout.addRow("Unit:", self.unit_input)
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
# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     add_test_dialog = AddTestDialog()
#     if add_test_dialog.exec_() == QDialog.Accepted:
#         test_info = add_test_dialog.get_inputs()
#         print(test_info)  # Handle the added test data here
 
class AddTestDialogmeters_latest(QDialog): #original addtest
    values_from_add_test = pyqtSignal(float,float,str)
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Add Test")
        self.setStyleSheet("""
            QDialog {
                background-color: #333333;  /* Dark background */
            }
            
            QLabel {
                color: #76B900;  /* NVIDIA green for label text */
                font-weight: bold;
            }
            QLineEdit {
                background-color: #333333;  /* Darker gray input field */
                color: #76B900;
                border: 1px solid #76B900;  /* NVIDIA green border */
                padding: 5px;
                font-size: 14px;
                border-radius: 5px;
            }
            QDialogButtonBox QPushButton {
                background-color: #76B900;
                color: #333333;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
            }
            QDialogButtonBox QPushButton:hover {
                background-color: #5a8c00;  /* Slightly darker green for hover */
            }
             
        """)




        self.layout = QFormLayout(self)
        
        self.model_combo = QComboBox()
        self.model_combo.addItems(["","SingleMultiMeter", "LuxMeter", "DoubleMeters", "NO/NC"])
        self.model_combo.setCurrentIndex(0)
        self.model_combo.currentTextChanged.connect(self.update_form_once)
        self.model_combo.setStyleSheet("""
    QComboBox {
        background-color: #333333;  /* Darker gray input field */
        color: #76B900;  /* NVIDIA green text */
        border: 1px solid #76B900;  /* NVIDIA green border */
        padding: 5px;
        font-size: 14px;
        border-radius: 5px;
    }
    QComboBox::drop-down {
        border: 2px solid #333333;  /* White border for the dropdown */
        border-radius: 5px;
        background-color: #333333;  /* White background for the dropdown arrow area */
    }
    
    QComboBox QAbstractItemView {
        background-color: #333333;  /* Dark background for dropdown list */
        color: white;  /* White text color for dropdown items */
        selection-background-color: #333333;  /* Dark background when an item is selected */
        selection-color: #76B900;  /* NVIDIA green text when an item is selected */
    }
    """)    # self.model_combo.setStyleSheet("""
        #     QComboBox{
        #         background-color: #333333;  /* Darker gray input field */
        #         color: #76B900;
        #         border: 1px solid #76B900;  /* NVIDIA green border */
        #         padding: 5px;
        #         font-size: 14px;
        #         border-radius: 5px;
            
        #     }
        #     QComboBox::drop-down {
        #         border: 2px solid #fff;
        #         border-radius: 10px;
        #         background-color: #fff;
        #     }
        #     QComboBox::down-arrow {
        #         image: url(data:image/png;base64,...);  # Optional: custom down-arrow image
        #     }
        #     QComboBox QAbstractItemView {
        #         background-color: #333333;  # Dark background for the dropdown list
        #         color: white;  # Light cyan text color for the dropdown items
        #         selection-background-color: #333333;  # Darker background when an item is selected
        #         selection-color: #76B900;  # White text when an item is selected
        #     }
        # """)
        # Input fields for test details
        self.tester_input1 = QLineEdit()
        self.value_input1 = QLineEdit()
        self.tolerance_input1 = QLineEdit()
        self.unit_input1 = QLineEdit()
        self.floating1 = QLineEdit()
        # self.tester_input = QLineEdit()
        self.value_input2 = QLineEdit()
        self.tolerance_input2 = QLineEdit()
        self.unit_input2 = QLineEdit()
        self.floating2 = QLineEdit()
        # self.stabilization_time_input = QLineEdit()

        # current_time = datetime.now().strftime("%H%M%S")
        # self.stabilization_time_input.setText(current_time)
        self.layout.addRow("Model", self.model_combo)
        self.layout.addRow("Tester :", self.tester_input1)
        self.layout.addRow("Value 1:", self.value_input1)
        self.layout.addRow("Tolerance 1:", self.tolerance_input1)
        self.layout.addRow("Unit 1:", self.unit_input1)
        # # self.layout.addRow("Enter meter 2 values")
        # # self.layout.addRow("Tester 2:", self.tester_input)
        # self.layout.addRow("Value 2:", self.value_input2)
        # self.layout.addRow("Tolerance 2:", self.tolerance_input2)
        # self.layout.addRow("Unit 2:", self.unit_input2)
        # # Button box for dialog actions
        # buttons = QDialogButtonBox()
        # buttons.addButton("Add", QDialogButtonBox.AcceptRole)
        # buttons.addButton("Cancel", QDialogButtonBox.RejectRole)
        # buttons.accepted.connect(self.on_accept)
        # buttons.rejected.connect(self.reject)

        # self.layout.addRow(buttons)
    # def model(self):
    #     return self.model 
    # def ocr1(self):
    #     return self.ocr1
    # def ocr2(self):
    #     return self.ocr2
    
    def update_form_once(self):
        # print(f"model Name : {self.model_combo.currentText()}")
        if self.model_combo.currentText() == "DoubleMeters":
            try:
                while self.layout.rowCount() > 1:
                    self.layout.removeRow(1)
                self.tester_input1 = QLineEdit()
                self.value_input1 = QLineEdit()
                self.tolerance_input1 = QLineEdit()
                self.unit_input1 = QLineEdit()
                self.floating1 = QLineEdit()
                # self.tester_input = QLineEdit()
                self.value_input2 = QLineEdit()
                self.tolerance_input2 = QLineEdit()
                self.unit_input2 = QLineEdit()
                self.floating2 = QLineEdit()
            except:
                print("No previous rows found :)")
            self.layout.addRow("Tester :", self.tester_input1)
            self.layout.addRow("Value 1:", self.value_input1)
            self.layout.addRow("Tolerance 1:", self.tolerance_input1)
            self.layout.addRow("Unit 1:", self.unit_input1)
            self.layout.addRow("Compulsory Floating point 1 (y/n)",self.floating1)
            # self.layout.addRow("Enter meter 2 values")
            # self.layout.addRow("Tester 2:", self.tester_input)
            self.layout.addRow("Value 2:", self.value_input2)
            self.layout.addRow("Tolerance 2:", self.tolerance_input2)
            self.layout.addRow("Unit 2:", self.unit_input2)
            self.layout.addRow("Compulsory Floating point 2 (y/n)",self.floating2)
            # Button box for dialog actions
            buttons = QDialogButtonBox()
            buttons.addButton("Add", QDialogButtonBox.AcceptRole)
            buttons.addButton("Cancel", QDialogButtonBox.RejectRole)
            buttons.accepted.connect(self.on_accept)
            buttons.rejected.connect(self.reject)

            self.layout.addRow(buttons)
        elif self.model_combo.currentText() == "NO/NC":
            try:
                while self.layout.rowCount() > 1:
                  self.layout.removeRow(1)
                self.tester_input1 = QLineEdit()
                self.value_input1 = QLineEdit()
                self.tolerance_input1 = QLineEdit()
                self.floating1 = QLineEdit()
            except:
                print("No previous rows found :)")
            
            self.layout.addRow("Tester :", self.tester_input1)
            self.layout.addRow("Value 1:", self.value_input1)
            self.layout.addRow("Tolerance 1:", self.tolerance_input1)
            self.layout.addRow("Compulsory Floating point 1 (y/n)",self.floating1)
            # print("floating point values :", self.floating1.text())
            # print("floating point values without text() :", self.floating1)
            buttons = QDialogButtonBox()
            buttons.addButton("Add", QDialogButtonBox.AcceptRole)
            buttons.addButton("Cancel", QDialogButtonBox.RejectRole)
            buttons.accepted.connect(self.on_accept)
            buttons.rejected.connect(self.reject)
            self.layout.addRow(buttons)

        else:
            try:
                while self.layout.rowCount() > 1:
                  self.layout.removeRow(1)
                self.tester_input1 = QLineEdit()
                self.value_input1 = QLineEdit()
                self.tolerance_input1 = QLineEdit()
                self.unit_input1 = QLineEdit()
                self.floating1 = QLineEdit()
                # self.tester_input = QLineEdit()
               
            except:
                print("No previous rows found :)")
            
            self.layout.addRow("Tester :", self.tester_input1)
            self.layout.addRow("Value 1:", self.value_input1)
            self.layout.addRow("Tolerance 1:", self.tolerance_input1)
            self.layout.addRow("Unit 1:", self.unit_input1)
            self.layout.addRow("Compulsory Floating point 1 (y/n)",self.floating1)
            # print("floating point values :", self.floating1.text())
            # print("floating point values without text() :", self.floating1)
            buttons = QDialogButtonBox()
            buttons.addButton("Add", QDialogButtonBox.AcceptRole)
            buttons.addButton("Cancel", QDialogButtonBox.RejectRole)
            buttons.accepted.connect(self.on_accept)
            buttons.rejected.connect(self.reject)
            self.layout.addRow(buttons)
    def keyPressEvent(self, event):
        # Get the currently focused widget
        focus_widget = self.focusWidget()

        if isinstance(focus_widget, QLineEdit):
            key = event.key()
            if key == 16777219:  # Backspace
                focus_widget.backspace()
            elif key == 16777220:  # Enter
                self.on_accept()
            elif key == 16777221:  # Escape
                self.reject()
            elif key == 46:  # Decimal point (.)
                focus_widget.insert('.')
            elif 48 <= key <= 57:  # Number keys 0-9
                focus_widget.insert(chr(key))

    def on_accept(self):
        if self.validate_inputs():
            # global value_input = self.value_input.text() , tolerance_input = self.tolerance_input.text() , unit_input = self.unit_input.text()
            # print(f'add test values are {value_input} , {tolerance_input}, {unit_input}')
            self.accept()
            # add_test_dialog = AddTestDialog()
            # if add_test_dialog.exec_() == QDialog.Accepted:
            #      value_input = self.value_input.text()
            #      tolerance_input = self.tolerance_input.text()
            #      unit_input = self.unit_input.text() 

                 
        
        else:
            QMessageBox.warning(self, "Input Error", "Please enter valid data.")
    
    # def store_values():
    #     print(f'store values are {self.value_input.text()}, {self.tolerance_input.text()} , {self.unit_input.text()}')
    #     return [self.value_input.text(), self.tolerance_input.text() , self.unit_input.text()]
    def validate_inputs(self):
        tester = self.tester_input1.text().strip()
        if not tester:
            QMessageBox.warning(self, "Input Error", "Tester cannot be empty.")
            return False
        #checking if the entered values are in the correct format
        if self.model_combo == "DoubleMeters":
            if not self.is_numeric(self.value_input1.text()) or not self.is_numeric(self.tolerance_input1.text()) or not self.is_numeric(self.value_input2.text()) or not self.is_numeric(self.tolerance_input2.text()):
                QMessageBox.warning(self, "Input Error", "Value and Tolerance must be numbers.")
                return False
            if not (self.floating1.text().strip() == "y" or self.floating1.text().strip() == "n" or self.floating2.text().strip() == "y" or self.floating2.text().strip() == "n"):
                QMessageBox.warning(self, "Input Error", "COmpulsory FP should be y or n")
                return False
        else:
             if not self.is_numeric(self.value_input1.text()) or not self.is_numeric(self.tolerance_input1.text()):
                QMessageBox.warning(self, "Input Error", "Value and Tolerance must be numbers.")
                return False
            #  print("floating point values :",self.floating1.text().strip())
             if not(self.floating1.text().strip() == "y" or self.floating1.text().strip() == "n"):
                QMessageBox.warning(self, "Input Error", "COmpulsory FP should be y or n")
                return False
        # if not self.is_time_format(self.stabilization_time_input.text()):
        #     QMessageBox.warning(self, "Input Error", "Stabilization Time must be in HHMMSS format.")
        #     return False

        return True

    @staticmethod
    def is_numeric(value):
        return re.match(r'^-?\d+(\.\d+)?$', value) is not None

    @staticmethod
    def is_time_format(value):
        return re.match(r'^\d{6}$', value) is not None

    def get_inputs(self):
        if self.model_combo.currentText() == "DoubleMeters":
            return {
            "Model": self.model_combo.currentText(),
            "tester1": self.tester_input1.text(),
            "value1": self.value_input1.text(),
            "tolerance1": self.tolerance_input1.text(),
            "unit1": self.unit_input1.text(),
            "floatingPoint1": self.floating1.text(),
            # "tester2": self.tester_input.text(),
            "value2": self.value_input2.text(),
            "tolerance2": self.tolerance_input2.text(),
            "unit2": self.unit_input2.text(),
            "floatingPoint2": self.floating2.text(),
            }
        elif self.model_combo.currentText() == "NO/NC":
            return {
            "Model": self.model_combo.currentText(),
            "tester1": self.tester_input1.text(),
            "value1": self.value_input1.text(),
            "tolerance1": self.tolerance_input1.text(),
            
            "floatingPoint1": self.floating1.text(),
            # "tester2": self.tester_input.text(),
            }
        else :
            return {
            "Model": self.model_combo.currentText(),
            "tester1": self.tester_input1.text(),
            "value1": self.value_input1.text(),
            "tolerance1": self.tolerance_input1.text(),
            "unit1": self.unit_input1.text(),
            "floatingPoint1": self.floating1.text(),
            # "tester2": self.tester_input.text(),
            
            
            }
class AddTestDialogmeters(QDialog): #original addtest
    values_from_add_test = pyqtSignal(float,float,str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Test")
        self.layout = QFormLayout(self)
        # self.model_combo = QComboBox()
        # self.model_combo.addItems(["SingleMultiMeter", "LuxMeter", "DoubleMeters"])
        # self.model_combo.setCurrentIndex(0)
        # Input fields for test details
        self.tester_input1 = QLineEdit()
        self.value_input1 = QLineEdit()
        self.tolerance_input1 = QLineEdit()
        self.unit_input1 = QLineEdit()
        # self.tester_input = QLineEdit()
        self.value_input2 = QLineEdit()
        self.tolerance_input2 = QLineEdit()
        self.unit_input2 = QLineEdit()
        # self.stabilization_time_input = QLineEdit()

        # current_time = datetime.now().strftime("%H%M%S")
        # self.stabilization_time_input.setText(current_time)
        # self.layout.addRow("Model", self.model_combo)
        self.layout.addRow("Tester :", self.tester_input1)
        self.layout.addRow("Value 1:", self.value_input1)
        self.layout.addRow("Tolerance 1:", self.tolerance_input1)
        self.layout.addRow("Unit 1:", self.unit_input1)
        # self.layout.addRow("Enter meter 2 values")
        # self.layout.addRow("Tester 2:", self.tester_input)
        self.layout.addRow("Value 2:", self.value_input2)
        self.layout.addRow("Tolerance 2:", self.tolerance_input2)
        self.layout.addRow("Unit 2:", self.unit_input2)
        # Button box for dialog actions
        buttons = QDialogButtonBox()
        buttons.addButton("Add", QDialogButtonBox.AcceptRole)
        buttons.addButton("Cancel", QDialogButtonBox.RejectRole)
        buttons.accepted.connect(self.on_accept)
        buttons.rejected.connect(self.reject)

        self.layout.addRow(buttons)

    def keyPressEvent(self, event):
        # Get the currently focused widget
        focus_widget = self.focusWidget()

        if isinstance(focus_widget, QLineEdit):
            key = event.key()
            if key == 16777219:  # Backspace
                focus_widget.backspace()
            elif key == 16777220:  # Enter
                self.on_accept()
            elif key == 16777221:  # Escape
                self.reject()
            elif key == 46:  # Decimal point (.)
                focus_widget.insert('.')
            elif 48 <= key <= 57:  # Number keys 0-9
                focus_widget.insert(chr(key))

    def on_accept(self):
        if self.validate_inputs():
            # global value_input = self.value_input.text() , tolerance_input = self.tolerance_input.text() , unit_input = self.unit_input.text()
            # print(f'add test values are {value_input} , {tolerance_input}, {unit_input}')
            self.accept()
            # add_test_dialog = AddTestDialog()
            # if add_test_dialog.exec_() == QDialog.Accepted:
            #      value_input = self.value_input.text()
            #      tolerance_input = self.tolerance_input.text()
            #      unit_input = self.unit_input.text() 

                 
        
        else:
            QMessageBox.warning(self, "Input Error", "Please enter valid data.")
    
    # def store_values():
    #     print(f'store values are {self.value_input.text()}, {self.tolerance_input.text()} , {self.unit_input.text()}')
    #     return [self.value_input.text(), self.tolerance_input.text() , self.unit_input.text()]
    def validate_inputs(self):
        tester = self.tester_input1.text().strip()
        if not tester:
            QMessageBox.warning(self, "Input Error", "Tester cannot be empty.")
            return False
        #checking if the entered values are in the correct format
        if not self.is_numeric(self.value_input1.text()) or not self.is_numeric(self.tolerance_input1.text()) or not self.is_numeric(self.value_input2.text()) or not self.is_numeric(self.tolerance_input2.text()):
            QMessageBox.warning(self, "Input Error", "Value and Tolerance must be numbers.")
            return False

        # if not self.is_time_format(self.stabilization_time_input.text()):
        #     QMessageBox.warning(self, "Input Error", "Stabilization Time must be in HHMMSS format.")
        #     return False

        return True

    @staticmethod
    def is_numeric(value):
        return re.match(r'^-?\d+(\.\d+)?$', value) is not None

    @staticmethod
    def is_time_format(value):
        return re.match(r'^\d{6}$', value) is not None

    def get_inputs(self):
        return {
            "tester1": self.tester_input1.text(),
            "value1": self.value_input1.text(),
            "tolerance1": self.tolerance_input1.text(),
            "unit1": self.unit_input1.text(),
            # "tester2": self.tester_input.text(),
            "value2": self.value_input2.text(),
            "tolerance2": self.tolerance_input2.text(),
            "unit2": self.unit_input2.text(),
            
        }