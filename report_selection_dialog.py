import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QPushButton, QLabel, 
    QHBoxLayout, QMessageBox, QFrame
)
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal

class ReportSelectionDialog(QDialog):
    # Define the signal to emit when a report is selected
    report_selected = pyqtSignal(str)

    def __init__(self, reports_folder, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Report")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #1E1E1E; color: white;")
        self.reports_folder = reports_folder

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("Select a Report")
        title_label.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Report List
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("background-color: #2B2B2B; color: white; border: none; border-radius: 5px;")
        layout.addWidget(self.list_widget)

        # Populate the list with Excel files from the reports folder
        self.populate_reports()

        # Button Layout
        button_layout = QHBoxLayout()

        confirm_button = QPushButton("Open Report")
        confirm_button.clicked.connect(self.open_report)
        confirm_button.setStyleSheet("background-color: #2980B9; color: white; border: none; border-radius: 5px; padding: 10px;")
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("background-color: #C0392B; color: white; border: none; border-radius: 5px; padding: 10px;")

        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)

        for button in button_layout.children():
            button.setMinimumWidth(100)

        layout.addLayout(button_layout)

        # Footer
        footer = QFrame()
        footer.setStyleSheet("background-color: #3B3B3B; height: 2px;")
        layout.addWidget(footer)

        self.setLayout(layout)

    def populate_reports(self):
        self.list_widget.clear()  # Clear the list widget
        try:
            files = os.listdir(self.reports_folder)
            if not files:
                QMessageBox.warning(self, "No Reports", "No reports found in the specified folder.", QMessageBox.Ok)
                self.reject()
                return
            
            for file_name in files:
                if file_name.endswith(('.xlsx', '.xls')):  # Check for Excel files
                    self.list_widget.addItem(file_name)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Reports folder not found.", QMessageBox.Ok)

    def open_report(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            file_path = os.path.join(self.reports_folder, selected_item.text())
            self.report_selected.emit(file_path)  # Emit the signal with the selected file path
            self.accept()  # Close the dialog
        else:
            QMessageBox.warning(self, "Warning", "Please select a report to open.")
