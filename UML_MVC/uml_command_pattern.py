from abc import ABC, abstractmethod
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_arrow_line import UMLArrow as ArrowLine

class Command(ABC):
    """
    Abstract base class for the Command pattern.

    This class defines the interface for commands that can be executed and undone.
    All concrete command classes should inherit from this class and implement the `execute` and `undo` methods.
    """

    @abstractmethod
    def execute(self, is_undo_or_redo=False):
        """
        Execute the command.

        Parameters:
            is_undo_or_redo (bool): Indicates whether the command is being executed as part of an undo or redo operation.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        pass

    @abstractmethod
    def undo(self):
        """
        Undo the command.

        Returns:
            bool: True if the command was undone successfully, False otherwise.
        """
        pass
        
class MoveUnitCommand(Command):
    """
    Command to move a UML class box from one position to another.

    This command encapsulates the action of moving a UML class box to a new position.
    It can be undone to move the class box back to its original position.
    """

    def __init__(self, class_box, old_x, old_y, new_x, new_y):
        """
        Initialize the MoveUnitCommand.

        Parameters:
            class_box (UMLClassBox): The UML class box to move.
            old_x (float): The original x-coordinate of the class box.
            old_y (float): The original y-coordinate of the class box.
            new_x (float): The new x-coordinate for the class box.
            new_y (float): The new y-coordinate for the class box.
        """
        self.class_box = class_box
        self.old_x = old_x
        self.old_y = old_y
        self.new_x = new_x
        self.new_y = new_y
        
    def execute(self, is_undo_or_redo=False):
        """
        Execute the move command by setting the new position of the class box.

        Parameters:
            is_undo_or_redo (bool): Indicates if the command is part of an undo or redo operation.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        if self.class_box:
            self.class_box.setPos(self.new_x, self.new_y)
            self.class_box.update_box()
            return True
        return False
        
    def undo(self):
        """
        Undo the move command by resetting the position of the class box to its original coordinates.

        Returns:
            bool: True if the undo was successful, False otherwise.
        """
        if self.class_box:
            self.class_box.setPos(self.old_x, self.old_y)
            self.class_box.update_box()
            return True
        return False
        
class AddClassCommand(Command):
    """
    Command to add a new UML class to the model and, if applicable, to the GUI.

    This command encapsulates the action of adding a new class to the UML model.
    It can be undone to remove the class from the model and GUI.
    """

    def __init__(self, uml_model, class_name, view=None, class_box=None, is_gui=False):
        """
        Initialize the AddClassCommand.

        Parameters:
            uml_model: The UML model where the class will be added.
            class_name (str): The name of the class to add.
            view (UMLGraphicsView, optional): The view for GUI updates.
            class_box (UMLClassBox, optional): The GUI representation of the class.
            is_gui (bool): Flag indicating whether the command is for GUI mode.
        """
        self.uml_model = uml_model
        self.class_name = class_name
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        """
        Execute the add class command by adding the class to the model and GUI.

        Parameters:
            is_undo_or_redo (bool): Indicates if the command is part of an undo or redo operation.

        Returns:
            bool: True if the class was added successfully, False otherwise.
        """
        is_class_added = self.uml_model._add_class(self.class_name, is_undo_or_redo=is_undo_or_redo)
        if is_class_added and self.is_gui:
            self.view.scene().addItem(self.class_box)
            self.view.class_name_list[self.class_name] = self.class_box
        return is_class_added

    def undo(self):
        """
        Undo the add class command by removing the class from the model and GUI.

        Returns:
            bool: True if the class was removed successfully, False otherwise.
        """
        if self.is_gui:       
            # Remove all associated arrow lines from the scene
            arrow_lines = list(self.class_box.arrow_line_list)
            for arrow_line in arrow_lines:
                # Remove the arrow from the scene if it exists
                if arrow_line.scene() == self.view.scene():
                    self.view.scene().removeItem(arrow_line)
                # Update arrow_line_list of source and destination classes
                if arrow_line.source_class != self.class_box:
                    if arrow_line in arrow_line.source_class.arrow_line_list:
                        arrow_line.source_class.arrow_line_list.remove(arrow_line)
                if arrow_line.dest_class != self.class_box:
                    if arrow_line in arrow_line.dest_class.arrow_line_list:
                        arrow_line.dest_class.arrow_line_list.remove(arrow_line)
                self.class_box.arrow_line_list.remove(arrow_line)
                    
            # Clear all fields and methods in the class_box
            for field_item in self.class_box.field_list.values():
                if field_item.scene() == self.view.scene():
                    self.view.scene().removeItem(field_item)

            for method_entry in self.class_box.method_list:
                if method_entry["method_text"].scene() == self.view.scene():
                    self.view.scene().removeItem(method_entry["method_text"])
                method_entry["method_key"] = None
                method_entry["method_text"] = None
                method_entry["parameters"] = []
                    
            # Clear lists to avoid any visual overlaps on restore
            self.class_box.field_list = {}
            self.class_box.field_key_list = []
            self.class_box.method_list = []
            self.class_box.param_num = 0 
                
            # Remove the class from the class_name_list and scene
            self.view.class_name_list.pop(self.class_name, None)  
            if self.class_box.scene() == self.view.scene():
                self.view.scene().removeItem(self.class_box)    
        return self.uml_model._delete_class(self.class_name, is_undo_or_redo=True)
        
