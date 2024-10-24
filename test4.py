import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QListWidget, QLabel

class SearchApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # List of strings to search from
        self.items = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape"]
        
        # Create the search bar (QLineEdit)
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.update_list)  # Connect to search function

        # Create the list widget to display the search results
        self.result_list = QListWidget(self)
        self.update_list()  # Populate the list with all items initially

        # Layout for widgets
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Search fruits:"))
        layout.addWidget(self.search_bar)
        layout.addWidget(self.result_list)

        self.setLayout(layout)
        self.setWindowTitle("Simple Search App")

    # Update list based on search query
    def update_list(self):
        search_text = self.search_bar.text().lower()  # Get text from search bar and convert to lowercase
        self.result_list.clear()  # Clear previous results

        # Filter items that match the search text
        for item in self.items:
            if search_text in item.lower():  # Case-insensitive search
                self.result_list.addItem(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SearchApp()
    window.show()
    sys.exit(app.exec_())
