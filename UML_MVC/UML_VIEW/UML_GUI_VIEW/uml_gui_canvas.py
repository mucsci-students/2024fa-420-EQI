###################################################################################################

import re
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_class_box import UMLClassBox
# from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_arrow_line import Arrow
from UML_ENUM_CLASS.uml_enum import RelationshipType

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
        
        # Initialize canvas properties
        self.is_dark_mode = False  # Flag for light/dark mode

        # Set initial view properties
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setSceneRect(-5000, -5000, 10000, 10000)  # Large scene size
        self.setScene(self.scene())

        # Panning state variables
        self.is_panning = False  # Flag to indicate if panning is active

        # Track selected class or arrow
        self.selected_class = None

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

        # Resize UMLClassBox items in the scene
        for item in self.scene().items():
            if isinstance(item, UMLClassBox):
                current_rect = item.rect()
                new_width = current_rect.width() * sx
                new_height = current_rect.height() * sy
                item.setRect(0, 0, new_width, new_height)
                item.update_box()

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
            else:
                QtWidgets.QMessageBox.warning(None, "Warning", f"Class name'{old_class_name}' does not exist!")
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")
    
    def change_name_in_relationship_after_rename_class(self, old_class_name, new_class_name):
        for item in self.scene().items():
            if isinstance(item, UMLClassBox):
                if item.relationship_list:
                    for each_relationship in item.relationship_list:
                        if each_relationship["source"].toPlainText() == old_class_name:
                            self.scene().removeItem(each_relationship["source"])
                            each_relationship["source"] = item.create_text_item(new_class_name, selectable=True, color=item.text_color)
                        if each_relationship["dest"].toPlainText() == old_class_name:
                            self.scene().removeItem(each_relationship["dest"])
                            each_relationship["dest"] = item.create_text_item(new_class_name, selectable=True, color=item.text_color)
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
                        field_text = selected_class_box.create_text_item(loaded_field_name, is_field=True, selectable=True, color=selected_class_box.text_color)
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
                        field_text = self.selected_class.create_text_item(field_name, is_field=True, selectable=True, color=self.selected_class.text_color)
                        self.selected_class.field_list[field_name] = field_text  # Add the field to the internal list
                        self.selected_class.field_name_list.append(field_name)  # Track the field name in the name list
                        self.selected_class.update_box()  # Update the box to reflect the changes
                    else:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Field name '{field_name}' has already existed!")
            else:
                QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")

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
            else:
                QtWidgets.QMessageBox.warning(None, "Warning", "No field selected!")
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")

    def rename_field(self):
        """
        Rename an existing field in the UML class.

        This function allows the user to select a field and provide a new name.
        The field's name is updated, and the UML class box is refreshed.

        Steps:
        1. Prompt the user to select a field to rename.
        2. Ask the user for a new name and update the field's name.
        3. If no class or field is selected, display a warning.
        """
        if self.selected_class:
            if self.selected_class.field_name_list:
                # Display a dialog to choose the field to rename
                old_field_name, ok = QtWidgets.QInputDialog.getItem(None, "Change Field Name", "Select field to change:", self.selected_class.field_name_list, 0, False)
                if ok and old_field_name:
                    # Ask for the new name for the selected field
                    new_field_name, ok = QtWidgets.QInputDialog.getText(None, "Rename Field", f"Enter new name for the field '{old_field_name}':")
                    if ok and new_field_name:
                        is_field_name_valid = self.interface.is_valid_input(new_name=new_field_name)
                        if not is_field_name_valid:
                            QtWidgets.QMessageBox.warning(None, "Warning", f"Field name {new_field_name} is invalid! Only allow a-zA-Z, number, and underscore!")
                            return
                        selected_class_name = self.selected_class.class_name_text.toPlainText()
                        is_field_renamed = self.interface.rename_field(selected_class_name, old_field_name, new_field_name)
                        if is_field_renamed:
                            # Update the field name in the list and refresh the display
                            if old_field_name in self.selected_class.field_list:
                                self.selected_class.field_list[new_field_name] = self.selected_class.field_list.pop(old_field_name)  # Rename the field in the internal list
                                self.selected_class.field_list[new_field_name].setPlainText(new_field_name)  # Set the new field name
                                self.selected_class.field_name_list[self.selected_class.field_name_list.index(old_field_name)] = new_field_name  # Update the name list
                                self.selected_class.update_box()  # Refresh the box display
                        else:
                            QtWidgets.QMessageBox.warning(None, "Warning", f"New field name '{new_field_name}' has already existed!")
            else:
                QtWidgets.QMessageBox.warning(None, "Warning", "No fields to change!")
        else:
            # Show a warning if there are no fields to rename
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")
            
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
                        method_text = selected_class_box.create_text_item(loaded_method_name + "()", is_method=True, selectable=True, color=selected_class_box.text_color)
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
                        method_text = self.selected_class.create_text_item(method_name + "()", is_method=True, selectable=True, color=self.selected_class.text_color)
                        self.selected_class.method_list[method_name] = method_text  # Store the method text
                        self.selected_class.method_name_list[method_name] = []  # Track the method's parameters
                        if len(self.selected_class.method_name_list) == 1:  # If this is the first method, create a separator
                            self.selected_class.create_separator(is_first=False)
                        self.selected_class.update_box()  # Update the UML box
                    else:
                        QtWidgets.QMessageBox.warning(None, "Warning", f"Method name '{method_name}' has already existed!")
            else:
                QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")
    
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
                        # Remove associated parameters and the method itself
                        for param_name in self.selected_class.method_name_list[method_name]:
                            self.scene().removeItem(self.selected_class.parameter_list.pop(param_name))  # Remove parameter
                        self.selected_class.method_name_list.pop(method_name)  # Remove from method list
                        self.scene().removeItem(self.selected_class.method_list.pop(method_name))  # Remove the method text
                        self.selected_class.update_box()  # Refresh the UML box
            else:
                # Show a warning if there are no methods to remove
                QtWidgets.QMessageBox.warning(None, "Warning", "No methods to remove!")
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")

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
                # Prompt the user to select the method to rename
                old_method_name, ok = QtWidgets.QInputDialog.getItem(None, "Change Method Name", "Select method to change:", self.selected_class.method_name_list, 0, False)
                if ok and old_method_name:
                    # Prompt for the new name
                    new_method_name, ok = QtWidgets.QInputDialog.getText(None, "Rename Method", f"Enter new name for the method '{old_method_name}':")
                    if ok and new_method_name:
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
                        else:
                            QtWidgets.QMessageBox.warning(None, "Warning", f"New method name '{new_method_name}' has already existed!")
            else:
                QtWidgets.QMessageBox.warning(None, "Warning", "No method to change name!")
        else:
            # Show a warning if there are no class selected
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")
            
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
                        param_text = selected_class_box.create_text_item(loaded_param_name , is_parameter=True, selectable=True, color=selected_class_box.text_color)
                        selected_class_box.method_name_list[loaded_method_name].append(loaded_param_name)  # Track the parameter
                        selected_class_box.parameter_list[loaded_param_name] = param_text  # Store the parameter text
                        selected_class_box.parameter_name_list.append(loaded_param_name)  # Add to the list of parameter names
                        selected_class_box.update_box()  # Update the UML box
        else:
            if self.selected_class:
                if self.selected_class.method_list:
                    # Ask the user to choose a method to add a parameter to
                    method_name, ok = QtWidgets.QInputDialog.getItem(None, "Choose Method Name", "Select method to add parameter:", list(self.selected_class.method_name_list.keys()), 0, False)
                    if ok and method_name:
                        # Ask for the parameter name
                        param_name, ok = QtWidgets.QInputDialog.getText(None, "Add Parameter", "Enter parameter name:")
                        if ok and param_name:
                            is_param_name_valid = self.interface.is_valid_input(parameter_name=param_name)
                            if not is_param_name_valid:
                                QtWidgets.QMessageBox.warning(None, "Warning", f"Parameter name {param_name} is invalid! Only allow a-zA-Z, number, and underscore!")
                                return
                            selected_class_name = self.selected_class.class_name_text.toPlainText()
                            is_param_added = self.interface.add_parameter(selected_class_name, method_name, param_name)
                            if is_param_added:
                                # Add the parameter to the selected method and update the UML box
                                param_text = self.selected_class.create_text_item(param_name , is_parameter=True, selectable=True, color=self.selected_class.text_color)
                                self.selected_class.method_name_list[method_name].append(param_name)  # Track the parameter
                                self.selected_class.parameter_list[param_name] = param_text  # Store the parameter text
                                self.selected_class.parameter_name_list.append(param_name)  # Add to the list of parameter names
                                self.selected_class.update_box()  # Update the UML box
                            else:
                                QtWidgets.QMessageBox.warning(None, "Warning", f"New parameter name '{param_name}' has already existed!")
                else:
                    # Show a warning if there are no methods available
                    QtWidgets.QMessageBox.warning(None, "Warning", "No methods to choose!")
            else:
                # Show a warning if there are no methods available
                QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")

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
                # Ask the user to choose a method to remove a parameter from
                method_name, ok = QtWidgets.QInputDialog.getItem(None, "Choose Method Name", "Select method to remove parameter:", 
                                                                 list(self.selected_class.method_name_list.keys()), 0, False)
                if ok and method_name:
                    # Check if the selected method has parameters
                    if self.selected_class.method_name_list[method_name]:
                        # Ask the user to choose the parameter to remove
                        param_name, ok = QtWidgets.QInputDialog.getItem(None, "Delete Parameter", "Choose parameter name to remove:", 
                                                                        self.selected_class.method_name_list[method_name], 0, False)
                        if ok and param_name:
                            selected_class_name = self.selected_class.class_name_text.toPlainText()
                            is_param_deleted = self.interface.delete_parameter(selected_class_name, method_name, param_name)
                            if is_param_deleted:
                                # Remove the parameter and update the UML box
                                self.selected_class.method_name_list[method_name].remove(param_name)  # Remove from method's parameter list
                                self.selected_class.parameter_name_list.remove(param_name)  # Remove from the global parameter list
                                self.scene().removeItem(self.selected_class.parameter_list.pop(param_name))  # Remove from the scene
                                self.selected_class.update_box()  # Refresh the UML box
                            else:
                                QtWidgets.QMessageBox.warning(None, "Warning", "No parameters to choose!")
                    else:
                        # Show a warning if there are no parameters to remove
                        QtWidgets.QMessageBox.warning(None, "Warning", "No parameters to choose!")
            else:
                # Show a warning if there are no methods available
                QtWidgets.QMessageBox.warning(None, "Warning", "No methods to choose!")
        else:
            # Show a warning if there are no class selected
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")
            
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
                # Ask the user to choose a method containing the parameter
                method_name, ok = QtWidgets.QInputDialog.getItem(None, "Choose Method Name", "Select method:", list(self.selected_class.method_name_list.keys()), 0, False)
                if ok and method_name:
                    # Check if the selected method has parameters
                    if self.selected_class.method_name_list[method_name]:
                        # Ask the user to choose the parameter to rename
                        old_param_name, ok = QtWidgets.QInputDialog.getItem(None, "Choose Parameter", "Choose parameter name to rename:", 
                                                                        self.selected_class.method_name_list[method_name], 0, False)
                        if ok and old_param_name:
                            # Ask for the new parameter name
                            new_param_name, ok = QtWidgets.QInputDialog.getText(None, "Rename Parameter", "Enter new parameter name:")
                            if ok and new_param_name:
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
                                    self.selected_class.parameter_list[new_param_name] = self.selected_class.parameter_list.pop(old_param_name)  # Update the parameter list
                                    self.selected_class.parameter_list[new_param_name].setPlainText(new_param_name)  # Set the new name in the UI
                                    self.selected_class.parameter_name_list[self.selected_class.parameter_name_list.index(old_param_name)] = new_param_name  # Track the change
                                    self.selected_class.update_box()  # Refresh the UML box
                                else:
                                    QtWidgets.QMessageBox.warning(None, "Warning", f"New param name '{new_param_name}' has already existed!")
                    else:
                        # Show a warning if there are no parameters to rename
                        QtWidgets.QMessageBox.warning(None, "Warning", "No parameters to choose.")
            else:
                # Show a warning if there are no methods available
                QtWidgets.QMessageBox.warning(None, "Warning", "No methods to choose.")
        else:
            # Show a warning if there are no class selected
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")

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
                # Select the method to replace parameters for
                method_name, ok = QtWidgets.QInputDialog.getItem(None, "Choose Method Name", 
                                                             "Select method to replace parameters:", 
                                                             list(self.selected_class.method_name_list.keys()), 0, False)
                if ok and method_name:
                    # Prompt user to enter the new parameters as a comma-separated string
                    param_string, ok = QtWidgets.QInputDialog.getText(None, "Replace Parameters", 
                                                                  "Enter new parameters (comma-separated):")
                    if ok and param_string:
                        # Split the input string by commas to form a list of parameters
                        new_param_list = [param.strip() for param in param_string.split(",") if param.strip()]
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
                                # Clear current parameters
                                for param_name in self.selected_class.method_name_list[method_name]:
                                    self.scene().removeItem(self.selected_class.parameter_list.pop(param_name))
                                # Clear the method's parameter list
                                self.selected_class.method_name_list[method_name].clear()
                                # Add new parameters to the method
                                for new_param in new_param_list:
                                    param_text = self.selected_class.create_text_item(new_param, is_parameter=True, selectable=True, color=self.selected_class.text_color)
                                    self.selected_class.method_name_list[method_name].append(new_param)
                                    self.selected_class.parameter_list[new_param] = param_text
                                    self.selected_class.parameter_name_list.append(new_param)
                                # Update the box to reflect changes
                                self.selected_class.update_box()
            else:
                # Display a warning if no methods are available
                QtWidgets.QMessageBox.warning(None, "Warning", "No methods available to replace parameters.")
        else:
            # Show a warning if there are no class selected
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")
            
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
                        # Append the source and destination class names to their respective lists
                        selected_class_box.source_class_list.append(loaded_source_class)
                        selected_class_box.dest_class_list.append(loaded_dest_class)
                        # Create text items for the source, destination, and type
                        source_text = selected_class_box.create_text_item(loaded_source_class, selectable=True, color=selected_class_box.text_color)
                        dest_text = selected_class_box.create_text_item(loaded_dest_class, selectable=True, color=selected_class_box.text_color)
                        type_text = selected_class_box.create_text_item(loaded_type, selectable=True, color=selected_class_box.text_color)
                        # Append the relationship data to the class's relationship list
                        selected_class_box.relationship_list.append({"source": source_text, "dest": dest_text, "type": type_text})
                        if len(selected_class_box.relationship_list) == 1:
                            # If this is the first relationship, create a separator
                            selected_class_box.create_separator(is_first=False, is_second=False)
                        # Update the class box
                        selected_class_box.update_box()
        else:
            if self.selected_class:
                # Prompt the user to select a source class
                source_class, ok = QtWidgets.QInputDialog.getItem(None, "Choose Source Class", "Select source class:", self.class_name_list, 0, False)
                if ok and source_class:
                    # Ensure the source class is the same as the current class's name
                    if source_class != self.selected_class.class_name_text.toPlainText():
                        QtWidgets.QMessageBox.warning(None, "Warning", "Source class must be the same as class name!")
                        return
                    # Prompt the user to select a destination class
                    dest_class, ok = QtWidgets.QInputDialog.getItem(None, "Choose Destination Class", "Select destination class:", self.class_name_list, 0, False)
                    if ok and dest_class:
                        # Prompt the user to select the relationship type
                        enum_items = [enum.value for enum in RelationshipType]
                        relationship_type, ok = QtWidgets.QInputDialog.getItem(None, "Choose Relationship Type", "Select type:", enum_items, 0, False)
                        if ok and relationship_type:
                            # Add the relationship via the interface
                            is_rel_added = self.interface.add_relationship_gui(source_class_name=source_class, destination_class_name=dest_class, type=relationship_type)
                            if is_rel_added:
                                # Append the source and destination class names to their respective lists
                                self.selected_class.source_class_list.append(source_class)
                                self.selected_class.dest_class_list.append(dest_class)
                                # Create text items for the source, destination, and type
                                source_text = self.selected_class.create_text_item(source_class, selectable=True, color=self.selected_class.text_color)
                                dest_text = self.selected_class.create_text_item(dest_class, selectable=True, color=self.selected_class.text_color)
                                type_text = self.selected_class.create_text_item(relationship_type, selectable=True, color=self.selected_class.text_color)
                                # Append the relationship data to the class's relationship list
                                self.selected_class.relationship_list.append({"source": source_text, "dest": dest_text, "type": type_text})
                                if len(self.selected_class.relationship_list) == 1:
                                    # If this is the first relationship, create a separator
                                    self.selected_class.create_separator(is_first=False, is_second=False)
                                # Update the class box
                                self.selected_class.update_box()
                            else:
                                QtWidgets.QMessageBox.warning(None, "Warning", "Relationship has already existed!")
            else:
                # Show a warning if no class is selected
                QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")

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
                # Prompt the user to select a source class for the relationship to be deleted
                source_class, ok = QtWidgets.QInputDialog.getItem(None, "Choose Source Class To Delete", "Select source class:", self.class_name_list, 0, False)
                if ok and source_class:
                    # Ensure the source class matches the current class name
                    if source_class != self.selected_class.class_name_text.toPlainText():
                        QtWidgets.QMessageBox.warning(None, "Warning", "Source class must be the same as class name!")
                        return
                    # Prompt the user to select a destination class
                    dest_class, ok = QtWidgets.QInputDialog.getItem(None, "Choose Destination Class To Delete", "Select destination class:", self.class_name_list, 0, False)
                    if ok and dest_class:
                        # Check if the relationship exists
                        is_rel_exist = self.interface.relationship_exist(source_class, dest_class)
                        if not is_rel_exist:
                            QtWidgets.QMessageBox.warning(None, "Warning", f"There is no relationship between '{source_class}' class and '{dest_class}' class!")
                            return
                        # Delete the relationship if found
                        is_rel_deleted = self.interface.delete_relationship(source_class, dest_class)
                        if is_rel_deleted:
                            self.find_and_remove_relationship_helper(source_class, dest_class)
            else:
                QtWidgets.QMessageBox.warning(None, "Warning", "No relationship exists!")
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")

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
                # Prompt the user to select a source class
                source_class, ok = QtWidgets.QInputDialog.getItem(None, "Choose Source Class To Change Type", "Select source class:", self.class_name_list, 0, False)
                if ok and source_class:
                    if source_class != self.selected_class.class_name_text.toPlainText():
                        QtWidgets.QMessageBox.warning(None, "Warning", "Source class must be the same as class name!")
                        return
                    # Prompt the user to select a destination class
                    dest_class, ok = QtWidgets.QInputDialog.getItem(None, "Choose Destination Class To Change Type", "Select destination class:", self.class_name_list, 0, False)
                    if ok and dest_class:
                        is_rel_exist = self.interface.relationship_exist(source_class, dest_class)
                        if not is_rel_exist:
                            QtWidgets.QMessageBox.warning(None, "Warning", f"There is no relationship between '{source_class}' class and '{dest_class}' class!")
                            return
                        # Prompt the user to select a new relationship type
                        enum_items = [enum.value for enum in RelationshipType]
                        relationship_type, ok = QtWidgets.QInputDialog.getItem(None, "Choose New Relationship Type", "Select type:", enum_items, 0, False)
                        if ok and relationship_type:
                            is_type_changed = self.interface.change_type(source_class, dest_class, relationship_type)
                            if is_type_changed:
                                self.find_and_replace_relationship_type_helper(source_class, dest_class, relationship_type)
                            else:
                                QtWidgets.QMessageBox.warning(None, "Warning", f"New relationship type is identical to current type {relationship_type}!")
            else:
                QtWidgets.QMessageBox.warning(None, "Warning", "No relationship exists!")
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")

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
                each_relationship["type"] = self.selected_class.create_text_item(new_type, selectable=True, color=self.selected_class.text_color)
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
        
        # Remove the source and destination class names from their respective lists
        self.selected_class.source_class_list.remove(source_class)
        self.selected_class.dest_class_list.remove(dest_class)
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
    ## MOUSE RELATED ##

    def contextMenuEvent(self, event):
        """
        Show the context menu when right-clicking on the UMLClassBox or the background. 
        
        The context menu provides various options to modify the selected UML class or perform global actions 
        such as saving and loading UML diagrams.
        
        Parameters:
        - event (QContextMenuEvent): The event that triggers the context menu, typically a right-click on the scene.
        """
        
        # Create the context menu object
        contextMenu = QtWidgets.QMenu()

        # Check if a class is selected
        if self.selected_class:
            """
            If a UML class is selected, show the following options for modifying the class's appearance, 
            fields, methods, and parameters.
            """

            #################################
            # CLASS MANAGEMENT OPTIONS ##
            
            # Add an option to rename the selected class
            rename_class_button = contextMenu.addAction("Rename Class")
            # Connect the rename class action to the rename_class method
            rename_class_button.triggered.connect(self.rename_class)
            
            # Add a separator to separate class management options from field options
            contextMenu.addSeparator()

            #################################
            ## FIELD OPTIONS ##
            
            # Add options to manage fields within the selected class
            add_field_button = contextMenu.addAction("Add Field")  # Add a field
            delete_field_button = contextMenu.addAction("Delete Field")  # Delete a field
            rename_field_button = contextMenu.addAction("Rename Field")  # Rename a field

            # Connect field actions to their respective methods
            add_field_button.triggered.connect(self.add_field)
            delete_field_button.triggered.connect(self.delete_field)
            rename_field_button.triggered.connect(self.rename_field)

            # Add a separator to separate field options from method options
            contextMenu.addSeparator()

            #################################
            # METHOD OPTIONS ##
            
            # Add options to manage methods within the selected class
            add_method_button = contextMenu.addAction("Add Method")  # Add a method
            delete_method_button = contextMenu.addAction("Delete Method")  # Delete a method
            rename_method_button = contextMenu.addAction("Rename Method")  # Rename a method

            # Connect method actions to their respective methods
            add_method_button.triggered.connect(self.add_method)
            delete_method_button.triggered.connect(self.delete_method)
            rename_method_button.triggered.connect(self.rename_method)

            # Add a separator to separate method options from parameter options
            contextMenu.addSeparator()

            #################################
            # PARAMETER OPTIONS ##
            
            # Add options to manage parameters within the selected class
            add_parameter_button = contextMenu.addAction("Add Parameter")  # Add a parameter
            delete_parameter_button = contextMenu.addAction("Delete Parameter")  # Delete a parameter
            rename_parameter_button = contextMenu.addAction("Rename Parameter")  # Rename a parameter
            replace_parameter_button = contextMenu.addAction("Replace Parameter")  # Replace a parameter

            # Connect parameter actions to their respective methods
            add_parameter_button.triggered.connect(self.add_param)
            delete_parameter_button.triggered.connect(self.delete_param)
            rename_parameter_button.triggered.connect(self.rename_param)
            replace_parameter_button.triggered.connect(self.replace_param)

            # Add a separator to separate method options from relationship options
            contextMenu.addSeparator()
            
            #################################
            # PARAMETER OPTIONS ##
            
            # Add options to manage relationship within the selected class
            add_rel_button = contextMenu.addAction("Add Relationship")  # Add relationship
            delete_rel_button = contextMenu.addAction("Delete Relationship")  # Delete relationship
            change_type_button = contextMenu.addAction("Change Type")  # Change relationship type
            
            # Connect relationship actions to their respective methods
            add_rel_button.triggered.connect(self.add_relationship)
            delete_rel_button.triggered.connect(self.delete_relationship)
            change_type_button.triggered.connect(self.change_relationship_type)
            
            # Execute the context menu at the global position (where the right-click happened)
            contextMenu.exec_(event.globalPos())

            # After executing an action, update the class box to reflect changes
            self.selected_class.update_box()

        else:
            """
            If no UML class is selected, display options for adding a class, selecting all classes, 
            or managing files (open, save, etc.).
            """

            #################################
            # CLASS OPTIONS
            # Add an option to create a new UML class
            add_class_action = contextMenu.addAction("Add Class")
            # Connect the add_class action to the add_class method
            add_class_action.triggered.connect(self.add_class)

            # Add an option to select all UML classes in the scene
            select_all_class_action = contextMenu.addAction("Select All Class")
            # Connect the action to a method that selects all items in the grid
            select_all_class_action.triggered.connect(self.select_items_in_rect)

            # Add a separator before file management options
            contextMenu.addSeparator()

            #################################
            # Execute the context menu at the global position (where the right-click happened)
            contextMenu.exec_(event.globalPos())
            
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
            self.viewport().update()
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