class DeleteClassCommand(Command):
    """
    Command to delete a UML class from the model and GUI.

    This command encapsulates the action of deleting a class from the UML model.
    It stores the state before deletion to allow undoing the deletion.
    """

    def __init__(self, uml_model, class_name, view=None, class_box=None, is_gui=False):
        """
        Initialize the DeleteClassCommand.

        Parameters:
            uml_model: The UML model from which the class will be deleted.
            class_name (str): The name of the class to delete.
            view (UMLGraphicsView, optional): The view for GUI updates.
            class_box (UMLClassBox, optional): The GUI representation of the class.
            is_gui (bool): Flag indicating whether the command is for GUI mode.
        """
        super().__init__()
        self.uml_model = uml_model
        self.class_name = class_name
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui
        self.cli_class_list = None
        self.cli_main_data = None

        # Store the state of the class before deletion
        self.stored_fields = []          # List of tuples: (field_type, field_name)
        self.stored_methods = []         # List of tuples: (method_type, method_name)
        self.stored_parameters = {}      # Dict: {method_key: [(param_type, param_name), ...]}
        self.stored_relationships = {}   # Dictionary of relationships

    def execute(self, is_undo_or_redo=False):
        """
        Execute the delete class command by removing the class from the model and GUI.

        Parameters:
            is_undo_or_redo (bool): Indicates if the command is part of an undo or redo operation.

        Returns:
            bool: True if the class was deleted successfully, False otherwise.
        """
        self.cli_main_data = self.uml_model._get_main_data()
        if self.is_gui:
            # Store relationships
            self.stored_relationships = self.view.relationship_track_list.copy()
            
            # Store all fields before deletion
            self.stored_fields = list(self.class_box.field_list.keys())

            # Store all methods and their parameters before deletion
            for method_entry in self.class_box.method_list:
                method_key = method_entry["method_key"]
                self.stored_methods.append(method_key)
                self.stored_parameters[method_key] = list(method_entry["parameters"])

            # Remove all associated arrow lines from the scene
            arrow_lines = list(self.class_box.arrow_line_list)
            for arrow_line in arrow_lines:
                if arrow_line.scene() == self.view.scene():
                    self.view.scene().removeItem(arrow_line)
                if arrow_line.source_class != self.class_box:
                    if arrow_line in arrow_line.source_class.arrow_line_list:
                        arrow_line.source_class.arrow_line_list.remove(arrow_line)
                if arrow_line.dest_class != self.class_box:
                    if arrow_line in arrow_line.dest_class.arrow_line_list:
                        arrow_line.dest_class.arrow_line_list.remove(arrow_line)
                self.class_box.arrow_line_list.remove(arrow_line)

            # Remove all fields from the scene
            for field_key in self.stored_fields:
                field_text = self.class_box.field_list.get(field_key)
                if field_text and field_text.scene() == self.view.scene():
                    self.view.scene().removeItem(field_text)

            # Remove all methods and their parameters from the scene
            for method_entry in self.class_box.method_list:
                method_text = method_entry["method_text"]
                if method_text and method_text.scene() == self.view.scene():
                    self.view.scene().removeItem(method_text)

            # Update the class box and remove it from the scene
            self.class_box.update_box()
            if self.class_box.scene() == self.view.scene():
                self.view.scene().removeItem(self.class_box)

            # Clear lists to avoid any visual overlaps on restore
            self.class_box.field_list = {}
            self.class_box.field_key_list = []
            self.class_box.method_list = []
            self.class_box.param_num = 0
            self.view.relationship_track_list = {}
            self.view.class_name_list.pop(self.class_name, None)

        # Delete the class from the model
        result = self.uml_model._delete_class(self.class_name, is_undo_or_redo=is_undo_or_redo)
        return result

    def undo(self):
        """
        Undo the delete class command by restoring the class to the model and GUI.

        Returns:
            bool: True if the class was restored successfully, False otherwise.
        """
        if self.is_gui:
            if self.class_name in self.view.class_name_list:
                return False
            # Re-execute the AddClassCommand to add the class back
            add_class_command = AddClassCommand(
                uml_model=self.uml_model,
                class_name=self.class_name,
                view=self.view,
                class_box=self.class_box,
                is_gui=True
            )
            add_class_command.execute(is_undo_or_redo=True)

            # Re-execute all AddFieldCommands to restore fields
            for field_key in self.stored_fields:
                field_type, field_name = field_key
                add_field_command = AddFieldCommand(
                    uml_model=self.uml_model,
                    class_name=self.class_name,
                    type=field_type,
                    field_name=field_name,
                    view=self.view,
                    class_box=self.class_box,
                    is_gui=True
                )
                add_field_command.execute(is_undo_or_redo=True)

            # Re-execute all AddMethodCommands to restore methods
            for i, method_key in enumerate(self.stored_methods, start=1):
                method_type, method_name = method_key
                add_method_command = AddMethodCommand(
                    uml_model=self.uml_model,
                    class_name=self.class_name,
                    type=method_type,
                    method_name=method_name,
                    view=self.view,
                    class_box=self.class_box,
                    is_gui=True
                )
                add_method_command.execute(is_undo_or_redo=True)

                # Re-execute all AddParameterCommands for each method
                parameters = self.stored_parameters.get(method_key, [])
                method_num = str(i)  # Assign method_num based on the order of restoration
                for param_type, param_name in parameters:
                    add_param_command = AddParameterCommand(
                        uml_model=self.uml_model,
                        class_name=self.class_name,
                        method_num=method_num,
                        param_type=param_type,
                        param_name=param_name,
                        view=self.view,
                        class_box=self.class_box,
                        is_gui=True
                    )
                    add_param_command.execute(is_undo_or_redo=True)

            # Restore all relationships (arrow lines)
            for source_class_str, arrow_list in self.stored_relationships.items():
                source_class_obj = self.view.class_name_list.get(source_class_str)
                if not source_class_obj:
                    continue  # Skip if source class doesn't exist

                for relationship in arrow_list:
                    dest_class_str = relationship["dest_class"]
                    arrow_line = relationship["arrow_list"]
                    
                    dest_class_obj = self.view.class_name_list.get(dest_class_str)
                    if not dest_class_obj:
                        continue  # Skip if destination class doesn't exist

                    source_class_box = source_class_obj  

                    # Instantiate the AddRelationshipCommand
                    add_relationship_command = AddRelationshipCommand(
                        uml_model=self.uml_model,
                        source_class=source_class_str,
                        dest_class=dest_class_str,
                        rel_type=arrow_line.arrow_type,
                        view=self.view,
                        class_box=source_class_box,
                        is_gui=True
                    )
                    add_relationship_command.execute(is_undo_or_redo=True)
        else:
            # For CLI mode, re-add the class and its components
            if self.class_name in self.uml_model._get_class_list():
                return False
            main_data = self.cli_main_data
            class_data = main_data["classes"]
            relationship_data = main_data["relationships"]
            extracted_class_data = self.uml_model._extract_class_data(class_data)

            for each_pair in extracted_class_data:
                for class_name, data in each_pair.items():
                    field_list = data["fields"]
                    method_list = data["method_list"]

                    if class_name != self.class_name:
                        continue
                    add_class_command = AddClassCommand(
                        uml_model=self.uml_model,
                        class_name=self.class_name,
                        view=self.view,
                        class_box=self.class_box,
                    )
                    add_class_command.execute(is_undo_or_redo=True)
                    
                    for each_field in field_list:
                        field_name = each_field["name"]
                        field_type = each_field["type"]
                        add_field_command = AddFieldCommand(
                            uml_model=self.uml_model,
                            class_name=self.class_name,
                            type=field_type,
                            field_name=field_name,
                            view=self.view,
                            class_box=self.class_box,
                        )
                        add_field_command.execute(is_undo_or_redo=True)
                            
                    method_num = "0"
                    i = 0
                    for each_element in method_list:
                        i += 1
                        method_num = f"{i}"
                        method_name = each_element["name"]
                        return_type = each_element["return_type"]
                        parameter_list = each_element["params"]
                        
                        add_method_command = AddMethodCommand(
                            uml_model=self.uml_model,
                            class_name=self.class_name,
                            type=return_type,
                            method_name=method_name,
                            view=self.view,
                            class_box=self.class_box,
                        )
                        add_method_command.execute(is_undo_or_redo=True)
                            
                        for param in parameter_list:
                            param_type = param["type"]
                            param_name = param["name"]
                            add_param_command = AddParameterCommand(
                                uml_model=self.uml_model,
                                class_name=self.class_name,
                                method_num=method_num,
                                param_type=param_type,
                                param_name=param_name,
                                view=self.view,
                                class_box=self.class_box,
                            )
                            add_param_command.execute(is_undo_or_redo=True)
                                
            # Recreate relationships from the loaded data
            for each_dictionary in relationship_data:
                if each_dictionary["source"] == self.class_name:
                    self.uml_model._add_relationship(each_dictionary["source"], each_dictionary["destination"], each_dictionary["type"], is_loading=True, is_gui=False)
                if each_dictionary["destination"] == self.class_name:
                    self.uml_model._add_relationship(each_dictionary["source"], each_dictionary["destination"], each_dictionary["type"], is_loading=True, is_gui=False)
                
        # Clear stored data
        self.stored_fields = []
        self.stored_methods = []
        self.stored_parameters = {}
        self.stored_relationships = {}
        return True

class RenameClassCommand(Command):
    """
    Command to rename an existing UML class in the model and GUI.

    This command encapsulates the action of renaming a class.
    It can be undone to restore the original class name.
    """

    def __init__(self, uml_model, class_name, new_name, view=None, class_box=None, is_gui=False):
        """
        Initialize the RenameClassCommand.

        Parameters:
            uml_model: The UML model containing the class to rename.
            class_name (str): The current name of the class.
            new_name (str): The new name for the class.
            view (UMLGraphicsView, optional): The view for GUI updates.
            class_box (UMLClassBox, optional): The GUI representation of the class.
            is_gui (bool): Flag indicating whether the command is for GUI mode.
        """
        self.uml_model = uml_model
        self.class_name = class_name
        self.new_name = new_name
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        """
        Execute the rename class command by updating the class name in the model and GUI.

        Parameters:
            is_undo_or_redo (bool): Indicates if the command is part of an undo or redo operation.

        Returns:
            bool: True if the class was renamed successfully, False otherwise.
        """
        is_class_renamed = self.uml_model._rename_class(self.class_name, self.new_name, is_undo_or_redo=is_undo_or_redo)
        if is_class_renamed and self.is_gui:
            self.class_box.class_name_text.setPlainText(self.new_name)
            self.class_box.update_box()
        return is_class_renamed

    def undo(self):
        """
        Undo the rename class command by restoring the original class name.

        Returns:
            bool: True if the class name was restored successfully, False otherwise.
        """
        if self.is_gui:
            self.class_box.class_name_text.setPlainText(self.class_name)
        return self.uml_model._rename_class(self.new_name, self.class_name, is_undo_or_redo=True)
            
