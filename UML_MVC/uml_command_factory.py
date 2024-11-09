from UML_MVC import uml_command_pattern as Command
from UML_ENUM_CLASS.uml_enum import InterfaceOptions as CommandType

class CommandFactory:
    """
    Factory class to create command objects based on command names.

    This class encapsulates the creation of command objects for various UML operations.
    It uses the command pattern to create instances of command classes that can be executed,
    undone, or redone by the application.

    Attributes:
        uml_model: The UML model instance where the commands will operate.
        view: The GUI view, if applicable.
        class_box: The UMLClassBox instance representing the class in the GUI.
        is_gui (bool): Indicates if the commands are for the GUI.
    """

    def __init__(self, uml_model, view=None, class_box=None, is_gui=False):
        """
        Initialize the CommandFactory.

        Parameters:
            uml_model: The UML model instance where the commands will operate.
            view: The GUI view, if applicable.
            class_box: The UMLClassBox instance representing the class in the GUI.
            is_gui (bool): Indicates if the commands are for the GUI.
        """
        self.uml_model = uml_model
        self.view = view
        self.class_box = class_box
        self.is_gui = is_gui

    def create_command(
        self, command_name: str, class_name=None, input_name=None,
        old_x=None, old_y=None, new_x=None, new_y=None, new_name=None,
        old_name=None, field_type=None, method_type=None,
        method_num=None, param_type=None, selected_param_index=None,
        new_param_list_obj=None, new_param_list_str=None,
        source_class=None, dest_class=None,
        rel_type=None, new_type=None, arrow_line=None
    ) -> Command:
        """
        Create a command object based on the provided command name and parameters.

        Parameters:
            command_name (str): The name of the command to create.
            class_name (str, optional): The name of the class involved in the command.
            input_name (str, optional): The name of the field, method, or parameter.
            old_x (float, optional): The original x-coordinate (for move commands).
            old_y (float, optional): The original y-coordinate (for move commands).
            new_x (float, optional): The new x-coordinate (for move commands).
            new_y (float, optional): The new y-coordinate (for move commands).
            new_name (str, optional): The new name for rename commands.
            old_name (str, optional): The old name for rename commands.
            field_type (str, optional): The type of the field.
            method_type (str, optional): The return type of the method.
            method_num (str, optional): The index number of the method.
            param_type (str, optional): The type of the parameter.
            selected_param_index (int, optional): The index of the parameter in the parameter list.
            new_param_list_obj (list, optional): The new parameter list as objects.
            new_param_list_str (list, optional): The new parameter list as strings.
            source_class (str, optional): The source class name (for relationships).
            dest_class (str, optional): The destination class name (for relationships).
            rel_type (str, optional): The type of the relationship.
            new_type (str, optional): The new type for change type commands.
            arrow_line: The arrow line object in the GUI (for relationships).

        Returns:
            Command: An instance of a command class corresponding to the command name.

        Raises:
            ValueError: If an unknown command name is provided.
        """
        # Check the command name and create the appropriate command object
        if command_name == CommandType.MOVE_UNIT.value:
            # Create a MoveUnitCommand to move a class box
            return Command.MoveUnitCommand(
                class_box=self.class_box,
                old_x=old_x,
                old_y=old_y,
                new_x=new_x,
                new_y=new_y
            )
        elif command_name == CommandType.ADD_CLASS.value:
            # Create an AddClassCommand to add a new class
            return Command.AddClassCommand(
                class_name=class_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.DELETE_CLASS.value:
            # Create a DeleteClassCommand to delete a class
            return Command.DeleteClassCommand(
                class_name=class_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.RENAME_CLASS.value:
            # Create a RenameClassCommand to rename a class
            return Command.RenameClassCommand(
                class_name=class_name,
                new_name=new_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.ADD_FIELD.value:
            # Create an AddFieldCommand to add a field to a class
            return Command.AddFieldCommand(
                class_name=class_name,
                type=field_type,
                field_name=input_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.DELETE_FIELD.value:
            # Create a DeleteFieldCommand to delete a field from a class
            return Command.DeleteFieldCommand(
                class_name=class_name,
                field_name=input_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.RENAME_FIELD.value:
            # Create a RenameFieldCommand to rename a field in a class
            return Command.RenameFieldCommand(
                class_name=class_name,
                old_field_name=old_name,
                new_field_name=new_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.ADD_METHOD.value:
            # Create an AddMethodCommand to add a method to a class
            return Command.AddMethodCommand(
                class_name=class_name,
                type=method_type,
                method_name=input_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.DELETE_METHOD.value:
            # Create a DeleteMethodCommand to delete a method from a class
            return Command.DeleteMethodCommand(
                class_name=class_name,
                method_num=method_num,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.RENAME_METHOD.value:
            # Create a RenameMethodCommand to rename a method in a class
            return Command.RenameMethodCommand(
                class_name=class_name,
                method_num=method_num,
                new_name=new_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.ADD_PARAM.value:
            # Create an AddParameterCommand to add a parameter to a method
            return Command.AddParameterCommand(
                class_name=class_name,
                method_num=method_num,
                param_type=param_type,
                param_name=input_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.DELETE_PARAM.value:
            # Create a DeleteParameterCommand to delete a parameter from a method
            return Command.DeleteParameterCommand(
                class_name=class_name,
                method_num=method_num,
                selected_param_index=selected_param_index,
                param_name=input_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.RENAME_PARAM.value:
            # Create a RenameParameterCommand to rename a parameter in a method
            return Command.RenameParameterCommand(
                class_name=class_name,
                method_num=method_num,
                old_param_name=old_name,
                new_param_name=new_name,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.REPLACE_PARAM.value:
            # Create a ReplaceParameterListCommand to replace parameters in a method
            return Command.ReplaceParameterListCommand(
                class_name=class_name,
                method_num=method_num,
                new_param_list_obj=new_param_list_obj,
                new_param_list_str=new_param_list_str,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.ADD_REL.value:
            # Create an AddRelationshipCommand to add a relationship between classes
            return Command.AddRelationshipCommand(
                source_class=source_class,
                dest_class=dest_class,
                rel_type=rel_type,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.DELETE_REL.value:
            # Create a DeleteRelationshipCommand to delete a relationship between classes
            return Command.DeleteRelationshipCommand(
                source_class=source_class,
                dest_class=dest_class,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.EDIT_FIELD_TYPE.value:
            # Create a ChangeTypeCommand to change the type of a field
            return Command.ChangeTypeCommand(
                class_name=class_name,
                input_name=input_name,
                new_type=new_type,
                is_field=True,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.EDIT_METHOD_TYPE.value:
            # Create a ChangeTypeCommand to change the return type of a method
            return Command.ChangeTypeCommand(
                class_name=class_name,
                method_num=method_num,
                new_type=new_type,
                is_method=True,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.EDIT_PARAM_TYPE.value:
            # Create a ChangeTypeCommand to change the type of a parameter
            return Command.ChangeTypeCommand(
                class_name=class_name,
                method_num=method_num,
                input_name=input_name,
                new_type=new_type,
                is_param=True,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        elif command_name == CommandType.EDIT_REL_TYPE.value:
            # Create a ChangeTypeCommand to change the type of a relationship
            return Command.ChangeTypeCommand(
                source_class=source_class,
                dest_class=dest_class,
                new_type=new_type,
                arrow_line=arrow_line,
                is_rel=True,
                uml_model=self.uml_model,
                view=self.view,
                class_box=self.class_box,
                is_gui=self.is_gui,
            )
        else:
            # Raise an error if an unknown command name is provided
            raise ValueError(f"Unknown command name: {command_name}")
