###################################################################################################

import os
from PyQt5 import QtWidgets, QtGui, QtCore
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_class_box import UMLClassBox
# from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_arrow_line import Arrow
from UML_ENUM_CLASS.uml_enum import RelationshipType
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_custom_dialog import CustomInputDialog as Dialog

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
        
        # Class name list
        self.class_name_list = []
        
        # Relationship pair list
        self.relationship_track_list = {}
        
        # Initialize canvas properties
        self.is_dark_mode = False  # Flag for light/dark mode

        # Set initial view properties
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setSceneRect(-5000, -5000, 10000, 10000)  # Large scene size
        self.setScene(self.scene())

        # Panning state variables
        self.is_panning = False  # Flag to indicate if panning is active

        # Track selected class or arrow
        self.selected_class = False

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
    def add_class(self, loaded_class_name=None, is_loading=False):
        """
        Add a sample UML class box to the scene.
        """
        if is_loading:
            is_class_added = self.interface.add_class(loaded_class_name)
            if is_class_added:
                class_box = UMLClassBox(self.interface, class_name=loaded_class_name)
                self.class_name_list.append(loaded_class_name)
                self.scene().addItem(class_box)
        else:
            # Display a dialog asking the user for the new class name
            input_class_name, ok = QtWidgets.QInputDialog.getText(None, "Add Class", "Enter class name:")
            if ok and input_class_name:
                is_class_name_valid = self.interface.is_valid_input(class_name=input_class_name)
                if not is_class_name_valid:
                    QtWidgets.QMessageBox.warning(None, "Warning", f"Class name {input_class_name} is invalid! Only allow a-zA-Z, number, and underscore!")
                    return
                is_class_added = self.interface.add_class(input_class_name)
                if is_class_added:
                    self.class_name_list.append(input_class_name)
                    class_box = UMLClassBox(self.interface, class_name=input_class_name)
                    self.scene().addItem(class_box)
                else:
                    QtWidgets.QMessageBox.warning(None, "Warning", f"Class '{input_class_name}' has already existed!")
            
    def delete_class(self):
        """
        Delete the selected class or arrow from the scene.
        """  
        if self.selected_class:
            # Remove the class box
            input_class_name = self.selected_class.class_name_text.toPlainText()
            is_class_deleted = self.interface.delete_class(input_class_name)
            if is_class_deleted:
                self.class_name_list.remove(input_class_name)
                self.scene().removeItem(self.selected_class)
                self.selected_class = None
            else:
                QtWidgets.QMessageBox.warning(None, "Warning", f"Class '{input_class_name}' has already existed!")
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
                is_class_renamed = self.interface.rename_class(old_class_name, new_class_name)
                if is_class_renamed:
                    self.change_name_in_relationship_after_rename_class(old_class_name, new_class_name)
                    self.class_name_list[self.class_name_list.index(old_class_name)] = new_class_name
                    self.selected_class.class_name_text.setPlainText(new_class_name)
                    self.selected_class.update_box()
                else:
                    QtWidgets.QMessageBox.warning(None, "Warning", f"New class name'{new_class_name}' has already existed!")
    
    def change_name_in_relationship_after_rename_class(self, old_class_name, new_class_name):
        for item in self.scene().items():
            if isinstance(item, UMLClassBox):
                if item.relationship_list:
                    for each_relationship in item.relationship_list:
                        if each_relationship["source"].toPlainText() == old_class_name:
                            self.scene().removeItem(each_relationship["source"])
                            each_relationship["source"] = item.create_text_item(new_class_name, selectable=False, color=item.text_color)
                        if each_relationship["dest"].toPlainText() == old_class_name:
                            self.scene().removeItem(each_relationship["dest"])
                            each_relationship["dest"] = item.create_text_item(new_class_name, selectable=False, color=item.text_color)
                    item.update_box()
            
    def add_field(self, loaded_class_name=None, loaded_field_name=None, is_loading=False):
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
                    is_field_added = self.interface.add_field(loaded_class_name, loaded_field_name)
                    if is_field_added:
                        # Create a text item for the field and add it to the list of the found class box
                        field_text = selected_class_box.create_text_item(loaded_field_name, is_field=True, selectable=False, color=selected_class_box.text_color)
                        selected_class_box.field_list[loaded_field_name] = field_text  # Add the field to the internal list
                        selected_class_box.field_name_list.append(loaded_field_name)  # Track the field name in the name list
                        selected_class_box.update_box()  # Update the box to reflect the changes
        else:
            if self.selected_class:
                # Display a dialog asking the user for the new field name
                field_name, ok = QtWidgets.QInputDialog.getText(None, "Add Field", "Enter field name:")
                # If the user confirms and provides a valid name, create and add the field
                if ok and field_name:
                    is_field_name_valid = self.interface.is_valid_input(field_name=field_name)
                    if not is_field_name_valid:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Field name {field_name} is invalid! Only allow a-zA-Z, number, and underscore!")
                        return
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    is_field_added = self.interface.add_field(selected_class_name, field_name)
                    if is_field_added:
                        # Create a text item for the field and add it to the list
                        field_text = self.selected_class.create_text_item(field_name, is_field=True, selectable=False, color=self.selected_class.text_color)
                        self.selected_class.field_list[field_name] = field_text  # Add the field to the internal list
                        self.selected_class.field_name_list.append(field_name)  # Track the field name in the name list
                        self.selected_class.update_box()  # Update the box to reflect the changes
                    else:
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
            if self.selected_class.field_name_list:
                # Display a dialog asking the user to select a field to remove
                field_name, ok = QtWidgets.QInputDialog.getItem(None, "Remove Field", "Select field to remove:", self.selected_class.field_name_list, 0, False)
                # If the user confirms, remove the selected field from the class
                if ok and field_name:
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    is_field_deleted = self.interface.delete_field(selected_class_name, field_name)
                    if is_field_deleted:
                        self.selected_class.field_name_list.remove(field_name)  # Remove from the name list
                        self.selected_class.scene().removeItem(self.selected_class.field_list.pop(field_name))  # Remove the text item from the scene
                        self.selected_class.update_box()  # Update the box to reflect the changes
    
    def rename_field(self):
        if self.selected_class:
            if self.selected_class.field_name_list: 
                # Initialize the dialog
                rename_field_dialog = Dialog("Rename Field")
                rename_field_dialog.rename_field_popup(self.selected_class)
                
                # Execute the dialog and wait for user confirmation (OK or Cancel)
                if rename_field_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    
                    # Get the old and new field names after the dialog is accepted
                    old_field_name = rename_field_dialog.input_widgets['old_field_name'].currentText()  # Use `currentText()` for QComboBox
                    new_field_name = rename_field_dialog.input_widgets['new_field_name'].text()  # Use `text()` for QLineEdit

                    # Check if the new field name already exists
                    if new_field_name in self.selected_class.field_name_list:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Field name '{new_field_name}' has already existed!")
                        return

                    # Validate the new field name
                    is_field_name_valid = self.interface.is_valid_input(new_name=new_field_name)
                    if not is_field_name_valid:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Field name {new_field_name} is invalid! Only allow a-zA-Z, number, and underscore!")
                        return

                    # Proceed with renaming the field (example logic below)
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    is_field_renamed = self.interface.rename_field(selected_class_name, old_field_name, new_field_name)
                        
                    if is_field_renamed:
                        # Update the field name in the list and refresh the display
                        if old_field_name in self.selected_class.field_list:
                            self.selected_class.field_list[new_field_name] = self.selected_class.field_list.pop(old_field_name)  # Rename the field in the internal list
                            self.selected_class.field_list[new_field_name].setPlainText(new_field_name)  # Set the new field name
                            self.selected_class.field_name_list[self.selected_class.field_name_list.index(old_field_name)] = new_field_name  # Update the name list
                            self.selected_class.update_box()  # Refresh the box display
                    
            
    def add_method(self, loaded_class_name=None, loaded_method_name=None, is_loading=False):
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
                    is_method_added = self.interface.add_method(loaded_class_name, loaded_method_name)
                    if is_method_added:
                        # Create a text item for the method and add it to the list of the found class box
                        method_text = selected_class_box.create_text_item(loaded_method_name + "()", is_method=True, selectable=False, color=selected_class_box.text_color)
                        selected_class_box.method_list[loaded_method_name] = method_text  # Add the method to the internal list
                        selected_class_box.method_name_list[loaded_method_name] = []  # Track the method name in the name list
                        if len(selected_class_box.method_name_list) == 1:  # If this is the first method, create a separator
                            selected_class_box.create_separator(is_first=False)
                        selected_class_box.update_box()  # Update the box to reflect the changes
        else:
            if self.selected_class:
                # Display a dialog asking for the new method name
                method_name, ok = QtWidgets.QInputDialog.getText(None, "Add Method", "Enter method name:")

                # If the user confirms and provides a valid method name, add it to the UML box
                if ok and method_name:
                    is_method_name_valid = self.interface.is_valid_input(method_name=method_name)
                    if not is_method_name_valid:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Method name {method_name} is invalid! Only allow a-zA-Z, number, and underscore!")
                        return
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    is_method_added = self.interface.add_method(selected_class_name, method_name)
                    if is_method_added:
                        method_text = self.selected_class.create_text_item(method_name + "()", is_method=True, selectable=False, color=self.selected_class.text_color)
                        self.selected_class.method_list[method_name] = method_text  # Store the method text
                        self.selected_class.method_name_list[method_name] = []  # Track the method's parameters
                        if len(self.selected_class.method_name_list) == 1:  # If this is the first method, create a separator
                            self.selected_class.create_separator(is_first=False)
                        self.selected_class.update_box()  # Update the UML box
                    else:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Method name '{method_name}' has already existed!")
    
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
                # Ask the user to select a method to remove
                method_name, ok = QtWidgets.QInputDialog.getItem(None, "Remove Method", "Select method to remove:", self.selected_class.method_name_list, 0, False)

                if ok and method_name:
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    is_method_deleted = self.interface.delete_method(selected_class_name, method_name)
                    if is_method_deleted:
                        self.selected_class.method_name_list.pop(method_name)  # Remove from method list
                        self.scene().removeItem(self.selected_class.method_list.pop(method_name))  # Remove the method text
                        self.selected_class.update_box()  # Refresh the UML box

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
                    
                    # Get the old and new field names after the dialog is accepted
                    old_method_name = rename_method_dialog.input_widgets['old_method_name'].currentText()  # Use `currentText()` for QComboBox
                    new_method_name = rename_method_dialog.input_widgets['new_method_name'].text()  # Use `text()` for QLineEdit

                    # Check if the new field name already exists
                    method_names = list(self.selected_class.method_name_list.keys())
                    if new_method_name in method_names:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Method name '{new_method_name}' has already existed!")
                        return
                
                    is_method_name_valid = self.interface.is_valid_input(new_name=new_method_name)
                    if not is_method_name_valid:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Method name {new_method_name} is invalid! Only allow a-zA-Z, number, and underscore!")
                        return
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    is_method_renamed = self.interface.rename_method(selected_class_name, old_method_name, new_method_name)
                    if is_method_renamed:
                        # Update the method name and refresh the UI
                        if old_method_name in self.selected_class.method_list:
                            self.selected_class.method_list[new_method_name] = self.selected_class.method_list.pop(old_method_name)  # Update the method name in the list
                            self.selected_class.method_list[new_method_name].setPlainText(new_method_name + "()")  # Set the new name in the UML box
                            self.selected_class.method_name_list[new_method_name] = self.selected_class.method_name_list.pop(old_method_name)  # Track the change
                            self.selected_class.update_box()  # Refresh the UML box display
            
    def add_param(self,loaded_class_name=None, loaded_method_name=None, loaded_param_name=None, is_loading=False):
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
                    is_param_added = self.interface.add_parameter(loaded_class_name, loaded_method_name, loaded_param_name)
                    if is_param_added:
                        # Add the parameter to the selected method and update the UML box
                        selected_class_box.method_name_list[loaded_method_name].append(loaded_param_name)  # Track the parameter
                        selected_class_box.parameter_name_list.append(loaded_param_name)  # Add to the list of parameter names
                        selected_class_box.update_box()  # Update the UML box
        else:
            if self.selected_class:
                if self.selected_class.method_list:
                    # Initialize the dialog
                    add_param_dialog = Dialog("Add Parameter")
                    add_param_dialog.add_param_popup(self.selected_class)
                    
                    # Execute the dialog and wait for user confirmation (OK or Cancel)
                    if add_param_dialog.exec_() == QtWidgets.QDialog.Accepted:
                        
                        # Get the old and new field names after the dialog is accepted
                        method_name = add_param_dialog.input_widgets['current_method'].currentText()  # Use `currentText()` for QComboBox
                        param_name = add_param_dialog.input_widgets['new_param_name'].text()  # Use `text()` for QLineEdit
                        if param_name in self.selected_class.method_name_list[method_name]:
                            QtWidgets.QMessageBox.warning(None, "Warning", f"Parameter name '{param_name}' has already existed!")
                            return
                        is_param_name_valid = self.interface.is_valid_input(parameter_name=param_name)
                        if not is_param_name_valid:
                            QtWidgets.QMessageBox.warning(None, "Warning", f"Parameter name {param_name} is invalid! Only allow a-zA-Z, number, and underscore!")
                            return
                        selected_class_name = self.selected_class.class_name_text.toPlainText()
                        is_param_added = self.interface.add_parameter(selected_class_name, method_name, param_name)
                        if is_param_added:
                            # Add the parameter to the selected method and update the UML box
                            self.selected_class.method_name_list[method_name].append(param_name)  # Track the parameter
                            self.selected_class.parameter_name_list.append(param_name)  # Add to the list of parameter names
                            self.selected_class.update_box()  # Update the UML box

    def delete_param(self):
        """
        Remove a parameter from a selected method in the UML class.

        This function allows the user to choose a method and a parameter to delete.
        The parameter is removed from the method, and the UML class box is updated.

        Steps:
        1. Check if a class and method are selected.
        2. Prompt the user to select a method and a parameter to delete.
        3. Remove the parameter and update the UML class box.
        """
        if self.selected_class:
            if self.selected_class.method_name_list:
               # Initialize the dialog
                delete_param_dialog = Dialog("Delete Parameter")
                delete_param_dialog.delete_param_popup(self.selected_class)
                
                # Execute the dialog and wait for user confirmation (OK or Cancel)
                if delete_param_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    
                    # Get the old and new field names after the dialog is accepted
                    method_name = delete_param_dialog.input_widgets['current_method'].currentText()  # Use `currentText()` for QComboBox
                    param_name = delete_param_dialog.input_widgets['param_name'].currentText()  # Use `currentText()` for QComboBox
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    is_param_deleted = self.interface.delete_parameter(selected_class_name, method_name, param_name)
                    if is_param_deleted:
                        # Remove the parameter and update the UML box
                        self.selected_class.method_name_list[method_name].remove(param_name)  # Remove from method's parameter list
                        self.selected_class.parameter_name_list.remove(param_name)  # Remove from the global parameter list
                        self.selected_class.update_box()  # Refresh the UML box
            
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
            if self.selected_class.method_name_list:
                # Initialize the dialog
                rename_param_dialog = Dialog("Rename Parameter")
                rename_param_dialog.rename_param_popup(self.selected_class)
                
                # Execute the dialog and wait for user confirmation (OK or Cancel)
                if rename_param_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    
                    # Get the old and new field names after the dialog is accepted
                    method_name = rename_param_dialog.input_widgets['current_method'].currentText()  # Use `currentText()` for QComboBox
                    old_param_name = rename_param_dialog.input_widgets['old_param_name'].currentText()  # Use `currentText()` for QComboBox
                    new_param_name = rename_param_dialog.input_widgets['new_param_name'].text()  # Use `text()` for QLineEdit
                    if new_param_name in self.selected_class.method_name_list:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Parameter name '{new_param_name}' has already existed!")
                        return
                    is_param_name_valid = self.interface.is_valid_input(new_name=new_param_name)
                    if not is_param_name_valid:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Parameter name {new_param_name} is invalid! Only allow a-zA-Z, number, and underscore!")
                        return
                    selected_class_name = self.selected_class.class_name_text.toPlainText()
                    is_param_renamed = self.interface.rename_parameter(selected_class_name, method_name, old_param_name, new_param_name)
                    if is_param_renamed:
                        # Update the parameter name and refresh the UML box
                        param_list = self.selected_class.method_name_list[method_name]
                        param_list[param_list.index(old_param_name)] = new_param_name  # Update in the method's parameter list
                        self.selected_class.parameter_name_list[self.selected_class.parameter_name_list.index(old_param_name)] = new_param_name  # Track the change
                        self.selected_class.update_box()  # Refresh the UML box

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
            if self.selected_class.method_name_list:
                # Initialize the dialog
                replace_param_dialog = Dialog("Rename Parameter")
                replace_param_dialog.replace_param_list_popup(self.selected_class)
                
                # Execute the dialog and wait for user confirmation (OK or Cancel)
                if replace_param_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    
                    # Get the old and new field names after the dialog is accepted
                    method_name = replace_param_dialog.input_widgets['current_method'].currentText()  # Use `currentText()` for QComboBox
                    new_param_string = replace_param_dialog.input_widgets['new_param_string'].text()  # Use `text()` for QLineEdit
                    # Split the input string by commas to form a list of parameters
                    new_param_list = [param.strip() for param in new_param_string.split(",") if param.strip()]
                    # Check for duplicate parameter names
                    unique_param_names = list(set(new_param_list))
                    for each_param in unique_param_names:
                        is_param_name_valid = self.interface.is_valid_input(parameter_name=each_param)
                        if not is_param_name_valid:
                            QtWidgets.QMessageBox.warning(None, "Warning", f"Parameter name {each_param} is invalid! Only allow a-zA-Z, number, and underscore!")
                            return
                    if len(unique_param_names) != len(new_param_list):
                        duplicates = [param for param in new_param_list if new_param_list.count(param) > 1]
                        QtWidgets.QMessageBox.warning(None, "Warning", f"New list contain duplicate{duplicates}!")
                    else:
                        selected_class_name = self.selected_class.class_name_text.toPlainText()
                        is_param_list_replaced = self.interface.replace_param_list_gui(selected_class_name, method_name, new_param_list)
                        if is_param_list_replaced:
                            # Clear the method's parameter list
                            self.selected_class.method_name_list[method_name].clear()
                            # Add new parameters to the method
                            for new_param in new_param_list:
                                self.selected_class.method_name_list[method_name].append(new_param)
                                self.selected_class.parameter_name_list.append(new_param)
                            # Update the box to reflect changes
                            self.selected_class.update_box()
            
    def add_relationship(self, loaded_class_name=None, loaded_source_class=None, loaded_dest_class=None, loaded_type=None, is_loading=False):
        """
        Add a relationship between two UML classes.

        This function adds a relationship between a source class and a destination class, either by loading the data
        from a saved file or by prompting the user to enter the required information.

        Parameters:
            loaded_class_name (str): The name of the class being loaded (used when loading from a file).
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
            # Find the UML class box by the loaded class name in the scene
            for item in self.scene().items():
                if isinstance(item, UMLClassBox) and item.class_name_text.toPlainText() == loaded_class_name:
                    selected_class_box = item  # Found the class box
                    # Add the relationship via the interface
                    is_rel_added = self.interface.add_relationship_gui(source_class_name=loaded_source_class, destination_class_name=loaded_dest_class, type=loaded_type)
                    if is_rel_added:
                        # Create text items for the source, destination, and type
                        source_text = selected_class_box.create_text_item(loaded_source_class, selectable=False, color=selected_class_box.text_color)
                        dest_text = selected_class_box.create_text_item(loaded_dest_class, selectable=False, color=selected_class_box.text_color)
                        type_text = selected_class_box.create_text_item(loaded_type, selectable=False, color=selected_class_box.text_color)
                        # Append the relationship data to the class's relationship list
                        selected_class_box.relationship_list.append({"source": source_text, "dest": dest_text, "type": type_text})
                        self.track_relationship(loaded_source_class, loaded_dest_class)
                        if len(selected_class_box.relationship_list) == 1:
                            # If this is the first relationship, create a separator
                            selected_class_box.create_separator(is_first=False, is_second=False)
                        # Update the class box
                        selected_class_box.update_box()
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
                    # Add the relationship via the interface
                    is_rel_added = self.interface.add_relationship_gui(source_class_name=source_class, destination_class_name=dest_class, type=type)
                    if is_rel_added:
                        # Create text items for the source, destination, and type
                        source_text = self.selected_class.create_text_item(source_class, selectable=False, color=self.selected_class.text_color)
                        dest_text = self.selected_class.create_text_item(dest_class, selectable=False, color=self.selected_class.text_color)
                        type_text = self.selected_class.create_text_item(type, selectable=False, color=self.selected_class.text_color)
                        # Append the relationship data to the class's relationship list
                        self.selected_class.relationship_list.append({"source": source_text, "dest": dest_text, "type": type_text})
                        self.track_relationship(source_class, dest_class)
                        if len(self.selected_class.relationship_list) == 1:
                            # If this is the first relationship, create a separator
                            self.selected_class.create_separator(is_first=False, is_second=False)
                        # Update the class box
                        self.selected_class.update_box()
                    else:
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
            if self.selected_class.relationship_list:
                source_class = self.selected_class.class_name_text.toPlainText()
                delete_rel_dialog = Dialog("Delete Relationship")
                delete_rel_dialog.delete_relationship_popup(source_class, self.relationship_track_list)
                
                # Execute the dialog and wait for user confirmation (OK or Cancel)
                if delete_rel_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    
                    # Get the old and new field names after the dialog is accepted
                    dest_class = delete_rel_dialog.input_widgets["destination_class_list_of_current_source_class"].currentText()  # Use `currentText()` 
                    # Delete the relationship if found
                    is_rel_deleted = self.interface.delete_relationship(source_class, dest_class)
                    if is_rel_deleted:
                        self.find_and_remove_relationship_helper(source_class, dest_class)
                            
    def track_relationship(self, source_class, dest_class):
        """
        Keep track of relationships between source class and destination class.
        """
        # If the source class is not in the dictionary, add it with an empty list
        if source_class not in self.relationship_track_list:
            self.relationship_track_list[source_class] = []

        # Append the destination class to the source class's list if it's not already there
        if dest_class not in self.relationship_track_list[source_class]:
            self.relationship_track_list[source_class].append(dest_class)

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
            if self.selected_class.relationship_list:
                type_list = [enum.value for enum in RelationshipType]
                source_class = self.selected_class.class_name_text.toPlainText()
                change_rel_type_dialog = Dialog("Change Relationship Type")
                change_rel_type_dialog.change_type_popup(source_class, self.relationship_track_list, type_list)
                
                # Execute the dialog and wait for user confirmation (OK or Cancel)
                if change_rel_type_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    
                    # Get the old and new field names after the dialog is accepted
                    dest_class = change_rel_type_dialog.input_widgets["destination_class_list_of_current_source_class"].currentText()  # Use `currentText()` 
                    type = change_rel_type_dialog.input_widgets["type"].currentText()  # Use `currentText()` 
                    is_type_changed = self.interface.change_type(source_class, dest_class, type)
                    if is_type_changed:
                        self.find_and_replace_relationship_type_helper(source_class, dest_class, type)
                    else:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"New relationship type is identical to current type {type}!")

    def find_and_replace_relationship_type_helper(self, source_class, dest_class, new_type):
        """
        Helper function to find and replace the relationship type between two UML classes.

        Parameters:
            source_class (str): The source class for the relationship.
            dest_class (str): The destination class for the relationship.
            new_type (str): The new relationship type.
        """
        # Iterate through the relationships to find the one that matches the source and destination
        for each_relationship in self.selected_class.relationship_list:
            if (each_relationship["source"].toPlainText() == source_class and 
                each_relationship["dest"].toPlainText() == dest_class):
                # Remove the old type and replace it with the new one
                self.scene().removeItem(each_relationship["type"])
                each_relationship["type"] = self.selected_class.create_text_item(new_type, selectable=False, color=self.selected_class.text_color)
                break
        self.selected_class.update_box()

    def find_and_remove_relationship_helper(self, source_class, dest_class):
        """
        Helper function to find and remove a relationship between two UML classes.

        This function removes the source, destination, and type text items from the scene and updates the UML class box.

        Parameters:
            source_class (str): The source class for the relationship.
            dest_class (str): The destination class for the relationship.
        """
        for each_relationship in self.selected_class.relationship_list:
            # Find the relationship that matches the source and destination classes
            if (each_relationship["source"].toPlainText() == source_class and 
                each_relationship["dest"].toPlainText() == dest_class):
                # Remove the text items for source, destination, and type from the scene
                self.scene().removeItem(each_relationship["source"])
                self.scene().removeItem(each_relationship["dest"])
                self.scene().removeItem(each_relationship["type"])
                # Also remove any associated labels
                self.scene().removeItem(each_relationship["source_label"])
                self.scene().removeItem(each_relationship["dest_label"])
                self.scene().removeItem(each_relationship["type_label"])
                # Remove the relationship from the list
                self.selected_class.relationship_list.remove(each_relationship)
                break
        self.relationship_track_list[source_class].remove(dest_class)
        # This is for checking the list in the terminal
        print(f"Current relationship tracking: {self.relationship_track_list}")
        self.selected_class.update_box()

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
        self.clear_current_scene()  # Clear the scene before loading a new file
        # Show an open file dialog and store the selected file path
        full_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", os.getcwd(), "JSON Files (*.json)")
        # Check if the user canceled the dialog (full_path will be empty if canceled)
        if not full_path:
            return  # Exit the function if the user cancels the dialog
        # Check if the selected file is a JSON file
        if not full_path.endswith('.json'):
            QtWidgets.QMessageBox.warning(None, "Warning", "The selected file is not a JSON file. Please select a valid JSON file.")
            return
        
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
            self.interface.save_gui(file_name_only, current_active_file_path)     
    
    def clear_current_scene(self):
        """
        Remove all UMLClassBox items from the scene.
        """
        # Iterate through all items in the scene
        for item in self.scene().items():
            # Check if the item is a UMLClassBox
            if isinstance(item, UMLClassBox):
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
            if self.selected_class.field_name_list:
                self.add_context_menu_action(contextMenu, "Delete Field", self.delete_field, enabled=True)
                self.add_context_menu_action(contextMenu, "Rename Field", self.rename_field, enabled=True)
            else:
                self.add_context_menu_action(contextMenu, "Delete Field", self.delete_field, enabled=False)
                self.add_context_menu_action(contextMenu, "Rename Field", self.rename_field, enabled=False)

            self.add_context_menu_separator(contextMenu)

            # METHOD OPTIONS
            self.add_context_menu_action(contextMenu, "Add Method", self.add_method, enabled=True)
            if self.selected_class.method_name_list:
                self.add_context_menu_action(contextMenu, "Delete Method", self.delete_method, enabled=True)
                self.add_context_menu_action(contextMenu, "Rename Method", self.rename_method, enabled=True)
                self.add_context_menu_separator(contextMenu)
                self.add_context_menu_action(contextMenu, "Add Parameter", self.add_param, enabled=True)
                # PARAMETER OPTIONS
                if self.selected_class.parameter_name_list:
                    self.add_context_menu_action(contextMenu, "Delete Parameter", self.delete_param, enabled=True)
                    self.add_context_menu_action(contextMenu, "Rename Parameter", self.rename_param, enabled=True)
                    self.add_context_menu_action(contextMenu, "Replace Parameter", self.replace_param, enabled=True)
                else:
                    self.add_context_menu_action(contextMenu, "Delete Parameter", self.delete_param, enabled=False)
                    self.add_context_menu_action(contextMenu, "Rename Parameter", self.rename_param, enabled=False)
                    self.add_context_menu_action(contextMenu, "Replace Parameter", self.replace_param, enabled=False)
            else:
                self.add_context_menu_action(contextMenu, "Delete Method", self.delete_method, enabled=False)
                self.add_context_menu_action(contextMenu, "Rename Method", self.rename_method, enabled=False)
                self.add_context_menu_separator(contextMenu)
                self.add_context_menu_action(contextMenu, "Add Parameter", self.add_param, enabled=False)
                self.add_context_menu_action(contextMenu, "Delete Parameter", self.delete_param, enabled=False)
                self.add_context_menu_action(contextMenu, "Rename Parameter", self.rename_param, enabled=False)
                self.add_context_menu_action(contextMenu, "Replace Parameter", self.replace_param, enabled=False)

            self.add_context_menu_separator(contextMenu)

            # RELATIONSHIP OPTIONS
            self.add_context_menu_action(contextMenu, "Add Relationship", self.add_relationship, enabled=True)
            if self.selected_class.relationship_list:
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
            self.class_name_list = []
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