class AddFieldCommand(Command):
    """
    Command to add a new field to a UML class in the model and GUI.

    This command encapsulates the action of adding a new field to a class.
    It can be undone to remove the field from the class.
    """

    def __init__(self, uml_model, class_name, type, field_name, view=None, class_box=None, is_gui=False):
        """
        Initialize the AddFieldCommand.

        Parameters:
            uml_model: The UML model containing the class.
            class_name (str): The name of the class to which the field will be added.
            type (str): The data type of the field.
            field_name (str): The name of the field.
            view (UMLGraphicsView, optional): The view for GUI updates.
            class_box (UMLClassBox, optional): The GUI representation of the class.
            is_gui (bool): Flag indicating whether the command is for GUI mode.
        """
        self.uml_model = uml_model
        self.class_name = class_name
        self.field_type = type
        self.field_name = field_name
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        """
        Execute the add field command by adding the field to the model and GUI.

        Parameters:
            is_undo_or_redo (bool): Indicates if the command is part of an undo or redo operation.

        Returns:
            bool: True if the field was added successfully, False otherwise.
        """
        is_field_added = self.uml_model._add_field(self.class_name, self.field_type, self.field_name, is_undo_or_redo=is_undo_or_redo)
        if is_field_added and self.is_gui:
            field_text = self.class_box.create_text_item(
                f"{self.field_type} {self.field_name}",
                is_field=True,
                selectable=False,
                color=self.class_box.text_color
            )
            field_key = (self.field_type, self.field_name)
            self.class_box.field_list[field_key] = field_text  # Add to internal list
            self.class_box.field_key_list.append(field_key)    # Track field name
            self.class_box.update_box()
        return is_field_added

    def undo(self):
        """
        Undo the add field command by removing the field from the model and GUI.

        Returns:
            bool: True if the field was removed successfully, False otherwise.
        """
        if self.is_gui:
            for field_key in self.class_box.field_key_list:
                if field_key[1] != self.field_name:
                    continue
                self.class_box.field_key_list.remove(field_key)
                self.class_box.scene().removeItem(self.class_box.field_list.pop(field_key))
            self.class_box.update_box()
        return self.uml_model._delete_field(self.class_name, self.field_name, is_undo_or_redo=True)

class DeleteFieldCommand(Command):
    """
    Command to delete a field from a UML class in the model and GUI.

    This command encapsulates the action of deleting a field from a class.
    It stores the field's data to allow undoing the deletion.
    """

    def __init__(self, uml_model, class_name, field_name, view=None, class_box=None, is_gui=False):
        """
        Initialize the DeleteFieldCommand.

        Parameters:
            uml_model: The UML model containing the class.
            class_name (str): The name of the class from which the field will be deleted.
            field_name (str): The name of the field to delete.
            view (UMLGraphicsView, optional): The view for GUI updates.
            class_box (UMLClassBox, optional): The GUI representation of the class.
            is_gui (bool): Flag indicating whether the command is for GUI mode.
        """
        self.uml_model = uml_model
        self.class_name = class_name
        self.field_name = field_name
        self.field_type = None  # To store the type of the field when it's deleted
        self.view = view
        self.class_box = class_box
        self.position = None  # To store the position of the field when deleted
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        """
        Execute the delete field command by removing the field from the model and GUI.

        Parameters:
            is_undo_or_redo (bool): Indicates if the command is part of an undo or redo operation.

        Returns:
            bool: True if the field was deleted successfully, False otherwise.
        """
        if self.is_gui:
            chosen_field = self.uml_model._get_chosen_field_or_method(self.class_name, self.field_name, is_field=True)
            if chosen_field is not None:
                self.field_type = chosen_field._get_type()
            for index, field_key in enumerate(self.class_box.field_key_list):
                if field_key[1] != self.field_name:
                    continue
                self.position = index
                self.class_box.field_key_list.remove(field_key)
                self.class_box.scene().removeItem(self.class_box.field_list.pop(field_key))
            self.class_box.update_box()
        return self.uml_model._delete_field(self.class_name, self.field_name, is_undo_or_redo=is_undo_or_redo)

    def undo(self):
        """
        Undo the delete field command by restoring the field to the model and GUI.

        Returns:
            bool: True if the field was restored successfully, False otherwise.
        """
        is_field_added = self.uml_model._add_field(self.class_name, self.field_type, self.field_name, is_undo_or_redo=True)
        if is_field_added and self.is_gui:
            field_text = self.class_box.create_text_item(
                f"{self.field_type} {self.field_name}",
                is_field=True,
                selectable=False,
                color=self.class_box.text_color
            )
            field_key = (self.field_type, self.field_name)
            self.class_box.field_list[field_key] = field_text
            self.class_box.field_key_list.insert(self.position, field_key)
            self.class_box.update_box()
        return is_field_added

class RenameFieldCommand(Command):
    """
    Command to rename a field in a UML class in the model and GUI.

    This command encapsulates the action of renaming a field.
    It can be undone to restore the original field name.
    """

    def __init__(self, uml_model, class_name, old_field_name, new_field_name, view=None, class_box=None, is_gui=False):
        """
        Initialize the RenameFieldCommand.

        Parameters:
            uml_model: The UML model containing the class.
            class_name (str): The name of the class containing the field.
            old_field_name (str): The current name of the field.
            new_field_name (str): The new name for the field.
            view (UMLGraphicsView, optional): The view for GUI updates.
            class_box (UMLClassBox, optional): The GUI representation of the class.
            is_gui (bool): Flag indicating whether the command is for GUI mode.
        """
        self.uml_model = uml_model
        self.class_name = class_name
        self.old_name = old_field_name
        self.new_name = new_field_name
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        """
        Execute the rename field command by updating the field name in the model and GUI.

        Parameters:
            is_undo_or_redo (bool): Indicates if the command is part of an undo or redo operation.

        Returns:
            bool: True if the field was renamed successfully, False otherwise.
        """
        is_field_renamed = self.uml_model._rename_field(self.class_name, self.old_name, self.new_name, is_undo_or_redo=is_undo_or_redo)
        if is_field_renamed and self.is_gui:
            for field_key in self.class_box.field_list:
                if field_key[1] != self.old_name:
                    continue
                new_key = (field_key[0], self.new_name)
                self.class_box.field_list[new_key] = self.class_box.field_list.pop(field_key)
                self.class_box.field_list[new_key].setPlainText(f"{field_key[0]} {self.new_name}")
                index = self.class_box.field_key_list.index(field_key)
                self.class_box.field_key_list[index] = new_key
                break
            self.class_box.update_box()
        return is_field_renamed

    def undo(self):
        """
        Undo the rename field command by restoring the original field name.

        Returns:
            bool: True if the field name was restored successfully, False otherwise.
        """
        is_field_renamed = self.uml_model._rename_field(self.class_name, self.new_name, self.old_name, is_undo_or_redo=True)
        if is_field_renamed and self.is_gui:
            for field_key in self.class_box.field_list:
                if field_key[1] != self.new_name:
                    continue
                new_key = (field_key[0], self.old_name)
                self.class_box.field_list[new_key] = self.class_box.field_list.pop(field_key)
                self.class_box.field_list[new_key].setPlainText(f"{field_key[0]} {self.old_name}")
                index = self.class_box.field_key_list.index(field_key)
                self.class_box.field_key_list[index] = new_key
                break
            self.class_box.update_box()
        return is_field_renamed

