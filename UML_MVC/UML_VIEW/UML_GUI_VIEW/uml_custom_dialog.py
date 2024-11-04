from PyQt5 import QtWidgets
import re

class CustomInputDialog(QtWidgets.QDialog):
    def __init__(self, title="Input Dialog"):
        super().__init__()
        self.setWindowTitle(title)
        self.input_widgets = {}  # Store all input widgets for retrieval
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        
    def add_field_popup(self):
        """
        Creates a dialog for renaming a field.
        """
        # Create input for the new parameter name
        field_type = self.__add_input("Enter field type:", widget_type="line")
        field_name = self.__add_input("Enter field name:", widget_type="line")
        
        # Store the widgets for later use
        self.input_widgets["field_type"] = field_type
        self.input_widgets["field_name"] = field_name
        self.__add_buttons()

    def rename_field_popup(self, selected_class):
        """
        Creates a dialog for renaming a field.
        """
        field_name_list = [field_key[1] for field_key in selected_class.field_key_list]
        old_field_name = self.__add_input("Select Field To Rename:", widget_type="combo", options=field_name_list)
        new_field_name = self.__add_input("Enter New Field Name:", widget_type="line")
        
        # Store the widgets for later use
        self.input_widgets["old_field_name"] = old_field_name
        self.input_widgets["new_field_name"] = new_field_name
        self.__add_buttons()
        
    def edit_field_type_popup(self, selected_class):
        """
        Creates a dialog for renaming a field type.
        """
        field_name_list = [field_key[1] for field_key in selected_class.field_key_list]
        field_name = self.__add_input("Select Field To Edit Type:", widget_type="combo", options=field_name_list)
        new_field_type = self.__add_input("Enter New Type Name:", widget_type="line")
        
        # Store the widgets for later use
        self.input_widgets["field_name"] = field_name
        self.input_widgets["new_field_type"] = new_field_type
        self.__add_buttons()
        
    def add_method_popup(self):
        """
        Creates a dialog for renaming a field.
        """
        # Create input for the new parameter name
        method_type = self.__add_input("Enter method type:", widget_type="line")
        method_name = self.__add_input("Enter method name:", widget_type="line")
        
        # Store the widgets for later use
        self.input_widgets["method_type"] = method_type
        self.input_widgets["method_name"] = method_name
        self.__add_buttons()
        
    def delete_method_popup(self, selected_class):
        """
        Creates a dialog for deleting a method.
        """
        method_display_list = []
        method_keys_list = []
        
        for i, dictionary in enumerate(selected_class.method_list):
            method_key = dictionary["method_key"]
            param_list = dictionary["parameters"]
            # Convert parameter tuples to strings
            param_str_list = [f"{param_type} {param_name}" for param_type, param_name in param_list]
            params_str = ', '.join(param_str_list)
            # Build the display string
            display_str = f"{i + 1}: {method_key[0]} {method_key[1]}({params_str})"
            method_display_list.append(display_str)
            method_keys_list.append(method_key)
        # Show the dialog for selecting the method to remove
        method_name_widget = self.__add_input("Select Method To Rename:", widget_type="combo", options=method_display_list)
        match = re.search(r': (\w+) (\w+)\(', method_name_widget.currentText())
        type_name_tuple = (match.group(1), match.group(2)) if match else (None, None)
        
        # Store the widgets for later use
        self.input_widgets["method_type"] = type_name_tuple[0]
        self.input_widgets["method_name"] = type_name_tuple[1]
        self.input_widgets["raw_method_name"] = method_name_widget
        self.__add_buttons()
        
    def rename_method_popup(self, selected_class):
        """
        Creates a dialog for renaming a method.
        """
        method_display_list = []
        method_keys_list = []
        
        for i, dictionary in enumerate(selected_class.method_list):
            method_key = dictionary["method_key"]
            param_list = dictionary["parameters"]
            # Convert parameter tuples to strings
            param_str_list = [f"{param_type} {param_name}" for param_type, param_name in param_list]
            params_str = ', '.join(param_str_list)
            # Build the display string
            display_str = f"{i + 1}: {method_key[0]} {method_key[1]}({params_str})"
            method_display_list.append(display_str)
            method_keys_list.append(method_key)
            
        old_method_name = self.__add_input("Select Method To Rename:", widget_type="combo", options=method_display_list)
        new_method_name = self.__add_input("Enter New Method Name:", widget_type="line")
        
        # Store the widgets for later use
        self.input_widgets["raw_method_name"] = old_method_name
        self.input_widgets["new_method_name"] = new_method_name
        self.input_widgets["method_keys_list"] = method_keys_list
        self.__add_buttons()
        
    def edit_method_return_type_popup(self, selected_class):
        """
        Creates a dialog for renaming a method.
        """
        method_display_list = []
        method_keys_list = []
        
        for i, dictionary in enumerate(selected_class.method_list):
            method_key = dictionary["method_key"]
            param_list = dictionary["parameters"]
            # Convert parameter tuples to strings
            param_str_list = [f"{param_type} {param_name}" for param_type, param_name in param_list]
            params_str = ', '.join(param_str_list)
            # Build the display string
            display_str = f"{i + 1}: {method_key[0]} {method_key[1]}({params_str})"
            method_display_list.append(display_str)
            method_keys_list.append(method_key)
  
        method_name = self.__add_input("Select Method To Edit Return Type:", widget_type="combo", options=method_display_list)
        new_method_return_type = self.__add_input("Enter New Method Return Type:", widget_type="line")
        
        # Store the widgets for later use
        self.input_widgets["method_name"] = method_name
        self.input_widgets["new_method_return_type"] = new_method_return_type
        self.input_widgets["method_keys_list"] = method_keys_list
        self.__add_buttons()
        
    def add_param_popup(self, selected_class):
        """
        Creates a dialog for adding a parameter.
        """
        method_names = []
        method_keys = []

        # Build method names and collect method keys
        for i, dictionary in enumerate(selected_class.method_list):
            # Each method_dict is a dictionary with one method
            method_key = dictionary["method_key"]
            param_list = dictionary["parameters"]

            # Build the method name string with parameters
            params_str = ', '.join(f"{param_type} {param_name}" for param_type, param_name in param_list)
            method_name_str = f"{i + 1}: {method_key[0]} {method_key[1]} ({params_str})"
            method_names.append(method_name_str)
            method_keys.append(method_key)

        # Create combo box for methods
        method_name_widget = self.__add_input("Select Method To Add Parameter:", widget_type="combo", options=method_names)
        match = re.search(r': (\w+) (\w+)\(', method_name_widget.currentText())
        type_name_tuple = (match.group(1), match.group(2)) if match else (None, None)
        
        # Create inputs for parameter type and name
        param_type_widget = self.__add_input("Enter Parameter Type:", widget_type="line")
        new_param_name_widget = self.__add_input("Enter New Parameter Name:", widget_type="line")
        
        # Store widgets and data for later use
        self.input_widgets["method_type"] = type_name_tuple[0]
        self.input_widgets["method_name"] = type_name_tuple[1]
        self.input_widgets["param_type"] = param_type_widget
        self.input_widgets["new_param_name"] = new_param_name_widget
        self.input_widgets["method_name_widget"] = method_name_widget

        # Add OK and Cancel buttons
        self.__add_buttons()
        
    def delete_param_popup(self, selected_class):
        """
        Creates a dialog for deleting a parameter from a selected method.
        """
        method_names = []
        method_keys = []

        # Build method names and collect method keys
        for i, dictionary in enumerate(selected_class.method_list):
            method_key = dictionary["method_key"]
            param_list = dictionary["parameters"]
            # Build the method name string with parameters
            params_str = ', '.join(f"{param_type} {param_name}" for param_type, param_name in param_list)
            method_name_str = f"{i + 1}: {method_key[0]} {method_key[1]} ({params_str})"
            method_names.append(method_name_str)
            method_keys.append(method_key)

        # Create combo box for methods
        method_name_widget = self.__add_input("Select Method To Delete Parameter:", widget_type="combo", options=method_names)

        selected_index = method_name_widget.currentIndex()
        chosen_entry = selected_class.method_list[selected_index]

        # Get the parameters for the initially selected method
        param_options = [f"{param_type} {param_name}" for param_type, param_name in chosen_entry["parameters"]]

        param_name_widget = self.__add_input("Select Parameter To Delete:", widget_type="combo", options=param_options)
        
        self.input_widgets["method_name_widget"] = method_name_widget
        self.input_widgets["param_name_widget"] = param_name_widget

        # Initialize 'param_name_only' based on the initial selection
        self.__update_param_name_only(param_name_widget)

        # Add buttons (OK/Cancel)
        self.__add_buttons()

        # Connect the method_name combo box change to update the parameter list dynamically
        method_name_widget.currentIndexChanged.connect(lambda index: self.__update_param_list(selected_class, index, param_name_widget))

        # Connect the param_name_widget change to update 'param_name_only'
        param_name_widget.currentIndexChanged.connect(lambda: self.__update_param_name_only(param_name_widget))
        
    def rename_param_popup(self, selected_class):
        """
        Creates a dialog for renaming a parameter.
        """
        method_names = []
        method_keys = []

        # Build method names and collect method keys
        for i, dictionary in enumerate(selected_class.method_list):
            method_key = dictionary["method_key"]
            param_list = dictionary["parameters"]
            # Build the method name string with parameters
            params_str = ', '.join(f"{param_type} {param_name}" for param_type, param_name in param_list)
            method_name_str = f"{i + 1}: {method_key[0]} {method_key[1]} ({params_str})"
            method_names.append(method_name_str)
            method_keys.append(method_key)

        # Create combo box for methods
        method_name_widget = self.__add_input("Select Method To Change Parameter:", widget_type="combo", options=method_names)
        self.input_widgets["method_name_widget"] = method_name_widget

        selected_index = method_name_widget.currentIndex()
        chosen_entry = selected_class.method_list[selected_index]

        # Get the parameters for the initially selected method
        param_options = [f"{param_type} {param_name}" for param_type, param_name in chosen_entry["parameters"]]

        old_param_name_widget = self.__add_input("Select Parameter To Change:", widget_type="combo", options=param_options)
        new_param_name_widget = self.__add_input("Enter New Parameter:", widget_type="line")
        
        self.input_widgets["method_name_widget"] = method_name_widget
        self.input_widgets["old_param_name_widget"] = old_param_name_widget
        self.input_widgets["new_param_name_widget"] = new_param_name_widget

        # Initialize 'param_name_only' based on the initial selection
        self.__update_param_name_only(old_param_name_widget)

        # Add buttons (OK/Cancel)
        self.__add_buttons()

        # Connect the method_name combo box change to update the parameter list dynamically
        method_name_widget.currentIndexChanged.connect(lambda index: self.__update_param_list(selected_class, index, old_param_name_widget))

        # Connect the param_name_widget change to update 'param_name_only'
        old_param_name_widget.currentIndexChanged.connect(lambda: self.__update_param_name_only(old_param_name_widget))
        
    def replace_param_list_popup(self, selected_class):
        """
        Creates a dialog for replacing parameter list.
        """
        method_names = []
        method_keys = []

        # Build method names and collect method keys
        for i, dictionary in enumerate(selected_class.method_list):
            method_key = dictionary["method_key"]
            param_list = dictionary["parameters"]
            # Build the method name string with parameters
            params_str = ', '.join(f"{param_type} {param_name}" for param_type, param_name in param_list)
            method_name_str = f"{i + 1}: {method_key[0]} {method_key[1]} ({params_str})"
            method_names.append(method_name_str)
            method_keys.append(method_key)

        # Create combo box for methods
        method_name_widget = self.__add_input("Select Method To Replace Parameter List:", widget_type="combo", options=method_names)
        self.input_widgets["method_name_widget"] = method_name_widget
        
        # Create input for the new parameter name
        new_param_string = self.__add_input("Enter New Parameter Name (comma-separated):", widget_type="line")
        
        # Store the widgets for later use
        self.input_widgets["new_param_string"] = new_param_string
        self.input_widgets["method_name_widget"] = method_name_widget
        
        # Add buttons (OK/Cancel)
        self.__add_buttons()
        
    def edit_param_type_popup(self, selected_class):
        """
        Creates a dialog for renaming a parameter type.
        """
        method_names = []
        method_keys = []
        
        for i, dictionary in enumerate(selected_class.method_list):
            method_key = dictionary["method_key"]
            param_list = dictionary["parameters"]
            # Convert parameter tuples to strings
            param_str_list = [f"{param_type} {param_name}" for param_type, param_name in param_list]
            params_str = ', '.join(param_str_list)
            # Build the display string
            display_str = f"{i + 1}: {method_key[0]} {method_key[1]}({params_str})"
            method_names.append(display_str)
            method_keys.append(method_key)
  
        # Create combo box for methods
        method_name_widget = self.__add_input("Select Method To Change Parameter:", widget_type="combo", options=method_names)
        
        print(method_name_widget.currentText())

        selected_index = method_name_widget.currentIndex()
        chosen_entry = selected_class.method_list[selected_index]

        # Get the parameters for the initially selected method
        param_options = [f"{param_type} {param_name}" for param_type, param_name in chosen_entry["parameters"]]

        param_name_widget = self.__add_input("Select Parameter To Change Type:", widget_type="combo", options=param_options)
        param_name_format = param_name_widget.currentText()
        param_name = param_name_format.split()[-1]  # Extract only the param_name (last part)
        
        new_param_type = self.__add_input("Enter New Parameter Type:", widget_type="line")
        
        self.input_widgets["method_name_widget"] = method_name_widget
        self.input_widgets["param_name"] = param_name
        self.input_widgets["new_param_type"] = new_param_type
        
        self.__update_param_name_only(param_name_widget)
        
        self.__add_buttons()
        
        # Connect the method_name combo box change to update the parameter list dynamically
        method_name_widget.currentIndexChanged.connect(lambda index: self.__update_param_list(selected_class, index, param_name_widget))

        # Connect the param_name_widget change to update 'param_name_only'
        param_name_widget.currentIndexChanged.connect(lambda: self.__update_param_name_only(param_name_widget))
        
    
    def add_relationship_popup(self, class_name_list, type_list):
        """
        Creates a dialog for adding a relationship.
        """
        name_list = [class_name for class_name in class_name_list.keys()]
        # Create combo box for class names
        destination_class = self.__add_input("Select Destination Class To Set Relationship:", widget_type="combo", options=name_list)
        
        # Create combo box for type
        type = self.__add_input("Select A Type For The Relationship:", widget_type="combo", options=type_list)
        
        # Store the widgets for later use
        self.input_widgets["destination_class"] = destination_class
        self.input_widgets["type"] = type
        
        # Add buttons (OK/Cancel)
        self.__add_buttons()
        
    def delete_relationship_popup(self, source_class_name, relationship_track_list):
        """
        Creates a dialog for deleting a relationship.
        """
        # Extract all dest_class names from the relationship track list
        dest_classes = []
        relationships = relationship_track_list.get(source_class_name, [])
        
        for relationship in relationships:
            dest_class = relationship["dest_class"]  # Access the dest_class key in the dictionary
            dest_classes.append(dest_class)
        
        # Create combo box for destination class names
        destination_class_list_of_current_source_class = self.__add_input(
            "Select Destination Class To Delete Relationship:", 
            widget_type="combo", 
            options=dest_classes
        )
        self.input_widgets["destination_class_list_of_current_source_class"] = destination_class_list_of_current_source_class
        
        # Add buttons (OK/Cancel)
        self.__add_buttons()
        
    def change_type_popup(self, source_class_name, relationship_track_list, type_list):
        """
        Creates a dialog for changing the type of a relationship.
        """
        # Extract all dest_class names from the relationship track list
        dest_classes = []
        relationships = relationship_track_list.get(source_class_name, [])
        
        for relationship in relationships:
            dest_class = relationship["dest_class"]  # Access the dest_class key in the dictionary
            dest_classes.append(dest_class)

        # Create combo box for destination class names
        destination_class_list_of_current_source_class = self.__add_input(
            "Select Destination Class To Change Relationship Type:", 
            widget_type="combo", 
            options=dest_classes
        )
        
        # Create combo box for relationship types
        relationship_type = self.__add_input(
            "Select A New Type For The Relationship:", 
            widget_type="combo", 
            options=type_list
        )
        
        # Store the input widgets
        self.input_widgets["destination_class_list_of_current_source_class"] = destination_class_list_of_current_source_class
        self.input_widgets["type"] = relationship_type
        
        # Add buttons (OK/Cancel)
        self.__add_buttons()
        
    def __add_input(self, label_text, widget_type, options=None):
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
    
    def __add_buttons(self):
        """
        Helper function to add OK and Cancel buttons.
        """
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)
    
    def __update_param_list(self, selected_class, selected_index, param_name_widget):
        """
        Updates the parameter combo box options based on the selected method.
        """
        # Retrieve the parameter list for the selected method
        if 0 <= selected_index < len(selected_class.method_list):
            selected_method_dict = selected_class.method_list[selected_index]
            param_list = selected_method_dict["parameters"]

            # Update the parameter combo box with the correct options
            param_options = [f"{param_type} {param_name}" for param_type, param_name in param_list]
            param_name_widget.clear()
            param_name_widget.addItems(param_options)

            # Handle the case where there are no parameters
            if not param_options:
                QtWidgets.QMessageBox.warning(self, "No Parameters", "The selected method has no parameters to delete.")
                self.input_widgets["param_name_only"] = ""
                return

            # After updating the param_name_widget, update 'param_name_only'
            self.__update_param_name_only(param_name_widget)
    
    def __update_param_name_only(self, param_name_widget):
        """
        Updates the 'param_name_only' based on the current selection in param_name_widget.
        """
        current_text = param_name_widget.currentText()
        if current_text:
            # Assuming the parameter name is the last word
            self.input_widgets["param_name_only"] = current_text.split()[-1]
            print(f"Param name: {self.input_widgets['param_name_only']}")
        else:
            self.input_widgets["param_name_only"] = ""
            print("No parameter selected.")