from PyQt5 import QtWidgets

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
        
        
    def rename_method_popup(self, selected_class):
        """
        Creates a dialog for renaming a method.
        """
        method_names = list(selected_class.method_name_list.keys())
        old_method_name = self.__add_input("Select Method To Rename:", widget_type="combo", options=method_names)
        new_method_name = self.__add_input("Enter New Method Name:", widget_type="line")
        
        # Store the widgets for later use
        self.input_widgets["old_method_name"] = old_method_name
        self.input_widgets["new_method_name"] = new_method_name
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
        self.input_widgets["new_param_name"] = new_param_name
        self.input_widgets["current_method"] = method_name
        
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
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def change_data_type_popup(self, selected_class, class_name_list, relationship_list, type_list):
    #     """
    #     Creates a dialog for changing data types of fields, methods, parameters, or relationships.
    #     """
    #     # Step 1: Add Radio Buttons for Options
    #     self.option_group = QtWidgets.QButtonGroup(self)
    #     self.option_layout = QtWidgets.QHBoxLayout()
        
    #     self.field_radio = QtWidgets.QRadioButton("Field")
    #     self.method_radio = QtWidgets.QRadioButton("Method")
    #     self.param_radio = QtWidgets.QRadioButton("Parameter")
    #     self.rel_radio = QtWidgets.QRadioButton("Relationship")
        
    #     self.option_group.addButton(self.field_radio)
    #     self.option_group.addButton(self.method_radio)
    #     self.option_group.addButton(self.param_radio)
    #     self.option_group.addButton(self.rel_radio)
        
    #     self.option_layout.addWidget(self.field_radio)
    #     self.option_layout.addWidget(self.method_radio)
    #     self.option_layout.addWidget(self.param_radio)
    #     self.option_layout.addWidget(self.rel_radio)
        
    #     self.layout.addLayout(self.option_layout)
        
    #     # Step 2: Create Stacked Widget to Hold Different Input Forms
    #     self.stacked_widget = QtWidgets.QStackedWidget()
    #     self.layout.addWidget(self.stacked_widget)
        
    #     # Step 3: Create Input Forms for Each Option
    #     self.field_widget = self.__create_field_widget(selected_class)
    #     self.method_widget = self.__create_method_widget(selected_class)
    #     self.param_widget = self.__create_param_widget(selected_class)
    #     self.rel_widget = self.__create_relationship_widget(selected_class, class_name_list, relationship_list, type_list)
        
    #     self.stacked_widget.addWidget(self.field_widget)
    #     self.stacked_widget.addWidget(self.method_widget)
    #     self.stacked_widget.addWidget(self.param_widget)
    #     self.stacked_widget.addWidget(self.rel_widget)
        
    #     # Step 4: Connect Radio Buttons to Update the Stacked Widget
    #     self.field_radio.toggled.connect(lambda: self.__update_stacked_widget())
    #     self.method_radio.toggled.connect(lambda: self.__update_stacked_widget())
    #     self.param_radio.toggled.connect(lambda: self.__update_stacked_widget())
    #     self.rel_radio.toggled.connect(lambda: self.__update_stacked_widget())
        
    #     # Step 5: Add OK and Cancel Buttons
    #     self.__add_buttons()
        
    #     # Step 6: Initialize by Selecting the First Option
    #     self.field_radio.setChecked(True)
    #     self.__update_stacked_widget()
    
    # def __update_stacked_widget(self):
    #     """
    #     Updates the stacked widget based on the selected radio button.
    #     """
    #     if self.field_radio.isChecked():
    #         self.stacked_widget.setCurrentWidget(self.field_widget)
    #     elif self.method_radio.isChecked():
    #         self.stacked_widget.setCurrentWidget(self.method_widget)
    #     elif self.param_radio.isChecked():
    #         self.stacked_widget.setCurrentWidget(self.param_widget)
    #     elif self.rel_radio.isChecked():
    #         self.stacked_widget.setCurrentWidget(self.rel_widget)
    
    # def __create_field_widget(self, selected_class):
    #     """
    #     Creates the input form for changing the data type of a field.
    #     """
    #     widget = QtWidgets.QWidget()
    #     layout = QtWidgets.QFormLayout()
    #     widget.setLayout(layout)
        
    #     # Field selection
    #     field_names = [field_key[1] for field_key in selected_class.field_key_list]
    #     field_combo = QtWidgets.QComboBox()
    #     field_combo.addItems(field_names)
        
    #     # New type input
    #     new_type_line = QtWidgets.QLineEdit()
        
    #     layout.addRow("Select Field:", field_combo)
    #     layout.addRow("New Type:", new_type_line)
        
    #     # Store widgets
    #     self.input_widgets["field_name"] = field_combo
    #     self.input_widgets["field_new_type"] = new_type_line
    #     self.input_widgets["is_field"] = True  # Indicator for later use
        
    #     return widget
    
    # def __create_method_widget(self, selected_class):
    #     """
    #     Creates the input form for changing the return type of a method.
    #     """
    #     widget = QtWidgets.QWidget()
    #     layout = QtWidgets.QFormLayout()
    #     widget.setLayout(layout)
        
    #     # Method selection
    #     method_names = list(selected_class.method_name_list.keys())
    #     method_combo = QtWidgets.QComboBox()
    #     method_combo.addItems(method_names)
        
    #     # New type input
    #     new_type_line = QtWidgets.QLineEdit()
        
    #     layout.addRow("Select Method:", method_combo)
    #     layout.addRow("New Return Type:", new_type_line)
        
    #     # Store widgets
    #     self.input_widgets["method_name"] = method_combo
    #     self.input_widgets["method_new_type"] = new_type_line
    #     self.input_widgets["is_method"] = True  # Indicator for later use
        
    #     return widget
    
    # def __create_param_widget(self, selected_class):
    #     """
    #     Creates the input form for changing the data type of a parameter.
    #     """
    #     widget = QtWidgets.QWidget()
    #     layout = QtWidgets.QFormLayout()
    #     widget.setLayout(layout)
        
    #     # Method selection
    #     method_names = list(selected_class.method_name_list.keys())
    #     method_combo = QtWidgets.QComboBox()
    #     method_combo.addItems(method_names)
        
    #     # Parameter selection (initially based on the first method)
    #     first_method_params = selected_class.method_name_list.get(method_names[0], [])
    #     param_combo = QtWidgets.QComboBox()
    #     param_combo.addItems(first_method_params)
        
    #     # Update param_combo when method_combo changes
    #     method_combo.currentIndexChanged.connect(lambda: self.__update_param_combo(selected_class, method_combo, param_combo))
        
    #     # New type input
    #     new_type_line = QtWidgets.QLineEdit()
        
    #     layout.addRow("Select Method:", method_combo)
    #     layout.addRow("Select Parameter:", param_combo)
    #     layout.addRow("New Type:", new_type_line)
        
    #     # Store widgets
    #     self.input_widgets["param_method_name"] = method_combo
    #     self.input_widgets["param_name"] = param_combo
    #     self.input_widgets["param_new_type"] = new_type_line
    #     self.input_widgets["is_param"] = True  # Indicator for later use
        
    #     return widget
    
    # def __create_relationship_widget(self, selected_class, class_name_list, relationship_list, type_list):
    #     """
    #     Creates the input form for changing the type of a relationship.
    #     """
    #     widget = QtWidgets.QWidget()
    #     layout = QtWidgets.QFormLayout()
    #     widget.setLayout(layout)
        
    #     # Source class (current class)
    #     source_class_line = QtWidgets.QLineEdit()
    #     source_class_line.setText(selected_class.class_name_text.toPlainText())
    #     source_class_line.setReadOnly(True)
        
    #     # Destination class selection
    #     # Get relationships from the selected class
    #     source_class_name = selected_class.class_name_text.toPlainText()
    #     dest_classes = [rel.dest_class_name for rel in relationship_list if rel.source_class_name == source_class_name]
    #     dest_combo = QtWidgets.QComboBox()
    #     dest_combo.addItems(dest_classes)
        
    #     # New type selection
    #     type_combo = QtWidgets.QComboBox()
    #     type_combo.addItems(type_list)
        
    #     layout.addRow("Source Class:", source_class_line)
    #     layout.addRow("Destination Class:", dest_combo)
    #     layout.addRow("New Relationship Type:", type_combo)
        
    #     # Store widgets
    #     self.input_widgets["rel_source_class"] = source_class_line
    #     self.input_widgets["rel_dest_class"] = dest_combo
    #     self.input_widgets["rel_new_type"] = type_combo
    #     self.input_widgets["is_rel"] = True  # Indicator for later use
        
    #     return widget
    
    # def __update_param_combo(self, selected_class, method_combo, param_combo):
    #     """
    #     Updates the parameter combo box based on the selected method.
    #     """
    #     selected_method = method_combo.currentText()
    #     params = selected_class.method_name_list.get(selected_method, [])
    #     param_combo.clear()
    #     param_combo.addItems(params)