class AddMethodCommand(Command):
    """
    Command to add a new method to a UML class in the model and GUI.

    This command encapsulates the action of adding a new method to a class.
    It can be undone to remove the method from the class.
    """

    def __init__(self, uml_model, class_name, type, method_name, view=None, class_box=None, is_gui=False):
        """
        Initialize the AddMethodCommand.

        Parameters:
            uml_model: The UML model containing the class.
            class_name (str): The name of the class to which the method will be added.
            type (str): The return type of the method.
            method_name (str): The name of the method.
            view (UMLGraphicsView, optional): The view for GUI updates.
            class_box (UMLClassBox, optional): The GUI representation of the class.
            is_gui (bool): Flag indicating whether the command is for GUI mode.
        """
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_type = type
        self.method_name = method_name
        self.method_text = None
        self.view = view
        self.class_box = class_box
        self.method_num = None
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        """
        Execute the add method command by adding the method to the model and GUI.

        Parameters:
            is_undo_or_redo (bool): Indicates if the command is part of an undo or redo operation.

        Returns:
            bool: True if the method was added successfully, False otherwise.
        """
        is_method_added = self.uml_model._add_method(self.class_name, self.method_type, self.method_name, is_undo_or_redo=is_undo_or_redo)
        if is_method_added and self.is_gui:
            method_text = self.class_box.create_text_item(
                f"{self.method_type} {self.method_name}()",
                is_method=True,
                selectable=False,
                color=self.class_box.text_color
            )
            method_key = (self.method_type, self.method_name)
            method_entry = {
                "method_key": method_key,
                "method_text": method_text,
                "parameters": []
            }
            self.class_box.method_list.append(method_entry)
            self.method_num = str(len(self.class_box.method_list))
            if len(self.class_box.method_list) == 1:
                self.class_box.create_separator(is_first=False, is_second=True)
            self.class_box.update_box()
        return is_method_added

    def undo(self):
        """
        Undo the add method command by removing the method from the model and GUI.

        Returns:
            bool: True if the method was removed successfully, False otherwise.
        """
        method_and_parameter_list = self.uml_model._get_data_from_chosen_class(self.class_name, is_method_and_param_list=True)
        current_method_index_cli = len(method_and_parameter_list)
        is_method_deleted_cli = self.uml_model._delete_method(self.class_name, str(current_method_index_cli), is_undo_or_redo=True)
        if self.is_gui and is_method_deleted_cli:
            method_entry = self.class_box.method_list[int(self.method_num) - 1]
            if method_entry["method_text"].scene() == self.view.scene():
                self.view.scene().removeItem(method_entry["method_text"])
            self.class_box.method_list.pop(int(self.method_num) - 1)
            self.class_box.update_box()
        return is_method_deleted_cli

class DeleteMethodCommand(Command):
    """
    Command to delete a method from a UML class in the model and GUI.

    This command encapsulates the action of deleting a method from a class.
    It stores the method's data to allow undoing the deletion.
    """

    def __init__(self, uml_model, class_name, method_num, view=None, class_box=None, is_gui=False):
        """
        Initialize the DeleteMethodCommand.

        Parameters:
            uml_model: The UML model containing the class.
            class_name (str): The name of the class from which the method will be deleted.
            method_num (str): The index number of the method to delete.
            view (UMLGraphicsView, optional): The view for GUI updates.
            class_box (UMLClassBox, optional): The GUI representation of the class.
            is_gui (bool): Flag indicating whether the command is for GUI mode.
        """
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.method_name = None
        self.method_type = None
        self.view = view
        self.old_param_list = []
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        """
        Execute the delete method command by removing the method from the model and GUI.

        Parameters:
            is_undo_or_redo (bool): Indicates if the command is part of an undo or redo operation.

        Returns:
            bool: True if the method was deleted successfully, False otherwise.
        """
        chosen_method = self.uml_model._get_method_based_on_index(self.class_name, self.method_num)
        if chosen_method is None:
            return False
        self.method_type = chosen_method._get_type()
        self.method_name = chosen_method._get_name()
        
        method_entry = self.class_box.method_list[int(self.method_num) - 1]
        self.old_param_list = method_entry["parameters"]
        is_method_deleted = self.uml_model._delete_method(self.class_name, self.method_num, is_undo_or_redo=is_undo_or_redo)
        
        if is_method_deleted and self.is_gui:
            if method_entry["method_text"].scene() == self.view.scene():
                self.view.scene().removeItem(method_entry["method_text"])
            self.class_box.method_list.pop(int(self.method_num) - 1)
            self.class_box.update_box()
                
        return is_method_deleted
            
    def undo(self):
        """
        Undo the delete method command by restoring the method to the model and GUI.

        Returns:
            bool: True if the method was restored successfully, False otherwise.
        """
        if self.method_type and self.method_name:
            is_method_added = self.uml_model._add_method(self.class_name, self.method_type, self.method_name, is_undo_or_redo=True)
            if is_method_added and self.is_gui:
                method_text = self.class_box.create_text_item(
                    f"{self.method_type} {self.method_name}()",
                    is_method=True,
                    selectable=False,
                    color=self.class_box.text_color
                )
                method_key = (self.method_type, self.method_name)
                method_entry = {
                    "method_key": method_key,
                    "method_text": method_text,
                    "parameters": self.old_param_list
                }
                self.class_box.method_list.insert(int(self.method_num) - 1, method_entry)
                if len(self.class_box.method_list) == 1:
                    self.class_box.create_separator(is_first=False, is_second=True)
                self.class_box.update_box()
            return is_method_added
        return False
    
class RenameMethodCommand(Command):
    """
    Command to rename a method in a UML class in the model and GUI.

    This command encapsulates the action of renaming a method.
    It can be undone to restore the original method name.
    """

    def __init__(self, uml_model, class_name, method_num, new_name, view=None, class_box=None, is_gui=False):
        """
        Initialize the RenameMethodCommand.

        Parameters:
            uml_model: The UML model containing the class.
            class_name (str): The name of the class containing the method.
            method_num (str): The index number of the method to rename.
            new_name (str): The new name for the method.
            view: The GUI view, if applicable.
            class_box: The UMLClassBox instance representing the class in the GUI.
            is_gui (bool): Indicates if the command is for the GUI.
        """
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.old_name = None  # Will be set during execution
        self.new_name = new_name
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        """
        Execute the rename method command, renaming the method in the model and GUI.

        Parameters:
            is_undo_or_redo (bool): Indicates if the execution is part of an undo or redo operation.

        Returns:
            bool: True if the method was renamed successfully, False otherwise.
        """
        # Retrieve the method to rename
        chosen_method = self.uml_model._get_method_based_on_index(self.class_name, self.method_num)
        if chosen_method is None:
            return False
        self.old_name = chosen_method._get_name()

        # Rename the method in the model
        is_method_renamed = self.uml_model._rename_method(
            self.class_name, self.method_num, self.new_name, is_undo_or_redo=is_undo_or_redo
        )

        if is_method_renamed and self.is_gui:
            # Access the method entry to rename
            method_entry = self.class_box.method_list[int(self.method_num) - 1]
            old_method_key = method_entry["method_key"]
            method_type = old_method_key[0]

            # Create the new method key with the updated name
            new_method_key = (method_type, self.new_name)
            method_entry["method_key"] = new_method_key  # Update key in method entry

            # Update the display text of the method in the UI
            method_text = method_entry["method_text"]
            param_list = method_entry["parameters"]
            param_str = ', '.join(f"{param_type} {param_name}" for param_type, param_name in param_list)
            method_text.setPlainText(f"{method_type} {self.new_name}({param_str})")

            self.class_box.update_box()  # Refresh the UML box display
        return is_method_renamed

    def undo(self):
        """
        Undo the rename method command, restoring the method's original name.

        Returns:
            bool: True if the undo was successful, False otherwise.
        """
        if self.old_name:
            # Rename the method back to its original name in the model
            is_method_renamed = self.uml_model._rename_method(
                self.class_name, self.method_num, self.old_name, is_undo_or_redo=True
            )
            if is_method_renamed and self.is_gui:
                # Access the method entry to rename
                method_entry = self.class_box.method_list[int(self.method_num) - 1]
                old_method_key = method_entry["method_key"]
                method_type = old_method_key[0]

                # Create the new method key with the original name
                new_method_key = (method_type, self.old_name)
                method_entry["method_key"] = new_method_key  # Update key in method entry

                # Update the display text of the method in the UI
                method_text = method_entry["method_text"]
                param_list = method_entry["parameters"]
                param_str = ', '.join(f"{param_type} {param_name}" for param_type, param_name in param_list)
                method_text.setPlainText(f"{method_type} {self.old_name}({param_str})")

                self.class_box.update_box()  # Refresh the UML box display
            return is_method_renamed
        return False
    
