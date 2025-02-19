from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QDialog, QMessageBox
from PyQt5 import QtGui
from add_test import AddTestDialogmeters,AddTestDialogmeters_latest#AddTestDialog
from delete_test_dialog import DeleteTestDialog
from running_test_page import RunningTestPage
from select_test import SelectTestFrame
from tests_manager import TestsManager
from add_user import AddUserDialog
from users_manager import UsersManager
from confirm_user_dialog import ConfirmUserDialog

class MasterPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1E1E1E;")
        self.init_ui()
        self.tests_manager = TestsManager()
        self.users_manager = UsersManager()
        # self.model = YOLO(r"D:\best_lux_meter_inc_2_11_24.pt")# newly added on 2_11_24
        # self.ocr1 = PaddleOCR(use_angle_cls=False, lang='en',show_log=False)
        # self.ocr2 = PaddleOCR(use_angle_cls=False, lang='en',show_log=False)
        # store_values()
    # def model(self):
    #     return self.model
    # def ocr1(self):
    #     return self.ocr1
    # def ocr2(self):
    #     return self.ocr2

    def init_ui(self):
        layout = QHBoxLayout()
        left_card = QFrame()
        left_card.setStyleSheet("background-color: #3B3B3B; border-radius: 10px; padding: 20px;")
        left_layout = QVBoxLayout()

        button_labels = [
            "SELECT TEST", "DELETE TEST", "ADD TEST",
            "ADD USER", "DELETE USER", "HELP",
            "LOG OUT", "QUIT"
        ]

        self.button_actions = [
            self.display_tests, self.delete_test, self.add_test,
            self.add_user, self.delete_user, self.show_help,
            self.logout, self.close
        ]

        for i, label in enumerate(button_labels):
            button = QPushButton(label)
            button.setStyleSheet("""
                                     background-color: #76B900; 
                                    color: white; 
                                    padding: 10px; 
                                    border: white; 
                                    font-weight: bold; /* Make the text bold */
                                    border-radius: 5px; 
                                    font-size: 16px;  /* Adjust the size as needed */
                                    height: 50px;     /* Set a fixed height */
                                    width: 150px;     /* Set a fixed width */
                                """)
            button.clicked.connect(lambda checked, index=i: self.on_button_clicked(index))
            left_layout.addWidget(button)

        left_card.setLayout(left_layout)
        self.select_test_frame = SelectTestFrame()

        layout.addWidget(left_card, 1)
        layout.addWidget(self.select_test_frame, 3)

        self.setLayout(layout)

    def on_button_clicked(self, index):
        if self.button_actions[index]:
            self.button_actions[index]()

    def display_tests(self):
        tests = self.tests_manager.get_tests()
        self.select_test_frame.display_tests(tests)

    def add_test(self):

        # dialog = AddTestDialog()
        # dialog = AddTestDialogmeters()
        dialog = AddTestDialogmeters_latest()

        if dialog.exec_() == QDialog.Accepted:
            test_info = dialog.get_inputs()
            self.tests_manager.add_test(test_info)
            self.display_tests()
            # print(f'test info ::',test_info)
            # return test_info

    def add_user(self):
        dialog = AddUserDialog()
        if dialog.exec_() == QDialog.Accepted:
            user_info = dialog.get_user_info()
            confirm_dialog = ConfirmUserDialog(user_info)
            if confirm_dialog.exec_() == QDialog.Accepted:
                self.users_manager.add_user(user_info)
                QMessageBox.information(self, "Success", "User added successfully.")
                store_values()

    def delete_test(self):
        tests = self.tests_manager.get_tests()
        if not tests:
            QMessageBox.warning(self, "Delete Test", "No tests available to delete.", QMessageBox.Ok)
            return

        dialog = DeleteTestDialog(tests)
        if dialog.exec_() == QDialog.Accepted:
            test_index = dialog.get_test_to_delete()
            if test_index is not None:
                self.tests_manager.tests.pop(test_index)
                self.display_tests()

    def delete_user(self):
        # Implement user deletion logic here
        QMessageBox.warning(self, "Delete User", "User deletion functionality is not implemented yet.", QMessageBox.Ok)

    def show_help(self):
        # Implement help dialog or documentation display here
        QMessageBox.information(self, "Help", "Help documentation is not implemented yet.", QMessageBox.Ok)

    def logout(self):
        # Handle logout logic here
        QMessageBox.information(self, "Logged Out", "You have been logged out successfully.")

    def show_running_test(self, test):
        self.clear_layout()
        running_test_page = RunningTestPage(test, self.show_test_selection)
        self.layout().addWidget(running_test_page)

    def show_test_selection(self):
        self.clear_layout()
        self.select_test_frame = SelectTestFrame()
        self.layout().addWidget(self.select_test_frame)
        self.display_tests()

    def clear_layout(self):
        while self.layout().count():
            widget = self.layout().takeAt(0).widget()
            if widget is not None:
                widget.deleteLater()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MasterPage()
    window.setWindowTitle("Test Manager - AI-PROBE")
    # window.resize(1200, 600)
    window.setWindowIcon(QtGui.QIcon('icon.ico'))  # Set your application icon
    window.show()
    sys.exit(app.exec_())
