from PyQt5 import QtWidgets

class CustomInputDialog(QtWidgets.QDialog):
    def __init__(self, title="Input Dialog"):
        super().__init__()
        self.setWindowTitle(title)
        self.input_widgets = {}  # Store all input widgets for retrieval
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

    def rename_field_popup(self, selected_class):
        """
        Creates a dialog for renaming a field.
        """
        old_field_name = self.__add_input("Select Field To Rename:", widget_type="combo", options=selected_class.field_name_list)
        new_field_name = self.__add_input("Enter New Field Name:", widget_type="line")
        
        # Store the widgets for later use
        self.input_widgets['old_field_name'] = old_field_name
        self.input_widgets['new_field_name'] = new_field_name
        self.__add_buttons()
        
    def rename_method_popup(self, selected_class):
        """
        Creates a dialog for renaming a method.
        """
        method_names = list(selected_class.method_name_list.keys())
        old_method_name = self.__add_input("Select Method To Rename:", widget_type="combo", options=method_names)
        new_method_name = self.__add_input("Enter New Method Name:", widget_type="line")
        
        # Store the widgets for later use
        self.input_widgets['old_method_name'] = old_method_name
        self.input_widgets['new_method_name'] = new_method_name
        self.__add_buttons()
        
    def add_param_popup(self, selected_class):
        """
        Creates a dialog for adding a parameter.
        """
        method_names_list = list(selected_class.method_name_list.keys())
        
        # Create combo box for methods
        method_name = self.__add_input("Select Method To Add Parameter:", widget_type="combo", options=method_names_list)
        
        # Create input for the new parameter name
        new_param_name = self.__add_input("Enter New Parameter Name:", widget_type="line")
        
        # Store the widgets for later use
        self.input_widgets['new_param_name'] = new_param_name
        self.input_widgets['current_method'] = method_name
        
        # Add buttons (OK/Cancel)
        self.__add_buttons()
        
    def delete_param_popup(self, selected_class):
        """
        Creates a dialog for adding a parameter.
        """
        method_names_list = list(selected_class.method_name_list.keys())
        
        # Create combo box for methods
        method_name = self.__add_input("Select Method To Delete Parameter:", widget_type="combo", options=method_names_list)
        
        # Create combo box for parameters (initially based on the first method in the list)
        param_name = self.__add_input("Select Parameter To Delete:", widget_type="combo", options=selected_class.method_name_list[method_name.currentText()])
        
        # Store the widgets for later use
        self.input_widgets["param_name"] = param_name
        self.input_widgets["current_method"] = method_name
        
        # Add buttons (OK/Cancel)
        self.__add_buttons()
        
        # Connect the method_name combo box change to update the parameter list
        method_name.currentIndexChanged.connect(lambda: self.__update_param_list(selected_class, method_name, param_name))
        
    def rename_param_popup(self, selected_class):
        """
        Creates a dialog for renaming a parameter.
        """
        method_names_list = list(selected_class.method_name_list.keys())
        
        # Create combo box for methods
        method_name = self.__add_input("Select Method To Rename Parameter:", widget_type="combo", options=method_names_list)
        
        # Create combo box for parameters (initially based on the first method in the list)
        old_param_name = self.__add_input("Select Parameter To Delete:", widget_type="combo", options=selected_class.method_name_list[method_name.currentText()])
        
        # Create input for the new parameter name
        new_param_name = self.__add_input("Enter New Parameter Name:", widget_type="line")
        
        self.input_widgets["current_method"] = method_name
        self.input_widgets["old_param_name"] = old_param_name
        self.input_widgets["new_param_name"] = new_param_name
        
        # Add buttons (OK/Cancel)
        self.__add_buttons()
        
    def replace_param_list_popup(self, selected_class):
        """
        Creates a dialog for replacing parameter list.
        """
        method_names_list = list(selected_class.method_name_list.keys())
        
        # Create combo box for methods
        method_name = self.__add_input("Select Method:", widget_type="combo", options=method_names_list)
        
        # Create input for the new parameter name
        new_param_string = self.__add_input("Enter New Parameter Name (comma-separated):", widget_type="line")

        # Store the widgets for later use
        self.input_widgets["new_param_string"] = new_param_string
        self.input_widgets["current_method"] = method_name
        
        # Add buttons (OK/Cancel)
        self.__add_buttons()
        
    
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
        # Extract all dest_class names from the list of tuples
        dest_classes = [dest_class for dest_class, arrow_line in relationship_track_list[source_class_name]]
        
        # Create combo box for source class names
        destination_class_list_of_current_source_class = self.__add_input("Select Destination Class To Delete Relationship:", 
                                                                          widget_type="combo", options=dest_classes)
        self.input_widgets["destination_class_list_of_current_source_class"] = destination_class_list_of_current_source_class
        # Add buttons (OK/Cancel)
        self.__add_buttons()
        
    def change_type_popup(self, source_class_name, relationship_track_list, type_list):
        """
        Creates a dialog for deleting a relationship.
        """
        # Extract all dest_class names from the list of tuples
        dest_classes = [dest_class for dest_class, arrow_line in relationship_track_list[source_class_name]]
        # Create combo box for source class names
        destination_class_list_of_current_source_class = self.__add_input("Select Destination Class To Change Relationship Type:", 
                                                                          widget_type="combo", 
                                                                          options=dest_classes)
         # Create combo box for type
        type = self.__add_input("Select A New Type For The Relationship:", widget_type="combo", options=type_list)
        
        self.input_widgets["destination_class_list_of_current_source_class"] = destination_class_list_of_current_source_class
        self.input_widgets["type"] = type
        
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
        
    def __update_param_list(self, selected_class, method_name_combo, param_combo):
        """
        Updates the parameter combo box options based on the selected method.
        """
        # Get the currently selected method
        selected_method = method_name_combo.currentText()
        
        # Get the parameters for the selected method
        param_list = selected_class.method_name_list.get(selected_method, [])
        
        # Clear and update the parameter combo box
        param_combo.clear()
        param_combo.addItems(param_list)
    
    def __add_buttons(self):
        """
        Helper function to add OK and Cancel buttons.
        """
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)