class AddParameterCommand(Command):
    """
    Command to add a parameter to a method in a UML class in the model and GUI.

    This command encapsulates the action of adding a parameter to a method.
    It can be undone to remove the parameter from the method.
    """

    def __init__(self, uml_model, class_name: str = None, method_num: str = None,
                 param_type: str = None, param_name: str = None, view=None, class_box=None, is_gui=False):
        """
        Initialize the AddParameterCommand.

        Parameters:
            uml_model: The UML model containing the class.
            class_name (str): The name of the class containing the method.
            method_num (str): The index number of the method to add the parameter to.
            param_type (str): The type of the parameter.
            param_name (str): The name of the parameter.
            view: The GUI view, if applicable.
            class_box: The UMLClassBox instance representing the class in the GUI.
            is_gui (bool): Indicates if the command is for the GUI.
        """
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.param_type = param_type
        self.param_name = param_name
        self.selected_param_index = None  # Will be set during execution
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        """
        Execute the add parameter command, adding the parameter to the method in the model and GUI.

        Parameters:
            is_undo_or_redo (bool): Indicates if the execution is part of an undo or redo operation.

        Returns:
            bool: True if the parameter was added successfully, False otherwise.
        """
        is_param_added = self.uml_model._add_parameter(
            self.class_name, str(self.method_num), self.param_type, self.param_name, is_undo_or_redo=is_undo_or_redo
        )
        if is_param_added and self.is_gui:
            # Append the parameter to the method's parameter list
            param_tuple = (self.param_type, self.param_name)
            method_entry = self.class_box.method_list[int(self.method_num) - 1]
            method_entry["parameters"].append(param_tuple)
            self.class_box.param_num = len(method_entry["parameters"])
            self.selected_param_index = self.class_box.param_num - 1
            self.class_box.update_box()  # Update the UML box
        return is_param_added

    def undo(self):
        """
        Undo the add parameter command, removing the parameter from the method in the model and GUI.

        Returns:
            bool: True if the undo was successful, False otherwise.
        """
        if self.is_gui:
            # Remove the parameter from the method's parameter list
            method_entry = self.class_box.method_list[int(self.method_num) - 1]
            method_entry["parameters"].pop(self.selected_param_index)
            self.class_box.param_num = len(method_entry["parameters"])
            self.class_box.update_box()  # Refresh the UML box
        return self.uml_model._delete_parameter(
            self.class_name, str(self.method_num), self.param_name, is_undo_or_redo=True
        )

class DeleteParameterCommand(Command):
    """
    Command to delete a parameter from a method in a UML class in the model and GUI.

    This command encapsulates the action of deleting a parameter from a method.
    It can be undone to restore the parameter to the method.
    """

    def __init__(self, uml_model, class_name, method_num, param_name, selected_param_index=None, view=None, class_box=None, is_gui=False):
        """
        Initialize the DeleteParameterCommand.

        Parameters:
            uml_model: The UML model containing the class.
            class_name (str): The name of the class containing the method.
            method_num (str): The index number of the method from which to delete the parameter.
            param_name (str): The name of the parameter to delete.
            selected_param_index (int, optional): The index of the parameter in the parameter list.
            view: The GUI view, if applicable.
            class_box: The UMLClassBox instance representing the class in the GUI.
            is_gui (bool): Indicates if the command is for the GUI.
        """
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.param_name = param_name
        self.param_type = None  # Will be set during execution
        self.selected_param_index = selected_param_index
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        """
        Execute the delete parameter command, removing the parameter from the method in the model and GUI.

        Parameters:
            is_undo_or_redo (bool): Indicates if the execution is part of an undo or redo operation.

        Returns:
            bool: True if the parameter was deleted successfully, False otherwise.
        """
        chosen_param = self.uml_model._get_param_based_on_index(
            self.class_name, self.method_num, self.param_name
        )
        if chosen_param is None:
            return False
        self.param_type = chosen_param._get_type()
        is_param_deleted = self.uml_model._delete_parameter(
            self.class_name, str(self.method_num), self.param_name, is_undo_or_redo=is_undo_or_redo
        )
        if is_param_deleted and self.is_gui:
            # Remove the parameter from the method's parameter list
            method_entry = self.class_box.method_list[int(self.method_num) - 1]
            method_entry["parameters"].pop(self.selected_param_index)
            self.class_box.update_box()  # Refresh the UML box
            self.class_box.param_num -= 1
        return is_param_deleted

    def undo(self):
        """
        Undo the delete parameter command, restoring the parameter to the method in the model and GUI.

        Returns:
            bool: True if the undo was successful, False otherwise.
        """
        if self.param_type:
            param_tuple = (self.param_type, self.param_name)
            if self.is_gui:
                # Append the parameter back to the method's parameter list
                method_entry = self.class_box.method_list[int(self.method_num) - 1]
                method_entry["parameters"].append(param_tuple)
                self.selected_param_index = len(method_entry["parameters"]) - 1
                self.class_box.param_num += 1
                self.class_box.update_box()  # Update the UML box
            return self.uml_model._add_parameter(
                self.class_name, str(self.method_num), self.param_type, self.param_name, is_undo_or_redo=True
            )
        return False

class RenameParameterCommand(Command):
    """
    Command to rename a parameter in a method in the UML model and GUI.

    This command encapsulates the action of renaming a parameter within a method.
    It can be undone to restore the parameter's original name.
    """

    def __init__(self, uml_model, class_name, method_num, old_param_name, new_param_name, view=None, class_box=None, is_gui=False):
        """
        Initialize the RenameParameterCommand.

        Parameters:
            uml_model: The UML model containing the class.
            class_name (str): The name of the class containing the method.
            method_num (str): The index number of the method containing the parameter.
            old_param_name (str): The current name of the parameter.
            new_param_name (str): The new name for the parameter.
            view: The GUI view, if applicable.
            class_box: The UMLClassBox instance representing the class in the GUI.
            is_gui (bool): Indicates if the command is for the GUI.
        """
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.old_param_name = old_param_name
        self.new_param_name = new_param_name
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        """
        Execute the rename parameter command, renaming the parameter in the model and GUI.

        Parameters:
            is_undo_or_redo (bool): Indicates if the execution is part of an undo or redo operation.

        Returns:
            bool: True if the parameter was renamed successfully, False otherwise.
        """
        is_param_renamed = self.uml_model._rename_parameter(
            self.class_name, self.method_num, self.old_param_name, self.new_param_name, is_undo_or_redo=is_undo_or_redo
        )
        if is_param_renamed and self.is_gui:
            # Find and replace the parameter in the method's parameter list
            method_entry = self.class_box.method_list[int(self.method_num) - 1]
            for i, param_tuple in enumerate(method_entry["parameters"]):
                if param_tuple[1] != self.old_param_name:
                    continue
                method_entry["parameters"][i] = (param_tuple[0], self.new_param_name)
                break
            self.class_box.update_box()  # Refresh the UML box
        return is_param_renamed

    def undo(self):
        """
        Undo the rename parameter command, restoring the parameter's original name.

        Returns:
            bool: True if the undo was successful, False otherwise.
        """
        is_param_renamed = self.uml_model._rename_parameter(
            self.class_name, self.method_num, self.new_param_name, self.old_param_name, is_undo_or_redo=True
        )
        if is_param_renamed and self.is_gui:
            # Find and replace the parameter back to its original name
            method_entry = self.class_box.method_list[int(self.method_num) - 1]
            for i, param_tuple in enumerate(method_entry["parameters"]):
                if param_tuple[1] != self.new_param_name:
                    continue
                method_entry["parameters"][i] = (param_tuple[0], self.old_param_name)
                break
            self.class_box.update_box()  # Refresh the UML box
        return is_param_renamed

