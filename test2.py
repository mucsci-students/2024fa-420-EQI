from PyQt5 import QtWidgets

class CustomInputDialog(QtWidgets.QDialog):
    def __init__(self, title="Input Dialog"):
        super().__init__()
        self.setWindowTitle(title)
        self.input_widgets = {}  # Store all input widgets for retrieval
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

    def add_input(self, label_text, widget_type, options=None):
        """
        Abstract method to add various types of input fields to the dialog.

        Parameters:
        - label_text (str): The label text for the input.
        - widget_type (str): Type of the widget ('combo', 'line', etc.).
        - options (list): Optional list of options for combo boxes.

        Returns:
        - QWidget: The created input widget.
        """
        label = QtWidgets.QLabel(label_text)
        self.layout.addWidget(label)
        
        if widget_type == 'combo':
            combo_box = QtWidgets.QComboBox()
            if options:
                combo_box.addItems(options)
            self.layout.addWidget(combo_box)
            return combo_box
        
        elif widget_type == 'line':
            line_edit = QtWidgets.QLineEdit()
            self.layout.addWidget(line_edit)
            return line_edit
        
        # Add more widget types as needed (e.g., checkboxes, date pickers)
        # Example for a checkbox:
        elif widget_type == 'checkbox':
            checkbox = QtWidgets.QCheckBox()
            self.layout.addWidget(checkbox)
            return checkbox

    def add_field_popup(self, class_list):
        """
        Example: Creates a dialog for adding a field.
        Uses the abstract method to dynamically create inputs.
        """
        class_combo_box = self.add_input("Select Class:", widget_type="combo", options=class_list)
        field_name_input = self.add_input("Enter Field Name:", widget_type="line")
        
        # Store the widgets for later use
        self.input_widgets['class_combo_box'] = class_combo_box
        self.input_widgets['field_name_input'] = field_name_input
        
        self.add_buttons()

    def add_method_popup(self, class_list):
        """
        Example: Creates a dialog for adding a method.
        Uses the abstract method to dynamically create inputs.
        """
        class_combo_box = self.add_input("Select Class:", widget_type="combo", options=class_list)
        method_name_input = self.add_input("Enter Method Name:", widget_type="line")
        
        # Store the widgets for later use
        self.input_widgets['class_combo_box'] = class_combo_box
        self.input_widgets['method_name_input'] = method_name_input
        
        self.add_buttons()

    def add_buttons(self):
        """
        Helper function to add OK and Cancel buttons.
        """
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

    def get_inputs(self):
        """
        Retrieve input values based on the stored widgets.
        """
        inputs = {}
        for key, widget in self.input_widgets.items():
            if isinstance(widget, QtWidgets.QComboBox):
                inputs[key] = widget.currentText()
            elif isinstance(widget, QtWidgets.QLineEdit):
                inputs[key] = widget.text()
        return inputs

# Example usage
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    dialog = CustomInputDialog(title="Add Field")
    
    # Example 1: Add Field
    dialog.add_field_popup(class_list=["Class1", "Class2", "Class3"])
    
    if dialog.exec_() == QtWidgets.QDialog.Accepted:
        inputs = dialog.get_inputs()
        print(f"Selected Class: {inputs['class_combo_box']}, Entered Field: {inputs['field_name_input']}")
    
    sys.exit(app.exec_())
