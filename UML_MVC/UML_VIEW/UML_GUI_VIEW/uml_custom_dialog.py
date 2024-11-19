from PyQt5 import QtWidgets
import re

class CustomInputDialog(QtWidgets.QDialog):
    """
    A custom input dialog class for various input operations in a GUI.

    This class provides methods to create different input dialogs for actions such as
    adding fields, renaming fields, editing field types, adding methods, deleting methods,
    renaming methods, editing method return types, and handling parameters and relationships.

    Attributes:
        input_widgets (dict): A dictionary to store input widgets for later retrieval.
        layout (QVBoxLayout): The layout manager for the dialog.
    """

    def __init__(self, title="Input Dialog"):
        """
        Initialize the CustomInputDialog.

        Parameters:
            title (str): The title of the dialog window.
        """
        super().__init__()
        self.setWindowTitle(title)
        self.input_widgets = {}  # Store all input widgets for retrieval
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        
    def add_field_popup(self):
        """
        Creates a dialog for adding a new field to a class.

        The dialog collects the field type and field name from the user.
        """
        # Create input for the field type
        field_type = self.__add_input("Enter field type:", widget_type="line")
        # Create input for the field name
        field_name = self.__add_input("Enter field name:", widget_type="line")
        
        # Store the widgets for later use
        self.input_widgets["field_type"] = field_type
        self.input_widgets["field_name"] = field_name
        # Add OK and Cancel buttons
        self.__add_buttons()

    def rename_field_popup(self, selected_class):
        """
        Creates a dialog for renaming an existing field in a class.

        Parameters:
            selected_class: The class object containing the fields.

        The dialog allows the user to select an existing field and provide a new name.
        """
        # Get a list of existing field names
        field_name_list = [field_key[1] for field_key in selected_class.field_key_list]
        # Create a combo box for selecting the field to rename
        old_field_name = self.__add_input("Select Field To Rename:", widget_type="combo", options=field_name_list)
        # Create input for the new field name
        new_field_name = self.__add_input("Enter New Field Name:", widget_type="line")
        
        # Store the widgets for later use
        self.input_widgets["old_field_name"] = old_field_name
        self.input_widgets["new_field_name"] = new_field_name
        # Add OK and Cancel buttons
        self.__add_buttons()
        
    def edit_field_type_popup(self, selected_class):
        """
        Creates a dialog for editing the type of an existing field.

        Parameters:
            selected_class: The class object containing the fields.

        The dialog allows the user to select a field and enter a new type.
        """
        # Get a list of existing field names
        field_name_list = [field_key[1] for field_key in selected_class.field_key_list]
        # Create a combo box for selecting the field to edit
        field_name = self.__add_input("Select Field To Edit Type:", widget_type="combo", options=field_name_list)
        # Create input for the new field type
        new_field_type = self.__add_input("Enter New Type Name:", widget_type="line")
        
        # Store the widgets for later use
        self.input_widgets["field_name"] = field_name
        self.input_widgets["new_field_type"] = new_field_type
        # Add OK and Cancel buttons
        self.__add_buttons()
        
    def add_method_popup(self):
        """
        Creates a dialog for adding a new method to a class.

        The dialog collects the method type and method name from the user.
        """
        # Create input for the method type
        method_type = self.__add_input("Enter method type:", widget_type="line")
        # Create input for the method name
        method_name = self.__add_input("Enter method name:", widget_type="line")
        
        # Store the widgets for later use
        self.input_widgets["method_type"] = method_type
        self.input_widgets["method_name"] = method_name
        # Add OK and Cancel buttons
        self.__add_buttons()
        
    def delete_method_popup(self, selected_class):
        """
        Creates a dialog for deleting an existing method from a class.

        Parameters:
            selected_class: The class object containing the methods.

        The dialog allows the user to select a method to delete.
        """
        method_display_list = []
        method_keys_list = []
        
        # Build display strings for methods
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
        method_name_widget = self.__add_input("Select Method To Delete:", widget_type="combo", options=method_display_list)
        # Extract the method type and name from the selected text
        match = re.search(r': (\w+) (\w+)\(', method_name_widget.currentText())
        type_name_tuple = (match.group(1), match.group(2)) if match else (None, None)
        
        # Store the widgets and data for later use
        self.input_widgets["method_type"] = type_name_tuple[0]
        self.input_widgets["method_name"] = type_name_tuple[1]
        self.input_widgets["raw_method_name"] = method_name_widget
        # Add OK and Cancel buttons
        self.__add_buttons()
        
    def rename_method_popup(self, selected_class):
        """
        Creates a dialog for renaming an existing method in a class.

        Parameters:
            selected_class: The class object containing the methods.

        The dialog allows the user to select a method and provide a new name.
        """
        method_display_list = []
        method_keys_list = []
        
        # Build display strings for methods
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
        
        # Store the widgets and data for later use
        self.input_widgets["raw_method_name"] = old_method_name
        self.input_widgets["new_method_name"] = new_method_name
        self.input_widgets["method_keys_list"] = method_keys_list
        # Add OK and Cancel buttons
        self.__add_buttons()
        
    def edit_method_return_type_popup(self, selected_class):
        """
        Creates a dialog for editing the return type of an existing method.

        Parameters:
            selected_class: The class object containing the methods.

        The dialog allows the user to select a method and enter a new return type.
        """
        method_display_list = []
        method_keys_list = []
        
        # Build display strings for methods
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
        
        # Store the widgets and data for later use
        self.input_widgets["method_name"] = method_name
        self.input_widgets["new_method_return_type"] = new_method_return_type
        self.input_widgets["method_keys_list"] = method_keys_list
        # Add OK and Cancel buttons
        self.__add_buttons()
        
    def add_param_popup(self, selected_class):
        """
        Creates a dialog for adding a parameter to a method.

        Parameters:
            selected_class: The class object containing the methods.

        The dialog allows the user to select a method and provide parameter type and name.
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

        # Create combo box for selecting the method
        method_name_widget = self.__add_input("Select Method To Add Parameter:", widget_type="combo", options=method_names)
        # Extract the method type and name from the selected text
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

        Parameters:
            selected_class: The class object containing the methods.

        The dialog allows the user to select a method and then select a parameter to delete.
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

        # Create combo box for selecting the method
        method_name_widget = self.__add_input("Select Method To Delete Parameter:", widget_type="combo", options=method_names)

        selected_index = method_name_widget.currentIndex()
        chosen_entry = selected_class.method_list[selected_index]

        # Get the parameters for the initially selected method
        param_options = [f"{param_type} {param_name}" for param_type, param_name in chosen_entry["parameters"]]

        # Create combo box for selecting the parameter to delete
        param_name_widget = self.__add_input("Select Parameter To Delete:", widget_type="combo", options=param_options)
        
        # Store widgets and data for later use
        self.input_widgets["method_name_widget"] = method_name_widget
        self.input_widgets["param_name_widget"] = param_name_widget

        # Initialize 'param_name_only' based on the initial selection
        self.__update_param_name_only(param_name_widget)

        # Add OK and Cancel buttons
        self.__add_buttons()

        # Connect the method_name combo box change to update the parameter list dynamically
        method_name_widget.currentIndexChanged.connect(lambda index: self.__update_param_list(selected_class, index, param_name_widget))

        # Connect the param_name_widget change to update 'param_name_only'
        param_name_widget.currentIndexChanged.connect(lambda: self.__update_param_name_only(param_name_widget))
        
    def rename_param_popup(self, selected_class):
        """
        Creates a dialog for renaming a parameter in a selected method.

        Parameters:
            selected_class: The class object containing the methods.

        The dialog allows the user to select a method, select a parameter, and provide a new parameter name.
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

        # Create combo box for selecting the method
        method_name_widget = self.__add_input("Select Method To Change Parameter:", widget_type="combo", options=method_names)
        self.input_widgets["method_name_widget"] = method_name_widget

        selected_index = method_name_widget.currentIndex()
        chosen_entry = selected_class.method_list[selected_index]

        # Get the parameters for the initially selected method
        param_options = [f"{param_type} {param_name}" for param_type, param_name in chosen_entry["parameters"]]

        # Create combo box for selecting the parameter to rename
        old_param_name_widget = self.__add_input("Select Parameter To Change:", widget_type="combo", options=param_options)
        # Create input for the new parameter name
        new_param_name_widget = self.__add_input("Enter New Parameter Name:", widget_type="line")
        
        # Store widgets and data for later use
        self.input_widgets["method_name_widget"] = method_name_widget
        self.input_widgets["old_param_name_widget"] = old_param_name_widget
        self.input_widgets["new_param_name_widget"] = new_param_name_widget

        # Initialize 'param_name_only' based on the initial selection
        self.__update_param_name_only(old_param_name_widget)

        # Add OK and Cancel buttons
        self.__add_buttons()

        # Connect the method_name combo box change to update the parameter list dynamically
        method_name_widget.currentIndexChanged.connect(lambda index: self.__update_param_list(selected_class, index, old_param_name_widget))

        # Connect the param_name_widget change to update 'param_name_only'
        old_param_name_widget.currentIndexChanged.connect(lambda: self.__update_param_name_only(old_param_name_widget))
        
    def replace_param_list_popup(self, selected_class):
        """
        Creates a dialog for replacing the parameter list of a selected method.

        Parameters:
            selected_class: The class object containing the methods.

        The dialog allows the user to select a method and provide a new parameter list.
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

        # Create combo box for selecting the method
        method_name_widget = self.__add_input("Select Method To Replace Parameter List:", widget_type="combo", options=method_names)
        self.input_widgets["method_name_widget"] = method_name_widget
        
        # Create input for the new parameter list as a string
        new_param_string = self.__add_input("Enter New Parameter List (comma-separated):", widget_type="line")
        
        # Store the widgets for later use
        self.input_widgets["new_param_string"] = new_param_string
        self.input_widgets["method_name_widget"] = method_name_widget
        
        # Add OK and Cancel buttons
        self.__add_buttons()
        
    def edit_param_type_popup(self, selected_class):
        """
        Creates a dialog for editing the type of a parameter in a method.

        Parameters:
            selected_class: The class object containing the methods.

        The dialog allows the user to select a method, select a parameter, and provide a new type for the parameter.
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
      
        # Create combo box for selecting the method
        method_name_widget = self.__add_input("Select Method To Change Parameter Type:", widget_type="combo", options=method_names)
        
        selected_index = method_name_widget.currentIndex()
        chosen_entry = selected_class.method_list[selected_index]

        # Get the parameters for the initially selected method
        param_options = [f"{param_type} {param_name}" for param_type, param_name in chosen_entry["parameters"]]

        # Create combo box for selecting the parameter
        param_name_widget = self.__add_input("Select Parameter To Change Type:", widget_type="combo", options=param_options)
        # Extract only the parameter name
        param_name_format = param_name_widget.currentText()
        param_name = param_name_format.split()[-1]  # Extract the param_name (last part)
        
        # Create input for the new parameter type
        new_param_type = self.__add_input("Enter New Parameter Type:", widget_type="line")
        
        # Store widgets and data for later use
        self.input_widgets["method_name_widget"] = method_name_widget
        self.input_widgets["param_name"] = param_name
        self.input_widgets["new_param_type"] = new_param_type
        
        # Initialize 'param_name_only' based on the initial selection
        self.__update_param_name_only(param_name_widget)
        
        # Add OK and Cancel buttons
        self.__add_buttons()
        
        # Connect the method_name combo box change to update the parameter list dynamically
        method_name_widget.currentIndexChanged.connect(lambda index: self.__update_param_list(selected_class, index, param_name_widget))

        # Connect the param_name_widget change to update 'param_name_only'
        param_name_widget.currentIndexChanged.connect(lambda: self.__update_param_name_only(param_name_widget))
            
    def add_relationship_popup(self, class_name_list, type_list):
        """
        Creates a dialog for adding a relationship between classes.

        Parameters:
            class_name_list (dict): A dictionary of class names and their corresponding class objects.
            type_list (list): A list of relationship types.

        The dialog allows the user to select a destination class and a relationship type.
        """
        name_list = [class_name for class_name in class_name_list.keys()]
        # Create combo box for selecting the destination class
        destination_class = self.__add_input("Select Destination Class To Set Relationship:", widget_type="combo", options=name_list)
        
        # Create combo box for selecting the relationship type
        relationship_type = self.__add_input("Select A Type For The Relationship:", widget_type="combo", options=type_list)
        
        # Store the widgets for later use
        self.input_widgets["destination_class"] = destination_class
        self.input_widgets["type"] = relationship_type
        
        # Add OK and Cancel buttons
        self.__add_buttons()
        
    def delete_relationship_popup(self, source_class_name, relationship_track_list):
        """
        Creates a dialog for deleting a relationship from a source class.

        Parameters:
            source_class_name (str): The name of the source class.
            relationship_track_list (dict): A dictionary tracking relationships for each class.

        The dialog allows the user to select a destination class to delete the relationship.
        """
        # Extract all destination class names from the relationship track list
        dest_classes = []
        relationships = relationship_track_list.get(source_class_name, [])
        
        for relationship in relationships:
            dest_class = relationship["dest_class"]  # Access the dest_class key in the dictionary
            dest_classes.append(dest_class)
        
        # Create combo box for selecting the destination class
        destination_class_widget = self.__add_input(
            "Select Destination Class To Delete Relationship:", 
            widget_type="combo", 
            options=dest_classes
        )
        # Store the widget for later use
        self.input_widgets["destination_class_list_of_current_source_class"] = destination_class_widget
        
        # Add OK and Cancel buttons
        self.__add_buttons()
        
    def change_type_popup(self, source_class_name, relationship_track_list, type_list):
        """
        Creates a dialog for changing the type of a relationship from a source class.

        Parameters:
            source_class_name (str): The name of the source class.
            relationship_track_list (dict): A dictionary tracking relationships for each class.
            type_list (list): A list of relationship types.

        The dialog allows the user to select a destination class and a new relationship type.
        """
        # Extract all destination class names from the relationship track list
        dest_classes = []
        relationships = relationship_track_list.get(source_class_name, [])
        
        for relationship in relationships:
            dest_class = relationship["dest_class"]  # Access the dest_class key in the dictionary
            dest_classes.append(dest_class)

        # Create combo box for selecting the destination class
        destination_class_widget = self.__add_input(
            "Select Destination Class To Change Relationship Type:", 
            widget_type="combo", 
            options=dest_classes
        )
        
        # Create combo box for selecting the new relationship type
        relationship_type = self.__add_input(
            "Select A New Type For The Relationship:", 
            widget_type="combo", 
            options=type_list
        )
        
        # Store the input widgets
        self.input_widgets["destination_class_list_of_current_source_class"] = destination_class_widget
        self.input_widgets["type"] = relationship_type
        
        # Add OK and Cancel buttons
        self.__add_buttons()
        
    def __add_input(self, label_text, widget_type, options=None):
        """
        Helper method to add various types of input fields to the dialog.

        Parameters:
            label_text (str): The label text for the input.
            widget_type (str): Type of the widget ('combo' for combo box, 'line' for line edit).
            options (list, optional): List of options for combo boxes.

        Returns:
            QWidget: The created input widget.
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
        Helper method to add OK and Cancel buttons to the dialog.

        Connects the buttons to the accept and reject methods of the dialog.
        """
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)
        
    def __update_param_list(self, selected_class, selected_index, param_name_widget):
        """
        Updates the parameter combo box options based on the selected method.

        Parameters:
            selected_class: The class object containing the methods.
            selected_index (int): The index of the selected method.
            param_name_widget (QComboBox): The combo box widget for parameter selection.
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
                QtWidgets.QMessageBox.warning(self, "No Parameters", "The selected method has no parameters.")
                self.input_widgets["param_name_only"] = ""
                return

            # After updating the param_name_widget, update 'param_name_only'
            self.__update_param_name_only(param_name_widget)
        
    def __update_param_name_only(self, param_name_widget):
        """
        Updates the 'param_name_only' in input_widgets based on the current selection in param_name_widget.

        Parameters:
            param_name_widget (QComboBox): The combo box widget for parameter selection.
        """
        current_text = param_name_widget.currentText()
        if current_text:
            # Assuming the parameter name is the last word
            self.input_widgets["param_name_only"] = current_text.split()[-1]
            print(f"Param name: {self.input_widgets['param_name_only']}")
        else:
            self.input_widgets["param_name_only"] = ""
            print("No parameter selected.")
