import os
from PyQt5 import QtWidgets, QtGui, QtCore
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_class_box import UMLClassBox
from UML_ENUM_CLASS.uml_enum import RelationshipType
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_custom_dialog import CustomInputDialog as Dialog
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_arrow_line import UMLArrow as ArrowLine
from UML_MVC.uml_command_factory import CommandFactory

class UMLGraphicsView(QtWidgets.QGraphicsView):
    """
    A custom graphics view for displaying and interacting with UML diagrams.

    Inherits from QGraphicsView to provide advanced interactions such as adding/removing classes,
    fields, methods, and relationships in a UML diagram. It handles user interactions, rendering,
    and the internal state of UML elements.
    """

    #################################################################
    ### CONSTRUCTOR ###

    def __init__(self, interface, parent=None):
        """
        Initializes a new UMLGraphicsView instance.

        Parameters:
            interface (InterfaceType): Interface to communicate with the UMLCoreManager for UML data processing.
            parent (QWidget, optional): The parent widget that holds this view, typically the main window or canvas.
        """
        super().__init__(QtWidgets.QGraphicsScene(parent), parent)

        self.interface = interface  # Interface to communicate with UMLCoreManager
        self.model = self.interface.Controller._get_model_obj()

        self.command_factory = CommandFactory(uml_model=self.model, view=self, is_gui=True)

        self.input_handler = self.interface.Controller._get_input_handler()

        self.class_name_list = {}  # Maps class names to their respective UMLClassBox objects

        self.relationship_track_list: dict[str, list[tuple]] = {}  # Stores relationships between classes

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

        self.move_start_pos = None  # Starting position for move actions

    #################################################################
    ## GRID VIEW RELATED ##

    def scale(self, sx, sy):
        """
        Overrides the scale method to resize class boxes when zooming.

        Parameters:
            sx (float): Scaling factor in the x-direction (horizontal zoom).
            sy (float): Scaling factor in the y-direction (vertical zoom).
        """
        super().scale(sx, sy)

    def drawBackground(self, painter, rect):
        """
        Draws the background grid pattern.

        Parameters:
            painter (QPainter): The painter object used to draw onto the scene.
            rect (QRectF): The rectangle area to be painted.
        """
        # Fill background based on mode (dark or light)
        if self.is_dark_mode:
            painter.fillRect(rect, QtGui.QColor(30, 30, 30))  # Dark mode background
        else:
            painter.fillRect(rect, QtGui.QColor(255, 255, 255))  # Light mode background

    #################################################################
    ## CLASS OPERATION ##

    def add_class(self, loaded_class_name=None, x=None, y=None, is_loading=False):
        """
        Adds a UML class box to the scene.

        This method allows the user to add a new class box to the canvas either interactively or by loading data
        from a saved file. It also validates the class name before adding it.

        Parameters:
            loaded_class_name (str, optional): The class name to load during the loading process.
            x (int, optional): The x-coordinate for placing the class box.
            y (int, optional): The y-coordinate for placing the class box.
            is_loading (bool): Flag indicating whether the operation is a load process or user-driven interaction.
        """
        if is_loading:
            is_class_added = self.interface.add_class(loaded_class_name)
            if not is_class_added:
                return
            # Create the UMLClassBox with loaded class name and position
            class_box = UMLClassBox(self.interface, class_name=loaded_class_name, x=x, y=y)
            class_box.set_box_position()  # Position the box on the scene
            self.class_name_list[loaded_class_name] = class_box
            self.scene().addItem(class_box)
        else:
            # Prompt user for class name if not loading
            input_class_name, ok = QtWidgets.QInputDialog.getText(None, "Add Class", "Enter class name:")
            if not ok or not input_class_name:
                return

            # Validate class name
            is_class_name_valid = self.interface.is_valid_input(class_name=input_class_name)
            if not is_class_name_valid:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Warning",
                    f"Class name '{input_class_name}' is invalid! Only letters, numbers, and underscores allowed."
                )
                return
            class_box = UMLClassBox(self.interface, class_name=input_class_name)
            self.command_factory.class_box = class_box
            add_class_command = self.command_factory.create_command(
                command_name="add_class", class_name=input_class_name
            )
            is_class_added = self.input_handler.execute_command(add_class_command)

            if not is_class_added:
                QtWidgets.QMessageBox.warning(
                    None, "Warning", f"Class '{input_class_name}' already exists!"
                )

    def delete_class(self):
        """
        Deletes the selected class or arrow from the scene.

        This function deletes the currently selected class or arrow (if any) from the UML diagram.
        It uses the command pattern for undo/redo functionality, allowing the action to be undone.

        If no class or arrow is selected, it shows a warning to the user.
        """
        if self.selected_class:
            # Get the class name from the selected class and issue the delete command
            input_class_name = self.selected_class.class_name_text.toPlainText()
            self.command_factory.class_box = self.selected_class
            delete_class_command = self.command_factory.create_command(
                command_name="delete_class", class_name=input_class_name
            )
            is_class_deleted = self.input_handler.execute_command(delete_class_command)
            if not is_class_deleted:
                QtWidgets.QMessageBox.warning(
                    None, "Warning", f"Class '{input_class_name}' does not exist!"
                )
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "No class selected!")

    def rename_class(self):
        """
        Renames the class displayed in the UML box.

        This method prompts the user for a new class name, validates it, and updates the class name in the UML box.
        If the class name is invalid or already exists, a warning is shown to the user.
        """
        if not self.selected_class:
            return
        old_class_name = self.selected_class.class_name_text.toPlainText()
        new_class_name, ok = QtWidgets.QInputDialog.getText(
            None, "Rename Class", f"Enter new name for class '{old_class_name}'"
        )
        if not ok or not new_class_name:
            return
        is_class_name_valid = self.interface.is_valid_input(new_name=new_class_name)
        if not is_class_name_valid:
            QtWidgets.QMessageBox.warning(
                None,
                "Warning",
                f"Class name '{new_class_name}' is invalid! Only letters, numbers, and underscores allowed.",
            )
            return

        self.command_factory.class_box = self.selected_class
        rename_class_command = self.command_factory.create_command(
            command_name="rename_class", class_name=old_class_name, new_name=new_class_name
        )

        is_class_renamed = self.input_handler.execute_command(rename_class_command)
        if is_class_renamed:
            self.class_name_list[new_class_name] = self.class_name_list.pop(old_class_name)
            self.selected_class.update_box()  # Refresh the class box to reflect the new name
        else:
            QtWidgets.QMessageBox.warning(
                None, "Warning", f"Class name '{new_class_name}' already exists!"
            )

    def add_field(self, loaded_class_name=None, loaded_field_type=None, loaded_field_name=None, is_loading=False):
        """
        Adds a field to a UML class box, either during loading or interactively.

        This function either loads a field into the UML class during the loading process or allows the user
        to add a new field through a dialog box. It updates the UML class box and its internal lists.

        Parameters:
            loaded_class_name (str, optional): The name of the class to which the field is added (used during loading).
            loaded_field_type (str, optional): The type of the field being added (used during loading).
            loaded_field_name (str, optional): The name of the field being added (used during loading).
            is_loading (bool): Whether the function is being called during the loading process.
        """
        if is_loading:
            # Find the UML class box by the loaded class name in the scene
            for item in self.scene().items():
                if (
                    isinstance(item, UMLClassBox)
                    and item.class_name_text.toPlainText() == loaded_class_name
                ):
                    selected_class_box = item  # Found the class box
                    # Add the field to the found class box
                    is_field_added = self.interface.add_field(
                        loaded_class_name, loaded_field_type, loaded_field_name
                    )
                    if not is_field_added:
                        continue
                    # Create a text item for the field and add it to the list of the found class box
                    field_text = selected_class_box.create_text_item(
                        loaded_field_type + " " + loaded_field_name,
                        is_field=True,
                        selectable=False,
                        color=selected_class_box.text_color,
                    )
                    field_key = (loaded_field_type, loaded_field_name)
                    selected_class_box.field_list[field_key] = field_text  # Add the field to the internal list
                    selected_class_box.field_key_list.append(
                        field_key
                    )  # Track the field name in the name list
                    selected_class_box.update_box()  # Update the box to reflect the changes
        else:
            if not self.selected_class:
                return
            add_field_dialog = Dialog("Add Field")
            add_field_dialog.add_field_popup()

            # Execute the dialog and wait for user confirmation (OK or Cancel)
            if add_field_dialog.exec_() != QtWidgets.QDialog.Accepted:
                return

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
                QtWidgets.QMessageBox.warning(
                    None,
                    "Warning",
                    f"Field type {field_type} is invalid! Only letters, numbers, and underscores allowed!",
                )
                return
            is_field_name_valid = self.interface.is_valid_input(field_name=field_name)
            if not is_field_name_valid:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Warning",
                    f"Field name {field_name} is invalid! Only letters, numbers, and underscores allowed!",
                )
                return

            self.command_factory.class_box = self.selected_class
            add_field_command = self.command_factory.create_command(
                command_name="add_field",
                class_name=selected_class_name,
                field_type=field_type,
                input_name=field_name,
            )

            is_field_added = self.input_handler.execute_command(add_field_command)

            if not is_field_added:
                QtWidgets.QMessageBox.warning(
                    None, "Warning", f"Field name '{field_name}' has already existed!"
                )

    def delete_field(self):
        """
        Removes an existing field from the UML class.

        This function allows the user to select a field from the selected class and remove it.
        It updates the internal lists and the graphical display.
        """
        if not self.selected_class:
            return
        if not self.selected_class.field_key_list:
            return
        # Display a dialog asking the user to select a field to remove
        field_name_list = [field_key[1] for field_key in self.selected_class.field_key_list]
        field_name, ok = QtWidgets.QInputDialog.getItem(
            None, "Remove Field", "Select field to remove:", field_name_list, 0, False
        )
        # If the user confirms, remove the selected field from the class
        if not ok and not field_name:
            return
        selected_class_name = self.selected_class.class_name_text.toPlainText()

        self.command_factory.class_box = self.selected_class
        delete_field_command = self.command_factory.create_command(
            command_name="delete_field", class_name=selected_class_name, input_name=field_name
        )

        self.input_handler.execute_command(delete_field_command)

    def rename_field(self):
        """
        Renames an existing field in the selected UML class.

        This method allows the user to choose a field and provide a new name for it. It updates
        the UML class box and validates the new field name to ensure it doesn't already exist
        and adheres to naming conventions.
        """
        if not self.selected_class:
            return
        if not self.selected_class.field_key_list:
            return
        # Initialize the dialog
        rename_field_dialog = Dialog("Rename Field")
        rename_field_dialog.rename_field_popup(self.selected_class)

        # Execute the dialog and wait for user confirmation (OK or Cancel)
        if rename_field_dialog.exec_() != QtWidgets.QDialog.Accepted:
            return

        # Get the old and new field names after the dialog is accepted
        selected_class_name = self.selected_class.class_name_text.toPlainText()
        old_field_name = rename_field_dialog.input_widgets[
            'old_field_name'
        ].currentText()  # Use `currentText()` for QComboBox
        new_field_name = rename_field_dialog.input_widgets[
            'new_field_name'
        ].text()  # Use `text()` for QLineEdit

        if not new_field_name.strip():
            return

        # Check if the new field name already exists
        if new_field_name in self.selected_class.field_key_list:
            QtWidgets.QMessageBox.warning(
                None, "Warning", f"Field name '{new_field_name}' has already existed!"
            )
            return

        # Validate the new field name
        is_field_name_valid = self.interface.is_valid_input(new_name=new_field_name)
        if not is_field_name_valid:
            QtWidgets.QMessageBox.warning(
                None,
                "Warning",
                f"Field name {new_field_name} is invalid! Only letters, numbers, and underscores allowed!",
            )
            return

        self.command_factory.class_box = self.selected_class
        rename_field_command = self.command_factory.create_command(
            command_name="rename_field",
            class_name=selected_class_name,
            old_name=old_field_name,
            new_name=new_field_name,
        )

        self.input_handler.execute_command(rename_field_command)

    def edit_field_type(self):
        """
        Edits the type of an existing field in the selected UML class.

        This method allows the user to select a field and change its data type. It validates
        the new type and updates the UML class box accordingly.
        """
        if not self.selected_class:
            return
        if not self.selected_class.field_key_list:
            return
        # Initialize the dialog
        edit_field_type_dialog = Dialog("Edit Field Type")
        edit_field_type_dialog.edit_field_type_popup(self.selected_class)

        # Execute the dialog and wait for user confirmation (OK or Cancel)
        if edit_field_type_dialog.exec_() != QtWidgets.QDialog.Accepted:
            return

        # Get the field name and new type after the dialog is accepted
        selected_class_name = self.selected_class.class_name_text.toPlainText()
        field_name = edit_field_type_dialog.input_widgets[
            'field_name'
        ].currentText()  # Use `currentText()` for QComboBox
        new_field_type = edit_field_type_dialog.input_widgets[
            'new_field_type'
        ].text()  # Use `text()` for QLineEdit

        self.command_factory.class_box = self.selected_class
        edit_field_type_command = self.command_factory.create_command(
            command_name="edit_field_type",
            class_name=selected_class_name,
            input_name=field_name,
            new_type=new_field_type,
        )

        self.input_handler.execute_command(edit_field_type_command)

    def add_method(self, loaded_class_name=None, loaded_return_type=None, loaded_method_name=None, is_loading=False):
        """
        Adds a method to a UML class box, either during loading or interactively.

        This function either loads a method into the UML class during the loading process or allows the user
        to add a new method through a dialog box. It updates the UML class box and its internal lists.

        Parameters:
            loaded_class_name (str, optional): The name of the class to which the method is added (used during loading).
            loaded_return_type (str, optional): The return type of the method being added (used during loading).
            loaded_method_name (str, optional): The name of the method being added (used during loading).
            is_loading (bool): Whether the function is being called during the loading process.
        """
        if is_loading:
            # Find the UML class box by the loaded class name in the scene
            for item in self.scene().items():
                if (
                    isinstance(item, UMLClassBox)
                    and item.class_name_text.toPlainText() == loaded_class_name
                ):
                    selected_class_box = item  # Found the class box
                    # Add the method to the found class box
                    is_method_added = self.interface.add_method(
                        loaded_class_name, loaded_return_type, loaded_method_name
                    )
                    if not is_method_added:
                        continue
                    # Create a text item for the method and add it to the list of the found class box
                    method_text = selected_class_box.create_text_item(
                        loaded_return_type + " " + loaded_method_name + "()",
                        is_method=True,
                        selectable=False,
                        color=selected_class_box.text_color,
                    )
                    method_key = (loaded_return_type, loaded_method_name)
                    method_entry = {
                        "method_key": method_key,
                        "method_text": method_text,
                        "parameters": [],
                    }
                    selected_class_box.method_list.append(
                        method_entry
                    )  # Add the method to the internal list
                    if len(selected_class_box.method_list) == 1:
                        # If this is the first method, create a separator
                        selected_class_box.create_separator(is_first=False)
                    selected_class_box.update_box()  # Update the box to reflect the changes
        else:
            if not self.selected_class:
                return
            add_method_dialog = Dialog("Add Method")
            add_method_dialog.add_method_popup()

            # Execute the dialog and wait for user confirmation (OK or Cancel)
            if add_method_dialog.exec_() != QtWidgets.QDialog.Accepted:
                return

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
                QtWidgets.QMessageBox.warning(
                    None,
                    "Warning",
                    f"Method type {method_type} is invalid! Only letters, numbers, and underscores allowed!",
                )
                return
            is_method_name_valid = self.interface.is_valid_input(method_name=method_name)
            if not is_method_name_valid:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Warning",
                    f"Method name {method_name} is invalid! Only letters, numbers, and underscores allowed!",
                )
                return

            selected_class_name = self.selected_class.class_name_text.toPlainText()

            self.command_factory.class_box = self.selected_class
            add_method_command = self.command_factory.create_command(
                command_name="add_method",
                class_name=selected_class_name,
                input_name=method_name,
                method_type=method_type,
            )

            is_method_added = self.input_handler.execute_command(add_method_command)

            if not is_method_added:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Warning",
                    f"Method name '{method_name}' has the same parameter list signature as an existing method in class!",
                )

    def delete_method(self):
        """
        Removes an existing method from the selected UML class.

        This function allows the user to select a method from the currently selected class
        and delete it along with all associated parameters. It updates the UML class box
        and its internal lists accordingly.
        """
        if not self.selected_class:
            return
        if not self.selected_class.method_list:
            return
        delete_method_dialog = Dialog("Delete Method")
        delete_method_dialog.delete_method_popup(self.selected_class)

        # Execute the dialog and wait for user confirmation (OK or Cancel)
        if delete_method_dialog.exec_() != QtWidgets.QDialog.Accepted:
            return

        selected_class_name = self.selected_class.class_name_text.toPlainText()

        # Extract the selected index from the display list
        raw_method_name = delete_method_dialog.input_widgets["raw_method_name"].currentText()
        selected_index = int(raw_method_name.split(":")[0].strip()) - 1
        selected_class_name = self.selected_class.class_name_text.toPlainText()

        # Execute the delete command with the correct method index
        self.command_factory.class_box = self.selected_class
        delete_method_command = self.command_factory.create_command(
            command_name="delete_method",
            class_name=selected_class_name,
            method_num=str(selected_index + 1),
        )

        self.input_handler.execute_command(delete_method_command)

    def rename_method(self):
        """
        Renames an existing method in the selected UML class.

        This function allows the user to select a method and provide a new name for it.
        The method name is updated, and the UML class box is refreshed.
        """
        if not self.selected_class:
            return
        if not self.selected_class.method_list:
            return
        # Initialize the dialog
        rename_method_dialog = Dialog("Rename Method")
        rename_method_dialog.rename_method_popup(self.selected_class)

        # Execute the dialog and wait for user confirmation (OK or Cancel)
        if rename_method_dialog.exec_() != QtWidgets.QDialog.Accepted:
            return

        # Get new method name after the dialog is accepted
        new_method_name = rename_method_dialog.input_widgets[
            "new_method_name"
        ].text()  # Use `text()` for QLineEdit
        if not new_method_name.strip():
            return
        old_method_name_widget = rename_method_dialog.input_widgets["raw_method_name"]
        selected_index = old_method_name_widget.currentIndex()
        method_keys_list = rename_method_dialog.input_widgets["method_keys_list"]

        # Check if the new method name already exists
        for each_key in method_keys_list:
            if each_key[1] != new_method_name:
                continue
            QtWidgets.QMessageBox.warning(
                None, "Warning", f"Method name '{new_method_name}' has already existed!"
            )
            return

        is_method_name_valid = self.interface.is_valid_input(new_name=new_method_name)
        if not is_method_name_valid:
            QtWidgets.QMessageBox.warning(
                None,
                "Warning",
                f"Method name {new_method_name} is invalid! Only letters, numbers, and underscores allowed!",
            )
            return

        selected_class_name = self.selected_class.class_name_text.toPlainText()

        self.command_factory.class_box = self.selected_class
        rename_method_command = self.command_factory.create_command(
            command_name="rename_method",
            class_name=selected_class_name,
            method_num=str(selected_index + 1),
            new_name=new_method_name,
        )

        self.input_handler.execute_command(rename_method_command)

    def edit_method_return_type(self):
        """
        Edits the return type of an existing method in the selected UML class.

        This method allows the user to select a method and change its return type. It validates
        the new type and updates the UML class box accordingly.
        """
        if not self.selected_class:
            return
        if not self.selected_class.method_list:
            return
        # Initialize the dialog
        edit_method_return_type_dialog = Dialog("Edit Method Return Type")
        edit_method_return_type_dialog.edit_method_return_type_popup(self.selected_class)

        # Execute the dialog and wait for user confirmation (OK or Cancel)
        if edit_method_return_type_dialog.exec_() != QtWidgets.QDialog.Accepted:
            return

        # Get the method number and new return type after the dialog is accepted
        selected_class_name = self.selected_class.class_name_text.toPlainText()
        method_num = edit_method_return_type_dialog.input_widgets['method_name'].currentIndex()
        new_method_return_type = edit_method_return_type_dialog.input_widgets[
            'new_method_return_type'
        ].text()

        self.command_factory.class_box = self.selected_class
        edit_method_return_type_command = self.command_factory.create_command(
            command_name="edit_method_type",
            class_name=selected_class_name,
            method_num=str(method_num + 1),
            new_type=new_method_return_type,
        )

        self.input_handler.execute_command(edit_method_return_type_command)

    def add_param(self, loaded_class_name=None, loaded_method_num=None, loaded_param_type=None, loaded_param_name=None, is_loading=False):
        """
        Adds a parameter to a method in the UML class, either during loading or interactively.

        This function either loads a parameter into a method during the loading process
        or allows the user to add a new parameter interactively through a dialog.

        Parameters:
            loaded_class_name (str, optional): The class name where the parameter is being added.
            loaded_method_num (int, optional): The method number where the parameter is being added.
            loaded_param_type (str, optional): The type of the parameter being added.
            loaded_param_name (str, optional): The name of the parameter being added.
            is_loading (bool): Whether the function is being called during the loading process.
        """
        if is_loading:
            # Find the UML class box by the loaded class name in the scene
            for item in self.scene().items():
                if (
                    isinstance(item, UMLClassBox)
                    and item.class_name_text.toPlainText() == loaded_class_name
                ):
                    selected_class_box = item  # Found the class box
                    is_param_added = self.interface.add_parameter(
                        loaded_class_name, str(loaded_method_num), loaded_param_type, loaded_param_name
                    )
                    if not is_param_added:
                        continue
                    # Append the parameter to the method's parameter list
                    param_tuple = (loaded_param_type, loaded_param_name)
                    method_entry = selected_class_box.method_list[int(loaded_method_num) - 1]
                    method_entry["parameters"].append(param_tuple)
                    selected_class_box.param_num = len(method_entry["parameters"])
                    selected_class_box.update_box()  # Update the UML box
        else:
            if not self.selected_class:
                return
            if not self.selected_class.method_list:
                return
            # Initialize the dialog
            add_param_dialog = Dialog("Add Parameter")
            add_param_dialog.add_param_popup(self.selected_class)

            # Execute the dialog and wait for user confirmation (OK or Cancel)
            if add_param_dialog.exec_() != QtWidgets.QDialog.Accepted:
                return
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
                QtWidgets.QMessageBox.warning(
                    None,
                    "Warning",
                    f"Parameter type '{param_type}' is invalid! Only letters, numbers, and underscores are allowed!",
                )
                return

            is_param_name_valid = self.interface.is_valid_input(parameter_name=param_name)
            if not is_param_name_valid:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Warning",
                    f"Parameter name '{param_name}' is invalid! Only letters, numbers, and underscores are allowed!",
                )
                return

            method_entry = self.selected_class.method_list[selected_index]

            # Check if parameter name already exists in the selected method
            for param_tuple in method_entry["parameters"]:
                if param_tuple[1] != param_name:
                    continue
                QtWidgets.QMessageBox.warning(
                    None,
                    "Warning",
                    f"Parameter name '{param_name}' already exists in the selected method!",
                )
                return

            # Get the method number (assuming method numbers start from 1)
            method_num = str(selected_index + 1)

            self.command_factory.class_box = self.selected_class
            add_param_command = self.command_factory.create_command(
                command_name="add_param",
                class_name=selected_class_name,
                method_num=method_num,
                param_type=param_type,
                input_name=param_name,
            )

            is_param_added = self.input_handler.execute_command(add_param_command)

            if not is_param_added:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Warning",
                    f"Method name '{method_name}' has the same parameter list signature as an existing method in class!",
                )

    def delete_param(self):
        """
        Removes a parameter from a selected method in the UML class.

        This function allows the user to select a method and a parameter to delete.
        It updates the UML class box and handles any necessary validations.
        """
        if not self.selected_class:
            return
        if not self.selected_class.method_list:
            return

        delete_param_dialog = Dialog("Delete Parameter")
        delete_param_dialog.delete_param_popup(self.selected_class)

        # Execute dialog and wait for user confirmation
        if delete_param_dialog.exec_() != QtWidgets.QDialog.Accepted:
            return

        param_name = delete_param_dialog.input_widgets["param_name_only"]
        selected_class_name = self.selected_class.class_name_text.toPlainText()
        selected_method_index = delete_param_dialog.input_widgets["method_name_widget"].currentIndex()
        selected_param_index = delete_param_dialog.input_widgets["param_name_widget"].currentIndex()

        self.command_factory.class_box = self.selected_class
        delete_param_command = self.command_factory.create_command(
            command_name="delete_param",
            class_name=selected_class_name,
            method_num=str(selected_method_index + 1),
            selected_param_index=selected_param_index,
            input_name=param_name,
        )

        is_param_deleted = self.input_handler.execute_command(delete_param_command)
        method_entry = self.selected_class.method_list[selected_method_index]

        if not is_param_deleted:
            method_key = method_entry["method_key"]
            QtWidgets.QMessageBox.warning(
                None,
                "Warning",
                f"Method name '{method_key[1]}' has the same parameter list signature as an existing method in class!",
            )

    def rename_param(self):
        """
        Renames a parameter within a selected method in the UML class.

        This function allows the user to select a method and a parameter and provide a new name for the parameter.
        The parameter's name is updated, and the UML class box is refreshed.
        """
        if not self.selected_class:
            return
        if not self.selected_class.method_list:
            return
        # Initialize the dialog
        rename_param_dialog = Dialog("Rename Parameter")
        rename_param_dialog.rename_param_popup(self.selected_class)

        # Execute the dialog and wait for user confirmation (OK or Cancel)
        if rename_param_dialog.exec_() != QtWidgets.QDialog.Accepted:
            return

        selected_method_index = rename_param_dialog.input_widgets['method_name_widget'].currentIndex()
        old_param_name = rename_param_dialog.input_widgets["param_name_only"]
        new_param_name = rename_param_dialog.input_widgets[
            'new_param_name_widget'
        ].text()  # Use `text()` for QLineEdit
        if not new_param_name.strip():
            return
        method_entry = self.selected_class.method_list[selected_method_index]

        for each_tuple in method_entry["parameters"]:
            if new_param_name == each_tuple[1]:
                QtWidgets.QMessageBox.warning(
                    None, "Warning", f"Parameter name '{new_param_name}' has already existed!"
                )
                return

        is_param_name_valid = self.interface.is_valid_input(new_name=new_param_name)
        if not is_param_name_valid:
            QtWidgets.QMessageBox.warning(
                None,
                "Warning",
                f"Parameter name {new_param_name} is invalid! Only letters, numbers, and underscores allowed!",
            )
            return

        selected_class_name = self.selected_class.class_name_text.toPlainText()

        self.command_factory.class_box = self.selected_class
        rename_param_command = self.command_factory.create_command(
            command_name="rename_param",
            class_name=selected_class_name,
            method_num=str(selected_method_index + 1),
            old_name=old_param_name,
            new_name=new_param_name,
        )

        is_param_renamed = self.input_handler.execute_command(rename_param_command)

        if not is_param_renamed:
            QtWidgets.QMessageBox.warning(None, "Rename Failed", "Failed to rename the parameter.")

    def replace_param(self):
        """
        Replaces all parameters of a selected method in the UML class.

        This function allows the user to replace the entire list of parameters for a given method with a new set.
        It prompts the user for a comma-separated list of parameters and updates the UML class box accordingly.
        """
        if not self.selected_class:
            return
        # Ensure there are methods to choose from
        if not self.selected_class.method_list:
            return

        # Initialize the dialog
        replace_param_dialog = Dialog("Replace Parameter List")
        replace_param_dialog.replace_param_list_popup(self.selected_class)

        # Execute the dialog and wait for user confirmation (OK or Cancel)
        if replace_param_dialog.exec_() != QtWidgets.QDialog.Accepted:
            return

        # Get the new parameter string after the dialog is accepted
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
            QtWidgets.QMessageBox.warning(None, "Warning", f"New list contains duplicates: {duplicates}!")
            return

        for each_param in unique_param_names:
            is_param_name_valid = self.interface.is_valid_input(parameter_name=each_param)
            if not is_param_name_valid:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Warning",
                    f"Parameter name {each_param} is invalid! Only letters, numbers, and underscores allowed!",
                )
                return

        self.command_factory.class_box = self.selected_class
        replace_param_command = self.command_factory.create_command(
            command_name="replace_param",
            class_name=selected_class_name,
            method_num=str(selected_method_index + 1),
            new_param_list_obj=new_param_list_obj,
            new_param_list_str=new_param_list_str,
        )

        is_param_list_replaced = self.input_handler.execute_command(replace_param_command)

        if not is_param_list_replaced:
            method_key = method_entry["method_key"]
            QtWidgets.QMessageBox.warning(
                None,
                "Warning",
                f"Method name '{method_key[1]}' has the same parameter list signature as an existing method in class!",
            )

    def edit_param_type(self):
        """
        Edits the type of an existing parameter in a method of the selected UML class.

        This function allows the user to select a parameter and change its data type. It validates
        the new type and updates the UML class box accordingly.
        """
        if not self.selected_class:
            return
        if not self.selected_class.method_list:
            return
        # Initialize the dialog
        edit_param_type_dialog = Dialog("Edit Parameter Type")
        edit_param_type_dialog.edit_param_type_popup(self.selected_class)

        # Execute the dialog and wait for user confirmation (OK or Cancel)
        if edit_param_type_dialog.exec_() != QtWidgets.QDialog.Accepted:
            return

        # Get the method number, parameter name, and new type after the dialog is accepted
        selected_class_name = self.selected_class.class_name_text.toPlainText()
        method_num = edit_param_type_dialog.input_widgets['method_name_widget'].currentIndex()
        param_name = edit_param_type_dialog.input_widgets["param_name_only"]
        new_param_type = edit_param_type_dialog.input_widgets['new_param_type'].text()

        self.command_factory.class_box = self.selected_class
        edit_param_type_command = self.command_factory.create_command(
            command_name="edit_param_type",
            class_name=selected_class_name,
            method_num=str(method_num + 1),
            input_name=param_name,
            new_type=new_param_type,
        )

        self.input_handler.execute_command(edit_param_type_command)

    def add_relationship(self, loaded_source_class=None, loaded_dest_class=None, loaded_type=None, is_loading=False):
        """
        Adds a relationship between two UML classes.

        This function adds a relationship between a source class and a destination class, either by loading the data
        from a saved file or by prompting the user to enter the required information.

        Parameters:
            loaded_source_class (str, optional): The source class for the relationship (used when loading from a file).
            loaded_dest_class (str, optional): The destination class for the relationship (used when loading from a file).
            loaded_type (str, optional): The type of relationship (e.g., inheritance, association) (used when loading from a file).
            is_loading (bool): If True, load the relationship from a saved file.
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
                    value = {"dest_class": loaded_dest_class, "arrow_list": arrow_line}
                    if loaded_source_class not in self.relationship_track_list:
                        self.relationship_track_list[loaded_source_class] = []
                    self.relationship_track_list[loaded_source_class].append(value)
                    self.scene().addItem(arrow_line)  # Add the arrow to the scene to display it
                    # Update the class boxes
                    source_class_obj.update_box()
                    dest_class_obj.update_box()
        else:
            if not self.selected_class:
                return
            # Initialize the dialog
            type_list = [enum.value for enum in RelationshipType]
            add_rel_dialog = Dialog("Add Relationship")
            add_rel_dialog.add_relationship_popup(self.class_name_list, type_list)

            # Execute the dialog and wait for user confirmation (OK or Cancel)
            if add_rel_dialog.exec_() != QtWidgets.QDialog.Accepted:
                return
            # Get the destination class and type after the dialog is accepted
            dest_class = add_rel_dialog.input_widgets[
                "destination_class"
            ].currentText()  # Use `currentText()`
            type = add_rel_dialog.input_widgets["type"].currentText()  # Use `currentText()`
            source_class = self.selected_class.class_name_text.toPlainText()

            self.command_factory.class_box = self.selected_class
            add_rel_command = self.command_factory.create_command(
                command_name="add_rel",
                source_class=source_class,
                dest_class=dest_class,
                rel_type=type,
            )

            is_rel_added = self.input_handler.execute_command(add_rel_command)

            if not is_rel_added:
                QtWidgets.QMessageBox.warning(None, "Warning", "Relationship has already existed!")

    def delete_relationship(self):
        """
        Deletes an existing relationship from the UML class.

        This function prompts the user to select a destination class for the relationship to be deleted.
        The relationship is removed if it exists, and the UML class box is updated.
        """
        if not self.selected_class:
            return
        if not self.selected_class.arrow_line_list:
            return

        source_class = self.selected_class.class_name_text.toPlainText()
        delete_rel_dialog = Dialog("Delete Relationship")
        delete_rel_dialog.delete_relationship_popup(source_class, self.relationship_track_list)

        # Execute the dialog and wait for user confirmation (OK or Cancel)
        if delete_rel_dialog.exec_() != QtWidgets.QDialog.Accepted:
            return
        # Get the destination class after the dialog is accepted
        dest_class = delete_rel_dialog.input_widgets[
            "destination_class_list_of_current_source_class"
        ].currentText()  # Use `currentText()`

        self.command_factory.class_box = self.selected_class
        delete_rel_command = self.command_factory.create_command(
            command_name="delete_rel",
            source_class=source_class,
            dest_class=dest_class,
        )

        self.input_handler.execute_command(delete_rel_command)

    def change_relationship_type(self):
        """
        Changes the type of an existing relationship between two UML classes.

        This function allows the user to modify the relationship type between a source and destination class.
        The updated relationship type is applied, and the UML class box is updated.
        """
        if not self.selected_class:
            return
        if not self.selected_class.arrow_line_list:
            return
        type_list = [enum.value for enum in RelationshipType]
        source_class = self.selected_class.class_name_text.toPlainText()
        change_rel_type_dialog = Dialog("Change Relationship Type")
        change_rel_type_dialog.change_type_popup(source_class, self.relationship_track_list, type_list)

        # Execute the dialog and wait for user confirmation (OK or Cancel)
        if change_rel_type_dialog.exec_() != QtWidgets.QDialog.Accepted:
            return

        # Get the destination class and new type after the dialog is accepted
        dest_class = change_rel_type_dialog.input_widgets[
            "destination_class_list_of_current_source_class"
        ].currentText()  # Use `currentText()`
        new_type = change_rel_type_dialog.input_widgets["type"].currentText()  # Use `currentText()`

        relationships = self.relationship_track_list.get(source_class)
        for relationship in relationships:
            if relationship["dest_class"] != dest_class:
                continue
            arrow_line = relationship["arrow_list"]

            # Normalize and compare the relationship types
            if new_type.strip().lower() == arrow_line.arrow_type.strip().lower():
                QtWidgets.QMessageBox.warning(
                    None, "Warning", f"New relationship type is identical to current type {new_type}!"
                )
                return

            self.command_factory.class_box = self.selected_class
            change_rel_type_command = self.command_factory.create_command(
                command_name="edit_rel_type",
                source_class=source_class,
                dest_class=dest_class,
                new_type=new_type,
                arrow_line=arrow_line,
            )

            is_rel_type_changed = self.input_handler.execute_command(change_rel_type_command)
            if not is_rel_type_changed:
                return

    #################################################################
    ### FILE OPERATIONS ###

    def open_folder_gui(self):
        """
        Opens a file dialog to allow the user to select a JSON file for loading into the application.

        This function uses the `QFileDialog` to let the user select a `.json` file from the file system.
        If a valid JSON file is selected, the function proceeds to load the file into the interface.
        If the selected file is not a JSON file, a warning is displayed to the user.
        """
        # Show an open file dialog and store the selected file path
        full_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open File", os.getcwd(), "JSON Files (*.json)"
        )
        # Check if the user canceled the dialog (full_path will be empty if canceled)
        if not full_path:
            return  # Exit the function if the user cancels the dialog
        # Check if the selected file is a JSON file
        if not full_path.endswith('.json'):
            QtWidgets.QMessageBox.warning(
                None,
                "Warning",
                "The selected file is not a JSON file. Please select a valid JSON file.",
            )
            return
        self.clear_current_scene()  # Clear the scene before loading a new file
        # If a valid file is selected, proceed to load it into the interface
        if full_path:
            file_base_name = os.path.basename(full_path)  # Extract the file name from the full path
            file_name_only = os.path.splitext(file_base_name)[0]  # Remove the file extension
            self.interface.load_gui(file_name_only, full_path, self)  # Load the file into the GUI

    def save_as_gui(self):
        """
        Opens a save file dialog to select a file location for saving.

        This function allows the user to specify a file name and location to save the current UML diagram.
        If the user cancels the dialog or selects an invalid file, appropriate actions are taken.
        """
        full_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", os.getcwd(), "JSON Files (*.json)"
        )
        if not full_path:
            return  # If canceled, just return and do nothing
        if not full_path.endswith('.json'):
            QtWidgets.QMessageBox.warning(
                None,
                "Warning",
                "The selected file is not a JSON file. Please select a valid JSON file.",
            )
            return
        if full_path:
            file_base_name = os.path.basename(full_path)
            file_name_only = os.path.splitext(file_base_name)[0]
            self.interface.save_gui(file_name_only, full_path)

    def save_gui(self):
        """
        Saves to the current active file; if no active file, prompts the user to create a new JSON file.

        This function checks if there is an active file to save to. If there isn't, it invokes the save_as_gui()
        function to prompt the user for a file name and location. If there is an active file, it saves the current
        UML diagram to that file.
        """
        current_active_file_path = self.interface.get_active_file_gui()
        if current_active_file_path == "No active file!":
            self.save_as_gui()
        else:
            file_base_name = os.path.basename(current_active_file_path)
            file_name_only = os.path.splitext(file_base_name)[0]
            self.interface.save_gui(file_name_only, current_active_file_path, self.class_name_list)

    #################################################################
    ### UNDO/REDO OPERATIONS ###

    def undo(self):
        """
        Undoes the last action performed by the user.

        This function interfaces with the input handler to undo the last command executed.
        It also updates the scene to reflect the changes.
        """
        self.input_handler.undo()
        self.scene().update()

    def redo(self):
        """
        Redoes the last action that was undone.

        This function interfaces with the input handler to redo the last command that was undone.
        It also updates the scene to reflect the changes.
        """
        self.input_handler.redo()
        self.scene().update()

    def clear_current_scene(self):
        """
        Removes all UMLClassBox and ArrowLine items from the scene.

        This function iterates through all items in the scene and removes any UMLClassBox or ArrowLine
        instances. This effectively clears the canvas for a new UML diagram.
        """
        # Iterate through all items in the scene
        for item in self.scene().items():
            # Check if the item is a UMLClassBox or ArrowLine
            if isinstance(item, UMLClassBox) or isinstance(item, ArrowLine):
                # Remove the item from the scene
                self.scene().removeItem(item)

    #################################################################
    ## CONTEXT MENU ACTIONS ##

    def contextMenuEvent(self, event):
        """
        Shows the context menu when right-clicking on the UMLClassBox or the background.

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
        """
        Helper function to add a separator in the context menu.

        Parameters:
            context_menu (QMenu): The context menu to add the separator to.
        """
        context_menu.addSeparator()

    #################################################################
    ## MOUSE EVENTS ##

    def wheelEvent(self, event):
        """
        Handles zoom in/out functionality using the mouse wheel.

        Parameters:
            event (QWheelEvent): The wheel event.
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
        Handles mouse press events for starting selection, panning, or determining item selection.

        Prevents the rubber band selection from activating when clicking on UMLClassBox handles.
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
        Handles mouse move events for updating the rubber band rectangle or panning the view.

        This function handles two behaviors based on user interaction:
        - If the user is dragging while holding the left button, update the rubber band selection.
        - If the user is dragging while holding the middle button, pan the view.

        Parameters:
            event (QMouseEvent): The mouse event, providing the current mouse position, buttons pressed, etc.
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
        Handles mouse release events to end panning or finalize the rectangular selection.

        This function ends user actions depending on the released mouse button:
        - Left-click: Finalize the rubber band selection and select items within the rectangle.
        - Middle-click: End panning mode and reset the cursor.

        Parameters:
            event (QMouseEvent): The mouse event, providing information about the button released and the position.
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
                self.command_factory.class_box = self.selected_class
                move_unit_command = self.command_factory.create_command(
                    command_name="move_unit", old_x=old_x, old_y=old_y, new_x=new_x, new_y=new_y
                )
                self.input_handler.execute_command(move_unit_command)

        # Call the parent class's mouseReleaseEvent to ensure default behavior
        super().mouseReleaseEvent(event)
        self.viewport().update()

    def keyPressEvent(self, event):
        """
        Handles key press events (e.g., Delete key to remove items).

        Parameters:
            event (QKeyEvent): The key event.
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
        Selects all items within the provided rectangular area.

        Parameters:
            rect (QRectF): The rectangular area within which to select items.
        """
        items_in_rect = self.scene().items(rect)
        for item in self.scene().selectedItems():
            if isinstance(item, UMLClassBox):
                item.setSelected(False)  # Deselect previously selected items
        for item in items_in_rect:
            if isinstance(item, UMLClassBox):
                item.setSelected(True)  # Select new items in the rectangle

    def new_file(self):
        """
        Creates a new file, clearing any unsaved work.

        This function prompts the user to confirm the creation of a new file.
        If confirmed, it clears the current scene and resets the application state.
        """
        reply = QtWidgets.QMessageBox.question(
            self,
            "New File",
            "Any unsaved work will be deleted! Are you sure you want to create a new file?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Save,
        )
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
        Controls the visibility of the grid lines.

        Parameters:
            visible (bool): If True, the grid is shown; if False, it is hidden.
        """
        self.grid_visible = visible
        self.viewport().update()

    def set_light_mode(self):
        """
        Sets the view to light mode.

        This function changes the background and updates the scene to reflect light mode settings.
        """
        self.is_dark_mode = False
        self.viewport().update()
        self.scene().update()

    def set_dark_mode(self):
        """
        Sets the view to dark mode.

        This function changes the background and updates the scene to reflect dark mode settings.
        """
        self.is_dark_mode = True
        self.viewport().update()
        self.scene().update()

    def toggle_mode(self):
        """
        Toggles between dark mode and light mode.

        This function checks the current mode and switches to the opposite mode.
        """
        if self.is_dark_mode:
            self.set_light_mode()
        else:
            self.set_dark_mode()
