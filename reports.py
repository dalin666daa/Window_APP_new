from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox, QScrollArea, QFrame, QPushButton
import pandas as pd

class ReportsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Back button
        self.back_button = QPushButton("Back to Home")
        self.back_button.setStyleSheet("background-color: #C0392B; color: white; border: none; border-radius: 5px; padding: 10px;")
        self.back_button.clicked.connect(self.go_back)
        
        # Add the back button to the layout at the top
        self.layout.addWidget(self.back_button)

    def load_reports(self, file_path):
        try:
            # Read the Excel file
            data = pd.read_excel(file_path)

            # Clear previous contents except back button
            for i in reversed(range(self.layout.count())): 
                widget = self.layout.itemAt(i).widget()
                if widget is not None and widget != self.back_button:  
                    widget.deleteLater()

            # Display the report header
            header_label = QLabel(f"Loaded Report: {file_path}")
            header_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
            self.layout.addWidget(header_label)

            # Create a scroll area for the data
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_content = QFrame()
            scroll_layout = QVBoxLayout(scroll_content)

            # Convert DataFrame to HTML and create a QLabel for it
            data_html = data.to_html(index=False, border=0)  # Adjust border for a cleaner look
            data_label = QLabel(data_html)
            data_label.setStyleSheet("background-color: #2B2B2B; color: white; padding: 10px; border-radius: 5px;")
            data_label.setOpenExternalLinks(True)  # Make links clickable, if any

            scroll_layout.addWidget(data_label)
            scroll_content.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_content)
            self.layout.addWidget(scroll_area)

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "The report file was not found.")
        except pd.errors.EmptyDataError:
            QMessageBox.warning(self, "Error", "The report file is empty.")
        except Exception as e:
            print(f"Error loading report: {e}")
            QMessageBox.warning(self, "Error", f"Failed to load report: {e}")

    def go_back(self):
        self.parent().setCurrentIndex(0)  # Switch to the home page
