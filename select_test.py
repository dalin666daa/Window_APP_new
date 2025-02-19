from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QScrollArea, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt
from test_detail import TestDetailDialog  # Import the TestDetailDialog

class SelectTestFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #333333; border-radius: 10px; padding: 20px;")

        # Create a scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Create a container frame with a grid layout for the test cards
        self.container = QFrame()
        self.container_layout = QGridLayout(self.container)
        self.scroll_area.setWidget(self.container)

        # Main layout for the SelectTestFrame
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

        self.tests = []

    def display_tests(self, tests):
        """Display the list of tests in cards."""
        self.tests = tests
        self.clear_existing_cards()

        if not tests:
            self.container_layout.addWidget(QLabel("No tests available.", self), 0, 0)
            return

        row, col = 0, 0
        columns = self.calculate_columns()  # Calculate columns dynamically based on size
        for index, test in enumerate(tests):
            test_card = self.create_test_card(test, index)
            self.container_layout.addWidget(test_card, row, col)

            col += 1
            if col >= columns:
                col = 0
                row += 1

    def clear_existing_cards(self):
        """Remove all existing test cards from the layout."""
        for i in reversed(range(self.container_layout.count())):
            self.container_layout.itemAt(i).widget().setParent(None)

    def create_test_card(self, test, index):
        """Create a card for a single test."""
        test_card = QFrame()
        test_card.setStyleSheet("""
            background-color: #333333; 
            border-radius: 10px; 
            padding: 15px; 
            margin: 5px; 
        """)
        test_card.setFixedWidth(250)
        test_card.setMinimumHeight(150)

        # Safely get test details
        model = test.get('Model', 'N/A')
        tester = test.get('tester1', 'N/A')
        value = test.get('value1', 'N/A')
        tolerance = test.get('tolerance1', 'N/A')
        # stabilization_time = test.get('stabilization_time', 'N/A')
        # print(f" select test frame values : {model},{tester},{value},{tolerance}")
        test_details = (
            f"Model: {model}\n"
            f"Tester: {tester}\n"
            f"Value: {value}\n"
            f"Tolerance: {tolerance}\n"
            # f"Stabilization Time: {stabilization_time}"
        )
        test_label = QLabel(test_details, test_card)
        test_label.setStyleSheet("color: white; font-size: 14px;")

        test_layout = QVBoxLayout()
        test_layout.addWidget(test_label)
        test_card.setLayout(test_layout)

        # Connect mouse click to show details
        test_card.mousePressEvent = lambda event: self.handle_card_click(index)

        # Add hover effect
        test_card.setMouseTracking(True)
        test_card.enterEvent = lambda event: self.update_card_style_on_hover(test_card, True)
        test_card.leaveEvent = lambda event: self.update_card_style_on_hover(test_card, False)
        test_card.setCursor(Qt.PointingHandCursor)

        return test_card

    def handle_card_click(self, index):
        """Handle click event on a test card."""
        test = self.tests[index]  # Get the selected test
        try:
            detail_dialog = TestDetailDialog(test, self.parent())  # Pass the parent here
            detail_dialog.exec_()  # Show the dialog modally
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open test details: {e}")

    def update_card_style_on_hover(self, card, hover):
        """Update card style based on hover state."""
        card.setStyleSheet("background-color: #5f9403;" if hover else "background-color: #76B900;")

    def calculate_columns(self):
        """Calculate the number of columns based on the available width."""
        available_width = self.scroll_area.width()  # Get the width of the scroll area
        column_width = 250  # Width of each test card
        return max(1, available_width // column_width)  # Ensure at least one column