class ReplaceParameterListCommand(Command):
    """
    Command to replace the entire parameter list of a method in the UML model and GUI.

    This command encapsulates the action of replacing a method's parameter list.
    It can be undone to restore the original parameter list.
    """

    def __init__(self, uml_model, class_name, method_num,
                 new_param_list_obj=None, new_param_list_str=None, view=None, class_box=None, is_gui=False):
        """
        Initialize the ReplaceParameterListCommand.

        Parameters:
            uml_model: The UML model containing the class.
            class_name (str): The name of the class containing the method.
            method_num (str): The index number of the method.
            new_param_list_obj (list of tuples): The new parameter list as objects (type, name).
            new_param_list_str (list of str): The new parameter list as strings.
            view: The GUI view, if applicable.
            class_box: The UMLClassBox instance representing the class in the GUI.
            is_gui (bool): Indicates if the command is for the GUI.
        """
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.old_param_list_str = None  # Will be set during execution
        self.old_param_list_obj = None  # Will be set during execution
        self.new_param_list_str = new_param_list_str
        self.new_param_list_obj = new_param_list_obj
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        """
        Execute the replace parameter list command, replacing the method's parameters in the model and GUI.

        Parameters:
            is_undo_or_redo (bool): Indicates if the execution is part of an undo or redo operation.

        Returns:
            bool: True if the parameter list was replaced successfully, False otherwise.
        """
        is_param_list_replaced = self.uml_model._replace_param_list(
            self.class_name, self.method_num, self.new_param_list_str, is_undo_or_redo=is_undo_or_redo
        )
        if is_param_list_replaced and self.is_gui:
            # Store the old parameter list before replacing
            method_entry = self.class_box.method_list[int(self.method_num) - 1]
            self.old_param_list_obj = method_entry["parameters"]
            self.old_param_list_str = [f"{ptype} {pname}" for ptype, pname in self.old_param_list_obj]
            # Replace the parameter list
            method_entry["parameters"] = self.new_param_list_obj
            self.class_box.param_num = len(method_entry["parameters"])
            self.class_box.update_box()  # Update the UML box
        return is_param_list_replaced

    def undo(self):
        """
        Undo the replace parameter list command, restoring the original parameter list.

        Returns:
            bool: True if the undo was successful, False otherwise.
        """
        is_param_list_replaced = self.uml_model._replace_param_list(
            self.class_name, self.method_num, self.old_param_list_str, is_undo_or_redo=True
        )
        if is_param_list_replaced and self.is_gui:
            # Restore the old parameter list
            method_entry = self.class_box.method_list[int(self.method_num) - 1]
            self.new_param_list_obj = method_entry["parameters"]
            method_entry["parameters"] = self.old_param_list_obj
            self.class_box.param_num = len(method_entry["parameters"])
            self.class_box.update_box()  # Update the UML box
        return is_param_list_replaced

class AddRelationshipCommand(Command):
    """
    Command to add a relationship between two UML classes in the model and GUI.

    This command encapsulates the action of adding a relationship.
    It can be undone to remove the relationship.
    """

    def __init__(self, uml_model, source_class, dest_class, rel_type, view=None, class_box=None, is_gui=False):
        """
        Initialize the AddRelationshipCommand.

        Parameters:
            uml_model: The UML model containing the classes.
            source_class (str): The name of the source class.
            dest_class (str): The name of the destination class.
            rel_type (str): The type of the relationship.
            view: The GUI view, if applicable.
            class_box: The UMLClassBox instance representing the source class in the GUI.
            is_gui (bool): Indicates if the command is for the GUI.
        """
        super().__init__()
        self.uml_model = uml_model
        self.source_class = source_class
        self.dest_class = dest_class
        self.rel_type = rel_type
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui
        self.arrow_line = None  # Will be set during execution

    def execute(self, is_undo_or_redo=False):
        """
        Execute the add relationship command, adding the relationship to the model and GUI.

        Parameters:
            is_undo_or_redo (bool): Indicates if the execution is part of an undo or redo operation.

        Returns:
            bool: True if the relationship was added successfully, False otherwise.
        """
        is_relationship_added = self.uml_model._add_relationship(
            self.source_class,
            self.dest_class,
            self.rel_type,
            is_gui=self.is_gui,
            is_undo_or_redo=is_undo_or_redo
        )
        if is_relationship_added and self.is_gui:
            self.class_box.is_source_class = True
            source_class_obj = self.class_box
            dest_class_obj = self.view.class_name_list[self.dest_class]

            # Remove existing arrow if any
            existing_arrow = next((arrow for arrow in self.class_box.arrow_line_list if arrow.dest_class == self.dest_class), None)
            if existing_arrow:
                self.view.scene().removeItem(existing_arrow)
                self.class_box.arrow_line_list.remove(existing_arrow)

            # Create the arrow line between the GUI components
            self.arrow_line = ArrowLine(source_class_obj, dest_class_obj, self.rel_type)

            # Track the relationship in the view
            value = {"dest_class": self.dest_class, "arrow_list": self.arrow_line}
            if self.source_class not in self.view.relationship_track_list:
                self.view.relationship_track_list[self.source_class] = []
            self.view.relationship_track_list[self.source_class].append(value)

            # Add the arrow to the scene to display it
            self.view.scene().addItem(self.arrow_line)
            self.class_box.update_box()
        return is_relationship_added

    def undo(self):
        """
        Undo the add relationship command, removing the relationship from the model and GUI.

        Returns:
            bool: True if the undo was successful, False otherwise.
        """
        is_relationship_deleted = self.uml_model._delete_relationship(
            self.source_class,
            self.dest_class,
            is_undo_or_redo=True
        )
        if is_relationship_deleted and self.is_gui:
            relationships = self.view.relationship_track_list.get(self.source_class)
            for relationship in relationships:
                if relationship["dest_class"] != self.dest_class:
                    continue
                arrow_line = relationship["arrow_list"]
                if arrow_line.scene() == self.view.scene():
                    self.view.scene().removeItem(arrow_line)
                relationships.remove(relationship)
                break

            if len(self.view.relationship_track_list.get(self.source_class)) == 0:
                self.class_box.is_source_class = False
        return is_relationship_deleted

class DeleteRelationshipCommand(Command):
    """
    Command to delete a relationship between two UML classes in the model and GUI.

    This command encapsulates the action of deleting a relationship.
    It can be undone to restore the relationship.
    """

    def __init__(self, uml_model, source_class, dest_class, view=None, class_box=None, is_gui=False):
        """
        Initialize the DeleteRelationshipCommand.

        Parameters:
            uml_model: The UML model containing the classes.
            source_class (str): The name of the source class.
            dest_class (str): The name of the destination class.
            view: The GUI view, if applicable.
            class_box: The UMLClassBox instance representing the source class in the GUI.
            is_gui (bool): Indicates if the command is for the GUI.
        """
        super().__init__()
        self.uml_model = uml_model
        self.source_class = source_class
        self.dest_class = dest_class
        self.rel_type = None  # Will be set during execution
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui
        self.arrow_line = None  # Will be set during undo if needed

    def execute(self, is_undo_or_redo=False):
        """
        Execute the delete relationship command, removing the relationship from the model and GUI.

        Parameters:
            is_undo_or_redo (bool): Indicates if the execution is part of an undo or redo operation.

        Returns:
            bool: True if the relationship was deleted successfully, False otherwise.
        """
        self.rel_type = self.uml_model._get_rel_type(self.source_class, self.dest_class)
        is_relationship_deleted = self.uml_model._delete_relationship(
            self.source_class,
            self.dest_class,
            is_undo_or_redo=is_undo_or_redo
        )
        if is_relationship_deleted and self.is_gui:
            relationships = self.view.relationship_track_list.get(self.source_class)
            for relationship in relationships:
                if relationship["dest_class"] != self.dest_class:
                    continue
                arrow_line = relationship["arrow_list"]
                if arrow_line.scene() == self.view.scene():
                    self.view.scene().removeItem(arrow_line)
                relationships.remove(relationship)
                break

            if len(self.view.relationship_track_list.get(self.source_class)) == 0:
                self.class_box.is_source_class = False
        return is_relationship_deleted

    def undo(self):
        """
        Undo the delete relationship command, restoring the relationship in the model and GUI.

        Returns:
            bool: True if the undo was successful, False otherwise.
        """
        if self.rel_type:
            is_relationship_added = self.uml_model._add_relationship(
                self.source_class,
                self.dest_class,
                self.rel_type,
                is_gui=False,
                is_undo_or_redo=True
            )
            if is_relationship_added and self.is_gui:
                self.class_box.is_source_class = True
                source_class_obj = self.class_box
                dest_class_obj = self.view.class_name_list[self.dest_class]

                # Create the arrow line between the GUI components
                self.arrow_line = ArrowLine(source_class_obj, dest_class_obj, self.rel_type)

                # Track the relationship in the view
                value = {"dest_class": self.dest_class, "arrow_list": self.arrow_line}
                if self.source_class not in self.view.relationship_track_list:
                    self.view.relationship_track_list[self.source_class] = []
                self.view.relationship_track_list[self.source_class].append(value)

                # Add the arrow to the scene to display it
                self.view.scene().addItem(self.arrow_line)
                self.class_box.update_box()
            return is_relationship_added
        return False

