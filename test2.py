import sys
from PyQt5 import QtWidgets, QtCore

class CustomInputDialog(QtWidgets.QDialog):
    def __init__(self, title="Input Dialog"):
        super().__init__()
        self.setWindowTitle(title)
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        
        self.input_widgets = {}  # Store all input widgets for retrieval
        self.selected_option = None  # To track the selected option
    
    def change_data_type_popup(self, selected_class, class_name_list, relationship_list, type_list):
        """
        Creates a dialog for changing data types of fields, methods, parameters, or relationships.
        """
        # Step 1: Add Radio Buttons for Options
        self.option_group = QtWidgets.QButtonGroup(self)
        self.option_layout = QtWidgets.QHBoxLayout()
        
        self.field_radio = QtWidgets.QRadioButton("Field")
        self.method_radio = QtWidgets.QRadioButton("Method")
        self.param_radio = QtWidgets.QRadioButton("Parameter")
        self.rel_radio = QtWidgets.QRadioButton("Relationship")
        
        self.option_group.addButton(self.field_radio)
        self.option_group.addButton(self.method_radio)
        self.option_group.addButton(self.param_radio)
        self.option_group.addButton(self.rel_radio)
        
        self.option_layout.addWidget(self.field_radio)
        self.option_layout.addWidget(self.method_radio)
        self.option_layout.addWidget(self.param_radio)
        self.option_layout.addWidget(self.rel_radio)
        
        self.layout.addLayout(self.option_layout)
        
        # Step 2: Create Stacked Widget to Hold Different Input Forms
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.layout.addWidget(self.stacked_widget)
        
        # Step 3: Create Input Forms for Each Option
        self.field_widget = self.__create_field_widget(selected_class)
        self.method_widget = self.__create_method_widget(selected_class)
        self.param_widget = self.__create_param_widget(selected_class)
        self.rel_widget = self.__create_relationship_widget(selected_class, class_name_list, relationship_list, type_list)
        
        self.stacked_widget.addWidget(self.field_widget)
        self.stacked_widget.addWidget(self.method_widget)
        self.stacked_widget.addWidget(self.param_widget)
        self.stacked_widget.addWidget(self.rel_widget)
        
        # Step 4: Connect Radio Buttons to Update the Stacked Widget
        self.field_radio.toggled.connect(lambda: self.__update_stacked_widget())
        self.method_radio.toggled.connect(lambda: self.__update_stacked_widget())
        self.param_radio.toggled.connect(lambda: self.__update_stacked_widget())
        self.rel_radio.toggled.connect(lambda: self.__update_stacked_widget())
        
        # Step 5: Add OK and Cancel Buttons
        self.__add_buttons()
        
        # Step 6: Initialize by Selecting the First Option
        self.field_radio.setChecked(True)
        self.__update_stacked_widget()
    
    def __update_stacked_widget(self):
        """
        Updates the stacked widget based on the selected radio button.
        """
        if self.field_radio.isChecked():
            self.stacked_widget.setCurrentWidget(self.field_widget)
            self.selected_option = "field"
        elif self.method_radio.isChecked():
            self.stacked_widget.setCurrentWidget(self.method_widget)
            self.selected_option = "method"
        elif self.param_radio.isChecked():
            self.stacked_widget.setCurrentWidget(self.param_widget)
            self.selected_option = "param"
        elif self.rel_radio.isChecked():
            self.stacked_widget.setCurrentWidget(self.rel_widget)
            self.selected_option = "rel"
    
    def __create_field_widget(self, selected_class):
        """
        Creates the input form for changing the data type of a field.
        """
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout()
        widget.setLayout(layout)
        
        # Field selection
        field_names = [field_key[1] for field_key in selected_class['fields']]
        field_combo = QtWidgets.QComboBox()
        field_combo.addItems(field_names)
        
        # New type input
        new_type_line = QtWidgets.QLineEdit()
        
        layout.addRow("Select Field:", field_combo)
        layout.addRow("New Type:", new_type_line)
        
        # Store widgets specific to this option
        self.field_input_widgets = {}
        self.field_input_widgets["field_name"] = field_combo
        self.field_input_widgets["field_new_type"] = new_type_line
        
        return widget
    
    def __create_method_widget(self, selected_class):
        """
        Creates the input form for changing the return type of a method.
        """
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout()
        widget.setLayout(layout)
        
        # Method selection
        method_names = [method['name'] for method in selected_class['methods']]
        method_combo = QtWidgets.QComboBox()
        method_combo.addItems(method_names)
        
        # New type input
        new_type_line = QtWidgets.QLineEdit()
        
        layout.addRow("Select Method:", method_combo)
        layout.addRow("New Return Type:", new_type_line)
        
        # Store widgets specific to this option
        self.method_input_widgets = {}
        self.method_input_widgets["method_name"] = method_combo
        self.method_input_widgets["method_new_type"] = new_type_line
        
        return widget
    
    def __create_param_widget(self, selected_class):
        """
        Creates the input form for changing the data type of a parameter.
        """
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout()
        widget.setLayout(layout)
        
        # Method selection
        method_names = [method['name'] for method in selected_class['methods']]
        method_combo = QtWidgets.QComboBox()
        method_combo.addItems(method_names)
        
        # Parameter selection (initially based on the first method)
        first_method_params = selected_class['methods'][0]['parameters']
        param_names = [param['name'] for param in first_method_params]
        param_combo = QtWidgets.QComboBox()
        param_combo.addItems(param_names)
        
        # Update param_combo when method_combo changes
        method_combo.currentIndexChanged.connect(lambda: self.__update_param_combo(selected_class, method_combo, param_combo))
        
        # New type input
        new_type_line = QtWidgets.QLineEdit()
        
        layout.addRow("Select Method:", method_combo)
        layout.addRow("Select Parameter:", param_combo)
        layout.addRow("New Type:", new_type_line)
        
        # Store widgets specific to this option
        self.param_input_widgets = {}
        self.param_input_widgets["param_method_name"] = method_combo
        self.param_input_widgets["param_name"] = param_combo
        self.param_input_widgets["param_new_type"] = new_type_line
        
        return widget
    
    def __create_relationship_widget(self, selected_class, class_name_list, relationship_list, type_list):
        """
        Creates the input form for changing the type of a relationship.
        """
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout()
        widget.setLayout(layout)
        
        # Source class (current class)
        source_class_line = QtWidgets.QLineEdit()
        source_class_line.setText(selected_class['name'])
        source_class_line.setReadOnly(True)
        
        # Destination class selection
        # Get relationships from the selected class
        source_class_name = selected_class['name']
        dest_classes = [rel['destination'] for rel in relationship_list if rel['source'] == source_class_name]
        dest_combo = QtWidgets.QComboBox()
        dest_combo.addItems(dest_classes)
        
        # New type selection
        type_combo = QtWidgets.QComboBox()
        type_combo.addItems(type_list)
        
        layout.addRow("Source Class:", source_class_line)
        layout.addRow("Destination Class:", dest_combo)
        layout.addRow("New Relationship Type:", type_combo)
        
        # Store widgets specific to this option
        self.rel_input_widgets = {}
        self.rel_input_widgets["rel_source_class"] = source_class_line
        self.rel_input_widgets["rel_dest_class"] = dest_combo
        self.rel_input_widgets["rel_new_type"] = type_combo
        
        return widget
    
    def __update_param_combo(self, selected_class, method_combo, param_combo):
        """
        Updates the parameter combo box based on the selected method.
        """
        selected_method_name = method_combo.currentText()
        # Find the selected method
        selected_method = next((method for method in selected_class['methods'] if method['name'] == selected_method_name), None)
        if selected_method:
            params = selected_method.get('parameters', [])
            param_names = [param['name'] for param in params]
            param_combo.clear()
            param_combo.addItems(param_names)
    
    def __add_buttons(self):
        """
        Helper function to add OK and Cancel buttons.
        """
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

    def get_selected_inputs(self):
        """
        Returns the input widgets corresponding to the selected option.
        """
        if self.selected_option == "field":
            return self.field_input_widgets
        elif self.selected_option == "method":
            return self.method_input_widgets
        elif self.selected_option == "param":
            return self.param_input_widgets
        elif self.selected_option == "rel":
            return self.rel_input_widgets
        else:
            return {}

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynamic Dialog Test")
        self.resize(400, 200)
        
        # Mock data for testing
        self.selected_class = {
            'name': 'ExampleClass',
            'fields': [('int', 'field1'), ('string', 'field2')],
            'methods': [
                {'name': 'method1', 'return_type': 'void', 'parameters': [{'type': 'int', 'name': 'param1'}, {'type': 'string', 'name': 'param2'}]},
                {'name': 'method2', 'return_type': 'int', 'parameters': [{'type': 'float', 'name': 'param3'}]}
            ]
        }
        self.class_name_list = ['ExampleClass', 'OtherClass']
        self.relationship_list = [
            {'source': 'ExampleClass', 'destination': 'OtherClass', 'type': 'Inheritance'},
            {'source': 'ExampleClass', 'destination': 'ThirdClass', 'type': 'Association'}
        ]
        self.type_list = ['Aggregation', 'Composition', 'Inheritance', 'Realization']
        
        # Create a central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout for central widget
        layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Button to open the dialog
        self.open_dialog_button = QtWidgets.QPushButton("Open Change Data Type Dialog")
        self.open_dialog_button.clicked.connect(self.open_change_data_type_dialog)
        layout.addWidget(self.open_dialog_button)
        
        # Text edit to display results
        self.result_text = QtWidgets.QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
    
    def open_change_data_type_dialog(self):
        # Initialize the dialog
        change_type_dialog = CustomInputDialog("Change Data Type")
        change_type_dialog.change_data_type_popup(self.selected_class, self.class_name_list, self.relationship_list, self.type_list)
        
        # Execute the dialog and wait for user confirmation (OK or Cancel)
        if change_type_dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Get the inputs corresponding to the selected option
            selected_inputs = change_type_dialog.get_selected_inputs()
            selected_option = change_type_dialog.selected_option
            
            # Process inputs based on the selected option
            if selected_option == "field":
                field_name = selected_inputs["field_name"].currentText()
                new_type = selected_inputs["field_new_type"].text()
                self.result_text.append(f"Field '{field_name}' type changed to '{new_type}'.")
                # Here you would call your model method to change the field type
                
            elif selected_option == "method":
                method_name = selected_inputs["method_name"].currentText()
                new_type = selected_inputs["method_new_type"].text()
                self.result_text.append(f"Method '{method_name}' return type changed to '{new_type}'.")
                # Here you would call your model method to change the method return type
                
            elif selected_option == "param":
                method_name = selected_inputs["param_method_name"].currentText()
                param_name = selected_inputs["param_name"].currentText()
                new_type = selected_inputs["param_new_type"].text()
                self.result_text.append(f"Parameter '{param_name}' in method '{method_name}' type changed to '{new_type}'.")
                # Here you would call your model method to change the parameter type
                
            elif selected_option == "rel":
                source_class = selected_inputs["rel_source_class"].text()
                dest_class = selected_inputs["rel_dest_class"].currentText()
                new_type = selected_inputs["rel_new_type"].currentText()
                self.result_text.append(f"Relationship from '{source_class}' to '{dest_class}' type changed to '{new_type}'.")
                # Here you would call your model method to change the relationship type

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
