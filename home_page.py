import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QStackedWidget,
    QPushButton, QFrame, QLabel, QHBoxLayout, QDialog
)
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from login import LoginWindow
from reports import ReportsPage
from report_selection_dialog import ReportSelectionDialog

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-PROBE")
        self.setGeometry(100, 100, 1280, 800)
        self.setStyleSheet("background-color: #1E1E1E;")

        self.stacked_widget = QStackedWidget(self)
        self.home_page = QWidget()
        self.reports_page = ReportsPage()

        self.init_home_page()

        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.reports_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def init_home_page(self):
        layout = QVBoxLayout()
        layout.addWidget(self.create_title_card())
        layout.addLayout(self.create_second_card_layout())
        self.home_page.setLayout(layout)

    def create_title_card(self):
        title_card = QFrame()
        title_card.setStyleSheet("background-color: #3B3B3B; border-radius: 10px; padding: 20px;")

        title_label = QLabel("AI-PROBE", title_card)
        title_label.setFont(QtGui.QFont("Arial", 36, QtGui.QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white;")

        subheading_label = QLabel("enProducts", title_card)
        subheading_label.setFont(QtGui.QFont("Arial", 18))
        subheading_label.setAlignment(Qt.AlignCenter)
        subheading_label.setStyleSheet("color: #D9E3E0;")

        title_layout = QVBoxLayout()
        title_layout.addWidget(title_label)
        title_layout.addWidget(subheading_label)

        title_card.setLayout(title_layout)
        return title_card

    def create_second_card_layout(self):
        second_card_layout = QHBoxLayout()
        graph_card = self.create_graph_card()
        button_card = self.create_button_card()
        second_card_layout.addWidget(graph_card)
        second_card_layout.addWidget(button_card)
        return second_card_layout

    def create_graph_card(self):
        graph_card = QFrame()
        graph_card.setStyleSheet("background-color: #2B2B2B; border-radius: 10px; padding: 20px;")
        
        graph_widget = QLabel("Graph Widget Placeholder")
        graph_layout = QVBoxLayout()
        graph_layout.addWidget(graph_widget)
        graph_card.setLayout(graph_layout)
        return graph_card

    def create_button_card(self):
        button_card = QFrame()
        button_card.setStyleSheet("background-color: #3B3B3B; border-radius: 10px; padding: 20px;")
        button_layout = QVBoxLayout()

        login_button = self.create_button("Login", '#2980B9', self.on_login)
        reports_button = self.create_button("Report", '#2980B9', self.on_select_report)
        quit_button = self.create_button("Quit", '#27AE60', self.on_quit)

        button_layout.addWidget(login_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(reports_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(quit_button, alignment=Qt.AlignCenter)

        button_card.setLayout(button_layout)
        return button_card

    def create_button(self, text, color, callback):
        button = QPushButton(text)
        button.setStyleSheet(f"background-color: {color}; color: white; padding: 10px; border: none; border-radius: 5px;")
        button.setFont(QtGui.QFont("Arial", 24))
        button.setMinimumSize(200, 60)
        button.clicked.connect(callback)
        return button

    def on_login(self):
        login_window = LoginWindow()
        if login_window.exec_() == QDialog.Accepted:
            # Navigate to master page if implemented
            pass

    def on_select_report(self):
        dialog = ReportSelectionDialog(reports_folder='reports/', parent=self)
        dialog.report_selected.connect(self.on_report_selected)
        dialog.exec_()

    def on_report_selected(self, file_path):
        try:
            self.reports_page.load_reports(file_path)
            self.stacked_widget.setCurrentWidget(self.reports_page)
        except Exception as e:
            print(f"Error loading report: {e}")

    def on_quit(self):
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())