class ChangeTypeCommand(Command):
    """
    Command to change the data type of a field, method return type, parameter type, or relationship type.

    This command encapsulates changing types in various elements of the UML model and GUI.
    It can be undone to restore the original types.
    """

    def __init__(self, uml_model,
                 class_name: str = None, method_num: int = None,
                 input_name: str = None, source_class: str = None,
                 dest_class: str = None, new_type: str = None, arrow_line=None,
                 is_field: bool = None, is_method: bool = None,
                 is_param: bool = None, is_rel: bool = None,
                 view=None, class_box=None, is_gui=False):
        """
        Initialize the ChangeTypeCommand.

        Parameters:
            uml_model: The UML model containing the elements to change.
            class_name (str): The name of the class containing the element.
            method_num (int): The index number of the method (if applicable).
            input_name (str): The name of the field or parameter.
            source_class (str): The source class name (for relationships).
            dest_class (str): The destination class name (for relationships).
            new_type (str): The new type to set.
            arrow_line: The arrow line object in the GUI (for relationships).
            is_field (bool): True if changing a field type.
            is_method (bool): True if changing a method return type.
            is_param (bool): True if changing a parameter type.
            is_rel (bool): True if changing a relationship type.
            view: The GUI view, if applicable.
            class_box: The UMLClassBox instance representing the class in the GUI.
            is_gui (bool): Indicates if the command is for the GUI.
        """
        self.uml_model = uml_model
        self.class_name = class_name
        self.method_num = method_num
        self.input_name = input_name
        self.source_class = source_class
        self.dest_class = dest_class
        self.new_type = new_type
        self.arrow_line = arrow_line
        self.class_box = class_box
        self.view = view
        self.is_field = is_field
        self.is_method = is_method
        self.is_param = is_param
        self.is_rel = is_rel
        self.original_field_type = None  # Will be set during execution
        self.original_method_type = None
        self.original_param_type = None
        self.original_rel_type = None
        self.is_gui = is_gui

    def execute(self, is_undo_or_redo=False):
        """
        Execute the change type command, changing the type in the model and GUI.

        Parameters:
            is_undo_or_redo (bool): Indicates if the execution is part of an undo or redo operation.

        Returns:
            bool: True if the type was changed successfully, False otherwise.
        """
        # Determine which element's type is being changed: field, method, parameter, or relationship
        if self.is_field:
            # Handle changing the data type of a field
            chosen_field = self.uml_model._get_chosen_field_or_method(self.class_name, self.input_name, is_field=True)
            if chosen_field is not None:
                # Store the original field type for undo
                self.original_field_type = chosen_field._get_type()
                # Change the field's data type in the model
                is_field_type_changed = self.uml_model._change_data_type(
                    class_name=self.class_name,
                    input_name=self.input_name,
                    new_type=self.new_type,
                    is_field=True,
                    is_undo_or_redo=is_undo_or_redo
                )
                if is_field_type_changed and self.is_gui:
                    # Update the field in the GUI
                    for index, field_key in enumerate(self.class_box.field_key_list):
                        if field_key[1] != self.input_name:
                            continue
                        # Store the position for re-insertion
                        self.position = index
                        # Remove the old field from the name list and scene
                        self.class_box.field_key_list.remove(field_key)
                        self.class_box.scene().removeItem(self.class_box.field_list.pop(field_key))
                    # Create a new text item with the updated type
                    field_text = self.class_box.create_text_item(
                        f"{self.new_type} {self.input_name}",
                        is_field=True,
                        selectable=False,
                        color=self.class_box.text_color
                    )
                    # Update the internal field lists with the new field
                    field_key = (self.new_type, self.input_name)
                    self.class_box.field_list[field_key] = field_text
                    self.class_box.field_key_list.insert(self.position, field_key)
                    # Refresh the UML box to reflect changes
                    self.class_box.update_box()
                return is_field_type_changed

        elif self.is_method:
            # Handle changing the return type of a method
            chosen_method = self.uml_model._get_method_based_on_index(self.class_name, self.method_num)
            if chosen_method is not None:
                # Store the original method return type for undo
                self.original_method_type = chosen_method._get_type()
                # Change the method's return type in the model
                is_method_return_type_changed = self.uml_model._change_data_type(
                    class_name=self.class_name,
                    method_num=self.method_num,
                    new_type=self.new_type,
                    is_method=True,
                    is_undo_or_redo=is_undo_or_redo
                )
                if is_method_return_type_changed and self.is_gui:
                    # Update the method in the GUI
                    method_entry = self.class_box.method_list[int(self.method_num) - 1]
                    # Remove the old method's text item from the scene
                    if method_entry["method_text"].scene() == self.view.scene():
                        self.view.scene().removeItem(method_entry["method_text"])
                    # Remove the old method entry from the method list
                    self.class_box.method_list.pop(int(self.method_num) - 1)
                    method_key = method_entry["method_key"]
                    current_param_list = method_entry["parameters"]
                    # Create a new method text item with the updated return type
                    new_method_text = self.class_box.create_text_item(
                        f"{self.new_type} {method_key[1]}()",
                        is_method=True,
                        selectable=False,
                        color=self.class_box.text_color
                    )
                    # Create a new method entry with the updated type
                    new_method_key = (self.new_type, method_key[1])
                    method_entry = {
                        "method_key": new_method_key,
                        "method_text": new_method_text,
                        "parameters": current_param_list
                    }
                    # Insert the updated method entry back into the method list
                    self.class_box.method_list.insert(int(self.method_num) - 1, method_entry)
                    # Add separators if needed
                    if len(self.class_box.method_list) == 1:
                        self.class_box.create_separator(is_first=False, is_second=True)
                    # Refresh the UML box to reflect changes
                    self.class_box.update_box()
                return is_method_return_type_changed

        elif self.is_param:
            # Handle changing the data type of a parameter
            chosen_param = self.uml_model._get_param_based_on_index(self.class_name, self.method_num, self.input_name)
            if chosen_param is None:
                return False
            # Store the original parameter type for undo
            self.original_param_type = chosen_param._get_type()
            # Change the parameter's data type in the model
            is_param_type_changed = self.uml_model._change_data_type(
                class_name=self.class_name,
                method_num=self.method_num,
                input_name=self.input_name,
                new_type=self.new_type,
                is_param=True,
                is_undo_or_redo=is_undo_or_redo
            )
            if is_param_type_changed and self.is_gui:
                # Update the parameter in the GUI
                method_entry = self.class_box.method_list[int(self.method_num) - 1]
                for i, param_tuple in enumerate(method_entry["parameters"]):
                    if param_tuple[1] != self.input_name:
                        continue
                    # Replace the parameter type with the new type
                    method_entry["parameters"][i] = (self.new_type, param_tuple[1])
                    break  # Exit after updating
                # Refresh the UML box to reflect changes
                self.class_box.update_box()
            return is_param_type_changed

        elif self.is_rel:
            # Handle changing the type of a relationship
            # Store the original relationship type for undo
            self.original_rel_type = self.uml_model._get_rel_type(self.source_class, self.dest_class)
            # Change the relationship type in the model
            is_rel_type_changed = self.uml_model._change_data_type(
                source_class=self.source_class,
                dest_class=self.dest_class,
                new_type=self.new_type,
                is_rel=True,
                is_undo_or_redo=is_undo_or_redo
            )
            if is_rel_type_changed and self.is_gui:
                # Update the relationship in the GUI
                relationships = self.view.relationship_track_list.get(self.source_class)
                for relationship in relationships:
                    if relationship["dest_class"] != self.dest_class:
                        continue
                    arrow_line = relationship["arrow_list"]
                    # Remove the old arrow line from the scene
                    if arrow_line.scene() == self.view.scene():
                        self.view.scene().removeItem(arrow_line)
                    relationships.remove(relationship)
                    break
                if len(self.view.relationship_track_list.get(self.source_class)) == 0:
                    self.class_box.is_source_class = False

                # Create a new arrow line with the updated type
                source_class_obj = self.class_box
                dest_class_obj = self.view.class_name_list[self.dest_class]
                self.arrow_line = ArrowLine(source_class_obj, dest_class_obj, self.new_type)
                # Track the updated relationship in the view
                value = {"dest_class": self.dest_class, "arrow_list": self.arrow_line}
                if self.source_class not in self.view.relationship_track_list:
                    self.view.relationship_track_list[self.source_class] = []
                self.view.relationship_track_list[self.source_class].append(value)
                # Add the new arrow line to the scene
                self.view.scene().addItem(self.arrow_line)
                # Refresh the UML box to reflect changes
                self.class_box.update_box()
            return is_rel_type_changed

        # Return False if none of the conditions were met
        return False

    def undo(self):
        """
        Undo the change type command, restoring the original type.

        Returns:
            bool: True if the undo was successful, False otherwise.
        """
        # Restore the original type based on which element was changed
        if self.is_field and self.original_field_type:
            # Handle restoring the data type of a field
            chosen_field = self.uml_model._get_chosen_field_or_method(self.class_name, self.input_name, is_field=True)
            if chosen_field is not None:
                # Change the field's data type back to the original type in the model
                is_field_type_changed = self.uml_model._change_data_type(
                    class_name=self.class_name,
                    input_name=self.input_name,
                    new_type=self.original_field_type,
                    is_field=True,
                    is_undo_or_redo=True
                )
                if is_field_type_changed and self.is_gui:
                    # Update the field in the GUI
                    for index, field_key in enumerate(self.class_box.field_key_list):
                        if field_key[1] != self.input_name:
                            continue
                        # Store the position for re-insertion
                        self.position = index
                        # Remove the updated field from the name list and scene
                        self.class_box.field_key_list.remove(field_key)
                        popped_item = self.class_box.field_list.pop(field_key)
                        if popped_item.scene() == self.view.scene():
                            self.class_box.scene().removeItem(popped_item)
                    # Create a new text item with the original type
                    field_text = self.class_box.create_text_item(
                        f"{self.original_field_type} {self.input_name}",
                        is_field=True,
                        selectable=False,
                        color=self.class_box.text_color
                    )
                    # Update the internal field lists with the original field
                    field_key = (self.original_field_type, self.input_name)
                    self.class_box.field_list[field_key] = field_text
                    self.class_box.field_key_list.insert(self.position, field_key)
                    # Refresh the UML box to reflect changes
                    self.class_box.update_box()
                return is_field_type_changed

        elif self.is_method and self.original_method_type:
            # Handle restoring the return type of a method
            chosen_method = self.uml_model._get_method_based_on_index(self.class_name, self.method_num)
            if chosen_method is not None:
                # Change the method's return type back to the original type in the model
                is_method_return_type_changed = self.uml_model._change_data_type(
                    class_name=self.class_name,
                    method_num=self.method_num,
                    new_type=self.original_method_type,
                    is_method=True,
                    is_undo_or_redo=True
                )
                if is_method_return_type_changed and self.is_gui:
                    # Update the method in the GUI
                    method_entry = self.class_box.method_list[int(self.method_num) - 1]
                    # Remove the updated method's text item from the scene
                    if method_entry["method_text"].scene() == self.view.scene():
                        self.view.scene().removeItem(method_entry["method_text"])
                    # Remove the updated method entry from the method list
                    self.class_box.method_list.pop(int(self.method_num) - 1)
                    method_key = method_entry["method_key"]
                    current_param_list = method_entry["parameters"]
                    # Create a new method text item with the original return type
                    new_method_text = self.class_box.create_text_item(
                        f"{self.original_method_type} {method_key[1]}()",
                        is_method=True,
                        selectable=False,
                        color=self.class_box.text_color
                    )
                    # Create a new method entry with the original type
                    new_method_key = (self.original_method_type, method_key[1])
                    method_entry = {
                        "method_key": new_method_key,
                        "method_text": new_method_text,
                        "parameters": current_param_list
                    }
                    # Insert the restored method entry back into the method list
                    self.class_box.method_list.insert(int(self.method_num) - 1, method_entry)
                    # Add separators if needed
                    if len(self.class_box.method_list) == 1:
                        self.class_box.create_separator(is_first=False, is_second=True)
                    # Refresh the UML box to reflect changes
                    self.class_box.update_box()
                return is_method_return_type_changed

        elif self.is_param and self.original_param_type:
            # Handle restoring the data type of a parameter
            # Change the parameter's data type back to the original type in the model
            is_param_type_changed = self.uml_model._change_data_type(
                class_name=self.class_name,
                method_num=self.method_num,
                input_name=self.input_name,
                new_type=self.original_param_type,
                is_param=True,
                is_undo_or_redo=True
            )
            if is_param_type_changed and self.is_gui:
                # Update the parameter in the GUI
                method_entry = self.class_box.method_list[int(self.method_num) - 1]
                for i, param_tuple in enumerate(method_entry["parameters"]):
                    if param_tuple[1] != self.input_name:
                        continue
                    # Restore the parameter type to the original type
                    method_entry["parameters"][i] = (self.original_param_type, param_tuple[1])
                    break
                # Refresh the UML box to reflect changes
                self.class_box.update_box()
            return is_param_type_changed

        elif self.is_rel and self.original_rel_type:
            # Handle restoring the type of a relationship
            # Change the relationship type back to the original type in the model
            is_rel_type_changed = self.uml_model._change_data_type(
                source_class=self.source_class,
                dest_class=self.dest_class,
                new_type=self.original_rel_type,
                is_rel=True,
                is_undo_or_redo=True
            )
            if is_rel_type_changed and self.is_gui:
                # Update the relationship in the GUI
                relationships = self.view.relationship_track_list.get(self.source_class)
                for relationship in relationships:
                    if relationship["dest_class"] != self.dest_class:
                        continue
                    arrow_line = relationship["arrow_list"]
                    # Remove the updated arrow line from the scene
                    if arrow_line.scene() == self.view.scene():
                        self.view.scene().removeItem(arrow_line)
                    relationships.remove(relationship)
                    break

                if len(self.view.relationship_track_list.get(self.source_class)) == 0:
                    self.class_box.is_source_class = False

                # Create a new arrow line with the original type
                source_class_obj = self.class_box
                dest_class_obj = self.view.class_name_list[self.dest_class]
                self.arrow_line = ArrowLine(source_class_obj, dest_class_obj, self.original_rel_type)
                # Track the restored relationship in the view
                value = {"dest_class": self.dest_class, "arrow_list": self.arrow_line}
                if self.source_class not in self.view.relationship_track_list:
                    self.view.relationship_track_list[self.source_class] = []
                self.view.relationship_track_list[self.source_class].append(value)
                # Add the restored arrow line to the scene
                self.view.scene().addItem(self.arrow_line)
                # Refresh the UML box to reflect changes
                self.class_box.update_box()
                return is_rel_type_changed

        # Return False if none of the conditions were met
        return False

