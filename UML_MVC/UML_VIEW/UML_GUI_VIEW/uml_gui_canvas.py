###################################################################################################

import os
from PyQt5 import QtWidgets, QtGui, QtCore
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_class_box import UMLClassBox
# from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_arrow_line import Arrow
from UML_ENUM_CLASS.uml_enum import RelationshipType
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_custom_dialog import CustomInputDialog as Dialog
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_arrow_line import UMLArrow as ArrowLine
from UML_MVC import uml_command_pattern as Command

###################################################################################################

class UMLGraphicsView(QtWidgets.QGraphicsView):
    """
    A custom graphics view that displays a grid pattern and handles user interactions.
    Inherits from QGraphicsView.
    """

    #################################################################
    ### CONSTRUCTOR ###

    def __init__(self, interface, parent=None):
        """
        Initializes a new UMLGraphicsView instance.

        Parameters:
        - parent (QWidget): The parent widget.
        - grid_size (int): The spacing between grid lines in pixels.
        - color (QColor): The color of the grid lines.
        """
        super().__init__(QtWidgets.QGraphicsScene(parent), parent)

        # Interface to communicate with UMLCoreManager
        self.interface = interface  
        self.model = self.interface.Controller._get_model_obj()
        
        self.input_handler = self.interface.Controller._get_input_handler()
        
        # Class name list
        self.class_name_list = {}
        
        # Relationship pair list
        self.relationship_track_list: dict[str, list[tuple]] = {}
        
        # Initialize canvas properties
        self.is_dark_mode = False  # Flag for light/dark mode

        # Set initial view properties
        self.setRenderHint(QtGui.QPainter.Antialiasing, True)
        self.setSceneRect(-5000, -5000, 10000, 10000)  # Large scene size
        self.setScene(self.scene())

        # Panning state variables
        self.is_panning = False  # Flag to indicate if panning is active

        # Track selected class or arrow
        self.selected_class = False
        
        self.move_start_pos = None

    #################################################################
    ## GRID VIEW RELATED ##

    def scale(self, sx, sy):
        """
        Override scale method to resize class boxes when zooming.

        Parameters:
        - sx (float): Scaling factor in x-direction.
        - sy (float): Scaling factor in y-direction.
        """
        super().scale(sx, sy)

    def drawBackground(self, painter, rect):
        """
        Draw the background grid pattern.

        Parameters:
        - painter (QPainter): The painter object.
        - rect (QRectF): The area to be painted.
        """
        # Fill background based on mode
        if self.is_dark_mode:
            painter.fillRect(rect, QtGui.QColor(30, 30, 30))
        else:
            painter.fillRect(rect, QtGui.QColor(255, 255, 255))
    
    #################################################################
    ## CLASS OPERATION ##
    def add_class(self, loaded_class_name=None, x=None, y=None, is_loading=False):
        """
        Add a sample UML class box to the scene.
        """
        if is_loading:
            is_class_added = self.interface.add_class(loaded_class_name)
            if is_class_added:
                class_box = UMLClassBox(self.interface, class_name=loaded_class_name, x=x, y=y)
                class_box.set_box_position()
                self.class_name_list[loaded_class_name] = class_box
                self.scene().addItem(class_box)
        else:
            # Display a dialog asking the user for the new class name
            input_class_name, ok = QtWidgets.QInputDialog.getText(None, "Add Class", "Enter class name:")
            if ok and input_class_name:
                is_class_name_valid = self.interface.is_valid_input(class_name=input_class_name)
                if not is_class_name_valid:
                    QtWidgets.QMessageBox.warning(None, "Warning", f"Class name {input_class_name} is invalid! Only allow a-zA-Z, number, and underscore!")
                    return
                class_box = UMLClassBox(self.interface, class_name=input_class_name)
                add_class_command = Command.AddClassCommand(self.model, class_name=input_class_name, view=self, class_box=class_box, is_gui=True)
                is_class_added = self.input_handler.execute_command(add_class_command)

                if not is_class_added:
                    QtWidgets.QMessageBox.warning(None, "Warning", f"Class '{input_class_name}' has already existed!")
        
            
    def delete_class(self):
        """
        Delete the selected class or arrow from the scene.
        """
        if self.selected_class:
            # Remove the class box
            input_class_name = self.selected_class.class_name_text.toPlainText()
            delete_class_command = Command.DeleteClassCommand(self.model, class_name=input_class_name, view=self, class_box=self.selected_class, is_gui=True)
            is_class_deleted = self.input_handler.execute_command(delete_class_command)
            if not is_class_deleted:
                QtWidgets.QMessageBox.warning(None, "Warning", f"Class '{input_class_name}' does not exist!")
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")

    def rename_class(self):
        """
        Rename the class displayed in the UML box.

        This method prompts the user to input a new name for the class. 
        If the user confirms and enters a valid name, the class name is updated 
        and the box is refreshed to reflect the new name.
        """
        if self.selected_class:
            # Display a dialog asking the user for the new class name
            old_class_name = self.selected_class.class_name_text.toPlainText()
            new_class_name, ok = QtWidgets.QInputDialog.getText(None, "Rename Class", f"Enter new name for class '{old_class_name}'")
            if ok and new_class_name:
                is_class_name_valid = self.interface.is_valid_input(new_name=new_class_name)
                if not is_class_name_valid:
                    QtWidgets.QMessageBox.warning(None, "Warning", f"Class name {new_class_name} is invalid! Only allow a-zA-Z, number, and underscore!")
                    return
                rename_class_command = Command.RenameClassCommand(self.model, class_name=old_class_name, new_name=new_class_name, view=self, class_box=self.selected_class, is_gui=True)
                is_class_renamed = self.input_handler.execute_command(rename_class_command)
                if is_class_renamed:
                    self.class_name_list[new_class_name] = self.class_name_list.pop(old_class_name)
                    self.selected_class.update_box()
                else:
                    QtWidgets.QMessageBox.warning(None, "Warning", f"New class name'{new_class_name}' has already existed!")
            
    def add_field(self, loaded_class_name=None, loaded_field_type=None, loaded_field_name=None, is_loading=False):
        """
        Add a field to a UML class box, either during loading or interactively.

        This function either loads a field into the UML class during the loading process or allows the user
        to add a new field through a dialog box. It updates the UML class box and its internal lists.

        Parameters:
            loaded_class_name (str): The name of the class to which the field is added (used during loading).
            loaded_field_name (str): The name of the field being added (used during loading).
            is_loading (bool): Whether the function is being called during the loading process.

        Steps:
        1. If loading, find the UML class by its name and add the loaded field.
        2. If not loading, prompt the user for a field name to add to the selected UML class.
        3. Update the UML class box to reflect the new field.
        """
        if is_loading:
            # Find the UML class box by the loaded class name in the scene
            for item in self.scene().items():
                if isinstance(item, UMLClassBox) and item.class_name_text.toPlainText() == loaded_class_name:
                    selected_class_box = item  # Found the class box
                    # Add the field to the found class box
                    is_field_added = self.interface.add_field(loaded_class_name, loaded_field_type, loaded_field_name)
                    if is_field_added:
                        # Create a text item for the field and add it to the list of the found class box
                        field_text = selected_class_box.create_text_item(loaded_field_type + " " + loaded_field_name, is_field=True, selectable=False, 
                                                                         color=selected_class_box.text_color)
                        field_key = (loaded_field_type, loaded_field_name)
                        selected_class_box.field_list[field_key] = field_text  # Add the field to the internal list
                        selected_class_box.field_key_list.append(field_key)  # Track the field name in the name list
                        selected_class_box.update_box()  # Update the box to reflect the changes
        else:
            if self.selected_class:
                add_field_dialog = Dialog("Add Field")
                add_field_dialog.add_field_popup()
                
                # Execute the dialog and wait for user confirmation (OK or Cancel)
                if add_field_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    field_type = add_field_dialog.input_widgets["field_type"].text()
                    field_name = add_field_dialog.input_widgets["field_name"].text()
                    
                    if not field_type.strip() and not field_name.strip():
                        return
                    elif not field_name.strip():
                        QtWidgets.QMessageBox.warning(None, "Warning", "Field name is empty!")
                        return
                    elif not field_type.strip():
                        QtWidgets.QMessageBox.warning(None, "Warning", "Field type is empty!")
                        return
                    
                    is_field_type_valid = self.interface.is_valid_input(field_type=field_type)
                    if not is_field_type_valid:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Field type {field_type} is invalid! Only allow a-zA-Z, number, and underscore!")
                        return
                    is_field_name_valid = self.interface.is_valid_input(field_name=field_name)
                    if not is_field_name_valid:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Field name {field_name} is invalid! Only allow a-zA-Z, number, and underscore!")
                        return
                    
                    add_field_command = Command.AddFieldCommand(self.model, class_name=selected_class_name, type=field_type, 
                                                                field_name=field_name, view=self, class_box=self.selected_class, is_gui=True)
                    is_field_added = self.input_handler.execute_command(add_field_command)
                    
                    if not is_field_added:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Field name '{field_name}' has already existed!")
                    

    def delete_field(self):
        """
        Remove an existing field from the UML class.

        This function allows the user to select a field from the selected class and remove it.
        It updates the internal lists and the graphical display.

        Steps:
        1. Prompt the user to select a field from the class.
        2. Remove the selected field and update the UML class box.
        3. If no class or field is selected, display a warning.
        """
        if self.selected_class:
            if self.selected_class.field_key_list:
                # Display a dialog asking the user to select a field to remove
                field_name_list = [field_key[1] for field_key in self.selected_class.field_key_list]
                field_name, ok = QtWidgets.QInputDialog.getItem(None, "Remove Field", "Select field to remove:", field_name_list, 0, False)
                # If the user confirms, remove the selected field from the class
                if ok and field_name:
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    
                    delete_field_command = Command.DeleteFieldCommand(self.model, class_name=selected_class_name, field_name=field_name, 
                                                                      view=self, class_box=self.selected_class, is_gui=True)
                    self.input_handler.execute_command(delete_field_command)
    
    def rename_field(self):
        if self.selected_class:
            if self.selected_class.field_key_list: 
                # Initialize the dialog
                rename_field_dialog = Dialog("Rename Field")
                rename_field_dialog.rename_field_popup(self.selected_class)
                
                # Execute the dialog and wait for user confirmation (OK or Cancel)
                if rename_field_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    
                    # Get the old and new field names after the dialog is accepted
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    old_field_name = rename_field_dialog.input_widgets['old_field_name'].currentText()  # Use `currentText()` for QComboBox
                    new_field_name = rename_field_dialog.input_widgets['new_field_name'].text()  # Use `text()` for QLineEdit
                    
                    if not new_field_name.strip():
                        return

                    # Check if the new field name already exists
                    if new_field_name in self.selected_class.field_key_list:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Field name '{new_field_name}' has already existed!")
                        return

                    # Validate the new field name
                    is_field_name_valid = self.interface.is_valid_input(new_name=new_field_name)
                    if not is_field_name_valid:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Field name {new_field_name} is invalid! Only allow a-zA-Z, number, and underscore!")
                        return
     
                    rename_field_command = Command.RenameFieldCommand(self.model, class_name=selected_class_name, old_field_name=old_field_name, 
                                                                      new_field_name=new_field_name, view=self, class_box=self.selected_class, is_gui=True)
                    self.input_handler.execute_command(rename_field_command)
                        
       
    def edit_field_type(self):
        if self.selected_class:
            if self.selected_class.field_key_list: 
                # Initialize the dialog
                edit_field_type_dialog = Dialog("Edit Field Type")
                edit_field_type_dialog.edit_field_type_popup(self.selected_class)
                
                # Execute the dialog and wait for user confirmation (OK or Cancel)
                if edit_field_type_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    
                    # Get the old and new field names after the dialog is accepted
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    field_name = edit_field_type_dialog.input_widgets['field_name'].currentText()  # Use `currentText()` for QComboBox
                    new_field_type = edit_field_type_dialog.input_widgets['new_field_type'].text()  # Use `text()` for QLineEdit
                    
                    edit_field_type_command = Command.ChangeTypeCommand(
                                self.model, 
                                class_name=selected_class_name,
                                input_name=field_name,
                                new_type=new_field_type,
                                view=self, 
                                class_box=self.selected_class, 
                                is_gui=True, 
                                is_field=True
                            )
                    self.input_handler.execute_command(edit_field_type_command)
        
            
    def add_method(self, loaded_class_name=None, loaded_return_type=None, loaded_method_name=None, is_loading=False):
        """
        Add a method to a UML class box, either during loading or interactively.

        This function either loads a method into the UML class during the loading process or allows the user
        to add a new method through a dialog box. It updates the UML class box and its internal lists.

        Parameters:
            loaded_class_name (str): The name of the class to which the method is added (used during loading).
            loaded_method_name (str): The name of the method being added (used during loading).
            is_loading (bool): Whether the function is being called during the loading process.

        Steps:
        1. If loading, find the UML class by its name and add the loaded method.
        2. If not loading, prompt the user for a method name to add to the selected UML class.
        3. Update the UML class box to reflect the new method.
        """
        if is_loading:
            # Find the UML class box by the loaded class name in the scene
            for item in self.scene().items():
                if isinstance(item, UMLClassBox) and item.class_name_text.toPlainText() == loaded_class_name:
                    selected_class_box = item  # Found the class box
                    # Add the method to the found class box
                    is_method_added = self.interface.add_method(loaded_class_name, loaded_return_type, loaded_method_name)
                    if is_method_added:
                        # Create a text item for the method and add it to the list of the found class box
                        method_text = selected_class_box.create_text_item(loaded_return_type + " " + loaded_method_name + "()", is_method=True, selectable=False, color=selected_class_box.text_color)
                        method_key = (loaded_return_type, loaded_method_name)
                        method_entry = {
                            "method_key": method_key,
                            "method_text": method_text,
                            "parameters": []
                        }
                        selected_class_box.method_list.append(method_entry)  # Add the method to the internal list
                        if len(selected_class_box.method_list) == 1:  # If this is the first method, create a separator
                            selected_class_box.create_separator(is_first=False)
                        selected_class_box.update_box()  # Update the box to reflect the changes
        else:
            if self.selected_class:
                add_method_dialog = Dialog("Add Field")
                add_method_dialog.add_method_popup()
                
                # Execute the dialog and wait for user confirmation (OK or Cancel)
                if add_method_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    method_type = add_method_dialog.input_widgets["method_type"].text()
                    method_name = add_method_dialog.input_widgets["method_name"].text()
                    
                    if not method_type.strip() and not method_name.strip():
                        return
                    elif not method_name.strip():
                        QtWidgets.QMessageBox.warning(None, "Warning", "Method name is empty!")
                        return
                    elif not method_type.strip():
                        QtWidgets.QMessageBox.warning(None, "Warning", "Method type is empty!")
                        return
                    
                    is_method_type_valid = self.interface.is_valid_input(method_type=method_type)
                    if not is_method_type_valid:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Method type {method_type} is invalid! Only allow a-zA-Z, number, and underscore!")
                        return
                    is_method_name_valid = self.interface.is_valid_input(method_name=method_name)
                    if not is_method_name_valid:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Method name {method_name} is invalid! Only allow a-zA-Z, number, and underscore!")
                        return
                    
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    
                    add_method_command = Command.AddMethodCommand(self.model, class_name=selected_class_name, type=method_type, method_name=method_name, 
                                                                  view=self, class_box=self.selected_class, is_gui=True)
                    is_method_added = self.input_handler.execute_command(add_method_command)
                    
                    if not is_method_added:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Method name '{method_name}' has the same parameter list signature as an existing method in class!")
    
    def delete_method(self):
        """
        Remove an existing method from the selected UML class.

        This function allows the user to select a method from the currently selected class 
        and delete it along with all associated parameters. It updates the UML class box 
        and its internal lists accordingly.

        Steps:
        1. Check if a class and method are selected.
        2. Prompt the user to select a method to remove.
        3. Delete the selected method and all associated parameters.
        4. Update the UML class box to reflect the changes.
        """
        if self.selected_class:
            if self.selected_class.method_list:
                delete_method_dialog = Dialog("Add Field")
                delete_method_dialog.delete_method_popup(self.selected_class)
                
                # Execute the dialog and wait for user confirmation (OK or Cancel)
                if delete_method_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    
                    # Extract the selected index from the display list
                    raw_method_name = delete_method_dialog.input_widgets["raw_method_name"].currentText()
                    selected_index = int(raw_method_name.split(":")[0].strip()) - 1
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    
                    # Execute the delete command with the correct method index
                    delete_method_command = Command.DeleteMethodCommand(self.model, class_name=selected_class_name, 
                                                                        method_num=str(selected_index + 1), view=self, class_box=self.selected_class, is_gui=True)
                    self.input_handler.execute_command(delete_method_command)

    def rename_method(self):
        """
        Rename an existing method in the selected UML class.

        This function allows the user to select a method and provide a new name for it.
        The method name is updated, and the UML class box is refreshed.

        Steps:
        1. Check if a class and method are selected.
        2. Prompt the user to select a method and provide a new name.
        3. Rename the method and update the UML class box.
        """
        if self.selected_class:
            if self.selected_class.method_list:
                # Initialize the dialog
                rename_method_dialog = Dialog("Rename Field")
                rename_method_dialog.rename_method_popup(self.selected_class)
                
                # Execute the dialog and wait for user confirmation (OK or Cancel)
                if rename_method_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    
                    # Get new method name after the dialog is accepted
                    new_method_name = rename_method_dialog.input_widgets["new_method_name"].text()  # Use `text()` for QLineEdit
                    if not new_method_name.strip():
                        return
                    old_method_name_widget = rename_method_dialog.input_widgets["raw_method_name"]
                    selected_index = old_method_name_widget.currentIndex()
                    method_keys_list = rename_method_dialog.input_widgets["method_keys_list"]
                    
                    # Check if the new method name already exists
                    for each_key in method_keys_list:
                        if each_key[1] == new_method_name:
                            QtWidgets.QMessageBox.warning(None, "Warning", f"Method name '{new_method_name}' has already existed!")
                            return
                
                    is_method_name_valid = self.interface.is_valid_input(new_name=new_method_name)
                    if not is_method_name_valid:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Method name {new_method_name} is invalid! Only allow a-zA-Z, number, and underscore!")
                        return
                    
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    
                    rename_method_command = Command.RenameMethodCommand(self.model, class_name=selected_class_name, method_num=str(selected_index + 1), 
                                                                        new_name=new_method_name, view=self, class_box=self.selected_class, is_gui=True)
                    self.input_handler.execute_command(rename_method_command)
                    
                    
    def edit_method_return_type(self):
        if self.selected_class:
            if self.selected_class.method_list: 
                # Initialize the dialog
                edit_method_return_type_dialog = Dialog("Edit Method Return Type")
                edit_method_return_type_dialog.edit_method_return_type_popup(self.selected_class)
                
                # Execute the dialog and wait for user confirmation (OK or Cancel)
                if edit_method_return_type_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    
                    # Get the old and new field names after the dialog is accepted
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    method_num = edit_method_return_type_dialog.input_widgets['method_name'].currentIndex()
                    new_method_return_type = edit_method_return_type_dialog.input_widgets['new_method_return_type'].text()
                    
                    edit_method_return_type_command = Command.ChangeTypeCommand(
                                self.model, 
                                class_name=selected_class_name,
                                new_type=new_method_return_type,
                                method_num=str(method_num + 1),
                                view=self, 
                                class_box=self.selected_class, 
                                is_gui=True, 
                                is_method=True
                            )
                    self.input_handler.execute_command(edit_method_return_type_command)
                    
            
    def add_param(self,loaded_class_name=None, loaded_method_num=None, loaded_param_type=None, loaded_param_name=None, is_loading=False):
        """
        Add a parameter to a method in the UML class, either during loading or interactively.

        This function either loads a parameter into a method during the loading process 
        or allows the user to add a new parameter interactively through a dialog.

        Parameters:
            loaded_class_name (str): The class name where the parameter is being added.
            loaded_method_name (str): The method name where the parameter is being added.
            loaded_param_name (str): The parameter name being added.
            is_loading (bool): Whether the function is being called during the loading process.

        Steps:
        1. If loading, find the UML class and add the parameter to the method.
        2. If not loading, prompt the user to add a new parameter to a selected method.
        3. Update the UML class box to reflect the new parameter.
        """
        if is_loading:
            # Find the UML class box by the loaded class name in the scene
            for item in self.scene().items():
                if isinstance(item, UMLClassBox) and item.class_name_text.toPlainText() == loaded_class_name:
                    selected_class_box = item  # Found the class box
                    is_param_added = self.interface.add_parameter(loaded_class_name, str(loaded_method_num), loaded_param_type, loaded_param_name)
                    if is_param_added:
                        # Append the parameter to the method's parameter list
                        param_tuple = (loaded_param_type, loaded_param_name)
                        method_entry = selected_class_box.method_list[int(loaded_method_num) - 1]
                        method_entry["parameters"].append(param_tuple)
                        selected_class_box.param_num = len(method_entry["parameters"])
                        selected_class_box.update_box()  # Update the UML box
        else:
            if self.selected_class:
                if self.selected_class.method_list:
                    # Initialize the dialog
                    add_param_dialog = Dialog("Add Parameter")
                    add_param_dialog.add_param_popup(self.selected_class)
                    
                    # Execute the dialog and wait for user confirmation (OK or Cancel)
                    if add_param_dialog.exec_() == QtWidgets.QDialog.Accepted:
                        # Retrieve input values
                        param_type = add_param_dialog.input_widgets["param_type"].text()
                        param_name = add_param_dialog.input_widgets["new_param_name"].text()
                        method_name = add_param_dialog.input_widgets["method_type"]
                        method_name_widget = add_param_dialog.input_widgets["method_name_widget"]
                        selected_class_name = self.selected_class.class_name_text.toPlainText()
                        
                        if not param_type.strip() and not param_name.strip():
                            return
                        elif not param_name.strip():
                            QtWidgets.QMessageBox.warning(None, "Warning", "Parameter name is empty!")
                            return
                        elif not param_type.strip():
                            QtWidgets.QMessageBox.warning(None, "Warning", "Parameter type is empty!")
                            return
                        
                        # Get the selected index from the combo box
                        selected_index = method_name_widget.currentIndex()
                        
                        # Validate parameter type and name
                        is_param_type_valid = self.interface.is_valid_input(parameter_type=param_type)
                        if not is_param_type_valid:
                            QtWidgets.QMessageBox.warning(None, "Warning", f"Parameter type '{param_type}' is invalid! Only letters, numbers, and underscores are allowed!")
                            return
                        
                        is_param_name_valid = self.interface.is_valid_input(parameter_name=param_name)
                        if not is_param_name_valid:
                            QtWidgets.QMessageBox.warning(None, "Warning", f"Parameter name '{param_name}' is invalid! Only letters, numbers, and underscores are allowed!")
                            return
                        
                        method_entry = self.selected_class.method_list[selected_index]
                        
                        # Check if parameter name already exists in the selected method
                        for param_tuple in method_entry["parameters"]:
                            if param_tuple[1] == param_name:
                                QtWidgets.QMessageBox.warning(None, "Warning", f"Parameter name '{param_name}' already exists in the selected method!")
                                return
                        
                        # Get the method number (assuming method numbers start from 1)
                        method_num = str(selected_index + 1)
                        
                        add_param_command = Command.AddParameterCommand(self.model,class_name=selected_class_name,
                                                                        method_num=method_num,param_type=param_type,
                                                                        param_name=param_name, view=self, class_box=self.selected_class, is_gui=True)
                        is_param_added = self.input_handler.execute_command(add_param_command)
                        
                        if not is_param_added:
                            QtWidgets.QMessageBox.warning(None, "Warning", f"Method name '{method_name}' has the same parameter list signature as an existing method in class!")

    def delete_param(self):
        """
        Remove a parameter from a selected method in the UML class.
        """
        if self.selected_class:
            if self.selected_class.method_list:
                delete_param_dialog = Dialog("Delete Parameter")
                delete_param_dialog.delete_param_popup(self.selected_class)
                
                # Execute dialog and wait for user confirmation
                if delete_param_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    param_name = delete_param_dialog.input_widgets["param_name_only"]
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    selected_method_index = delete_param_dialog.input_widgets["method_name_widget"].currentIndex()
                    selected_param_index = delete_param_dialog.input_widgets["param_name_widget"].currentIndex()
                    
                    delete_param_command = Command.DeleteParameterCommand(self.model, class_name=selected_class_name,
                                                                          method_num=str(selected_method_index + 1), view=self, class_box=self.selected_class, 
                                                                          selected_param_index=selected_param_index, param_name=param_name, is_gui=True)
                    is_param_deleted = self.input_handler.execute_command(delete_param_command)
                    method_entry = self.selected_class.method_list[selected_method_index]
                    if not is_param_deleted:
                        method_key = method_entry["method_key"]
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Method name '{method_key[1]}' has the same parameter list signature as an existing method in class!")
            
    def rename_param(self):
        """
        Rename a parameter within a selected method in the UML class.

        This function allows the user to select a method and a parameter and provide a new name for the parameter.
        The parameter's name is updated, and the UML class box is refreshed.

        Steps:
        1. Check if a class and method are selected.
        2. Prompt the user to select a method and a parameter to rename.
        3. Rename the parameter and update the UML class box.
        """
        if self.selected_class:
            if self.selected_class.method_list:
                # Initialize the dialog
                rename_param_dialog = Dialog("Rename Parameter")
                rename_param_dialog.rename_param_popup(self.selected_class)
                
                # Execute the dialog and wait for user confirmation (OK or Cancel)
                if rename_param_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    
                    selected_method_index = rename_param_dialog.input_widgets['method_name_widget'].currentIndex()
                    old_param_name = rename_param_dialog.input_widgets["param_name_only"]
                    new_param_name = rename_param_dialog.input_widgets['new_param_name_widget'].text()  # Use `text()` for QLineEdit
                    if not new_param_name.strip():
                        return
                    method_entry = self.selected_class.method_list[selected_method_index]
                    
                    for each_tuple in method_entry["parameters"]:
                        if new_param_name == each_tuple[1] :
                            QtWidgets.QMessageBox.warning(None, "Warning", f"Parameter name '{new_param_name}' has already existed!")
                            return
                        
                    is_param_name_valid = self.interface.is_valid_input(new_name=new_param_name)
                    if not is_param_name_valid:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Parameter name {new_param_name} is invalid! Only allow a-zA-Z, number, and underscore!")
                        return
                    
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    
                    rename_param_command = Command.RenameParameterCommand(self.model, class_name=selected_class_name, method_num=str(selected_method_index + 1),
                                                                          view=self, class_box=self.selected_class, 
                                                                          old_param_name=old_param_name, new_param_name=new_param_name, is_gui=True)
                    is_param_renamed = self.input_handler.execute_command(rename_param_command)

                    if not is_param_renamed:
                        QtWidgets.QMessageBox.warning(None, "Rename Failed", "Failed to rename the parameter.")

    def replace_param(self):
        """
        Replace all parameters of a selected method in the UML class.

        This function allows the user to replace the entire list of parameters for a given method with a new set.
        It prompts the user for a comma-separated list of parameters and updates the UML class box accordingly.

        Steps:
        1. Check if a class and method are selected.
        2. Prompt the user to enter a new list of parameters.
        3. Replace the current parameters with the new ones and update the UML class box.
        """
        if self.selected_class:
            # Ensure there are methods to choose from
            if self.selected_class.method_list:
                # Initialize the dialog
                replace_param_dialog = Dialog("Rename Parameter")
                replace_param_dialog.replace_param_list_popup(self.selected_class)
                
                # Execute the dialog and wait for user confirmation (OK or Cancel)
                if replace_param_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    
                    # Get the old and new field names after the dialog is accepted
                    new_param_string = replace_param_dialog.input_widgets['new_param_string']
                    if not new_param_string.text().strip():
                        return
                    selected_method_index = replace_param_dialog.input_widgets['method_name_widget'].currentIndex()             
                    method_entry = self.selected_class.method_list[selected_method_index]
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    new_param_list_str = [param.strip() for param in new_param_string.text().split(",") if param.strip()]
                    
                    new_param_list_obj = []
                    for param in new_param_string.text().split(","):
                        # Strip any leading or trailing whitespace from the parameter string
                        param = param.strip()
                        # Split once on the first space to separate the type and the name
                        if " " in param:
                            type_name = param.split(" ", 1)
                            # Append the tuple (type, name) to the new_param_list
                            new_param_list_obj.append((type_name[0].strip(), type_name[1].strip()))
                            
                    # Extract only the names from the new_param_list
                    param_names_only = [param[1] for param in new_param_list_obj]
                            
                    # Check for duplicate parameter names
                    unique_param_names = list(set(param_names_only))
                    if len(unique_param_names) != len(param_names_only):
                        duplicates = [param for param in param_names_only if param_names_only.count(param) > 1]
                        QtWidgets.QMessageBox.warning(None, "Warning", f"New list contain duplicate{duplicates}!")
                        return
                        
                    for each_param in unique_param_names:
                        is_param_name_valid = self.interface.is_valid_input(parameter_name=each_param)
                        if not is_param_name_valid:
                            QtWidgets.QMessageBox.warning(None, "Warning", f"Parameter name {each_param} is invalid! Only allow a-zA-Z, number, and underscore!")
                            return
                            
                    print(new_param_list_obj)
                    
                    rename_param_command = Command.ReplaceParameterListCommand(self.model, class_name=selected_class_name, 
                                                                               method_num=str(selected_method_index + 1), view=self, 
                                                                               class_box=self.selected_class,
                                                                               new_param_list_obj=new_param_list_obj,
                                                                               new_param_list_str=new_param_list_str, is_gui=True)
                    is_param_list_replaced = self.input_handler.execute_command(rename_param_command)
                    
                    if not is_param_list_replaced:
                        method_key = method_entry["method_key"]
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Method name '{method_key[1]}' has the same parameter list signature as an existing method in class!")
                        
    def edit_param_type(self):
        if self.selected_class:
            if self.selected_class.method_list: 
                # Initialize the dialog
                edit_param_type_dialog = Dialog("Edit Method Return Type")
                edit_param_type_dialog.edit_param_type_popup(self.selected_class)
                
                # Execute the dialog and wait for user confirmation (OK or Cancel)
                if edit_param_type_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    
                    # Get the old and new field names after the dialog is accepted
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    method_num = edit_param_type_dialog.input_widgets['method_name_widget'].currentIndex()
                    param_name = edit_param_type_dialog.input_widgets["param_name_only"]
                    new_param_type = edit_param_type_dialog.input_widgets['new_param_type'].text()
                    
                    edit_param_type_command = Command.ChangeTypeCommand(
                                self.model, 
                                class_name=selected_class_name,
                                new_type=new_param_type,
                                method_num=str(method_num + 1),
                                input_name=param_name,
                                view=self, 
                                class_box=self.selected_class, 
                                is_gui=True, 
                                is_param=True
                            )
                    self.input_handler.execute_command(edit_param_type_command)
    
            
    def add_relationship(self, loaded_source_class=None, loaded_dest_class=None, loaded_type=None, is_loading=False):
        """
        Add a relationship between two UML classes.

        This function adds a relationship between a source class and a destination class, either by loading the data
        from a saved file or by prompting the user to enter the required information.

        Parameters:
            loaded_source_class (str): The source class for the relationship (used when loading from a file).
            loaded_dest_class (str): The destination class for the relationship (used when loading from a file).
            loaded_type (str): The type of relationship (e.g., inheritance, association) (used when loading from a file).
            is_loading (bool): If True, load the relationship from a saved file.

        Steps:
        1. If loading, find the UML class in the scene and add the relationship to the class.
        2. If not loading, prompt the user to select a source class, destination class, and relationship type.
        3. Add the selected relationship to the UML class and update the display.
        """
        if is_loading:
            # Initialize variables to hold the source and destination class boxes
            source_class_obj = None
            dest_class_obj = None

            # Loop through the scene items to find the source and destination classes
            for item in self.scene().items():
                if isinstance(item, UMLClassBox):
                    class_name = item.class_name_text.toPlainText()
                    if class_name == loaded_source_class:
                        source_class_obj = item
                        source_class_obj.is_source_class = True
                    elif class_name == loaded_dest_class:
                        dest_class_obj = item
                # If both classes are found, no need to continue looping
                if source_class_obj and dest_class_obj:
                    break

            if source_class_obj and dest_class_obj:
                # Add the relationship via the interface
                is_rel_added = self.interface.add_relationship_gui(
                    source_class_name=loaded_source_class,
                    destination_class_name=loaded_dest_class,
                    type=loaded_type
                )
                if is_rel_added:
                    arrow_line = ArrowLine(source_class_obj, dest_class_obj, loaded_type)
                    value = {"dest_class" : loaded_dest_class, 
                            "arrow_list" : arrow_line}
                    if loaded_source_class not in self.relationship_track_list:
                        self.relationship_track_list[loaded_source_class] = []
                    self.relationship_track_list[loaded_source_class].append(value)
                    self.scene().addItem(arrow_line)  # Add the arrow to the scene to display it
                    # Update the class boxes
                    source_class_obj.update_box()
                    dest_class_obj.update_box()
        else:
            if self.selected_class:
                # Initialize the dialog
                type_list = [enum.value for enum in RelationshipType]
                add_rel_dialog = Dialog("Add Relationship")
                add_rel_dialog.add_relationship_popup(self.class_name_list, type_list)
                
                # Execute the dialog and wait for user confirmation (OK or Cancel)
                if add_rel_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    
                    # Get the old and new field names after the dialog is accepted
                    dest_class = add_rel_dialog.input_widgets["destination_class"].currentText()  # Use `currentText()` 
                    type = add_rel_dialog.input_widgets["type"].currentText()  # Use `currentText()` 
                    source_class = self.selected_class.class_name_text.toPlainText()
                    
                    add_rel_command = Command.AddRelationshipCommand(self.model, source_class=source_class,
                                                                    view=self, class_box=self.selected_class,
                                                                    dest_class=dest_class, 
                                                                    rel_type=type, is_gui=True)
                    is_rel_added = self.input_handler.execute_command(add_rel_command)
                    
                    if not is_rel_added:
                        QtWidgets.QMessageBox.warning(None, "Warning", "Relationship has already existed!")

    def delete_relationship(self):
        """
        Delete an existing relationship from the UML class.

        This function prompts the user to select a source class and destination class for the relationship to be deleted.
        The relationship is removed if it exists, and the UML class box is updated.

        Steps:
        1. Prompt the user to select a source class and destination class.
        2. Check if the relationship exists and delete it if found.
        3. Update the UML class box display.
        """
        if self.selected_class:
            if self.selected_class.arrow_line_list:
                source_class = self.selected_class.class_name_text.toPlainText()
                delete_rel_dialog = Dialog("Delete Relationship")
                delete_rel_dialog.delete_relationship_popup(source_class, self.relationship_track_list)
                
                # Execute the dialog and wait for user confirmation (OK or Cancel)
                if delete_rel_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    
                    # Get the old and new field names after the dialog is accepted
                    dest_class = delete_rel_dialog.input_widgets["destination_class_list_of_current_source_class"].currentText()  # Use `currentText()`
                     
                    delete_rel_command = Command.DeleteRelationshipCommand(self.model, source_class=source_class,
                                                                           view=self, class_box=self.selected_class, 
                                                                           dest_class=dest_class, is_gui=True)
                    self.input_handler.execute_command(delete_rel_command)

        # This is for checking the list in the terminal
        print(f"Current relationship tracking: {self.relationship_track_list}")

    def change_relationship_type(self):
        """
        Change the type of an existing relationship between two UML classes.

        This function allows the user to modify the relationship type between a source and destination class.
        The updated relationship type is applied, and the UML class box is updated.

        Steps:
        1. Prompt the user to select the source and destination classes.
        2. Check if the relationship exists and allow the user to select a new type.
        3. Update the UML class box with the new relationship type.
        """
        if self.selected_class:
            if self.selected_class.arrow_line_list:
                type_list = [enum.value for enum in RelationshipType]
                source_class = self.selected_class.class_name_text.toPlainText()
                change_rel_type_dialog = Dialog("Change Relationship Type")
                change_rel_type_dialog.change_type_popup(source_class, self.relationship_track_list, type_list)
                
                # Execute the dialog and wait for user confirmation (OK or Cancel)
                if change_rel_type_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    
                    # Get the old and new field names after the dialog is accepted
                    dest_class = change_rel_type_dialog.input_widgets["destination_class_list_of_current_source_class"].currentText()  # Use `currentText()` 
                    new_type = change_rel_type_dialog.input_widgets["type"].currentText()  # Use `currentText()` 

                    relationships = self.relationship_track_list.get(source_class)
                    for relationship in relationships:
                        if relationship["dest_class"] == dest_class:
                            arrow_line = relationship["arrow_list"]
                            print(f"Current Type: {arrow_line.arrow_type}, New Type: {new_type}")  # Debugging output

                            # Normalize and compare the relationship types
                            if new_type.strip().lower() == arrow_line.arrow_type.strip().lower():
                                QtWidgets.QMessageBox.warning(None, "Warning", f"New relationship type is identical to current type {new_type}!")
                                return
                            
                            change_rel_type_command = Command.ChangeTypeCommand(
                                self.model, 
                                source_class=source_class, 
                                dest_class=dest_class,  # Use dest_class directly
                                new_type=new_type,
                                arrow_line=arrow_line, 
                                view=self, 
                                class_box=self.selected_class, 
                                is_gui=True, 
                                is_rel=True
                            )
                            
                            is_rel_type_changed = self.input_handler.execute_command(change_rel_type_command)
                            if not is_rel_type_changed:
                                return
                        
    #################################################################
    def open_folder_gui(self):
        """
        Open a file dialog to allow the user to select a JSON file for loading into the application.

        This function uses the `QFileDialog` to let the user select a `.json` file from the file system.
        If a valid JSON file is selected, the function proceeds to load the file into the interface.
        If the selected file is not a JSON file, a warning is displayed to the user.

        Steps:
        1. Clear the current UML scene.
        2. Open the file dialog and retrieve the file path selected by the user.
        3. Validate that the selected file is a JSON file.
        4. If valid, load the selected JSON file into the interface.
        """
        # Show an open file dialog and store the selected file path
        full_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", os.getcwd(), "JSON Files (*.json)")
        # Check if the user canceled the dialog (full_path will be empty if canceled)
        if not full_path:
            return  # Exit the function if the user cancels the dialog
        # Check if the selected file is a JSON file
        if not full_path.endswith('.json'):
            QtWidgets.QMessageBox.warning(None, "Warning", "The selected file is not a JSON file. Please select a valid JSON file.")
            return
        self.clear_current_scene()  # Clear the scene before loading a new file
        # If a valid file is selected, proceed to load it into the interface
        if full_path:
            file_base_name = os.path.basename(full_path)  # Extract the file name from the full path
            file_name_only = os.path.splitext(file_base_name)[0]  # Remove the file extension
            self.interface.load_gui(file_name_only, full_path, self)  # Load the file into the GUI
     
    def save_as_gui(self):
        """
        Open a save file dialog to select a file location for saving.
        """
        full_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", os.getcwd(),"JSON Files (*.json)")
        if not full_path:
            return  # If canceled, just return and do nothing
        if not full_path.endswith('.json'):
            QtWidgets.QMessageBox.warning(None, "Warning", "The selected file is not a JSON file. Please select a valid JSON file.")
            return
        if full_path:
            file_base_name = os.path.basename(full_path)
            file_name_only = os.path.splitext(file_base_name)[0]
            self.interface.save_gui(file_name_only, full_path)

    def save_gui(self):
        """
        Save to current active file, if no active file, prompt user to create new json file
        """
        current_active_file_path = self.interface.get_active_file_gui()
        if current_active_file_path == "No active file!":
            self.save_as_gui()
        else:
            file_base_name = os.path.basename(current_active_file_path)
            file_name_only = os.path.splitext(file_base_name)[0]
            self.interface.save_gui(file_name_only, current_active_file_path, self.class_name_list)  
            
    def undo(self):
        self.input_handler.undo()
        self.scene().update()
    
    def redo(self):
        self.input_handler.redo()   
        self.scene().update()
    
    def clear_current_scene(self):
        """
        Remove all UMLClassBox items from the scene.
        """
        # Iterate through all items in the scene
        for item in self.scene().items():
            # Check if the item is a UMLClassBox
            if isinstance(item, UMLClassBox) or isinstance(item, ArrowLine):
                # Remove the UMLClassBox from the scene
                self.scene().removeItem(item)
                     
    #################################################################
    ## CONTEXT MENU ACTIONS ##
            
    def contextMenuEvent(self, event):
        """
        Show the context menu when right-clicking on the UMLClassBox or the background.
        
        The context menu provides various options to modify the selected UML class or perform global actions 
        such as saving and loading UML diagrams.
        """

        # Create the context menu object
        contextMenu = QtWidgets.QMenu()
        
        if not self.selected_class:
            # If no UML class is selected, display options for adding a class or selecting all classes
            self.add_context_menu_action(contextMenu, "Add Class", self.add_class, enabled=True)
            if len(self.class_name_list) > 0:
                self.add_context_menu_action(contextMenu, "Select All Class", self.select_items_in_rect, enabled=True)
            else:
                self.add_context_menu_action(contextMenu, "Select All Class", self.select_items_in_rect, enabled=False)
        else:
            self.add_context_menu_separator(contextMenu)

            # CLASS MANAGEMENT OPTIONS
            self.add_context_menu_action(contextMenu, "Rename Class", self.rename_class, enabled=True)

            self.add_context_menu_separator(contextMenu)

            # FIELD OPTIONS
            self.add_context_menu_action(contextMenu, "Add Field", self.add_field, enabled=True)
            if self.selected_class.field_key_list:
                self.add_context_menu_action(contextMenu, "Delete Field", self.delete_field, enabled=True)
                self.add_context_menu_action(contextMenu, "Rename Field", self.rename_field, enabled=True)
                self.add_context_menu_action(contextMenu, "Edit Field Type", self.edit_field_type, enabled=True)
            else:
                self.add_context_menu_action(contextMenu, "Delete Field", self.delete_field, enabled=False)
                self.add_context_menu_action(contextMenu, "Rename Field", self.rename_field, enabled=False)
                self.add_context_menu_action(contextMenu, "Edit Field Type", self.edit_field_type, enabled=False)

            self.add_context_menu_separator(contextMenu)

            # METHOD OPTIONS
            self.add_context_menu_action(contextMenu, "Add Method", self.add_method, enabled=True)
            if self.selected_class.method_list:
                self.add_context_menu_action(contextMenu, "Delete Method", self.delete_method, enabled=True)
                self.add_context_menu_action(contextMenu, "Rename Method", self.rename_method, enabled=True)
                self.add_context_menu_action(contextMenu, "Edit Method Type", self.edit_method_return_type, enabled=True)
                self.add_context_menu_separator(contextMenu)
                self.add_context_menu_action(contextMenu, "Add Parameter", self.add_param, enabled=True)
                # PARAMETER OPTIONS
                if self.selected_class.param_num > 0:
                    self.add_context_menu_action(contextMenu, "Delete Parameter", self.delete_param, enabled=True)
                    self.add_context_menu_action(contextMenu, "Rename Parameter", self.rename_param, enabled=True)
                    self.add_context_menu_action(contextMenu, "Edit Param Type", self.edit_param_type, enabled=True)
                else:
                    self.add_context_menu_action(contextMenu, "Delete Parameter", self.delete_param, enabled=False)
                    self.add_context_menu_action(contextMenu, "Rename Parameter", self.rename_param, enabled=False) 
                    self.add_context_menu_action(contextMenu, "Edit Param Type", self.edit_param_type, enabled=False)
                self.add_context_menu_action(contextMenu, "Replace Parameter", self.replace_param, enabled=True)
            else:
                self.add_context_menu_action(contextMenu, "Delete Method", self.delete_method, enabled=False)
                self.add_context_menu_action(contextMenu, "Rename Method", self.rename_method, enabled=False)
                self.add_context_menu_action(contextMenu, "Edit Method Type", self.edit_method_return_type, enabled=False)
                self.add_context_menu_separator(contextMenu)
                self.add_context_menu_action(contextMenu, "Add Parameter", self.add_param, enabled=False)
                self.add_context_menu_action(contextMenu, "Delete Parameter", self.delete_param, enabled=False)
                self.add_context_menu_action(contextMenu, "Rename Parameter", self.rename_param, enabled=False)
                self.add_context_menu_action(contextMenu, "Edit Param Type", self.edit_param_type, enabled=False)
                self.add_context_menu_action(contextMenu, "Replace Parameter", self.replace_param, enabled=False)
                
            self.add_context_menu_separator(contextMenu)

            # RELATIONSHIP OPTIONS
            self.add_context_menu_action(contextMenu, "Add Relationship", self.add_relationship, enabled=True)
            if self.selected_class.is_source_class:
                self.add_context_menu_action(contextMenu, "Delete Relationship", self.delete_relationship, enabled=True)
                self.add_context_menu_action(contextMenu, "Change Type", self.change_relationship_type, enabled=True)
            else:
                self.add_context_menu_action(contextMenu, "Delete Relationship", self.delete_relationship, enabled=False)
                self.add_context_menu_action(contextMenu, "Change Type", self.change_relationship_type, enabled=False)

            # After executing an action, update the class box to reflect changes
            self.selected_class.update_box()

        # Execute the context menu at the global position (where the right-click happened)
        contextMenu.exec_(event.globalPos())


    def add_context_menu_action(self, context_menu, label, callback=None, enabled=True):
        """
        Helper function to add an action to the context menu.
        
        Parameters:
            context_menu (QMenu): The context menu to add the action to.
            label (str): The text label for the action.
            callback (function, optional): The function to be triggered when the action is selected.
            enabled (bool): Whether the action should be enabled (default is True).
        
        Returns:
            QAction: The created action.
        """
        action = context_menu.addAction(label)
        if callback:
            action.triggered.connect(callback)
        action.setEnabled(enabled)
        return action

    def add_context_menu_separator(self, context_menu):
        """ Helper function to add a separator in the context menu """
        context_menu.addSeparator()

            
    ## MOUSE EVENTS ##
            
    def wheelEvent(self, event):
        """
        Handle zoom in/out functionality using the mouse wheel.

        Parameters:
        - event (QWheelEvent): The wheel event.
        """
        if event.modifiers() & QtCore.Qt.ControlModifier:
            delta = event.angleDelta().y()
            zoom_limit = 0.5
            max_zoom_limit = 10.0
            current_scale = self.transform().m11()

            # Zoom in or out based on wheel movement
            if delta > 0 and current_scale < max_zoom_limit:
                self.scale(1.1, 1.1)
            elif delta < 0 and current_scale > zoom_limit:
                self.scale(0.9, 0.9)
            event.accept()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        """
        Handle mouse press events for starting selection, panning, or determining item selection.
        Prevent the rubber band selection from activating when clicking on UMLClassBox handles.
        """
        item = self.itemAt(event.pos())
        if isinstance(item, UMLClassBox):
            self.selected_class = item
            self.move_start_pos = item.pos()  # Store the initial position
        else:
            self.selected_class = None

        # Panning logic for middle mouse button
        if event.button() == QtCore.Qt.MiddleButton:
            # Start panning mode when the middle mouse button is pressed
            self.is_panning = True
            self.last_mouse_pos = event.pos()
            self.setCursor(QtCore.Qt.ClosedHandCursor)
            event.accept()

        # Call the parent class's mousePressEvent for default behavior
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """
        Handle mouse move events for updating the rubber band rectangle or panning the view.

        This function handles two behaviors based on user interaction:
        - If the user is dragging while holding the left button, update the rubber band selection.
        - If the user is dragging while holding the middle button, pan the view.

        Parameters:
        - event (QMouseEvent): The mouse event, providing the current mouse position, buttons pressed, etc.
        """
        if self.is_panning and self.last_mouse_pos is not None:
            # If panning is active, calculate the delta (movement) of the mouse
            delta = event.pos() - self.last_mouse_pos
            # Temporarily disable the anchor point for transformations to pan freely
            self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
            # Translate the view based on the mouse movement
            self.translate(delta.x(), delta.y())
            # Update the last mouse position to the current position
            self.last_mouse_pos = event.pos()
            # Request an update of the view
            self.viewport().update()
            event.accept()
            
        # Call the parent class's mouseMoveEvent to ensure default behavior
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events to end panning or finalize the rectangular selection.

        This function ends user actions depending on the released mouse button:
        - Left-click: Finalize the rubber band selection and select items within the rectangle.
        - Middle-click: End panning mode and reset the cursor.

        Parameters:
        - event (QMouseEvent): The mouse event, providing information about the button released and the position.
        """
        if event.button() == QtCore.Qt.MiddleButton and self.is_panning:
            # End panning mode when the middle mouse button is released
            self.is_panning = False
            self.last_mouse_pos = None
            # Restore the cursor to the default arrow
            self.setCursor(QtCore.Qt.ArrowCursor)
            event.accept()
            
        if self.selected_class and event.button() == QtCore.Qt.LeftButton:
            # Capture the new position after the move
            new_x = self.selected_class.pos().x()
            new_y = self.selected_class.pos().y()
            old_x = self.move_start_pos.x()
            old_y = self.move_start_pos.y()
            
            # Only create and execute the command if the position has changed
            if (new_x, new_y) != (old_x, old_y):
                move_unit_command = Command.MoveUnitCommand(
                    class_box=self.selected_class, 
                    old_x=old_x, 
                    old_y=old_y, 
                    new_x=new_x, 
                    new_y=new_y
                )
                self.input_handler.execute_command(move_unit_command)

        # Call the parent class's mouseReleaseEvent to ensure default behavior
        super().mouseReleaseEvent(event)
        self.viewport().update()
    
    def keyPressEvent(self, event):
        """
        Handle key press events (e.g., Delete key to remove items).

        Parameters:
        - event (QKeyEvent): The key event.
        """
        if event.key() == QtCore.Qt.Key_Delete:
            self.delete_class()
            event.accept()
        else:
            super().keyPressEvent(event)

    #################################################################
    ## UTILITY FUNCTIONS ##
    
    def select_items_in_rect(self, rect):
        """
        Select all items within the provided rectangular area.
        """
        items_in_rect = self.scene().items(rect)
        for item in self.scene().selectedItems():
            if isinstance(item, UMLClassBox):
                item.setSelected(False)  # Deselect previously selected items
        for item in items_in_rect:
            if isinstance(item, UMLClassBox):
                item.setSelected(True)  # Select new items in the rectangle
                
    def new_file(self):
        reply = QtWidgets.QMessageBox.question(self, "New File",
                                            "Any unsaved work will be deleted! Are you sure you want to create a new file? ",
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Save)
        # If the user chooses 'Yes', the program will create a new file
        if reply == QtWidgets.QMessageBox.Yes:
            self.clear_current_scene()
            self.set_light_mode()
            self.class_name_list = {}
            self.interface.new_file()
        elif reply == QtWidgets.QMessageBox.Save:
            self.save_gui()

    def set_grid_visible(self, visible):
        """
        Control the visibility of the grid lines.

        Parameters:
        - visible (bool): If True, the grid is shown; if False, it is hidden.
        """
        self.grid_visible = visible
        self.viewport().update()

    def set_light_mode(self):
        """
        Set the view to light mode.
        """
        self.is_dark_mode = False
        self.viewport().update()
        self.scene().update()

    def set_dark_mode(self):
        """
        Set the view to dark mode.
        """
        self.is_dark_mode = True
        self.viewport().update()
        self.scene().update()

    def toggle_mode(self):
        """
        Toggle between dark mode and light mode.
        """
        if self.is_dark_mode:
            self.set_light_mode()
        else:
            self.set_dark_mode()