class InputHandler:
    """
    Handles the execution of commands and manages the undo/redo stack.

    This class maintains a list of executed commands and a pointer to the current position.
    It provides methods to execute commands, undo, and redo actions.
    """

    def __init__(self):
        """
        Initialize the InputHandler.

        Attributes:
            command_list (list): The list of executed commands.
            pointer (int): The index of the current command in the command_list.
        """
        self.command_list = []
        self.pointer = -1  # Start before the first command

    def execute_command(self, command):
        """
        Execute a new command and add it to the command list.

        Parameters:
            command (Command): The command to execute.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        # Clear all commands after the current pointer position (for redo)
        del self.command_list[self.pointer + 1:]
        # Execute the new command
        is_command_valid = command.execute()
        if not is_command_valid:
            return False
        # Add the command to the list and increment the pointer
        self.command_list.append(command)
        self.pointer += 1
        return True

    def undo(self):
        """
        Undo the last executed command.

        Moves the pointer back and calls undo on the current command.
        """
        if self.pointer >= 0:
            # Retrieve the current command
            command = self.command_list[self.pointer]
            # Undo the command
            command.undo()
            # Move the pointer back
            self.pointer -= 1

    def redo(self):
        """
        Redo the last undone command.

        Moves the pointer forward and calls execute on the current command.
        """
        if self.pointer < len(self.command_list) - 1:
            # Move the pointer forward
            self.pointer += 1
            # Retrieve the command to redo
            command = self.command_list[self.pointer]
            # Execute the command again
            command.execute(is_undo_or_redo=True)